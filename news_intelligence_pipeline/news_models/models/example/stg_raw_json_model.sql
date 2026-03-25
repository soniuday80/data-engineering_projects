{{ config(
    materialized='view',
    schema='staging'
) }}

WITH source AS (
    SELECT *
    FROM {{ source('NEWS_INTELLIGENCE_DB', 'RAW_NEWS') }}
),

parsed AS (
    SELECT
        id as article_id,
        loaded_at,
        
        
         {{ cleanse_html_tags(RAW_DATA:author::VARCHAR) }} AS author,
         {{ cleanse_html_tags(RAW_DATA:title::VARCHAR) }} AS title,
         {{ RAW_DATA:'url'::CAST(url AS VARCHAR) }} AS url,
         {{ RAW_DATA:publish_at::DATETIME }} AS published,
         {{ cleanse_html_tags(RAW_DATA:content::VARCHAR) }} AS content
        
        -- Handle missing/null values
        CASE 
            WHEN json_data:timestamp IS NOT NULL 
            THEN json_data:timestamp::TIMESTAMP 
            ELSE NULL 
        END AS event_timestamp,
        
        
    FROM source
)

SELECT * FROM parsed