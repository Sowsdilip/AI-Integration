
Day 1  24-09-2026 
=================
1.Created a virtual environament to run my project
**python -m venv venv**
2.activated it
**.\venv\Scripts\activate**
3. Installed pydantic,anthropic and .env packages using pip install(like maven install)
**pip install pydantic anthropic python-dotenv**
pydantic is for schema validation kind when I am expecting a json response or sending json requests it helps me validate with schema
anthropic => to connect to claude apis
.env => to store secrets 
4. created a gitingnore file to skip unwanted file commits
venv/ , .env, __pycahce__/  added these 3 to the file
5. created one basic python file hello.py
**print("Environment Working")**
6.Refreshed python basics
datatypes,list,dict,function,class

Day 2 25-09-2026
================

1. create a .env file to import secrets from an environment file instead of hardcoding in code

2.**Pydantic deep dive**
- Explored lax type coercion (`"10000.00"` silently becomes `10000` for an `int` field) vs `StrictInt`, 
  which rejects that instead — relevant for validating LLM-extracted data later
- Learned `EmailStr` validation via `pydantic[email]`
- Clarified: Python doesn't support constructor overloading like Java — one `__init__` per class; 
  use default arguments or `@classmethod` alternates instead
- Clarified: `class X(BaseModel)` is inheritance (like Java's `extends`); pydantic auto-generates `__init__` 
  from declared fields, similar to Lombok's `@AllArgsConstructor`
- Discussed how production Python teams enforce discipline Java gets for free: mypy/pyright for type 
  checking, `__slots__` to block dynamic attributes, dataclasses/pydantic as the default over bare classes, 
  linters (ruff/pylint) in CI

3.**Setup**
- Created Claude Console account (separate from claude.ai chat), added prepaid credit, set a monthly 
  spend limit under Settings → Limits, created a **Default**-scope API key, stored it in `.env`

4.  **Debugging (the real learning today)**
- Fixed a `.env` file that was accidentally named `key.env` — python-dotenv expects the literal filename `.env`
- Hit a broken venv: prompt showed `(venv)` as active, but `python`/`pip` still pointed to the global install. 
  Root-caused it with `sys.executable` and `where python`/`where pip`, then recreated the venv from scratch
- Learned: don't trust the `(venv)` prompt alone — verify with `python -c "import sys; print(sys.executable)"`


Day 3 26-09-2026
================

1. Call Anthropic api using the claude API-KEY stored in .env file
2. structure the output as a json using json.loads
3. list comprehension using forloop in 1 line
4. *args and **kwargs
5. try and except recap
6. hints,contextmanagers, optional, enum
7. difference between args and kwargs and general usecases
8. debugged issues like 
token => max_tokens, 
forgot to call load_dotenv()
forgot to give model name gave empty string ""
getting confused with : using = in that place for dict understod with example
json.load instead of json.loads through which got to know loads always looks for a string and load looks for a file as input
token uasge and pricing details
9. like try with resources in java which will take care of closures
    # file is automatically closed here, even if an error happens
    ex1.with open("data.txt", "r") as f:
    content = f.read()
    # The anthropic client itself supports this pattern for streaming responses:
    ex2.with client.messages.stream(...) as stream:
    for text in stream.text_stream:
        print(text, end="")

Day 4 27-09-2026
================

# Java Collections internals, hash collison

1. equals()/hashCode() contract — why both must be overridden together, what breaks if only one is
2. How HashMap.get()/put() actually work internally — hashCode → bucket → equals() within the bucket
3. Hash collisions — what they are, why they're normal, linked-list vs. Java 8+ treeification
4. ArrayList vs LinkedList — real performance trade-offs, corrected from your initial (wrong) assumption
5. LinkedHashMap vs LinkedList — cleared up as separate concerns (map ordering vs. list structure)
6. Thread-safety of collections — real production race condition, fully diagnosed
7. GC and collections — when GC can/can't cause missing entries

Day 5 28-09-2026
================

# FastAPI runs on uvicorn server

1. FastAPI  is a python's webframe work(like spring for java) for building APIs, popular for AI services specially because it has in-built support for async operations and automatic request/response validation using pydantic.(this is important when calling slow things like LLM apis )

2. install fastapi and uvicorn
  # pip install gastapi uvicorn
3. change port on uvicorn server if needed
  # uvicorn main:app --reload --host 0.0.0.0 --port 8001
4. used async def for learning async api calls, and how await and futures work
  

Day 6 29-09-2026
================

1. Semantic cache — concept notes

The problem it solves
Calling an LLM API costs money and time (seconds of latency) per request. If many users ask the same question worded differently, a naive cache (exact text match) misses almost all of them — "What is FastAPI?" and "Explain FastAPI to me" are different strings, so a plain dict cache treats them as two unrelated questions and calls the API twice.

The idea
Instead of matching by exact text, match by meaning. Convert each question into an embedding — a list of numbers (a vector) that represents its meaning in a way that similar-meaning text produces similar numbers, regardless of the exact words used. Then, for a new question, compare its embedding against previously stored ones. If one is close enough, reuse that stored answer instead of calling the LLM again.

Key building blocks

Embedding model: turns text into a vector (e.g. all-MiniLM-L6-v2, which you ran locally today, or an embeddings API call to a provider like Claude/OpenAI). "Similar meaning" ends up "close together" in this vector space.
Cosine similarity: the standard way to measure how close two embeddings are. Produces a score, typically 0 to 1, where 1 means identical direction/meaning, 0 means unrelated.
Threshold: a cutoff score (e.g. 0.85) above which you treat two questions as "the same" and reuse the cached answer. Too low → wrong answers get reused for unrelated questions. Too high → barely any cache hits, defeats the purpose. Tuning this is a real, non-trivial part of building one of these for production.

The basic flow

New question comes in.
Compute its embedding.
Compare against embeddings of all previously cached questions (cosine similarity).
If the best match is above the threshold → return the cached answer, skip the LLM call entirely.
If not → call the LLM for a real answer, then store the new question, its embedding, and the answer for future reuse.

Why this matters for your project specifically

Cost control: fewer LLM calls for repeated-meaning questions = lower API spend, directly relevant to the cost-control topic from the original career plan.
Latency: a cache hit returns almost instantly; an LLM call takes seconds. Big win for user experience if many questions repeat in meaning.
A genuine production pattern, not a toy exercise — real AI systems (support bots, internal Q&A tools) use exactly this to cut cost and latency at scale.

Day 7 30-09-2026
================

Notes for today

Semantic cache, next level — pydantic + real Claude integration + best-match fix

Anthropic does not offer its own embeddings model. Claude is built for generation/reasoning; Anthropic's own docs point to Voyage AI as the recommended embeddings provider. Embeddings and chat generation are handled by separate services even in a "Claude-based" system — good to know precisely rather than assume Claude does everything.
Fixed yesterday's bug: the earlier version returned the first cached entry that cleared the threshold. Today's version tracks the highest similarity score across all entries and only returns a match if that best score clears the threshold — a meaningfully more correct approach for when multiple similar entries exist.
CacheEntry(BaseModel) replaced loose tuples — same pydantic pattern from Day 1, now applied to real structured data (question, answer, embedding) instead of a toy Ticket example.
Real integration point: the ask() function is the actual usable piece — check cache first, only call Claude on a genuine miss, then store the new answer for future reuse. This is the shape a real FastAPI endpoint would wrap around.
Hit/miss stats — a simple counter ({"hits": 2, "misses": 2}) is a first, real example of the "observability/cost tracking" concept from the original career plan — proof, in numbers, that the cache is doing its job.
Real results observed:
Unrelated question ("capital of France") scored 0.091 similarity — confirms clear separation between related/unrelated content, not a fragile threshold.
Two different reworded FastAPI questions scored 0.936 and 0.900 — both cleared the 0.85 threshold, but with different scores reflecting how differently worded each was. Graduated similarity, not binary match/no-match — something a keyword-based cache could never produce.
Open discussion point, not yet resolved: two questions can be topically similar but need genuinely different answers (e.g., "cancel my order" vs "return my order"). This is a real risk in any threshold-based semantic cache, worth returning to before considering this pattern "done."

Day 8 03-10-2026
================

## Semantic Cache Service (FastAPI + Claude + sentence-transformers)

**What it does**
A FastAPI service that reduces redundant LLM calls by caching answers based on
*meaning*, not exact text. A new question is compared against previously
answered ones using embedding similarity — if a close-enough match exists
(cosine similarity above a threshold), the cached answer is reused instantly
instead of calling Claude again.

**How it works**
1. Incoming question → converted to an embedding via `sentence-transformers`
   (`all-MiniLM-L6-v2`, running locally)
2. Compared against all cached questions using cosine similarity
3. **Cache hit** (similarity > 0.85): return the stored answer, no API call
4. **Cache miss**: call Claude (`claude-haiku-4-5-20251001`), store the new
   question/answer/embedding as a `CacheEntry`, return the answer
5. `/stats` endpoint tracks hit/miss counts to measure effectiveness

**Stack**
- FastAPI + pydantic (request/response validation)
- Anthropic Python SDK (Claude API)
- sentence-transformers (local embeddings)
- NumPy (cosine similarity)

**Endpoints**
- `POST /askAI` — ask a question, get an answer (cached or fresh)
- `GET /stats` — current hit/miss counts

**Known limitation**
In-memory only — cache and stats reset on restart. Next step: persist via
Redis or a vector DB (e.g. pgvector) so the cache survives restarts and
scales beyond a single process.

**Real bugs hit and fixed while building this** (see Daily Log for details):
calling a variable instead of a class, a pydantic field-name mismatch between
class definition and usage, accidentally nesting the storage list inside the
entry class instead of keeping it separate, and a misplaced return that broke
best-match selection across multiple cache entries.

Day 9 04-10-2026
=================

1. .\venv\Scripts\activate
    # pip install pytest httpx
   pytest is a tresting framework, Pthons rough equivalent of junit
   fucntions should start with pretext test_ and use a simple assert statement 

## Testing the Semantic Cache

**What's tested**
- `cosine_similarity` — verified against known mathematical properties: identical
  vectors score 1.0, orthogonal (perpendicular) vectors score 0.0
- `find_best_match` — verified the empty-cache edge case returns no match

**Project structure (why it matters)**

Pytest fundamentals

Test functions prefixed test_, use plain assert, auto-discovered by pytest
pytest <file> runs one file; plain pytest recursively discovers and imports every test_*.py file from the current directory down — this can unexpectedly drag in slow/heavy imports from unrelated test files

Import/packaging lessons (the real depth of today)

A module's import behavior differs depending on how it's loaded — run directly as a script vs. imported as part of a package. A plain from similarity import X works standalone but fails when the same file is imported through a package path; fixed with an explicit relative import: from .similarity import X
__init__.py files mark folders as proper Python packages, enabling imports like from Semantic_Cache.module import X — the Python equivalent of Java's package/folder structure matching
Run pytest from the project root, not from inside a subfolder, so package-style imports resolve correctly

Test isolation and speed

Heavy, slow-to-import code (anything loading a large model) should be separated from pure, fast logic (cosine_similarity moved into its own lightweight similarity.py) — this alone took a test from 43s to 0.35s
cache.clear() at the start of a test prevents one test's leftover state from silently affecting another — tests should be independent and repeatable

Floating-point comparisons

== 1.0 works for clean hand-picked numbers, but real-world floating-point results can have tiny rounding errors; pytest.approx(1.0) is the safer comparison for real computed values (not needed yet, but good to remember)

Mocking — introduced, not yet implemented

find_best_match calls the real embedding model internally, making its exact output unpredictable for a test
Mocking means substituting a fake, test-controlled version of that dependency so the test becomes deterministic and isolated from the real model
Correctly identified as the next real testing skill to learn — intentionally left for a future session rather than rushed today

## Java Concurrency Refresher (for interview prep)

Covered conceptually, mapped against this week's Python concurrency work
(ThreadPoolExecutor/Futures, FastAPI async vs blocking):

- **ExecutorService + Future** — Java's thread pool + blocking `.get()`,
  direct parallel to Python's `ThreadPoolExecutor` + `.result()`
- **CompletableFuture** — non-blocking chaining via `.thenApply`/`.thenAccept`,
  but still thread-pool-based underneath, not a true single-event-loop
  runtime like Python's `async`/`await`
- **Virtual threads (Java 21+)** — JVM-managed lightweight threads; blocking
  a virtual thread doesn't tie up a real OS thread, since the JVM unmounts
  it from its carrier thread while waiting
- **Key migration caveat**: switching to `newVirtualThreadPerTaskExecutor()`
  is often a near drop-in replacement, but code that used a fixed pool size
  as an implicit resource limiter (e.g., capping DB connections) needs an
  explicit limiter (e.g., `Semaphore`) added, since virtual threads are
  effectively unbounded by default

  ## Java Concurrency Deep Dive: synchronized vs ReentrantLock, applied to a real bug

Extended the concurrency refresher by revisiting the earlier production race
condition (static map cache, multi-node, multi-thread) with the actual fix:

- Wrapping the null-check-and-reload logic in `synchronized` or `ReentrantLock`
  with **double-checked locking** (check → lock → check again → act) would
  have resolved it correctly while preserving the caching behavior
- Simpler alternative: remove the runtime reload logic entirely if nothing
  legitimately nulls the cache after initial load
- Clarified that CompletableFuture's non-blocking call style still executes
  on reused pool threads underneath — not a true single-event-loop model
- Clarified that `volatile`/locking still fully apply with virtual threads,
  since the Java Memory Model's visibility problem is about CPU cores/caching,
  not thread weight — virtual threads still run on real carrier threads

Day 10 Java concurrency Practice
================================

# Java Concurrency Practice

Small exercises on thread pools, virtual threads, and double-checked locking.
Requires Java 21+. Run with `java FileName.java`.

## PoolTiming.java
Runs two 5-second tasks on:
1. Fixed pool with 1 thread (control): ~10s
2. Fixed pool with 2 threads: ~5s
3. Virtual-thread-per-task executor: ~5s

Shows parallel execution through elapsed time and thread names.
Virtual threads shine with many blocking tasks (e.g. 10,000 x 1s sleeps).

## LazyCache.java
Lazy-loaded cache using double-checked locking with a `volatile` field.
50 virtual threads are released together with `CountDownLatch`; `load()`
should run exactly once.

Experiments:
- Without the lock and second check, `load()` runs many times.
- Without `volatile`, safe publication is not guaranteed.

## Key takeaways
- `volatile` = visibility + ordering, not atomicity.
- DCL needs: volatile field, local copy, two null checks, synchronized.
- Prefer the holder idiom or `computeIfAbsent` in new code.
- This mirrors a production bug where several threads initialized the same resource.

Day 11 semantic_cache with mock for testing and python package structure
=========================================================================

## 1. Testing with pytest and mocks (Semantic Cache)
- Fixtures: `@pytest.fixture(autouse=True)` clears the cache before and after every
  test (code after `yield` is teardown).
- Mocking the model: `patch.object(embed_model, "encode")` replaces the real model,
  so tests are fast and deterministic. Set `return_value` to control the embedding.
- The mock returns the **embedding**. The **answer** comes from the `CacheEntry`
  that `find_best_match` selects.
- Inspect a mock: `.return_value`, `.call_args`, `.call_args_list`, `.call_count`,
  `.assert_called_once()`.
- Float comparisons: use `pytest.approx(1.0)`, not `== 1.0`.
- Assert before using a value (`assert match is not None`, then `match.answer`).
- Print visibility: `pytest -s` or `pytest -rP`. Prefer asserts over prints.
- Tests I wrote: empty cache, exact match, dissimilar question, best of several.

## Run commands
```bash
java PoolTiming.java
java LazyCache.java
python -m pytest -v
python -m pytest -s -v

## 2. Python package structure

| Term | Meaning |
|---|---|
| Module | A single `.py` file |
| Package | A directory of modules, normally with an `__init__.py` |
| Import path | Where Python looks for modules (`sys.path`, starting with the script's directory or the current directory) |

Example layout:

```
project/
├── Semantic_Cache/
│   ├── __init__.py
│   └── semantic_with_fastapi.py
└── tests/
    └── test_semantic_cache.py
```

```python
from Semantic_Cache.semantic_with_fastapi import find_best_match   # absolute import
from .utils import helper                                          # relative import (inside a package)
```

Key points:
- `__init__.py` marks a directory as a regular package. It can be empty, or it can
  re-export names to shorten imports. Since Python 3.3 folders without it still work
  as "namespace packages", but adding it is clearer and avoids test-discovery surprises.
- Importing a module **executes its top-level code once**, then caches it in
  `sys.modules`. In the cache project, importing `semantic_with_fastapi` loads the
  embedding model, which is why test startup is slow.
- `if __name__ == "__main__":` runs code only when the file is executed directly,
  not when it is imported.
- Run from the project root. Use `python -m pytest` or `python -m package.module`
  so the root is on the import path. This fixes most `ModuleNotFoundError`s.
- Absolute imports are preferred. Relative imports only work inside a package.

## 3. Java classes vs Python modules

| | Java | Python |
|---|---|---|
| Unit of code | Class (everything lives in a class) | Module (a file); functions and variables can sit at top level |
| File rule | One public class per file; file name must match the class name | Any number of classes/functions per file; no name rule |
| Package | `package com.x;` declaration must match the directory path | Directory (+ `__init__.py`) |
| Import | Compile-time name lookup; runs no code | Runtime; executes the module the first time |
| Compiled form | `.class` bytecode files | `.pyc` cache, handled automatically |
| Access control | `public/private/protected/package-private` | Convention only (`_name` means "internal") |
| Singleton-like state | `static` fields, initialized when the class is first used | Module-level variables, created once on first import |

Takeaway: a Python module behaves like a Java class with only static members.
Both initialize lazily on first use, which is the same idea as the lazy cache
(and why the holder idiom works in Java).

Day 12 recap and refresh
========================

# FastAPI, Pydantic, pytest, Semantic Cache: Notes

## FastAPI
- `async def` runs on the event loop. `await` frees it for other requests.
- Plain `def` runs in a worker thread pool, so blocking calls are safe there.
- A blocking call inside `async def` freezes the whole event loop. Use `def`
  or `asyncio.to_thread(...)` for `embed_model.encode()`.
- "Invalid body returns 422 in FastAPI (400 in Spring by default); both are valid, and the handler is customizable." FASTApi build
- `Depends()` is dependency injection (shared model/cache). Tests swap it with
  `app.dependency_overrides`.

## Pydantic
- Validates and coerces at runtime: `"5"` becomes `5`; `"abc"` raises an error.
- Unlike `dict`/`dataclass`: enforced types, `model_dump()`, JSON schema for /docs.

## pytest
- Test endpoints in-process: `TestClient(app)`, no server needed.
- Fixture scopes: function (default), module, session. Use session for a slow
  read-only model, function for mutable state like the cache.
- Mock the embedding model for fast, deterministic, isolated unit tests; add a
  separate integration test with the real model.

## Semantic cache
- Threshold too low: wrong hits. Too high: needless misses.
- Tune it on labeled similar/different question pairs.
- Concurrency: identical simultaneous questions both miss (cache stampede).
  Same check-then-act race as the Java DCL bug. Fix with a lock / in-flight tracking.
- Python has no `volatile`. The GIL covers single operations, not check-then-act.
- Scaling: O(n) scan, so use a NumPy matrix, then FAISS/vector DB. Add LRU/TTL eviction.

## To revise
- `Depends()` and `dependency_overrides`
- `TestClient` basics
- HTTP status codes (400 vs 422)
- Fixture scopes with examples

# Java Collections Internals: equals/hashCode, HashMap, ConcurrentHashMap

## equals / hashCode
- Contract: equal objects must have equal hash codes. The reverse isn't required.
- hashCode picks the bucket, equals confirms the match inside it.
- Override only equals: equal objects land in different buckets, so lookups miss.
- **Override vs overload:** `equals(Point p)` does NOT override `equals(Object)`.
  HashMap/HashSet call `equals(Object)`. Always use `@Override`.
- Records (Java 16+) generate correct equals/hashCode.
- `==` compares references; `.equals()` compares per the class. `new String("a") == "a"`
  is false (heap object vs pooled literal). Always use equals for strings.
- Keys must be immutable: mutating a field used by hashCode makes the entry unfindable.

## HashMap put()
1. `hash = h ^ (h >>> 16)`  2. `index = (n-1) & hash`
3. Empty bucket: store node. Otherwise walk chain: same hash + equals means replace value; else append.
4. `++size > capacity * 0.75` triggers resize (double and redistribute).
- Capacity is a power of two so indexing is a bit mask, and resize moves entries cheaply.
- Chain of 8+ nodes with capacity >= 64 becomes a red-black tree (O(n) to O(log n)); reverts at 6.

## Thread safety
- HashMap shared across threads: lost updates, resize corruption, stale reads.
- `Hashtable` / `synchronizedMap`: one lock for the whole map.
- `ConcurrentHashMap` (Java 8+): lock-free reads, CAS for empty buckets, locks only the
  head node of one bucket otherwise. No null keys or values.
- Check-then-act still needs atomic methods: `computeIfAbsent`, `merge`.

## To revise
- Load factor and resize details
- Mutable keys in HashSet
- Write a correct equals/hashCode by hand, then compare with a record


## Phase 2: FDE Track

### Day 1 Recap (Oct 10, 2026)

Reviewed 28 gap areas from the FDE self-audit against actual knowledge, via live Q&A.

**Solid:** Idempotency, Background jobs, Webhooks, Embeddings, Retrieval relevance,
Structured outputs, Customer discovery

**Needs Refresh** (concept right, details/vocabulary thin): Retry/backoff, REST APIs,
OAuth, Model APIs (FastAPI's actual role), Tool calling, Prompt/context design,
Hybrid search, Workflow orchestration, Eval dataset design, Tool-call success rate,
Hallucination rate, Latency/cost tradeoffs, Java interview fluency, Solution design
docs, Architecture diagrams, Demo/rollout/adoption

**Real Gap** (new, no hands-on yet): SQL joins, Docker Compose, AWS managed deploy
(ECS/Fargate), RAG end-to-end (citations/groundedness), Classification accuracy,
Groundedness

**Key corrections from today:**
- Tool/function calling ≠ calling your own functions — it's the LLM requesting
  *your* code run something, via a structured `tool_use` block, then you feed the
  result back
- REST = resource URLs + stateless + standard verbs, not "uses HTTP" or "returns JSON"
- OAuth: code (front-channel, browser) vs token exchange (back-channel, server +
  client_secret) — separation protects the token from leaking via the browser
- Groundedness and hallucination rate are near-inverse metrics — both check if
  claims trace back to retrieved source text
- Hybrid search = semantic (embeddings) + keyword (BM25) combined, needed because
  pure embeddings miss exact IDs/codes

**Real Gaps feed directly into the Core Project Roadmap:**
RAG citations + hybrid search → Stage 2. Docker Compose + AWS (ECS/Fargate) →
Stage 5. SQL joins → standalone drill before Stage 2's retrieval work.

Next session: Stage 2 (RAG layer) — chunking → embeddings → Chroma → retrieve →
cite source, now with hybrid search and groundedness folded in from the start.  \

### RAG Layer(Chunking + Vector Store)

**Built**
- `chunk_document()`: fixed-size chunker with overlap
- Embedded chunks with `all-MiniLM-L6-v2` and stored them in Chroma (`PersistentClient`, cosine distance)
- Idempotent ingestion: chunk IDs = SHA-256 of `source + content`, written with `upsert`
- Paragraph-based chunker (`chunk_by_paragraph`) as an improvement

**Bugs found and fixed**
- Chunker used `end = chunk_size` instead of `start + chunk_size`, so every chunk after the first was empty
- `overlap` parameter was never used; the step is now `chunk_size - overlap`
- `import chunk_function` imported the module, not the function, so calling it failed (`TypeError: 'module' object is not callable`); fixed with `from chunk_function import chunk_document`
- `chunk_index` metadata was a fixed value, so every result showed `#1` (still to fix)

**Learnings**
- Fixed-size chunking (500 chars) split Section 6 in two, so the "pinning" answer ranked 3rd
- Paragraph chunking kept the section whole: the top hit improved (distance 0.516 → 0.495)
- Stale data: re-ingesting with a new chunker left the old chunks in the store. Changing the chunking strategy means clearing the collection first
- Duplicate check = `collection.count()` before and after ingest, not chunk sizes
- Printing only `doc[:80]` hid correct results; always inspect full chunks

**Next**
- Split into `ingest.py` / `query.py` / `rag.py`
- Fix `chunk_index`, clear the collection, re-ingest, rerun the test questions
- Add delete-by-source for stale chunks

### Oct 11, 2026: RAG Layer, Day 2 (Code Structure + Answer Generation)

**Java practice (new daily habit)**
- Q: HashMap put() internals and resize → 6/10. Mixed up resize (total entries > capacity × 0.75 → table doubles)
  with treeify (one bucket > 8 entries and capacity ≥ 64 → red-black tree)
- Follow-up: mutable keys → 6/10. Missed the main point: changing the hashCode leaves the entry in its old bucket,
  so get()/remove() can't find it (unreachable entry, memory leak)

**Built**
- Split code into `rag.py` (model, collection, ingest, search), `ingest.py` (run when docs change), `query.py` (question loop)
- Fixed `chunk_index` metadata (was a constant), cleared stale chunks, printed full chunks
- Distance threshold (`max_distance`) so search returns only relevant chunks, not always k results
- `answer.py`: retrieved chunks → Claude API → JSON `{answer, citations}`
- Skip the LLM call when retrieval finds nothing (no cost, no made-up answer)
- API key loaded from `.env` via python-dotenv; `.env` added to `.gitignore`

**Bugs and lessons**
- Empty results: `query.py` ran before `ingest.py`. Query never loads data, so a guard prints "store is empty"
- `delete_collection` doesn't belong in shared code; it would wipe the data on every import
- Threshold filter wasn't applied because the loop still iterated the raw results instead of `hits`
- Code changes need a script restart; a running loop keeps the old code
- `$env:` is PowerShell syntax; cmd uses `set VAR=value` and only applies to that window
- `AttributeError: 'ThinkingBlock' object has no attribute 'text'`: the response content is a list of blocks,
  so filter by `type == "text"` instead of using `content[0]`
- Defensive JSON parsing: strip ```json fences, fall back to raw text instead of crashing
- Prompt fix ("complete answer", "partial answer if partly covered"): the pinning answer now includes the ReentrantLock fix

**Results (4 test questions)**
| Question | Result |
|---|---|
| What is a virtual thread? | ✅ Correct, cites #5 (Section 6, 0-based index) |
| Explain Kafka | ✅ Not found, no API call |
| What is pinning? | ✅ Complete after prompt fix |
| Load factor + treeification | ❌ False negative: blocked at retrieval (threshold), LLM never called |

**Open issue**
- Multi-part question embeds far from each individual section. Next: check distances; tune the threshold,
  or use query splitting / hybrid search (BM25) next week

**Next**
- Q3 distance diagnostic + threshold tuning
- Delete-by-source on re-ingest
- 10–15 question eval set (retrieval hit rate)


## Oct 12, 2026 — Phase 2, Day 3 (light day)

### Retry with exponential backoff
- Retry only transient errors: 429, 529, 5xx, timeouts. Never 400/401.
- Delay = min(max_delay, base * 2^attempt) + random jitter
- Jitter prevents many clients retrying at the same time
- Always cap max attempts and max delay
- Java equivalent: Spring `@Retryable` + `@Backoff(multiplier = 2)`
- Semantic cache project: retry the Claude API call; for the cache,
  fail open (skip cache on error, call API directly) instead of retrying
- Similarity threshold tuning = hit quality, not reliability

### HashMap vs ConcurrentHashMap
- HashMap: not thread-safe; fail-fast iterators (throw ConcurrentModificationException)
- ConcurrentHashMap (Java 8+):
  - Empty bucket → CAS insert (no lock)
  - Occupied bucket → `synchronized` on first node only
  - Reads mostly lock-free → scales well for read-heavy loads
  - Weakly consistent iterators (no CME)
- No null keys/values: `get()` returning null would be ambiguous
  (absent vs null value), and `containsKey()` + `get()` isn't atomic
  across threads

### Pending
- Write `call_with_retry()` in plain Python + test with a fake failing function

## Oct 13, 2026 — Phase 2, Day 2

### Retry with backoff (implemented)
- Built `call_with_retry()` in plain Python: loop + try/except per attempt
- Exit on success with `return`; re-raise on last attempt; no sleep after final attempt
- Delay = min(max_delay, base * 2^attempt) + random.uniform(0, 0.5) → ~1s, 2s, 4s
- Retry only `TransientError`; anything else (e.g. ValueError) propagates immediately (fail fast)
- Tested: fails twice then succeeds ✅ | always fails → raises after 4 attempts ✅

### Python lessons learned
- Custom exception: `class TransientError(Exception): pass` (like `extends RuntimeException`)
- Exception raised inside an `except` block is NOT caught by a sibling `except` (same as Java)
- Can't raise a string — only exception objects
- `raise X(...) from e` keeps the original cause (like Java's `new Exception(msg, cause)`)
- Pass a function without `()` → `fn` (like `this::method`); `fn()` calls it immediately
- Function needing args: `lambda: call_claude_api("prompt")` or forward `*args, **kwargs`
- Python runs top to bottom: a name must exist at the moment the call runs (Java compiles whole class first)
- Convention: snake_case, not camelCase
- In production: decorators (`@retry`), the `tenacity` library, or the SDK's built-in retries
  (`anthropic.Anthropic(max_retries=4)`)

### Idempotency
- Idempotent = doing it twice has the same effect as doing it once (GET/PUT/DELETE yes, POST no)
- Fix for POST: client sends an `Idempotency-Key` (UUID); server stores processed keys and
  returns the saved response on repeats
- Client must generate the key ONCE and reuse it on every retry
- Without server support: do a status inquiry (check by client reference) before retrying
- Claude API call: safe to retry (no side effects), but costs tokens and wording may differ
- Claude doesn't cache answers — my semantic cache does
- Becomes critical with tool calling: the tool wrapper (MCP layer) generates the key;
  the Spring API enforces it (unique constraint + stored response)

### Java: equals()/hashCode() contract
- equal objects → MUST have equal hashCodes; unequal objects MAY collide
- Only equals() overridden → equal keys land in different buckets → get() returns null, duplicates
- Only hashCode() overridden → same bucket, but identity equals never matches → same problems
- Bucket lookup order: hash → `==` → equals()
- Java 8+: bucket with more than 8 nodes → red-black tree (O(n) → O(log n))
- Keys should be immutable: mutating a hashed field after put() makes the entry unfindable

### Carry-over from Oct 12: done ✅

## Oct 14, 2026: RAG Layer, Step 1 (Ingest)

**Done**
- Built folder ingest: reads all `.txt` files from `docs/` with `pathlib`, then chunks, embeds (all-MiniLM-L6-v2), and upserts each one into Chroma
- Made ingest idempotent: SHA-256 IDs from `source:index:chunk`, plus delete-by-source before upsert so stale chunks are removed when a doc changes
- Guard for empty files (`if not chunks: return`)
- Switched the collection to cosine distance (`hnsw:space: cosine`)
- Verified: 4 docs → 17 chunks; re-run → added=0

**Learned**
- `enumerate` (index + item), slicing `d[:150]`, `Path.glob` / `read_text`, `if __name__ == "__main__"`
- Chroma's `query_texts` uses its own embedding model, so use `query_embeddings` with the same model as ingest
- Delete + upsert isn't atomic

**Found**
- One chunk is 1,130 chars, near MiniLM's ~256-token limit, so its tail may be truncated. Add a max chunk size later.

**Java Q of the day:** HashMap vs LinkedHashMap vs TreeMap. Gap: TreeMap (sorted, O(log n), NavigableMap) and the LinkedHashMap LRU cache.

**Next:** retrieval test with 3 queries, then pass the top-k chunks to Claude (generation).

### Oct 15, 2026 — RAG: Chunking layer 

**What I built**
- `chunk_size_overlap(text, overlap, chunk_size)` — splits text into fixed-size chunks with overlap
- Ran it on `Docs/letter_of_credit.txt`

**What I learned**
- Chunking: documents are split before embedding because models have input limits and smaller chunks retrieve more precisely
- Overlap: repeats a few characters between chunks so ideas on a boundary aren't cut in half
- `range(0, len(text), step)` with `step = chunk_size - overlap` controls where each chunk starts
- Slice step (`text[a:b:n]`) picks every nth char, it does NOT chunk text

**Open question**
- Keep or drop tiny leftover chunks at the end?

**Next**
- Return chunks as dicts `{id, text, start, end, hash}`
- Sentence-aware chunking (don't cut mid-sentence)

**Evening practice**
- `range()` never includes the stop value (like `i < n` in Java); default start is 0; negative step counts down
- List comprehensions: `[value for x in items if condition]` — value in front, filter at the end
- Bug I hit: `word.upper` (method object) vs `word.upper()` (call)
- Bug I hit: `[x % 2 == 0 for x in nums]` gives booleans; filter belongs after `if`
- Rewrote chunker as a one-liner comprehension

**Java question: ConcurrentModificationException**
- Removing from a list inside for-each → CME (iterator's modCount check fails)
- `new ArrayList<>(List.of(...))` is mutable; `List.of(...)` alone is immutable
- Edge case: removing the 2nd-to-last element doesn't throw; the loop exits early and silently skips the last element
- Fixes: `Iterator.remove()` or `list.removeIf(...)`

### Oct 16, 2026 — Chunk records with stable IDs

**Built**
- `make_chunk(text, source, size=500, overlap=50)` returns a list of dicts built with one list comprehension:
  `{id, text, start, end, hash, source, chunk_index}`
- `id` = sha256 of `source:start` (stable location → idempotent upsert)
- `hash` = sha256 of chunk text (detects content change)
- Added `main()` behind `if __name__ == "__main__":`

**Bug fixed**
- Sliced with `text[start:size]` instead of `text[start:start+size]`, so every chunk after the first was empty and had identical hashes. Chunk 0 hid the bug because `start=0` makes both slices the same.

**Finding**
- Same-length edit → only the containing chunk's hash changes.
- Length-changing edit → every later chunk's hash changes (positions shift); IDs stay the same.
- Takeaway: fixed-size chunking is position-sensitive; paragraph/sentence-aware chunking would limit re-embedding.

**Java Q:** Fail-fast vs fail-safe iterators. ArrayList/HashMap check modCount and throw CME; ConcurrentHashMap is weakly consistent; CopyOnWriteArrayList iterates a snapshot.

**Next:** tail-duplicate edge case, split chunker/ingest/query, Chroma upsert, delete-by-source, eval set.

## Day 8 — Sat Oct 17, 2026 · Paragraph-aware chunking (redo from scratch)

**What I built**
- `split_into_paras`: regex split on blank lines (`\n\s*\n`) + strip/filter
- `merge`: greedy merge up to `max_size`; oversized paragraphs fall back to fixed-size slicing
- `make_record`: stable id `sha(source:i)` + content hash; chunking and record-building now separate functions
- `main()` with `__name__` guard; asserts for max size, no empty chunks, id/hash stability

**Bugs I hit and fixed**
- Checked `len(current)` instead of `len(candidate)`, so chunks could exceed the limit
- Empty chunk pushed when the first paragraph was oversized
- Data loss: reset `current` without flushing it first
- Stability assert compared records with itself (could never fail)
- `chunks = list[str]` assigned the type instead of an empty list
- Literal `"source"` as source name → would collide ids across files

**Lessons**
- Trace loops with a table before trusting output
- Guard clause at loop top → handle special case → `continue`
- Test special cases at first / middle / last positions
- A test must be able to fail

**Java:** HashMap resize (threshold 12), treeify (≥8 nodes AND cap ≥64), power-of-2 indexing

**Also:** created the "FDE phase" Claude Project with STATUS.md for daily continuity

**Next:** eval set (12 Qs incl. not-found), re-ingest, Claude answer + citations

