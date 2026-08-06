[CmdletBinding()]
param(
  [string]$Model = $env:HB_XAI_MODEL
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$p7Root = Split-Path -Parent $PSScriptRoot
$inputsRoot = Join-Path $p7Root 'inputs'
$workflowRoot = Join-Path $p7Root 'workflow'
$outputRoot = Join-Path $p7Root 'out'
$wave1Path = Join-Path $inputsRoot 'wave1.csv'
$workbookTemplatePath = Join-Path $inputsRoot 'workboard_60_blank.xlsx'
$activePath = Join-Path $p7Root 'workboard.xlsx'
$templatePath = Join-Path $workflowRoot 'P7-production-line.template.json'
$workflowPath = Join-Path $workflowRoot 'P7-production-line.json'

if ([string]::IsNullOrWhiteSpace($Model) -or $Model -like 'paste *') {
  throw 'HB_XAI_MODEL is empty or still a placeholder. Restore the course model value, then run Prepare-P7.ps1 again.'
}

foreach ($requiredPath in @($wave1Path, $workbookTemplatePath, $templatePath)) {
  if (-not (Test-Path -LiteralPath $requiredPath -PathType Leaf)) {
    throw "Required P7 file is missing: $requiredPath"
  }
}

New-Item -ItemType Directory -Force -Path $inputsRoot, $workflowRoot, $outputRoot | Out-Null

$wave1 = @(Import-Csv -LiteralPath $wave1Path)
if ($wave1.Count -ne 60) {
  throw "Wave 1 must contain 60 records; found $($wave1.Count)."
}
if (@($wave1.id | Sort-Object -Unique).Count -ne 60) {
  throw 'Wave 1 IDs must be unique.'
}

Copy-Item -LiteralPath $workbookTemplatePath -Destination $activePath -Force

$knownArtifacts = @(
  'AI_workboard.csv',
  'run_receipt.json',
  'workboard_24h.xlsx'
)
foreach ($artifact in $knownArtifacts) {
  $artifactPath = Join-Path $outputRoot $artifact
  if (Test-Path -LiteralPath $artifactPath -PathType Leaf) {
    Remove-Item -LiteralPath $artifactPath -Force
  }
}

function Convert-ToN8nPath {
  param([Parameter(Mandatory = $true)][string]$Path)
  return ([System.IO.Path]::GetFullPath($Path) -replace '\\', '/')
}

$activeN8nPath = Convert-ToN8nPath -Path $activePath
$outputN8nPath = Convert-ToN8nPath -Path $outputRoot
$template = Get-Content -LiteralPath $templatePath -Raw
$generated = $template.Replace('__P7_WORKBOARD__', $activeN8nPath)
$generated = $generated.Replace('__P7_OUTPUT_DIR__', $outputN8nPath)
$generated = $generated.Replace('__P7_MODEL__', $Model)

if ($generated -match '__P7_[A-Z_]+__') {
  throw 'The generated workflow still contains an unresolved P7 placeholder.'
}

$null = $generated | ConvertFrom-Json
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($workflowPath, $generated, $utf8NoBom)

# n8n reads this process-level setting when it starts in the same PowerShell window.
$env:N8N_RESTRICT_FILE_ACCESS_TO = $p7Root

Write-Host 'P7 WAVE 1 READY: 60 records'
Write-Host "IMPORT: $workflowPath"
Write-Host "AI WORKBOARD: $activePath"
Write-Host "MODEL: $Model"
Write-Host "VERIFIER EVIDENCE: $outputRoot"
Write-Host "N8N FILE ACCESS: $p7Root"
Write-Host 'NEXT: open workboard.xlsx and inspect the blank AI columns. Close Excel before you run n8n, then import the generated workflow and attach the xAI credential once.'
