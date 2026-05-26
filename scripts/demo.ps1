# One-command WhatsApp demo: prerequisites + webhook + cloudflared tunnel.
# Usage (from anywhere):
#   powershell -ExecutionPolicy Bypass -File .\scripts\demo.ps1
#   powershell -ExecutionPolicy Bypass -File .\scripts\demo.ps1 -CheckOnly

param(
    [switch]$CheckOnly,
    [int]$Port = 8000
)

$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $Root

$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" +
            [System.Environment]::GetEnvironmentVariable("Path", "User")

function Write-Step($msg) { Write-Host "`n==> $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "  OK  $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "  !!  $msg" -ForegroundColor Yellow }
function Write-Fail($msg) { Write-Host "  XX  $msg" -ForegroundColor Red; throw $msg }

Write-Host "Office Leave WhatsApp demo - $Root" -ForegroundColor White

# --- Python / venv ---
Write-Step "Python venv"
$Py = Join-Path $Root ".cursor\mcp-venv\Scripts\python.exe"
if (-not (Test-Path $Py)) {
    $base = Get-Command python -ErrorAction SilentlyContinue
    if (-not $base) { Write-Fail "python not found. Install Python 3.10+." }
    Write-Warn "Creating .cursor\mcp-venv ..."
    & $base.Source -m venv (Join-Path $Root ".cursor\mcp-venv")
    if (-not (Test-Path $Py)) { Write-Fail "venv creation failed." }
}
Write-Ok "venv: $Py"

Write-Step "Install package [whatsapp]"
& $Py -m pip install -q -e ".[whatsapp]"
Write-Ok "dependencies installed"

# --- .env ---
Write-Step ".env"
$EnvFile = Join-Path $Root ".env"
if (-not (Test-Path $EnvFile)) {
    Copy-Item (Join-Path $Root ".env.example") $EnvFile
    Write-Fail "Created .env from .env.example - fill TWILIO_* and WHATSAPP_PHONE_MAP, then re-run."
}

$prevEap = $ErrorActionPreference
$ErrorActionPreference = "Continue"
$envCheckOut = & $Py -c @"
import sys
from dotenv import dotenv_values
v = dotenv_values('.env')
need = ('TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'WHATSAPP_PHONE_MAP')
bad = []
for k in need:
    x = (v.get(k) or '').strip()
    if not x or 'your_' in x.lower() or 'YOUR_' in x:
        bad.append(k)
if bad:
    sys.stderr.write('missing:' + ','.join(bad))
    raise SystemExit(1)
print('ok')
"@ 2>&1
$envExit = $LASTEXITCODE
$ErrorActionPreference = $prevEap
if ($envExit -ne 0) {
    $missing = ($envCheckOut | Out-String).Trim()
    if ($missing -match 'missing:(.+)') {
        Write-Fail @"
.env is missing or empty on disk: $($Matches[1])
1. Open .env in Cursor and paste from https://console.twilio.com/
2. Save the file (Ctrl+S) - unsaved editor content is not read by this script
3. Re-run: powershell -ExecutionPolicy Bypass -File .\scripts\demo.ps1
"@
    }
    Write-Fail "Invalid .env: $missing"
}
Write-Ok ".env has Twilio + WHATSAPP_PHONE_MAP"

# --- Database ---
Write-Step "Database"
$dbRel = (& $Py -c "from dotenv import dotenv_values; print(dotenv_values('.env').get('DATABASE_PATH') or 'data/employees.db')").Trim()
$DbPath = Join-Path $Root $dbRel
if (-not (Test-Path $DbPath)) {
    Write-Warn "Initializing $dbRel ..."
    & $Py -m src.init_db
}
if (-not (Test-Path $DbPath)) { Write-Fail "Database missing after init_db." }
Write-Ok "database: $dbRel"

# --- cloudflared ---
Write-Step "cloudflared"
$CfCandidates = @(
    "C:\Program Files (x86)\cloudflared\cloudflared.exe",
    "C:\Program Files\cloudflared\cloudflared.exe",
    (Join-Path $env:LOCALAPPDATA "Microsoft\WinGet\Links\cloudflared.exe")
)
$Cf = $null
foreach ($c in $CfCandidates) {
    if (Test-Path $c) { $Cf = $c; break }
}
if (-not $Cf) {
    $which = Get-Command cloudflared -ErrorAction SilentlyContinue
    if ($which) { $Cf = $which.Source }
}
if (-not $Cf) {
    Write-Fail @"
cloudflared not found. Install:
  winget install Cloudflare.cloudflared -e
Then open a NEW terminal and re-run this script.
"@
}
Write-Ok "cloudflared: $Cf"

# --- Port ---
Write-Step "Port $Port"
$onPort = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
if ($onPort) {
    Write-Warn "Port $Port in use (PID $($onPort.OwningProcess)). Stopping ..."
    Stop-Process -Id $onPort.OwningProcess -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
}
Write-Ok "port $Port free"

# --- Health import smoke test ---
Write-Step "Import webhook app"
& $Py -c "from src.whatsapp.twilio_webhook import app; print('app ok')" 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) { Write-Fail "Cannot import src.whatsapp.twilio_webhook" }
Write-Ok "FastAPI app loads"

if ($CheckOnly) {
    Write-Host "`nAll prerequisites passed (-CheckOnly). Run without -CheckOnly to start demo." -ForegroundColor Green
    exit 0
}

# --- Start webhook (background) ---
Write-Step "Starting webhook on :$Port"
$uvicornArgs = "-m uvicorn src.whatsapp.twilio_webhook:app --host 0.0.0.0 --port $Port"
$webhookJob = Start-Process -FilePath $Py -ArgumentList $uvicornArgs `
    -WorkingDirectory $Root -PassThru -WindowStyle Minimized
Start-Sleep -Seconds 2
try {
    $health = Invoke-RestMethod "http://127.0.0.1:$Port/health" -TimeoutSec 5
    if ($health.status -ne "ok") { Write-Fail "Health check failed." }
} catch {
    Stop-Process -Id $webhookJob.Id -Force -ErrorAction SilentlyContinue
    Write-Fail "Webhook did not start on port $Port. Check minimized window for errors."
}
Write-Ok "webhook PID $($webhookJob.Id) - http://127.0.0.1:$Port/health"

Write-Host @"

  Twilio sandbox webhook (POST) - update EVERY time you run this script:
    https://<your-new-url>.trycloudflare.com/whatsapp/webhook

  WhatsApp: help | balance | status | apply annual 2026-06-10 2026-06-11 reason

  Press Ctrl+C to stop cloudflared (webhook keeps running in background; kill PID $($webhookJob.Id) if needed).

"@ -ForegroundColor Yellow

Write-Step "Starting cloudflared (public URL below)"
& $Cf tunnel --url "http://127.0.0.1:$Port"
