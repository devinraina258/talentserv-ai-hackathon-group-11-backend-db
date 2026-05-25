# office-leave MCP only:
#   irm https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main/scripts/bootstrap-office-leave-mcp.ps1 | iex
$ErrorActionPreference = "Stop"
if (-not (Test-Path "scripts\bootstrap_mcp.py")) {
    throw "Run from repository root."
}
$py = if (Get-Command python -ErrorAction SilentlyContinue) { "python" } else { "python3" }
& $py scripts/bootstrap_mcp.py --office-leave
