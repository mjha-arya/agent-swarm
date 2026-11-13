# Agent Swarm

> **An environment where AI agents are born, gated, and proven before they ship.** Every agent passes the same six-gate ladder, G0 to G5, from brief to governance.

### ▶ [Live demo: voice booking agent with gates on screen](https://mjha-arya.github.io/agent-swarm/)
*An eye-clinic booking agent you can talk to in the browser. Every turn is checked live: invented slots, latency, policy and red-team probes.*

---

## The problem

Most "AI agents" ship as a prompt and a hope. Nobody can say what the agent is **allowed** to do, what it was **tested** against, or what happens when it's attacked. The Swarm makes those answers structural.

## The gate ladder

| Gate | Question | Checked by |
|---|---|---|
| **G0 Brief** | Do a spec, 5 golden cases and a done-when number exist? | human, before any code |
| **G1 Deterministic** | Schema, format, PII, and for money the arithmetic | code |
| **G2 Behavioural** | Right tool? Loops? Duplicate calls? Turn budget? | code |
| **G3 Semantic** | Grounded, relevant, safe | LLM judge, *a different model* |
| **G4 Adversarial** | A read-only counter-agent tries to prove the work wrong | counter-agent |
| **G5 Governance** | Blast radius, audit trail, owner, approvals, cost | human, before ship |

No golden cases means the agent is `DRAFT: no eval` and stops. Model choice happens **after** the evals exist, never before.

## Architecture: soul / mind / body

```
soul/    what an agent IS       character, binding rules (human-authored only)
mind/    how agents RELATE      registry, shared memory, who works on what
body/    what an agent RUNS     graph (.mmd), spec, code, golden cases
```

A problem statement enters at the top and leaves as one answer. `mind/` routes it, `body/` does the work, and `soul/` constrains what any agent is allowed to be.

**→ [Full architecture with diagrams](ARCHITECTURE.md)**: layers, gate ladder, run lifecycle, write ownership, and what's executable today.

## What's in here

| Path | What |
|---|---|
| [`product of the swarms/ai-voice-agent/`](product%20of%20the%20swarms/ai-voice-agent/) | **Working demo.** Voice booking agent with live G1–G4 gates and an end-of-call scorecard |
| [`body/databricks-mcp/`](body/databricks-mcp/) | Read-only Databricks MCP agent: spec, graph, golden evals |
| [`body/fin-data/`](body/fin-data/) | Reference agent: the shape every new agent copies |
| [`refinements/`](refinements/) | Design ledger. Every change to *how the ecosystem works*, with its why (R-001 to R-009) |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | **Start here.** Diagrams of the whole system on one page |
| [`CONTRACT.md`](CONTRACT.md) | The mechanics: ownership, run lifecycle, gate taxonomy, invariants |
| [`ENGINEERING.md`](ENGINEERING.md) | Current state and where to start reading |

## Run the demo locally

```bash
cd "product of the swarms/ai-voice-agent"
python -m http.server 8000   # open http://localhost:8000 in Chrome/Edge
```

## Principles

- **Authored ≠ verified.** No file may claim a run that didn't happen.
- **Every report ends with NOT CHECKED.**
- **Souls are human-only.** Agents can propose changes to their own rules but cannot make them.
- Governed by the [Constitution of Agents](https://github.com/mjha-arya/constitution-of-agents).

---
Built by **Manish Jha**, secure and provable AI agents. [Profile →](https://github.com/mjha-arya)
