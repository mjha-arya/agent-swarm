# The collective mind

The container, not an actor. It answers three questions and nothing more: **who exists, what may they call, and how do they address each other.**

## 1. Who exists

`state/agents.json` is the only source of truth. An agent not listed there cannot be routed to, and the router may not invent one. Three lineage slots are reserved: `mine`, `k21`, `open-source` — provenance, not species.

## 2. What may they call

A shared tool registry. Tools are declared once, in the body that owns them, and referenced by id. Rules:

- **Read tools are shared by default.**
- **Write tools are private to the owning agent** unless a line in that agent's soul grants the loan.
- **Outward tools** (post, email, deploy, schedule) are never shared and always need a human yes.
- A tool used by two agents is a signal to move the *calculation* to a shared module, not to duplicate the call.

## 3. How they address each other

One envelope, one shape, no free-form chatter. Prose between agents is untraceable, so there is none.

```json
{
  "run_id": "2026-10-22T14-03-fin-data-01",
  "from": "router",
  "to": "fin-data",
  "intent": "answer_question",
  "payload": { "...": "typed per intent" },
  "budget": { "turns": 30, "usd": 1.0 },
  "done_when": "5 of 5 golden cases pass; zero compliance violations",
  "attachments": ["priors:3", "memory:semantic:12"],
  "reply_to": "router"
}
```

Every message is appended to `conscious/decisions.jsonl`. A conversation that is not in the log did not happen.

## 4. What the collective mind is not

- It is not a planner. Planning is the router's job.
- It is not memory. Memory is the unconscious.
- It does not adjudicate. Gates adjudicate.

Keeping these apart is what stops the layer from becoming a second orchestrator that nobody can debug.

## 5. Shared state

| Item | Where | Who writes |
|---|---|---|
| Agent registry | `state/agents.json` | human + status updates |
| Tool registry | each `body/<id>/body.md` | that agent's builder |
| Routing decisions | `conscious/decisions.jsonl` | router, append-only |
| Run traces | `../runs/*.jsonl` | runtime, append-only |
| Priors | `unconscious/priors.md` | filtered writer only |

## 6. The negotiation rule

When two agents both claim a problem, the router does **not** let them argue. It picks one, records why, and puts the other's objection in the log. Two agents debating is unbounded cost with no audit trail; a recorded decision is reviewable.

Bounded by construction: at most **two** returns between router and an agent, then escalate to a human.
