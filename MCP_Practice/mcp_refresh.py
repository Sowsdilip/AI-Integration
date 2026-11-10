from mcp.server.mcpserver import MCPServer
from RAG_Practice.hybrid_search import hybrid_top
from RAG_Practice.bm25_search import CHUNK_TEXT
import json
from RAG_Practice import call_spring_api

mcp = MCPServer("mcp application")

@mcp.tool()
def normalize_lc_number(lc_number:str|None = None)-> str:
    """Clean up an LC number: trim spaces and uppercase it.
    return empty if it is None else return the upper case of the lc_number after trimming it.
    use before looking up an LC’s status, to clean the LC number the user typed.
    no need to use when specific lc number is not given or when general trade finance query is asked.
    example: " lc-1001 " → "LC-1001" """
    return lc_number.strip().upper() if lc_number else ""

@mcp.tool()
def search_docs(query:str)->list[str]:
    """Search for the documnets provided to answer queries related to tradefinance.
    If query is relevant search from documents for accurate answer.
    It returns labelled chunks like [label] + text.
    Use it when the query is related to trade finance for general info
    Dont use it when a specific status of LC or LG is requested."""
    labels = hybrid_top(query)
    parts = [f"[{label}]\n{CHUNK_TEXT[label]}" for label in labels]
    return parts

@mcp.tool()
def get_lc_status(lc_number: str)->dict:
    """Get the lc status using the lc_number in the format LC-1001) and returns (the LC status, or an error if not found).
    Use it when Lc status is requested for specific lc_number
    Dont use it when query is for general info."""
    message,is_error = call_spring_api.get_lc_status(lc_number)
    if is_error:
        raise ValueError(message)
    else:
      return json.loads(message)

if __name__ == "__main__":
    mcp.run(transport="streamable-http", stateless_http=True, port=8001)