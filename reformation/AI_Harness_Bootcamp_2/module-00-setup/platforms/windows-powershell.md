# Windows PowerShell setup

This path installs the course tools on native Windows and proves one bounded write from Oh My Pi. Plan for 60 to 120 minutes. Open **Windows PowerShell** on the Windows computer, from the Start menu. PowerShell on macOS or Linux is not this path, and an elevated Administrator window is not required after Windows itself is already installed.

You need Git, Python 3.12 or newer, a browser, an ordinary text editor, and Oh My Pi 18.3.5. The only provider key is `OPENROUTER_API_KEY`. The course launcher selects `openrouter/anthropic/claude-sonnet-4.6`. You do not install Node, npm, n8n, Obsidian, or another agent for this path.

A checksum is a fingerprint of a file. You compare the fingerprint of the downloaded program with the fingerprint published beside it, and you do that before the program is allowed to run. PATH is the list of folders Windows searches when you type a command name.

The work falls into five parts: install Git and Python, install the verified Oh My Pi binary, put the course checkout in your home folder, enter the key only into this process, and then run the proof and the prerequisite report.

If a company policy denies an installer, stop and save the message. Do not open an Administrator window to get around that denial. When a step stops, start from the first failed check in [When setup stops](../shared/TROUBLESHOOTING.md).

## Check the disk and the processor

You need enough free space for Git, Python, and the course checkout, and you need the Windows binary that matches the processor. The processor code comes from Windows itself: 12 means ARM64 and 9 means x64. The process you happen to be running can report a different architecture, so this check does not use that process value.

**Terminal: Windows PowerShell, ordinary user.**

```powershell
$driveName = ([IO.Path]::GetPathRoot($HOME).TrimEnd('\'))[0]
$freeGb = (Get-PSDrive -Name $driveName).Free / 1GB
Write-Output ("free GB: " + [math]::Round($freeGb, 1))
$archCode = (Get-CimInstance -ClassName Win32_Processor | Select-Object -First 1).Architecture
if ($archCode -eq 12) {
  $asset = 'omp-windows-arm64.exe'
} elseif ($archCode -eq 9) {
  $asset = 'omp-windows-x64.exe'
} else {
  throw 'STOP: this processor does not have a published course binary.'
}
Write-Output $asset
```

**Expected:** free space of at least 15 GB, then either `omp-windows-arm64.exe` or `omp-windows-x64.exe`.

**Stop:** free space is under 15 GB, the processor query fails, or the script stops because no published binary matches.

**Recovery:** free space on the Windows drive and run the block again. If the processor still does not match, save the code it printed and use the support packet. Do not download the other architecture and hope it runs.

The architecture numbers are documented with [Win32_Processor](https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-processor).

## Install Git and Python for your user

Git copies the course repository. Python 3.12 or newer runs the course helpers. Both installs stay in your user account when the package manager allows that.

**Terminal: Windows PowerShell, ordinary user.**

```powershell
winget --version
winget install --exact --id Git.Git --source winget --scope user --accept-package-agreements --accept-source-agreements
winget install --exact --id Python.Python.3.12 --source winget --scope user --accept-package-agreements --accept-source-agreements
```

**Expected:** `winget` prints a version, and both install commands finish without an access-denied or policy message. The installers can take several minutes and may ask you to approve an official installer prompt.

**Stop:** `winget` is not recognized, either install reports that a policy blocked it, or an approval prompt is denied.

