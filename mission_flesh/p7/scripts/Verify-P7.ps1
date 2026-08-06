[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Assert-True {
  param(
    [Parameter(Mandatory = $true)][bool]$Condition,
    [Parameter(Mandatory = $true)][string]$Message
  )
  if (-not $Condition) {
    throw "VERIFY FAIL: $Message"
  }
}

$p7Root = Split-Path -Parent $PSScriptRoot
$inputsRoot = Join-Path $p7Root 'inputs'
$outputRoot = Join-Path $p7Root 'out'
$wave1Path = Join-Path $inputsRoot 'wave1.csv'
$wave2Path = Join-Path $inputsRoot 'wave2.csv'
$workboardPath = Join-Path $p7Root 'workboard.xlsx'
$mirrorPath = Join-Path $outputRoot 'AI_workboard.csv'
$receiptPath = Join-Path $outputRoot 'run_receipt.json'

foreach ($productPath in @($workboardPath, $mirrorPath, $receiptPath)) {
  Assert-True (Test-Path -LiteralPath $productPath -PathType Leaf) "missing product $productPath"
  Assert-True ((Get-Item -LiteralPath $productPath).Length -gt 0) "empty product $productPath"
}
Assert-True ((Get-Item -LiteralPath $workboardPath).Length -gt 1000) 'workboard.xlsx is too small to be a valid workbook'
Write-Host 'PASS products: workboard.xlsx, AI_workboard.csv, and run_receipt.json exist'

$wave1 = @(Import-Csv -LiteralPath $wave1Path)
$wave2 = @(Import-Csv -LiteralPath $wave2Path)
Assert-True ($wave1.Count -eq 60) "Wave 1 source has $($wave1.Count) records, expected 60"
Assert-True ($wave2.Count -eq 20) "Wave 2 source has $($wave2.Count) records, expected 20"
Assert-True (@(($wave1 + $wave2).id | Sort-Object -Unique).Count -eq 80) 'source IDs are not unique across waves'
Write-Host 'PASS source fixtures: Wave 1 = 60, Wave 2 = 20, unique IDs = 80'

$rows = @(Import-Csv -LiteralPath $mirrorPath)
Assert-True (($rows.Count -eq 60) -or ($rows.Count -eq 80)) "AI workboard mirror has $($rows.Count) rows, expected 60 or 80"
$expectedIds = if ($rows.Count -eq 60) { @($wave1.id) } else { @(($wave1 + $wave2).id) }
Assert-True (@($rows.id | Sort-Object -Unique).Count -eq $rows.Count) 'AI workboard mirror contains duplicate IDs'
Assert-True ((Compare-Object ($expectedIds | Sort-Object) ($rows.id | Sort-Object)).Count -eq 0) 'AI workboard IDs do not match the revealed source waves'

$requiredColumns = @(
  'id', 'received_at', 'requester', 'channel', 'text', 'wave',
  'workstream', 'priority', 'summary', 'next_action',
  'branch_policy', 'policy_value', 'sla_hours', 'target_by'
)
$actualColumns = @($rows[0].PSObject.Properties.Name)
foreach ($column in $requiredColumns) {
  Assert-True ($actualColumns -contains $column) "AI Workboard is missing column $column"
}

$allowedWorkstreams = @('OPERATIONS', 'FINANCE', 'PEOPLE', 'TECHNOLOGY')
$allowedPriorities = @('P1', 'P2', 'P3')
foreach ($row in $rows) {
  Assert-True ($allowedWorkstreams -contains $row.workstream) "record $($row.id) has invalid workstream $($row.workstream)"
  Assert-True ($allowedPriorities -contains $row.priority) "record $($row.id) has invalid priority $($row.priority)"
  foreach ($field in @('id', 'received_at', 'requester', 'channel', 'text', 'wave', 'summary', 'next_action', 'branch_policy', 'policy_value')) {
    Assert-True (-not [string]::IsNullOrWhiteSpace([string]$row.$field)) "record $($row.id) has blank $field"
  }
}
Write-Host "PASS AI Workboard: $($rows.Count) rows, exact IDs, 14 columns, complete AI fields, valid enums"

$policySpecs = @(
  @{ Workstream = 'FINANCE'; Policy = 'Finance owner + evidence'; PolicyValue = 'Assign an owner and attach the supporting financial evidence' },
  @{ Workstream = 'PEOPLE'; Policy = 'People owner + private channel'; PolicyValue = 'Assign a People owner and continue in the private case channel' },
  @{ Workstream = 'TECHNOLOGY'; Policy = 'Technology triage + incident link'; PolicyValue = 'Assign technical triage and link the service or incident record' }
)
$workstreamCounts = @{}
foreach ($workstream in $allowedWorkstreams) {
  $workstreamCounts[$workstream] = @($rows | Where-Object { $_.workstream -eq $workstream }).Count
  Assert-True ($workstreamCounts[$workstream] -gt 0) "$workstream has no rows"
}
Assert-True (($workstreamCounts.Values | Measure-Object -Sum).Sum -eq $rows.Count) 'workstream counts do not sum to the AI Workboard row count'

foreach ($spec in $policySpecs) {
  foreach ($row in @($rows | Where-Object { $_.workstream -eq $spec.Workstream })) {
    Assert-True ($row.branch_policy -eq $spec.Policy) "record $($row.id) did not receive the exact $($spec.Workstream) branch policy"
    Assert-True ($row.policy_value -eq $spec.PolicyValue) "record $($row.id) did not receive the exact $($spec.Workstream) policy value"
    Assert-True ([string]::IsNullOrWhiteSpace([string]$row.sla_hours)) "record $($row.id) has an unexpected non-Operations SLA"
    Assert-True ([string]::IsNullOrWhiteSpace([string]$row.target_by)) "record $($row.id) has an unexpected non-Operations target_by"
  }
}
Write-Host "PASS workstream routing: OPERATIONS=$($workstreamCounts.OPERATIONS) FINANCE=$($workstreamCounts.FINANCE) PEOPLE=$($workstreamCounts.PEOPLE) TECHNOLOGY=$($workstreamCounts.TECHNOLOGY)"

$operations = @($rows | Where-Object { $_.workstream -eq 'OPERATIONS' })
$slaValues = @($operations.sla_hours | ForEach-Object { [int]$_ } | Sort-Object -Unique)
Assert-True ($slaValues.Count -eq 1) 'Operations rows do not share one SLA value'
$operationsSlaHours = [int]$slaValues[0]
Assert-True (($operationsSlaHours -eq 24) -or ($operationsSlaHours -eq 8)) "Operations SLA is ${operationsSlaHours}h, expected the starting 24h or learner edit 8h"
foreach ($row in $operations) {
  Assert-True ($row.branch_policy -eq "Operations SLA ${operationsSlaHours}h") "record $($row.id) branch_policy does not match ${operationsSlaHours}h"
  Assert-True ($row.policy_value -eq "Respond within $operationsSlaHours hours") "record $($row.id) policy_value does not match ${operationsSlaHours}h"
  $received = [DateTimeOffset]::Parse($row.received_at)
  $target = [DateTimeOffset]::Parse($row.target_by)
  $deltaSeconds = [Math]::Abs(($target - $received.AddHours($operationsSlaHours)).TotalSeconds)
  Assert-True ($deltaSeconds -lt 1) "record $($row.id) target_by is not received_at + ${operationsSlaHours}h"
}
Write-Host "PASS Operations policy: ${operationsSlaHours}h applied to $($operations.Count)/$($operations.Count) Operations rows"
Write-Host 'PASS branch policies: exact Finance, People, and Technology rules; SLA fields only on Operations'

$receipt = Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json
Assert-True ($receipt.sheet_name -eq 'AI Workboard') 'run receipt sheet_name is not AI Workboard'
Assert-True ([int]$receipt.record_count -eq $rows.Count) 'run receipt record_count does not match the AI Workboard'
Assert-True ([int]$receipt.operations_sla_hours -eq $operationsSlaHours) 'run receipt Operations SLA does not match the AI Workboard'
foreach ($workstream in $allowedWorkstreams) {
  Assert-True ([int]$receipt.workstream_counts.$workstream -eq $workstreamCounts[$workstream]) "run receipt $workstream count does not match the AI Workboard"
}
$expectedProducts = @('workboard.xlsx', 'AI_workboard.csv', 'run_receipt.json')
Assert-True (@($receipt.products).Count -eq 3) 'run receipt must name three products'
foreach ($product in $expectedProducts) {
  Assert-True (@($receipt.products) -contains $product) "run receipt is missing product $product"
}
Write-Host 'PASS run receipt: row count, workstream counts, SLA, sheet, and product list agree'

Write-Host "P7 SPREADSHEET CONTROL VERIFIED: $($rows.Count) rows, workboard.xlsx + verifier evidence, Operations SLA ${operationsSlaHours}h"
