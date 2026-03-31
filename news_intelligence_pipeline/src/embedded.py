import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import snowflake.connector
import pandas as pd
from sentence_transformers import SentenceTransformer

load_dotenv()


print("Connecting to Snowflake...")
conn = snowflake.connector.connect(
    user=os.getenv('TF_VAR_snowflake_username'),
    password=os.getenv('TF_VAR_snowflake_password'),
    account=os.getenv('snowflake_org-account'),
    warehouse='NEWS_INGESTION_WH',
    database='NEWS_INTELLIGENCE_DB',
    schema='DATA_SCHEMA_INTERMEDIATE'
)


print("Fetching data...")
cursor = conn.cursor()
cursor.execute("SELECT * FROM FCT_NEWS")
rows = cursor.fetchall()
col_names = [desc[0].lower() for desc in cursor.description]
df = pd.DataFrame(rows, columns=col_names)
cursor.close()
conn.close()
print(f"Fetched {len(df)} rows")


def chunk_text(text, chunk_size=400, overlap=50):
    sentences = text.split('. ')
    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        words = sentence.split()
        current_length += len(words)
        current_chunk.append(sentence)

        if current_length >= chunk_size:
            chunks.append('. '.join(current_chunk))
            current_chunk = [current_chunk[-1]]
            current_length = len(current_chunk[0].split())

    if current_chunk:
        chunks.append('. '.join(current_chunk))

    return chunks


print("Loading embedding model...")
model = SentenceTransformer("Snowflake/snowflake-arctic-embed-m")

print("Embedding chunks...")
vectors = []
for _, row in df.iterrows():
    chunks = chunk_text(row['content'])
    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk, prompt_name="document")
        vectors.append({
            "id": f"{row['article_id']}_chunk_{i}",
            "values": embedding.tolist(),
            "metadata": {
                "title": row['title'],
                "url": row['url'],
                "content": chunk,
                "article_id": str(row['article_id'])
            }
        })

print(f"Total chunks to upsert: {len(vectors)}")


print("Connecting to Pinecone...")
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

if "news" not in pc.list_indexes().names():
    pc.create_index(
        name="news",
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

index = pc.Index("news")


print("Upserting to Pinecone...")
batch_size = 100
for i in range(0, len(vectors), batch_size):
    batch = vectors[i:i + batch_size]
    index.upsert(vectors=batch)
    print(f"Upserted batch {i//batch_size + 1} of {len(vectors)//batch_size + 1}")

print("Done!")
