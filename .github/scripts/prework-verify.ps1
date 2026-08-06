<#
.SYNOPSIS
  Windows x64 install/start smoke for AI Harness Bootcamp pre-work.

.DESCRIPTION
  Run on a real Windows 11 x64 machine (candidate staff build or clinic laptop).
  Does NOT require API keys. Does NOT install missing tools (reports absence).
  Writes prework-verify-results.md beside this script unless -ResultsPath is set.

  Exit codes:
    0 = all hard checks passed (soft warnings allowed)
    1 = one or more hard failures
    2 = not Windows / could not write results

.PARAMETER ResultsPath
  Optional full path for the markdown results file.

.PARAMETER SkipOpenCodeDisableRoundTrip
  Skip setting/reading OPENCODE_DISABLE_CLAUDE_CODE (use on locked-down images).
#>
[CmdletBinding()]
param(
    [string]$ResultsPath = "",
    [switch]$SkipOpenCodeDisableRoundTrip
)

$ErrorActionPreference = "Continue"
$script:HardFails = New-Object System.Collections.Generic.List[string]
$script:SoftFails = New-Object System.Collections.Generic.List[string]
$script:Passes = New-Object System.Collections.Generic.List[string]
$script:Lines = New-Object System.Collections.Generic.List[string]

function Write-Result {
    param(
        [string]$Name,
        [bool]$Ok,
        [string]$Detail,
        [bool]$Hard = $true
    )
    $mark = if ($Ok) { "PASS" } elseif ($Hard) { "FAIL" } else { "WARN" }
    $line = "[$mark] ${Name}: $Detail"
    Write-Host $line
    [void]$script:Lines.Add($line)
    if ($Ok) {
        [void]$script:Passes.Add($Name)
    } elseif ($Hard) {
        [void]$script:HardFails.Add("$Name - $Detail")
    } else {
        [void]$script:SoftFails.Add("$Name - $Detail")
    }
}

function Test-CommandVersion {
    param(
        [string]$Name,
        [string]$Exe,
        [string[]]$VersionArgs = @("--version"),
        [bool]$Hard = $true,
        [scriptblock]$Validator = $null
    )
    $cmd = Get-Command $Exe -ErrorAction SilentlyContinue
    if (-not $cmd) {
        Write-Result -Name "bin.$Name" -Ok $false -Detail "$Exe not on PATH" -Hard $Hard
        return $null
    }
    try {
        $out = & $Exe @VersionArgs 2>&1 | Out-String
        $commandExit = $LASTEXITCODE
        $out = $out.Trim()
        $snippet = if ($out.Length -gt 120) { $out.Substring(0, 120) + "..." } else { $out }
        if ($commandExit -ne 0) {
            Write-Result -Name "bin.$Name" -Ok $false -Detail "exited $commandExit - $snippet" -Hard $Hard
            return $out
        }
        if ([string]::IsNullOrWhiteSpace($out)) {
            Write-Result -Name "bin.$Name" -Ok $false -Detail "returned no version text" -Hard $Hard
            return $out
        }
        if ($Validator) {
            $ok = & $Validator $out
            if (-not $ok) {
                Write-Result -Name "bin.$Name" -Ok $false -Detail "present but unexpected output: $($out.Substring(0, [Math]::Min(160, $out.Length)))" -Hard $Hard
                return $out
            }
        }
        Write-Result -Name "bin.$Name" -Ok $true -Detail "$($cmd.Source) - $snippet" -Hard $Hard
        return $out
    } catch {
        Write-Result -Name "bin.$Name" -Ok $false -Detail $_.Exception.Message -Hard $Hard
        return $null
    }
}

# --- gate: Windows ---
if ($env:OS -ne "Windows_NT") {
    Write-Host "This smoke is for Windows x64. Current OS=$($env:OS). Use verify-stack-facts.py on this machine."
    exit 2
}

$arch = $env:PROCESSOR_ARCHITECTURE
if ($arch -and $arch -match "ARM") {
    Write-Result -Name "os.arch" -Ok $false -Detail "ARM64 ($arch) - course requires x64; OpenCode/goose path is RED" -Hard $true
} else {
    Write-Result -Name "os.arch" -Ok $true -Detail ($arch, "unknown" | Where-Object { $_ } | Select-Object -First 1) -Hard $true
}

