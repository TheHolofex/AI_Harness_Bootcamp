#Requires -Version 5.1

[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Reference = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$Kit = [System.IO.Path]::GetFullPath((Join-Path $Reference '..'))
$Starter = Join-Path $Kit 'starter'
$Temporary = Join-Path ([System.IO.Path]::GetTempPath()) ('p2-project-organizer-config-' + [guid]::NewGuid().ToString('N'))
$Project = Join-Path $Temporary 'P2_Project_Organizer'

function Resolve-PythonForSmoke {
    $Python = Get-Command python -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($null -ne $Python) {
        return @($Python.Source)
    }
    $Py = Get-Command py -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($null -ne $Py) {
        return @($Py.Source, '-3')
    }
    throw 'Python 3 is required for the P2 configuration smoke test.'
}

function Invoke-PythonForSmoke {
    param([Parameter(Mandatory = $true)][string[]]$Arguments)
    $Launcher = @(Resolve-PythonForSmoke)
    $Command = $Launcher[0]
    $Prefix = @()
    if ($Launcher.Count -gt 1) {
        $Prefix = $Launcher[1..($Launcher.Count - 1)]
    }
    & $Command @Prefix @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Python command failed with exit code $LASTEXITCODE."
    }
}

New-Item -ItemType Directory -Path $Project -Force | Out-Null
try {
    Get-ChildItem -LiteralPath $Starter -Force | Copy-Item -Destination $Project -Recurse -Force
    foreach ($File in @('schema.sql', 'build_project_ledger.py', 'verify_project_ledger.py', 'configure_project_organizer.ps1')) {
        Copy-Item -LiteralPath (Join-Path $Reference $File) -Destination (Join-Path $Project $File) -Force
    }
    $PluginDestination = Join-Path $Project 'plugins\project-organizer'
    New-Item -ItemType Directory -Path (Split-Path $PluginDestination -Parent) -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $Reference 'plugins\project-organizer') -Destination $PluginDestination -Recurse -Force
    $CopiedNodeModules = Join-Path $PluginDestination 'node_modules'
    if (Test-Path -LiteralPath $CopiedNodeModules) {
        Remove-Item -LiteralPath $CopiedNodeModules -Recurse -Force
    }
    New-Item -ItemType Directory -Path (Join-Path $Project '.codex\agents') -Force | Out-Null
    Get-ChildItem -LiteralPath (Join-Path $Reference '.codex\agents') -File | Copy-Item -Destination (Join-Path $Project '.codex\agents') -Force
    Copy-Item -LiteralPath (Join-Path $Reference '.agents\plugins\marketplace.json') -Destination (Join-Path $Project '.agents\plugins\marketplace.json') -Force

    Invoke-PythonForSmoke -Arguments @((Join-Path $Project 'build_project_ledger.py'), '--project-root', $Project)

    $Npm = (Get-Command npm -CommandType Application -ErrorAction Stop | Select-Object -First 1).Source
    & $Npm ci --prefix $PluginDestination --ignore-scripts --no-audit --no-fund
    if ($LASTEXITCODE -ne 0) {
        throw "npm ci failed with exit code $LASTEXITCODE."
    }

    $Config = Join-Path $Project '.codex\config.toml'
    [System.IO.File]::AppendAllText(
        $Config,
        "`r`n[mcp_servers.unrelated]`r`ncommand = `"C:/tools/unrelated.exe`"`r`nenabled = false`r`n",
        (New-Object System.Text.UTF8Encoding($false))
    )
    $Before = [System.IO.File]::ReadAllText($Config)
    & (Join-Path $Project 'configure_project_organizer.ps1') -ProjectRoot $Project
    $FirstHash = (Get-FileHash -LiteralPath $Config -Algorithm SHA256).Hash
    & (Join-Path $Project 'configure_project_organizer.ps1') -ProjectRoot $Project
    $SecondHash = (Get-FileHash -LiteralPath $Config -Algorithm SHA256).Hash
    if ($FirstHash -ne $SecondHash) {
        throw 'Second configuration run changed config.toml; the bounded edit is not idempotent.'
    }

    $After = [System.IO.File]::ReadAllText($Config)
    foreach ($Preserved in @(
        'model = "gpt-5.6-terra"',
        'default_subagent_model = "gpt-5.6-terra"',
        '[mcp_servers.unrelated]',
        'command = "C:/tools/unrelated.exe"'
    )) {
        if (-not $After.Contains($Preserved)) {
            throw "Configuration lost unrelated or Terra setting: $Preserved"
        }
    }
    if (-not $Before.Contains('[mcp_servers.unrelated]')) {
        throw 'Smoke fixture did not contain the unrelated MCP server.'
    }
    foreach ($Pattern in @(
        '# >>> AI Harness Bootcamp P2 Project Organizer MCP >>>',
        '# <<< AI Harness Bootcamp P2 Project Organizer MCP <<<',
        '[mcp_servers.project_organizer]'
    )) {
        if ([regex]::Matches($After, [regex]::Escape($Pattern)).Count -ne 1) {
            throw "Expected exactly one managed configuration marker/table: $Pattern"
        }
    }
    foreach ($Tool in @('get_project_snapshot', 'get_ready_work', 'get_dependency_path', 'get_decision_queue')) {
        if (-not $After.Contains($Tool)) {
            throw "Configured MCP allowlist is missing $Tool."
        }
    }
    if ($After.Contains('.mcp.json')) {
        throw 'Configuration unexpectedly depends on .mcp.json.'
    }
    Write-Host 'PASS P2 Project Organizer Windows config: verified MCP, bounded idempotent merge, unrelated settings preserved'
} finally {
    if (Test-Path -LiteralPath $Temporary) {
        Remove-Item -LiteralPath $Temporary -Recurse -Force
    }
}
