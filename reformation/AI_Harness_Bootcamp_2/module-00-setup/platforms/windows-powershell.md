# Windows · PowerShell only

This path keeps the whole command-line course in native Windows PowerShell. Reserve 90–150 minutes on an unmanaged Windows 11 x64 laptop. A managed laptop can take longer because an administrator or IT owner may have to approve software.

Use this path only if you intend to stay in PowerShell for the course. If you want Linux command-line behavior on Windows, use [Windows with WSL](windows-wsl.md) instead.

## 1. Before you change the machine

Check the PowerShell version, operating system, architecture, administrator access, disk, network, and restart window before installing anything.

Every command in this path runs on Windows PowerShell 5.1 — the version that ships with Windows 11 and opens when you choose **Windows PowerShell** from Start — and on PowerShell 7.x if you have installed it. Nothing here needs a newer version than 5.1.

**Terminal: Windows PowerShell · normal user.**

```powershell
$PSVersionTable.PSVersion
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsBuildNumber, OsArchitecture
Get-PSDrive -Name C | Select-Object Used, Free
winget --version
```

**You should see:** in the first line's `Major` and `Minor` columns, either `5` and `1`, or a `Major` of `7` or higher with any `Minor`. Both run every command in this path, so continue with whichever one you have and do not install a newer PowerShell to satisfy this guide. `WindowsProductName` begins `Windows 11` and `OsArchitecture` reads `64-bit`. `Free` on the C drive is a byte count of at least `15000000000`, which is 15 GB. WinGet prints a version such as `v1.9.25200`. The official goose PowerShell installer currently supports Windows x86_64, not Windows ARM64.

**Stop here if:** `Major` is below `5`, or `Major` is `5` and `Minor` is below `1`, or the architecture is ARM64, free space is below 15 GB, WinGet is blocked, or you cannot approve software required by your organization. Use the [support packet](../shared/TROUBLESHOOTING.md) rather than changing security policy. On Windows ARM64, stop this path. Use the WSL guide only if its Linux tools support your ARM64 machine; otherwise use a supported x64 laptop.

