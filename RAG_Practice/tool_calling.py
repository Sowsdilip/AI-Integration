from anthropic import Anthropic
from dotenv import load_dotenv
from RAG_Practice.hybrid_search import hybrid_top
from RAG_Practice.bm25_search import CHUNK_TEXT
import json
from RAG_Practice.call_spring_api import get_lc_status

not_found = "not found"
unavailable = "lc service unavailable please retry"
ALLOWED_NO_CITATION = {not_found, unavailable}
SYSTEM = f"""You answer questions using ONLY context and tool results”.
Rules:
- Give a complete answer: include related details from the context (causes, limitations, fixes), in 2-5 sentences.
- If the context directly answers only part of the question specially for multi part questions, answer that part and state what is missing.
- If the context doesn’t contain the specific fact asked for, set "answer" to "{not_found}" and "citations" to [].
- Cite the chunk IDs you used from search_docs, e.g. "letter_of_credit.txt#3".
- For facts from get_lc_status, cite "api:lc/<LC number>", e.g. "api:lc/LC-1001". If get_lc_status returns an error, say the LC was not found or the service is unavailable; never invent LC details.
- If get_lc_status returns an error, its text starts with the error kind in brackets:
  - [not_found]: set "answer" to "{not_found}", "citations" to [].
  - [unavailable] or [upstream_error]: set "answer" to "LC service unavailable please retry", "citations" to []. Never say the LC does not exist, and never guess a status.
  - [invalid_input]: set "answer" to "bad input please check", "citations" to [].
- Respond with JSON only: {{"answer": "...", "citations": ["..."]}}"""

load_dotenv()
client = Anthropic()


def add_turn(messages, role, content):
    messages.append({"role": role, "content": content})


SEARCH_TOOL = {
    "name": "search_docs",
    "description": "Search the trade-finance knowledge base for concepts, rules and document requirements (e.g. what a confirmed LC is, UCP 600, Incoterms). do not answer from memory.Not for the live status of a specific LC number; use get_lc_status for that.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search keywords taken from the user’s question.",
            }
        },
        "required": ["query"],
    },
}

LC_TOOL = {
    "name": "get_lc_status",
    "description": "Get LC details live status/amount/expiry/beneficiary for one specific LC number like LC-1001, Not for general trade-finance concepts; use search_docs for those.",
    "input_schema": {
        "type": "object",
        "properties": {
            "lc_number": {"type": "string", "description": "lc_number e.g. LC-1001."}
        },
        "required": ["lc_number"],
    },
}


def parse_json(message: str) -> dict:
    clean_msg = message.strip()
    if clean_msg.startswith("```"):
        clean_msg = clean_msg.split("\n", 1)[1]
        clean_msg = clean_msg.rsplit("```", 1)[0]
    try:
        return json.loads(clean_msg)
    except json.JSONDecodeError:
        return {
            "answer": message.strip(),
            "citations": [],
            "warning": "model did not return valid JSON",
        }


def send_message(messages):
    message = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=1500,
        tools=[SEARCH_TOOL, LC_TOOL],
        system=SYSTEM,
        messages=messages,
    )
    print(message.stop_reason)
    add_turn(messages, role="assistant", content=message.content)
    return message


def get_context(labels, tool_use_id):
    parts = [f"[{label}]\n{CHUNK_TEXT[label]}" for label in labels]
    context = "\n\n".join(parts)
    content = {"type": "tool_result", "tool_use_id": tool_use_id, "content": context}
    return content


def run_search(tool_input, tool_use_id):
    labels = hybrid_top(tool_input["query"])
    return get_context(labels, tool_use_id), labels


def run_lc_status(tool_input, tool_use_id):
    message, is_error = get_lc_status(tool_input["lc_number"])
    if is_error:
        labels = []
    else:
        labels = [f"api:lc/{tool_input["lc_number"].strip().upper()}"]
    result = {
        "type": "tool_result",
        "tool_use_id": tool_use_id,
        "content": f"[{is_error}] {message}" if is_error is not None else message,
        "is_error": bool(is_error),
    }
    return result, labels


TOOLS = {"search_docs": run_search, "get_lc_status": run_lc_status}


def call_claude(messages):
    message = send_message(messages)
    query = ""
    json_message = {"answer": not_found, "citations": []}
    stop_reason = message.stop_reason
    turns, max_turns = 0, 4
    sent_labels = set()
    sent_labels_dict = []
    while stop_reason == "tool_use" and turns < max_turns:
        content = []
        for block in message.content:
            if block.type == "tool_use":
                handler = TOOLS.get(block.name)
                if handler is None:
                    content.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": "unknown tool",
                            "is_error": True,
                        }
                    )
                    continue
                context, labels = handler(block.input, block.id)
                sent_labels_dict.append({"tool_id": block.id, "labels": labels})
                sent_labels.update(labels)
                content.append(context)
        if not content:
            return json_message
        add_turn(messages, role="user", content=content)
        message = send_message(messages)
        stop_reason = message.stop_reason
        turns += 1
    print(f"turns  = {turns}")
    print(f"stop_reason   {stop_reason}")
    if stop_reason == "end_turn":
        resp_message = next((b.text for b in message.content if b.type == "text"), None)
        if resp_message:
            json_message = parse_json(resp_message)
        received_labels = json_message.get("citations", [])
        print(
            f"response from calude: answer={json_message.get("answer","")} received={received_labels}"
        )
        #received_labels = ["letter_of_credit.txt#0","x.txt#9"]
        if not received_labels:
            print(
                f"no citations from calude: answer={json_message.get("answer","")} received={received_labels}"
            )
            claude_response = json_message.get("answer", "").strip(" .").lower()
            if claude_response in ALLOWED_NO_CITATION:
                return {
                    "answer": claude_response,
                    "citations": [],
                }
            return {
                "answer": not_found,
                "citations": [],
                "warning": "no citations from calude",
            }
        citations = [
            citation for citation in received_labels if citation in sent_labels
        ]
        if not citations:
            print(
                f"no valid citations: answer={json_message.get("answer","")} received={received_labels}"
            )
            return {
                "answer": not_found,
                "citations": [],
                "warning": "no valid citations",
            }
        json_message["citations"] = citations
    return json_message


def main():
    messages = []
    add_turn(
        messages,
        role="user",
        content="what is the status of LC-1001?",
    )
    print(messages)
    response = call_claude(messages)
    print(response)


if __name__ == "__main__":
    main()
