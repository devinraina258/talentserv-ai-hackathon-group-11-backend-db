# Portable MCP bootstrap (Windows PowerShell):
#   irm https://raw.githubusercontent.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db/main/scripts/bootstrap-mcp.ps1 | iex
# Or from repo root:
#   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/bootstrap-mcp.ps1
param(
    [switch]$Clone,
    [string]$CloneDir = "talentserv-ai-hackathon-group-11-backend-db",
    [string]$RepoUrl = "https://github.com/devinraina258/talentserv-ai-hackathon-group-11-backend-db.git",
    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"

if ($Clone) {
    if (-not (Test-Path "$CloneDir\.git")) {
        Write-Host "[bootstrap] cloning $RepoUrl -> $CloneDir"
        git clone --depth 1 --branch $Branch $RepoUrl $CloneDir 2>$null
        if ($LASTEXITCODE -ne 0) { git clone --depth 1 $RepoUrl $CloneDir }
    }
    Set-Location $CloneDir
}

if (-not (Test-Path "scripts\bootstrap_mcp.py")) {
    throw "Run from repository root, or pass -Clone to clone first."
}

$py = $null
foreach ($candidate in @("python", "py", "python3")) {
    if (Get-Command $candidate -ErrorAction SilentlyContinue) {
        $ver = & $candidate -c "import sys; print(sys.version_info[:2])" 2>$null
        if ($LASTEXITCODE -eq 0) { $py = $candidate; break }
    }
}
if (-not $py) {
    throw "Python 3.10+ required. Install: winget install Python.Python.3.12"
}

Write-Host "[bootstrap] using $(& $py --version)"
& $py scripts/bootstrap_mcp.py --all
