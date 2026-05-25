# Graph Report - talentserv-ai-hackathon-group-11-backend-db  (2026-05-25)

## Corpus Check
- 33 files · ~7,684 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 258 nodes · 460 edges · 29 communities (19 shown, 10 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 67 edges (avg confidence: 0.64)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f98b15db`
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
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 29|Community 29]]

## God Nodes (most connected - your core abstractions)
1. `ToolResponse` - 25 edges
2. `utc_now_iso()` - 16 edges
3. `str` - 16 edges
4. `Office Leave MCP` - 14 edges
5. `Employee` - 13 edges
6. `LeaveRequest` - 13 edges
7. `str` - 12 edges
8. `generate_leave_advice_with_grok()` - 11 edges
9. `connect()` - 11 edges
10. `apply_leave()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `Any` --uses--> `ToolResponse`  [INFERRED]
  src/server.py → src/models.py
- `int` --uses--> `ToolResponse`  [INFERRED]
  src/server.py → src/models.py
- `temp_db()` --calls--> `init_db()`  [INFERRED]
  tests/test_tools.py → src/init_db.py
- `temp_db()` --calls--> `init_db()`  [INFERRED]
  tests/test_tools.py → scripts/init_db.py
- `generate_fallback_advice()` --calls--> `utc_now_iso()`  [INFERRED]
  src/grok_client.py → src/models.py

## Communities (29 total, 10 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.20
Nodes (35): date, Employee, float, LeaveRequest, Row, apply_leave(), calendar_days_inclusive(), check_leave_status() (+27 more)

### Community 1 - "Community 1"
Cohesion: 0.13
Nodes (24): advise_on_leave(), apply_leave(), check_leave_status(), employees_resource(), get_employee(), get_leave_balance(), _json_response(), leave_assistant() (+16 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (36): After any bootstrap, After install, Both MCPs at once, Both servers, code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), code:bash (python scripts/bootstrap_mcp.py --all), code:powershell (irm https://raw.githubusercontent.com/devinraina258/talentse), code:bash (python scripts/mcp_install_lib.py office-leave) (+28 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (25): Add to Cursor, Add to Cursor (one curl per MCP), Both MCPs, code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), code:bash (npm run graphify:sync), code:bash (graphify query "how does apply_leave connect to the database), code:bash (gh auth login), code:powershell (irm https://raw.githubusercontent.com/devinraina258/talentse) (+17 more)

### Community 4 - "Community 4"
Cohesion: 0.12
Nodes (12): init_db(), Connection, Path, run_sql_file(), init_db(), main(), Connection, Path (+4 more)

### Community 5 - "Community 5"
Cohesion: 0.15
Nodes (12): DATABASE_PATH, OFFICE_LEAVE_WORKSPACE, args, command, cwd, mcpServers, graphify, office-leave (+4 more)

### Community 6 - "Community 6"
Cohesion: 0.18
Nodes (11): 1. Create the database, 2. Environment, 3. Run tests, 4. Run the MCP server (stdio), code:bash (git clone https://github.com/devinraina258/talentserv-ai-hac), code:bash (office-leave-init-db), code:bash (copy .env.example .env), code:bash (pytest) (+3 more)

### Community 7 - "Community 7"
Cohesion: 0.23
Nodes (23): bool, ensure_venv(), main(), merge_mcp_server(), print_done(), int, Path, str (+15 more)

### Community 8 - "Community 8"
Cohesion: 0.27
Nodes (8): devDependencies, husky, name, private, scripts, graphify:sync, graphify:sync:unix, prepare

### Community 9 - "Community 9"
Cohesion: 0.67
Nodes (8): LeaveAdvice, default_next_steps(), generate_fallback_advice(), generate_leave_advice_with_grok(), parse_json_from_content(), Any, str, LeaveAdvice

### Community 12 - "Community 12"
Cohesion: 0.47
Nodes (5): main(), int, str, Export graphify-out/graph.json as a compact JSONL tree for LLM context.  Each li, _walk_tree()

## Knowledge Gaps
- **57 isolated node(s):** `prepare`, `graphify:sync`, `graphify:sync:unix`, `husky`, `Any` (+52 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `init_db()` connect `Community 4` to `Community 0`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Why does `ToolResponse` connect `Community 0` to `Community 1`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `utc_now_iso()` connect `Community 0` to `Community 1`, `Community 9`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `ToolResponse` (e.g. with `list_employees()` and `get_employee()`) actually correct?**
  _`ToolResponse` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `utc_now_iso()` (e.g. with `generate_fallback_advice()` and `generate_leave_advice_with_grok()`) actually correct?**
  _`utc_now_iso()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `str` (e.g. with `Employee` and `LeaveRequest`) actually correct?**
  _`str` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Employee` (e.g. with `row_to_employee()` and `Path`) actually correct?**
  _`Employee` has 11 INFERRED edges - model-reasoned connections that need verification._