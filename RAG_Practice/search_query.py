from rag_layer import model,collection
from lc_evalset import EVAL_SET

def search(query:str,k:int = 4,max_dist:float = 2.0,verbose:bool = False):
    query_emb = model.encode([query]).tolist()
    #print(collection.count())
    response = collection.query(query_embeddings = query_emb,n_results=k)
    hits = [
        (doc,meta,dist) for doc,meta,dist in zip(response["documents"][0],response["metadatas"][0],response["distances"][0]) 
        if dist<=max_dist
    ]
    if verbose:
       if hits:
           for doc,meta,dist in hits:
              print(f"\n[{meta['source']}#{meta['chunk_index']}] dist={dist:.3f}\n{doc}\n" + "-"*60)
       else:
           print("not found")
    return hits

def is_hit(item,hits):
    if item.get("key_phrase"):
        return any(item["key_phrase"].lower() in doc.lower() for doc,meta,dist in hits)
    if item.get("answered_by"):
        return any(meta["source"].lower() == item["answered_by"].lower() for doc,meta,dist in hits)
    return None

def run_eval():
    results = []
    for item in EVAL_SET:
        hits = search(item["question"])
        best = hits[0][2] if hits else None
        results.append({"id": item["id"], "hit": is_hit(item, hits), "best_dist": best})
    for r in results:
        print(r["id"], r["hit"], r["best_dist"])
           

def main():
    run_eval()
    #for item in EVAL_SET:
       # print(item["id"], list(item.keys()))

if __name__ == "__main__":
    main()






    