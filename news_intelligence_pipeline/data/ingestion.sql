USE ROLE SYSADMIN;
USE WAREHOUSE NEWS_INGESTION_WH;
USE DATABASE "NEWS_INTELLIGENCE_DB";
USE SCHEMA "DATA_SCHEMA";

-- creating a table raw_news
CREATE OR REPLACE TABLE raw_news (
 id NUMBER AUTOINCREMENT PRIMARY KEY,
 raw_data VARIANT,
 loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);


-- creating a file format which hold json
 CREATE OR REPLACE FILE FORMAT pj_json_format
  TYPE = JSON;

--staging the data
CREATE OR REPLACE  STAGE news_stage
FILE_FORMAT = pj_json_format;

-- staging data
--PUT file://C:\Users\AYUSHREE\Desktop\data- engineering_projects\news_intelligence_pipeline\data\news_api_response.json  
--@NEWS_STAGE AUTO_COMPRESS = TRUE;

-- copying data into table
INSERT INTO RAW_NEWS (raw_data)
SELECT 
    VALUE AS raw_data
FROM 
    @NEWS_STAGE,
    LATERAL FLATTEN(INPUT => PARSE_JSON($1):articles); -- read the raw json and find articles explode it and put one by one as input
--checking the data 
SELECT * FROM RAW_NEWS;
