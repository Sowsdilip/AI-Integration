# Python Snippets

## Files
- `Path("Docs") / "file.txt"` → build one path (`/` joins paths)
- `Path("Docs").glob("*.txt")` → generator of many files; loop over it, no `.read_text()` on it directly
- `file.read_text(encoding="utf-8")` → read whole file as string

## Slicing
- `text[a:b]` → chars from a up to (not incl.) b; going past the end is safe
- `text[a:b:n]` → every nth char (step), NOT chunks

## Loops
- `range(start, stop, step)` → numbers start, start+step, … < stop
- Java `for (int i=0; i<n; i+=7)` == Python `for i in range(0, n, 7)`
- List comprehension: `[expr for x in items]` == loop + append

## Chunking
- `[text[i:i+size] for i in range(0, len(text), size - overlap)]`

## Hashing
- `hashlib.sha256(text.encode("utf-8")).hexdigest()` → stable ID; bytes needed (`.encode`); used for dedupe/cache keys

## Java → Python gotchas
- Java `String text` → Python `text: str` (name first, type hint second; not enforced)
- `str` is the built-in type — never use it as a variable name
- Validation: `if not text:` catches both None and ""

## range
- `range(5)` → 0,1,2,3,4 (stop excluded, start defaults to 0)
- `range(10, 0, -2)` → 10,8,6,4,2

## List comprehensions
- `[x**2 for x in nums]` → transform
- `[x for x in nums if x % 2 == 0]` → filter; condition at the END
- `obj.method` = the method itself; `obj.method()` = calls it

## Java (interview)
- for-each + `list.remove()` → ConcurrentModificationException
- Fix: `Iterator.remove()` or `list.removeIf(d -> d.equals("BL"))`
- `List.of()` immutable; `new ArrayList<>(List.of())` mutable copy

## Oct 16, 2026

**enumerate**
```python
for i, start in enumerate(range(0, 1000, 450)):  # i = count from 0, start = value
```

**Stable ID vs content hash**
```python
sha(f"{source}:{start}")  # id: location -> idempotent upsert
sha(chunk_text)           # hash: content -> detects change
```

**Slicing bug**
```python
text[start:size]          # wrong: absolute end
text[start:start + size]  # right
```

**Entry point**
```python
if __name__ == "__main__":  # runs only when executed directly, not on import
```

**pathlib**
```python
f = Path("Docs") / "letter_of_credit.txt"
f.read_text(encoding="utf-8"); f.name
```

**Tip:** "`[` not closed" error → check for a missing comma on the line above.

**Java:** Fail-fast (ArrayList, HashMap: modCount → CME) vs fail-safe (ConcurrentHashMap weakly consistent, CopyOnWriteArrayList snapshot). for-each is an iterator.

**Java-Python**
dict ≈ LinkedHashMap, list ≈ ArrayList, tuple ≈ immutable List.of()/record, set ≈ HashSet
tuples are hashable → usable as dict keys; lists aren't

**zip**
list(zip(a, b))              # list of tuples; index by position or unpack
dict(zip(a, b))              # key lookup
zip(a, b, strict=True)       # error on length mismatch (default silently truncates)
list[...] is a type hint, list(...) is a call

list(x) / dict(x) → create (constructor call)
obj[0] / obj["k"] → retrieve (≈ .get())
list[str] / dict[str,int] → type hint (≈ generics)

**HashMap resize and bucket treeification to redblack tree**

HashMap resize: threshold = cap × 0.75 (16 → 12); resize when size > threshold → cap doubles, entries redistributed.
Treeify: bucket ≥ 8 AND cap ≥ 64 (else resize); untreeify ≤ 6. O(n) → O(log n).
Power of 2: index = (n-1) & hash (fast modulo); on resize, entry stays at i or moves to i+oldCap (check hash & oldCap).

**sort**
sorted(items, key=lambda x: x[1]) → ascending (default); reverse=True → descending.
Similarity: reverse=True. Distance (Chroma): default ascending. [0] = best either way.
**strip**
re.split(r"\n\s*\n") → \s matches \n too, greedy → whole blank-line gap = 1 separator, no empty items.
split("\n\n") = exact match only; splitlines() = every \n.
**split**
 Still strip()+filter for leading/trailing blanks.

 **assert**
 assert cond, "msg" → silent on pass, AssertionError on fail. Force a failure once to prove the check works.
