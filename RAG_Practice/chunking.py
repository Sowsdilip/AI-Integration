from pathlib import Path

def chunk_size_overlap(text:str,start:int =0,over_lap: int = 50,chunk_size:int = 600 )->list[str]:
    if str is None:
        raise ValueError
    if over_lap>chunk_size:
        raise ValueError
    chunks = []
    step = chunk_size-over_lap
    chunks = [text[start:start+chunk_size] for start in range(0,len(text),step)]
        
    return chunks

if __name__ == "__main__":
    file = Path("Docs")/"letter_of_credit.txt"
    chunks = chunk_size_overlap(file.read_text(encoding="utf-8"))
    for chunk in chunks:
        print(chunk)