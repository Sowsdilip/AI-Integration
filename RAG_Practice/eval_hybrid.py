from lc_evalset import EVAL_SET
from bm25_search import CHUNK_TEXT
from hybrid_search import vector_top,hybrid_top

def run_eval(search_fn):
    results = []
    for item in EVAL_SET:
        if not item.get("key_phrase") and not item.get("answered_by"):
            continue
        labels = search_fn(item["question"])
        results.append({"id": item["id"], "hit": is_hit(item, labels)})
    return  results
    

def is_hit(item,labels):
    if item.get("key_phrase"):
        return any(item["key_phrase"].lower() in CHUNK_TEXT[label].lower() for label in labels)
    if item.get("answered_by"):
        return any(label.split("#")[0].lower() == item["answered_by"].lower() for label in labels)
    return None

def main():
    vec = run_eval(vector_top)
    hyb = run_eval(hybrid_top)
    print(f"vec   {vec}")
    print(f"hyb   {hyb}")

if __name__ == "__main__":
    main()