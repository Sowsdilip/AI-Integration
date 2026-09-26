import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic
from pydantic import BaseModel

load_dotenv()
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=anthropic_api_key)

class Summary(BaseModel):
    topic:str
    key_points:list[str]

response = client.messages.create(
    model = "claude-haiku-4-5-20251001",
    max_tokens = 300,
    messages = [
        {"role":"user","content":(
                "Give me a JSON object with a 'topic' field and a 'key_points' "
                "field (a list of exactly 3 short strings) about MCP servers. "
                "Return ONLY the JSON object, no markdown, no explanation, no code fences."
            )}
    ]
)

print(f"complete response message: {response}")

raw_text = response.content[0].text
print(f"raw response:   {raw_text}")

data = json.loads(raw_text)
summary = Summary(**data)

print("Validated message: ")
print(f"topic:  {summary.topic}")
print(f"key_points:   {summary.key_points}")