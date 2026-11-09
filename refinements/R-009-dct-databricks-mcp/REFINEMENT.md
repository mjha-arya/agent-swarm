# R-009 — DCT: a product whose first backbone is a spec, not a build

| | |
|---|---|
| **Status** | authored (gate green on the spec; runtime not executed) |
| **Source** | session — Manish: *"New product for the swarm: DCT (Databricks Control Tool). Build it USING the swarm ecosystem, not around it."* |
| **Raw** | this conversation, 2026-10-27 |
| **Parent** | R-007 (product layer), R-008 (executable gates) |
| **Date** | 2026-10-27 |
| **Branch** | `2026-10-27-databricks-mcp` |

## Reading taken

DCT (Databricks Control Tool) is a **product**, not a demo: it lets an engineer operate a Databricks estate as themselves, from an assistant, with every call auditable. Its first backbone is a local stdio MCP server, `databricks`, already proven end to end against UAT on 2026-10-16.

The spec for that server exists and is reproducible. The temptation is to paraphrase it into the ecosystem's house style — which would destroy the only thing that makes it worth keeping: it is the configuration that actually worked.

## Decision

**ADOPTED.** DCT becomes `product of the swarms/dct/`. The Databricks MCP server becomes `body/databricks-mcp/`, with:

| Artifact | Rule |
|---|---|
| `spec.md` | **verbatim**, byte-identical to the attached source. Enforced by sha256 in `agent.json`, not by good intentions. |
| `body.md` | wiring: runtime, transport, auth, tools, failure behaviour, status |
| `graph.mmd` | mirrors the spec's moving parts |
| `evals/golden.jsonl` | 12 contract cases, each citing the section it comes from |
| `evals/verify_spec.py` | G1: proves the spec is intact and the cases cover §7 and §9 |

Gates are derived from the spec's own acceptance checks (§9) and safety design (§7). The spec is the done-when; the gate reads it.

## The rule this creates

**A preserved artifact is proven by hash, not by trust.** If `spec.md` drifts, G1 fails. Paraphrase is a silent edit; a hash is not.

Second rule: **a spec-only body may pass G1 and still not be built.** The gate says `runtime not executed` and the status stays `authored`. Claiming otherwise is the exact failure R-008 was written to prevent.

## Wrong if

- The hash check is satisfied by re-stamping `agent.json` after an edit. It must compare against the **recorded source digest**, so a re-stamp is a visible, reviewable change rather than a silent one.
- Or: the 12 cases read as prose rather than as assertions — then they are decoration, and G1 is a spellcheck.

## Eval

| Check | Pass |
|---|---|
| `spec.md` sha256 equals `agent.json.spec_sha256` | exit 0 |
| Any character in `spec.md` changed | exit 1 |
| A §7 safety clause removed from the spec | exit 1 |
| A §9 acceptance check has no golden case | exit 1 |
| Fewer than 12 cases, or no edge/adversarial case | exit 1 |
| Runtime claims in the report | never — printed as `not run` |

Measured this session, on the real branch.
