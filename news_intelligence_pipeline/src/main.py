import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

load_dotenv()


app = FastAPI()


model = SentenceTransformer("Snowflake/snowflake-arctic-embed-m")
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index = pc.Index("news")


class SearchRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    title: str
    url: str
    score: float


@app.get("/search", response_model=list[SearchResponse])
def search(query: str):

    
    query_vector = model.encode(query, prompt_name="query").tolist()

    
    results = index.query(
        vector=query_vector,
        top_k=4,
        include_metadata=True
    )


    
   

    filtered = [match for match in results.matches if match.score >= 0.1] # lowered the score 
    print("Filtered:", filtered) 


    return [
        SearchResponse(
            title=match.metadata['title'],
            url=match.metadata['url'],
            score=match.score
        )
        for match in filtered
    ]