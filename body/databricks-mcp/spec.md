# Databricks local MCP - reproducible spec

What this is: a local stdio MCP server (`databricks`) that lets Claude Code operate the Security Analysis Tool (SAT) in the UAT Databricks workspace as the signed-in engineer. SAT has worked end to end since 2026-10-16. This document is the configuration that made that possible.
Source of truth for the code: `secopsAutomationOperations\MCPs\databricksMcp\` (`pythonScripts\databricksMcp.py`, `requirements.txt`, `readme.md`). Audit log: `runs\toolCalls<yyyymmdd>.jsonl`.

## 1. Moving parts at a glance

| Part | Value |
|---|---|
| Server | `databricksMcp.py`, MCP server name `databricks`, stdio transport |
| Runtime | Python 3.14.6 in a venv at `%USERPROFILE%\.venvs\databricksMcp` |
| Packages | `mcp 2.3.0`, `mcp-types 2.3.0`, `httpx 0.28.1` (pinned ranges: `mcp>=2,<3`, `mcp-types>=2,<3`, `httpx>=0.27`) |
| Auth | Azure CLI 2.91.0 token per call. No app registration, no secret, no PAT |
| Registration scope | Claude Code, root project (`claude mcp add`), entry in `~\.claude.json` |
| Write gate | env `DATABRICKS_MCP_ALLOW_WRITE=1` (remove it for read-only) |
| Targets | UAT `adb-<workspace-id>.azuredatabricks.net` (read + write), DEV `adb-<workspace-id>.azuredatabricks.net` (read only) |

## 2. Install (reproduce from scratch)

```
python -m venv %USERPROFILE%\.venvs\databricksMcp
%USERPROFILE%\.venvs\databricksMcp\Scripts\python.exe -m pip install -r <repo>\secopsAutomationOperations\MCPs\databricksMcp\requirements.txt
claude mcp add databricks -e DATABRICKS_MCP_ALLOW_WRITE=1 -- "%USERPROFILE%\.venvs\databricksMcp\Scripts\python.exe" "<repo>\secopsAutomationOperations\MCPs\databricksMcp\pythonScripts\databricksMcp.py"
```
- Do not activate the venv: ConstrainedLanguage blocks `Activate.ps1`. Call the venv's `python.exe` directly.
- Use the venv python in the registration, never bare `python` (Python 3.14 only on this machine; SAT's own install script needs under 3.12, which is why SAT was installed with Terraform, not `install.sh`).
- Resulting entry in `~\.claude.json`:
  ```
  "databricks": { "type": "stdio",
    "command": "C:\\Users\\<user>\\.venvs\\databricksMcp\\Scripts\\python.exe",
    "args": ["<repo>\\...\\databricksMcp\\pythonScripts\\databricksMcp.py"],
    "env": { "DATABRICKS_MCP_ALLOW_WRITE": "1" } }
  ```
- Restart Claude Code after registering. Check with `/mcp`: 23 tools expected.

## 3. Identity and permissions it depends on

The server can do only what the signed-in user can do.
1. `az login` as `admin@contoso.com` (tenant `00000000-0000-0000-0000-000000000000`). The server calls `az account get-access-token --resource <audience>`; tokens are cached in memory for their lifetime.
2. Audiences: Databricks `00000000-0000-0000-0000-000000000000`; ARM `https://management.azure.com/`.
3. Databricks: workspace admin on UAT and DEV (not TST or PRD). Account-console access comes through the same Entra token (account ID `00000000-0000-0000-0000-000000000000`).
4. Azure: Reader on subscription Data - NonProduction (`00000000-0000-0000-0000-000000000000`) for the quota tool.
5. If a tool reports a token error: run `az login` in a terminal, then retry.

## 4. SAT-side configuration the tools assume

| Item | Value |
|---|---|
| Workspace | `adb-ne-dat-uat-common` (UAT), Terraform-installed 2026-06-15; Terraform state is lost, so the workspace is the source of truth |
| Repo | `/Repos/Applications/SAT_TF` (commit `3cde4a27`, v0.8.0-era) |
| Secret scope | `sat_scope` |
| Schema | `pdp_catalog_uat.security_analysis` |
| SAT service principal | SecOps-SP "Databricks UAT testing", app id `00000000-0000-0000-0000-000000000000` (account admin, workspace admin, Reader on subscription; client secret expires 2026-12-12) |
| Warehouses | SAT `ca81707eae9f2e40` (auto-stops); common `2cad3c98ebfffc4b` (X-Small Pro, always on, default for `sql_query`) |
| Job IDs | Initializer `234857405605358`, Driver `229384746132738`, Secrets Scanner `958880412247341`, Permissions Analysis `243297821093630` |
| Dashboards | Custom Lakeview `01f1c8c31ce81e8598b08c6cb7d3ced1`, stock SAT `01f1c713e3d51987ba89d51f98ef2a09` |

