#Requires -Version 5.1

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ManagedMarker = '# Managed by AI Harness Bootcamp P3 MCP evidence installer v1.'
$ConfigureScript = Join-Path $PSScriptRoot 'configure-p3-mcp.ps1'
$ServerPath = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'server.mjs'))
$FrozenBriefPath = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\p3_frozen_brief'))
$TemporaryRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("p3-mcp-config-smoke-" + [guid]::NewGuid().ToString('N'))
$OriginalPath = $env:PATH

function Write-TestFile {
    param(
        [Parameter(Mandatory = $true)][string]$LiteralPath,
        [Parameter(Mandatory = $true)][string]$Content
    )

    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($LiteralPath, $Content, $Utf8NoBom)
}

function Convert-TestTomlPath {
    param([Parameter(Mandatory = $true)][string]$Path)

    return ([System.IO.Path]::GetFullPath($Path)).Replace('\', '/').Replace('"', '\"')
}

function Assert-Equal {
    param(
        [Parameter(Mandatory = $true)]$Actual,
        [Parameter(Mandatory = $true)]$Expected,
        [Parameter(Mandatory = $true)][string]$Label
    )

    if ($Actual -cne $Expected) {
        throw "$Label did not match the expected value."
    }
}

function Assert-Throws {
    param(
        [Parameter(Mandatory = $true)][scriptblock]$Action,
        [Parameter(Mandatory = $true)][string]$MessagePattern,
        [Parameter(Mandatory = $true)][string]$Label
    )

    $Caught = $null
    try {
        & $Action
    } catch {
        $Caught = $_
    }
    if ($null -eq $Caught) {
        throw "$Label did not fail closed."
    }
    if ($Caught.Exception.Message -notmatch $MessagePattern) {
        throw "$Label failed for an unexpected reason: $($Caught.Exception.Message)"
    }
}

try {
    New-Item -ItemType Directory -Path $TemporaryRoot | Out-Null
    $DeskPath = Join-Path $TemporaryRoot 'p3_desk'
    New-Item -ItemType Directory -Path $DeskPath | Out-Null
    Copy-Item -LiteralPath (Join-Path $FrozenBriefPath 'BRIEF-v1.md') -Destination $DeskPath
    Get-ChildItem -LiteralPath (Join-Path $FrozenBriefPath 'engineering\corpus') -File | Copy-Item -Destination $DeskPath

    & $ConfigureScript -DeskPath $DeskPath

    $NodeCommand = Get-Command node -CommandType Application -ErrorAction Stop | Select-Object -First 1
    $NodePath = Convert-TestTomlPath $NodeCommand.Source
    $ServerToml = Convert-TestTomlPath $ServerPath
    $DeskToml = Convert-TestTomlPath $DeskPath
    $ExpectedEnabled = @"
$ManagedMarker

[mcp_servers.p3_evidence]
command = "$NodePath"
args = ["$ServerToml", "$DeskToml"]
cwd = "$DeskToml"
enabled = true
required = true
enabled_tools = ["list_evidence_files", "read_evidence_file"]
default_tools_approval_mode = "prompt"
startup_timeout_sec = 10
tool_timeout_sec = 15
"@
    $ExpectedEnabled = $ExpectedEnabled.TrimEnd() + [Environment]::NewLine
    $ConfigPath = Join-Path $DeskPath '.codex\config.toml'
    $ActualEnabled = [System.IO.File]::ReadAllText($ConfigPath)
    Assert-Equal -Actual $ActualEnabled -Expected $ExpectedEnabled -Label 'Enabled TOML'

    $UnrelatedDesk = Join-Path $TemporaryRoot 'unrelated_desk'
    $UnrelatedCodex = Join-Path $UnrelatedDesk '.codex'
    New-Item -ItemType Directory -Path $UnrelatedCodex -Force | Out-Null
    $UnrelatedConfig = Join-Path $UnrelatedCodex 'config.toml'
    $UnrelatedContent = "unrelated = true" + [Environment]::NewLine
    Write-TestFile -LiteralPath $UnrelatedConfig -Content $UnrelatedContent
    Assert-Throws -Action {
        & $ConfigureScript -DeskPath $UnrelatedDesk
    } -MessagePattern 'Refusing to overwrite unrelated|unexpected' -Label 'Unrelated config refusal'
    Assert-Equal -Actual ([System.IO.File]::ReadAllText($UnrelatedConfig)) -Expected $UnrelatedContent -Label 'Unrelated config preservation'

    $MalformedDesk = Join-Path $TemporaryRoot 'malformed_desk'
    $MalformedCodex = Join-Path $MalformedDesk '.codex'
    New-Item -ItemType Directory -Path $MalformedCodex -Force | Out-Null
    $MalformedConfig = Join-Path $MalformedCodex 'config.toml'
    $MalformedContent = $ManagedMarker + [Environment]::NewLine + 'enabled = true' + [Environment]::NewLine
    Write-TestFile -LiteralPath $MalformedConfig -Content $MalformedContent

    $DisableOnlyScript = Join-Path $TemporaryRoot 'configure-disable-only.ps1'
    Copy-Item -LiteralPath $ConfigureScript -Destination $DisableOnlyScript
    $env:PATH = ''
    Assert-Throws -Action {
        & $DisableOnlyScript -DeskPath $MalformedDesk -Disable
    } -MessagePattern 'unexpected shape|unexpected content' -Label 'Malformed managed config refusal'
    Assert-Equal -Actual ([System.IO.File]::ReadAllText($MalformedConfig)) -Expected $MalformedContent -Label 'Malformed config preservation'

    & $DisableOnlyScript -DeskPath $DeskPath -Disable
    $ExpectedDisabled = $ExpectedEnabled.Replace('enabled = true', 'enabled = false')
    $ActualDisabled = [System.IO.File]::ReadAllText($ConfigPath)
    Assert-Equal -Actual $ActualDisabled -Expected $ExpectedDisabled -Label 'Node-free disable'

    Write-Host 'P3 MCP configure smoke passed: exact enable, closed refusal, and dependency-free disable.'
} finally {
    $env:PATH = $OriginalPath
    if (Test-Path -LiteralPath $TemporaryRoot) {
        Remove-Item -LiteralPath $TemporaryRoot -Recurse -Force
    }
}
