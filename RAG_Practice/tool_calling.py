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

def call_claude(messages):
    message = send_message(messages)
    query = ""
    json_message = {"answer":not_found,"citations":[]}
    stop_reason = message.stop_reason
    turns,max_turns = 0,4
    while stop_reason == "tool_use" and turns<max_turns:
      tool_block = None
      for block in message.content:
        if block.type == "tool_use":
          query = block.input["query"]
          tool_block = block
          break
      if tool_block is None:
          return json_message
      labels = hybrid_top(query)
      parts = [f"[{label}]\n{CHUNK_TEXT[label]}" for label in labels]
      context = "\n\n".join(parts)
      content = {
        "type":"tool_result",
        "tool_use_id":tool_block.id,
        "content":context
      }
      add_turn(messages,role="user",content=[content])
      message = send_message(messages)
      stop_reason = message.stop_reason
      turns+=1
    print(f"turns  =>{turns}")
    print(f"stop_reason   {stop_reason}")
    if stop_reason == "end_turn":
       resp_message = next((b.text for b in message.content if b.type == "text"), None)
       if resp_message:
         json_message = parse_json(resp_message)
    return json_message
    
def main():
   messages = []
   add_turn(messages,role="user",content="What is LC?")
   print(messages)
   response = call_claude(messages)
   print(response)
  

if __name__ == "__main__":
   main()


    

