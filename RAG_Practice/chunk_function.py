def chunk_by_size(text:str, chunk_size: int =500, overlap: int =50) -> list[str]:
    if(overlap>chunk_size):
        raise ValueError("overap sixe must be lesser than chunk size")
    step = chunk_size-overlap
    chunks =[]
    start = 0
    while start < len(text):
        end = start+chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = start+step
    return chunks

def chunk_by_paragraph(text:str,max_size: int = 1200) -> list[str]:
    paragraphs =[p.strip() for p in text.split("\n\n") if p.strip()]
    chunks,current = [],""
    for p in paragraphs:
        if len(current) + len(p) > max_size and current:
            chunks.append(current)
            current = p
        else:
            current = f"{current}\n\n{p}" if current else p 
    if current:
        chunks.append(current)
    return chunks
