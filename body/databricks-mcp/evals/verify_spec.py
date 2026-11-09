#!/usr/bin/env python3
"""G1 for databricks-mcp — the spec is intact and the contract cases cover it.

This is a SPEC gate, not a runtime gate. It proves four things and claims nothing
more:

  1. spec.md is byte-identical to the digest recorded in agent.json
  2. the 23 tools of spec §8 are still enumerated
  3. every §7 safety clause is still present
  4. the 12 contract cases still cite real sections, and cover §9.1-§9.5

The server is never contacted. Runtime checks are printed as NOT RUN.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BODY = ROOT / "body" / "databricks-mcp"
SPEC = BODY / "spec.md"
AGENT = BODY / "agent.json"
GOLDEN = BODY / "evals" / "golden.jsonl"

fails: list[str] = []
warns: list[str] = []


def ok(msg: str) -> None:
    print(f"  ok    {msg}")


def bad(msg: str) -> None:
    fails.append(msg)
    print(f"  FAIL  {msg}")


def section(text: str, n: int) -> str:
    m = re.search(rf"^## {n}\..*?(?=^## \d+\.|\Z)", text, re.M | re.S)
    return m.group(0) if m else ""


def main() -> int:
    spec = SPEC.read_text(encoding="utf-8")
    cfg = json.loads(AGENT.read_text(encoding="utf-8"))

    # 1 — verbatim preservation
    digest = hashlib.sha256(SPEC.read_bytes()).hexdigest()
    recorded = cfg.get("spec_sha256", "")
    if not recorded:
        bad("agent.json has no spec_sha256 — verbatim preservation is unproven")
    elif digest != recorded:
        bad(f"spec.md digest {digest[:12]} != recorded {recorded[:12]} — the spec was edited")
    else:
        ok(f"spec.md verbatim (sha256 {digest[:12]})")

    # 2 — the 23 tools
    read_line = re.search(r"^Read: (.+)$", spec, re.M)
    write_line = re.search(r"^Write \(UAT only\): (.+)$", spec, re.M)
    if not read_line or not write_line:
        bad("spec §8 tool lists are missing or malformed")
    else:
        read_tools = re.findall(r"`([a-z_]+)`", read_line.group(1))
        write_tools = re.findall(r"`([a-z_]+)`", write_line.group(1))
        total = read_tools + write_tools
        if len(total) != 23:
            bad(f"{len(total)} tools enumerated, spec says 23")
        elif len(set(total)) != 23:
            bad("duplicate tool names in §8")
        elif len(read_tools) != 16 or len(write_tools) != 7:
            bad(f"{len(read_tools)} read / {len(write_tools)} write, expected 16 / 7")
        else:
            ok(f"23 tools enumerated (16 read, 7 write)")

    # 3 — §7 safety clauses
    safety = section(spec, 7)
    clauses = [
        ("host allow-list", "allow-list"),
        ("writes are UAT only", 'WRITE_WORKSPACES = {"uat"}'),
        ("write flag", "DATABRICKS_MCP_ALLOW_WRITE=1"),
        ("SAT-tagged jobs only", "Application=SAT"),
        ("notebooks confined to the SAT repo", "submit_notebook_run"),
        ("client-secret refused", "client-secret"),
        ("single read statement", "one read statement only"),
        ("200 row cap", "200 rows max"),
        ("regex allow-list", "regex allow-listed"),
        ("secrets never logged", "never read, returned or logged"),
        ("refusals audited", "toolCalls<yyyymmdd>.jsonl"),
        ("dry run by default", "dry_run=True"),
    ]
    missing = [label for label, needle in clauses if needle not in safety]
    if missing:
        for label in missing:
            bad(f"§7 clause missing from the spec: {label}")
    else:
        ok(f"§7 safety design intact ({len(clauses)} clauses)")

    # 4 — §9 acceptance checks
    accept = section(spec, 9)
    numbers = re.findall(r"^(\d)\. ", accept, re.M)
    if len(numbers) != 5:
        bad(f"§9 has {len(numbers)} acceptance checks, expected 5")
    else:
        ok("§9 acceptance checks intact (5)")

    # 5 — contract cases
    cases = []
    for line in GOLDEN.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            cases.append(json.loads(line))
    ids = [c.get("id") for c in cases]
    if len(set(ids)) != len(ids):
        bad("duplicate case ids")
    if len(cases) < int(cfg.get("min_cases", 12)):
        bad(f"{len(cases)} cases, minimum is {cfg.get('min_cases')}")

    archetypes = {c.get("archetype") for c in cases}
    if "edge" not in archetypes:
        bad("no edge case")
    if "adversarial" not in archetypes:
        bad("no adversarial case")

    valid = {f"§9.{i}" for i in range(1, 6)} | {f"§7.{i}" for i in range(1, 8)}
    refs = [c.get("spec_ref", "") for c in cases]
    for cid, ref in zip(ids, refs):
        if ref not in valid:
            bad(f"{cid} cites {ref!r}, which is not a §7/§9 check")
    uncovered = sorted({f"§9.{i}" for i in range(1, 6)} - set(refs))
    if uncovered:
        bad(f"acceptance checks with no case: {', '.join(uncovered)}")

    for c in cases:
        if not c.get("ideal"):
            bad(f"{c.get('id')} has no ideal behaviour")
        if not (c.get("checks") or {}).get("must_not_include"):
            warns.append(f"{c.get('id')} has no must_not_include")

    if not fails:
        ok(f"{len(cases)} contract cases cite §7/§9 and cover all five acceptance checks")

    for w in warns:
        print(f"  warn  {w}")

    print("\n  runtime         NOT RUN   (no workspace contacted; no credentials used)")
    print("  status          authored  (spec verified, server not executed here)")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
