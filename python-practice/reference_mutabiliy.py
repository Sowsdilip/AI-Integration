cache = [("what is UCP 600?", "answer A")]
backup = cache

cache.append(("what is an LC?", "answer B"))
print(len(backup))              # line 1

cache = []
print(len(backup))              # line 2

backup.clear()
print(len(cache), len(backup))  # line 3


cache = []
hits = 0

def lookup(q):
    global hits
    if q in cache:
        hits += 1
        return "hit"
    cache.append(q)
    return "miss"

print(lookup("LC"))
print(lookup("LC"))