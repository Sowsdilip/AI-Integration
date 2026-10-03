import os
from dotenv import load_dotenv
from anthropic import Anthropic
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import numpy as np

app = FastAPI()
load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

class Request(BaseModel):
    question:str

class AnswerResponse(BaseModel):
    answer:str
    cache_hit: bool
    similarity: float

class CacheEntry(BaseModel):
    question: str
    answer: str
    embedding: list[float] = []
    
cache: list[CacheEntry] = []
stats = {"hits": 0, "misses": 0}

@app.post("/askAI", response_model = AnswerResponse)
def ask_endpoint(payload:Request):
    match,score  = find_best_match(payload.question)
    if match:
        stats["hits"] += 1
        return AnswerResponse(answer=match.answer, cache_hit=True, similarity=round(score, 3))

    stats["misses"] += 1
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        messages=[{"role": "user", "content": payload.question}]
    )
    answer = response.content[0].text
    embedding = embed_model.encode(payload.question).tolist()
    cache.append(CacheEntry(question=payload.question, answer=answer, embedding=embedding))

    return AnswerResponse(answer=answer, cache_hit=False, similarity=round(score, 3))




def find_best_match(question:str,threshold:float = 0.85):
    best_entry = None
    best_score = 0.0
    q_embedding = embed_model.encode(question).tolist()
    for entry in cache:
        score = cosine_similarity(q_embedding, entry.embedding)
        if score>best_score:
           best_score = score
           best_entry = entry 
    if best_entry and best_score > threshold:
            return best_entry, best_score
    return None, best_score


def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


@app.get("/stats")
def getStats():
    return stats
    

