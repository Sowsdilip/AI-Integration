import asyncio
from mcp import Client

URL = "http://127.0.0.1:8001/mcp"


async def mcp_client():
    async with Client(URL) as client:
        tools = await client.list_tools()
        response = await client.call_tool("get_lc_status", {"lc_number": " lc-1001 "})
        print(response)


asyncio.run(mcp_client())
