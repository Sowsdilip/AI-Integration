from bm25_search import bm25_search
from search_query import search 

def rrf(result_lists,k=60,top_m=4):
   label_dict = {}
   for labels in result_lists:
       for rank,label in enumerate(labels,start = 1):
           score = label_dict.get(label,0)
           score = score + (1/(rank+k))
           label_dict[label]=score
   sorted_scores = sorted(label_dict, key = label_dict.get,reverse=True)
   return sorted_scores[:top_m]
    

def main():
    query = "Who is the applicant in an LC?"
    pairs = bm25_search(query,10)
    bm25_labels = [label for label,_ in pairs]
    hits = search(query,10)
    vector_labels =[f"{meta["source"]}#{meta["chunk_index"]}" for doc,meta,dist in hits]
    fused = rrf([vector_labels,bm25_labels])
    print(fused)

def hybrid_top(query):
    pairs = bm25_search(query,10)
    bm25_labels = [label for label,_ in pairs]
    hits = search(query,10)
    vector_labels =[f"{meta["source"]}#{meta["chunk_index"]}" for doc,meta,dist in hits]
    fused = rrf([vector_labels,bm25_labels])
    return fused

def vector_top(q,k=4):
     hits = search(q,k)
     vector_labels =[f"{meta["source"]}#{meta["chunk_index"]}" for doc,meta,dist in hits]
     return vector_labels

def hybrid_top(q,k=4):
     vector_labels = vector_top(q,10)
     pairs = bm25_search(q,10)
     bm25_labels = [label for label,_ in pairs]
     fused = rrf([vector_labels,bm25_labels],top_m=k)
     return fused


def test_main():    
    vector_labels = ["A", "B", "C"]
    bm25_labels   = ["B", "D", "A"] 
    fused = rrf([vector_labels,bm25_labels])
    assert fused[:2] == ["B", "A"]


if __name__ == "__main__":
    test_main()