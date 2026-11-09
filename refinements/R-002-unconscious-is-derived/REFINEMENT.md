# R-002 — The unconscious is derived context, not an actor

| | |
|---|---|
| **Status** | adopted |
| **Source** | R-001 — the vision left it undefined ("or somehow, I don't even understand") |
| **Raw** | VISION.md line 45: *"the collective unconscious would be it figuring it out, talking to the internet, or somehow, i don't even understand"* |
| **Parent** | R-001 |
| **Date** | 2026-10-22 |
| **Branch** | — |

## Reading taken

The vision defines the unconscious by what it *isn't* able to explain. Left literal, it becomes an agent with no trace, no budget and no owner — which is the one thing the contract forbids.

Mechanism adopted: **the unconscious is the context an agent receives without choosing to consult it** — reputation, episodic priors, semantic memory, cache priors. It has no goals and takes no actions.

## Decision

**ADOPTED.** Recorded in `CONTRACT.md` §3, `mind/unconscious/priors.md`, `mind/unconscious/memory-bus.md`.

## Wrong if

- Agents measurably need to *decide* to consult memory, i.e. implicit attachment causes worse routing than explicit lookup.
- Or: priors leak into decisions as justification rather than influence — then it must be removed, not tuned.

## Eval

Not yet measurable. Proxy: when `fin-data` runs, check whether any answer cites a prior as evidence. One occurrence = the boundary failed.
