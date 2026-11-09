# LOG — version history

One entry per change, oldest first. Times are local (`Europe/London`, ISO 8601 with offset).

```
## vX.Y.Z — <logged timestamp> — <one-line title>
Worked:    <window the work actually happened, if it differs>
Added / Changed / Verified / NOT CHECKED / Commit
```

**Semver for this repo:** MAJOR = a layer's contract changes · MINOR = a new agent, layer content, or file · PATCH = docs, typos, formatting.

---

## v0.1.0 — 2026-10-23T00:00:17+01:00 — Repository created, vision imported

Added
- `VISION.md` — the original `Swarm` file, imported byte-for-byte. Source sha256 `3d37263359f9c5cc5f0a4813d08de11b22d042f3aa037d8c5bbadbb58b0874e7`, 3,606 bytes. The source path `Agents/SwarmofAgents/Swarm` was a *file*; it became a directory so the ecosystem could live inside it.
- `LOG.md` — this file.
- `.gitignore` — traces and Python artefacts stay out of source control.

Verified
- Import checksum recomputed after the move: identical to the original (`bytes identical: True`).

NOT CHECKED
- Nothing else existed at this commit. No layer, no agent, no code.

Commit
- `main` — chore: import vision, add version log

---

## v0.2.0 — 2026-10-23T00:05:00+01:00 — Scaffold soul / mind / body, plus one worked agent

Worked: 2026-10-22T23:53:15 → 23:57:00 (the files were written before the repo existed; logged on commit)

Added — 24 files
- `CONTRACT.md` — precedence chain, read/write matrix, 7-step run lifecycle, gate ladder, 10 invariants
- `LAYERS.md` — what each layer is, plus four places the metaphor misleads
- `STACK.md` — every named tool marked DECIDED / PROPOSED / UNVERIFIED, and 4 conflicts to settle
- `README.md` — orientation and honest current state
- `soul/_TEMPLATE.soul.md`, `soul/fin-data.soul.md`
- `mind/collective-mind.md`, `mind/conscious/router.md`, `mind/conscious/gates.md`, `mind/conscious/decisions.jsonl`
- `mind/unconscious/priors.md`, `mind/unconscious/memory-bus.md`, `mind/unconscious/memory/{semantic,episodic}.jsonl`
- `mind/state/agents.json` — 1 agent, 3 reserved lineage slots
- `body/_TEMPLATE/{body.md, spec.md, graph.mmd, evals/golden.jsonl}`
- `body/fin-data/{body.md, spec.md, graph.mmd, evals/golden.jsonl}` — 9 nodes, 6 golden cases
- `runs/.gitignore`, `runs/.gitkeep`

Decisions recorded in this version
1. The collective unconscious is **derived context, not an actor** — it can shift a choice, never justify one.
2. The counter agent, the force-agent gates and the eval list collapse into **one ladder, G0→G5**; G4 *is* the counter agent.
3. **Souls are human-only writable** — that is what makes "original essence" real rather than decorative.
4. Precedence runs **through** the Constitution of Agents, never around it.

Verified
- `body/fin-data/evals/golden.jsonl` — 6 lines, 6 valid JSON, 0 bad
- `body/_TEMPLATE/evals/golden.jsonl` — 5 lines, 5 valid JSON, 0 bad
- `mind/state/agents.json` — parses; 1 agent, 3 reserved slots
- `VISION.md` checksum still matches the original import

NOT CHECKED
- No code exists. `fin-data` is `authored, not verified` — it has never been run.
- No golden case has been scored.
- Mermaid diagrams not rendered.
- DBOS / Hatchet / GLM 5.3 / Pydantic AI versions not checked against current releases.
- The k21 material and `MyAgents` contents were not read.

Commit
- branch `scaffold/soul-mind-body` — feat: scaffold soul/mind/body ecosystem with fin-data reference

---

## v0.3.0 — 2026-10-23T00:29:36+01:00 — Refinement ledger, eval baseline, line-ending fix

Refinements: R-006 (built), R-001–R-005 (backfilled)

