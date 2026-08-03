#Requires -Version 5.1

[CmdletBinding()]
param(
    [string]$ProjectRoot = (Get-Location).Path
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ManagedStart = '# >>> AI Harness Bootcamp P2 Project Organizer MCP >>>'
$ManagedEnd = '# <<< AI Harness Bootcamp P2 Project Organizer MCP <<<'
$ServerName = 'project_organizer'
$ToolNames = @(
    'get_project_snapshot',
    'get_ready_work',
    'get_dependency_path',
    'get_decision_queue'
)

function Convert-ToTomlPath {
    param([Parameter(Mandatory = $true)][string]$Path)
    return ([System.IO.Path]::GetFullPath($Path)).Replace('\', '/').Replace('"', '\"')
}

function Write-Utf8NoBom {
    param(
        [Parameter(Mandatory = $true)][string]$LiteralPath,
        [Parameter(Mandatory = $true)][string]$Content
    )
    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($LiteralPath, $Content, $Utf8NoBom)
}

function Test-ReparsePoint {
    param([Parameter(Mandatory = $true)][string]$LiteralPath)
    if (-not (Test-Path -LiteralPath $LiteralPath)) {
        return $false
    }
    $Item = Get-Item -LiteralPath $LiteralPath -Force
    return (($Item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0)
}

function Resolve-PythonInterpreter {
    $PythonCommand = Get-Command python -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($null -ne $PythonCommand) {
        $Resolved = & $PythonCommand.Source -c 'import os, sys; print(os.path.abspath(sys.executable))'
        if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($Resolved)) {
            return [System.IO.Path]::GetFullPath(($Resolved | Select-Object -Last 1).Trim())
        }
    }
    $PyCommand = Get-Command py -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($null -ne $PyCommand) {
        $Resolved = & $PyCommand.Source -3 -c 'import os, sys; print(os.path.abspath(sys.executable))'
        if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($Resolved)) {
            return [System.IO.Path]::GetFullPath(($Resolved | Select-Object -Last 1).Trim())
        }
    }
    throw 'Python 3 was not found. Return to the install clinic and verify Python before configuring P2.'
}

function New-ManagedBlock {
    param(
        [Parameter(Mandatory = $true)][string]$NodePath,
        [Parameter(Mandatory = $true)][string]$PythonPath,
        [Parameter(Mandatory = $true)][string]$ServerPath,
        [Parameter(Mandatory = $true)][string]$ResolvedProjectRoot
    )
    $NodeToml = Convert-ToTomlPath $NodePath
    $PythonToml = Convert-ToTomlPath $PythonPath
    $ServerToml = Convert-ToTomlPath $ServerPath
    $RootToml = Convert-ToTomlPath $ResolvedProjectRoot
    return @"
$ManagedStart
[mcp_servers.$ServerName]
command = "$NodeToml"
args = ["$ServerToml", "$RootToml"]
cwd = "$RootToml"
env = { PROJECT_ORGANIZER_PYTHON = "$PythonToml" }
enabled = true
required = true
enabled_tools = ["$($ToolNames -join '", "')"]
default_tools_approval_mode = "approve"
startup_timeout_sec = 10
tool_timeout_sec = 15
$ManagedEnd
"@
}

function Merge-ManagedBlock {
    param(
        [Parameter(Mandatory = $true)][string]$ExistingContent,
        [Parameter(Mandatory = $true)][string]$ManagedBlock
    )
    $NewLine = if ($ExistingContent.Contains("`r`n")) { "`r`n" } else { "`n" }
    $NormalizedBlock = $ManagedBlock.TrimEnd().Replace("`r`n", "`n").Replace("`n", $NewLine)
    $StartPattern = [regex]::Escape($ManagedStart)
    $EndPattern = [regex]::Escape($ManagedEnd)
    $BlockPattern = "(?ms)^$StartPattern\r?\n.*?^$EndPattern(?:\r?\n)?"
    $Matches = [regex]::Matches($ExistingContent, $BlockPattern)
    if ($Matches.Count -gt 1) {
        throw "Refusing to edit config with multiple managed Project Organizer blocks."
    }
    $WithoutManagedBlock = [regex]::Replace($ExistingContent, $BlockPattern, '')
    $ServerPattern = "(?m)^\s*\[mcp_servers\." + [regex]::Escape($ServerName) + "\]\s*$"
    if ([regex]::IsMatch($WithoutManagedBlock, $ServerPattern)) {
        throw "Refusing to overwrite an unmanaged [mcp_servers.$ServerName] table."
    }
    if ($Matches.Count -eq 1) {
        return [regex]::Replace($ExistingContent, $BlockPattern, $NormalizedBlock + $NewLine, 1)
    }
    if ([string]::IsNullOrEmpty($ExistingContent)) {
        return $NormalizedBlock + $NewLine
    }
    $Separator = if ($ExistingContent.EndsWith($NewLine + $NewLine)) {
        ''
    } elseif ($ExistingContent.EndsWith($NewLine)) {
        $NewLine
    } else {
        $NewLine + $NewLine
    }
    return $ExistingContent + $Separator + $NormalizedBlock + $NewLine
}

$ResolvedRoot = [System.IO.Path]::GetFullPath($ProjectRoot)
if (-not (Test-Path -LiteralPath $ResolvedRoot -PathType Container)) {
    throw "Project folder not found: $ResolvedRoot"
}
if (Test-ReparsePoint $ResolvedRoot) {
    throw "Project folder cannot be a symbolic link: $ResolvedRoot"
}

$ConfigDirectory = Join-Path $ResolvedRoot '.codex'
$ConfigPath = Join-Path $ConfigDirectory 'config.toml'
$ServerPath = Join-Path $ResolvedRoot 'plugins\project-organizer\mcp\server.mjs'
$LedgerPath = Join-Path $ResolvedRoot 'project_ledger.sqlite3'
$ServerPackage = Join-Path $ResolvedRoot 'plugins\project-organizer\node_modules\@modelcontextprotocol\server\package.json'
$ZodPackage = Join-Path $ResolvedRoot 'plugins\project-organizer\node_modules\zod\package.json'

foreach ($RequiredFile in @($ConfigPath, $ServerPath, $LedgerPath, $ServerPackage, $ZodPackage)) {
    if (-not (Test-Path -LiteralPath $RequiredFile -PathType Leaf)) {
        throw "Required P2 file is missing: $RequiredFile"
    }
    if (Test-ReparsePoint $RequiredFile) {
        throw "Required P2 file cannot be a symbolic link: $RequiredFile"
    }
}

$ExistingConfig = [System.IO.File]::ReadAllText($ConfigPath)

$NodeCommand = Get-Command node -CommandType Application -ErrorAction Stop | Select-Object -First 1
$NodePath = [System.IO.Path]::GetFullPath($NodeCommand.Source)
$PythonPath = Resolve-PythonInterpreter

$PreviousPython = $env:PROJECT_ORGANIZER_PYTHON
try {
    $env:PROJECT_ORGANIZER_PYTHON = $PythonPath
    & $NodePath $ServerPath $ResolvedRoot '--validate-only'
    if ($LASTEXITCODE -ne 0) {
        throw "Project Organizer MCP validation failed with exit code $LASTEXITCODE. Codex config was not changed."
    }
} finally {
    if ($null -eq $PreviousPython) {
        Remove-Item Env:PROJECT_ORGANIZER_PYTHON -ErrorAction SilentlyContinue
    } else {
        $env:PROJECT_ORGANIZER_PYTHON = $PreviousPython
    }
}

$ManagedBlock = New-ManagedBlock -NodePath $NodePath -PythonPath $PythonPath -ServerPath $ServerPath -ResolvedProjectRoot $ResolvedRoot
$UpdatedConfig = Merge-ManagedBlock -ExistingContent $ExistingConfig -ManagedBlock $ManagedBlock
Write-Utf8NoBom -LiteralPath $ConfigPath -Content $UpdatedConfig

Write-Host "Configured the read-only $ServerName MCP server in $ConfigPath"
Write-Host 'Restart Codex in this project, then use /mcp to confirm exactly four read-only tools.'
