-- players_stats.sql

CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE players_stats (
    player_id VARCHAR(50),
    player_name VARCHAR(100),
    kd_ratio FLOAT,
    gold_per_minute FLOAT,
    time TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

SELECT create_hypertable('players_stats', 'time');