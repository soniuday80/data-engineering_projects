from pyflink.table import EnvironmentSettings, TableEnvironment

# 1. Setup the execution environment
settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
t_env = TableEnvironment.create(settings)
# creating a table for the game events
t_env.execute_sql("""
    CREATE TABLE game_events (
        event_id        STRING,
        match_id        STRING,
        event_type      STRING,
        game_time       INT,
        player_id       STRING,       -- NULL for OBJECTIVE
        target_id       STRING,       -- only KILL
        gold_awarded    INT,          -- only KILL
        team            STRING,       -- only OBJECTIVE
        objective_type  STRING,       -- only OBJECTIVE
        item_id         STRING,       -- only ITEM_PURCHASE
        item_cost       INT,          -- only ITEM_PURCHASE
        ability_id      STRING,       -- only ABILITY_USED
        cooldown        INT           -- only ABILITY_USED
    ) WITH (
        'connector' = 'kafka',
        'topic'     = 'game-events',
        'format'    = 'json',
        'json.ignore-parse-errors' = 'true'   -- handles missing keys gracefully
    )
""")
# calculating the k/d
t_env.query_sql("""
    WITH kills AS (
    SELECT player_id,
           COUNT(*) AS total_kills
    FROM game_events
    WHERE event_type = 'KILL'
    GROUP BY player_id
),
deaths AS (
    SELECT target_id AS player_id,
           COUNT(*) AS total_deaths
    FROM game_events
    WHERE event_type = 'KILL'
    GROUP BY target_id
)
SELECT
    kills.player_id,
    kills.total_kills        AS kills,
    deaths.total_deaths      AS deaths,
    kills.total_kills / NULLIF(deaths.total_deaths, 0) AS kd_ratio
FROM kills
LEFT JOIN deaths
ON kills.player_id = deaths.player_id
""").execute()

# 4. Run the job
t_env.from_path("source").insert_into("sink")
t_env.execute("Esports Test Job")