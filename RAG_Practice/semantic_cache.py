from rag_layer import model
from pydantic import BaseModel
from cosine_similarity import find_cosine_similarity

class CacheEntry(BaseModel):
   question:str
   answer:str
   embedding: list[float] = []
   citations: list[str] = []

cache: list[CacheEntry] = []
  

def find_best_match(q_embedding,threshold:float = 0.80):
   best_entry = "" 
   best_score = 0.0
   for entry in cache:
      score = find_cosine_similarity(q_embedding,entry.embedding)
      if score > best_score:
         best_score = score
         best_entry = entry
   if best_entry and best_score > threshold:
      return best_entry,best_score
   return None,best_score