Write-Result -Name "os.ps_version" -Ok $true -Detail ("PS " + $PSVersionTable.PSVersion.ToString()) -Hard $false

# --- Git Bash path (install-clinic contract) ---
$bash = @(
    "C:\Program Files\Git\bin\bash.exe",
    (Join-Path $env:LOCALAPPDATA "Programs\Git\bin\bash.exe")
) | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if ($bash) {
    Write-Result -Name "git.bash_path" -Ok $true -Detail $bash -Hard $true
} else {
    $alt = Get-Command "bash.exe" -ErrorAction SilentlyContinue
    if ($alt) {
        Write-Result -Name "git.bash_path" -Ok $true -Detail "nonstandard path: $($alt.Source) - use this path for the Goose installer fallback" -Hard $true
    } else {
        Write-Result -Name "git.bash_path" -Ok $false -Detail "Git Bash not at either guide path and bash.exe not on PATH" -Hard $true
    }
}

Test-CommandVersion -Name "git" -Exe "git" -VersionArgs @("--version") -Hard $true | Out-Null

# --- Node and npm command surface ---
# Learners install the current Node LTS. The course commands below are the
# compatibility proof, so this diagnostic records the observed versions without
# freezing an otherwise working LTS release to a numeric range.
Test-CommandVersion -Name "node" -Exe "node" -VersionArgs @("-v") -Hard $true | Out-Null
Test-CommandVersion -Name "npm" -Exe "npm" -VersionArgs @("--version") -Hard $true | Out-Null

# --- Python not WindowsApps stub ---
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) {
    Write-Result -Name "bin.python" -Ok $false -Detail "python not on PATH" -Hard $true
} else {
    $src = $py.Source
    if ($src -match "WindowsApps") {
        Write-Result -Name "bin.python" -Ok $false -Detail "WindowsApps stub: $src - install real Python" -Hard $true
    } else {
        try {
            $pv = & python --version 2>&1 | Out-String
            $pythonVersion = $pv.Trim()
            $pythonOk = ($LASTEXITCODE -eq 0 -and $pythonVersion -match '^Python\s+3(?:\.|$)')
            Write-Result -Name "bin.python" -Ok $pythonOk -Detail "$src - $pythonVersion (want Python 3)" -Hard $true
        } catch {
            Write-Result -Name "bin.python" -Ok $false -Detail $_.Exception.Message -Hard $true
        }
    }
}

# --- Microsoft Visual C++ x64 runtime (goose prerequisite) ---
$vcRuntimePaths = @(
    "HKLM:\SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64",
    "HKLM:\SOFTWARE\WOW6432Node\Microsoft\VisualStudio\14.0\VC\Runtimes\x64"
)
$vcRuntime = $null
$vcRuntimePath = $null
foreach ($path in $vcRuntimePaths) {
    $candidate = Get-ItemProperty -LiteralPath $path -ErrorAction SilentlyContinue
    if ($candidate -and [int]$candidate.Installed -eq 1) {
        $vcRuntime = $candidate
        $vcRuntimePath = $path
        break
    }
}
if ($vcRuntime) {
    Write-Result -Name "runtime.vcredist_x64" -Ok $true -Detail "$($vcRuntime.Version) at $vcRuntimePath" -Hard $true
} else {
    Write-Result -Name "runtime.vcredist_x64" -Ok $false -Detail "Microsoft Visual C++ v14 x64 runtime not registered; install or repair https://aka.ms/vc14/vc_redist.x64.exe before starting goose" -Hard $true
}

# --- OpenCode ---
$script:OpenCodePin = "1.18.11"
$oc = Test-CommandVersion -Name "opencode" -Exe "opencode" -VersionArgs @("--version") -Hard $true -Validator {
    param($output)
    $output.Trim() -eq $script:OpenCodePin
}