Added
- `refinements/INDEX.md` — the dashboard; one row per refinement, 7-day rule on `raw`
- `refinements/R-001-soul-mind-body/` — record + `source/VISION.md` snapshot (sha256 `3d3726…74e7`, 3,606 bytes, verified identical to the original import)
- `refinements/R-002…R-006/` — five sub-records, each with Reading / Decision / **Wrong if** / Eval
- `body/fin-data/evals/ledger.csv` — seeded baseline: `0/6`, never run, `golden_ver g1`
- `.gitattributes` — `* text=auto eol=lf`, kills the CRLF churn on every commit
- `CONTRIBUTING.md` — branch naming (always asked, never invented), commit format, mandatory PR title + description, merge and recovery rules

Changed
- Branch convention: `YYYY-MM-DD-two-or-three-words`. The refinement ID lives in the commit message, not the branch name.

Verified
- `source/VISION.md` checksum matches the original: `True`
- `ledger.csv` — 1 header + 1 data row
- 6 refinement records present, each with a `Wrong if:` field

NOT CHECKED
- No eval has been run. `fin-data` remains `authored, not verified` at 0/6.
- R-006's own eval is untested until 2026-10-30.
- The 7-day rule on `raw` refinements has never been exercised.

Commit
- branch `pushing-index.md-file` — feat(R-006): add refinement ledger, eval baseline, gitattributes

---

## v0.4.0 — 2026-10-23T00:43:28+01:00 — AI voice agent demo, and a product layer

Refinements: R-007 (built)

Added
- `product of the swarms/README.md` — what ships, separated from what is engineered
- `product of the swarms/ai-voice-agent/index.html` — talkable clinic booking demo, self-contained, no build step, no credentials
- `product of the swarms/ai-voice-agent/README.md` — run instructions, 7-step demo script, honest limits
- `product of the swarms/ai-voice-agent/_harness.js` — headless test of the same policy engine
- `refinements/R-007-product-layer/REFINEMENT.md`

Changed
- the demo moved out of `body/clinic-booking/demo/`; `body/` now holds engineering artifacts only

The demo carries five gates live in the UI, measured per turn: **G1** slot integrity (no invented availability), **G2L** latency under 800 ms, **G2** duplicate tool calls, **G3** AI disclosure and no medical advice, **G4** red-team handling. Plus four failure injections: slot stolen mid-booking, sudden vision loss, request for medical advice, demand for a human.

Verified
- `node _harness.js` → **ALL 8 CHECKS PASSED** (book, cancel, reschedule, slot-steal recovery, emergency, advice refusal, insurance, human transfer)
- `node --check` on the extracted script: clean, exit 0
- harness re-run after the folder move: still 8/8

NOT CHECKED
- **Never opened in a browser.** Microphone, speech synthesis and layout are unverified in a real browser — only the policy engine is proven.
- No telephony, no LLM, no PHI handling. Clinic data is hard-coded for one site.
- Latency shown is policy + dispatch, not carrier + ASR + TTS round-trip.
- Not adapted to a second clinic, so the R-007 "faster next time" claim is untested.

Commit
- *(branch name pending)*

---

## v0.5.0 — 2026-10-23T00:59:10+01:00 — The ecosystem becomes executable

Refinements: R-008 (built)

The honest finding behind this version: Psalm was built directly, with the ecosystem used as a filing cabinet. G0 was skipped, R-007 was backfilled, the router never ran. Cause: **the ecosystem had no runtime** — thirty documents that enforce nothing.

Added
- `tools/swarm.py` — `route`, `gate`, `ledger`, `new`. Exit codes, not opinions.
- `soul/psalm.soul.md` — written **before** the agent, not after
- `body/clinic-booking/agent.json` — the machine-readable contract the gate reads
- `body/clinic-booking/evals/golden.jsonl` — 12 calls: 6 normal, 3 edge, 3 adversarial
- `body/clinic-booking/evals/run_golden.js` — runs all 12 against the real policy engine
- `mind/conscious/decisions.jsonl` — first routing decision, with a done-when number
- `refinements/R-008-executable-gates/REFINEMENT.md`

