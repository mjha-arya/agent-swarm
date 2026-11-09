# body/databricks-mcp — what runs

**Status:** `authored`. The spec is preserved and gated. The server itself lives in `secopsAutomationOperations\MCPs\databricksMcp\` and has **not** been executed from this repo.

## Wiring

| Aspect | Value |
|---|---|
| Runtime | Python 3.14.6, venv `%USERPROFILE%\.venvs\databricksMcp`, invoked by absolute path |
| Transport | stdio, MCP server name `databricks` |
| Auth | `az account get-access-token` per call; token cached in memory for its lifetime. No app registration, no secret, no PAT |
| Targets | UAT `adb-<workspace-id>.azuredatabricks.net` (read + write); DEV `adb-<workspace-id>.azuredatabricks.net` (read only) |
| Write gate | every write tool refuses unless `DATABRICKS_MCP_ALLOW_WRITE=1` |
| Tools | 23 — 16 read, 7 write (spec §8) |
| Audit | every call, **including refusals**, appended to `runs\toolCalls<yyyymmdd>.jsonl` |
| Identity | the signed-in engineer. The server can do only what the human can do — it is not a service account |

## Failure behaviour

| Failure | Behaviour |
|---|---|
| Token expired or missing | surface the tool error and the instruction `az login`; never retry silently |
| Write attempted without the env flag | refuse, log the refusal, change nothing |
| Job not tagged `Application=SAT` | refuse `run_job` / `delete_job` |
| SQL that is not a single read statement, or over 200 rows | refuse before dispatch |
| `put_secret` on `client-secret` | refuse; the secret is never read, returned or logged |
| Quota exhausted on Permissions Analysis | surface the core requirement and point at `list_node_types` |

## Non-negotiables

- Deterministic work is code. Anything a model produces is judgement, and is labelled as such.
- Every call writes an audit line before it answers.
- Status starts at `authored`, never `verified`.
- This body never stores credentials. It borrows the human's token per call.

## What is deliberately not here

- The server source — it stays in `secopsAutomationOperations` as the single implementation.
- Any workspace credential, secret value, or tenant token.
- Live golden runs. The 12 cases in `evals/golden.jsonl` are **contract cases**: they assert what the spec requires, and `evals/verify_spec.py` proves the spec and the cases still agree. They have not been replayed against a workspace from here.

## Gates

See `agent.json`. G1 here means: the spec is intact (sha256), all 23 tools are enumerated, every §7 safety clause is present, and every §9 acceptance check has a case. **Runtime checks are `not run`.**
