from rag_learning import collection,ingest


with open("sample.txt",encoding = "utf-8") as f:
    before = collection.count()
    ingest(f.read(),"sample.txt")
    after = collection.count()
    print(f"before={before} after={after} added={after - before}")
print("total chunks stored: ",collection.count())