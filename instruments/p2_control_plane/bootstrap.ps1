#Requires -Version 5.1

[CmdletBinding()]
param(
    [string]$Destination = (Join-Path $env:USERPROFILE 'Documents\HarnessBootcamp\P2_Project_Organizer')
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Starter = Join-Path $PSScriptRoot 'starter'
$RequiredStarterFiles = @(
    'AGENTS.md',
    'PROJECT_ORGANIZER_CONTRACT.md',
    '.codex\config.toml',
    '.agents\plugins\marketplace.json',
    'source_packet\01_project_charter.md',
    'source_packet\02_deliverables.csv',
    'source_packet\03_dependency_notes.md',
    'source_packet\04_decision_log.md',
    'source_packet\05_status_updates.md',
    'source_packet\06_source_register.csv'
)

if (-not (Test-Path -LiteralPath $Starter -PathType Container)) {
    throw "P2 starter folder is missing: $Starter"
}
foreach ($Relative in $RequiredStarterFiles) {
    if (-not (Test-Path -LiteralPath (Join-Path $Starter $Relative) -PathType Leaf)) {
        throw "P2 starter is incomplete. Missing: $Relative"
    }
}

$ResolvedDestination = [System.IO.Path]::GetFullPath($Destination)
if (Test-Path -LiteralPath $ResolvedDestination) {
    throw "P2 project already exists at $ResolvedDestination. Keep it, or move it to a dated archive before running this command again."
}

$DestinationParent = Split-Path $ResolvedDestination -Parent
if ([string]::IsNullOrWhiteSpace($DestinationParent)) {
    throw "Choose a destination with a parent folder."
}
New-Item -ItemType Directory -Path $DestinationParent -Force | Out-Null
$Staging = Join-Path $DestinationParent ('.p2-project-organizer-staging-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $Staging | Out-Null

try {
    Get-ChildItem -LiteralPath $Starter -Force | Copy-Item -Destination $Staging -Recurse -Force
    foreach ($Relative in $RequiredStarterFiles) {
        if (-not (Test-Path -LiteralPath (Join-Path $Staging $Relative) -PathType Leaf)) {
            throw "Staged P2 project is missing: $Relative"
        }
    }
    if (Test-Path -LiteralPath (Join-Path $Staging 'reference')) {
        throw 'The learner copy unexpectedly contains the maintainer reference implementation.'
    }
    Move-Item -LiteralPath $Staging -Destination $ResolvedDestination
} catch {
    $Failure = $_.Exception.Message
    $Cleanup = ''
    if (Test-Path -LiteralPath $Staging) {
        try {
            Remove-Item -LiteralPath $Staging -Recurse -Force
        } catch {
            $Cleanup = " Partial staging folder could not be removed: $Staging."
        }
    }
    throw "P2 bootstrap failed before the final project was created. $Failure$Cleanup"
}

Write-Host 'P2 Project Organizer starter created.'
Write-Host "Project: $ResolvedDestination"
Write-Host 'Next: open this folder in Codex and follow P2 Stage 01 on the course website.'
