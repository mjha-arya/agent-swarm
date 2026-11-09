# fin-data — graph spec

Design artifact. Code follows this. A failing run changes this file, not the node code.

## State

```python
class State(TypedDict):
    run_id: str
    problem: str
    restated: str
    inputs: dict            # principal, monthly_contribution, years, growth_assumption, fee_pct, inflation_pct
    missing: list[str]
    fetched: dict           # {key: {value, source, fetched_at, ttl_s}}
    computed: dict          # {nominal_low, nominal_high, real_low, real_high, contributions, growth, fees_paid}
    judgement: dict         # {model, verdict, reasons}
    answer: str
    verdict: str            # pass | needs_human
    trace: list[dict]
```

## Nodes

| # | Node | Archetype | Input state | Output state | Deterministic | Approval |
|---|---|---|---|---|---|---|
| 1 | `restate` | router | `problem` | `restated`, `inputs`, `missing` | no | — |
| 2 | `ask_if_missing` | human interrupt | `missing` | `inputs` | — | user |
| 3 | `fetch_rates` | tool call | `inputs` | `fetched` | yes | — |
| 4 | `compute_projection` | aggregator | `inputs`, `fetched` | `computed` | **yes** | — |
| 5 | `compute_fee_drag` | aggregator | `inputs` | `computed` | **yes** | — |
| 6 | `compliance_judge` | LLM judge | `restated`, `computed` | `judgement` | no | — |
| 7 | `refuse_advice` | human interrupt | `judgement` | `answer`, `verdict` | — | — |
| 8 | `present` | aggregator | `computed`, `judgement` | `answer` | yes | — |
| 9 | `trace` | tool call | all | `trace` | yes | — |

## Edges

```
START -> restate
restate -> ask_if_missing        [if missing]
restate -> fetch_rates           [else]
ask_if_missing -> fetch_rates
fetch_rates -> compute_projection -> compute_fee_drag -> compliance_judge
compliance_judge -> present      [if verdict == PASS]
compliance_judge -> refuse_advice [else]
refuse_advice -> trace
present -> trace -> END
```

## Conditional logic (deterministic, in code)

| Branch | Condition |
|---|---|
| ask | any of `monthly_contribution`, `years`, `principal` absent |
| refuse | judge finds a personal recommendation, a single-figure projection, a guaranteed-return implication, or hidden fees |
| present | judge PASS |

## Output contract

Always, in this order: **range** (low–high, nominal and real) → **contributions vs growth** as separate lines → **fees** and **inflation** as visible line items → **basis** (figures + fetch timestamps) → **NOT CHECKED**.

## Done when

**6 of 6 golden cases pass, zero compliance violations, and every figure in every answer is reproducible from its trace.**

## Cost

| Item | Budget |
|---|---|
| turns | 30 |
| $/run | 1.00 |
| latency | < 20 s p50 |
| tokens | < 40k |

## Deliberately absent

- Any node that recommends an action.
- Any LLM-produced number.
- Any write outside `runs/`.
- Any network call without a TTL.
