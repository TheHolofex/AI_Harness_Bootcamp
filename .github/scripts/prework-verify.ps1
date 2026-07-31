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
        $out = $out.Trim()
        if ($Validator) {
            $ok = & $Validator $out
            if (-not $ok) {
                Write-Result -Name "bin.$Name" -Ok $false -Detail "present but unexpected output: $($out.Substring(0, [Math]::Min(160, $out.Length)))" -Hard $Hard
                return $out
            }
        }
        $snippet = if ($out.Length -gt 120) { $out.Substring(0, 120) + "..." } else { $out }
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

# --- Git Bash path (guide contract) ---
$bash = "C:\Program Files\Git\bin\bash.exe"
if (Test-Path -LiteralPath $bash) {
    Write-Result -Name "git.bash_path" -Ok $true -Detail $bash -Hard $true
} else {
    $alt = Get-Command "bash.exe" -ErrorAction SilentlyContinue
    if ($alt) {
        Write-Result -Name "git.bash_path" -Ok $false -Detail "guide path missing; found $($alt.Source) - Pi shellPath may need edit" -Hard $true
    } else {
        Write-Result -Name "git.bash_path" -Ok $false -Detail "Git Bash not at guide path and bash.exe not on PATH" -Hard $true
    }
}

Test-CommandVersion -Name "git" -Exe "git" -VersionArgs @("--version") -Hard $true | Out-Null

# --- Node LTS band ---
$nodeOut = Test-CommandVersion -Name "node" -Exe "node" -VersionArgs @("-v") -Hard $true
if ($nodeOut) {
    if ($nodeOut -match "v?(\d+)\.(\d+)") {
        $maj = [int]$Matches[1]
        $min = [int]$Matches[2]
        $inBand = ($maj -eq 22 -and $min -ge 22) -or ($maj -ge 23 -and $maj -le 24) -or ($maj -eq 24)
        # Course band: 22.22-24.x inclusive majors 22 (patch>=22) through 24
        $inBand = ($maj -eq 22 -and $min -ge 22) -or ($maj -eq 23) -or ($maj -eq 24)
        Write-Result -Name "node.lts_band" -Ok $inBand -Detail "parsed $nodeOut (want 22.22-24.x)" -Hard $true
    } else {
        Write-Result -Name "node.lts_band" -Ok $false -Detail "could not parse node -v: $nodeOut" -Hard $true
    }
}

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
            Write-Result -Name "bin.python" -Ok $true -Detail "$src - $($pv.Trim())" -Hard $true
        } catch {
            Write-Result -Name "bin.python" -Ok $false -Detail $_.Exception.Message -Hard $true
        }
    }
}

# --- OpenCode ---
$oc = Test-CommandVersion -Name "opencode" -Exe "opencode" -VersionArgs @("--version") -Hard $true

# --- Pi / goose (soft if missing on partial install; hard preferred on staff candidate) ---
Test-CommandVersion -Name "pi" -Exe "pi" -VersionArgs @("--version") -Hard $false | Out-Null
$gooseOk = $false
foreach ($g in @("goose", "goose.exe")) {
    $c = Get-Command $g -ErrorAction SilentlyContinue
    if ($c) {
        # Avoid confusing with unrelated winget "goose" DB tool - version string heuristic
        try {
            $gout = & $c.Source "--version" 2>&1 | Out-String
            $gout = $gout.Trim()
            if ($gout -match "(?i)database|clickhouse|ibis") {
                Write-Result -Name "bin.goose" -Ok $false -Detail "looks like wrong winget goose (database tool): $gout" -Hard $true
            } else {
                Write-Result -Name "bin.goose" -Ok $true -Detail "$($c.Source) - $gout" -Hard $false
                $gooseOk = $true
            }
        } catch {
            Write-Result -Name "bin.goose" -Ok $false -Detail $_.Exception.Message -Hard $false
        }
        break
    }
}
if (-not $gooseOk -and -not ($script:Lines | Where-Object { $_ -match "bin\.goose" })) {
    Write-Result -Name "bin.goose" -Ok $false -Detail "goose not on PATH (install aaif-goose path from guide)" -Hard $false
}

# --- OPENCODE_DISABLE_CLAUDE_CODE round-trip ---
if (-not $SkipOpenCodeDisableRoundTrip) {
    $varName = "OPENCODE_DISABLE_CLAUDE_CODE"
    $priorUser = [Environment]::GetEnvironmentVariable($varName, "User")
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
        # Restore prior User value if we changed a non-1 prior; leave 1 if that is the course default
        if ($null -ne $priorUser -and $priorUser -ne "1") {
            [Environment]::SetEnvironmentVariable($varName, $priorUser, "User")
        }
        # If prior was empty and this is a CI-like ephemeral account, leave 1 (course-correct).
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

# --- winget ids resolve (soft if winget broken) ---
$winget = Get-Command winget -ErrorAction SilentlyContinue
if ($winget) {
    foreach ($pair in @(
            @{ Id = "SST.opencode"; Hard = $false },
            @{ Id = "OpenJS.NodeJS.LTS"; Hard = $false },
            @{ Id = "Git.Git"; Hard = $false }
        )) {
        try {
            $show = & winget show --id $pair.Id -e --accept-source-agreements 2>&1 | Out-String
            if ($LASTEXITCODE -eq 0 -and $show -match "Version") {
                $vm = [regex]::Match($show, "(?im)^\s*Version:\s*(\S+)")
                $ver = if ($vm.Success) { $vm.Groups[1].Value } else { "?" }
                Write-Result -Name "winget.$($pair.Id)" -Ok $true -Detail "Version $ver" -Hard $pair.Hard
            } else {
                Write-Result -Name "winget.$($pair.Id)" -Ok $false -Detail "winget show failed" -Hard $pair.Hard
            }
        } catch {
            Write-Result -Name "winget.$($pair.Id)" -Ok $false -Detail $_.Exception.Message -Hard $pair.Hard
        }
    }
} else {
    Write-Result -Name "winget.present" -Ok $false -Detail "winget not on PATH" -Hard $false
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
$md += "- Funded key write proofs (OpenCode/Pi/goose/Claude)"
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
