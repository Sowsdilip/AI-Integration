from chunk_function import chunk_by_size

chunks = chunk_by_size("a"*1000,500,50)
for chunk in chunks:
     print(len(chunk))