# --- Goose (required for a complete setup) ---
$gooseOk = $false
foreach ($g in @("goose", "goose.exe")) {
    $c = Get-Command $g -CommandType Application -ErrorAction SilentlyContinue
    if ($c) {
        # Avoid confusing with unrelated winget "goose" DB tool - version string heuristic
        try {
            $gout = & $c.Source "--version" 2>&1 | Out-String
            $gexit = $LASTEXITCODE
            $gout = $gout.Trim()
            if ($gexit -ne 0) {
                $detail = "exited $gexit"
                if ($gexit -eq -1073741515 -or $gexit -eq 3221225781) {
                    $detail += " (0xC0000135: a required DLL was not found; for this Goose build, first install or repair the Microsoft Visual C++ v14 x64 runtime)"
                }
                if ($gout) { $detail += ": $gout" }
                Write-Result -Name "bin.goose" -Ok $false -Detail "$($c.Source) - $detail" -Hard $true
            } elseif (-not $gout) {
                Write-Result -Name "bin.goose" -Ok $false -Detail "$($c.Source) returned no version text" -Hard $true
            } elseif ($gout -match "(?i)database|clickhouse|ibis") {
                Write-Result -Name "bin.goose" -Ok $false -Detail "looks like the unrelated database tool named goose: $gout" -Hard $true
            } else {
                Write-Result -Name "bin.goose" -Ok $true -Detail "$($c.Source) - $gout" -Hard $true
                $gooseOk = $true
            }
        } catch {
            Write-Result -Name "bin.goose" -Ok $false -Detail $_.Exception.Message -Hard $true
        }
        break
    }
}
if (-not $gooseOk -and -not ($script:Lines | Where-Object { $_ -match "bin\.goose" })) {
    Write-Result -Name "bin.goose" -Ok $false -Detail "goose not on PATH (use the AAIF installer in the website checklist)" -Hard $true
}

