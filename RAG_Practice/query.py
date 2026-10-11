from rag_learning import search

while True:
    q = input("\n Question (leave empty to quit) : ").strip()
    if not q:
        break
    search(q)