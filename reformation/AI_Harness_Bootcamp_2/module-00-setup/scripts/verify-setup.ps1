[CmdletBinding()]
param(
    [string]$Root = (Get-Location).Path,
    [string]$ResultsPath = ""
)

# Setup report for native Windows PowerShell.
#
# Every check ends in one of three states:
#   PASS  the check ran and the observed value matched.
#   WARN  the check ran, the value is outside the expected set, the work can continue.
#   FAIL  the check ran and the value blocks later work, or the check could not run.
# A check that cannot run reports FAIL with the reason. Nothing degrades to PASS.
# Every non-PASS line carries a NEXT ACTION.
#
# Exit 0 when no check is FAIL. Exit 1 when any check is FAIL.
#
# The report names resolved paths so a stub earlier on PATH is visible, but it replaces
# the user profile directory with ~ and removes any credential embedded in a URL. No
# secret value is printed.

$ErrorActionPreference = 'Continue'

$script:passCount = 0
$script:warnCount = 0
$script:failCount = 0
$script:lines = [System.Collections.Generic.List[string]]::new()

$resolvedRoot = (Resolve-Path -LiteralPath $Root -ErrorAction SilentlyContinue)
if ($resolvedRoot) { $Root = $resolvedRoot.Path }
$ModuleDir = Split-Path -Parent $PSScriptRoot
$PinsFile = Join-Path $ModuleDir 'shared\VERSIONS.md'
$StdErrFile = Join-Path ([IO.Path]::GetTempPath()) ("ahb-verify-{0}.txt" -f ([Guid]::NewGuid().ToString('N')))

