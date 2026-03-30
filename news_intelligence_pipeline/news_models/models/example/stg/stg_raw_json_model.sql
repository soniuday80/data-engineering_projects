{{ config(
    materialized='view',
    schema='staging'
) }}

WITH source AS (
    SELECT 
        ID as article_id,
        LOADED_AT as loaded_at,
        RAW_DATA
    FROM {{ source('NEWS_INTELLIGENCE_DB', 'RAW_NEWS') }}
),

parsed AS (
    SELECT
        article_id,
        loaded_at,
        
        {{ cleanse_html_tags('RAW_DATA:author::VARCHAR') }} AS author,
        {{ cleanse_html_tags('RAW_DATA:title::VARCHAR') }} AS title,
        RAW_DATA:url::VARCHAR AS url,
        RAW_DATA:publishedAt::TIMESTAMP AS published,
        {{ cleanse_html_tags('RAW_DATA:content::VARCHAR') }} AS content,
        
        CASE 
            WHEN RAW_DATA:timestamp IS NOT NULL 
            THEN RAW_DATA:timestamp::TIMESTAMP 
            ELSE NULL 
        END AS event_timestamp
        
    FROM source
)

SELECT * FROM parsed