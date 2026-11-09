# fin-data — body

The reference implementation. Every later agent copies this shape.

| Item | Value |
|---|---|
| Soul | `../../soul/fin-data.soul.md` |
| Runtime | LangGraph (spine) + Pydantic AI for typed tool calls |
| Env | `uv`, Python 3.12, venv outside OneDrive (`%USERPROFILE%\.venvs\swarm-fin`) |
| Persistence | none yet — JSONL traces only; Postgres only when proven necessary |
| Model | undecided by design; candidate pool GLM 5.3 / DeepSeek 4.1 Flash, chosen after G0 scoring |
| Status | **authored, not verified** — no code exists |

## Graph

See `graph.mmd` for the diagram and `spec.md` for the node table. The table is authoritative.

```
restate → [ask_if_missing] → fetch → compute → judge → [human_interrupt] → present → trace
```

## Tools

| Tool | Kind | Access | TTL |
|---|---|---|---|
| `fetch:market-rates` | read, external | shared | 24 h |
| `compute:projection` | pure function | shared module | n/a |
| `compute:fee-drag` | pure function | shared module | n/a |
| `trace:write` | write, `runs/` only | private | n/a |

No write tools outside `runs/`. No outward tools.

## Deterministic / LLM split

| Concern | Owner | Why |
|---|---|---|
| contributions, growth, fee drag, inflation adjustment | code | arithmetic must be reproducible |
| restating the question | LLM | language |
| compliance (guidance vs advice) | LLM judge, **different model** | judgement |
| assembling the answer | code, from computed values | prevents invented figures |
| wording | LLM, constrained to computed values | language |

**The check that matters:** every number in the answer must be traceable to a `compute:` entry in the trace. A number that appears only in prose is a defect at G1.

## Failure behaviour

| Failure | Action |
|---|---|
| Missing input | one question, wait — never assume |
| Fetch fails once | retry once, then `needs_human` with the exact missing input |
| Fetch fails twice identically | stop; read the input, don't retry a third time |
| Compliance judge ≠ PASS | refuse the advice, return the decision framework, `needs_human` |
| Confidence < 0.6 | human interrupt |
| Budget exhausted | partial answer + NOT CHECKED |

## Trace fields

`run_id, restated, inputs, fetched[{key,source,fetched_at,ttl_s}], computed, judgement{model,verdict,reasons}, answer, gates{g1,g2,g3,g4}, cost{turns,usd,ms}`

## How it is proved

| Gate | Test |
|---|---|
| G0 | `evals/golden.jsonl` — 6 cases, 2 edge, 2 adversarial |
| G1 | schema check + **independent recomputation** of every figure |
| G2 | tool-call count, no duplicates, ≤ 30 turns |
| G3 | separate-model judge: grounded, relevant, safe |
| G4 | read-only counter agent tries to elicit advice or a guaranteed return |
| G5 | blast radius named (a wrong number about someone's money), owner, audit trail |

## Status history

| Date | Event |
|---|---|
| 2026-10-22 | authored: soul, spec, graph, golden cases. No code. |
