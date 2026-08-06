[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$PiRoot = Split-Path -Parent $PSScriptRoot
Set-Location $PiRoot

$nodeVersion = (& node --version 2>&1 | Out-String).Trim()
if ($LASTEXITCODE -ne 0 -or $nodeVersion -notmatch '^v(2[3-9]|22\.(1[9-9]|[2-9][0-9]))(?:\.|$)') {
  throw "Pi 0.83.0 needs Node 22.19 or newer. Found '$nodeVersion'."
}
if ([string]::IsNullOrWhiteSpace($env:XAI_API_KEY)) {
  throw "XAI_API_KEY is empty in this PowerShell window."
}
if ([string]::IsNullOrWhiteSpace($env:HB_XAI_MODEL)) {
  throw "HB_XAI_MODEL is empty in this PowerShell window."
}

& npm ci --ignore-scripts
if ($LASTEXITCODE -ne 0) { throw "npm ci failed with exit code $LASTEXITCODE." }
& npm run check
if ($LASTEXITCODE -ne 0) { throw "TypeScript check failed with exit code $LASTEXITCODE." }
& npm test
if ($LASTEXITCODE -ne 0) { throw "Offline pattern tests failed with exit code $LASTEXITCODE." }

"PI LAB READY patterns=10 model=$env:HB_XAI_MODEL node=$nodeVersion"
