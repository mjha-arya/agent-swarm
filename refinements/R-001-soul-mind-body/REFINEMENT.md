# R-001 — Three-layer ecosystem: soul / mind / body

| | |
|---|---|
| **Status** | built, unverified |
| **Source** | scratch file `Swarm` + this session |
| **Raw** | [`source/VISION.md`](source/VISION.md) — sha256 `3d3726…74e7`, 3,606 bytes, unedited snapshot |
| **Parent** | — |
| **Date** | 2026-10-22 |
| **Branch** | `pushing-index.md-file` (originally `scaffold/soul-mind-body`, PR #1, merged `f3f0572`) |

## Raw, in the author's words

> "i have this ecosystem that i want to build for agents. it will have three layers… one will be the soul.md file which will contain the original essence of the agents… the second layer of architecture would be the mind.md files… the third layer would be the body.md files, a set of files that has the layout of the agent, the python scripts, and everything within those individual agents: the actual body. it basically mimics the experience of all human beings that have experience."

## Reading taken

The unit is not an agent, it is an **environment**. Three questions that are normally mixed get separated:

- what an agent *is* → `soul/`
- how agents *relate* → `mind/`
- what an agent *runs* → `body/`

The mind splits three ways: a container (collective mind), a deliberate planner (collective conscious), and a derived, non-deliberate stratum (collective unconscious).

## Decision

**ADOPTED.** Spawned four sub-refinements — R-002 (unconscious mechanism), R-003 (gate ladder), R-004 (soul write-lock), R-005 (precedence) — because a vision is not one decision, it is a tree of them.

## Wrong if

- A single agent with one file solves the same class of problems at lower cost and lower confusion.
- Or: the three layers cannot be kept in sync, so `soul` and `body` drift and the contract becomes fiction.

## Built

`v0.2.0` — 26 files. `CONTRACT.md`, `LAYERS.md`, `STACK.md`, `README.md`, one reference agent (`body/fin-data/`), templates for both soul and body.

## Eval

**NONE.** No golden case can test an architecture yet. This is the honest gap: R-001 is adopted on argument, not evidence. The first evidence arrives when `fin-data` is scored and when a second agent is added — if the second agent needs no new layer, the anatomy held; if it needs a fourth, the anatomy was wrong.
