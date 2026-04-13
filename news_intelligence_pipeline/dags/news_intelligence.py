import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

from news_intelligence_pipeline.src.embedded import embedding


def snowflake_check():
    # uses the SnowflakeHook to grab credentials from the Airflow connection
    # then runs a simple COUNT query to verify the connection is live and data exists
    from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
    hook = SnowflakeHook(snowflake_conn_id='snowflake_default')
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM FCT_NEWS") # optional: add a WHERE clause to check for recent data, e.g. WHERE published_at >= CURRENT_DATE - INTERVAL '7 days'
    count = cursor.fetchone()[0]

    if count == 0:
        raise Exception("FCT_NEWS table is empty — nothing to process.")
    else:
        print(f"Snowflake connection successful. {count} rows found in FCT_NEWS.")


def pinecone_health_check():
    # connects to Pinecone using the API key from environment variables
    # checks if the "news" index exists and has vectors in it
    # if index is empty it means the upsert failed so we raise an exception
    from pinecone import Pinecone
    pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

    if "news" not in pc.list_indexes().names():
        raise Exception("Pinecone index 'news' not found.")

    stats = pc.Index("news").describe_index_stats()
    if stats['total_vector_count'] == 0:
        raise Exception("Pinecone index is empty — upsert may have failed.")

    print(f"Pinecone health check passed. {stats['total_vector_count']} vectors found.")


with DAG(
    'news_intelligence_pipeline',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime(2024, 6, 1),
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    schedule_interval='@daily',
) as dag:

    # task 1 — verify Snowflake connection and data exists before running dbt
    snowflake_check_task = PythonOperator(
        task_id='snowflake_check',
        python_callable=snowflake_check
    )

    # task 2 — run dbt models to transform and deduplicate raw news articles into fct_news
    dbt_run_task = BashOperator(
        task_id='dbt_run',
        bash_command='dbt run --project-dir /opt/airflow/news_models --profiles-dir /opt/airflow/news_models'
    )

    # task 3 — run dbt tests to validate data quality before embedding
    # if tests fail the pipeline stops here and embed_and_upsert will not run
    dbt_test_task = BashOperator(
        task_id='dbt_test',
        bash_command='dbt test --project-dir /opt/airflow/news_models --profiles-dir /opt/airflow/news_models'
    )

    # task 4 — chunk articles, generate embeddings and upsert vectors into Pinecone
    # calls the run_embedding function from embedded.py
    embed_and_upsert_task = PythonOperator(
        task_id='embed_and_upsert',
        python_callable=embedding
    )

    # task 5 — verify Pinecone index exists and has vectors after upsert
    # acts as a sanity check to confirm the pipeline completed successfully
    pinecone_health_check_task = PythonOperator(
        task_id='pinecone_health_check',
        python_callable=pinecone_health_check
    )

    # pipeline flow
    snowflake_check_task >> dbt_run_task >> dbt_test_task >> embed_and_upsert_task >> pinecone_health_check_task


