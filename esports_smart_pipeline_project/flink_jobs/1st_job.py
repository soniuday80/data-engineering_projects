from pyflink.table import EnvironmentSettings, TableEnvironment

# 1. Setup the execution environment
settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
t_env = TableEnvironment.create(settings)

# 2. Create a dummy source (printing numbers 1 to 10)
t_env.execute_sql("""
    CREATE TEMPORARY TABLE source (
        word STRING
    ) WITH (
        'connector' = 'datagen',
        'number-of-rows' = '10'
    )
""")

# 3. Create a sink to print to the console (the TaskManager logs)
t_env.execute_sql("""
    CREATE TEMPORARY TABLE sink (
        word STRING
    ) WITH (
        'connector' = 'print'
    )
""")

# 4. Run the job
t_env.from_path("source").insert_into("sink")
t_env.execute("Esports Test Job")