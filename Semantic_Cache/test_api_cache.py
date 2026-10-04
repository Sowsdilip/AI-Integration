import os
from dotenv import load_dotenv
from anthropic import Anthropic
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel
from similarity import cosine_similarity
import numpy as np

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
embed_model = SentenceTransformer("all-MiniLM-L6-v2")


class CacheEntry(BaseModel):
    question: str
    answer: str

    class Config:
        arbitrary_types_allowed = True  # lets us store a numpy array on this model

    embedding: list[float] = []


cache: list[CacheEntry] = []
stats = {"hits": 0, "misses": 0}

def find_best_match(question: str, threshold: float = 0.85):
    q_embedding = embed_model.encode(question).tolist()
    best_entry = None
    best_score = 0.0

    for entry in cache:
        score = cosine_similarity(q_embedding, entry.embedding)
        if score > best_score:
            best_score = score
            best_entry = entry

    if best_entry and best_score > threshold:
        return best_entry, best_score
    return None, best_score


def ask(question: str) -> str:
    match, score = find_best_match(question)

    if match:
        stats["hits"] += 1
        print(f"[CACHE HIT] similarity={score:.3f} -> reusing answer for: '{match.question}'")
        return match.answer

    stats["misses"] += 1
    print(f"[CACHE MISS] best similarity={score:.3f} -> calling Claude")

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        messages=[{"role": "user", "content": question}]
    )
    answer = response.content[0].text

    embedding = embed_model.encode(question).tolist()
    cache.append(CacheEntry(question=question, answer=answer, embedding=embedding))

    return answer


# --- test it ---
print(ask("What is FastAPI?"))
print(ask("Explain FastAPI to me"))
print(ask("What's the capital of France?"))
print(ask("Tell me what FastAPI is used for"))

print("\nStats:", stats)