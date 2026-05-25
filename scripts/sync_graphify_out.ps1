# Regenerate graphify-out and stage tracked artifacts for the current commit.
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

function Invoke-Graphify {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Args)
    if (Get-Command graphify -ErrorAction SilentlyContinue) {
        & graphify @Args
        return
    }
    $py = $null
    if (Test-Path ".venv\Scripts\python.exe") { $py = ".venv\Scripts\python.exe" }
    elseif (Test-Path ".venv\bin\python") { $py = ".venv\bin\python" }
    else { $py = "python" }
    & $py -m graphify @Args
}

$python = if (Test-Path ".venv\Scripts\python.exe") { ".venv\Scripts\python.exe" } else { "python" }

Write-Host "[graphify] updating graph (AST, no API key)..."
Invoke-Graphify update .

Write-Host "[graphify] refreshing GRAPH_TREE.html..."
Invoke-Graphify tree --graph graphify-out/graph.json --output graphify-out/GRAPH_TREE.html

Write-Host "[graphify] exporting graph_tree.jsonl..."
& $python scripts/export_graph_tree_jsonl.py

Write-Host "[graphify] staging graphify-out/ (cache and manifest are gitignored)..."
git add graphify-out/

Write-Host "[graphify] sync complete."
