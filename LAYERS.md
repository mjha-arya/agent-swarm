# LAYERS.md — soul, mind, body

The three layers mimic a human being on purpose: an essence, a mind that relates to other minds, and a body that acts. The analogy earns its keep because it forces three questions apart that usually get mixed: *what is this agent*, *how does it relate*, *what does it run*.

---

## soul/ — what an agent IS

One file per agent. Binding, read first, every run.

Holds: purpose, lineage (yours / k21 / open source), inputs, hard rules, `needs_human` list, exact return format ending in `NOT CHECKED`, and the memory files it is allowed to write.

Does **not** hold: tool names, model versions, prices, prompts. Those go stale in a week and would drag the essence with them.

The soul is the only layer no agent may rewrite. It changes by human edit or by an accepted `PROPOSALS.md` entry, and nothing else. That single rule is what makes "original essence" real rather than decorative.

A soul **embeds** the Constitution articles that apply to its job — adapted, standalone, no links back. An agent must be able to stand alone with only its soul in front of it.

---

## mind/ — how agents RELATE

The interactive layer. Three strata, and they are not equally knowable.

### Collective mind — the container
The shared substrate: the registry, the typed message envelope, the tool registry, the gate criteria, the decision log. It is the *place* where relating happens, not an actor. It answers: who exists, what may they call, how do they address each other.

### Collective conscious — the deliberate part
What the vision calls "based on the capabilities of the existing tools, how it would interact to find the best solution."

This is the router. Given a problem it names the agent set, the tools, the plan, and a "done when" number — then writes that choice to `decisions.jsonl`. Deliberate, inspectable, reviewable. If it cannot name a done-when number, it does not proceed.

### Collective unconscious — the derived part
What the vision calls "it figuring it out, talking to the internet, or somehow, I don't even understand."

Made mechanical in `CONTRACT.md` §3: it is **the context an agent receives without choosing to consult it** — reputation, episodic priors, semantic memory, cache priors. Derived from traces, never authored deliberately, never binding.

The psychological mapping is honest: the unconscious is not a smaller conscious. It is a different kind of thing — implicit, prior, shaping behaviour without being deliberated. That is exactly how priors should work in an agent system.

---

## body/ — what an agent RUNS

Per agent: `body.md` (layout and wiring), `spec.md` (the node table), `graph.mmd` (the diagram), `evals/golden.jsonl` (the proof).

Built from the LangGraph pipeline in `../Designing-Better-Agents/langgraph-spec-to-code-pipeline.md`: spec the graph as a diagram plus a table, use the five node archetypes (tool call, LLM judge, router, human interrupt, aggregator), write fewer nodes, tests before code, debug in Studio and fix the *spec*, not the code.

No agent writes another agent's body. Cross-agent change goes through a proposal.

---

## Where the metaphor misleads — read this before extending it

The anatomy is good architecture. Three parts of it are not yet true, and pretending otherwise will cost you later:

1. **A soul is not immutable, it is *slow*.** Essence that never changes cannot learn. Essence that changes freely is not essence. The contract resolves this by making change *expensive* (human yes) rather than *impossible*.

2. **The unconscious does not "figure things out" on its own.** It has no goals and takes no actions. All action is in the body, all choice in the conscious. Calling it a mind risks expecting agency from a lookup table. It is context, and context is powerful enough.

3. **"Life of their own" is a scheduling question, not a metaphysical one.** An agent that acts unprompted needs a trigger, a budget, and an owner — all three undecided. Until then, agents are summoned, not alive. See `CONTRACT.md` §7.

4. **Three lineages are not three species.** Yours, k21's and open-source agents differ in provenance, not in anatomy. If they need different layers, the contract is wrong, not the agent.
