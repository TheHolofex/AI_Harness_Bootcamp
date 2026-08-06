[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("01", "02", "03", "04", "05", "06", "07", "08", "09", "10")]
  [string]$Pattern
)

$ErrorActionPreference = "Stop"
$PiRoot = Split-Path -Parent $PSScriptRoot
Set-Location $PiRoot

if (-not (Test-Path (Join-Path $PiRoot "node_modules"))) {
  throw "Pi lab dependencies are missing. Run .\scripts\Setup-PiLab.ps1 first."
}
if ([string]::IsNullOrWhiteSpace($env:XAI_API_KEY)) {
  throw "XAI_API_KEY is empty in this PowerShell window."
}

& npm run --silent pattern -- $Pattern
if ($LASTEXITCODE -ne 0) { throw "Pattern $Pattern failed with exit code $LASTEXITCODE." }
