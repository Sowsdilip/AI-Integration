from anthropic import Anthropic
from dotenv import load_dotenv
from hybrid_search import hybrid_top
from bm25_search import CHUNK_TEXT
import json

not_found = "not found"
SYSTEM = f"""You answer questions using ONLY the provided context.
Rules:
- Give a complete answer: include related details from the context (causes, limitations, fixes), in 2-5 sentences.
- If the context directly answers only part of the question specially for multi part questions, answer that part and state what is missing.
- If the context doesn’t contain the specific fact asked for, set "answer" to "{not_found}" and "citations" to [].
- Cite the chunk IDs you used, e.g. "letter_of_credit.txt#3".
- Respond with JSON only: {{"answer": "...", "citations": ["..."]}}"""

load_dotenv()
client = Anthropic()

def add_turn(messages, role, content):
    messages.append({"role": role, "content": content})

SEARCH_TOOL = {
    "name":"search_docs",
    "description":"Always use this for any trade-finance question; do not answer from memory",
    "input_schema":{
        "type":"object",
        "properties":{
            "query":{"type":"string","description":"Search keywords taken from the user’s question."}         
        },
        "required":["query"],
    }
}

LC_TOOL = {
    "name":"get_lc_status",
    "description":"Get LC details live status/amount/expiry/beneficiary for one specific LC number like LC-1001, Not for general trade-finance concepts; use search_docs for those.",
    "input_schema":{
        "type":"object",
        "properties":{
            "lc_number":{"type":"string","description":"lc_number e.g. LC-1001."}         
        },
        "required":["lc_number"],
    }
}

def parse_json(message: str) -> dict:
    clean_msg = message.strip()
    if clean_msg.startswith("```"):
        clean_msg = clean_msg.split("\n", 1)[1]      
        clean_msg = clean_msg.rsplit("```", 1)[0]  
    try:
        return json.loads(clean_msg)
    except json.JSONDecodeError:
        return {"answer": message.strip(), "citations": [], "warning": "model did not return valid JSON"}

def send_message(messages):
    message = client.messages.create(
     model = "claude-haiku-5-5",
            max_tokens=1500,
            tools = [SEARCH_TOOL],
            system=SYSTEM,
            messages = messages
    )
    print(message.stop_reason)
    add_turn(messages,role="assistant",content=message.content)
    return message

def get_context(labels,tool_use_id):
   parts = [f"[{label}]\n{CHUNK_TEXT[label]}" for label in labels]
   context = "\n\n".join(parts)
   content = {
      "type":"tool_result",
      "tool_use_id":tool_use_id,
      "content":context
    }
   return content
   

def call_claude(messages):
    message = send_message(messages)
    query = ""
    json_message = {"answer":not_found,"citations":[]}
    stop_reason = message.stop_reason
    turns,max_turns = 0,4
    sent_labels = set()
    sent_labels_dict = []
    while stop_reason == "tool_use" and turns<max_turns:
      content = []
      for block in message.content:
        if block.type == "tool_use":
          query = block.input["query"]
          labels = hybrid_top(query)
          sent_labels_dict.append({"tool_id":block.id,"labels":labels})
          sent_labels.update(labels)
          content.append(get_context(labels,block.id))
      if not content:
        return json_message
      add_turn(messages,role="user",content=content)
      message = send_message(messages)
      stop_reason = message.stop_reason
      turns+=1
    print(f"turns  = {turns}")
    print(f"stop_reason   {stop_reason}")
    if stop_reason == "end_turn":
       resp_message = next((b.text for b in message.content if b.type == "text"), None)
       if resp_message:
         json_message = parse_json(resp_message)
       received_labels =  json_message.get("citations",[])
       #received_labels = ["letter_of_credit.txt#0","x.txt#9"]
       if not received_labels:
         if json_message.get("answer","").strip(" .").lower() != not_found:
            print(f"no citations from calude: answer={json_message.get("answer","")} received={received_labels}")
            return {"answer":not_found,"citations":[],"warning": "no citation from claude"}
         return {"answer":not_found,"citations":[]}
       citations = [citation for citation in received_labels if citation in sent_labels]
       if not citations:
         print(f"no valid citations: answer={json_message.get("answer","")} received={received_labels}")
         return {"answer":not_found,"citations":[]}
       json_message["citations"] = citations
    return json_message
    
def main():
   messages = []
   add_turn(messages,role="user",content="What is the maximum validity period of an LC in the UAE?")
   print(messages)
   response = call_claude(messages)
   print(response)
  

if __name__ == "__main__":
   main()


    

