from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")  # small, free, runs locally

cache = []  # list of (question_text, embedding, answer)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_cached_answer(question, threshold=0.85):
    q_embedding = model.encode(question)
    for cached_q, cached_emb, answer in cache:
        if cosine_similarity(q_embedding, cached_emb) > threshold:
            return answer
    return None

def store_answer(question, answer):
    embedding = model.encode(question)
    cache.append((question, embedding, answer))

store_answer("What is FastAPI?", "FastAPI is a Python web framework for building APIs.")

result = get_cached_answer("Explain FastAPI to me")
print("Result:", result)

result2 = get_cached_answer("What's the capital of France?")
print("Unrelated question result:", result2)