python -O disables asserts → never use for production validation.

import: built-ins (print, len) need none; modules (re, json, os) need import.
Truthiness: "" / [] / 0 / None are False → `if current:`
Conditional expression: x if cond else y (Java ternary)
list.append(x) adds one item; list.extend(iterable) adds each item.
Fixed-size split: for i in range(0, len(s), size): s[i:i+size]; slicing past end is safe.
Guard clause: special case at loop top → handle → continue.
Never reset an accumulator without flushing it first → silent data loss.
Type hint vs value: x: list[str] = [] ✅ | x = list[str] → x is the TYPE ❌
Positional args follow signature order; keyword args (name=value) avoid order bugs.
Naming: snake_case in Python; don't put types in names (records, not list_chunks_dict).
if __name__ == "__main__": main() → runs only when executed directly; imported module's top-level code runs on import.
pytest: test_*.py files, test_* functions, plain assert; run `pytest -v`.
python -O disables asserts → not for production validation (use raise ValueError).
a, b = [], "" → tuple unpacking.

# 1. Pull one field from a list of dicts (Java: stream().map().collect())
ids   = [r["id"] for r in records]
metas = [{"source": r["source"], "chunk_index": r["chunk_index"]} for r in records]

# 2. append vs extend (Java: add vs addAll)
a.append([1, 2])   # [[1, 2]]  adds the list as ONE item
a.extend([1, 2])   # [1, 2]    adds each item

# 3. zip pairs lists by position, unpack in the for (Java: index loop with i)
for doc, meta, dist in zip(docs, metas, dists):
    ...

# 4. Chroma returns one list per query, so take [0] for a single query
res["distances"][0]          # not res["distances"]

# 5. Keyword args: positional fills parameters in order (Java has none)
search(q, verbose=True)      # search(q, True) would set k=True

# 6. Substring check (Java: b.contains(a))
"mt700" in doc.lower()

# 7. any() = at least one passes (Java: stream().anyMatch())
any(kp in doc.lower() for doc, meta, dist in hits)

# 8. Ternary (Java: cond ? a : b), value first, then condition
best = hits[0][2] if hits else None

# 9. Safe dict lookup (Java: map.getOrDefault(k, null))
item.get("key_phrase")       # None instead of KeyError

# 10. Debug a KeyError: print what's actually there
print(item["id"], list(item.keys()))

# 1. Last index of a substring (Java: s.lastIndexOf(".")), -1 if not found
cut = window.rfind(". ")

# 2. Integer division (Java int / int); "/" always gives a float in Python
half = max_size // 2      # 300, not 300.0

# 3. Slicing past the end is safe (Java substring would throw)
"abc"[1:100]              # "bc"

# 4. Omitted slice start = from 0 (Java: s.substring(0, n))
window[:cut + 1]

# 5. Don't grow the list you're looping over (Java throws CME, Python loops forever)
out = []
for p in paras:
    out.extend(get_chunks(p, 600))

# 6. import runs the whole module (Java import only names a class)
if __name__ == "__main__":   # guard top-level code like Java's main()
    main()

# 7. Quick timing (Java: System.currentTimeMillis())
import time; t = time.time(); ...; print(time.time() - t)


# 1. import a function from a module (Java: import static pkg.Cls.method)
from search_query import search     # "import search_query" gives the module, not the function

# 2. Paths relative to the script, not where you run it from
from pathlib import Path
BASE = Path(__file__).parent
files = list((BASE / "Docs").glob("*.txt"))   # glob is a generator; list() to count/reuse

# 3. Env var before import (Java: System.setProperty before class load)
import os
os.environ["HF_HUB_OFFLINE"] = "1"

# 4. Guard empty list before [0] (Java: list.isEmpty())
if not hits:
    return {"answer": "not found", "citations": [], "cached": False}

# 5. Tuple unpacking in a comprehension; _ for unused values
citations = [f"{m['source']}#{m['chunk_index']}" for _, m, _ in hits]

# 6. NamedTuple = Java record (still unpacks like a tuple)
from typing import NamedTuple
class Hit(NamedTuple):
    doc: str
    meta: dict
    dist: float

# 7. pydantic request body = Java DTO with validation
from pydantic import BaseModel
class AskRequest(BaseModel):
    question: str