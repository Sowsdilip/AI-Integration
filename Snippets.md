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