if (-not $ResultsPath) {
    $evidenceDir = Join-Path $env:USERPROFILE 'course-evidence\module-00'
    New-Item -ItemType Directory -Force -Path $evidenceDir | Out-Null
    $ResultsPath = Join-Path $evidenceDir ("setup-report-{0}.txt" -f [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ'))
}

# ------------------------------------------------------------------------------ reporting

function Get-Redacted {
    param([string]$Text)
    if ([string]::IsNullOrEmpty($Text)) { return '' }
    $out = [regex]::Replace($Text, '://[^/@\s]*@', '://***@')
    if ($env:USERPROFILE) {
        $out = [regex]::Replace($out, [regex]::Escape($env:USERPROFILE), '~', [Text.RegularExpressions.RegexOptions]::IgnoreCase)
    }
    return $out
}

function Get-OrNone {
    param([string]$Text)
    if ([string]::IsNullOrWhiteSpace($Text)) { return 'none' }
    return (Get-Redacted $Text)
}

function Add-Result {
    param([string]$State, [string]$Name, [string]$Detail, [string]$Action = '')
    $line = "[$State] ${Name}: $Detail"
    if ($State -ne 'PASS') {
        if ([string]::IsNullOrWhiteSpace($Action)) {
            $Action = 'Save this line and stop at this boundary; the troubleshooting guide starts from the first failed check.'
        }
        $line = $line + "`n        NEXT ACTION: $Action"
    }
    $script:lines.Add($line)
    Write-Host $line
    switch ($State) {
        'PASS' { $script:passCount++ }
        'WARN' { $script:warnCount++ }
        default { $script:failCount++ }
    }
}

# --------------------------------------------------------------------- version comparison

# Reads the version from standard output only. A tool that prints a warning to standard
# error still reports its real version.
function Test-VersionCommand {
    param(
        [string]$Name,
        [string]$Command,
        [string[]]$CommandArgs = @('--version'),
        [string]$Expected = ''
    )
    $found = Get-Command $Command -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $found) {
        Add-Result FAIL $Name "$Command is not on PATH" `
            "Install $Command with the step for it in your platform guide, open a new PowerShell window, and run this check again."
        return
    }
    try {
        $output = & $found.Source @CommandArgs 2>$StdErrFile
        $code = $LASTEXITCODE
        $errText = ''
        if (Test-Path -LiteralPath $StdErrFile) {
            $errLines = @(Get-Content -LiteralPath $StdErrFile -ErrorAction SilentlyContinue)
            if ($errLines.Count -gt 0) { $errText = $errLines[0] }
            Remove-Item -LiteralPath $StdErrFile -Force -ErrorAction SilentlyContinue
        }
        $first = ''
        foreach ($item in @($output)) {
            if ($null -ne $item -and -not [string]::IsNullOrWhiteSpace([string]$item)) { $first = ([string]$item).Trim(); break }
        }
        $where = Get-Redacted $found.Source
        if ($code -ne 0) {
            $shown = 'none'
            if ($errText) { $shown = $errText }
            Add-Result FAIL $Name "$where exited $code; first error line: $shown" `
                "Run $Command $($CommandArgs -join ' ') in this window and read the error it prints."
            return
        }
        if (-not $first) {
            Add-Result FAIL $Name "$where printed no version" `
                "Run $Command $($CommandArgs -join ' ') in this window; a command that prints nothing is not the tool the course expects."
            return
        }
        if ($Expected -eq 'UNKNOWN') {
            Add-Result WARN $Name "observed $first at $where; the course pin table could not be read" `
                "Update your clone so the pin table is present, then run this check again."
            return
        }
        if ($Expected -and $first -ne $Expected) {
            Add-Result WARN $Name "course pin $Expected, observed $first at $where" `
                "Write both versions in your setup notes, tell the instructor which one you have, and continue."
            return
        }
        Add-Result PASS $Name "$where - $first"
    } catch {
        Add-Result FAIL $Name "$Command could not be run: $($_.Exception.Message)" `
            "Run $Command $($CommandArgs -join ' ') in this window and read the error it prints."
    }
}

# ------------------------------------------------------------------------------ course pins

function Get-CoursePin {
    param([string]$Component)
    if (-not (Test-Path -LiteralPath $PinsFile)) { return '' }
    foreach ($line in (Get-Content -LiteralPath $PinsFile -ErrorAction SilentlyContinue)) {
        $m = [regex]::Match($line, "^\|\s*$([regex]::Escape($Component))\s*\|\s*``?([0-9][0-9.]*)``?\s*\|")
        if ($m.Success) { return $m.Groups[1].Value }
    }
    return ''
}

$pinOpenCode = Get-CoursePin 'OpenCode'
$pinN8n = Get-CoursePin 'n8n'

# ----------------------------------------------------------------------- platform and machine

# Report the architecture Windows is really running, not the one an emulated 64-bit
# process sees: a PowerShell running under x64 emulation on an ARM64 laptop reports AMD64.
$architecture = $env:PROCESSOR_ARCHITECTURE
if ($env:PROCESSOR_ARCHITEW6432) { $architecture = $env:PROCESSOR_ARCHITEW6432 }
try {
    $osArch = [System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString().ToUpperInvariant()
    if ($osArch) { $architecture = $osArch }
} catch { }
if ($architecture -eq 'X64') { $architecture = 'AMD64' }
$build = [Environment]::OSVersion.Version.Build

if ($env:OS -ne 'Windows_NT') {
    Add-Result FAIL platform 'this verifier reads a native Windows machine, and this is not one' `
        'Run the check for your own platform: the shell verifier for macOS, WSL, Ubuntu and Arch Linux.'
} else {
    if ($architecture -eq 'ARM64') {
        Add-Result FAIL platform "Windows $architecture, build $build" `
            'Stop this path here. The goose installer publishes no Windows ARM64 build. Use a supported x64 laptop, or ask the instructor whether the WSL path covers your machine.'
    } elseif ($architecture -ne 'AMD64') {
        Add-Result FAIL platform "Windows $architecture, build $build" `
            'Use a 64-bit x64 Windows laptop. The course tools publish no build for this architecture.'
    } elseif ($build -ge 22000) {
        Add-Result PASS platform "Windows 11 x64, build $build"
    } elseif ($build -ge 19041) {
        Add-Result WARN platform "Windows 10 x64, build $build; the guide is written on Windows 11" `
            'Record the build in your setup notes and continue. Tell the instructor if a step names a window you cannot find.'
    } else {
        Add-Result FAIL platform "Windows x64, build $build; WinGet and WSL 2 need build 19041 or later" `
            'Install current Windows updates until the build is 19041 or later, restart, and run this check again.'
    }
}

try {
    $profileRoot = [IO.Path]::GetPathRoot($env:USERPROFILE)
    $driveName = $profileRoot.TrimEnd('\', '/').TrimEnd(':')
    $drive = Get-PSDrive -Name $driveName -ErrorAction Stop
    $freeGb = [math]::Floor($drive.Free / 1GB)
    if ($freeGb -ge 15) {
        Add-Result PASS disk.home "$freeGb GB free on drive $driveName, which holds your user profile (course floor 15 GB)"
    } else {
        Add-Result FAIL disk.home "$freeGb GB free on drive $driveName, which holds your user profile; the course floor is 15 GB" `
            'Free space until at least 15 GB is available on that drive, then run this check again.'
    }
} catch {
    Add-Result FAIL disk.home "free space on the user profile drive could not be measured: $($_.Exception.Message)" `
        'Open File Explorer, read the free space on the drive that holds your user profile, and send it to the instructor.'
}

# An empty entry in PATH means the current directory, so any command in the folder you
# happen to be standing in can be run instead of the real one.
$pathParts = @()
if ($env:Path) { $pathParts = $env:Path -split ';' }
$emptyPositions = @()
for ($i = 0; $i -lt $pathParts.Count; $i++) {
    if ([string]::IsNullOrWhiteSpace($pathParts[$i])) { $emptyPositions += ($i + 1) }
}
if ($emptyPositions.Count -eq 0) {
    Add-Result PASS path.empty "$($pathParts.Count) entries in PATH, none of them empty"
} else {
    Add-Result FAIL path.empty "PATH has an empty entry at position $($emptyPositions -join ', ') of $($pathParts.Count); an empty entry means the current directory" `
        'Open Settings, search for "Edit environment variables for your account", delete the blank row and any stray semicolon in Path, open a new PowerShell window, and run this check again.'
}

# ---------------------------------------------------------------------------------- tools

if ($pinOpenCode -and $pinN8n) {
    Add-Result PASS pins.source "OpenCode $pinOpenCode and n8n $pinN8n read from $(Get-Redacted $PinsFile)"
} else {
    Add-Result FAIL pins.source "the course pin table at $(Get-Redacted $PinsFile) is missing or has no version rows" `
        'Update your clone of the course repository, then run this check again.'
    $pinOpenCode = 'UNKNOWN'
    $pinN8n = 'UNKNOWN'
}

Test-VersionCommand git git
Test-VersionCommand node node @('--version')
Test-VersionCommand npm npm
Test-VersionCommand codex codex
Test-VersionCommand opencode opencode @('--version') $pinOpenCode
Test-VersionCommand goose goose
Test-VersionCommand n8n n8n @('--version') $pinN8n

$npmPrefix = ''
$npmCommand = Get-Command npm -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
if ($npmCommand) {
    $npmPrefix = (& $npmCommand.Source config get prefix 2>$null | Out-String).Trim()
}
if ($npmPrefix -and $npmPrefix.StartsWith($env:USERPROFILE, [StringComparison]::OrdinalIgnoreCase) -and (Test-Path -LiteralPath $npmPrefix)) {
    Add-Result PASS npm.prefix "$(Get-Redacted $npmPrefix) is under your user profile"
} else {
    Add-Result FAIL npm.prefix "want a prefix under $(Get-Redacted $env:USERPROFILE), observed $(Get-OrNone $npmPrefix)" `
        'Set the npm prefix to a directory inside your user profile, as the npm step in your guide does, then open a new PowerShell window and run this check again.'
}

foreach ($tool in 'codex', 'opencode', 'n8n') {
    $toolPath = (Get-Command $tool -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1).Source
    if ($toolPath -and $npmPrefix -and $toolPath.StartsWith($npmPrefix, [StringComparison]::OrdinalIgnoreCase)) {
        Add-Result PASS "path.$tool" (Get-Redacted $toolPath)
    } else {
        Add-Result FAIL "path.$tool" "want a command under $(Get-OrNone $npmPrefix), observed $(Get-OrNone $toolPath)" `
            "Reinstall $tool with the global npm step in your guide, then open a new PowerShell window and run this check again."
    }
}

$goosePath = (Get-Command goose -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1).Source
$expectedGoose = Join-Path $env:USERPROFILE '.local\bin\goose.exe'
if ($goosePath -and ($goosePath -eq $expectedGoose)) {
    Add-Result PASS path.goose (Get-Redacted $goosePath)
} else {
    Add-Result FAIL path.goose "want $(Get-Redacted $expectedGoose), observed $(Get-OrNone $goosePath)" `
        'Reinstall goose with the official installer step in your guide, then open a new PowerShell window and run this check again.'
}

$nodeCommand = Get-Command node -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $nodeCommand) {
    Add-Result FAIL runtime.node 'node is not on PATH, so the running Node version could not be read' `
        'Install Node 24 with the step in your guide, open a new PowerShell window, and run this check again.'
} else {
    $nodeMajorText = (& $nodeCommand.Source -p 'Number(process.versions.node.split(".")[0])' 2>$null | Out-String).Trim()
    $nodeCode = $LASTEXITCODE
    if ($nodeCode -ne 0 -or $nodeMajorText -notmatch '^\d+$') {
        Add-Result FAIL runtime.node "the running Node version could not be read from $(Get-Redacted $nodeCommand.Source)" `
            'Run node --version in this window and read the error it prints.'
    } elseif ([int]$nodeMajorText -eq 24) {
        Add-Result PASS runtime.node "Node 24.x at $(Get-Redacted $nodeCommand.Source)"
    } else {
        Add-Result FAIL runtime.node "want Node 24.x, observed $nodeMajorText.x at $(Get-Redacted $nodeCommand.Source)" `
            'Install Node 24 with the step in your guide and make it the first node on PATH, then open a new PowerShell window and run this check again.'
    }
}

$python = Get-Command python -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $python) { $python = Get-Command py -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1 }
if (-not $python) {
    Add-Result FAIL runtime.python 'Python is not on PATH' `
        'Install Python 3.12 or newer with the step in your guide, open a new PowerShell window, and run this check again.'
} else {
    # A zero-length python.exe under WindowsApps is the Microsoft Store alias, not Python.
    # It opens the Store instead of running code.
    $isStoreAlias = $false
    try {
        $item = Get-Item -LiteralPath $python.Source -ErrorAction Stop
        if ($item.Length -eq 0 -and $python.Source -match '\\WindowsApps\\') { $isStoreAlias = $true }
    } catch { $isStoreAlias = $false }

    if ($isStoreAlias) {
        Add-Result FAIL runtime.python "$(Get-Redacted $python.Source) is the Microsoft Store app alias, not a Python installation" `
            'Open Settings, go to Apps, then Advanced app settings, then App execution aliases, and turn off the python.exe and python3.exe aliases. Install Python 3.12 or newer with the step in your guide, open a new PowerShell window, and run this check again.'
    } else {
        try {
            $launcherPrefix = @()
            if ($python.Name -eq 'py.exe') { $launcherPrefix = @('-3.12') }
            $printArgs = $launcherPrefix + @('-c', 'import sys; print(sys.version)')
            $gateArgs = $launcherPrefix + @('-c', 'import sys; raise SystemExit(0 if sys.version_info >= (3,12) else 1)')
            $versionText = (& $python.Source @printArgs 2>$null | Out-String).Trim()
            & $python.Source @gateArgs *> $null
            $pythonCode = $LASTEXITCODE
            $firstVersionLine = ($versionText -split "`r?`n")[0]
            if ($pythonCode -eq 0) {
                Add-Result PASS runtime.python "$(Get-Redacted $python.Source) - $firstVersionLine"
            } elseif ($pythonCode -eq 1) {
                $shownVersion = 'no version'
                if ($firstVersionLine) { $shownVersion = $firstVersionLine }
                Add-Result FAIL runtime.python "want Python 3.12 or newer, observed $shownVersion at $(Get-Redacted $python.Source)" `
                    'Install Python 3.12 or newer with the step in your guide and put it ahead of the older one on PATH, then open a new PowerShell window and run this check again.'
            } else {
                Add-Result FAIL runtime.python "$(Get-Redacted $python.Source) did not run; exit status $pythonCode" `
                    "Run $($python.Name) --version in this window and read the error it prints."
            }
        } catch {
            Add-Result FAIL runtime.python "Python could not be run: $($_.Exception.Message)" `
                "Run $($python.Name) --version in this window and read the error it prints."
        }
    }
}