Source: [Microsoft WinGet](https://learn.microsoft.com/en-us/windows/package-manager/winget/) and the official [goose Windows installer](https://raw.githubusercontent.com/aaif-goose/goose/main/download_cli.ps1).

## 2. Open the right terminal

Open **Windows PowerShell** from Start. Do not use Command Prompt, Git Bash, or a WSL tab for this path.

**Terminal: Windows PowerShell · normal user.**

```powershell
$Host.Name
$env:OS
```

**You should see:** `ConsoleHost` on the first line and `Windows_NT` on the second.

**Stop here if:** `$env:OS` is empty or the prompt is inside Ubuntu/WSL. Close it and open Windows PowerShell.

## 3. Install the base tools

WinGet installs the maintained Windows packages. Run each command separately so the first failure stays visible.

**Terminal: Windows PowerShell · normal user. Approve elevation only when Windows asks.**

Expect this to take 10 to 40 minutes on a normal connection. Each command prints a progress bar, then a short success line, and Windows may ask you to approve an installer. A minute of no visible change during a download is normal.

```powershell
winget install --exact --id Git.Git --source winget --accept-package-agreements --accept-source-agreements
winget install --exact --id OpenJS.NodeJS.LTS --source winget --accept-package-agreements --accept-source-agreements
winget install --exact --id Python.Python.3.12 --source winget --accept-package-agreements --accept-source-agreements
winget install --exact --id Microsoft.VCRedist.2015+.x64 --source winget --accept-package-agreements --accept-source-agreements
winget install --exact --id Obsidian.Obsidian --source winget --accept-package-agreements --accept-source-agreements
```

Close PowerShell and open a new PowerShell window before checking versions.

**Terminal: Windows PowerShell · normal user · new window.**

```powershell
git --version
node --version
npm --version
python --version
(Get-Command git,node,npm,python).Source
```

**You should see:** `git version 2.` followed by more digits, a Node version beginning `v24.`, an npm version number, `Python 3.12` or higher, and then four paths that each end in `.exe`.

Windows ships a placeholder named `python.exe` that opens the Microsoft Store instead of running Python. It sits in a folder called `WindowsApps` and is zero bytes long, so the path and the size tell you which one you have.

```powershell
$python = Get-Command python -CommandType Application -ErrorAction SilentlyContinue
$python.Source
if ($python) { (Get-Item -LiteralPath $python.Source).Length } else { 'python is not on PATH' }
```

**You should see:** a path like `C:\Users\you\AppData\Local\Programs\Python\Python312\python.exe` and a size of at least 90000 bytes.

**Stop here if:** the path contains `\WindowsApps\` or the size is `0`. That is the Store placeholder, not Python. Open **Settings › Apps › Advanced app settings › App execution aliases**, switch off the entries named `python.exe` and `python3.exe`, close PowerShell, open a new window, and run the check again.

**Stop here if:** Node is not 24.x, Python is below 3.12, a command is missing, or npm reports that scripts are disabled. If only npm reports that scripts are disabled, run `Get-ExecutionPolicy -List`. If `MachinePolicy` or `UserPolicy` has a value, the setting is controlled by IT. Stop and send them the output. Do not weaken it. If both are undefined and your organization permits it, use `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`; record the old value first and restore it after the course if it was course-only.

## 4. Put user tools on PATH

PATH is the list of folders Windows searches, in order, when you type a command name. The AI CLIs belong in folders your user owns, so their location stays on your PATH without an administrator install.

**Terminal: Windows PowerShell · normal user.**

```powershell
$npmPrefix = Join-Path $env:USERPROFILE '.npm-global'
New-Item -ItemType Directory -Force -Path $npmPrefix | Out-Null
npm config set prefix $npmPrefix

$userBin = Join-Path $env:USERPROFILE '.local\bin'
New-Item -ItemType Directory -Force -Path $userBin | Out-Null

$currentUserPath = [Environment]::GetEnvironmentVariable('Path','User')
$needed = @($npmPrefix, $userBin)
$parts = @($currentUserPath -split ';' | Where-Object { $_ })
foreach ($item in $needed) {
  if ($parts -notcontains $item) { $parts += $item }
}
[Environment]::SetEnvironmentVariable('Path', ($parts -join ';'), 'User')
$env:Path = (($needed + @($env:Path -split ';')) | Select-Object -Unique) -join ';'
```

**You should see:** no output at all from this block. Read the two settings back.

```powershell
npm config get prefix
Test-Path $userBin
```

**You should see:** `C:\Users\you\.npm-global`, with your own account name in place of `you`, then `True`.

**Stop here if:** npm reports a system directory or the user PATH cannot be changed because of policy. Capture the policy error. Do not switch to an elevated global npm install.

## 5. Clone and inspect the course

A clone is a local working copy with the repository's history. This step refuses to overwrite an existing folder.

**Terminal: Windows PowerShell · normal user.**

```powershell
$courseHome = Join-Path $env:USERPROFILE 'course'
$repo = Join-Path $courseHome 'AI_Harness_Bootcamp'
New-Item -ItemType Directory -Force -Path $courseHome | Out-Null
if (Test-Path -LiteralPath $repo) {
  throw "The destination already exists: $repo. Inspect it before renaming or reusing it."
}
git clone https://github.com/TheHolofex/AI_Harness_Bootcamp.git $repo
Set-Location $repo
git remote get-url origin
git rev-parse --short=12 HEAD
git status --short
```

**You should see:** the `TheHolofex/AI_Harness_Bootcamp` remote, a 12-character revision, and no output from `git status --short` on a clean clone.

**Stop here if:** the destination exists, the remote differs, the clone is incomplete, or status already shows changes. Do not delete an existing directory to make the command work.

## 6. Install the course applications

Install the exact OpenCode and n8n versions written below. A pinned version is what makes the result reproducible: the same command installs the same build tomorrow, and on the next machine. Codex and goose come from their official stable installers, which always serve the current release, so the report records whichever versions you receive.

**Terminal: Windows PowerShell · normal user.**

Expect this to take 5 to 20 minutes on a normal connection. npm prints a long stream of download lines and then a summary of the packages it added. Silence for a minute at a time is normal.

```powershell
npm install --global @openai/codex
npm install --global opencode-ai@1.18.17
npm install --global n8n@2.34.5
```

**You should see:** three summary lines of the form `added 214 packages in 31s`, one per install, and no line beginning `npm error`.

goose is installed by a PowerShell script published by its maintainers. PowerShell refuses to run any script file until your account's execution policy allows it, so check that setting first.

```powershell
Get-ExecutionPolicy -List
```

**You should see:** `Undefined` on the `MachinePolicy` and `UserPolicy` rows. On Windows PowerShell 5.1, `LocalMachine` usually reads `Restricted`. While `Restricted` is in force, PowerShell refuses to run any `.ps1` file, so the goose installer will not start.

**Stop here if:** `MachinePolicy` or `UserPolicy` shows anything other than `Undefined`. Your organization sets that value and you cannot change it from here. Send IT the output of `Get-ExecutionPolicy -List` and stop. Do not weaken a machine-wide setting.

If both are `Undefined` and your organization permits it, allow scripts for your own account only. The first line prints the value you are replacing, so write it down before you continue.

```powershell
Get-ExecutionPolicy -Scope CurrentUser
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
Get-ExecutionPolicy -Scope CurrentUser
```

**You should see:** the old value first — usually `Undefined` — then a confirmation question, which you answer `Y`, then `RemoteSigned`.

Now download the installer into a folder of its own, with a name nobody can predict, so nothing else can swap the file between the download and the run.

```powershell
$stage = Join-Path $env:TEMP ("goose-{0}" -f [Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $stage | Out-Null
$installer = Join-Path $stage 'download_cli.ps1'
Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/aaif-goose/goose/main/download_cli.ps1' -OutFile $installer
$installer
```

**You should see:** the full path of the downloaded file, inside a `goose-` folder under your temp directory.

Confirm the script names the `aaif-goose/goose` repository, that it downloads a Windows build, and that the architecture it selects is `x86_64`. Read it in the pager below: press the space bar for the next page, and press `Q` to leave the pager and return to the prompt.

```powershell
Get-Content -LiteralPath $installer | Out-Host -Paging
```

**You should see:** a PowerShell script whose download URL points at `github.com/aaif-goose/goose` and which names `windows` and `x86_64`.

**Stop here if:** the script names a different repository, a different architecture, or a download host you do not recognize. Delete the staging folder and use the [support packet](../shared/TROUBLESHOOTING.md).

Expect this to take 1 to 5 minutes. The installer prints a download line, then the path it installed goose to.

```powershell
$env:CONFIGURE = 'false'
& $installer
Remove-Item -LiteralPath $stage -Recurse -Force
```

**You should see:** a final line from the installer naming the file it wrote, ending `\.local\bin\goose.exe`.

```powershell
codex --version
opencode --version
goose --version
n8n --version
```

**You should see:** four version strings; OpenCode `1.18.17`; n8n `2.34.5`.

Open Obsidian from Start. Choose **Open folder as vault**, then select the course folder only for this setup check. You can close it after the vault opens.

**You should see:** `AI_Harness_Bootcamp` at the top of Obsidian's file pane, with `README.md` listed under it.

**Stop here if:** the goose installer reports ARM64, a missing DLL, or a different repository; a pinned version differs; Obsidian cannot open the folder; or any command resolves to an unexpected application. If goose exits with `0xC0000135`, repair the Microsoft Visual C++ runtime before changing goose.

Sources: [Codex CLI](https://developers.openai.com/codex/cli), [OpenCode installation](https://opencode.ai/docs/), [goose](https://github.com/aaif-goose/goose), [n8n npm requirements](https://docs.n8n.io/llms-full.txt), and [Obsidian](https://obsidian.md/download).

## 7. Connect the course accounts

Read [Connect the course accounts](../shared/CREDENTIALS.md) before entering a credential.

**Terminal: Windows PowerShell · normal user.**

```powershell
codex login
codex login status
```

**You should see:** a line from `codex login status` naming how you are signed in, such as `Logged in using ChatGPT`. Read that method and compare it with the one your cohort approved.

Copy and run the next line on its own, with nothing after it in the same paste. PowerShell hands whatever follows a prompt straight into that prompt, so a second pasted line would be stored as your key.

```powershell
$secure = Read-Host 'Paste the cohort XAI_API_KEY' -AsSecureString
```

**You should see:** the prompt text, and no characters as you paste the key.

```powershell
$ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
try { $env:XAI_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) }
finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
Remove-Variable secure
$env:GOOSE_PROVIDER = 'xai'
$env:GOOSE_MODEL = 'grok-4.5'
if ([string]::IsNullOrWhiteSpace($env:XAI_API_KEY)) { 'MISSING' } else { 'SET' }
```

**You should see:** `SET`. The key itself must not appear.

**Stop here if:** you are uncertain which account or model the cohort approved, login status shows the wrong method, or the key appeared in output or history. Revoke an exposed key before continuing.

## 8. Prove the setup

Check the local tools before making any request that may cost money. The report is saved outside the repository, and the repository must still be unchanged.

**Terminal: Windows PowerShell · normal user · repository root.**

The check is a PowerShell script file, so your account's execution policy has to allow scripts. The first line prints the policy actually in force; the second shows where it comes from.

```powershell
Get-ExecutionPolicy
Get-ExecutionPolicy -List
```

**You should see:** `RemoteSigned` on the first line, and `Undefined` for both `MachinePolicy` and `UserPolicy`.

**Stop here if:** the first line reads `Restricted`, or `MachinePolicy` or `UserPolicy` shows any value other than `Undefined`. A value on either of those two rows belongs to IT: send them the output of `Get-ExecutionPolicy -List` and stop, rather than weakening a machine-wide setting. If both are `Undefined` and the first line still reads `Restricted`, and your organization permits it, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` and record the old value so you can restore it after the course.

```powershell
Set-Location "$env:USERPROFILE\course\AI_Harness_Bootcamp"
$M0 = "reformation/AI_Harness_Bootcamp_2/module-00-setup"
& "$M0/scripts/verify-setup.ps1" -Root $PWD
```

**You should see:** `SETUP CHECK PASS` and a report under `%USERPROFILE%\course-evidence\module-00`.

**Stop here if:** the report ends with `SETUP CHECK HOLD`. Save its first failed check and use the [troubleshooting guide](../shared/TROUBLESHOOTING.md).

## 9. Repeat the proof in a fresh shell

Close every PowerShell and AI tool window, then open a new PowerShell window. Everything below runs in that one window.

**Terminal: Windows PowerShell · normal user · new window.**

```powershell
codex --version
opencode --version
goose --version
n8n --version
if ([string]::IsNullOrWhiteSpace($env:XAI_API_KEY)) { 'MISSING — expected in a fresh shell' } else { 'SET — investigate persistence' }
```

**You should see:** four version strings and `MISSING — expected in a fresh shell`. The key is entered per session on purpose.

Copy and run the next line on its own, with nothing after it in the same paste.

```powershell
$secure = Read-Host 'Paste the cohort XAI_API_KEY' -AsSecureString
```

**You should see:** the prompt text, and no characters as you paste the key.

```powershell
$ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
try { $env:XAI_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) }
finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
Remove-Variable secure
$env:GOOSE_PROVIDER = 'xai'
$env:GOOSE_MODEL = 'grok-4.5'
if ([string]::IsNullOrWhiteSpace($env:XAI_API_KEY)) { 'MISSING' } else { 'SET' }
```

**You should see:** `SET`.

```powershell
Set-Location "$env:USERPROFILE\course\AI_Harness_Bootcamp"
$M0 = "reformation/AI_Harness_Bootcamp_2/module-00-setup"
$run = Join-Path $env:USERPROFILE ("course-evidence\module-00\run-{0}" -f [Guid]::NewGuid().ToString("N"))
$proof = Join-Path $run 'proof'
New-Item -ItemType Directory -Path $proof | Out-Null
Set-Content -LiteralPath (Join-Path $env:USERPROFILE 'course-evidence\module-00\latest-run.txt') -Value $run
& "$M0/scripts/verify-setup.ps1" -Root $PWD -ResultsPath (Join-Path $run 'setup-report.txt')
```

**You should see:** `SETUP CHECK PASS` in this new window, and the path of the report it wrote.

Each of the three AI tools is now asked to write one file. The command below first makes a short random token and saves it, then puts that token in each request. A proof file counts only if it carries this run's token and was written after the token existed — which shows the file appeared during this run, not that a model rather than a person wrote it.

Expect this to take 1 to 5 minutes. Each tool prints its own progress and may pause for a while with no output while it works.

```powershell
Set-Location "$env:USERPROFILE\course\AI_Harness_Bootcamp"
$run = Get-Content -LiteralPath (Join-Path $env:USERPROFILE 'course-evidence\module-00\latest-run.txt')
$proof = Join-Path $run 'proof'
$token = python -c "import secrets; print(secrets.token_hex(4))"
Set-Content -LiteralPath (Join-Path $run 'run-token.txt') -Value $token
$token
Set-Location $proof
codex exec --sandbox workspace-write --skip-git-repo-check "Create a file named from-codex.txt whose only line is: codex works $token"
opencode run -m "xai/grok-4.5" "Create a file named from-opencode.txt in the current directory whose only line is: opencode works $token"
goose run --no-session --provider xai --model grok-4.5 -t "Create a file named from-goose.txt in the current directory whose only line is: goose works $token"
```

**You should see:** eight characters of the run token, for example `9f3c1ab2`, then each tool reporting that it created its file.

```powershell
Set-Location "$env:USERPROFILE\course\AI_Harness_Bootcamp"
$M0 = "reformation/AI_Harness_Bootcamp_2/module-00-setup"
$run = Get-Content -LiteralPath (Join-Path $env:USERPROFILE 'course-evidence\module-00\latest-run.txt')
python "$M0/shared/case/verify_tool_proof.py" (Join-Path $run 'proof') (Join-Path $run 'run-token.txt') | Tee-Object -FilePath (Join-Path $run 'tool-proof.txt')
```

**You should see:** one `PASS:` line for each of the three files, then `TOOL PROOF PASS`.

Start n8n in a second PowerShell window with `n8n start` and leave it running there. Back in this window:

```powershell
Set-Location "$env:USERPROFILE\course\AI_Harness_Bootcamp"
$M0 = "reformation/AI_Harness_Bootcamp_2/module-00-setup"
$run = Get-Content -LiteralPath (Join-Path $env:USERPROFILE 'course-evidence\module-00\latest-run.txt')
python "$M0/shared/case/verify_n8n.py" (Join-Path $run 'n8n.pass')
```

**You should see:** `PASS: n8n answered its health check at http://127.0.0.1:5678`.

Open Obsidian and choose **Open folder as vault**, then select `%USERPROFILE%\course\AI_Harness_Bootcamp`. Opening a folder as a vault makes Obsidian write a `.obsidian` folder inside it. Obsidian shows the number of files it indexed in the status bar at the bottom of the window; read that number and keep it in front of you.

```powershell
Set-Location "$env:USERPROFILE\course\AI_Harness_Bootcamp"
$run = Get-Content -LiteralPath (Join-Path $env:USERPROFILE 'course-evidence\module-00\latest-run.txt')
$marker = Join-Path $PWD '.obsidian'
if (-not (Test-Path -LiteralPath $marker)) { throw "Obsidian has not opened $PWD as a vault: there is no .obsidian folder here." }
$tracked = (git ls-files | Measure-Object).Count
$count = Read-Host 'File count from the Obsidian status bar'
if ($count -notmatch '^\d+$') { throw "Type digits only. PowerShell received: $count" }
if ([int]$count -lt [int]($tracked * 0.6) -or [int]$count -gt [int]($tracked * 1.4)) { throw "Obsidian reported $count files and Git tracks $tracked in this folder. Check which folder Obsidian opened." }
Set-Content -LiteralPath (Join-Path $run 'obsidian-observed.txt') -Value "vault=$((Get-Item -LiteralPath $PWD).Name)\.obsidian files=$count tracked=$tracked"
Get-Content -LiteralPath (Join-Path $run 'obsidian-observed.txt')
```

**You should see:** one line reading `vault=AI_Harness_Bootcamp\.obsidian files=` and the number you read from Obsidian, then `tracked=` and the number of files Git tracks in the clone. The two counts land close together; Obsidian does not index the hidden `.git` folder. The `.obsidian` folder proves Obsidian opened this clone, while the file count is a number you typed, so it proves only that what Obsidian displayed falls in the range this clone can produce.

Stop n8n in the second window with **Ctrl+C**.

**You should see:** in that second window, n8n stops printing and the PowerShell prompt returns, ending in `>`.

**Stop here if:** only the old window found a command, the fresh shell already contained the key, a proof file is wrong, the Obsidian block reported no `.obsidian` folder or refused the count you typed, or repository facts changed.

## 10. Save the setup record

Append the recorded results to the newest report outside Git.

**Terminal: Windows PowerShell · normal user.**

```powershell
Set-Location "$env:USERPROFILE\course\AI_Harness_Bootcamp"
$run = Get-Content -LiteralPath (Join-Path $env:USERPROFILE 'course-evidence\module-00\latest-run.txt') -ErrorAction Stop
$proofText = Get-Content -LiteralPath (Join-Path $run 'tool-proof.txt') -Raw -ErrorAction SilentlyContinue
$proofVerdict = @($proofText -split "\r?\n" | Where-Object { $_ -match 'TOOL PROOF' })[0]
if ($proofVerdict -ne 'TOOL PROOF PASS') { throw "The AI file-writing proof did not pass in $run" }
$n8n = Get-Content -LiteralPath (Join-Path $run 'n8n.pass') -ErrorAction SilentlyContinue
if ($n8n -ne 'PASS') { throw "The n8n health check did not pass in $run" }
$obsidian = ([string](Get-Content -LiteralPath (Join-Path $run 'obsidian-observed.txt') -Raw -ErrorAction SilentlyContinue)).Trim()
if ($obsidian -notmatch 'vault=AI_Harness_Bootcamp\\\.obsidian' -or $obsidian -notmatch 'files=\d+ tracked=\d+') { throw "No recorded Obsidian vault folder and file count in $run" }
$report = Get-Item -LiteralPath (Join-Path $run 'setup-report.txt')
@"
Setup path: Windows PowerShell only
Architecture: $env:PROCESSOR_ARCHITECTURE
New-terminal file-writing checks: $proofVerdict
Obsidian observed: $obsidian
n8n health check at 127.0.0.1:5678: $n8n
Target-platform execution: learner-run on this machine
"@ | Add-Content -LiteralPath $report.FullName
Get-Content -LiteralPath $report.FullName -Tail 7
```

**You should see:** the six lines you just appended, with no key, account identifier, or personal folder path among them.

**Stop here if:** the report includes a key, account identifier, internal host, or raw environment listing. Remove the exposed record and rotate a leaked key.

Setup is complete. Continue to the [shared Module 0 lab](../shared/MODULE_00_LAB.md).
