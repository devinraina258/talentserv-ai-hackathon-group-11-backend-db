# Graph Report - talentserv-ai-hackathon-group-11-backend-db  (2026-05-25)

## Corpus Check
- 34 files · ~9,634 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 333 nodes · 660 edges · 32 communities (22 shown, 10 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 92 edges (avg confidence: 0.66)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2d23d1fc`
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
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 31|Community 31]]

## God Nodes (most connected - your core abstractions)
1. `ToolResponse` - 25 edges
2. `utc_now_iso()` - 18 edges
3. `str` - 17 edges
4. `_json_response_enriched()` - 17 edges
5. `str` - 16 edges
6. `generate_output_recommendations()` - 14 edges
7. `generate_leave_advice_with_grok()` - 14 edges
8. `Office Leave MCP` - 14 edges
9. `Employee` - 13 edges
10. `LeaveRequest` - 13 edges

## Surprising Connections (you probably didn't know these)
- `test_fallback_unknown_employee()` --calls--> `generate_fallback_output_recommendations()`  [INFERRED]
  tests/test_grok_enrichment.py → src/grok_client.py
- `temp_db()` --calls--> `init_db()`  [INFERRED]
  tests/test_grok_enrichment.py → src/init_db.py
- `test_grok_enrich_enabled_default()` --calls--> `grok_enrich_enabled()`  [INFERRED]
  tests/test_grok_enrichment.py → src/grok_client.py
- `int` --uses--> `ToolResponse`  [INFERRED]
  src/server.py → src/models.py
- `temp_db()` --calls--> `init_db()`  [INFERRED]
  tests/test_tools.py → src/init_db.py

## Communities (32 total, 10 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.23
Nodes (33): date, Employee, float, LeaveRequest, Row, apply_leave(), calendar_days_inclusive(), check_leave_status() (+25 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (48): run(), grok_enrich_enabled(), advise_on_leave(), apply_leave(), check_leave_status(), _employee_context_for_args(), _employee_slug_from_args(), employees_resource() (+40 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (36): After any bootstrap, After install, Both MCPs at once, Both servers, code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), code:bash (python scripts/bootstrap_mcp.py --all), code:powershell (irm https://raw.githubusercontent.com/devinraina258/talentse), code:bash (python scripts/mcp_install_lib.py office-leave) (+28 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (36): 1. Create the database, 2. Environment, 3. Run tests, 4. Run the MCP server (stdio), Add to Cursor, Add to Cursor (one curl per MCP), Both MCPs, code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t) (+28 more)

### Community 4 - "Community 4"
Cohesion: 0.11
Nodes (13): init_db(), Connection, Path, run_sql_file(), init_db(), main(), Connection, Path (+5 more)

### Community 5 - "Community 5"
Cohesion: 0.15
Nodes (12): DATABASE_PATH, OFFICE_LEAVE_WORKSPACE, args, command, cwd, mcpServers, graphify, office-leave (+4 more)

### Community 6 - "Community 6"
Cohesion: 0.17
Nodes (19): CopyTo(), create_shortcut(), fixup_dbi(), get_root_hkey(), get_shortcuts_folder(), get_special_folder_path(), get_system_dir(), install() (+11 more)

### Community 7 - "Community 7"
Cohesion: 0.21
Nodes (24): bool, ensure_venv(), main(), merge_mcp_server(), print_done(), bool, int, Path (+16 more)

### Community 8 - "Community 8"
Cohesion: 0.27
Nodes (8): devDependencies, husky, name, private, scripts, graphify:sync, graphify:sync:unix, prepare

### Community 9 - "Community 9"
Cohesion: 0.38
Nodes (19): GrokSuggestions, LeaveAdvice, _api_key_configured(), _call_grok(), default_next_steps(), generate_fallback_advice(), generate_fallback_output_recommendations(), generate_leave_advice_with_grok() (+11 more)

### Community 10 - "Community 10"
Cohesion: 0.53
Nodes (4): leave_advice_to_grok(), Any, str, Map LeaveAdvice from advise_on_leave to the standard grok block shape.

### Community 12 - "Community 12"
Cohesion: 0.47
Nodes (5): main(), int, str, Export graphify-out/graph.json as a compact JSONL tree for LLM context.  Each li, _walk_tree()

### Community 31 - "Community 31"
Cohesion: 0.60
Nodes (4): find_and_run(), main(), A test runner for pywin32, run_test()

## Knowledge Gaps
- **57 isolated node(s):** `prepare`, `graphify:sync`, `graphify:sync:unix`, `husky`, `Connection` (+52 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run()` connect `Community 1` to `Community 7`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `init_db()` connect `Community 4` to `Community 0`, `Community 1`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Why does `ToolResponse` connect `Community 0` to `Community 1`, `Community 10`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 21 inferred relationships involving `ToolResponse` (e.g. with `list_employees()` and `get_employee()`) actually correct?**
  _`ToolResponse` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `utc_now_iso()` (e.g. with `_grok_from_parsed()` and `generate_fallback_output_recommendations()`) actually correct?**
  _`utc_now_iso()` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `_json_response_enriched()` (e.g. with `grok_enrich_enabled()` and `generate_output_recommendations()`) actually correct?**
  _`_json_response_enriched()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `str` (e.g. with `Employee` and `LeaveRequest`) actually correct?**
  _`str` has 3 INFERRED edges - model-reasoned connections that need verification._