# Refinements — index

The dashboard. One row per refinement. This is the only file you read weekly.

**What a refinement is:** a change to *how the ecosystem works*, born from an insight, a failure, a defect or something read. It is not a commit. One refinement can span many commits; one commit can implement zero.

## Status flow

```
raw → interpreted → decided → built → verified
                     ├─ rejected   (stays forever, with the reason)
                     └─ deferred   (stays, with the condition that revives it)
```

A refinement is `raw` the moment it is spoken. **Any `raw` row older than 7 days gets decided or dropped, weekly.**

## Index

| ID | Title | Source | Parent | Status | Branch | Date |
|---|---|---|---|---|---|---|
| [R-001](R-001-soul-mind-body/REFINEMENT.md) | Three-layer ecosystem: soul / mind / body | scratch file + session | — | built, unverified | `pushing-index.md-file` | 2026-10-22 |
| [R-002](R-002-unconscious-is-derived/REFINEMENT.md) | The unconscious is derived context, not an actor | R-001 | R-001 | adopted | — | 2026-10-22 |
| [R-003](R-003-one-gate-ladder/REFINEMENT.md) | One gate ladder G0–G5, replacing three review systems | R-001 | R-001 | adopted | — | 2026-10-22 |
| [R-004](R-004-souls-human-only/REFINEMENT.md) | Souls are human-only writable | R-001 | R-001 | adopted | — | 2026-10-22 |
| [R-005](R-005-constitution-precedence/REFINEMENT.md) | Precedence runs through the Constitution | R-001 | R-001 | adopted | — | 2026-10-22 |
| [R-006](R-006-refinement-ledger/REFINEMENT.md) | Refinement ledger: ideas tracked as first-class objects | session | — | built, unverified | `pushing-index.md-file` | 2026-10-23 |
| [R-007](R-007-product-layer/REFINEMENT.md) | A product layer: builds become sellable artifacts | session + job description | R-001 | built, unverified | `product-of_swarm` | 2026-10-23 |
| [R-008](R-008-executable-gates/REFINEMENT.md) | Make the ecosystem executable — gates that fail a build | session audit | R-006, R-007 | built, unverified | `product-of_swarm` | 2026-10-23 |
| [R-009](R-009-dct-databricks-mcp/REFINEMENT.md) | DCT: a product whose first backbone is a spec, not a build | session | R-007, R-008 | authored — spec gated, runtime not executed | `2026-10-27-databricks-mcp` | 2026-10-27 |

## How to add one

1. **Same turn it is spoken** — get an ID and a stub folder. Ideas at midnight do not survive to morning.
2. **Copy the origin verbatim** into `source/`. Never paraphrase the raw. The gap between what you meant and what got built is the whole value.
3. **Write `Wrong if:`** — if nothing could falsify it, it is a preference, not a refinement.
4. **One ID, four places:** branch name is `YYYY-MM-DD-slug`, and the commit message, `LOG.md` entry and trace all cite `R-00X`.

## Naming

Branches: `YYYY-MM-DD-two-or-three-words` (ISO date first, so the list sorts chronologically).
Refinement IDs: `R-00X`. Folders: `R-00X-short-slug/`.

The branch name carries the date. The ID carries the idea. They meet in the commit message.