# ----------------------------------------------------------------------------- course clone

$gitCommand = Get-Command git -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $gitCommand) {
    Add-Result FAIL repo.clone 'git is not on PATH, so the course clone could not be read' `
        'Install Git with the step in your guide, open a new PowerShell window, and run this check again.'
} elseif (Test-Path -LiteralPath (Join-Path $Root '.git')) {
    $remote = (& git -C $Root remote get-url origin 2>$null | Out-String).Trim()
    $revision = (& git -C $Root rev-parse --verify HEAD 2>$null | Out-String).Trim()
    $dirty = @(& git -C $Root status --porcelain 2>$null)
    if ($remote -eq 'https://github.com/TheHolofex/AI_Harness_Bootcamp.git') {
        Add-Result PASS repo.remote $remote
    } else {
        Add-Result FAIL repo.remote "want the course HTTPS origin, observed $(Get-OrNone $remote)" `
            'Point origin at the course repository over HTTPS, or clone it again into a new directory, then run this check again.'
    }
    if ($revision -match '^[0-9a-f]{40}$') {
        Add-Result PASS repo.revision $revision.Substring(0, 12)
    } else {
        Add-Result FAIL repo.revision "no commit is checked out in $(Get-Redacted $Root)" `
            'Run git log -1 in the repository root and read the error it prints.'
    }
    $dirtyCount = @($dirty | Where-Object { $_ -and $_.ToString().Trim() }).Count
    if ($dirtyCount -eq 0) {
        Add-Result PASS repo.clean 'no changed or untracked paths'
    } else {
        Add-Result FAIL repo.clean "$dirtyCount changed or untracked paths in the clone" `
            'Run git status --short in the repository root, then move your own files out of the clone or discard the changes. The clone must stay as cloned.'
    }
} else {
    Add-Result FAIL repo.clone "$(Get-Redacted $Root) is not a Git worktree" `
        'Change to the course repository directory and run this check again from there.'
}

$missingModule = @()
foreach ($required in 'shared\MODULE_00_LAB.md', 'shared\VERSIONS.md', 'shared\case\verify_tool_proof.py', 'shared\case\verify_n8n.py', 'platforms') {
    if (-not (Test-Path -LiteralPath (Join-Path $ModuleDir $required))) { $missingModule += $required }
}
$moduleInRoot = $ModuleDir.StartsWith($Root, [StringComparison]::OrdinalIgnoreCase)
if ($missingModule.Count -gt 0) {
    Add-Result FAIL repo.module "this clone is missing $($missingModule -join ', ') under $(Get-Redacted $ModuleDir)" `
        'Run git pull in the repository root to get the current course files, then run this check again.'
} elseif (-not $moduleInRoot) {
    Add-Result FAIL repo.module "the checks you are running live in $(Get-Redacted $ModuleDir), which is outside $(Get-Redacted $Root)" `
        'Run this check from the repository root you cloned, using the copy of the script inside that clone.'
} else {
    Add-Result PASS repo.module "the course files for this session are present at $(Get-Redacted $ModuleDir)"
}

# ------------------------------------------------------------------- credentials and auth

if ([string]::IsNullOrWhiteSpace($env:XAI_API_KEY)) {
    Add-Result FAIL secret.xai 'MISSING in current process' `
        'Enter the key again with the hidden-input step in your guide, in this same window, then run this check again.'
} else {
    Add-Result PASS secret.xai 'SET in current process; value not printed'
}

