# R-008 — Make the ecosystem executable

| | |
|---|---|
| **Status** | building |
| **Source** | session — Manish: *"were you just directly using your brain to build this demo, or leveraging the system that we have built"* |
| **Raw** | this conversation, 2026-10-23 |
| **Parent** | R-006, R-007 |
| **Date** | 2026-10-23 |
| **Branch** | `product-of_swarm` |

## Reading taken

The honest audit: Psalm was built directly, and the ecosystem was used as a filing cabinet. G0 was skipped, R-007 was backfilled after the work, the router never ran, and the counter agent was me grading myself.

Cause, not blame: **the ecosystem had no runtime.** Thirty markdown files describe behaviour and enforce nothing. Documents can only be followed, and under time pressure they weren't.

A rule that cannot fail a build is a preference.

## Decision

**ADOPTED.** Add `tools/swarm.py` — the executable spine:

| Command | Does |
|---|---|
| `swarm route "<problem>"` | writes a routing decision with a done-when number to `mind/conscious/decisions.jsonl` |
| `swarm gate <agent>` | runs G0 + the agent's test command; exits non-zero on failure |
| `swarm ledger <agent>` | appends a scored row to `evals/ledger.csv` |
| `swarm new <agent>` | scaffolds soul, spec, golden cases from templates |

Plus `body/<id>/agent.json` — the machine-readable contract the gate reads (soul path, golden path, done-when, test command, minimum cases).

## Ordering rule this enforces

This record was written **before** the runner was built. That is the correction, not a detail: R-008 exists at the turn the idea was spoken, and the code below cites it.

## Wrong if

- The gate passes things that are actually broken, and the team learns to ignore it. A gate that always passes is worse than none.
- Or: the gate is slow enough that it gets skipped. Budget: under 5 seconds.

## Eval

| Check | Pass |
|---|---|
| `swarm gate clinic-booking` fails while Psalm has no soul | exit 1 |
| It fails while golden cases are missing | exit 1 |
| It fails while the test command is red | exit 1 |
| It passes only when all three are green | exit 0 |
| Runtime | under 5 s |

Measured this session, on the real repo.
