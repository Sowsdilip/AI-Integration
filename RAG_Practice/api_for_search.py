from fastapi import FastAPI
from pydantic import BaseModel,Field
from search_query import search
import anthropic
from dotenv import load_dotenv
import json

app = FastAPI()
load_dotenv()
client = anthropic.Anthropic()

SYSTEM = """You answer questions using ONLY the provided context.
Rules:
- Give a complete answer: include related details from the context (causes, limitations, fixes), in 2-5 sentences.
- If the context answers only part of the question, answer that part and state what is missing.
- If the context contains nothing relevant, set "answer" to "not found" and "citations" to [] and cached to False.
- Cite the chunk IDs you used, e.g. "letter_of_credit.txt#3".
- Respond with JSON only: {"answer": "...", "citations": ["..."]}"""

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



def ask_claude(hits,question:str):
    labels = [f"{meta["source"]}#{meta["chunk_index"]}" for _,meta,_ in hits]
    sent_labels = set(labels)
    parts = [f"[{label}]\n{doc}" for label,(doc,meta,dist) in zip(labels,hits)]
    context = "Context:"+"\n\n".join(parts)
    message = client.messages.create(
        model = "claude-haiku-5-5",
        max_tokens=500,
        system=SYSTEM,
        messages = [{"role":"user","content":f"\n{context}\n\nQuestion:{question}"}],
    )
    resp_message = next((b.text for b in message.content if b.type == "text"), None)
    if not resp_message:
        return {"answer":"not found","citations":[]}
    json_message = parse_json(resp_message) 
    received_labels =  json_message.get("citations",[])
    citations = [citation for citation in received_labels if citation in sent_labels]
    response_message = {"answer":json_message.get("answer","not found"),"citations":citations}
    return response_message

@app.post("/ask", response_model=AskResponse)
def search_with_rag(req:RequestModel):
    hits = search(req.question,max_dist=0.65)
    if hits:
        claude_response = ask_claude(hits,req.question)
        response = AskResponse(
            answer = claude_response["answer"],
            #citations = [f"{meta["source"]}#{meta["chunk_index"]}" for doc,meta,dist in hits],
            citations = claude_response.get("citations",[]),
        )
    else:
        response = AskResponse(answer="not found")    
    return response

def main():
    question = "Who is the applicant in an LC"
    hits = search(question,max_dist=0.65)
    best_hit = {"answer":hits[0][0],"citation":f"{hits[0][1]["source"]}#{hits[0][1]["chunk_index"]}","cached":False}
    print(best_hit)

if __name__ == "__main__":
    main()
 
