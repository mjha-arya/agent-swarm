# R-006 — Refinement ledger: ideas tracked as first-class objects

| | |
|---|---|
| **Status** | built, unverified |
| **Source** | this session — Manish: *"every time we come up with a refinement… that is how i define a refinement so we need to drag that"* |
| **Raw** | the conversation of 2026-10-22/23; no external artifact |
| **Parent** | — |
| **Date** | 2026-10-23 |
| **Branch** | `pushing-index.md-file` |

## Reading taken

Git records *what changed*. It cannot record *what was meant*, and it cannot say whether a change was an improvement. Most refinements here begin as an insight in conversation, not as a failing test — so a failure-driven loop alone misses them.

A refinement is therefore a first-class object: **an idea with an origin, a reading, a decision, a falsifier, and an implementation.** One refinement may span many commits; one commit may implement none.

Three registers, one ID:

| Question | Register |
|---|---|
| What was the idea? | `refinements/R-00X/REFINEMENT.md` |
| What changed in the repo? | git commits citing `R-00X` |
| Did it improve anything? | `evals/ledger.csv` |

## Decision

**ADOPTED.** Added `refinements/INDEX.md`, six records, `body/fin-data/evals/ledger.csv`, `.gitattributes`.

Rules adopted:
- An ID is assigned the turn the idea is spoken, not after the build.
- The raw origin is copied verbatim into `source/` and never paraphrased.
- `Wrong if:` is mandatory. No falsifier means it is a preference, not a refinement.
- Rejected and deferred refinements stay forever, with the reason.
- Any `raw` row older than 7 days is decided or dropped, weekly.
- Branch names are `YYYY-MM-DD-two-or-three-words`; the ID lives in the commit message.

## Wrong if

- `INDEX.md` is never read, and refinements pile up in `raw`. That is the expected failure mode, and the 7-day rule is the only thing standing against it.
- Or: writing the record costs more than the change it describes, so real work routes around it. Then the record must get shorter, not the rule dropped.

## Eval

Measurable from day one, cheaply:

| Check | Pass |
|---|---|
| Every commit on `main` cites an `R-00X` | 100% |
| No `raw` refinement older than 7 days | 0 |
| Every `built` refinement has a `Wrong if:` | 100% |
| Every `verified` refinement has a ledger row | 100% |

First measurement: 2026-10-30, on this ledger itself.
