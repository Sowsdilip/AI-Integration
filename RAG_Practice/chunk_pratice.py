from pathlib import Path
import re

def split_into_paras(text:str)->list[str]:
    cleaned_text = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    return cleaned_text

def get_chunks(para, max_size):
    start = 0
    chunks = []
    while start<len(para):
        window = para[start:start+max_size]
        if start+max_size>=len(para):
            chunks.append(window.strip())
            break
        else:
            cut = window.rfind(". ")
            if cut < max_size//2 or cut == -1:
                cut = window.rfind(" ")
                if cut == -1:
                    cut = max_size-1
            chunks.append(window[:cut+1].strip())
            start += cut+1

    return chunks

def merge(paras,max_size:int = 1000)->list[str]:
    chunks:list[str] = []
    current = ""
    for para in paras:
        if len(para)>max_size:
            if current:
                chunks.append(current)
                current = ""
            chunks.extend(get_chunks(para,max_size))
            #chunks.extend(para[i:i+max_size] for i in range(0,len(para),max_size))
            continue
        candidate = f"{current}\n\n{para}" if current else para
        if len(candidate)<=max_size:
            current = candidate
        else:
           if current:
                chunks.append(current)
           current = para
    if current:
        chunks.append(current)
    return chunks

def main():
    max_size = 600
    file = Path("Docs")/"letter_of_credit.txt"
    text = file.read_text("utf-8")
    paras = split_into_paras(text)
    chunks = merge(paras, max_size) 
    i = 1
    for chunk in chunks:
        print(f"{i}:  {chunk}")
        i += 1

if __name__ =="__main__":
    main()