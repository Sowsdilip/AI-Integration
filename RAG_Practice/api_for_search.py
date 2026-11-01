from fastapi import FastAPI
from pydantic import BaseModel,Field
from search_query import search
import anthropic
from dotenv import load_dotenv
import json
import logging
from rag_layer import model
from semantic_cache import find_best_match,cache,CacheEntry
from bm25_search import bm25_search,CHUNK_TEXT
from hybrid_search import rrf

app = FastAPI()
load_dotenv()
client = anthropic.Anthropic()
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
stats = {"hits":0,"misses":0}
not_found = "not found"
SYSTEM = f"""You answer questions using ONLY the provided context.
Rules:
- Give a complete answer: include related details from the context (causes, limitations, fixes), in 2-5 sentences.
- If the context directly answers only part of the question specially fir multi part questions, answer that part and state what is missing.
- If the context doesn’t contain the specific fact asked for, set "answer" to "{not_found}" and "citations" to [].
- Cite the chunk IDs you used, e.g. "letter_of_credit.txt#3".
- Respond with JSON only: {{"answer": "...", "citations": ["..."]}}"""

class RequestModel(BaseModel):
    question:str

class AskResponse(BaseModel):
    answer:str | None
    citations:list[str] = Field(default_factory=list)
    cached:bool = False

def parse_json(message: str) -> dict:
    clean_msg = message.strip()
    if clean_msg.startswith("```"):
        clean_msg = clean_msg.split("\n", 1)[1]      
        clean_msg = clean_msg.rsplit("```", 1)[0]  
    try:
        return json.loads(clean_msg)
    except json.JSONDecodeError:
        return {"answer": message.strip(), "citations": [], "warning": "model did not return valid JSON"}



def ask_claude(labels,question:str):
    #labels = [f"{meta["source"]}#{meta["chunk_index"]}" for _,meta,_ in hits]
    sent_labels = set(labels)
    parts = [f"[{label}]\n{CHUNK_TEXT[label]}" for label in labels]
    context = "Context:\n"+"\n\n".join(parts)
    message = client.messages.create(
        model = "claude-haiku-5-5",
        max_tokens=1500,
        system=SYSTEM,
        messages = [{"role":"user","content":f"\n{context}\n\nQuestion:{question}"}],
    )
    resp_message = next((b.text for b in message.content if b.type == "text"), None)
    if not resp_message:
        return {"answer":not_found,"citations":[]}
    stop_reason = message.stop_reason
    log.info("stop_reason = %s ",stop_reason)
    if "max_tokens" == stop_reason:
        return {"answer":not_found,"citations":[]}
    json_message = parse_json(resp_message) 
    if not_found == json_message.get("answer","").strip(" .").lower():
        return {"answer":not_found,"citations":[]}
    received_labels =  json_message.get("citations",[])
    citations = [citation for citation in received_labels if citation in sent_labels]
    if not citations:
        log.warning("no valid citations: answer=%r received=%s",json_message.get("answer",""),received_labels)
        return {"answer":not_found,"citations":[]}
    response_message = {"answer":json_message.get("answer",not_found),"citations":citations}
    return response_message

@app.post("/ask", response_model=AskResponse)
def search_with_rag(req:RequestModel):
    embedding = model.encode(req.question).tolist()
    match,score = find_best_match(embedding)
    if match:
        stats["hits"]+=1
        log.info("question=%r stats=%s   cached=%s score=%f",req.question,stats,True,score)
        return AskResponse(answer = match.answer,citations = match.citations, cached = True)
    stats["misses"]+=1
    hits = search(req.question,k=10,max_dist=0.65) 
    best = None
    if hits:
        best = min([dist  for doc,meta,dist in hits]) 
        pairs = bm25_search(req.question,10)
        bm25_labels = [label for label,_ in pairs]
        vector_labels =[f"{meta["source"]}#{meta["chunk_index"]}" for doc,meta,dist in hits]
        fused = rrf([vector_labels,bm25_labels]) 
        claude_response = ask_claude(fused,req.question)
        response = AskResponse(
            answer = claude_response["answer"],
            #citations = [f"{meta["source"]}#{meta["chunk_index"]}" for doc,meta,dist in hits],
            citations = claude_response.get("citations",[]),
        )
    else:
        response = AskResponse(answer=not_found)    
    log.info("question=%r hits=%d best=%s",req.question,len(hits),best)
    log.info("cached=%s",response.cached)
    log.info("stats=%s score=%f",stats,score)
    if not_found != response.answer:
        cache.append(CacheEntry(question=req.question, answer=response.answer, embedding=embedding,citations = response.citations))
    return response

def main():
    question = "Who is the applicant in an LC"
    hits = search(question,max_dist=0.65)
   # best_hit = {"answer":hits[0][0],"citation":f"{hits[0][1]["source"]}#{hits[0][1]["chunk_index"]}","cached":False}
   # print(best_hit)

if __name__ == "__main__":
    main()
 
