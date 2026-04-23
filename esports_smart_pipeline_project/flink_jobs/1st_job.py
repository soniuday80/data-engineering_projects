from pyflink.table import EnvironmentSettings, TableEnvironment
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
t_env = TableEnvironment.create(settings)

# Source: Read from Kafka # using kafka:29092 for docker, localhost:9092 for local
t_env.execute_sql("""
    CREATE TABLE game_events (
        event_id STRING,
        player_id STRING,
        event_type STRING,
        gold_awarded INT,
        game_time INT
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'match-events',
        'properties.bootstrap.servers' = 'kafka:29092',   
        'format' = 'json',
        'scan.startup.mode' = 'earliest-offset'
    )
""")

# Sink: Write to PostgreSQL/TimescaleDB
t_env.execute_sql(f"""
    CREATE TABLE players_stats_sink (
        player_id STRING,
        player_name STRING,
        kd_ratio DOUBLE,
        gold_per_minute DOUBLE
    ) WITH (
        'connector' = 'jdbc',
        'url' = 'jdbc:postgresql://timescale:5432/esports_db',
        'table-name' = 'players_stats',
        'username' = '{os.getenv("DB_USERNAME", "postgres")}',
        'password' = '{os.getenv("DB_PASSWORD", "postgres")}'
    )
""")

# Process: Calculate stats
result = t_env.sql_query("""
    SELECT 
        player_id,
        'Unknown' as player_name,
        COUNT(*) FILTER (WHERE event_type = 'KILL') * 1.0 / 
            NULLIF(COUNT(*) FILTER (WHERE event_type = 'DEATH'), 0) as kd_ratio,
        AVG(gold_awarded) as gold_per_minute
    FROM game_events
    GROUP BY player_id
""")

# Send to database
result.execute_insert("players_stats_sink")

# Run job
t_env.execute("Esports Pipeline")