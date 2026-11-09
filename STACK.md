# STACK.md — decisions, not a wish list

Every entry is marked **DECIDED** (you said it), **PROPOSED** (my reading of your note), or **UNVERIFIED** (named from memory — check before use). Nothing here is installed.

| Concern | Choice | State | Note |
|---|---|---|---|
| Agent graphs | LangGraph | DECIDED | `VISION.md` line 1; studio debugging per the pipeline doc |
| Graph debugging | LangGraph Studio | DECIDED | line 17 |
| Agent runtime / tool layer | Pydantic AI | DECIDED | line 11 — overlaps LangGraph; see conflict below |
| Python env | `uv` (astral) | DECIDED | line 11 |
| Datastore | Postgres | DECIDED | line 11 |
| Durable workflows | DBOS | PROPOSED | written "deboss" in the vision — almost certainly DBOS |
| Durable workflows (alt) | Hatchet | DECIDED as an option | line 11 names both; pick one before building |
| UI | Streamlit | DECIDED | line 47 |
| Open-weight models | GLM 5.3, DeepSeek 4.1 Flash | DECIDED | line 11; DeepSeek V4.1 Flash is what this session runs on |
| Coding agent | OpenCode | DECIDED | line 11; this session is OpenCode-only |
| Smoke testing only | yes | DECIDED | line 11 — but see the tension below |
| Spec-driven | spec → agent.md | DECIDED | line 11 |
| `opencode .sh` / `omp.sh` / `reddit#` | — | UNVERIFIED | not resolvable as written; likely shell wrappers you already have |
| Google SecOps | — | UNVERIFIED | line 11; no role stated yet |
| pi coding agent | — | UNVERIFIED | line 11 |

## Conflicts to settle before the first build

1. **LangGraph vs Pydantic AI.** Both are agent frameworks. Pick one as the spine. My read: LangGraph for the auditable graph (gates, human interrupts, Studio traces), Pydantic AI only for typed tool/validation calls *inside* nodes. Don't run two orchestrators.

2. **DBOS vs Hatchet.** Same category, both named. DBOS is Postgres-native and you already chose Postgres — that argues DBOS. Hatchet is stronger for cross-service queues. Decide at first durable workflow, not now.

3. **"Only do smoke testing" vs the gate taxonomy.** Smoke tests satisfy G1 and part of G2. They cannot satisfy G3 (semantic) or G4 (adversarial). If smoke-only stands, the swarm can prove *it runs*, never *it is right* — and the golden cases become decoration. Recommendation: smoke tests on every change, full golden suite before any claim of "done".

4. **Open-weight models vs model choice last.** The vision names GLM 5.3 and DeepSeek 4.1 Flash up front. The playbook says choose the model after the golden set exists. Both can hold: name the *candidate pool* now, pick within it once `fin-data` is scored.

## Not yet chosen

- Message transport between agents (file bus / Postgres LISTEN-NOTIFY / Hatchet)
- Vector store for semantic memory
- Trace backend (raw JSONL is assumed until volume argues otherwise)
- Scheduler and budget model for autonomous runs
- Where the Streamlit UI reads from
