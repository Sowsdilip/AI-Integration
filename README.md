
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