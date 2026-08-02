#Requires -Version 5.1

[CmdletBinding()]
param(
    [string]$DeskPath = (Join-Path $env:USERPROFILE 'Documents\HarnessBootcamp\p3_desk'),
    [switch]$Disable
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ManagedMarker = '# Managed by AI Harness Bootcamp P3 MCP evidence installer v1.'
$ServerName = 'p3_evidence'

function Convert-ToTomlPath {
    param([Parameter(Mandatory = $true)][string]$Path)

    return ([System.IO.Path]::GetFullPath($Path)).Replace('\', '/').Replace('"', '\"')
}

function Test-ReparsePoint {
    param([Parameter(Mandatory = $true)][string]$LiteralPath)

    if (-not (Test-Path -LiteralPath $LiteralPath)) {
        return $false
    }
    $Item = Get-Item -LiteralPath $LiteralPath -Force
    return (($Item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0)
}

function Assert-ManagedConfigShape {
    param(
        [Parameter(Mandatory = $true)][string]$ConfigPath,
        [Parameter(Mandatory = $true)][string]$Content
    )

    $Normalized = $Content.Replace("`r`n", "`n")
    if ($Normalized.Contains("`r")) {
        throw "Refusing to rewrite managed config with unexpected line endings: $ConfigPath"
    }
    if ($Normalized.EndsWith("`n")) {
        $Normalized = $Normalized.Substring(0, $Normalized.Length - 1)
    }
    $Lines = @($Normalized -split "`n")
    $EscapedMarker = [regex]::Escape($ManagedMarker)
    $EscapedServerName = [regex]::Escape($ServerName)
    $ExpectedPatterns = @(
        "^$EscapedMarker$",
        '^$',
        "^\[mcp_servers\.$EscapedServerName\]$",
        '^command = "[^"\r\n]+"$',
        '^args = \["[^"\r\n]+", "[^"\r\n]+"\]$',
        '^cwd = "[^"\r\n]+"$',
        '^enabled = (true|false)$',
        '^required = true$',
        '^enabled_tools = \["list_evidence_files", "read_evidence_file"\]$',
        '^default_tools_approval_mode = "prompt"$',
        '^startup_timeout_sec = 10$',
        '^tool_timeout_sec = 15$'
    )

    if ($Lines.Count -ne $ExpectedPatterns.Count) {
        throw "Refusing to rewrite managed config with unexpected shape: $ConfigPath"
    }
    for ($Index = 0; $Index -lt $ExpectedPatterns.Count; $Index++) {
        if ($Lines[$Index] -notmatch $ExpectedPatterns[$Index]) {
            throw "Refusing to rewrite managed config with unexpected content on line $($Index + 1): $ConfigPath"
        }
    }
}

function Write-Utf8NoBom {
    param(
        [Parameter(Mandatory = $true)][string]$LiteralPath,
        [Parameter(Mandatory = $true)][string]$Content
    )

    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($LiteralPath, $Content, $Utf8NoBom)
}

function New-ManagedConfig {
    param(
        [Parameter(Mandatory = $true)][string]$NodePath,
        [Parameter(Mandatory = $true)][string]$ServerPath,
        [Parameter(Mandatory = $true)][string]$ResolvedDeskPath,
        [Parameter(Mandatory = $true)][bool]$Enabled
    )

    $EnabledValue = if ($Enabled) { 'true' } else { 'false' }
    $NodeToml = Convert-ToTomlPath $NodePath
    $ServerToml = Convert-ToTomlPath $ServerPath
    $DeskToml = Convert-ToTomlPath $ResolvedDeskPath

    return @"
$ManagedMarker

[mcp_servers.$ServerName]
command = "$NodeToml"
args = ["$ServerToml", "$DeskToml"]
cwd = "$DeskToml"
enabled = $EnabledValue
required = true
enabled_tools = ["list_evidence_files", "read_evidence_file"]
default_tools_approval_mode = "prompt"
startup_timeout_sec = 10
tool_timeout_sec = 15
"@
}

$ResolvedDeskPath = [System.IO.Path]::GetFullPath($DeskPath)
$CodexDirectory = Join-Path $ResolvedDeskPath '.codex'
$ConfigPath = Join-Path $CodexDirectory 'config.toml'

if ($Disable) {
    if (-not (Test-Path -LiteralPath $ConfigPath -PathType Leaf)) {
        throw "No managed P3 MCP config exists at $ConfigPath"
    }
    if ((Test-ReparsePoint $CodexDirectory) -or (Test-ReparsePoint $ConfigPath)) {
        throw "Refusing to rewrite a config reached through a symbolic link: $ConfigPath"
    }

    $ExistingContent = [System.IO.File]::ReadAllText($ConfigPath)
    Assert-ManagedConfigShape -ConfigPath $ConfigPath -Content $ExistingContent
    $EnabledMatches = [regex]::Matches($ExistingContent, '(?m)^enabled = (?:true|false)(?=\r?$)')
    if ($EnabledMatches.Count -ne 1) {
        throw "Refusing to rewrite config without exactly one managed enabled line: $ConfigPath"
    }
    $DisabledContent = [regex]::Replace($ExistingContent, '(?m)^enabled = (?:true|false)(?=\r?$)', 'enabled = false')
    Write-Utf8NoBom -LiteralPath $ConfigPath -Content $DisabledContent
    Write-Host "Disabled the managed $ServerName MCP server in $ConfigPath"
    return
}

if (-not (Test-Path -LiteralPath $ResolvedDeskPath -PathType Container)) {
    throw "P3 desk folder not found: $ResolvedDeskPath"
}
if (Test-ReparsePoint $ResolvedDeskPath) {
    throw "P3 desk folder cannot be a symbolic link: $ResolvedDeskPath"
}

if (Test-Path -LiteralPath $ConfigPath) {
    if (-not (Test-Path -LiteralPath $ConfigPath -PathType Leaf)) {
        throw "Codex config path is not a regular file: $ConfigPath"
    }
    if ((Test-ReparsePoint $CodexDirectory) -or (Test-ReparsePoint $ConfigPath)) {
        throw "Refusing to overwrite a config reached through a symbolic link: $ConfigPath"
    }
    $ExistingContent = [System.IO.File]::ReadAllText($ConfigPath)
    Assert-ManagedConfigShape -ConfigPath $ConfigPath -Content $ExistingContent
}

$ServerPath = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'server.mjs'))
if (-not (Test-Path -LiteralPath $ServerPath -PathType Leaf)) {
    throw "Course MCP server not found: $ServerPath"
}
if (Test-ReparsePoint $ServerPath) {
    throw "Course MCP server cannot be a symbolic link: $ServerPath"
}

$NodeCommand = Get-Command node -CommandType Application -ErrorAction Stop | Select-Object -First 1
$NodePath = [System.IO.Path]::GetFullPath($NodeCommand.Source)
$ServerPackage = Join-Path $PSScriptRoot 'node_modules\@modelcontextprotocol\server\package.json'
$ZodPackage = Join-Path $PSScriptRoot 'node_modules\zod\package.json'
if (-not (Test-Path -LiteralPath $ServerPackage -PathType Leaf) -or -not (Test-Path -LiteralPath $ZodPackage -PathType Leaf)) {
    throw "MCP dependencies are not installed. Run npm ci in $PSScriptRoot, then run this command again."
}

& $NodePath $ServerPath $ResolvedDeskPath '--validate-only'
if ($LASTEXITCODE -ne 0) {
    throw "P3 evidence validation failed with exit code $LASTEXITCODE. The Codex config was not changed."
}

if (-not (Test-Path -LiteralPath $CodexDirectory)) {
    New-Item -ItemType Directory -Path $CodexDirectory | Out-Null
}
if (Test-ReparsePoint $CodexDirectory) {
    throw "Codex config directory cannot be a symbolic link: $CodexDirectory"
}
$ConfigContent = New-ManagedConfig -NodePath $NodePath -ServerPath $ServerPath -ResolvedDeskPath $ResolvedDeskPath -Enabled $true
Write-Utf8NoBom -LiteralPath $ConfigPath -Content ($ConfigContent.TrimEnd() + [Environment]::NewLine)

Write-Host "Configured the managed $ServerName MCP server in $ConfigPath"
Write-Host 'Restart Codex, open this trusted P3 project, and use /mcp to confirm the server and its two tools.'
