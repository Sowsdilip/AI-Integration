print(TOOLS["search_docs"]({"query": "What is LC?"}, "t1"))
print(TOOLS["get_lc_status"]({"lc_number": "LC-1001"}, "t2"))
print(TOOLS.get("foo"))   # None → your unknown-tool path