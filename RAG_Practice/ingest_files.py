from pathlib import Path
from rag_learning import collection,ingest

def ingest_folder(folder = "Docs"):
    files = Path(folder).glob("*.txt")
    for f in files:
        before = collection.count()
        ingest(f.read_text(encoding="utf-8"), f.name)
        after = collection.count()
        print(f"before={before} after={after} added={after - before}")

if __name__ == "__main__":
    ingest_folder("Docs")
    print("after ingesttion")
    docs = collection.get(where={"source": "letter_of_credit.txt"})["documents"]
    for i, d in enumerate(docs):
        print(f"--- chunk {i} ({len(d)} chars) ---")
        print(d[:150])
    #print(collection.get(where={"source": "letter_of_credit.txt"})["documents"])
