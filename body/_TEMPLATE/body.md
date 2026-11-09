# body/ — what an agent RUNS

Copy this folder to `body/<agent_id>/` and fill it in. Nothing here is code yet: the spec comes first, and code is generated from the spec, never typed node by node.

## Files

| File | Purpose | Written by |
|---|---|---|
| `body.md` | wiring: runtime, tools, state, cost, failure behaviour | the builder |
| `spec.md` | the node table — the actual design artifact | the builder |
| `graph.mmd` | the same graph as a Mermaid diagram | the builder |
| `evals/golden.jsonl` | input → ideal output cases | **human, from real expert answers** |
| `code/` | implementation, generated from `spec.md` | builder, then reviewed |

## Order of work

1. `spec.md` first — if the table cannot be filled, the agent is not designed.
2. `graph.mmd` to match. If the diagram and the table disagree, the table is right.
3. `evals/golden.jsonl` — 5 cases minimum, ≥1 edge, ≥1 adversarial.
4. Only then code. Fix the *spec* when a run fails, not the code.

## Node archetypes

Almost every node is one of five. Keep one template per kind and stop inventing:

| Archetype | Deterministic? | Typical use |
|---|---|---|
| tool call | yes | fetch, query, read a file |
| LLM judge | no | compliance, relevance, grounding |
| router | yes | branch on state, ask the user |
| human interrupt | — | approval, missing input, low confidence |
| aggregator | yes | assemble the final answer |

## Runtime

Per `../STACK.md`: LangGraph for the auditable spine, Pydantic AI for typed tool calls *inside* nodes, `uv` for the env, Postgres only when persistence is proven necessary. No second orchestrator.

## Non-negotiables

- Deterministic work is code. If a number in the answer was produced by a model, that is a defect.
- Every agent has `--dry-run`.
- Every run writes a trace before it answers.
- Status starts at `authored`, never `verified`.
