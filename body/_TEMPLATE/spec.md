# <agent_id> — graph spec

The design artifact. Generated code follows this; when a run fails, this is what changes.

## State

```python
class State(TypedDict):
    run_id: str
    problem: str          # as stated
    restated: str         # one-line reading taken
    inputs: dict          # validated user figures
    missing: list[str]    # inputs still needed
    fetched: dict         # {key: {value, source, fetched_at, ttl_s}}
    computed: dict        # deterministic results only
    judgement: dict       # LLM verdicts
    answer: str
    verdict: str          # pass | needs_human
    trace: list[dict]
```

## Nodes

| # | Node | Archetype | Input state | Output state | Deterministic | Approval |
|---|---|---|---|---|---|---|
| 1 | `restate` | router | `problem` | `restated`, `missing` | no | — |
| 2 | `ask_if_missing` | human interrupt | `missing` | `inputs` | — | user |
| 3 | `fetch` | tool call | `inputs` | `fetched` | yes | — |
| 4 | `compute` | aggregator | `inputs`, `fetched` | `computed` | yes | — |
| 5 | `judge` | LLM judge | `computed` | `judgement` | no | — |
| 6 | `present` | aggregator | `computed`, `judgement` | `answer` | yes | — |
| 7 | `trace` | tool call | all | `trace` | yes | — |

## Edges

```
START -> restate -> (missing? ask_if_missing : fetch) -> fetch -> compute -> judge
judge -> (pass ? present : human_interrupt) -> present -> trace -> END
```

## Done when

A number, not an adjective. e.g. *5 of 6 golden cases pass; zero compliance violations; every figure reproducible from the trace.*

## Cost

| Item | Budget |
|---|---|
| turns | 30 |
| $/run | 1.00 |
| latency | < 20 s p50 |
