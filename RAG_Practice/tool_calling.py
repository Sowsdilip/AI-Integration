from anthropic import Anthropic
from dotenv import load_dotenv
from hybrid_search import hybrid_top
from bm25_search import CHUNK_TEXT
not_found = "not found"
SYSTEM = f"""You answer questions using ONLY the provided context.
Rules:
- Give a complete answer: include related details from the context (causes, limitations, fixes), in 2-5 sentences.
- If the context directly answers only part of the question specially fir multi part questions, answer that part and state what is missing.
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
    tool_block = None
    for block in message.content:
      if block.type == "tool_use":
        query = block.input["query"]
        tool_block = block
        break
    if tool_block is None:
     return
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
    resp_message = next((b.text for b in message.content if b.type == "text"), None)
    print(resp_message)
    
def main():
   messages = []
   add_turn(messages,role="user",content="What is HashMap?")
   print(messages)
   call_claude(messages)
  

if __name__ == "__main__":
   main()


    

