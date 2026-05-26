# Graph Report - talentserv-ai-hackathon-group-11-backend-db  (2026-05-26)

## Corpus Check
- 77 files · ~19,714 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 418 nodes · 604 edges · 48 communities (46 shown, 2 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 95 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `99d066d7`
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
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 47|Community 47]]

## God Nodes (most connected - your core abstractions)
1. `_json_response_enriched()` - 18 edges
2. `main()` - 14 edges
3. `run()` - 14 edges
4. `utc_now_iso()` - 14 edges
5. `Office Leave MCP` - 14 edges
6. `install()` - 12 edges
7. `ensure_enriched_text()` - 12 edges
8. `generate_output_recommendations()` - 11 edges
9. `generate_leave_advice_with_grok()` - 11 edges
10. `_resource_response_enriched()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `test_fallback_unknown_employee()` --calls--> `generate_fallback_output_recommendations()`  [INFERRED]
  tests/test_grok_enrichment.py → src/grok_client.py
- `office-leave MCP launcher` --semantically_similar_to--> `Office Leave MCP`  [INFERRED] [semantically similar]
  docs/MCP_SETUP.md → README.md
- `graphify MCP launcher` --semantically_similar_to--> `graphify knowledge graph`  [INFERRED] [semantically similar]
  docs/MCP_SETUP.md → README.md
- `test_enriched_apply_leave_fallback()` --calls--> `run()`  [INFERRED]
  tests/test_grok_enrichment.py → scripts/bootstrap_mcp.py
- `test_enriched_apply_leave_with_mock_grok()` --calls--> `run()`  [INFERRED]
  tests/test_grok_enrichment.py → scripts/bootstrap_mcp.py

## Hyperedges (group relationships)
- **Dual MCP hackathon stack** — readme_office_leave_mcp, readme_graphify_knowledge_graph, mcp_setup_office_leave_launcher, mcp_setup_graphify_launcher [INFERRED 0.85]

## Communities (48 total, 2 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (52): ordered_payload_with_grok(), apply_leave(), check_leave_status(), _employee_context_for_args(), _employee_slug_from_args(), employees_resource(), _format_enriched_response(), get_employee() (+44 more)

### Community 1 - "Community 1"
Cohesion: 0.14
Nodes (22): ensure_venv(), main(), print_done(), run(), setup_graphify(), setup_office_leave(), sync_graphify(), venv_python() (+14 more)

### Community 2 - "Community 2"
Cohesion: 0.14
Nodes (30): apply_leave(), calendar_days_inclusive(), check_leave_status(), connect(), _fetch_requests(), get_db_path(), get_employee(), get_employee_context_for_advice() (+22 more)

### Community 3 - "Community 3"
Cohesion: 0.17
Nodes (19): CopyTo(), create_shortcut(), fixup_dbi(), get_root_hkey(), get_shortcuts_folder(), get_special_folder_path(), get_system_dir(), install() (+11 more)

### Community 4 - "Community 4"
Cohesion: 0.29
Nodes (17): _api_key_configured(), _call_grok(), _chat_completions_url(), default_next_steps(), _effective_model(), generate_fallback_advice(), generate_fallback_output_recommendations(), generate_leave_advice_with_grok() (+9 more)

### Community 5 - "Community 5"
Cohesion: 0.12
Nodes (16): DATABASE_PATH, GROK_API_URL, GROK_ENRICH_OUTPUTS, GROK_MODEL, GROK_PROVIDER, OFFICE_LEAVE_WORKSPACE, args, command (+8 more)

### Community 6 - "Community 6"
Cohesion: 0.14
Nodes (6): init_db(), main(), Create SQLite database from packaged schema.sql and seed.sql., run_sql_file(), temp_db(), temp_db()

### Community 7 - "Community 7"
Cohesion: 0.22
Nodes (8): devDependencies, husky, name, private, scripts, graphify:sync, graphify:sync:unix, prepare

### Community 8 - "Community 8"
Cohesion: 0.32
Nodes (8): clone-free MCP install via curl, graphify MCP launcher, office-leave MCP launcher, graphify knowledge graph, Grok tool response enrichment, Office Leave MCP, SQLite employees database, CI graphify-out sync workflow

### Community 10 - "Community 10"
Cohesion: 0.60
Nodes (4): find_and_run(), main(), A test runner for pywin32, run_test()

### Community 11 - "Community 11"
Cohesion: 0.67
Nodes (3): main(), Export graphify-out/graph.json as a compact JSONL tree for LLM context.  Each, _walk_tree()

### Community 12 - "Community 12"
Cohesion: 0.50
Nodes (3): load_workspace_env(), Load .env from Cursor workspace before other modules read os.environ., Load .env from cwd, repo root, and OFFICE_LEAVE_WORKSPACE (MCP sets this).

### Community 32 - "Community 32"
Cohesion: 0.07
Nodes (28): 1. Create the database, 2. Environment, 3. Run tests, 4. Run the MCP server (stdio), Add to Cursor, code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), code:bash (npm run graphify:sync), code:bash (graphify query "how does apply_leave connect to the database) (+20 more)

### Community 33 - "Community 33"
Cohesion: 0.08
Nodes (24): After install, Both servers, code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), code:powershell (irm https://raw.githubusercontent.com/devinraina258/talentse), code:bash (python scripts/mcp_install_lib.py office-leave), code:bash (curl -fsSL https://raw.githubusercontent.com/devinraina258/t), code:powershell (irm https://raw.githubusercontent.com/devinraina258/talentse), code:bash (python scripts/mcp_install_lib.py graphify) (+16 more)

### Community 34 - "Community 34"
Cohesion: 0.12
Nodes (23): Middleware, _employee_context_for_args(), ensure_enriched_text(), format_enriched_response(), _grok_text_footer(), _grok_text_header(), GrokEnrichmentMiddleware, is_enriched_response() (+15 more)

### Community 35 - "Community 35"
Cohesion: 0.50
Nodes (3): Answer, Q: Why does init_db connect Database initialization to Leave database layer?, Source Nodes

### Community 36 - "Community 36"
Cohesion: 0.50
Nodes (3): Answer, Q: Is grok giving recommendations for MCP office-leave?, Source Nodes

### Community 37 - "Community 37"
Cohesion: 0.12
Nodes (24): allow(), allow_note(), allow_updated_shell(), cache_key(), conversation_id(), deny(), emit(), file_path() (+16 more)

### Community 39 - "Community 39"
Cohesion: 0.18
Nodes (10): cache-cow hooks (Cursor), code:powershell (Get-Content $env:TEMP\cursor-hooks.log -Wait -Tail 20), code:bash (git update-index --chmod=+x .cursor/hooks/*.sh), code:bash (chmod +x .cursor/hooks/*.sh), Configuration, Make scripts executable (Git on Windows), Prerequisites, Upstream (+2 more)

### Community 40 - "Community 40"
Cohesion: 0.29
Nodes (6): hooks, postToolUse, preCompact, preToolUse, sessionStart, version

### Community 47 - "Community 47"
Cohesion: 0.50
Nodes (8): _create_venv_python(), install_graphify(), install_office_leave(), _install_office_leave_into_venv(), main(), merge_mcp_json(), _venv_python(), write_launcher()

## Knowledge Gaps
- **69 isolated node(s):** `name`, `private`, `prepare`, `graphify:sync`, `graphify:sync:unix` (+64 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `_json_response_enriched()` connect `Community 0` to `Community 1`, `Community 2`, `Community 34`, `Community 4`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `advise_on_leave()` connect `Community 2` to `Community 0`, `Community 4`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `run()` connect `Community 1` to `Community 34`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `_json_response_enriched()` (e.g. with `resolve_grok_block()` and `format_enriched_response()`) actually correct?**
  _`_json_response_enriched()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `main()` (e.g. with `load_input()` and `conversation_id()`) actually correct?**
  _`main()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `run()` (e.g. with `test_enriched_apply_leave_fallback()` and `test_enriched_apply_leave_with_mock_grok()`) actually correct?**
  _`run()` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `utc_now_iso()` (e.g. with `list_employees()` and `get_employee()`) actually correct?**
  _`utc_now_iso()` has 12 INFERRED edges - model-reasoned connections that need verification._