## 5. What actually made SAT work (beyond the server)

1. **Firewall egress.** Rule `HAD-CAD-CommonURLs` in the dat-uat rule collection group allows `github.com`, `api.github.com`, `raw.githubusercontent.com`, `objects.githubusercontent.com` (and `*.githubusercontent.com`). Without it the TruffleHog install hung. PyPI and `*.azuredatabricks.net` were already allowed. Notes: `databricks\satGithubEgress.md`.
2. **Hung runs cleared.** Driver and Secrets Scanner runs from 2026-09-11 sat "In run" for 32 days and blocked everything (`max_concurrent_runs=1`). They were cancelled (`cancel_run`) and the jobs recreated (`create_sat_jobs`, dry run first).
3. **Compute quota.** Permissions Analysis needs 20 cores of the `standardEadv6Family` (limit was 10 in northeurope). Checked with `azure_quota`; raise the quota or use another family via `list_node_types`.
4. **Repo upgrade path.** `update_repo ref=<tag> ref_type=tag` checks out a release in the Git folder.
5. **Secrets.** `user-email-for-alerts` must hold an email address, not the client ID (fixed with `put_secret`). The server refuses to set `client-secret`.

## 6. Operating rules (learned the hard way)

- Run the **Secrets Scanner alone**. It races the Driver and Permissions Analysis on `COMMENT ON TABLE run_number_table` and fails with DELTA_METADATA_CHANGED.
- A parent scanner run can report SUCCESS with empty tables, because child failures are swallowed. Verify with row counts: `SELECT count(*) FROM pdp_catalog_uat.security_analysis.security_checks`.
- Publish dashboards on the always-on common warehouse (`2cad3c98ebfffc4b`), not the auto-stopping SAT warehouse.
- Do not reinstall SAT from scratch. Trigger jobs with `run_job`.

## 7. Safety design

- Hosts are an allow-list; writes are UAT only (`WRITE_WORKSPACES = {"uat"}`).
- Every write tool refuses unless `DATABRICKS_MCP_ALLOW_WRITE=1`.
- `run_job` and `delete_job` refuse jobs not tagged `Application=SAT`; `submit_notebook_run` refuses paths outside the SAT repo; `put_secret` refuses `client-secret`.
- SQL: one read statement only (`SELECT/SHOW/DESCRIBE/WITH/EXPLAIN`), 200 rows max.
- Inputs are regex allow-listed. Secret values are never read, returned or logged.
- Every call, including refusals, is appended to `runs\toolCalls<yyyymmdd>.jsonl`.
- `create_sat_jobs` defaults to `dry_run=True`.

## 8. Tools (23)

Read: `whoami`, `sat_status`, `list_jobs`, `get_job`, `list_runs`, `get_run`, `list_clusters`, `list_warehouses`, `list_node_types`, `list_secret_keys`, `list_repos`, `workspace_list`, `list_dashboards`, `sql_query`, `list_account_workspaces`, `azure_quota`.
Write (UAT only): `create_sat_jobs`, `update_repo`, `run_job`, `cancel_run`, `delete_job`, `put_secret`, `submit_notebook_run`.

## 9. Acceptance checks (how to prove a rebuild works)

1. `/mcp` shows `databricks` connected with 23 tools.
2. `whoami` returns admin@contoso.com with the `admins` group.
3. `sat_status` returns the repo commit, SAT jobs, warehouse state and `security_checks` row count.
4. `sql_query "DROP TABLE x"` is refused; a write tool without the env flag is refused.
5. `run_job` the Driver, then `security_checks` row count increases (latest run 40: 1,220 rows across 10 runs, 2 workspaces).

## 10. Known gaps

- `create_sat_jobs` knows only the original four SAT jobs; v0.9.0 adds three BrickHound jobs.
- Jobs created through the server are not in Terraform state.
- Default node type `Standard_E4ads_v6` hits the 10-core family quota for Permissions Analysis.
- The client secret for the SAT SP expires 2026-12-12; a second SP, "Databricks Prod Testing (SAT)" `49a5203d-...`, exists for a future PRD install.
- The Databricks MCP has no tool for other workspaces (TST, PRD) and none for Log Analytics or DCR work; those used `az` and the Logs Ingestion REST calls directly.