# The supported P6 prepare path validates the source recipe and confirms that
# Goose exposes the native Developer capability. It never calls a model. Use a
# disposable run root so this diagnostic leaves the course fixture unchanged.
$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot "..\.."))
$p6Root = Join-Path $repoRoot "mission_flesh\p6"
$p6Start = Join-Path $p6Root "scripts\Start-P6.ps1"
$p6TempRun = Join-Path ([IO.Path]::GetTempPath()) ("ahb-p6-prework-" + [Guid]::NewGuid().ToString("N"))
try {
    if (-not (Test-Path -LiteralPath $p6Start)) {
        Write-Result -Name "p6.prepare_only" -Ok $false -Detail "missing $p6Start" -Hard $true
    } else {
        $prepareOutput = & powershell -NoProfile -ExecutionPolicy Bypass -File $p6Start -PrepareOnly -RunRoot $p6TempRun 2>&1 | Out-String
        $prepareExit = $LASTEXITCODE
        $prepareOk = (
            $prepareExit -eq 0 -and
            $prepareOutput -match "P6 PREP PASS wave=1 evidence=14 run=" -and
            $prepareOutput -match "P6 PREPARE-ONLY PASS run=.* no model call started"
        )
        $prepareDetail = if ($prepareOk) {
            ($prepareOutput.Trim() -split '\r?\n' | Select-Object -Last 1)
        } else {
            "exit=$prepareExit output=$($prepareOutput.Trim())"
        }
        Write-Result -Name "p6.prepare_only" -Ok $prepareOk -Detail $prepareDetail -Hard $true
    }

} catch {
    Write-Result -Name "p6.prepare_exception" -Ok $false -Detail $_.Exception.Message -Hard $true
} finally {
    if (Test-Path -LiteralPath $p6TempRun) {
        Remove-Item -LiteralPath $p6TempRun -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# --- OPENCODE_DISABLE_CLAUDE_CODE round-trip ---
if (-not $SkipOpenCodeDisableRoundTrip) {
    $varName = "OPENCODE_DISABLE_CLAUDE_CODE"
    $priorUser = [Environment]::GetEnvironmentVariable($varName, "User")
    $priorProcess = [Environment]::GetEnvironmentVariable($varName, "Process")
    try {
        [Environment]::SetEnvironmentVariable($varName, "1", "User")
        $env:OPENCODE_DISABLE_CLAUDE_CODE = "1"
        # Re-read User hive (same process should see it via GetEnvironmentVariable)
        $readBack = [Environment]::GetEnvironmentVariable($varName, "User")
        $session = $env:OPENCODE_DISABLE_CLAUDE_CODE
        if ($readBack -eq "1" -and $session -eq "1") {
            Write-Result -Name "env.OPENCODE_DISABLE_CLAUDE_CODE" -Ok $true -Detail "User=1 and session=1" -Hard $true
        } else {
            Write-Result -Name "env.OPENCODE_DISABLE_CLAUDE_CODE" -Ok $false -Detail "User='$readBack' session='$session' (want 1/1)" -Hard $true
        }
    } catch {
        Write-Result -Name "env.OPENCODE_DISABLE_CLAUDE_CODE" -Ok $false -Detail $_.Exception.Message -Hard $true
    } finally {
        # This is a diagnostic round trip, so restore both scopes exactly.
        [Environment]::SetEnvironmentVariable($varName, $priorUser, "User")
        [Environment]::SetEnvironmentVariable($varName, $priorProcess, "Process")
    }
} else {
    Write-Result -Name "env.OPENCODE_DISABLE_CLAUDE_CODE" -Ok $true -Detail "skipped by switch" -Hard $false
}

# --- Codex config presence (soft - GUI still required) ---
$codexCfg = Join-Path $env:USERPROFILE ".codex\config.toml"
if (Test-Path -LiteralPath $codexCfg) {
    $raw = Get-Content -LiteralPath $codexCfg -Raw -ErrorAction SilentlyContinue
    $forced = $raw -match 'forced_login_method\s*=\s*"api"'
    Write-Result -Name "codex.config_api_lock" -Ok $forced -Detail $(if ($forced) { $codexCfg } else { "config exists but forced_login_method = api missing" }) -Hard $false
} else {
    Write-Result -Name "codex.config_api_lock" -Ok $false -Detail "no $codexCfg yet (GUI install still required)" -Hard $false
}

# --- Results file ---
if (-not $ResultsPath) {
    $ResultsPath = Join-Path $PSScriptRoot "prework-verify-results.md"
}

$exit = 0
if ($script:HardFails.Count -gt 0) { $exit = 1 }

$md = @()
$md += "# prework-verify results"
$md += ""
$md += "- When: $(Get-Date -Format o)"
$md += "- Host: $env:COMPUTERNAME"
$md += "- Arch: $arch"
$md += "- PS: $($PSVersionTable.PSVersion)"
$md += "- Exit: $exit"
$md += ""
$md += "## Checks"
$md += '```'
$md += ($script:Lines -join "`n")
$md += '```'
$md += ""
$md += "## Summary"
$md += "- Pass: $($script:Passes.Count)"
$md += "- Hard fail: $($script:HardFails.Count)"
$md += "- Warn: $($script:SoftFails.Count)"
$md += ""
if ($script:HardFails.Count -gt 0) {
    $md += "## Hard failures"
    foreach ($f in $script:HardFails) { $md += "- $f" }
    $md += ""
}
if ($script:SoftFails.Count -gt 0) {
    $md += "## Warnings"
    foreach ($f in $script:SoftFails) { $md += "- $f" }
    $md += ""
}
$md += "## Not covered (still need a person + keys)"
$md += "- Codex GUI sign-in and from-codex.txt write proof"
$md += "- Funded key write proofs (OpenCode/goose)"
$md += "- Funded P6 mission run (the no-key prepare and capability probes are covered)"
$md += "- xAI ACL end-to-end"
$md += "- Browser -> deck cold-smoke (lead/BROWSER_DECK_DEMO.md)"
$md += "- LOCAL PIN Ollama quality"
$md += ""
$md += "Pin sheet: lead/COHORT_PIN.md"
$md += ""

try {
    $dir = Split-Path -Parent $ResultsPath
    if ($dir -and -not (Test-Path -LiteralPath $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
    Set-Content -LiteralPath $ResultsPath -Value ($md -join "`n") -Encoding UTF8
    Write-Host ""
    Write-Host "Wrote $ResultsPath"
} catch {
    Write-Host "Could not write results: $($_.Exception.Message)"
    exit 2
}

Write-Host ""
Write-Host "summary: pass=$($script:Passes.Count) hard_fail=$($script:HardFails.Count) warn=$($script:SoftFails.Count) exit=$exit"
exit $exit
