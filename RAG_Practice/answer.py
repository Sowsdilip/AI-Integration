import json
import anthropic
from rag_learning import search
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from the environment

SYSTEM = """You answer questions using ONLY the provided context.
Rules:
- Give a complete answer: include related details from the context (causes, limitations, fixes), in 2-5 sentences.
- If the context answers only part of the question, answer that part and state what is missing.
- If the context contains nothing relevant, set "answer" to "Not found in the documents." and "citations" to [].
- Cite the chunk IDs you used, e.g. "sample.txt#5".
- Respond with JSON only: {"answer": "...", "citations": ["..."]}"""

def parse_json(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1]      # drop the ```json line
        cleaned = cleaned.rsplit("```", 1)[0]    # drop the closing ```
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"answer": text.strip(), "citations": [], "warning": "model did not return valid JSON"}


def ask(question: str) -> dict:
    hits = search(question, verbose=False)
    if not hits:   # skip the LLM call entirely: saves cost and avoids made-up answers
        return {"answer": "Not found in the documents.", "citations": []}

    context = "\n\n".join(
        f"[{meta['source']}#{meta['chunk_index']}]\n{doc}" for doc, meta, _ in hits
    )
    msg = client.messages.create(
        model="claude-haiku-5-5",   # cheap and fast for learning; use the model you used in Week 1 if different
        max_tokens=500,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}],
    )
    text = "".join(b.text for b in msg.content if b.type == "text")
    return parse_json(text)
    #return json.loads(msg.content[0].text)


if __name__ == "__main__":
    while True:
        q = input("\nQuestion (blank to quit): ").strip()
        if not q:
            break
        result = ask(q)
        print("\nAnswer:", result["answer"])
        print("Sources:", result["citations"])

