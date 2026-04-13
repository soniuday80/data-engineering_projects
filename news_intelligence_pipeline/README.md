# News Intelligence RAG Pipeline 🚀

An end-to-end semantic news search pipeline that ingests live news articles, transforms them, embeds them using state-of-the-art sentence transformers, and serves intelligent search results via a FastAPI endpoint.

## Architecture

```
NewsAPI.org → Snowflake → DBT → Python Ingestion → Pinecone → FastAPI
                                      ↑
                               Terraform (Infra)
                               Airflow (Orchestration)
                               Docker (Containerization)
```

## How It Works

1. News articles are fetched from NewsAPI.org and stored raw in Snowflake
2. DBT transforms and deduplicates the raw articles into a clean `fct_news` table
3. Articles are semantically chunked (400 token chunks with 50 token overlap) to respect model token limits
4. Each chunk is embedded using Snowflake Arctic Embed M (768 dimensions)
5. Embeddings are upserted into Pinecone vector database with metadata (title, url, content)
6. FastAPI endpoint accepts a search query, embeds it, and returns the most semantically similar articles from Pinecone

## Tech Stack

| Layer | Technology |
|-------|------------|
| Data Source | NewsAPI.org |
| Data Warehouse | Snowflake |
| Transformation | DBT |
| Infrastructure | Terraform |
| Embedding Model | Snowflake Arctic Embed M |
| Vector Database | Pinecone |
| API | FastAPI |
| Orchestration | Apache Airflow |
| Containerization | Docker |

## Project Structure

```
news_intelligence_pipeline/
├── dags/                          # Airflow DAG definitions
├── data/                          # Sample data for local testing
├── docs/                          # Screenshots and proof of work
├── infra/                         # Terraform files
│   ├── main.tf
│   └── variables.tf
├── news_models/                   # DBT project
│   ├── models/
│   │   └── example/
│   │       ├── fct_news.sql       # Main transformation model
│   │       └── schema.yml
│   └── macros/                    # Custom DBT macros (HTML cleansing)
├── src/
│   ├── embedded.py                # Chunking, embedding and Pinecone upsert
│   ├── main.py                    # FastAPI search endpoint
│   └── news.py                    # NewsAPI ingestion
├── dockerfile
├── docker-compose.yml
└── requirements.txt
```

## API Usage

Start the server:
```bash
cd src
uvicorn main:app --reload
```

Search endpoint:
```
GET /search?query=latest developments in AI
```

Response:
```json
[
  {
    "title": "Article title",
    "url": "https://...",
    "score": 0.87
  }
]
```

## Local Setup

1. Clone the repo
2. Create a `.env` file with your credentials:
```
PINECONE_API_KEY=your_key
TF_VAR_snowflake_username=your_username
TF_VAR_snowflake_password=your_password
SNOWFLAKE_ACCOUNT=your_account
NEWS_API_KEY=your_key
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Since Snowflake trial has expired, replace the Snowflake connection in `embedded.py` with:
```python
df = pd.read_csv("data/sample_news.csv")
```

5. Run ingestion:
```bash
python src/embedded.py
```

6. Start API:
```bash
cd src && uvicorn main:app --reload
```

## Database Preview

Screenshots of live Snowflake tables and Pinecone index are available in the `/docs` folder as proof of the pipeline running end to end.

## Orchestration and Containerization

Airflow DAG and Docker setup are included in the repo (`dags/`, `dockerfile`, `docker-compose.yml`). These were written after the Snowflake trial expired and have not been tested live. The DAG covers the following tasks:

```
snowflake_check → dbt_run → dbt_test → embed_and_upsert → pinecone_health_check
```

To run with Docker once Snowflake is available:
```bash
docker-compose up --build
```

## DBT Transformation

The DBT model handles deduplication of articles by content using a `ROW_NUMBER()` window function, and a custom macro `cleanse_html_tags` strips HTML entities and tags from raw article content before embedding.

## Key Design Decisions

- **Chunking strategy** — Articles average 7000 characters (~1500 tokens), exceeding the 512 token limit of Arctic Embed M. Fixed size chunking with overlap ensures no content is silently truncated.
- **Asymmetric search** — Arctic Embed M is designed for asymmetric search. `prompt_name="document"` is used at ingest time and `prompt_name="query"` at search time for best retrieval quality.
- **Score threshold** — Results below a similarity score of 0.1 are filtered out to avoid returning irrelevant matches.