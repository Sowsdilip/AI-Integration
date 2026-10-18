# STATUS — FDE Phase 2 (update at end of every session)

_Last updated: Sat Oct 17, 2026 (Day 8)_

## Goal
- AI integration / Forward Deployed Engineer (FDE) roles; start applying Jan 2027
- One evolving core project: semantic cache ✅ → **RAG layer (now)** → tool calling / MCP over Spring API → reliability (retry, idempotency) → security / deploy (Docker + AWS basics) → eval harness → solo project

## Milestones
| By | Milestone |
|---|---|
| Oct 31 | RAG end-to-end with citations (light week Oct 24–30, guests) |
| Nov 20 | Tool calling / MCP over Spring API + retry/idempotency (before wedding) |
| Dec 23 | Deploy + small eval harness + README / demo video |
| Jan 2027 | Start applying |

## This week: Oct 12–18 (RAG layer)
**Done**
- Split ingest.py / query.py ✅
- Fix chunk_index ✅
- Delete-by-source for stale chunks ✅
- Retry/backoff + idempotency (Oct 13) ✅
- Paragraph chunker: split_into_paras + merge with oversized-paragraph fallback ✅
- make_record (stable id = sha(source:i), content hash) + asserts (max size, non-empty, stability) ✅

**Pending**
- [ ] Re-ingest letter_of_credit.txt with the new paragraph chunker
- [ ] Eval set: 10–15 questions with expected answers (incl. 2–3 "not found")
- [ ] Claude API answer with citations + "not found" handling
- [ ] FastAPI /ask with semantic cache in front
- [ ] Deliverable: /ask returns JSON answer + citations; cache hit skips RAG

## Files
- ingest.py: ingest docs into Chroma (cosine), delete-by-source + upsert
- query.py: retrieval queries
- make_chunk.py: `sha` helper, fixed-size chunker (with overlap)
- chunker.py: paragraph chunker (split_into_paras, merge, make_record, main)
- Docs/letter_of_credit.txt: main ingestion doc

## Known notes / limitations
- Index-based ids shift if a paragraph is inserted earlier; content hash + delete-by-source handle it for now
- Later: sentence level between paragraph and character split (recursive chunker); move asserts to pytest (test_chunker.py)

## Daily routine
- Weekdays ~1 hr (mornings before work); weekends up to 4 hrs
- Every day: Python refresh (used in project code next session) + 1 Java interview question
- Java questions done: equals/hashCode, HashMap vs ConcurrentHashMap, HashMap/LinkedHashMap/TreeMap, ConcurrentModificationException, fail-fast vs fail-safe, HashMap resize/treeify/power-of-2
- Next Java question: ConcurrentHashMap internals

## How to mentor me
- Concise answers; detail only when I ask
- Hints before code; let me write it myself; review my code for bugs
- Give daily snippets inline in chat (I paste into my own snippets.md)
- Timebox: if a step goes past 2 sessions, ship "good enough" and move on

## Upcoming breaks
- Oct 24–30: guests (light study)
- ~Nov 22: wedding (~10 days off)
- Dec 24 – Jan 7: guests (partial)
- SAP BTP basics only after the wedding (~30 min weekends/holidays)

## End-of-session update (1 min)
1. Move finished items to Done (use the plan's exact wording)
2. Add carry-overs to Pending
3. Update "Last updated" + next Java question