**Recovery:** if `winget` is simply not recognized, and the message does not say that installs are blocked, install current-user Git from [Git for Windows](https://git-scm.com/downloads/win) and current-user Python 3.12 or newer from [Python for Windows](https://docs.python.org/3/using/windows.html). On the Python installer, choose the current-user option and turn on **Add python.exe to PATH**. If a policy message blocks the install, stop. Do not switch to an Administrator window to bypass it. [WinGet](https://learn.microsoft.com/en-us/windows/package-manager/winget/) is the package command used above.

Close this PowerShell window after the installers finish. The next window has to read the saved PATH.

## Resolve the real Python 3.12 executable

The later helpers must run on one absolute Python program, not on a Store stub that only opens a shop page. This new window also shows whether the installer PATH survived outside the window that ran the install.

**Terminal: Windows PowerShell, ordinary user.**

```powershell
$PY = $null
$launcher = Get-Command py -ErrorAction SilentlyContinue
if ($launcher -and $launcher.Source -notlike '*\WindowsApps\*') {
  $PY = (& $launcher.Source -3.12 -c 'import sys; print(sys.executable)').Trim()
}
if (-not $PY) {
  foreach ($name in @('python', 'python3')) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    if ($cmd -and $cmd.Source -notlike '*\WindowsApps\*') {
      $PY = $cmd.Source
      break
    }
  }
}
if (-not $PY) { throw 'STOP: Python 3.12 or newer was not found outside the Store alias.' }
$item = Get-Item -LiteralPath $PY -Force
if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
  $PY = $item.Target
  if ($PY -is [array]) { $PY = $PY[0] }
  $item = Get-Item -LiteralPath $PY -Force
}
if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
  throw 'STOP: Python still resolves through a link. It was not accepted.'
}
if ($PY -like '*\WindowsApps\*') { throw 'STOP: Python points at the Store alias.' }
& $PY -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)'
if ($LASTEXITCODE -ne 0) { throw 'STOP: that Python is older than 3.12.' }
Write-Output $PY
& $PY --version
```

**Expected:** one absolute path to `python.exe`, then a version line beginning `Python 3.12` or newer. The path does not contain `WindowsApps`.

**Stop:** no usable Python is found, the path is a Store alias or a link that cannot be resolved, or the version is older than 3.12.

**Recovery:** install Python 3.12 for the current user, turn off the `python.exe` and `python3.exe` app execution aliases under Settings, Apps, Advanced app settings, App execution aliases, then close PowerShell and run this block in a new window. Do not point `$PY` at a copy you typed by hand. The alias setting is described in [Python for Windows](https://docs.python.org/3/using/windows.html).

Keep this window open. `$PY` exists only in this process.

## Download Oh My Pi and verify it before it can run

You download the selected binary and `SHA256SUMS.txt` from the pinned release into a new folder that belongs only to this attempt. The published file lists a lowercase SHA-256 fingerprint, two spaces, then the exact filename. Nothing is copied into place, and nothing is executed, unless that exact line matches the file you downloaded.

The release page is [Oh My Pi v18.3.5](https://github.com/can1357/oh-my-pi/releases/tag/v18.3.5). `Get-FileHash` is the Windows command that computes the fingerprint: [Get-FileHash](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-filehash).

**Terminal: Windows PowerShell, ordinary user.**

```powershell
$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
if (-not $env:LOCALAPPDATA) { throw 'STOP: LOCALAPPDATA is not set.' }
$archCode = (Get-CimInstance -ClassName Win32_Processor | Select-Object -First 1).Architecture
if ($archCode -eq 12) {
  $asset = 'omp-windows-arm64.exe'
} elseif ($archCode -eq 9) {
  $asset = 'omp-windows-x64.exe'
} else {
  throw 'STOP: this processor does not have a published course binary.'
}
$downloadParent = Join-Path $env:LOCALAPPDATA 'omp-downloads'
if (Test-Path -LiteralPath $downloadParent) {
  $parentItem = Get-Item -LiteralPath $downloadParent -Force
  if ($parentItem.Attributes -band [IO.FileAttributes]::ReparsePoint) {
    throw 'STOP: the download parent is a link. Nothing was downloaded.'
  }
} else {
  New-Item -ItemType Directory -Path $downloadParent | Out-Null
}
$download = Join-Path $downloadParent ([guid]::NewGuid().ToString('n'))
New-Item -ItemType Directory -Path $download | Out-Null
$base = 'https://github.com/can1357/oh-my-pi/releases/download/v18.3.5'
$sumsPath = Join-Path $download 'SHA256SUMS.txt'
$binaryPath = Join-Path $download $asset
Invoke-WebRequest -Uri ($base + '/SHA256SUMS.txt') -OutFile $sumsPath -UseBasicParsing
Invoke-WebRequest -Uri ($base + '/' + $asset) -OutFile $binaryPath -UseBasicParsing
if (-not (Test-Path -LiteralPath $sumsPath) -or -not (Test-Path -LiteralPath $binaryPath)) {
  throw 'STOP: a download is missing. Nothing was installed.'
}
$matches = @(Get-Content -LiteralPath $sumsPath | Where-Object {
  $pair = $_ -split '  ', 2
  $pair.Length -eq 2 -and $pair[1].Trim() -eq $asset
})
if ($matches.Count -ne 1) { throw 'STOP: the checksum file has no single exact line for the selected file. Nothing was installed.' }
$expected = (($matches[0] -split '  ', 2)[0]).Trim().ToLowerInvariant()
if ($expected -notmatch '^[0-9a-f]{64}$') { throw 'STOP: the checksum line is not a SHA-256 value. Nothing was installed.' }
$actual = (Get-FileHash -LiteralPath $binaryPath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actual -ne $expected) { throw 'STOP: checksum failed. Nothing was installed.' }
$destDir = Join-Path $env:LOCALAPPDATA 'omp'
$dest = Join-Path $destDir 'omp.exe'
foreach ($probe in @($destDir, $dest)) {
  if (Test-Path -LiteralPath $probe) {
    $probeItem = Get-Item -LiteralPath $probe -Force
    if ($probeItem.Attributes -band [IO.FileAttributes]::ReparsePoint) {
      throw 'STOP: the destination is a symlink or junction. It was not replaced.'
    }
  }
}
if (Test-Path -LiteralPath $dest) {
  $destItem = Get-Item -LiteralPath $dest -Force
  if ($destItem.PSIsContainer) { throw 'STOP: the destination is a folder. It was not replaced.' }
  $existing = (Get-FileHash -LiteralPath $dest -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($existing -ne $actual) { throw 'STOP: a different file is already at the destination. It was not replaced.' }
} else {
  if (-not (Test-Path -LiteralPath $destDir)) {
    New-Item -ItemType Directory -Path $destDir | Out-Null
  }
  Copy-Item -LiteralPath $binaryPath -Destination $dest
}
Write-Output $download
Write-Output $dest
& $dest --version
```

**Expected:** the download folder path, the destination path ending in `\omp\omp.exe` under your local app data, and a version line `omp/18.3.5`. That version command is the first time the program runs, and it runs only after the fingerprint matched.

**Stop:** the script stops on a failed download, a missing or extra checksum line, a fingerprint mismatch, a symlink or junction, or a different file already at the destination. The destination is left untouched in those cases.

**Recovery:** leave the download folder in place and run the block again only after you have read the stop line. A second run uses a new download folder. Do not copy the binary into place yourself, and do not delete a different existing `omp.exe`. If Windows itself blocks the verified file from starting, save that message and stop. Do not turn off a security control to force it.

## Save the program folder on your user PATH

The launcher finds `omp` by name. This step records the destination folder in your user PATH so a later window can find the same binary. It does not store the API key.

**Terminal: Windows PowerShell, ordinary user.**

```powershell
$ompDir = Join-Path $env:LOCALAPPDATA 'omp'
$dest = Join-Path $ompDir 'omp.exe'
if (-not (Test-Path -LiteralPath $dest)) { throw 'STOP: the verified binary is not at the destination.' }
$current = [Environment]::GetEnvironmentVariable('Path', 'User')
$kept = @()
if ($current) {
  $kept = @($current -split ';' | Where-Object { $_ -and ($_.TrimEnd('\') -ine $ompDir.TrimEnd('\')) })
}
$updated = (@($ompDir) + $kept) -join ';'
[Environment]::SetEnvironmentVariable('Path', $updated, 'User')
$env:Path = $ompDir + ';' + $env:Path
$found = (Get-Command omp -ErrorAction SilentlyContinue).Source
Write-Output $found
```

**Expected:** the printed path is the same `\omp\omp.exe` path under local app data.

**Stop:** the command is not found, or the found path is a different file.

**Recovery:** run the download block again only if the destination file is missing. If a different `omp` is found, do not overwrite it. Save the printed path and stop. PATH changes are documented in [about_Environment_Variables](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables).

## Use the course checkout, or clone it once

The course lives at `$HOME\AI_Harness_Bootcamp`. An existing checkout of the course origin is used as it is. A different folder at that path is left alone.

Git can rewrite line endings while it copies text files. A line ending is the hidden character at the end of a line. Later checks compare exact bytes, so a rewritten ending makes a frozen control look changed even when the words are the same. The copy command below turns that rewrite off for this one command. It does not save a Git setting, and it does not reset, clean, pull, or renormalize a folder that is already there. The published course also marks these text files to keep their published line endings on a later fresh copy.

After the copy is found or made, this step reads three frozen controls: the Module 1 source manifest, the Module 7 policy file, and the Module 9 restore control. A carriage return in any of them means this copy was already rewritten. That result is a hold. Leave the folder untouched and get an intact fresh copy. This step does not give permission to repair the existing files.

**Terminal: Windows PowerShell, ordinary user.**

```powershell
$R = Join-Path $HOME 'AI_Harness_Bootcamp'
$origin = 'https://github.com/TheHolofex/AI_Harness_Bootcamp.git'
$usingExisting = $false
if (Test-Path -LiteralPath $R) {
  if (-not (Test-Path -LiteralPath (Join-Path $R '.git'))) {
    throw 'STOP: the home folder already has AI_Harness_Bootcamp, and it is not a Git checkout. It was not replaced.'
  }
  $remote = (& git -C $R remote get-url origin 2>$null)
  if ($LASTEXITCODE -ne 0 -or $remote.Trim() -ne $origin) {
    throw 'STOP: that checkout has a different origin. It was not replaced, reset, pulled, or cleaned.'
  }
  $usingExisting = $true
} else {
  & git -c core.autocrlf=false clone $origin $R
  if ($LASTEXITCODE -ne 0) { throw 'STOP: clone failed. No partial folder was cleaned up by this step.' }
}
$M = Join-Path $R 'reformation\AI_Harness_Bootcamp_2\module-00-setup'
$lab = Join-Path $M 'shared\MODULE_00_LAB.md'
if (-not (Test-Path -LiteralPath $lab)) {
  throw 'STOP: this checkout does not contain the Module 0 lab. It was not reset, pulled, or cleaned.'
}
$frozen = @(
  'reformation\AI_Harness_Bootcamp_2\module-01-mission-thread\shared\case\SOURCE_MANIFEST.json',
  'reformation\AI_Harness_Bootcamp_2\module-07-change-eval\shared\controls\policy.json',
  'reformation\AI_Harness_Bootcamp_2\module-09-capstone\shared\baseline\run.json'
)
foreach ($rel in $frozen) {
  $path = Join-Path $R $rel
  if (-not (Test-Path -LiteralPath $path)) {
    throw 'STOP: a frozen control is missing. The checkout was not reset, pulled, or cleaned.'
  }
  $item = Get-Item -LiteralPath $path -Force
  if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
    throw 'STOP: a frozen control is a folder or a link. It was not followed or changed.'
  }
  $bytes = [IO.File]::ReadAllBytes($path)
  if ([Array]::IndexOf($bytes, [byte]13) -ge 0) {
    throw 'HOLD: a frozen control has rewritten line endings. The checkout was not reset, cleaned, pulled, or renormalized.'
  }
}
if ($usingExisting) {
  Write-Output 'Using the existing course checkout.'
} else {
  Write-Output 'Cloned the course checkout.'
}
Write-Output 'Line endings unchanged.'
Write-Output $R
Write-Output $M
```

**Expected:** either `Using the existing course checkout.` or `Cloned the course checkout.`, then `Line endings unchanged.`, then the absolute course path and the Module 0 path.

**Stop:** the folder exists but is not the course origin, Git cannot read the origin, the clone fails, the lab file is missing, a frozen control is missing or is a folder or link, or a frozen control contains a rewritten line ending. The hold line is `HOLD: a frozen control has rewritten line endings. The checkout was not reset, cleaned, pulled, or renormalized.`

**Recovery:** leave the existing folder in place. If it is the wrong project, choose a different computer folder only with the person who supports your machine; do not delete, reset, pull, or clean this one. If the hold names rewritten line endings, do not edit those files and do not renormalize them. Ask the person who supports your machine before moving the folder aside. After `$HOME\AI_Harness_Bootcamp` is no longer occupied, run this block again so the new copy is intact. If a copy you just made still prints that hold, stop and save the message. If the clone failed before creating the folder, run the block again. If a partial folder was created and it is not a valid course checkout, stop and save the Git message. The one-command setting is documented in [git](https://git-scm.com/docs/git). The line-ending setting it overrides is [core.autocrlf](https://git-scm.com/docs/git-config#Documentation/git-config.txt-coreautocrlf). The clone URL is the course repository documented in [Cloning a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

`$R` and `$M` belong to this window. You will set them again in the window that runs the proof.

## Enter the key without showing it

The next command does nothing except wait for the key. Type the key at that hidden prompt and press Enter. Do not paste the key into the command, a file, a profile, or a chat. The rules for where a key must not go are in [Connect the course account without leaking a key](../shared/CREDENTIALS.md).

**Terminal: Windows PowerShell, ordinary user.**

```powershell
$secret = Read-Host -Prompt 'OpenRouter API key' -AsSecureString
```

**Expected:** the prompt returns, and the key does not appear as readable text. Windows PowerShell may show asterisks. That is still hidden input.

**Stop:** the key appears in readable text, or you pasted it into the command line instead of the prompt.

**Recovery:** if the key was displayed or pasted into a command, revoke it with the provider, use the replacement, and run only this command again. Do not continue with a key that has been displayed.

## Load the key into this process only

This second command turns the hidden value into a process environment variable, clears the temporary copy, and prints only `SET` or `MISSING`. A SecureString is the hidden value from the previous command. The conversion uses a temporary BSTR, which is an unmanaged string, and then zeroes that memory. The key is not written to a file, a profile, or the saved user environment.

The conversion and zeroing methods are [SecureStringToBSTR](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.interopservices.marshal.securestringtobstr) and [ZeroFreeBSTR](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.interopservices.marshal.zerofreebstr).

**Terminal: Windows PowerShell, ordinary user.**

```powershell
$bstr = [IntPtr]::Zero
$plain = $null
try {
  if ($null -eq $secret) { throw 'STOP: run the hidden read in this window first.' }
  $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secret)
  $plain = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
  if ([string]::IsNullOrWhiteSpace($plain)) {
    Write-Output 'MISSING'
  } else {
    $env:OPENROUTER_API_KEY = $plain
    Write-Output 'SET'
  }
} finally {
  if ($bstr -ne [IntPtr]::Zero) {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
  }
  $plain = $null
  if ($null -ne $secret) { $secret.Dispose() }
  $secret = $null
}
```

**Expected:** `SET`.

**Stop:** `MISSING`, an error before either word, or any output that contains the key.

**Recovery:** run the hidden-read command again in this same window, then run this command again. Do not check the key by printing the environment. Do not save it with `SetEnvironmentVariable`.

## Open an independent window and read the difference

A window you open from the Start menu is a new process. It does not inherit the previous window's environment, so the key you loaded only into that process should be absent here. A child process is different: typing `powershell` inside the window that has the key can inherit the variable. `SET` in that child does not prove the key was written to a profile or a file. `SET` by itself is never proof of a saved leak. `MISSING` in an independently opened window is the check that this new process did not receive a saved key.

Close the previous window's work only after you have seen `SET` there. Then open Windows PowerShell from the Start menu. Do not type `powershell` in the old window. This window also does not have `$PY`, `$R`, or `$M`. Resolve Python again in this window before the proof, and let the proof block set `$R` and `$M` again.

**Terminal: Windows PowerShell, ordinary user.**

```powershell
$dest = Join-Path $env:LOCALAPPDATA 'omp\omp.exe'
$found = (Get-Command omp -ErrorAction SilentlyContinue).Source
Write-Output $found
& $dest --version
if ([string]::IsNullOrWhiteSpace($env:OPENROUTER_API_KEY)) { Write-Output 'MISSING' } else { Write-Output 'SET' }
```

**Expected:** the found path is the verified `\omp\omp.exe`, the version line is `omp/18.3.5`, and the last line is `MISSING`.

**Stop:** the command is missing, the path differs, the version differs, or an independently opened window prints `SET` before you type a key.

**Recovery:** if the program path or version is wrong, return to the install step and do not overwrite a different file. If this independent window prints `SET`, run the next check before you enter a key. Do not print the variable.

## Check for a saved key without displaying it

Run this only when the independent window printed `SET` before you typed a key. It looks for the variable name in the saved environment and in PowerShell profiles, and it does not print a value or a matching line.

**Terminal: Windows PowerShell, ordinary user.**

```powershell
foreach ($scope in @('User', 'Machine')) {
  $saved = [Environment]::GetEnvironmentVariable('OPENROUTER_API_KEY', $scope)
  if (-not [string]::IsNullOrEmpty($saved)) {
    $saved = $null
    throw ('STOP: a saved ' + $scope + ' environment entry exists. The value was not printed.')
  }
}
$profiles = @(
  $PROFILE.CurrentUserCurrentHost,
  $PROFILE.CurrentUserAllHosts,
  $PROFILE.AllUsersCurrentHost,
  $PROFILE.AllUsersAllHosts
)
foreach ($path in $profiles) {
  if ($path -and (Test-Path -LiteralPath $path)) {
    if (Select-String -LiteralPath $path -Pattern 'OPENROUTER_API_KEY' -SimpleMatch -Quiet) {
      throw 'STOP: a PowerShell profile names the key variable. The line was not printed.'
    }
  }
}
Write-Output 'No saved environment entry or profile reference was found.'
```

**Expected:** if you reached this command because the new window printed `SET`, the script stops with a saved-entry or profile message. If you ran it after a correct `MISSING`, the line is `No saved environment entry or profile reference was found.`

**Stop:** a saved entry or a profile reference exists. Also stop if the independent window printed `SET` but this check finds nothing: something else is supplying the variable, and you still must not print it.

**Recovery:** revoke the key at the provider. If the stop line names the User scope, remove that saved name with the next command, then open a new window from the Start menu and confirm `MISSING` before you enter the replacement. If the stop line names Machine scope or a profile, do not delete the profile blindly and do not change machine settings. Remove the assignment in an editor without copying the value, or ask the person who supports the computer. Then confirm a new Start-menu window prints `MISSING`.

**Terminal: Windows PowerShell, ordinary user.**

```powershell
[Environment]::SetEnvironmentVariable('OPENROUTER_API_KEY', $null, 'User')
Write-Output 'User environment name cleared. The value was not printed.'
```

**Expected:** the cleared line, and no key text.

**Stop:** you did not first see a stop line that named the User scope, or the key appears in the output.

**Recovery:** run this only after the check names the User scope. For a Machine scope or profile finding, use the recovery in the previous step instead of this command.

## Enter the key again in the proof window

The proof has to run in the independent window, because that is the window whose PATH came from the saved user setting. The key does not come along. Repeat the hidden read, then the separate conversion. Do not skip the read and paste the key into the conversion command.

**Terminal: Windows PowerShell, ordinary user.**

```powershell
$secret = Read-Host -Prompt 'OpenRouter API key' -AsSecureString
```

**Expected:** the prompt returns, and the key is not readable on screen.

**Stop:** the key is visible as readable text.

**Recovery:** revoke a displayed key, then run this read again.

**Terminal: Windows PowerShell, ordinary user.**

```powershell
$bstr = [IntPtr]::Zero
$plain = $null
try {
  if ($null -eq $secret) { throw 'STOP: run the hidden read in this window first.' }
  $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secret)
  $plain = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
  if ([string]::IsNullOrWhiteSpace($plain)) {
    Write-Output 'MISSING'
  } else {
    $env:OPENROUTER_API_KEY = $plain
    Write-Output 'SET'
  }
} finally {
  if ($bstr -ne [IntPtr]::Zero) {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
  }
  $plain = $null
  if ($null -ne $secret) { $secret.Dispose() }
  $secret = $null
}
```

**Expected:** `SET`.

**Stop:** `MISSING`, or any output that contains the key.

**Recovery:** run the hidden read and this conversion again in this window. Do not continue to the proof on `MISSING`.

## Create a fresh proof folder and token

The proof folder is outside the course checkout. You are preparing one fresh attempt so the model can read a token and write only `from-omp.txt`. The token is created by Python's secrets module and stored outside the proof folder, then copied in, so the model has to read it. The evidence folder is only a path at this point. You do not create it. You also do not create `from-omp.txt`.

Run the Python resolve block in this window before this block. `$PY` from an earlier window is not here. This block sets `$R` and `$M` again. Stay in this window through the checker and the report, because a new Start-menu window does not keep `$PY`, `$R`, `$M`, `$attempt`, or the key.

Windows PowerShell removes quotation marks that sit inside a short `-c` program before Python sees them. The programs below are sent on standard input, which is the text a program reads when you pipe into it, and each file path is a separate argument. The quotation marks therefore stay in the program. Those programs write UTF-8 text and do not print the token. This block also stops if a frozen control was rewritten, and it does not repair that copy. The quoting rules are in [about_Quoting_Rules](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_quoting_rules?view=powershell-5.1). `$OutputEncoding` is the encoding PowerShell uses when it sends that text, described in [about_Preference_Variables](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables?view=powershell-5.1).

**Terminal: Windows PowerShell, ordinary user.**

```powershell
if (-not $PY) { throw 'STOP: resolve Python again in this window before the proof.' }
$R = Join-Path $HOME 'AI_Harness_Bootcamp'
$M = Join-Path $R 'reformation\AI_Harness_Bootcamp_2\module-00-setup'
$frozen = @(
  'reformation\AI_Harness_Bootcamp_2\module-01-mission-thread\shared\case\SOURCE_MANIFEST.json',
  'reformation\AI_Harness_Bootcamp_2\module-07-change-eval\shared\controls\policy.json',
  'reformation\AI_Harness_Bootcamp_2\module-09-capstone\shared\baseline\run.json'
)
foreach ($rel in $frozen) {
  $path = Join-Path $R $rel
  if (-not (Test-Path -LiteralPath $path)) {
    throw 'STOP: a frozen control is missing. Nothing was created for this proof.'
  }
  $item = Get-Item -LiteralPath $path -Force
  if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
    throw 'STOP: a frozen control is a folder or a link. It was not followed or changed.'
  }
  $bytes = [IO.File]::ReadAllBytes($path)
  if ([Array]::IndexOf($bytes, [byte]13) -ge 0) {
    throw 'HOLD: a frozen control has rewritten line endings. Nothing was created, and the checkout was not changed.'
  }
}
$runId = [guid]::NewGuid().ToString('n')
$run = Join-Path (Join-Path $HOME 'course-evidence\reformation-qa') $runId
$attempt = Join-Path $run 'module-00'
$proof = Join-Path $attempt 'proof'
$tokenFile = Join-Path $attempt 'run-token.txt'
$evidence = Join-Path $attempt ('evidence-' + [guid]::NewGuid().ToString('n'))
if ((Test-Path -LiteralPath $proof) -or (Test-Path -LiteralPath $tokenFile) -or (Test-Path -LiteralPath $evidence)) {
  throw 'STOP: an attempt path already exists. Nothing was overwritten.'
}
New-Item -ItemType Directory -Path $proof | Out-Null
$savedOutputEncoding = $OutputEncoding
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
try {
@'
import pathlib, secrets, sys
pathlib.Path(sys.argv[1]).write_text(secrets.token_hex(16) + "\n", encoding="utf-8")
'@ | & $PY - $tokenFile
if ($LASTEXITCODE -ne 0) { throw 'STOP: the token file was not written.' }
Copy-Item -LiteralPath $tokenFile -Destination (Join-Path $proof 'run-token.txt')
$promptFile = Join-Path $proof 'prompt.txt'
@'
import pathlib, sys
pathlib.Path(sys.argv[1]).write_text("Use only the course_read and course_write tools. Do not use any other tool.\nUse course_read to read the file run-token.txt in your work directory. The token is the exact text of that file, with surrounding space removed.\nUse course_write to write only the file from-omp.txt. The entire file must be the two words omp works, then one space, then that exact token. Do not write any other file.\n", encoding="utf-8")
'@ | & $PY - $promptFile
if ($LASTEXITCODE -ne 0) { throw 'STOP: the prompt file was not written.' }
} finally {
  $OutputEncoding = $savedOutputEncoding
}
Write-Output $proof
Write-Output $tokenFile
Write-Output $evidence
Write-Output ('evidence exists now: ' + (Test-Path -LiteralPath $evidence))
```

**Expected:** three absolute paths, then `evidence exists now: False`. The token value is not printed.

**Stop:** Python is missing, a frozen control is missing or rewritten, a path already exists, a file cannot be written, or the evidence line is `True`. The line-ending hold is `HOLD: a frozen control has rewritten line endings. Nothing was created, and the checkout was not changed.`

**Recovery:** if the stop says to resolve Python, run that block in this window and then run this block again. If the hold names rewritten line endings, return to the checkout step. Do not edit the course files. Leave any partial attempt in place and run this block again only after the checkout hold is cleared, so the new attempt has new paths. Do not delete the course checkout, and do not create the evidence folder or `from-omp.txt` by hand.

## Ask for the one permitted write

The launcher runs the pinned Oh My Pi binary with permission to write only `from-omp.txt`. It reads the key from this process. If the key is missing, it stops before it creates the evidence folder. If the live attempt fails, it keeps the evidence it created. Do not run the launcher a second time against a proof folder that already contains `from-omp.txt`.

**Terminal: Windows PowerShell, ordinary user.**

```powershell
$launcher = Join-Path $R 'reformation\shared\run_omp.py'
if (Test-Path -LiteralPath $evidence) { throw 'STOP: the evidence path already exists. Choose a new attempt.' }
if (Test-Path -LiteralPath (Join-Path $proof 'from-omp.txt')) { throw 'STOP: the proof folder already has a write. Keep it and start a new attempt.' }
& $PY $launcher --workdir $proof --prompt $promptFile --evidence $evidence --allow-write 'from-omp.txt'
Write-Output ('launcher exit ' + $LASTEXITCODE)
Write-Output ('evidence exists after launch: ' + (Test-Path -LiteralPath $evidence))
```

**Expected:** the launcher finishes, the exit line is `launcher exit 0`, and the evidence folder now exists. The launcher may also print a status line of its own. That line is not the tool proof.

**Stop:** exit 2, especially with a missing-key hold, means a prerequisite failed. The evidence folder should still be absent, and you must not invent the proof file. Exit 1 means the live attempt failed. Exit 0 with no evidence folder is also a stop.

**Recovery:** on exit 2 with no evidence folder, enter the key again in this window and start again at the fresh-proof step so the new attempt has new paths. On exit 1, or if `from-omp.txt` already exists, keep both folders and start again at the fresh-proof step. Do not retry into the same proof folder, and do not write `from-omp.txt` yourself.

## Check the write against the token and the receipt

The checker takes the proof folder, the token file outside that folder, and the evidence folder. It passes only when `from-omp.txt` contains the words `omp works`, one space, and this run's token, and a `course_write` receipt matches the file on disk.

**Terminal: Windows PowerShell, ordinary user.**

```powershell
$checker = Join-Path $M 'shared\case\verify_tool_proof.py'
& $PY $checker $proof $tokenFile $evidence
Write-Output ('checker exit ' + $LASTEXITCODE)
```

**Expected:** the checker's last result line is `TOOL PROOF PASS`, and the exit line is `checker exit 0`.

**Stop:** the last result line is `TOOL PROOF HOLD`, the checker exits nonzero, or the proof file is missing. A file you create by hand is not a pass.

**Recovery:** keep this attempt. Return to the fresh-proof step and use new folders. Do not edit `from-omp.txt` to make the words match.

## Record prerequisites, not the live turn

This report checks that Git, Python, Oh My Pi, the checkout, and the key are present in this process. A passing report does not prove the live write. A dirty checkout is not a reason to reset, pull, or clean. The tool proof you already ran is the live-write check. Stay in the proof window for this report. `$R`, `$M`, and `$attempt` are already set there, and a new Start-menu window does not have them or the key.

Windows PowerShell may refuse a `.ps1` file until the current user allows local scripts. A managed policy is left unchanged. Execution policies are described in [about_Execution_Policies](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies).

**Terminal: Windows PowerShell, ordinary user.**

```powershell
Get-ExecutionPolicy -List | Format-Table -AutoSize | Out-String | Write-Output
$machinePolicy = (Get-ExecutionPolicy -Scope MachinePolicy)
$userPolicy = (Get-ExecutionPolicy -Scope UserPolicy)
if ($machinePolicy -ne 'Undefined' -or $userPolicy -ne 'Undefined') {
  throw 'STOP: a managed execution policy is in effect. It was not changed.'
}
$currentPolicy = Get-ExecutionPolicy -Scope CurrentUser
Write-Output ('CurrentUser before: ' + $currentPolicy)
if ($currentPolicy -eq 'Restricted' -or $currentPolicy -eq 'Undefined' -or $currentPolicy -eq 'AllSigned') {
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
}
Write-Output ('CurrentUser after: ' + (Get-ExecutionPolicy -Scope CurrentUser))
```

**Expected:** the policy list, then a CurrentUser value of `RemoteSigned`, `Unrestricted`, or `Bypass` on the after line. This command does not change Machine or User policy.

**Stop:** MachinePolicy or UserPolicy is anything other than `Undefined`, or CurrentUser remains `Restricted` after the command.

**Recovery:** if a managed policy is set, send the list to the person who supports the computer and stop. Do not set `Bypass`, and do not change LocalMachine. If CurrentUser is still `Restricted` and no managed policy is set, run this block again in this window.

**Terminal: Windows PowerShell, ordinary user.**

```powershell
$report = Join-Path $attempt 'setup-report.txt'
if (Test-Path -LiteralPath $report) { throw 'STOP: the report path already exists. It was not overwritten.' }
& (Join-Path $M 'scripts\verify-setup.ps1') -Root $R -ResultsPath $report
Write-Output ('report exit ' + $LASTEXITCODE)
Write-Output $report
```

**Expected:** a report file path, and a last report line that begins `SETUP CHECK PASS` or `SETUP CHECK HOLD`. The report does not contain the key.

**Stop:** the script is blocked by execution policy, the report path already exists, or the report contains the key. A hold in this report is a prerequisite hold. It is not repaired by editing the proof file, and a pass in this report does not replace `TOOL PROOF PASS`.

**Recovery:** fix the first failed prerequisite named in the report, then run this report command again only after choosing a new report path if the old file exists. Do not reset, pull, or clean the checkout because the report mentions local changes. Continue to the lab only after the tool proof printed `TOOL PROOF PASS`.

The next work is the [Module 0 lab](../shared/MODULE_00_LAB.md). The pins are in [Course setup pins](../shared/VERSIONS.md), and the cited install pages are collected in [Primary setup sources](../shared/SOURCES.md). If you are working in Ubuntu on WSL instead of native Windows, use [Windows WSL 2 with Ubuntu setup](windows-wsl.md) from the start rather than mixing the two paths.
