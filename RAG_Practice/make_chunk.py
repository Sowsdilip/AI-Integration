import hashlib
from pathlib import Path

def sha(chunk:str)->str:
    return hashlib.sha256(chunk.encode()).hexdigest()[:16]


def make_chunk(text:str,source:str,size:int = 500,overlap:int = 50)->list[dict]:
    step = size-overlap
    chunks = [
        {
            "id":sha(f"{source}:{start}"),
            "text":(chunk := text[start:start + size]),
            "end":min(start+size,len(text)),
            "hash":sha(chunk),
            "source":source,
            "chunk_index":i,
            "start":start,
        }
        for i,start in enumerate(range(0,len(text),step))
    ]
    return chunks

if __name__ == "__main__":
    f = Path("Docs")/"letter_of_credit.txt"
    chunks = make_chunk(f.read_text(),f.name)
    print(chunks)

    #chunks = [text[start:start+size] for start in range(0,len(text),size-overlap)]
    

