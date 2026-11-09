# Swarm — an agentic ecosystem

Not a single agent. The **environment** agents live, interact and improve in — the analogue of what DeepMind built for models, built for agents instead.

Source of intent: [`VISION.md`](VISION.md) (verbatim, untouched).
Mechanics: [`CONTRACT.md`](CONTRACT.md) — read this before adding anything.
Definitions: [`LAYERS.md`](LAYERS.md). Tooling: [`STACK.md`](STACK.md).

## The three layers

```
soul/    what an agent IS        essence, binding, rarely changes
mind/    how agents RELATE       collective mind / conscious / unconscious
body/    what an agent RUNS      graph, spec, code, golden cases
```

A problem statement enters at the top and leaves as one answer. `mind/` decides who works on it and what they already implicitly know; `body/` does the work; `soul/` constrains what any of them is allowed to be.

## Current state

| Item | State |
|---|---|
| Layer contract | Authored |
| One worked example (`body/fin-data/`) | Authored, not verified — no code, no run |
| Agent registry | 1 agent + 3 lineage slots |
| Golden cases | 5 for `fin-data`, unscored |
| Anything executing | Nothing. No runtime exists yet. |

## Where to start

1. Read `CONTRACT.md` §4 (the run lifecycle) — that is the whole system in seven steps.
2. Read `body/fin-data/spec.md` — the shape every future agent copies.
3. Then read `VISION.md` and check the scaffold still matches what you meant.

## Non-negotiables

- Nothing here overrides [Constitution of Agents](https://github.com/mjha-arya/constitution-of-agents/blob/main/AGENTS.md). A soul may tighten an article, never loosen one.
- `Authored` is not `verified`. No file in this tree may claim a run that did not happen.
- Every report ends with **NOT CHECKED**.
