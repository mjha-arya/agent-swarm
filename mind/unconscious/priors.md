# The collective unconscious — priors

The derived stratum. **Context an agent receives without choosing to consult it.**

It has no goals, takes no actions, and can never justify a decision. It only shifts what feels plausible. That is enough to matter, and it is the honest boundary.

## The four sources

### 1. Reputation
Per agent, per problem category, from `runs/*.jsonl`:

```
fin-data / projection questions / 12 runs / 10 pass / 1 compliance refusal / 1 timeout
```

Used to order candidates at routing time. Never to skip a gate. An agent with a 100% record still passes G1.

### 2. Episodic priors
Patterns across past runs, in one line each:

- "Projection questions with no stated contribution amount failed 4 of 5 times — ask first."
- "Rate fetches after 18:00 UTC are stale next morning; re-fetch."

These are *observations*, not rules. They live in `observations.jsonl` per the Constitution and carry hypothesis weight only.

### 3. Semantic memory
Facts and preferences about the user. The only auto-writable stratum:

- "Reports in GBP."
- "Prefers ranges with the pessimistic case first."
- "Has a workplace pension; provider asked twice."

Write immediately, correct immediately, never infer a preference from a single instance.

### 4. Cache priors
Fresh tool results inside their TTL. Outside it, the result is **dropped**, not softened. A stale number with a caveat is still a wrong number.

## Decay

| Kind | Half-life | Why |
|---|---|---|
| Reputation | 30 runs | an old record stops predicting |
| Episodic | 90 days | market behaviour shifts |
| Semantic | until contradicted | a preference is not a trend |
| Cache | per source TTL | 24 h default |

## The filter — what may enter

Most traces never reach this layer. Writing everything back makes the agent worse.

| Signal | Enters? |
|---|---|
| Same failure twice | yes, as an episodic prior |
| Single anecdote | no |
| Fact about the user, stated | yes, semantic |
| Fact about the user, inferred | no — proposal only |
| Method change | no — `PROPOSALS.md` |
| Successful run, nothing notable | no |

## Hard limits

1. **Nothing here is binding.** Priors inform; they never justify. A decision that cites only a prior is a defect.
2. **No procedural content.** Rules, tone, policies never enter here — they need human review and evals before touching the hot path.
3. **No PII beyond what the user stated.** Redact where it costs nothing.
4. **Nothing enters unlabelled.** Every prior carries its source, its date, and its half-life.
5. **The agent cannot see the machinery.** It receives a conditioned prompt, not a reputation table. If an agent can read its own score, it starts gaming it.

## Why this is not "the swarm figuring it out on its own"

Because it cannot act. The unconscious is a lookup that changes the prior on a choice the conscious then makes explicitly and logs. Autonomy without a trigger, a budget and an owner is not autonomy — it is an uncontrolled loop. See `CONTRACT.md` §7.
