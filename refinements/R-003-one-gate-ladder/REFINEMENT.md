# R-003 — One gate ladder G0–G5, replacing three review systems

| | |
|---|---|
| **Status** | adopted |
| **Source** | VISION.md lines 3–5 + `forge-agent` skill + production playbook |
| **Raw** | *"Based on key params and evals such as tracing, memory, self learning, golden test cases, TTL caching, model optimisation improve the agents… Build a counter agent which will validate the entire code against the point 3 params"* / *"The force-code agent skill is good which has multiple gates"* |
| **Parent** | R-001 |
| **Date** | 2026-10-22 |
| **Branch** | — |

## Reading taken

Three review systems were named — a counter agent, the force-agent gates, and a list of evals — and they overlapped almost completely. Three overlapping reviewers means a defect can be "somebody else's gate".

Collapsed into one ladder: **G0 Brief → G1 Deterministic → G2 Behavioural → G3 Semantic → G4 Adversarial → G5 Governance.** G4 *is* the counter agent.

## Decision

**ADOPTED.** `mind/conscious/gates.md` is now the only gate list; everything else references it.

## Wrong if

- A defect slips through all six, or the same defect is caught twice by different gates — either means the boundaries are drawn wrong.
- Or: the ladder is too expensive to run, so it gets skipped in practice. Then it needs collapsing to three.

## Eval

Proxy: every production failure must map to exactly one gate. If a failure maps to none, add a gate. If it maps to two, merge them.
