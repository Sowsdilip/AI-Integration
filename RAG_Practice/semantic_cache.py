cd..from pydantic import BaseModel
from cosine_similarity import find_cosine_similarity

class CacheEntry(BaseModel):
   question:str
   answer:str
   embedding: list[float] = []
   citations: list[str] = []


class Semantic_Cache():

   def __init__(self,cache_entries=None,thresh_hold=0.80):
      self.cache_entries = cache_entries if cache_entries is not None else [] 
      self.thresh_hold = thresh_hold

   def find_best_match(self,q_embedding):
      best_entry = "" 
      best_score = 0.0
      for entry in self.cache_entries:
         score = find_cosine_similarity(q_embedding,entry.embedding)
         if score > best_score:
            best_score = score
            best_entry = entry
      if best_entry and best_score > self.thresh_hold:
         return best_entry,best_score
      return None,best_score
  
   def store(self,question, q_emb, answer, citations):
      self.cache_entries.append(CacheEntry(question=question, answer=answer, embedding=q_emb,citations = citations))
         
   def clear(self):
      self.cache_entries.clear()
