import os
os.environ["HF_HUB_OFFLINE"] = "1"
import re
from make_chunk import sha
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")
BASE = Path(__file__).parent
client = chromadb.PersistentClient(str(BASE / "chromd_db"))
#client = chromadb.PersistentClient("./chromd_db")
collection = client.get_or_create_collection("docs",metadata={"hnsw:space":"cosine"})

def split_into_paras(text:str)->list[str]:
    cleaned_text = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return cleaned_text

def get_chunks(para, max_size):
    start = 0
    chunks = []
    while start<len(para):
        window = para[start:start+max_size]
        if start+max_size>=len(para):
            chunks.append(window.strip())
            break
        else:
            cut = window.rfind(". ")
            if cut < max_size//2 or cut == -1:
                cut = window.rfind(" ")
                if cut == -1:
                    cut = max_size-1
            chunks.append(window[:cut+1].strip())
            start += cut+1

    return chunks

def merge(paras,max_size:int = 1000)->list[str]:
    chunks:list[str] = []
    current = ""
    for para in paras:
        if len(para)>max_size:
            if current:
                chunks.append(current)
                current = ""
            chunks.extend(get_chunks(para,max_size))
            #chunks.extend(para[i:i+max_size] for i in range(0,len(para),max_size))
            continue
        candidate = f"{current}\n\n{para}" if current else para
        if len(candidate)<=max_size:
            current = candidate
        else:
           if current:
                chunks.append(current)
           current = para
    if current:
        chunks.append(current)
    return chunks

def make_record(chunk: str, source: str, i: int) -> dict:
   return {
        "id":sha(f"{source}:{i}"),
        "text":chunk,
        "hash":sha(chunk),
        "source":source,
        "chunk_index":i,
    }

def store_records(records:list[dict],source:str):
    docs = [record["text"] for record in records] 
    ids =  [record["id"] for record in records] 
    metadatas = [{"source":record["source"],"chunk_index":record["chunk_index"]} for record in records]
    embeddings = model.encode(docs).tolist()
    assert len(ids) == len(docs) == len(metadatas)
    collection.delete(where={"source":source})
    collection.upsert(
        ids = ids,
        documents = docs,
        embeddings = embeddings,
        metadatas = metadatas
    )
  

def process():
    max_size = 600
    files = (BASE / "Docs").glob("*.txt")
    #files = Path("Docs").glob("*.txt")
    records = []
    before = collection.count()    
    for file in files:
        text = file.read_text("utf-8")
        paras = split_into_paras(text)
        chunks = merge(paras, max_size) 
        records = [make_record(c, file.name, i) for i, c in enumerate(chunks)]
        store_records(records,file.name)
    after = collection.count()
    print(f"before={before} after={after} added={after - before}")
   # records2 = [make_record(c, file.name, i) for i, c in enumerate(merge(split_into_paras(text), max_size))]
   # print(records)
   # assert all(len(r["text"]) <= max_size for r in records),"chunk exceeds max_size"
   # assert all(r["text"].strip() for r in records)  
   # assert [r["id"] for r in records] == [r["id"] for r in records2], "ids not stable"
   # assert [r["hash"] for r in records] == [r["hash"] for r in records2], "hashes not stable"
   
def main():
    max_size = 600
    file = Path("Docs")/"letter_of_credit.txt"
    text = file.read_text("utf-8")
    paras = split_into_paras(text)
    chunks = merge(paras, max_size) 
    #print(f"chunks    \n {chunks}")
    print([i for i, c in enumerate(chunks) if "examines the documents" in c])




if __name__ =="__main__":
    process()