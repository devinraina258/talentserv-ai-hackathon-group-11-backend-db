# Graph Report - talentserv-ai-hackathon-group-11-backend-db  (2026-05-25)

## Corpus Check
- 41 files · ~6,052 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 176 nodes · 229 edges · 24 communities (23 shown, 1 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 24 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `056fe5ab`
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
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]

## God Nodes (most connected - your core abstractions)
1. `Office Leave MCP` - 13 edges
2. `utc_now_iso()` - 12 edges
3. `ToolResponse` - 10 edges
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
- `advise_on_leave()` --calls--> `utc_now_iso()`  [INFERRED]
  src/server.py → src/models.py

## Communities (24 total, 1 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.23
Nodes (20): apply_leave(), calendar_days_inclusive(), check_leave_status(), connect(), _fetch_requests(), get_db_path(), get_employee(), get_employee_context_for_advice() (+12 more)

### Community 1 - "Community 1"
Cohesion: 0.12
Nodes (19): apply_leave(), check_leave_status(), employees_resource(), get_employee(), get_leave_balance(), _json_response(), leave_assistant(), list_employees() (+11 more)

### Community 2 - "Community 2"
Cohesion: 0.12
Nodes (15): After any bootstrap, Both MCPs at once, code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), code:bash (python scripts/bootstrap_mcp.py --all), code:powershell (irm https://raw.githubusercontent.com/devinraina258/talentse), code:bash (python scripts/bootstrap_mcp.py --office-leave), code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), code:powershell (irm https://raw.githubusercontent.com/devinraina258/talentse) (+7 more)

### Community 3 - "Community 3"
Cohesion: 0.12
Nodes (15): code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), code:bash (npm run graphify:sync), code:bash (graphify query "how does apply_leave connect to the database), code:bash (gh auth login), code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), code:bash (pip install "graphifyy[mcp]>=0.8.14"), Employees (seed data), Example prompts in Cursor (+7 more)

### Community 4 - "Community 4"
Cohesion: 0.17
Nodes (3): init_db(), run_sql_file(), temp_db()

### Community 5 - "Community 5"
Cohesion: 0.17
Nodes (11): DATABASE_PATH, args, command, cwd, mcpServers, graphify, office-leave, args (+3 more)

### Community 6 - "Community 6"
Cohesion: 0.18
Nodes (11): 1. Create the database, 2. Environment, 3. Run tests, 4. Run the MCP server (stdio), code:bash (git clone https://github.com/devinraina258/talentserv-ai-hac), code:bash (python scripts/init_db.py), code:bash (copy .env.example .env), code:bash (pytest) (+3 more)

### Community 7 - "Community 7"
Cohesion: 0.47
Nodes (9): ensure_venv(), main(), merge_mcp_server(), print_done(), run(), setup_graphify(), setup_office_leave(), sync_graphify() (+1 more)

### Community 8 - "Community 8"
Cohesion: 0.22
Nodes (8): devDependencies, husky, name, private, scripts, graphify:sync, graphify:sync:unix, prepare

### Community 9 - "Community 9"
Cohesion: 0.22
Nodes (9): Add to Cursor (one curl per MCP), Both MCPs, code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), code:powershell (irm https://raw.githubusercontent.com/devinraina258/talentse), code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), code:powershell (irm https://raw.githubusercontent.com/devinraina258/talentse), code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), graphify only (+1 more)

### Community 10 - "Community 10"
Cohesion: 0.25
Nodes (8): code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), code:powershell (irm https://raw.githubusercontent.com/devinraina258/talentse), code:bash (python scripts/bootstrap_mcp.py --graphify), code:bash (python scripts/bootstrap_mcp.py --graphify --force-graph), curl (macOS / Linux / Git Bash), graphify MCP (code graph queries), Local (no curl), PowerShell (Windows)

### Community 11 - "Community 11"
Cohesion: 0.43
Nodes (7): default_next_steps(), generate_fallback_advice(), generate_leave_advice_with_grok(), parse_json_from_content(), LeaveAdvice, advise_on_leave(), Get AI leave guidance using Grok from employee data and balances.

### Community 12 - "Community 12"
Cohesion: 0.67
Nodes (3): main(), Export graphify-out/graph.json as a compact JSONL tree for LLM context.  Each, _walk_tree()

## Knowledge Gaps
- **49 isolated node(s):** `name`, `private`, `prepare`, `graphify:sync`, `graphify:sync:unix` (+44 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `advise_on_leave()` connect `Community 11` to `Community 0`, `Community 1`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Why does `Office Leave MCP` connect `Community 3` to `Community 9`, `Community 6`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `utc_now_iso()` connect `Community 0` to `Community 11`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `utc_now_iso()` (e.g. with `list_employees()` and `get_employee()`) actually correct?**
  _`utc_now_iso()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `ToolResponse` (e.g. with `list_employees()` and `get_employee()`) actually correct?**
  _`ToolResponse` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `get_employee()` (e.g. with `ToolResponse` and `utc_now_iso()`) actually correct?**
  _`get_employee()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `private`, `prepare` to the rest of the system?**
  _60 weakly-connected nodes found - possible documentation gaps or missing edges._