# CONTRACT.md — the mechanics of the swarm

`VISION.md` says *what* the ecosystem is. This file says *who reads what, who may write it, and in what order*. Without this, soul/mind/body is a taxonomy, not an architecture.

**Precedence, highest first:**

1. What Manish says in the session
2. `Constitution-of-Agents/AGENTS.md`
3. This file
4. `soul/<agent>.soul.md`
5. `mind/**`
6. `body/**`

A soul may tighten a Constitution article. It may never loosen one. Code that disagrees with a settled decision is a bug.

---

## 1. Ownership matrix

| Path | Written by | Read by | When |
|---|---|---|---|
| `soul/<id>.soul.md` | **human only** (or an accepted PROPOSAL) | that agent, every run | always, first |
| `mind/collective-mind.md` | human | router + every participating agent | start of any multi-agent run |
| `mind/conscious/router.md` | human | router | per run |
| `mind/conscious/gates.md` | human | gates | per gate evaluation |
| `mind/conscious/decisions.jsonl` | router, append-only | humans, auditors | per run |
| `mind/unconscious/priors.md` | **automatic, filtered** | all agents, implicitly | per run, silently |
| `mind/unconscious/memory-bus.md` | human (schema) + filtered writer | memory bus | per read/write |
| `mind/state/agents.json` | human + status updates | router | per run |
| `body/<id>/body.md`, `spec.md`, `graph.mmd` | that agent's builder | that agent's builder | at build time |
| `body/<id>/evals/golden.jsonl` | **human (real expert answers)** | gates | G0 onward |
| `runs/<run_id>.jsonl` | runtime, append-only | eval, priors builder | after every run |

Three hard consequences:

- **No agent writes its own soul.** The essence is only changed by a human or an accepted proposal. This is what makes "original essence" mean something.
- **No agent writes another agent's body.** Cross-agent edits go through a proposal.
- **The unconscious is never authored by an agent deliberately.** It is *derived*. See §3.

---

## 2. What belongs in each layer

| Layer | Belongs | Does not belong |
|---|---|---|
| `soul` | purpose, method, hard rules, `needs_human`, return format, lineage | tool names, versions, prompts, current prices |
| `mind` | routing, typed messages, shared tool registry, gate criteria, priors | any single agent's implementation detail |
| `body` | graph, node table, code paths, fixtures, golden cases | policy, identity, anything another agent depends on |

If a fact would still be true after the agent is rewritten, it is soul. If it would still be true after one agent is deleted, it is mind. Otherwise it is body.

---

## 3. The collective unconscious, mechanically

The vision calls it the part "I don't even understand". It is not mystical; it is **the context an agent receives without choosing to consult it.**

| Stratum | Mechanism | Traceable? | Binding? |
|---|---|---|---|
| **Conscious** | Router picks agents, writes a plan, logs the choice | yes, full log | yes |
| **Unconscious** | Priors + retrieved memory silently attached to the prompt | derived from traces | **never** |

The unconscious is built from four sources only:

1. **Reputation** — per-agent pass rate per category, from `runs/*.jsonl`.
2. **Episodic priors** — "last 3 times this problem type appeared, X worked, Y looped".
3. **Semantic memory** — user facts and preferences (auto-writable).
4. **Cache priors** — fresh tool results with a TTL; stale ones are dropped, not softened.

**Rule: nothing in the unconscious is binding.** It can shape a choice, never justify one. An inference becomes a rule only through `PROPOSALS.md` and a human yes — exactly as the Constitution's memory stack requires.

---

## 4. The run lifecycle

Every problem statement takes this path. Seven steps, no shortcuts.

```
1 INTAKE        problem recorded, run_id assigned
2 ROUTE         conscious: which agents, which tools, what "done" means  -> decisions.jsonl
3 CONDITION     unconscious: priors + memory attached, silently
4 EXECUTE       body: agent runs its graph; code for math, LLM for judgement
5 GATES         G1..G5 applied; failure returns to the owning layer
6 TRACE         runs/<run_id>.jsonl written
7 WRITE-BACK    filtered; only survivors reach the unconscious
```

**Step 2 output is a plan, not an answer.** If the router cannot name a "done when" number, the run stops at intake.

**Step 7 filter** — most traces stay history. Some become eval cases. Only a small subset becomes memory:

| Signal | Destination |
|---|---|
| New failure mode | `evals/golden.jsonl` (new case) |
| Repeated fact about the user | semantic memory (auto) |
| Better method discovered | `PROPOSALS.md` (max 2 open, human yes) |
| Nothing notable | history only |

---

## 5. The single gate taxonomy

`VISION.md` names a counter agent, the force-agent gates, and a list of evals. These are the **same gates**. One list:

| Gate | Question | Owner | Cost | Blocks |
|---|---|---|---|---|
| **G0 Brief** | Does a spec, 5 golden cases and a done-when number exist? | human | free | any code |
| **G1 Deterministic** | Schema, format, PII, and — for money — the arithmetic | code | cheap | G2 |
| **G2 Behavioural** | Right tool? loops? duplicate calls? turn budget? | code | cheap | G3 |
| **G3 Semantic** | Grounded, relevant, safe — judge is a *different* model | LLM judge | medium | G4 |
| **G4 Adversarial** | A read-only counter agent tries to prove the work wrong | counter agent | medium | any "done at scale" claim |
| **G5 Governance** | Blast radius, audit trail, owner, approvals, cost | human | free | ship |

Rules:
- G0 comes before code. No golden cases → the artifact is `DRAFT: no eval` and stops.
- G4 is the "counter agent" from the vision. It reviews, it does not patch — the parent patches.
- Review loops are bounded at **2** returns, then escalate.
- CI runs a subset on every prompt change; the full suite runs on merge.
- Model choice happens *after* the golden cases exist, never before.

---

## 6. Invariants

Violating any of these is a defect, not a trade-off.

1. No agent writes its own soul.
2. No agent writes another agent's body.
3. Nothing in the unconscious is binding.
4. Code does mechanics, the LLM does judgement.
5. A run without a trace did not happen.
6. `Authored` is never reported as `verified`.
7. Every outward action — post, email, deploy, schedule — needs an explicit yes.
8. The router never invents an agent that is not in `agents.json`.
9. A reviewer reviews. The parent patches.
10. When unsure, report UNSURE. Never round a gap in your own favour.

---

## 7. What this contract does not yet settle

- **Inter-agent message transport.** File bus, Postgres, or Hatchet? Unresolved — see `STACK.md`.
- **How agents "have a life of their own"** (VISION line 11). Persistence and scheduling are undecided; nothing here assumes autonomy.
- **The ecosystem-level eval.** Per-agent golden cases exist. Whether the collective beats a single agent is not yet measured anywhere.
