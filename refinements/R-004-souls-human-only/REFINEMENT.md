# R-004 — Souls are human-only writable

| | |
|---|---|
| **Status** | adopted |
| **Source** | R-001 — "the original essence of the agents" |
| **Raw** | VISION.md line 41: *"one will be the soul.md file which will contain the original essence of the agents"* |
| **Parent** | R-001 |
| **Date** | 2026-10-22 |
| **Branch** | — |

## Reading taken

"Original essence" is only meaningful if something cannot overwrite it. An essence any agent can edit is a config file with a grander name.

Adopted rule: **no agent writes its own soul, or another agent's body.** Change requires a human edit or an accepted `PROPOSALS.md` entry.

## Decision

**ADOPTED.** `CONTRACT.md` §1 and §6, `soul/_TEMPLATE.soul.md`.

## Wrong if

- Souls ossify: an agent keeps making the same mistake because the fix needs a human who isn't there. Then the rule is too strict and needs a reviewed auto-path.
- Or: souls churn so often that "essence" is a fiction — then the layer should be renamed and the immutability dropped.

## Eval

Proxy: count soul edits per month. More than ~2 per agent per month means the layer is mis-scoped, not that the lock is wrong.