if ($env:GOOSE_PROVIDER -eq 'xai' -and -not [string]::IsNullOrWhiteSpace($env:GOOSE_MODEL)) {
    Add-Result PASS config.goose "provider=xai model=$env:GOOSE_MODEL"
} else {
    $shownProvider = 'unset'
    if ($env:GOOSE_PROVIDER) { $shownProvider = $env:GOOSE_PROVIDER }
    $shownModel = 'unset'
    if ($env:GOOSE_MODEL) { $shownModel = $env:GOOSE_MODEL }
    Add-Result FAIL config.goose "provider=$shownProvider model=$shownModel" `
        'Set GOOSE_PROVIDER and GOOSE_MODEL to the values in your guide, in this same window, then run this check again.'
}

$codexCommand = Get-Command codex -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $codexCommand) {
    Add-Result FAIL auth.codex 'codex is not on PATH, so its sign-in state could not be read' `
        'Install codex with the step in your guide, open a new PowerShell window, and run this check again.'
} else {
    try {
        & $codexCommand.Source login status *> $null
        if ($LASTEXITCODE -eq 0) {
            Add-Result PASS auth.codex 'login-status command passed; account details not copied'
        } else {
            Add-Result FAIL auth.codex "codex login status exited $LASTEXITCODE" `
                'Run codex login status in this window and read its message before signing in again.'
        }
    } catch {
        Add-Result FAIL auth.codex "codex login status could not be run: $($_.Exception.Message)" `
            'Run codex login status in this window and read its message.'
    }
}

# ---------------------------------------------------------------------------------- verdict

if ($script:failCount -eq 0) {
    $verdict = "SETUP CHECK PASS - $($script:passCount) PASS, $($script:warnCount) WARN, $($script:failCount) FAIL"
} else {
    $verdict = "SETUP CHECK HOLD - $($script:passCount) PASS, $($script:warnCount) WARN, $($script:failCount) FAIL"
}

$report = [System.Collections.Generic.List[string]]::new()
$report.Add('AI Harness Bootcamp setup report')
$report.Add("Generated: $([DateTime]::UtcNow.ToString('s'))Z")
if ($env:OS -eq 'Windows_NT') {
    $report.Add("Platform: Windows $architecture build $build")
} else {
    $report.Add("Platform: not Windows; this verifier could not read the machine")
}
$report.Add("Root: $(Get-Redacted $Root)")
$report.Add('')
$report.AddRange($script:lines)
$report.Add('')
$report.Add($verdict)
Set-Content -LiteralPath $ResultsPath -Value $report -Encoding utf8

Remove-Item -LiteralPath $StdErrFile -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "$verdict - report: $ResultsPath"
if ($script:failCount -eq 0) { exit 0 }
exit 1
