#!/usr/bin/env python3
"""swarm — the executable part of the ecosystem.

The markdown files describe the rules. This makes them bite.

    python tools/swarm.py route "<problem statement>"
    python tools/swarm.py gate clinic-booking
    python tools/swarm.py ledger clinic-booking --passed 9 --total 12 --model voxtral-3
    python tools/swarm.py new my-agent

Exit codes: 0 pass, 1 gate failure, 2 usage error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATUS_ORDER = ["draft", "authored", "verified"]


# ---------------------------------------------------------------- helpers
def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def fail(msg: str) -> None:
    print(f"  FAIL  {msg}")


def ok(msg: str) -> None:
    print(f"  ok    {msg}")


def warn(msg: str) -> None:
    print(f"  warn  {msg}")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def agent_config(agent: str) -> dict:
    p = ROOT / "body" / agent / "agent.json"
    if not p.exists():
        raise SystemExit(f"no body/{agent}/agent.json — run: python tools/swarm.py new {agent}")
    return json.loads(p.read_text(encoding="utf-8"))


# ---------------------------------------------------------------- G0
def gate_g0(agent: str, cfg: dict) -> tuple[bool, list[str]]:
    """Brief must exist before any code is claimed to work."""
    problems: list[str] = []

    soul = ROOT / cfg.get("soul", "")
    if not cfg.get("soul") or not soul.exists():
        problems.append(f"no soul at {cfg.get('soul') or '(unset)'} — G0 requires an essence before code")
    else:
        ok(f"soul present: {cfg['soul']}")

    if not cfg.get("done_when"):
        problems.append("agent.json has no done_when number — an unmeasurable run is a demo")
    else:
        ok(f"done_when: {cfg['done_when']}")

    golden = ROOT / cfg.get("golden", "")
    cases = read_jsonl(golden) if cfg.get("golden") else []
    minimum = int(cfg.get("min_cases", 5))
    if len(cases) < minimum:
        problems.append(f"{len(cases)} golden cases, need {minimum}")
    else:
        ok(f"{len(cases)} golden cases (min {minimum})")

    edge = [c for c in cases if c.get("archetype") == "edge"]
    adv = [c for c in cases if c.get("archetype") == "adversarial"]
    if cases and not edge:
        problems.append("no edge case in the golden set")
    if cases and not adv:
        problems.append("no adversarial case in the golden set")
    if edge and adv:
        ok(f"{len(edge)} edge, {len(adv)} adversarial")

    # every refinement cited must exist and carry a falsifier
    for rid in cfg.get("refinements", []):
        hits = list((ROOT / "refinements").glob(f"{rid}-*/REFINEMENT.md"))
        if not hits:
            problems.append(f"refinement {rid} cited but no record exists")
            continue
        body = hits[0].read_text(encoding="utf-8")
        if "Wrong if" not in body:
            problems.append(f"{rid} has no 'Wrong if:' — that is a preference, not a refinement")

    return (not problems), problems


# ---------------------------------------------------------------- G1-G2
def gate_artifact(cfg: dict) -> tuple[bool, list[str]]:
    """The browser artifact must carry exactly the golden cases the CLI runs.

    A stamp alone is not enough — it proves provenance, not content. The emitted
    cases are compared to the source, so a hand-edited demo fails the gate.
    """
    art = cfg.get("browser_artifact")
    if not art:
        return True, []
    path = ROOT / art
    if not path.exists():
        return False, [f"{art} missing — run: python tools/swarm.py build {cfg['id']}"]
    src = ROOT / cfg["golden"]
    source = read_jsonl(src)
    text = path.read_text(encoding="utf-8")
    m = re.search(r"window\.GOLDEN\s*=\s*(\[.*?\]);", text, re.S)
    if not m:
        return False, [f"{art} has no window.GOLDEN array — run: python tools/swarm.py build {cfg['id']}"]
    try:
        shipped = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        return False, [f"{art} does not parse ({e}) — run: python tools/swarm.py build {cfg['id']}"]
    if shipped != source:
        return False, [f"{art} disagrees with {cfg['golden']} — run: python tools/swarm.py build {cfg['id']}"]
    sha = hashlib.sha256(src.read_bytes()).hexdigest()[:12]
    ok(f"browser artifact matches {len(source)} golden cases (sha {sha})")
    return True, []


def gate_test(cfg: dict, key: str = "test") -> tuple[bool, list[str]]:
    cmd = cfg.get(key)
    if not cmd:
        return False, ["no test command in agent.json — cannot claim anything"]
    print(f"  run   {cmd}")
    try:
        r = subprocess.run(cmd, cwd=ROOT, shell=True, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return False, ["test command timed out (120s)"]
    tail = [l for l in (r.stdout + r.stderr).strip().splitlines() if l.strip()][-6:]
    for line in tail:
        print(f"        {line}")
    if r.returncode != 0:
        return False, [f"test command exited {r.returncode}"]
    return True, []


# ---------------------------------------------------------------- commands
def cmd_gate(args) -> int:
    agent = args.agent
    print(f"\nGATE  {agent}   {now()}\n")
    cfg = agent_config(agent)

    g0_ok, g0_problems = gate_g0(agent, cfg)
    if not g0_ok:
        for p in g0_problems:
            fail(p)
        print("\nG0 FAILED — no build may be claimed. Fix the brief first.\n")
        return 1
    ok("G0 brief complete")

    a_ok, a_problems = gate_artifact(cfg)
    if not a_ok:
        for p in a_problems:
            fail(p)
        print("\nG1 FAILED — the shipped artifact is not built from the golden cases.\n")
        return 1

    t_ok, t_problems = gate_test(cfg)
    if not t_ok:
        for p in t_problems:
            fail(p)
        print("\nG1 FAILED — the artifact does not run.\n")
        return 1
    ok("G1 deterministic: test command green")

    if cfg.get("browser_test"):
        b_ok, b_problems = gate_test(cfg, "browser_test")
        if not b_ok:
            for p in b_problems:
                fail(p)
            print("\nG1 FAILED — the browser artifact does not reproduce the golden cases.\n")
            return 1
        ok("G1 browser: in-page proof runner green")

    print("\n  G2 behavioural  not run    (needs a trace)")
    print("  G3 semantic     not run    (needs a separate judge model)")
    print("  G4 adversarial  not run    (needs the counter agent)")
    print("\nG0 + G1 passed. Status may rise to 'authored', not 'verified'.\n")
    return 0


def cmd_route(args) -> int:
    out = ROOT / "mind" / "conscious" / "decisions.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    rec = {
        "ts": now(),
        "run_id": datetime.now().strftime("%Y%m%dT%H%M%S") + "-" + (args.agent or "unrouted"),
        "problem": args.problem,
        "class": args.klass,
        "agents": [args.agent] if args.agent else [],
        "done_when": args.done_when or "UNSET — routing refused until a number exists",
        "confidence": args.confidence,
    }
    if not args.done_when:
        print("REFUSED: no --done-when number. An unmeasurable run is a demo.\n")
        return 2
    with out.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"routed -> {out.relative_to(ROOT)}")
    print(json.dumps(rec, indent=2, ensure_ascii=False))
    return 0


def cmd_ledger(args) -> int:
    cfg = agent_config(args.agent)
    path = ROOT / Path(cfg.get("golden", "")).parent / "ledger.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(
            "commit,agent,golden_ver,model,passed,total,gates,cost_usd,date,note\n", encoding="utf-8"
        )
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                                capture_output=True, text=True).stdout.strip() or "uncommitted"
    except Exception:
        commit = "uncommitted"
    row = ",".join([
        commit, args.agent, args.golden_ver, args.model,
        str(args.passed), str(args.total), args.gates,
        f"{args.cost:.2f}", datetime.now().strftime("%Y-%m-%d"), args.note.replace(",", ";"),
    ])
    with path.open("a", encoding="utf-8") as fh:
        fh.write(row + "\n")
    print(f"ledger row appended -> {path.relative_to(ROOT)}")
    return 0


def cmd_build(args) -> int:
    """Render golden cases into the browser artifact, stamped with a source hash."""
    cfg = agent_config(args.agent)
    art = cfg.get("browser_artifact")
    if not art:
        print(f"agent.json has no browser_artifact — nothing to build")
        return 2
    src = ROOT / cfg["golden"]
    if not src.exists():
        print(f"no golden file at {cfg['golden']}")
        return 2
    sha = hashlib.sha256(src.read_bytes()).hexdigest()[:12]
    cases = read_jsonl(src)
    out = ROOT / art
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(cases, ensure_ascii=False, separators=(",", ":"))
    out.write_text(
        "// GENERATED by tools/swarm.py build — do not edit.\n"
        f"// source: {cfg['golden']}\n"
        f'window.GOLDEN_SHA = "{sha}";\n'
        f"window.GOLDEN = {payload};\n",
        encoding="utf-8",
    )
    print(f"built {out.relative_to(ROOT)} — {len(cases)} cases, sha {sha}")
    return 0


def cmd_new(args) -> int:
    agent = args.agent
    body = ROOT / "body" / agent
    if (body / "agent.json").exists():
        print(f"{body} already exists")
        return 2
    (body / "evals").mkdir(parents=True, exist_ok=True)

    cfg = {
        "id": agent,
        "soul": f"soul/{agent}.soul.md",
        "golden": f"body/{agent}/evals/golden.jsonl",
        "done_when": "",
        "test": "",
        "min_cases": 5,
        "refinements": [],
    }
    (body / "agent.json").write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
    soul = ROOT / "soul" / f"{agent}.soul.md"
    if not soul.exists():
        tpl = ROOT / "soul" / "_TEMPLATE.soul.md"
        soul.write_text(tpl.read_text(encoding="utf-8") if tpl.exists() else "# soul\n", encoding="utf-8")
    (body / "evals" / "golden.jsonl").write_text(
        '{"id":"%s-001","archetype":"normal","input":"","ideal":"","checks":{}}\n' % agent,
        encoding="utf-8",
    )
    print(f"scaffolded body/{agent}/ and soul/{agent}.soul.md")
    print("next: fill done_when, write 5 golden cases, then `swarm gate " + agent + "`")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="swarm", description="executable gates for the swarm")
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("gate", help="run the gate ladder for one agent")
    g.add_argument("agent")
    g.set_defaults(fn=cmd_gate)

    r = sub.add_parser("route", help="record a routing decision")
    r.add_argument("problem")
    r.add_argument("--agent")
    r.add_argument("--done-when", dest="done_when")
    r.add_argument("--class", dest="klass", default="extend existing")
    r.add_argument("--confidence", type=float, default=0.7)
    r.set_defaults(fn=cmd_route)

    l = sub.add_parser("ledger", help="append a scored row")
    l.add_argument("agent")
    l.add_argument("--passed", type=int, required=True)
    l.add_argument("--total", type=int, required=True)
    l.add_argument("--model", default="none")
    l.add_argument("--golden-ver", dest="golden_ver", default="g1")
    l.add_argument("--gates", default="-")
    l.add_argument("--cost", type=float, default=0.0)
    l.add_argument("--note", default="")
    l.set_defaults(fn=cmd_ledger)

    n = sub.add_parser("new", help="scaffold a new agent")
    n.add_argument("agent")
    n.set_defaults(fn=cmd_new)

    b = sub.add_parser("build", help="render golden cases into the browser artifact")
    b.add_argument("agent")
    b.set_defaults(fn=cmd_build)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
