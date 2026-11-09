from mcp.server.mcpserver import MCPServer
mcp = MCPServer("mcp application")

@mcp.tool()
def normalize_lc_number(lc_number:str|None = None)-> str:
    """Clean up an LC number: trim spaces and uppercase it.
    return empty if it is None else return the upper case of the lc_number after trimming it.
    use before looking up an LC’s status, to clean the LC number the user typed.
    no need to use when specific lc number is not given or when general trade finance query is asked.
    example: " lc-1001 " → "LC-1001" """
    return lc_number.strip().upper() if lc_number else ""

if __name__ == "__main__":
    mcp.run()