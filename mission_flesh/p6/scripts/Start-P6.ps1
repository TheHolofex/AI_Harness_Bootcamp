<#
.SYNOPSIS
  Build Wave 1 of P6 Clear the Overnight Watch.
#>
param(
  [string]$RunRoot,
  [string]$Model = $env:HB_XAI_MODEL,
  [switch]$PrepareOnly
)

$ErrorActionPreference = "Stop"
$P6Root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$SourceRecipe = Join-Path $P6Root "clear_overnight_watch.yaml"

function Invoke-CheckedNative {
  param([string]$Command, [string[]]$CommandArgs, [string]$Failure)
  $output = & $Command @CommandArgs 2>&1
  if ($LASTEXITCODE -ne 0) {
    throw "$Failure`n$($output | Out-String)"
  }
  return @($output)
}

function Test-P6Runtime {
  if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    throw "P6 requires Node.js on PATH. Install the current Node.js LTS release, open a new PowerShell window, and try again."
  }
  if (-not (Get-Command goose -ErrorAction SilentlyContinue)) {
    throw "P6 requires Goose on PATH. Install the current stable Goose CLI, open a new PowerShell window, and try again."
  }

  $helpText = (Invoke-CheckedNative "goose" @("run", "--help") "Unable to inspect 'goose run --help'.") | Out-String
  if (-not $helpText.Contains("--with-builtin")) {
    throw "The installed Goose CLI does not expose the native Developer extension. Install the current stable Goose CLI, then try again."
  }
  $null = Invoke-CheckedNative "goose" @("recipe", "validate", $SourceRecipe) "The installed Goose CLI rejected the P6 recipe."
  Write-Host "P6 PREFLIGHT PASS recipe plus native Developer capability"
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

# Finish setup checks before replacing the learner's current run.
Test-P6Runtime
if (-not $PrepareOnly) {
  if ([string]::IsNullOrWhiteSpace($Model)) {
    throw "HB_XAI_MODEL is empty. Set the course xAI model or pass -Model before launch."
  }
  if ([string]::IsNullOrWhiteSpace($env:XAI_API_KEY)) {
    throw "XAI_API_KEY is empty. Set it in this PowerShell window, then try again."
  }
}

& node (Join-Path $PSScriptRoot "prepare.mjs") --run-root $RunRoot
if ($LASTEXITCODE -ne 0) { throw "P6 Wave 1 preparation failed." }

if ($PrepareOnly) {
  Write-Host "P6 PREPARE-ONLY PASS run=$RunRoot no model call started"
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
if ($gooseExit -ne 0) { throw "Goose Wave 1 exited with code $gooseExit." }

& node (Join-Path $P6Root "scripts\verify.mjs") --run-root $RunRoot --wave 1
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Open-CommandCenter -Path (Join-Path $RunRoot "command_center.html")
exit 0
