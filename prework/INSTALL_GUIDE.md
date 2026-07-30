# Install guide — student-owned workstation

Platform: **vanilla Windows 11**, 64-bit. **No WSL required.**
Authentication: **API keys only.** You will never sign into ChatGPT, Claude, or any monthly plan.

**Primary path:** the interactive checklist at `site/checklists/prework-install.html`. This file is the same content in printable form.

Plan two to four hours. Work in order — later sections depend on earlier ones. Keep `SETUP_LOG.md` open and record what broke and what fixed it.

> Staff issue you three API keys: OpenAI (`sk-proj-…`), xAI (`xai-…`), and Anthropic (`sk-ant-api03-…`).
> Sections 0–4 need no keys, so start installing even if your keys haven't arrived yet.

---

## 0. Baseline machine

```powershell
[Environment]::Is64BitOperatingSystem   # must be True
$env:PROCESSOR_ARCHITECTURE             # must be AMD64
```

- [ ] Windows 11, updated (`winver` — log the version)
- [ ] 64-bit, and **not ARM64**
- [ ] 25 GB or more free on C:
- [ ] You can approve an elevation prompt (Git, Node, and Codex's sandbox need one)

**ARM64 laptops cannot run this stack.** OpenCode fails to start on Windows ARM64 and goose ships no ARM build. Raise it with staff today.

**No admin rights?** Ticket IT immediately. This is the blocker that most reliably costs people their Monday.

---

## 1. Terminal and PowerShell

**You only need one shell: PowerShell.** Every command in this guide is typed into it. You will also install Git Bash, which is a different kind of terminal — but that is a dependency other tools reach for on their own, not a second thing for you to learn.

Open Windows Terminal as your **normal user** — not as administrator. Avoid the Start menu entry labelled *Windows PowerShell (x86)*; it is a 32-bit host and some installers refuse to run in it.

Windows ships three terminals that look similar, and commands are not interchangeable between them. Tell them apart by the prompt:

| Window | Prompt looks like | Use it for |
|---|---|---|
| **PowerShell** | `PS C:\Users\you>` — note the `PS` | Everything in this guide |
| Command Prompt | `C:\Users\you>` — no `PS` | Nothing here, unless a rescue step says so |
| Git Bash | `you@machine ~ $` — a `$`, and `/` in paths | One goose fallback in section 10 |

Confirm you are in the right one — a version number means PowerShell, an error means you are somewhere else:

```powershell
$PSVersionTable.PSVersion
```

Three errors later in this guide mean "wrong window" rather than "broken install":

| Error | Means |
|---|---|
| `'irm' is not recognized` | You are in Command Prompt, not PowerShell |
| `The token '&&' is not a valid statement separator` | A Command Prompt or Git Bash style command pasted into PowerShell |
| `A parameter cannot be found that matches parameter name 'fsSL'` | A Mac/Linux `curl` command pasted into PowerShell, where `curl` means something different. This is exactly what happens if you try OpenCode's website installer. |

```powershell
$PSVersionTable.PSVersion
```

Stock Windows 11 reports 5.1, which is enough for everything here. PowerShell 7 is optional; if you want it, force the MSI build:

```powershell
winget install --id Microsoft.PowerShell --source winget --installer-type wix --accept-source-agreements --accept-package-agreements
```

Allow scripts to run for your account — npm and several installers are scripts:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Get-ExecutionPolicy -List
```

- [ ] `CurrentUser` reads `RemoteSigned`
- [ ] `MachinePolicy` and `UserPolicy` both read `Undefined`

If either policy row is set, Group Policy overrides you and the command changes nothing regardless of what it reported. **Log the exact output and ticket IT.**

---

## 2. winget

```powershell
winget --version
winget source update --accept-source-agreements
```

Clearing the agreement now stops a later install appearing to hang while it waits for a keystroke you can't see.

If winget is missing, try in order, checking `winget --version` in a **new** window after each:

```powershell
Add-AppxPackage -RegisterByFamilyName -MainPackage Microsoft.DesktopAppInstaller_8wekyb3d8bbwe
```

```powershell
Install-PackageProvider -Name NuGet -Force | Out-Null
Install-Module -Name Microsoft.WinGet.Client -Force -Repository PSGallery | Out-Null
Repair-WinGetPackageManager -Force -Latest
```

If it still refuses, every tool below has a direct-download alternative. Note it and move on.

---

## 3. Git for Windows

Git also provides **Git Bash**, a second kind of terminal that some tools reach for behind the scenes — that is why Git comes this early.

**You type everything in PowerShell.** Git Bash is a dependency, not a second shell to get fluent in. Pi is the only tool that genuinely cannot run without it, and it calls it for you. The one time you would open Git Bash yourself is the goose install fallback in section 10.

```powershell
winget install --id Git.Git -e --source winget --scope machine --accept-source-agreements --accept-package-agreements
```

**Close the terminal and open a new one.** A terminal reads PATH once when it opens; your current window will insist Git isn't installed. This recurs after every install below.

```powershell
git --version
Test-Path "C:\Program Files\Git\bin\bash.exe"
```

- [ ] `git --version` answers
- [ ] Git Bash path recorded in your log

If `Test-Path` is `False`, Git installed per-user. Check `$env:LOCALAPPDATA\Programs\Git\bin\bash.exe` and log whichever is real.

---

## 4. Node.js and Python

```powershell
winget install --id OpenJS.NodeJS.LTS -e --source winget --accept-source-agreements --accept-package-agreements
winget install Python.Python.3.14 --accept-source-agreements --accept-package-agreements
```

**The `.LTS` suffix is not optional.** The package named plain `OpenJS.NodeJS` installs the newest experimental release, which is too new for n8n — it will refuse to start on Thursday and the error will not mention this step.

New terminal, then:

```powershell
node -v      # must be 22.22 or higher, and below 25
npm -v
python --version
(Get-Command python).Source
```

- [ ] Node inside 22.22–24.x (n8n needs 22.22+, Pi needs 22.19+)
- [ ] npm answers — if it fails with *"npm.ps1 cannot be loaded"*, that is the execution policy from section 1
- [ ] `python` resolves to a real install path, **not** one containing `\WindowsApps\`

A `\WindowsApps\` path means the Microsoft Store placeholder is intercepting the command. Turn it off: Settings → Apps → Advanced app settings → App execution aliases → switch off `python.exe` and `python3.exe`.

Wrong Node version? Fix it now:

```powershell
winget uninstall -e --id OpenJS.NodeJS
winget install -e --id OpenJS.NodeJS.LTS
```

---

## 5. Your three API keys

Read `site/keys.html` first. Then set each key. The `Read-Host` form keeps the secret out of your shell history:

```powershell
$key = Read-Host 'Paste OPENAI_API_KEY'
[Environment]::SetEnvironmentVariable('OPENAI_API_KEY', $key, 'User')
$env:OPENAI_API_KEY = $key
$key = $null
```

Repeat for `XAI_API_KEY` and `ANTHROPIC_API_KEY`.

Prefer this to `setx`, which truncates values past 1024 characters and leaves the key in your command history.

Close the terminal, open a **new** one, and verify:

```powershell
'OPENAI_API_KEY','XAI_API_KEY','ANTHROPIC_API_KEY' | ForEach-Object {
  '{0}: user={1} session={2}' -f $_,
    [Environment]::GetEnvironmentVariable($_,'User').Length,
    (Get-Item "env:$_" -EA SilentlyContinue).Value.Length
}
```

- [ ] Three lines, each with two matching non-zero numbers

Only lengths print, never the keys, so this is safe on a shared screen. `user=0` means it didn't save; `session=0` means this window predates the variable.

---

## 6. Smoke folder

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\Documents\HarnessBootcamp\prework-smoke"
```

Every tool below writes one uniquely named file here. **Chat output is a claim; a file in Explorer is evidence.** If the file isn't on disk, the tool did not pass, however confident its reply sounded.

---

## 7. Codex — home tool

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

Alternative if that is blocked and Node is present — use one method, never both:

```powershell
npm install -g @openai/codex
```

New terminal, then `codex --version`.

**Setting `OPENAI_API_KEY` is not enough on its own for Codex.** The variable only pre-fills its sign-in screen. Hand Codex the key once:

```powershell
$env:OPENAI_API_KEY | codex login --with-api-key
codex login status
```

The flag is `--with-api-key`. The older `--api-key` form appears in most guides online and has been retired.

Lock out ChatGPT sign-in so you can never be bounced to a screen you can't complete:

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex" | Out-Null
Add-Content -Path "$env:USERPROFILE\.codex\config.toml" -Value 'forced_login_method = "api"'
```

Run `codex` once to set up its sandbox and approve the elevation prompt. If your laptop blocks it (error `1385`), add to the same `config.toml`:

```toml
[windows]
sandbox = "unelevated"
```

Write proof:

```powershell
cd "$env:USERPROFILE\Documents\HarnessBootcamp\prework-smoke"
codex exec --sandbox workspace-write -a never "Create a file named from-codex.txt containing exactly the text: codex works"
Get-Content .\from-codex.txt
```

- [ ] `codex login status` reports API-key auth, not a ChatGPT account
- [ ] Sandbox mode logged (elevated or unelevated)
- [ ] `from-codex.txt` exists on disk

**Optional GUI:** the Codex graphical interface ships inside the **ChatGPT desktop app** for Windows — there is no separate product called "Codex app" to search for. On its signed-out screen choose *Sign in another way* and paste the key. Course instructions assume the command-line tool.

---

## 8. OpenCode — required second engine

P3 runs the **same frozen brief** through Codex and OpenCode, then you adjudicate. OpenCode runs on **Grok** via your xAI key. Without it, P3 has nothing to compare.

**Use the version staff pinned for your cohort.** OpenCode ships fast and its Windows support sometimes regresses between releases; staff test a build and pin it.

```powershell
winget install --id SST.opencode --exact --accept-package-agreements --accept-source-agreements
```

Alternative if winget lacks it and Node is present:

```powershell
npm install -g opencode-ai
```

**Do not use the `curl` install command from OpenCode's website.** It is a bash script and cannot run on plain Windows PowerShell; no PowerShell equivalent is published.

New terminal, then:

```powershell
opencode --version
opencode models xai --refresh
```

OpenCode reads `XAI_API_KEY` from the environment automatically — there is no login step. An empty model list means this window can't see the key.

Write proof — substitute the pinned model for `MODEL`:

```powershell
cd "$env:USERPROFILE\Documents\HarnessBootcamp\prework-smoke"
opencode run -m xai/MODEL "Create a file named from-opencode.txt in the current directory whose only contents are the text: opencode works"
Get-Content .\from-opencode.txt
```

- [ ] Version recorded in your log (Monday asks for it by name)
- [ ] `from-opencode.txt` exists on disk

If OpenCode reports success but no file appears, that is the known Windows defect. Record the version and exact wording and tell staff.

---

## 9. Pi — bare loop

Pi reads, writes, edits files and runs shell commands, and little else. You use it to watch a harness loop with nothing hidden. **It asks no permission before acting**, so keep it pointed at the smoke folder.

```powershell
powershell -c "irm https://pi.dev/install.ps1 | iex"
```

The installer is interactive — run it in a real terminal window. If it offers to install its own Node, answer **Y**; it won't disturb your existing install.

New terminal, then `pi --version`.

Pi can see all three keys, so **you must name the model** or it picks one you didn't expect and bills that provider:

```powershell
cd "$env:USERPROFILE\Documents\HarnessBootcamp\prework-smoke"
pi -p --model openai/MODEL "Create a file named from-pi.txt in the current directory containing exactly: pi works"
Get-Content .\from-pi.txt
```

There is no `-m` shorthand despite what several guides claim.

Then prove it can reach a shell. Pi only looks for Git Bash at the moment it first needs one, so a missing shell otherwise fails mid-exercise:

```powershell
pi -p --model openai/MODEL "Run the shell command 'echo bash-ok > bash-check.txt' and tell me the result"
Get-Content .\bash-check.txt
```

If it reports no bash shell found, create `%USERPROFILE%\.pi\agent\settings.json`:

```json
{ "shellPath": "C:\\Program Files\\Git\\bin\\bash.exe" }
```

Doubled backslashes are required.

- [ ] `from-pi.txt` exists on disk
- [ ] `bash-check.txt` exists on disk

---

## 10. goose — bounded, repeatable work

**Do not install goose with winget.** A winget package named *goose* is an unrelated database tool that shares the name. It installs cleanly and is the wrong program.

Turn off the Windows keyring **before** installing — goose defaults to Credential Manager, which fails often enough on managed laptops that its own docs tell you to decline it:

```powershell
[Environment]::SetEnvironmentVariable('GOOSE_DISABLE_KEYRING','1','User')
$env:GOOSE_DISABLE_KEYRING = '1'
```

goose only checks whether this variable *exists*, not what it says — setting it to `0` also disables the keyring. To re-enable, delete the variable.

Set provider and model so you never have to walk goose's provider list, which mixes API-key providers with subscription ones (ChatGPT Codex, GitHub Copilot, Cursor Agent) that need logins you don't have:

```powershell
[Environment]::SetEnvironmentVariable('GOOSE_PROVIDER','openai','User')
[Environment]::SetEnvironmentVariable('GOOSE_MODEL','MODEL','User')
$env:GOOSE_PROVIDER = 'openai'
$env:GOOSE_MODEL = 'MODEL'
```

Install:

```powershell
$env:CONFIGURE = "false"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/aaif-goose/goose/main/download_cli.ps1" -OutFile "download_cli.ps1"
.\download_cli.ps1
```

If PowerShell blocks the script: `powershell -ExecutionPolicy ByPass -File ".\download_cli.ps1"`

If execution policy is locked by Group Policy so neither form works, use the Git Bash path (you installed Git Bash in section 3). Open **Git Bash** and run:

```bash
curl -fsSL https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh | bash
```

The project moved to **`aaif-goose`**; older instructions pointing at `block/goose` fail or fetch a stale build. Current docs: <https://goose-docs.ai>

The installer does not add itself to PATH — it only warns:

```powershell
$userPath = [Environment]::GetEnvironmentVariable('PATH','User')
[Environment]::SetEnvironmentVariable('PATH', "$userPath;$env:USERPROFILE\.local\bin", 'User')
```

New terminal, then:

```powershell
goose --version
goose info -v
```

Write proof:

```powershell
cd "$env:USERPROFILE\Documents\HarnessBootcamp\prework-smoke"
$env:GOOSE_MODE = "auto"
goose run --no-session -t "Create a file named from-goose.txt in the current directory containing exactly the line: goose works"
Get-Content .\from-goose.txt
```

- [ ] `goose info -v` shows the provider and model you intended
- [ ] `from-goose.txt` exists on disk

---

## 11. Obsidian

```powershell
winget install -e --id Obsidian.Obsidian --scope user --accept-package-agreements --accept-source-agreements
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\Documents\HarnessBootcamp\vault"
```

Launch Obsidian, choose **Open folder as vault**, select that folder, click Open. No account is needed and none should be created.

```powershell
Get-ChildItem -Force "$env:USERPROFILE\Documents\HarnessBootcamp\vault"
```

- [ ] `.obsidian` folder present (the `-Force` reveals it; Explorer hides dot-folders)

---

## 12. n8n

Re-check Node first — n8n exits immediately on anything below 22.22:

```powershell
node -v
npm install n8n -g
n8n start
```

The install is slow, often several minutes with long silent stretches while antivirus scans each file. Let it finish.

Open <http://localhost:5678>.

**The first screen looks like a signup and is not one.** It creates an owner account in a database file on your own laptop. Nothing is transmitted, no verification email is sent, and it cannot be skipped. Use any email and a password of at least eight characters with a number and a capital letter — **write both down**, you need them Thursday.

Afterwards n8n offers a free licence key by email. **Skip it.** The course uses none of those features, and it is the only step that would contact n8n's servers.

Stop with `Ctrl+C`.

- [ ] UI loaded once, owner account created and recorded
- [ ] You know how to stop it

There is no n8n desktop app any more; the command line is the current path.

---

## 13. Course repo and operator pack

```powershell
cd "$env:USERPROFILE\Documents\HarnessBootcamp"
git clone https://github.com/TheHolofex/AI_Harness_Bootcamp.git
cd AI_Harness_Bootcamp
python -m http.server 8080
```

Open <http://localhost:8080/site/>. Stop with `Ctrl+C`.

- [ ] Repo cloned
- [ ] `operator/` copied into your working project (brief, log, pass bars, adversarial, measurement, transfer)
- [ ] Site serves locally

Protect your keys before your first commit. In any folder you'll commit from, `.gitignore` must contain at least:

```
.env
.env.*
*.key
auth.json
```

Then run `git status` and confirm none of those appear.

---

## 14. Optional — Claude Code

**Optional.** Skipping it does not affect your gate. OpenCode is the required second engine.

```powershell
irm https://claude.ai/install.ps1 | iex
```

New terminal, then `claude --version`. If not found:

```powershell
$userPath = [Environment]::GetEnvironmentVariable('PATH','User')
[Environment]::SetEnvironmentVariable('PATH', "$userPath;$env:USERPROFILE\.local\bin", 'User')
```

It reads `ANTHROPIC_API_KEY` on its own and asks you to approve the key once.

```powershell
cd "$env:USERPROFILE\Documents\HarnessBootcamp\prework-smoke"
claude --bare -p "Use the Write tool to create from-claude-optional.txt containing exactly: claude works" --allowedTools "Write"
Get-Content .\from-claude-optional.txt
```

Use the command-line tool, **not** the Claude desktop app — the desktop app's Code tab requires a subscription and will not accept your key.

---

## 15. Health check gate

```powershell
Get-ChildItem "$env:USERPROFILE\Documents\HarnessBootcamp\prework-smoke\from-*.txt"
```

- [ ] `from-codex.txt`, `from-opencode.txt`, `from-pi.txt`, `from-goose.txt` all present

Then work `HEALTH_CHECK.md` or `site/checklists/prework-health.html` end to end and declare GREEN, YELLOW, or RED.

---

## Rescue paths

| Symptom | Cause | Fix |
|---|---|---|
| A command that should work doesn't | Wrong terminal | Run `$PSVersionTable.PSVersion`. A version means PowerShell; an error means Command Prompt or Git Bash. See the table in section 1. |
| `'x' is not recognized` after a clean install | Terminal read PATH when it opened | Close **every** terminal, open a new one. Nine times in ten this is it. |
| Still not recognized after two new windows | Installer didn't update PATH | Add the tool's folder (usually `%USERPROFILE%\.local\bin`) to User PATH |
| `running scripts is disabled on this system` | Execution policy | Section 1. If `MachinePolicy`/`UserPolicy` are set, IT owns it — ticket them. Stopgap: `cmd /c npm install n8n -g` |
| Tool won't authenticate | Key missing in this window, wrong prefix, or wrong key for that tool | Re-run the section 5 check; confirm prefix; Codex additionally needs `codex login --with-api-key` |
| Worked yesterday, now `429` / quota / spend limit | Key hit its cap | Staff fix, not a reinstall. Message them with the key and what you ran. |
| Tool claims it wrote a file that isn't there | Believe the folder, not the chat | `Get-Location`, `Get-ChildItem`. On OpenCode this is a known Windows defect — report version and exact wording. |
| goose installed but is a database tool | winget package name collision | Uninstall it; use the `aaif-goose` installer in section 10 |
| Pi: "no bash shell found" mid-exercise | Git Bash not found | Set `shellPath` in `%USERPROFILE%\.pi\agent\settings.json` |
| n8n exits on startup with a version message | Node outside 22.22–24.x | Reinstall with the `.LTS` package id |
| Stuck 30 minutes on one step | — | Post the step number, exact error, and what you tried. Move to the next section; most are independent. |

---

## Identity lock

The goal is not a pretty install. The goal is that **you can rebuild this chair** — you know where each tool keeps its credentials, what its boundaries are, and how it fails — and that you have a trail of what broke.

A recorded failure is evidence, not shame.
