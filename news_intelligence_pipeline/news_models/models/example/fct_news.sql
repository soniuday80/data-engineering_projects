{{ config(
    materialized='table',
    schema='intermediate',
    tags=['intermediate']
) }}

WITH deduped AS (
    SELECT 
        article_id,
        title,
        url,
        content,
        ROW_NUMBER() OVER (
            PARTITION BY content  
            ORDER BY article_id 
        ) AS row_num
    FROM {{ ref('stg_raw_json_model') }}
)

SELECT 
    article_id,
    title,
    url,
    content
FROM deduped 
WHERE row_num = 1  -- Keep only unique content


