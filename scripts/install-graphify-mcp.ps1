# Clone-free: configure graphify MCP in the current directory only.
#   irm https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main/scripts/install-graphify-mcp.ps1 | iex
$ErrorActionPreference = "Stop"
$Base = "https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main"
$Ws = (Get-Location).Path
if (Test-Path "scripts\mcp_install_lib.py") {
    $py = if (Get-Command python -ErrorAction SilentlyContinue) { "python" } else { "python3" }
    & $py scripts/mcp_install_lib.py graphify $Ws
    exit $LASTEXITCODE
}
$Tmp = Join-Path $env:TEMP "mcp-install-$PID"
New-Item -ItemType Directory -Force -Path $Tmp | Out-Null
$Lib = Join-Path $Tmp "mcp_install_lib.py"
Invoke-WebRequest -Uri "$Base/scripts/mcp_install_lib.py" -OutFile $Lib -UseBasicParsing
$py = if (Get-Command python -ErrorAction SilentlyContinue) { "python" } else { "python3" }
& $py $Lib graphify $Ws
