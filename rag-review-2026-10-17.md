# RAG layer review (Oct 17)

Hints only, no code. Ordered by your Pending list. Files reviewed are the uploads; where STATUS.md says something is already fixed (chunk_index, delete-by-source), I skipped it.

## 1. Re-ingest with the paragraph chunker

- **Mid-word splits.** I ran your `merge(split_into_paras(text), 600)` on all four docs. Every doc has one paragraph over 600 chars, and the hard slice cuts words: letter_of_credit.txt chunk 2 ends in `"A transf"` and chunk 3 starts `"erable LC allows..."`. ucp600 leaves a 98-char orphan tail. Hint: in the oversized branch, cut at the last sentence end (`". "`) before `max_size` instead of at a fixed index. This is the "sentence level" step already in your Later list; it is small enough to do now.
- **Two chunkers exist.** `chunk_function.chunk_by_paragraph` (old) has no oversized fallback and ignores the 2 chars of `"\n\n"` when checking size. Make sure `ingest()` imports `merge` from chunker.py, then delete the old one so nothing drifts back.
- **`chunk_by_size`:** the guard is `overlap > chunk_size`, so `overlap == chunk_size` makes `step = 0` and loops forever. Think about which comparison you want. Also notice the last 1–2 chunks are fully contained in the previous one.
- **Use your content hash.** `make_record` computes `hash` but nothing reads it. Store it in metadata; on re-ingest you can skip re-embedding chunks whose hash didn't change. Good thing to talk about in interviews (cost of re-indexing).
- **Ingest all 4 docs, not just letter_of_credit.** Your eval set needs distractor docs, otherwise retrieval looks perfect for free.

## 2. Eval set

- Format idea: one JSONL line per question with `question`, `expected_source`, `expected_chunk_index` (or a key phrase that must appear in the retrieved chunk), and `should_answer: true/false`.
- Mix: ~4 single-fact, ~3 that span two chunks (e.g. "difference between a confirming and advising bank"), ~2 across docs (LC vs bank guarantee), 2–3 not-found. Make one not-found a **near miss** (in-domain but absent, e.g. typical LC fees at a specific bank) and one fully off-topic.
- Measure retrieval first, separately from Claude: hit@k (is the expected chunk in the top k?). Then answer quality, then not-found accuracy.
- Log the distance of every hit. You need those numbers for item 3.

## 3. answer.py (citations + not found)

- **Bug: `search` returns nothing.** The `search` in the uploaded code prints and returns `None`, and takes no `verbose` arg. `ask()` calls `search(question, verbose=False)` and unpacks `(doc, meta, dist)`. Check your current `search` returns that list.
- **Bug: "not found" never triggers on retrieval.** Chroma always returns k results if the collection has ≥k chunks, so `if not hits` is only true for an empty DB. Hint: drop hits above a distance threshold, and pick the threshold from the eval-set distances (where do answerable vs not-found questions separate?).
- **Validate citations.** Claude can cite an id that wasn't in the context. Hint: compare `citations` against the set of ids you actually sent, and drop or flag the rest.
- `parse_json` only handles a leading code fence. If the model adds a sentence before the JSON it falls back. Prefill or structured output would remove the parsing problem entirely; worth reading about.
- The prompt example `"sample.txt#5"` is from the old doc; update it so the model mimics the real id format.

## 4. FastAPI /ask behind the semantic cache

- **Stale cache after re-ingest.** If a doc changes, cached answers still cite old chunks. Hint: put a corpus version (or ingest timestamp) in the cache key or clear the cache on ingest.
- **Don't cache failures.** Skip caching "model did not return valid JSON" fallbacks and API errors. Decide deliberately whether "Not found" should be cached.
- **Blocking call.** The Anthropic client in answer.py is sync. Inside `async def` it blocks the event loop; either use a plain `def` endpoint or `AsyncAnthropic`.
- **Import side effects.** Loading the model and Chroma client at import is fine, but check nothing at module level deletes or wipes the collection (the old `client.delete_collection("docs")` would wipe the DB every time the API starts, and raises on a fresh DB).
- Return a Pydantic response model with `answer`, `citations`, and a `cache_hit` bool. That last field makes your deliverable ("cache hit skips RAG") demonstrable.

## FDE portfolio angle

What makes this stand out is the eval table, not the RAG itself: a README row like (numbers illustrative) "hit@4 = 0.9, not-found accuracy 3/3, threshold 0.45 chosen from data" plus the cache hit rate. Trade finance is a good domain choice: it is a real enterprise use case with strict rules (UCP 600), which is exactly the kind of customer FDEs get sent to.
