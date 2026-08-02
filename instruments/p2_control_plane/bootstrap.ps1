[CmdletBinding()]
param(
    [string]$P1Source,

    [string]$Destination = (Join-Path $env:USERPROFILE "Documents\HarnessBootcamp\P2_Control_Plane")
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$starter = Join-Path $PSScriptRoot "starter"
if ([string]::IsNullOrWhiteSpace($P1Source)) {
    $P1Source = Join-Path $repoRoot "mission_flesh\p1"
}

foreach ($required in @($starter, $P1Source)) {
    if (-not (Test-Path -LiteralPath $required -PathType Container)) {
        throw "Required course path is missing: $required"
    }
}

$p1EvidenceFiles = @("SOURCE_MANIFEST.md", "AUDIT.md", "RELEASE_RECORD.md")
$missingEvidence = @(
    foreach ($relative in $p1EvidenceFiles) {
        if (-not (Test-Path -LiteralPath (Join-Path $P1Source $relative) -PathType Leaf)) {
            $relative
        }
    }
    if (-not (Test-Path -LiteralPath (Join-Path $P1Source "corpus") -PathType Container)) {
        "corpus"
    }
)
if ($missingEvidence.Count -gt 0) {
    throw "P1 is not complete at $P1Source. Missing: $($missingEvidence -join ', '). If you completed P1 in another project, rerun with -P1Source set to that project's mission_flesh\p1 folder."
}
$p1CorpusFiles = @(Get-ChildItem -LiteralPath (Join-Path $P1Source "corpus") -File -Filter "C*.md")
if ($p1CorpusFiles.Count -eq 0) {
    throw "P1 is not complete at $P1Source. Its corpus contains no C-number source files."
}

if (Test-Path -LiteralPath $Destination) {
    throw "P2 project already exists at $Destination. Keep it, or move it to a dated archive before running this command again."
}

$destinationParent = Split-Path $Destination -Parent
New-Item -ItemType Directory -Path $destinationParent -Force | Out-Null
$staging = Join-Path $destinationParent (".p2-control-plane-staging-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $staging | Out-Null

try {
    Get-ChildItem -LiteralPath $starter -Force | Copy-Item -Destination $staging -Recurse -Force

    $p1Destination = Join-Path $staging "inputs\p1"
    New-Item -ItemType Directory -Path $p1Destination -Force | Out-Null
    Get-ChildItem -LiteralPath $P1Source -Force | Copy-Item -Destination $p1Destination -Recurse -Force

    $stagedRequired = @(
        "AGENTS.md",
        "HARNESS_PROFILE.md",
        "P2_CONTROL_PLANE.json",
        ".agents\skills\daily-brief-release\SKILL.md",
        ".codex\agents\evidence_scout.toml",
        ".codex\agents\docs_researcher.toml",
        ".codex\agents\decision_reviewer.toml",
        "plugins\p2-release-control\hooks\quality_gate.py",
        "inputs\p1\SOURCE_MANIFEST.md",
        "inputs\p1\AUDIT.md",
        "inputs\p1\RELEASE_RECORD.md"
    )
    foreach ($relative in $stagedRequired) {
        if (-not (Test-Path -LiteralPath (Join-Path $staging $relative) -PathType Leaf)) {
            throw "Staged P2 project is missing $relative"
        }
    }
    $stagedCorpus = Join-Path $staging "inputs\p1\corpus"
    if (-not (Test-Path -LiteralPath $stagedCorpus -PathType Container) -or
        @(Get-ChildItem -LiteralPath $stagedCorpus -File -Filter "C*.md").Count -eq 0) {
        throw "Staged P2 project has no P1 C-number source files"
    }

    Move-Item -LiteralPath $staging -Destination $Destination
} catch {
    $failure = $_.Exception.Message
    $cleanup = ""
    if (Test-Path -LiteralPath $staging) {
        try {
            Remove-Item -LiteralPath $staging -Recurse -Force
        } catch {
            $cleanup = " Partial staging folder could not be removed: $staging."
        }
    }
    throw "P2 bootstrap failed before the final project was created. $failure$cleanup"
}

Write-Host "P2 control-plane project created."
Write-Host "Project:   $Destination"
Write-Host "P1 source: $P1Source"
Write-Host "Next: open this project in Codex and follow P2 Stage 01 on the course website."
