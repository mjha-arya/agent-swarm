# Gates — the single taxonomy

The vision names three overlapping review systems: a counter agent, the force-agent gates, and a list of evals. They are one ladder. This file is the ladder; everything else references it.

## The ladder

```
G0 Brief ──> G1 Deterministic ──> G2 Behavioural ──> G3 Semantic ──> G4 Adversarial ──> G5 Governance
   no code        cheap              cheap               medium          medium              human
```

| Gate | Question | Pass criterion | Owner | Blocks |
|---|---|---|---|---|
| **G0 Brief** | Is there a spec, 5 golden cases, and a done-when number? | all three exist; ≥1 edge, ≥1 adversarial case | human | any code |
| **G1 Deterministic** | Does it parse, and is the arithmetic right? | schema/regex valid; **money recomputed independently**; no PII in output | code | G2 |
| **G2 Behavioural** | Did it behave sanely? | right tool; no loops; no duplicate calls; within turn budget | code | G3 |
| **G3 Semantic** | Is it grounded, relevant, safe? | judge = a **different** model from the primary; groundedness + relevance + safety all pass | LLM judge | G4 |
| **G4 Adversarial** | Can a hostile reader break it? | read-only counter agent finds no unaddressed defect | counter agent | "done at scale" |
| **G5 Governance** | Is it safe to ship? | blast radius named; audit trail present; owner named; approvals wired; cost projected | human | ship |

## Rules

1. **G0 before code.** No golden cases → the artifact is `DRAFT: no eval` and work stops.
2. **Order matters.** A wrong answer that took three DB calls is a cost defect — catch it at G2, not G4.
3. **The judge is never the primary model.** Self-review at G3 is theatre.
4. **G4 reviews, it does not patch.** The parent patches. A reviewer that edits loses its independence.
5. **Loops are bounded at 2.** A third return is an escalation, not a retry.
6. **G1 for money is non-negotiable.** Every figure in a finance answer is recomputed by a separate code path from the one that produced it. Validating arithmetic against the code that computed it proves nothing.
7. **Smoke tests are G1 only.** They prove it runs. They cannot prove it is right. A claim of "verified" requires G3 and G4.
8. **CI runs a subset per change; the full suite runs on merge.**
9. **A production failure becomes a golden case** before the fix is merged. Categories (security, compliance, data, latency) so regressions map to problem types.
10. **Model choice happens after G0.** With a golden set, picking a model is a measured run. Without one it is weeks of debate.

## What G4 (the counter agent) checks

Read-only. It is given the artifact and the gate criteria, never the author's reasoning.

- Re-reads the source, does not trust the manifest that drove the work.
- Recomputes every number by an independent path.
- Tries to make the agent give advice, leak PII, or assert a guaranteed return.
- Checks the trace: did every claim in the answer come from a logged step?
- Outputs `VERDICT / DEFECTS / EVIDENCE / NOT CHECKED`. No prose.

## Status vocabulary

| Status | Means |
|---|---|
| `DRAFT: no eval` | no golden cases; nothing may be claimed |
| `Authored, not verified` | written, never run against the golden set |
| `Verified (<date>, <score>)` | full ladder passed, score recorded |
| `Needs human` | blocked on a decision, with the exact question |

Never promote a status without the run that justifies it.
