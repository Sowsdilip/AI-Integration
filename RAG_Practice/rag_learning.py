import hashlib
import chromadb
from sentence_transformers import SentenceTransformer
from chunk_function import chunk_by_size
from chunk_function import chunk_by_paragraph


model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient("./chroma_db")
#client.delete_collection("docs")
collection = client.get_or_create_collection("docs",metadata={"hnsw:space":"cosine"})


def ingest(text:str,source:str):
    chunks=chunk_by_paragraph(text)
    ids = [hashlib.sha256(f"{source}:{c}".encode()).hexdigest() for c in chunks]  # idempotent
    embeddings = model.encode(chunks).tolist()
    collection.upsert(
        ids = ids,
        documents = chunks,
        embeddings = embeddings,
        metadatas = [{"source":source,"chunk_index":i} for i in range(len(chunks))]
    )

def search(query:str,k:int = 4, max_distance:float = 0.7,verbose:bool = False):
    q_emb = model.encode([query]).tolist()
    res = collection.query(query_embeddings = q_emb,n_results = k)
    hits = [
        (doc,meta,dist)
        for doc,meta,dist in zip(res["documents"][0],res["metadatas"][0],res["distances"][0])
        if dist<=max_distance 
    ]
    if verbose:
       if hits:
        for doc,meta,dist in hits:
            print(f"\n[{meta['source']}#{meta['chunk_index']}] dist={dist:.3f}\n{doc}\n" + "-"*60)
       #for doc,meta, dist in zip(res["documents"][0],res["metadatas"][0],res["distances"][0]):
       # print(f"[{meta['source']}#{meta['chunk_index']}] dist={dist:.3f}  {doc[:80]}...")       
       else:
          print("No relevant chunks found")
    return hits
