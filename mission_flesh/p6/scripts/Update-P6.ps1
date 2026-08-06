<#
.SYNOPSIS
  Apply a plain-language intent and rebuild P6 after the late update.
#>
param(
  [string]$RunRoot,
  [string]$Model = $env:HB_XAI_MODEL,
  [string]$Intent,
  [switch]$PrepareOnly
)

$ErrorActionPreference = "Stop"
$P6Root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path

function Test-P6Runtime {
  if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    throw "P6 requires Node.js on PATH. Install the current Node.js LTS release, open a new PowerShell window, and try again."
  }
  if (-not (Get-Command goose -ErrorAction SilentlyContinue)) {
    throw "P6 requires Goose on PATH. Install the current stable Goose CLI, open a new PowerShell window, and try again."
  }
}

function Open-CommandCenter {
  param([string]$Path)
  if ([System.Environment]::OSVersion.Platform -ne [System.PlatformID]::Win32NT) { return }
  try {
    Start-Process -FilePath $Path | Out-Null
  } catch {
    Write-Warning "P6 passed, but Windows could not open the command center automatically. Open it manually: $Path"
  }
}

if ([string]::IsNullOrWhiteSpace($RunRoot)) {
  $RunRoot = Join-Path $P6Root "runs\current"
}
$RunRoot = [System.IO.Path]::GetFullPath($RunRoot)
if ([string]::IsNullOrWhiteSpace($Intent)) {
  throw "Paste one complete Wave 2 command from the P6 lesson."
}

# Finish setup checks before changing the current command center or revealing Wave 2.
Test-P6Runtime
if (-not $PrepareOnly) {
  if ([string]::IsNullOrWhiteSpace($Model)) {
    throw "HB_XAI_MODEL is empty. Set the course xAI model or pass -Model before launch."
  }
  if ([string]::IsNullOrWhiteSpace($env:XAI_API_KEY)) {
    throw "XAI_API_KEY is empty. Set it in this PowerShell window, then try again."
  }
}

& node (Join-Path $P6Root "scripts\update.mjs") --run-root $RunRoot --intent $Intent
if ($LASTEXITCODE -ne 0) { throw "P6 Wave 2 preparation failed." }

if ($PrepareOnly) {
  Write-Host "P6 UPDATE PREPARE-ONLY PASS run=$RunRoot no model call started"
  exit 0
}

$env:GOOSE_PROVIDER = "xai"
$env:GOOSE_MODEL = $Model
$env:GOOSE_MODE = "auto"

Push-Location -LiteralPath $RunRoot
try {
  & goose run --recipe ./mission.yaml --provider xai --model $Model --with-builtin developer
  $gooseExit = $LASTEXITCODE
} finally {
  Pop-Location
}
if ($gooseExit -ne 0) { throw "Goose Wave 2 exited with code $gooseExit." }

& node (Join-Path $P6Root "scripts\verify.mjs") --run-root $RunRoot --wave 2
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Open-CommandCenter -Path (Join-Path $RunRoot "command_center.html")
exit 0
