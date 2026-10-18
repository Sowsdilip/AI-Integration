# Rebalanced 14-week plan (Oct 17, 2026)

Based on Sowmya's weekly plan table (Oct 17), STATUS.md milestones, the gap analysis and known breaks.
Times: weekdays ~1 h, weekends up to 4 h. Each study day also has the daily Python refresh + the next Java topic from the STATUS.md list.

## Why rebalance

| Issue | Effect | Fix |
|---|---|---|
| Guests Oct 24–30 | Week 2 weekend and most of Week 3 are light | Pull Week 2 work into weekdays; Week 3 weekdays = reading only |
| Wedding ~Nov 22 (~10 days off, assumed ~Nov 19–28) | Weeks 6–7 mostly lost (~18 h) | Merge orchestration into tool-calling weeks; cut items already "solid" |
| Guests Dec 24–Jan 7 | Weeks 11–13 mostly lost | Put low-focus work (CV, LinkedIn, company list, Java refresh, STAR stories) there |
| STATUS.md milestones differ | Plan has MCP by Nov 1, deploy by Nov 29, eval Dec 6 | Align to STATUS: RAG Oct 31, tool calling/MCP Nov 20, deploy + eval + demo Dec 23 |
| Gaps not covered | SQL joins, docker-compose, ECS/Fargate, classification accuracy | Added below |
| Already solid per gap analysis | Webhooks/HMAC, background jobs, idempotency | Trimmed to a short recap, no full weekend |
| Separate capstone week | No time for a second project | The trade-finance RAG + tools service *is* the capstone; write its design doc |
| K8s in Week 7 | Not a stated gap; costly | Drop hands-on K8s; know the concepts only |

## Week 1 remainder (updated Oct 17 evening)

**Sat Oct 17 (done, 2.5 h):** paragraph chunker redo with oversized fallback, make_record, asserts. Java: HashMap resize/treeify.

**Sun Oct 18 (~4 h, ~3 h left in the Week 1 budget)**, ship good enough:
1. Re-ingest all 4 docs; run the existing eval set (`/mnt/project-files/eval/lc_eval_set.py`): hit@4 + distances. With 4 docs ingested, use `answered_by` for the not-found questions (1 h).
2. answer.py: `search` returns `(doc, meta, dist)`; distance threshold for "not found" from the eval distances; validate citations against ids sent (1.5 h).
3. FastAPI `/ask` (plain `def`), semantic cache in front, Pydantic response with `answer`, `citations`, `cache_hit` (1.5 h).

Moved to Mon Oct 19: don't cache failures, clear the cache on ingest, README Phase 2 entry.

Done when: `/ask` returns JSON answer + citations; second identical call shows `cache_hit: true`. Still meets the Oct 31 RAG milestone early.

## Week 2 (Oct 19–25): Better retrieval, guests from Sat

| Day | Task (1 h unless noted) |
|---|---|
| Mon 19 | Week 1 carry-over: don't cache failures, clear cache on ingest, README Phase 2 entry (hit@4, not-found accuracy) |
| Tue 20 | `eval_retrieval.py`: one command, hit@k for vector baseline and BM25 (`rank_bm25`) |
| Wed 21 | Hybrid: merge both rankings with Reciprocal Rank Fusion; hit@k |
| Thu 22 | Before/after table in README; note which questions each method wins (keyword vs semantic) |
| Fri 23 | SQL joins drill 1: INNER vs LEFT vs FULL on two small tables (sqlite3 in Python) |
| Sat 24 (guests, ~1 h) | Read only: cross-encoder re-ranking (what, when worth the latency) |
| Sun 25 (guests, ~30 min) | Update STATUS.md actual hours |

Re-ranking moves to stretch. Done when: README has the baseline vs BM25 vs hybrid hit@k table.

## Weeks 3–14 (rebalanced)

| Wk | Dates | Focus | Done when |
|---|---|---|---|
| 3 | Oct 26–Nov 1 | Weekdays (guests, 30 min): Claude tool-use docs, MCP concepts. Sat–Sun: Claude calls one Spring REST endpoint via tool use | Claude answers using the live API |
| 4 | Nov 2–8 | Wrap the Spring API as an MCP server; Python MCP client. SQL joins drill 2 | Same question works via MCP |
| 5 | Nov 9–15 | Orchestration lite: route RAG vs tool (LLM-driven branching), step trace log; retry + backoff + jitter, timeouts | One query uses docs + API, with a trace; survives an injected failure |
| 6 | Nov 16–18 | Light before wedding: rate-limit handling, structured errors, fallback. Recap idempotency/webhooks (already solid) | Nov 20 tool calling/MCP milestone met |
| 7 | ~Nov 19–28 | Off (wedding) | |
| 8 | Nov 29–Dec 6 | Docker + **docker-compose** (API + Chroma/Redis); secrets via env; prompt-injection basics | `docker compose up` runs the whole stack |
| 9 | Dec 7–13 | AWS: **ECR + ECS Fargate**, IAM role, secrets in SSM/Secrets Manager; OAuth/JWT on the API (concepts + one protected route) | Service reachable on AWS, no secrets in code |
| 10 | Dec 14–20 | Eval harness: hit@k, groundedness, hallucination rate, not-found + routing **classification accuracy / precision / recall**, tool-call success rate, latency/cost per query. Start solution design doc (eval, privacy, cost sections) | One command produces an eval report |
| 11 | Dec 21–23 | Demo video (3 min), architecture diagram, polished README, design doc done | Dec 23 milestone: deploy + eval + demo |
| 12 | Dec 24–Jan 3 (guests) | Low-focus: CV rewrite, LinkedIn headline, Dubai company shortlist (20+), STAR stories, Java core refresh | CV + LinkedIn live, target list |
| 13 | Jan 4–10 | Guests until Jan 7: Java/system-design refresh. Jan 8–10: first 5–10 applications, referral outreach, one mock interview | First applications sent |
| 14+ | Jan 11 on | Applications + mocks (AI system design, explain capstone in 10 min); keep one small build going | |

## Cut or deferred
- Hands-on K8s (concepts only).
- Redis worker queue (FastAPI BackgroundTasks for ingestion is enough; background jobs already solid).
- Separate capstone build (current project is the capstone).
- Cross-encoder re-ranking (stretch, only if Week 2 finishes early).
