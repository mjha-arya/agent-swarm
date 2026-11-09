# The memory bus

How the unconscious is read and written. One schema, one writer, one filter. If memory is written from more than one place, it becomes unauditable and the agent starts believing its own noise.

## Stores

| Store | File | Kind | Weight | Written by |
|---|---|---|---|---|
| Semantic | `memory/semantic.jsonl` | what it knows: facts, preferences | auto | bus |
| Episodic | `memory/episodic.jsonl` | what it has experienced: patterns | auto, decayed | bus |
| Procedural | `../soul/*.soul.md`, `PROPOSALS.md` | how it behaves | binding / proposed | human only |
| Working | `runs/<run_id>.jsonl` | this run's scratchpad and evidence | none | runtime |

Procedural is **not** in the bus on purpose. It is the layer where the biggest behaviour gains live — and therefore the layer that must never be written automatically.

## Record shape

```json
{"id":"sem_0042","kind":"semantic","agent":"fin-data",
 "text":"Reports in GBP","source":"user, stated 2026-10-19",
 "confidence":"stated","created":"2026-10-19T09:12:00Z","half_life":"none",
 "last_used":"2026-10-22T14:03:11Z","uses":6}
```

`confidence` is one of `stated` | `observed` | `inferred`. **`inferred` may never be read back into a prompt** — it exists only to support a proposal.

## The loop

```
read long-term -> run -> trace -> FILTER -> write back
```

The filter is the whole point:

| Trace shows | Action |
|---|---|
| A new failure mode | add a golden case (G0), not a memory |
| A repeated fact about the user | semantic write, immediate |
| A better method | `PROPOSALS.md`, max 2 open, human yes |
| A one-off oddity | nothing |
| A contradiction of an existing memory | supersede, don't append — keep both with `superseded_by` |

## Retrieval

On each run the bus attaches at most **8 records**: semantic first, then episodic, ranked by `last_used` recency and `uses`. Nothing else. A prompt stuffed with 40 memories performs worse than one with 8 good ones, and the cost is linear in tokens.

Retrieved records are attached as *context*, labelled by source. They are never cited as evidence — evidence is a file, a command, or a URL.

## Cache discipline

- Default TTL 24 h for anything that goes stale.
- **Outside TTL, drop the value.** Never present a stale number with a caveat.
- **Reload explicitly.** A long-running agent can miss a memory update because its runtime state was cached at start. Declare what is reloaded and when; default is "reload memory at the start of every run, never mid-run".
- Cache keys include the source and the date, not just the query.

## Contradiction handling

1. Two records disagree → the newer `stated` wins over any `observed`.
2. `stated` vs `stated` → do not choose. Ask, and record the answer.
3. Code disagrees with a settled decision → the code is the bug.
4. Never resolve a contradiction by averaging. An average of two facts is a third fact nobody said.

## Hard rules

- One writer: the bus. Agents emit *signals*; the bus decides what becomes memory.
- Nothing inferred enters a prompt.
- Nothing procedural enters automatically.
- Every record carries source, date, confidence, half-life.
- An agent may not read its own reputation score.
