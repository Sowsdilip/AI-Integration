text = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
chunks = []
overlap = 3
chunk_size = 10
step = chunk_size-overlap
for start in range(0,len(text),step):
    chunks.append(text[start:start+chunk_size])
print(chunks)