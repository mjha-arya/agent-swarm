# Product of the Swarms

What the swarm **ships**. One folder per product, each one demoable, sellable and built from the layers in `../soul`, `../mind`, `../body`.

| Product | What it is | State |
|---|---|---|
| [`ai-voice-agent/`](ai-voice-agent/README.md) | Eye-care clinic booking agent — talkable demo with live gates | working demo, not deployed |

## Why this folder exists

`body/` holds agents as *engineering artifacts*: graph, spec, golden cases.
This folder holds them as *things a client can see, run and buy*.

The difference matters commercially. A build sold at $30–70k is not the spec — it is the demo, the scorecard, the failure handling and the launch pack. Keeping them apart means the engineering can be refactored without touching what was promised.

## What belongs here

- A runnable demo with no setup beyond `python -m http.server`
- A README a non-technical buyer can follow
- The measured evidence: what was tested, what passed, what was not checked
- The honest limits, written down before a client finds them

## What does not

- Golden cases and gate definitions → `body/<agent>/evals/`
- Soul, policy, escalation rules → `soul/`
- Routing and memory → `mind/`

## Naming

Folder names keep spaces, as asked. Note that spaces need quoting in the shell and arrive URL-encoded (`%20`) on GitHub — if that becomes friction, `product-of-the-swarms` is the drop-in alternative.

## The commercial test

Every product here should answer one question: **does this make the next build faster?**

If clinic #2 costs the same as clinic #1, this folder is a portfolio, not a product line.
