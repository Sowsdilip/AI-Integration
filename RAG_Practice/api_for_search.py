from fastapi import FastAPI
from pydantic import BaseModel
from search_query import search

app = FastAPI()

class RequestModel(BaseModel):
    question:str

@app.post("/ask")
def search_with_rag(req:RequestModel):
    hits = search(req.question,max_dist=0.65)
    if hits:
        response = {
                "answer" : None,
                "citations" : [f"{meta["source"]}#{meta["chunk_index"]}" for doc,meta,dist in hits],
                "chunks" : [doc for doc,meta,dist in hits],
                "cached" : False,
            }
    else:
        response = {
            "answer" : "NotFound",
            "citations" : [],
            "chunks" : [],
            "cached" : False,
        }

    
    #best_hit = {"answer":hits[0][0],"citation":f"{hits[0][1]["source"]}#{hits[0][1]["chunk_index"]}","cached":False}
    return response

def main():
    question = "Who is the applicant in an LC"
    hits = search(question,max_dist=0.65)
    best_hit = {"answer":hits[0][0],"citation":f"{hits[0][1]["source"]}#{hits[0][1]["chunk_index"]}","cached":False}
    print(best_hit)

if __name__ == "__main__":
    main()
 