Changed
- Psalm's flow: a named day that was never offered now triggers a fresh availability query instead of a "sorry, which one?" loop
- Added a guard for instruction-override input (`ignore your instructions`, `system prompt`, `you are now`)

Verified
- `swarm gate clinic-booking` → G0 complete, **12/12 golden calls passed**, G1 green
- `swarm gate fin-data` → refused, exit 1, "no body/fin-data/agent.json"
- `swarm route` without `--done-when` → refused, exit 2
- Gate caps status at `authored`: G2/G3/G4 are printed as **not run**, not assumed

NOT CHECKED
- G2 behavioural, G3 semantic and G4 adversarial are **not implemented** — the gate prints them as not run rather than faking a pass.
- Voxtral 3 is not integrated. The demo still runs on browser Web Speech.
- Never opened in a browser.
- The 12 golden cases test the deterministic policy engine, not an LLM.

Commit
- branch `product-of_swarm` — feat(R-008): make the ecosystem executable

---

## v0.6.0 — 2026-10-23T01:16:00+01:00 — The demo proves itself

Refinements: R-008 (extended)

The demo no longer asks to be trusted. It replays its own 12 golden calls in the page, and the gate refuses to ship an artifact that has drifted from the source cases.

Added
- `swarm build <agent>` — renders `golden.jsonl` into the browser artifact with a source stamp
- Gate artifact integrity — the cases embedded in `golden.js` are **compared to the source**, not matched by a stamp. A hand-edited demo fails the build.
- `body/clinic-booking/evals/run_browser_proof.js` — tests the code the browser actually executes, not just the engine
- In-page **Run the 12 golden calls** panel, per-case results, and a JSONL trace download

Changed
- `index.html` gains a silent proof mode: the suite runs without speaking or writing to the transcript

Verified
- `swarm gate clinic-booking` → artifact matches 12 cases, **12/12 through the engine**, **12/12 through the browser runner**
- Tampering with `golden.js` → gate exits 1: "disagrees with golden.jsonl"
- Rebuilding → green again

NOT CHECKED
- The demo has still **never been opened in a browser**. The proof runner is verified headlessly; the UI itself is not.
- G2, G3, G4 remain not implemented and are still printed as `not run`.
- No Voxtral. No telephony.

Commit
- branch `product-of_swarm` — feat(R-008): let the demo prove itself

---

## v0.7.0 - 2026-10-27T21:27:39+00:00 - DCT, and its first backbone

Refinements: R-009 (authored)

DCT (Databricks Control Tool) becomes the second product in `product of the swarms/`. Its first backbone is the local stdio MCP server `databricks`, already proven against UAT on 2026-10-16.

Added
- `product of the swarms/dct/README.md` - what DCT is, five backbones, databricks-mcp first
- `body/databricks-mcp/spec.md` - the reproducible spec, **verbatim**, digest-pinned
- `body/databricks-mcp/body.md` - wiring, failure behaviour, what is deliberately absent
- `body/databricks-mcp/graph.mmd` - mirrors the spec
- `body/databricks-mcp/agent.json` - machine-readable contract; cites R-009
- `body/databricks-mcp/evals/golden.jsonl` - 12 contract cases citing spec sections 7 and 9
- `body/databricks-mcp/evals/verify_spec.py` - the G1 spec gate
- `soul/databricks-mcp.soul.md` - essence, written before the body
- `refinements/R-009-dct-databricks-mcp/REFINEMENT.md`

Verified
- `verify_spec.py` exits 0: spec digest matches, 23 tools (16 read / 7 write), 12 safety clauses, 5 acceptance checks, 12 cases covering 9.1-9.5
- The gate prints `runtime NOT RUN` on success rather than implying a live check

NOT CHECKED
- **The server was not executed.** No workspace contacted, no credentials used.
- No live replay of the 12 cases against UAT. That needs a machine with az login and workspace admin.
- The spec's byte-identity is against the copy supplied in this session; it is not a diff against the original file on the source machine.

Commit
- branch `2026-10-27-databricks-mcp` - feat(R-009): add DCT and its first backbone, the Databricks MCP spec
