# Graph Report - talentserv-ai-hackathon-group-11-backend-db  (2026-05-25)

## Corpus Check
- 31 files · ~4,577 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 123 nodes · 179 edges · 13 communities (12 shown, 1 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 24 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `03c9a311`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]

## God Nodes (most connected - your core abstractions)
1. `utc_now_iso()` - 12 edges
2. `ToolResponse` - 10 edges
3. `Office Leave MCP` - 10 edges
4. `connect()` - 9 edges
5. `get_employee()` - 8 edges
6. `apply_leave()` - 8 edges
7. `_json_response()` - 8 edges
8. `resolve_slug()` - 7 edges
9. `check_leave_status()` - 7 edges
10. `get_employee_context_for_advice()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `temp_db()` --calls--> `init_db()`  [INFERRED]
  tests/test_tools.py → scripts/init_db.py
- `row_to_leave_request()` --calls--> `LeaveRequest`  [INFERRED]
  src/db.py → src/models.py
- `generate_fallback_advice()` --calls--> `utc_now_iso()`  [INFERRED]
  src/grok_client.py → src/models.py
- `generate_leave_advice_with_grok()` --calls--> `utc_now_iso()`  [INFERRED]
  src/grok_client.py → src/models.py
- `advise_on_leave()` --calls--> `generate_leave_advice_with_grok()`  [INFERRED]
  src/server.py → src/grok_client.py

## Communities (13 total, 1 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.23
Nodes (20): apply_leave(), calendar_days_inclusive(), check_leave_status(), connect(), _fetch_requests(), get_db_path(), get_employee(), get_employee_context_for_advice() (+12 more)

### Community 1 - "Community 1"
Cohesion: 0.11
Nodes (21): advise_on_leave(), apply_leave(), check_leave_status(), employees_resource(), get_employee(), get_leave_balance(), _json_response(), leave_assistant() (+13 more)

### Community 2 - "Community 2"
Cohesion: 0.11
Nodes (17): Any OS (Python only), code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), code:powershell (irm https://raw.githubusercontent.com/devinraina258/talentse), code:powershell (irm https://raw.githubusercontent.com/devinraina258/talentse), code:powershell (powershell -NoProfile -ExecutionPolicy Bypass -File scripts/), code:bash (python scripts/bootstrap_mcp.py), code:powershell (npm.cmd install) (+9 more)

### Community 3 - "Community 3"
Cohesion: 0.14
Nodes (13): Add to Cursor (one command), code:bash (gh auth login), code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), code:powershell (irm https://raw.githubusercontent.com/devinraina258/talentse), code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), Employees (seed data), Example prompts in Cursor, License (+5 more)

### Community 4 - "Community 4"
Cohesion: 0.17
Nodes (3): init_db(), run_sql_file(), temp_db()

### Community 5 - "Community 5"
Cohesion: 0.18
Nodes (11): 1. Create the database, 2. Environment, 3. Run tests, 4. Run the MCP server (stdio), code:bash (git clone https://github.com/devinraina258/talentserv-ai-hac), code:bash (python scripts/init_db.py), code:bash (copy .env.example .env), code:bash (pytest) (+3 more)

### Community 6 - "Community 6"
Cohesion: 0.62
Nodes (6): ensure_venv(), main(), run(), sync_graphify(), venv_python(), write_mcp_json()

### Community 7 - "Community 7"
Cohesion: 0.67
Nodes (5): default_next_steps(), generate_fallback_advice(), generate_leave_advice_with_grok(), parse_json_from_content(), LeaveAdvice

## Knowledge Gaps
- **27 isolated node(s):** `Prerequisites`, `code:bash (git clone https://github.com/devinraina258/talentserv-ai-hac)`, `code:bash (python scripts/init_db.py)`, `code:bash (copy .env.example .env)`, `code:bash (pytest)` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `advise_on_leave()` connect `Community 1` to `Community 0`, `Community 7`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Why does `utc_now_iso()` connect `Community 0` to `Community 1`, `Community 7`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `ToolResponse` connect `Community 0` to `Community 1`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `utc_now_iso()` (e.g. with `list_employees()` and `get_employee()`) actually correct?**
  _`utc_now_iso()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `ToolResponse` (e.g. with `list_employees()` and `get_employee()`) actually correct?**
  _`ToolResponse` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `get_employee()` (e.g. with `ToolResponse` and `utc_now_iso()`) actually correct?**
  _`get_employee()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `List all office employees with leave balances.`, `Get employee profile and leave balances. employee: slug or name (devin, nisha, g`, `Get remaining annual and sick leave for an employee.` to the rest of the system?**
  _37 weakly-connected nodes found - possible documentation gaps or missing edges._