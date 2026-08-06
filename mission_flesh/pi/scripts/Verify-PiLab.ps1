[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$PiRoot = Split-Path -Parent $PSScriptRoot
Set-Location $PiRoot

& npm run --silent verify
if ($LASTEXITCODE -ne 0) { throw "Pi lab verification failed with exit code $LASTEXITCODE." }
