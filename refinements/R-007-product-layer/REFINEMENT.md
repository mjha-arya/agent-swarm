# R-007 — A product layer: builds become sellable artifacts

| | |
|---|---|
| **Status** | built, unverified |
| **Source** | session — Manish: *"create a folder on git… named 'product of the swarms'"* |
| **Raw** | this conversation; also the job description's fifth bullet: *"Turn successful builds into reusable systems that make future delivery faster"* |
| **Parent** | R-001 |
| **Date** | 2026-10-23 |
| **Branch** | *(awaiting name)* |

## Reading taken

The three layers describe how an agent is *built*. None of them describes what is *sold*. A $30–70k clinic build is not a graph spec — it is a demo the buyer can talk to, a scorecard of what passed, and an honest list of limits.

Added `product of the swarms/` as a sibling of `soul/ mind/ body/`: one folder per shipped product.

## Decision

**ADOPTED.** `product of the swarms/README.md` and `product of the swarms/ai-voice-agent/` (the eye-care demo, moved out of `body/clinic-booking/demo/`).

## Wrong if

- The product folder drifts from the engineering folder: the demo says one thing, the golden cases test another. Then the split is worse than keeping them together.
- Or: clinic #2 costs the same as clinic #1. Then this is a portfolio, not a product line.

## Eval

Two numbers, both cheap:

| Check | Pass |
|---|---|
| Time from clone to talking demo | under 2 minutes, no credentials |
| Hours to adapt the demo to a second clinic | under 8, target under 4 |

Not yet measured. First measurement when a second clinic profile is added.
