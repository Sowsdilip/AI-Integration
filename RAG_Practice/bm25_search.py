from pathlib import Path
import chromadb
import re
from rank_bm25 import BM25Okapi

def tokenize(text:str)->list[str]:
    return re.findall(r"\w+",text.lower())

BASE = Path(__file__).parent
client = chromadb.PersistentClient(str(BASE / "chromd_db"))
collection = client.get_collection("docs")
data = collection.get(include=["documents","metadatas"])

tokens = []
for doc_text in data["documents"]:
    tokens.append(tokenize(doc_text))
bm25 = BM25Okapi(tokens)
metadatas = data["metadatas"]
labels = [f"{meta["source"]}#{meta["chunk_index"]}" for meta in metadatas]
CHUNK_TEXT = dict(zip(labels,data["documents"]))

def bm25_search(query:str,slice_index:int = 3):
    query_tokens = tokenize(query)
    scores = bm25.get_scores(query_tokens)
    pairs = zip(labels,scores)
    sorted_scores = sorted(pairs,key = lambda p:p[1],reverse=True)
    #return [p[0] for p in sorted_scores[:slice_index]]
    return sorted_scores


if __name__ == "__main__":
    query = "What is the maximum validity period of an LC in the UAE?"
    print(bm25_search(query,10))