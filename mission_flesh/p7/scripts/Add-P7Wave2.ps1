[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$p7Root = Split-Path -Parent $PSScriptRoot
$inputsRoot = Join-Path $p7Root 'inputs'
$wave1Path = Join-Path $inputsRoot 'wave1.csv'
$wave2Path = Join-Path $inputsRoot 'wave2.csv'
$workbookTemplatePath = Join-Path $inputsRoot 'workboard_80_blank.xlsx'
$activePath = Join-Path $p7Root 'workboard.xlsx'

foreach ($requiredPath in @($wave1Path, $wave2Path, $workbookTemplatePath)) {
  if (-not (Test-Path -LiteralPath $requiredPath -PathType Leaf)) {
    throw "Required P7 file is missing: $requiredPath"
  }
}

$wave1 = @(Import-Csv -LiteralPath $wave1Path)
$wave2 = @(Import-Csv -LiteralPath $wave2Path)
if ($wave1.Count -ne 60) {
  throw "Wave 1 must contain 60 records; found $($wave1.Count)."
}
if ($wave2.Count -ne 20) {
  throw "Wave 2 must contain 20 records; found $($wave2.Count)."
}

$allRows = @($wave1) + @($wave2)
if (@($allRows.id | Sort-Object -Unique).Count -ne 80) {
  throw 'Wave 1 and Wave 2 must contain 80 unique IDs together.'
}

# Replace the active workbook with the immutable 80-row template. Re-running this
# helper cannot duplicate Wave 2. Excel must be closed so the file can be replaced.
Copy-Item -LiteralPath $workbookTemplatePath -Destination $activePath -Force

Write-Host 'P7 WAVE 2 READY: 80 records'
Write-Host "AI WORKBOARD: $activePath"
Write-Host 'NEXT: open workboard.xlsx to see rows 61-80 with blank AI columns. Close Excel, then rerun the same saved P7 workflow. Do not import or rebuild it again.'
