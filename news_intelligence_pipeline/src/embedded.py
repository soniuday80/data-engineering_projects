import os
import dotenv
import pinecone
import snowflake.connector
import pandas as pd
from sentence_transformers import SentenceTransformer

dotenv.load_dotenv()
pc = pinecone.Pinecone(api_key=os.environ.get("pinecone_API_KEY"))

conn = snowflake.connector.connect(
    user= os.environ.get("TF_VAR_snowflake_username"),
    password=os.environ.get("TF_VAR_snowflake_password"),
    account=os.environ.get("snowflake_org-account"),  # e.g., 'xy12345.us-east-1'
    warehouse='NEWS_INGESTION_WH',
    database='NEWS_INTELLIGENCE_DB',
    schema='DATA_SCHEMA'
)
