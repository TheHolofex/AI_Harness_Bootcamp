# Install guide — student-owned workstation

Platform: **vanilla Windows 11**, 64-bit. **No WSL required.**
Authentication: **API keys only.** You will never sign into ChatGPT, Claude, or any monthly plan.

**Primary path:** the interactive checklist at `site/checklists/prework-install.html`. This file is the same content in printable form.

Plan two to four hours. Work in order — later sections depend on earlier ones. **Verify at the end of each section before you move on** (fresh terminal after anything that changes PATH). There is no separate health-check pass afterward. Keep `SETUP_LOG.md` open and record what broke and what fixed it. Monday’s install clinic re-runs these same verifies with help on hand.

> You'll be issued three API keys: OpenAI (`sk-proj-…`), xAI (`xai-…`), and Anthropic (`sk-ant-api03-…`).
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

**ARM64 laptops cannot run this stack.** OpenCode fails to start on Windows ARM64 and goose ships no ARM build. Flag it in the pre-work channel today — it isn't something you can fix from your seat.

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

Read `site/keys.html` first. Then set each key in turn. The `Read-Host` form prompts you to paste the key rather than putting it in the command, which keeps the secret out of your shell history:

```powershell
$key = Read-Host 'Paste OPENAI_API_KEY'
[Environment]::SetEnvironmentVariable('OPENAI_API_KEY', $key, 'User')
$env:OPENAI_API_KEY = $key
$key = $null
```

```powershell
$key = Read-Host 'Paste XAI_API_KEY'
[Environment]::SetEnvironmentVariable('XAI_API_KEY', $key, 'User')
$env:XAI_API_KEY = $key
$key = $null
```

```powershell
$key = Read-Host 'Paste ANTHROPIC_API_KEY'
[Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', $key, 'User')
$env:ANTHROPIC_API_KEY = $key
$key = $null
```

In each block, line two saves the key permanently for your Windows account, and line three sets it in this window too, so you can keep working without reopening anything. The xAI key is the one that drives OpenCode — check it starts with `xai-` before you paste, because mixing up two keys produces an authentication error that never tells you which key was wrong.

Prefer this to `setx`, which truncates values past 1024 characters and leaves the key in your command history.

### Model ids

A model id per provider should be posted in the pre-work channel. Set them once here and every later step picks them up — otherwise you would be hand-editing four commands further down.

If nothing has been posted yet, ask in the channel rather than saving a placeholder. If you use a current model id temporarily, replace it with the cohort pin before the write proofs — these are two variables you can change in ten seconds later, not a decision you're locked into.

Change the two quoted values to the ids you're using, then run all four lines:

```powershell
$env:HB_OPENAI_MODEL = 'paste the OpenAI model id'
$env:HB_XAI_MODEL    = 'paste the xAI model id'
[Environment]::SetEnvironmentVariable('HB_OPENAI_MODEL', $env:HB_OPENAI_MODEL, 'User')
[Environment]::SetEnvironmentVariable('HB_XAI_MODEL',    $env:HB_XAI_MODEL,    'User')
```

The first two lines set them for this window, the last two make them stick for every future one. These two values are the only thing in this guide you type rather than paste. The `HB_` prefix keeps them from colliding with anything a tool reads on its own.

Close the terminal, open a **new** one, and verify:

```powershell
'OPENAI_API_KEY','XAI_API_KEY','ANTHROPIC_API_KEY' | ForEach-Object {
  '{0}: user={1} session={2}' -f $_,
    ([string][Environment]::GetEnvironmentVariable($_,'User')).Length,
    ([string](Get-Item "env:$_" -EA SilentlyContinue).Value).Length
}
```

- [ ] Three lines, each with two matching non-zero numbers

Only lengths print, never the keys, so this is safe on a shared screen. `user=0` means it didn't save; `session=0` means this window predates the variable.

Model ids are not secret, so check those by eye:

```powershell
'HB_OPENAI_MODEL','HB_XAI_MODEL' | ForEach-Object {
  '{0} = {1}' -f $_, [Environment]::GetEnvironmentVariable($_,'User')
}
```

- [ ] Both read back the ids from the channel, not the words `paste the...`

If either id is unknown, leave that variable unset until staff posts a real id. Never save an empty value or the words `paste the...`; the tools will otherwise fail later with a blank model and the error will look like authentication trouble.

---

## 6. Smoke folder

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\Documents\HarnessBootcamp\prework-smoke"
```

Every tool below writes one uniquely named file here. **Chat output is a claim; a file in Explorer is evidence.** If the file isn't on disk, the tool did not pass, however confident its reply sounded.

---

## 7. Codex — home tool

Codex is not a separate download. It is a mode inside the **ChatGPT desktop app**, alongside Chat and Work. When the course says **"the Codex app,"** that is what it means: the ChatGPT desktop app, switched to Codex. You work in a window all week — no terminal for Codex at all.

Install it with the web installer at **get.microsoft.com/installer/download/9PLM9XGG6VKS**, or from PowerShell:

```powershell
winget install --id 9PLM9XGG6VKS -s msstore
```

The package is Store-signed, so Store components may flash past during install. You do not need to browse the Store yourself or sign into a Microsoft account. If your laptop blocks Microsoft's distribution service outright, there is a direct package — see the rescue table at the end.

Launch it. You land on a signed-out screen offering to sign in with a ChatGPT account — which you do not have and will not use.

**Choose *Sign in another way* instead**, paste your OpenAI key, and select *Continue*. That is the whole authentication step. Unlike most tools in this stack, setting `OPENAI_API_KEY` does nothing for the app; it reads the key you paste, not the variable.

Confirm it took: open the profile menu, which should report that you are on an API key rather than an account.

Now lock the door behind you, so a stray click can never bounce you to a ChatGPT login you cannot complete:

```powershell
$cfg = "$env:USERPROFILE\.codex\config.toml"
New-Item -ItemType Directory -Force -Path (Split-Path $cfg) | Out-Null
$keep = @(if (Test-Path $cfg) { Get-Content $cfg | Where-Object { $_ -notmatch '^\s*forced_login_method\s*=' } })
Set-Content -Path $cfg -Value (@('forced_login_method = "api"') + $keep)
```

Restart the app after writing that line.

Four lines rather than one, because this file has a shape you have to respect. In a TOML file, a line like `[windows]` opens a **table**, and every plain setting below it belongs to that table until the next one. So a setting appended to the bottom of a file that already has a table header stops being a top-level setting — it silently joins the table and stops doing its job. Nothing errors; the app just keeps asking you to sign in. Writing a second copy of the same key is a hard parse error instead.

The commands above sidestep both: they drop any existing `forced_login_method` line and rewrite the setting at the **top**, above every table. That makes them safe to re-run whenever you want to confirm the lock is in place — which the rescue table at the end of this guide will ask you to do.

### Point it at your smoke folder

Open the smoke folder you made in section 6 as a project — *Open project*, then pick `Documents\HarnessBootcamp\prework-smoke`.

The folder you open is the boundary. Codex reads and writes inside it and asks permission before reaching anywhere else, which is the whole idea you will spend the week learning to control.

### Set the permission mode

Beneath the message box is a permissions control. Set it to **Ask for approval**.

This is the setting that turns the Windows sandbox on, so do not skip it. On first use the app builds that sandbox and asks for an administrator prompt. Approve it — this is the strong `elevated` sandbox, and it is the one you want.

If your laptop refuses the elevation, or you see an error mentioning `1385`, Codex can fall back to weaker but workable boundaries. Add this to the **bottom** of the same `config.toml`, in a text editor — it is file content rather than a command to paste into PowerShell:

```toml
[windows]
sandbox = "unelevated"
```

That is a table header, so it has to be the last thing in the file — see the note above. If you later re-run the four-line command, it rewrites the top of the file and leaves this table where it is.

Write down which mode you ended up on. It is one of the two details worth having to hand when a machine behaves oddly mid-week.

### Write proof

In the chat box, ask for the file in plain language:

```text
Create a file named from-codex.txt in this folder containing exactly the text: codex works
```

Approve the write when it asks. Then look in Explorer.

**Chat output is a claim; the file in Explorer is the evidence.** A confident "I've created that for you" with no file on disk is a fail, and catching that difference is the first operator habit this course builds.

- [ ] Profile menu reports API-key sign-in, not a ChatGPT account
- [ ] Permission mode set to **Ask for approval**
- [ ] Sandbox mode logged (elevated or unelevated)
- [ ] `from-codex.txt` exists on disk

**What your key does not buy.** An API key runs the app's local work — projects, worktrees, code review, skills, scheduled tasks, the built-in browser. It does not unlock the cloud half of the product: Codex cloud, Sites, GitHub and Slack delegation, and voice all need a ChatGPT subscription. Nothing in this course needs them.

---

## 8. OpenCode — required second engine

P3 runs the **same frozen brief** through Codex and OpenCode, then you adjudicate. P5 uses it again to compare how a second harness expresses permissions. OpenCode runs on **Grok** via your xAI key, so the two engines differ underneath and not just in name. Without it, P3 has nothing to compare.

**Check the pre-work channel for a pinned build before you install.** OpenCode ships fast and its Windows support sometimes regresses between releases, which is why a cohort is better off on one known build than on whatever is newest that day. A pin names two things — a **channel** and a **version** — because winget and npm publish this tool on their own schedules and are usually a few releases apart. A version number without a channel doesn't identify a build.

If there is a pin, run **only** the line for the channel it names, substituting the version:

```powershell
# channel: winget
winget install --id SST.opencode --exact --version <pinned version> --accept-package-agreements --accept-source-agreements
```

```powershell
# channel: npm  — needs Node from section 4
npm install -g opencode-ai@<pinned version>
```

If there's no pin, don't stall on it. Install from winget without the `--version` flag:

```powershell
winget install --id SST.opencode --exact --accept-package-agreements --accept-source-agreements
```

Then write down the channel and the exact version you landed on and post it in the channel. Two people comparing notes is how the pin usually gets settled, and being able to say "I'm on winget 1.18.7" is what makes your result mean something on Tuesday. You may end up switching builds later; that's a two-minute reinstall, not a redo of this section.

**Do not use the `curl` install command from OpenCode's website.** It is a bash script and cannot run on plain Windows PowerShell; no PowerShell equivalent is published.

New terminal, then:

```powershell
opencode --version
opencode models xai --refresh
```

OpenCode reads `XAI_API_KEY` from the environment automatically — there is no login step. An empty model list means this window can't see the key.

If you installed against a pin, `opencode --version` should print that version exactly. If it prints anything else — higher or lower — an older install is probably still on PATH, or the other channel got used. Record both numbers in your log and mention it, rather than quietly upgrading to whatever is current. With no pin, whatever it prints is your answer; just write it down.

**Keep this engine independent.** When OpenCode finds Claude Code's files it reads them: `~/.claude/CLAUDE.md` and any `.claude/skills` folder. If you add Claude Code in section 14, your second engine quietly starts working from the first one's notes, and two engines sharing one memory file will agree more than they should. Turn that off:

```powershell
[Environment]::SetEnvironmentVariable("OPENCODE_DISABLE_CLAUDE_CODE", "1", "User")
$env:OPENCODE_DISABLE_CLAUDE_CODE = "1"
```

Two lines because they do different jobs. The first makes the setting stick for every window you open from now on; it does **not** reach the window you are in. The second applies it here, so the write proof below and anything else you do in this window are covered too.

New terminal, then check it took:

```powershell
$env:OPENCODE_DISABLE_CLAUDE_CODE
```

You want `1` back. A blank line means it didn't stick — set it again and note it in your log.

Write proof — this uses the xAI model id you set in section 5:

```powershell
cd "$env:USERPROFILE\Documents\HarnessBootcamp\prework-smoke"
opencode run -m "xai/$env:HB_XAI_MODEL" "Create a file named from-opencode.txt in the current directory whose only contents are the text: opencode works"
Get-Content .\from-opencode.txt
```

- [ ] Channel and version recorded in your log — matching the pin if there is one (Monday asks for both by name)
- [ ] `$env:OPENCODE_DISABLE_CLAUDE_CODE` returns `1` in a new terminal
- [ ] `from-opencode.txt` exists on disk

If OpenCode reports success but no file appears, that is the known Windows defect. Record the version and exact wording and post it — it's useful to the whole cohort, not just to you.

---

## 9. Pi — the harness you extend

[Pi](https://pi.dev) is a **minimal agent harness**: a small default configuration sitting on a large set of seams you can open. Out of the box it is read, write, edit, bash and a clean terminal UI — you can see the whole loop. Underneath sit skills, prompt templates, TypeScript extensions with a 33-event lifecycle, tree-shaped sessions you can branch, 15+ providers with mid-session model switching, and four run modes (interactive, print/JSON, RPC, embedded SDK).

The features you might expect to find missing — approval gates, plan mode, sub-agents — are missing on purpose, because they are yours to build. That is why Pi is in this course: every other tool asks you to configure a harness someone else designed, and this one hands you the parts. You will build some of them during the week.

**It has no guardrails out of the box, and the detail people get wrong matters.** Pi runs with exactly your permissions: no sandbox, no approval prompt, and **no working-directory fence**. Being "in" the smoke folder is a convention you keep, not a boundary Pi enforces — an absolute path or a `~` reaches anything your Windows account can reach, including SSH keys and saved credentials. Shell commands have no default timeout either.

Pi's docs say so plainly and explain why: a partial in-process sandbox *"would be easy to misunderstand as a security boundary while still depending on the host shell, filesystem, package managers, credentials, and extension code."* Real isolation has to come from the OS or a container. That is a sharper lesson about security theatre than most security training.

For pre-work: small, specific tasks inside the smoke folder; read what it proposes; don't leave it unattended. Do not use `/share` on work material — it uploads the whole session, system prompt and tool results included, to a public-by-URL gist. Do not install third-party Pi packages this week unless one has been named for the course; package code runs with full access to your machine.

```powershell
powershell -c "irm https://pi.dev/install.ps1 | iex"
```

The installer is interactive — run it in a real terminal window. If it offers to install its own Node, answer **Y**; it won't disturb your existing install.

New terminal, then `pi --version`.

Pi can see all three keys, so **you must name the model** or it picks one you didn't expect and bills that provider:

```powershell
cd "$env:USERPROFILE\Documents\HarnessBootcamp\prework-smoke"
pi -p --model "openai/$env:HB_OPENAI_MODEL" "Create a file named from-pi.txt in the current directory containing exactly: pi works"
Get-Content .\from-pi.txt
```

There is no `-m` shorthand despite what several guides claim.

Then prove it can reach a shell. Pi only looks for Git Bash at the moment it first needs one, so a missing shell otherwise fails mid-exercise:

```powershell
pi -p --model "openai/$env:HB_OPENAI_MODEL" "Run the shell command 'echo bash-ok > bash-check.txt' and tell me the result"
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

## 10. goose — local agent with recipe, tools, mode, and schedule

[goose](https://goose-docs.ai) is a **local-first agent platform** (CLI required for this course; Desktop optional). Thursday you will use it as the vehicle for an autonomy contract. The product is larger than “a chat that can write files.” Keep this shape in mind:

```text
goose = loop + packaged recipe + tool surface (extensions) + autonomy dial (mode / max turns) + unattended path (schedule / retry)
```

Pre-work only proves install and one write. The four levers — recipe, extensions, `GOOSE_MODE`, schedule — are what fill the **tool-enforced** column of Thursday’s contract. Docs: <https://goose-docs.ai>. Course default is the **CLI**; Desktop adds a recipe library and Scheduler UI if you want it later.

**Do not install goose with winget.** A winget package named *goose* is an unrelated database tool that shares the name. It installs cleanly and is the wrong program.

Goose's Windows executable also needs the Microsoft Visual C++ 2015+ x64 runtime. The Goose download contains `goose.exe` only; it does not install the runtime, and Python's bundled DLLs are not a substitute. Install this before the Goose CLI:

```powershell
winget install `
  --id "Microsoft.VCRedist.2015+.x64" `
  --exact `
  --source winget `
  --accept-source-agreements `
  --accept-package-agreements
```

If winget cannot install it, download Microsoft's x64 installer directly: <https://aka.ms/vs/17/release/vc_redist.x64.exe>. Run it, choosing **Install** or **Repair** if it is already present. Do not download individual DLL files from an untrusted site.

Turn off the Windows keyring **before** installing — goose defaults to Credential Manager, which fails often enough on managed laptops that its own docs tell you to decline it:

```powershell
[Environment]::SetEnvironmentVariable('GOOSE_DISABLE_KEYRING','1','User')
$env:GOOSE_DISABLE_KEYRING = '1'
```

goose only checks whether this variable *exists*, not what it says — setting it to `0` also disables the keyring. To re-enable, delete the variable.

Set provider and model so you never have to walk goose's provider list, which mixes API-key providers with subscription ones (ChatGPT Codex, GitHub Copilot, Cursor Agent) that need logins you don't have:

```powershell
if ([string]::IsNullOrWhiteSpace($env:HB_OPENAI_MODEL) -or $env:HB_OPENAI_MODEL -like 'paste *') {
  throw 'HB_OPENAI_MODEL is empty. Complete section 5 with a real model id, then open a new PowerShell window.'
}
[Environment]::SetEnvironmentVariable('GOOSE_PROVIDER','openai','User')
[Environment]::SetEnvironmentVariable('GOOSE_MODEL',$env:HB_OPENAI_MODEL,'User')
$env:GOOSE_PROVIDER = 'openai'
$env:GOOSE_MODEL = $env:HB_OPENAI_MODEL
```

Install:

```powershell
cd "$env:USERPROFILE\Downloads"
$env:CONFIGURE = "false"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/aaif-goose/goose/main/download_cli.ps1" -OutFile "download_cli.ps1"
.\download_cli.ps1
```

The `cd` matters only because the installer downloads into whatever folder you are standing in, and the last section left you in the smoke folder. Keep that one for evidence files.

If PowerShell blocks the script: `powershell -ExecutionPolicy ByPass -File ".\download_cli.ps1"`

If execution policy is locked by Group Policy so neither form works, use the Git Bash path (you installed Git Bash in section 3). Open **Git Bash** and run:

```bash
curl -fsSL https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh | bash
```

The project moved to **`aaif-goose`**; older instructions pointing at `block/goose` fail or fetch a stale build. Current docs: <https://goose-docs.ai>

The installer does not add itself to PATH — it only warns:

```powershell
$bin = "$env:USERPROFILE\.local\bin"
$userPath = [Environment]::GetEnvironmentVariable('PATH','User')
if (($userPath -split ';') -notcontains $bin) {
  [Environment]::SetEnvironmentVariable('PATH', "$userPath;$bin".Trim(';'), 'User')
}
```

The `if` is there because this exact folder comes up again in section 14, and PATH is a list you append to rather than a value you set. Without the guard, running it twice leaves the same folder in your PATH twice — harmless today, confusing the first time you have to read it. Note that this reads and writes **your** user PATH only; it never touches the system one.

Close every PowerShell window and open a new one, then run:

```powershell
Get-Command goose -All
where.exe MSVCP140.dll
goose --version
goose info -v
```

`Get-Command goose -All` should point at the `aaif-goose` executable, and `where.exe MSVCP140.dll` should print a Windows runtime path. If the DLL lookup prints nothing, the runtime install did not complete. `goose --version` must return a version before you continue; `goose info -v` must show the provider and model you intended.

Write proof. `GOOSE_MODE=auto` skips per-action approval so the smoke test can finish unattended — on Thursday you will deliberately dial this (often to `approve`) as a **tool-enforced** contract row:

```powershell
cd "$env:USERPROFILE\Documents\HarnessBootcamp\prework-smoke"
$env:GOOSE_MODE = "auto"
goose run --no-session -t "Create a file named from-goose.txt in the current directory containing exactly the line: goose works"
Get-Content .\from-goose.txt
```

- [ ] `goose info -v` shows the provider and model you intended
- [ ] `from-goose.txt` exists on disk
- [ ] You know Thursday’s pack lives at `mission_flesh/p6/` (`watch_officer.yaml` + recipe notes) once the course repo is cloned

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
```

The operator templates — brief, log, pass bars, adversarial prompt, measurement spine, transfer file — belong wherever you are actually working, not in a folder you downloaded and forgot. Right now that is the smoke folder, because it is the project you opened in the Codex app in section 7:

```powershell
Copy-Item -Recurse -Force `
  "$env:USERPROFILE\Documents\HarnessBootcamp\AI_Harness_Bootcamp\operator" `
  "$env:USERPROFILE\Documents\HarnessBootcamp\prework-smoke\"
Get-ChildItem "$env:USERPROFILE\Documents\HarnessBootcamp\prework-smoke\operator"
```

When you open a mission folder as a project during the week, bring `operator/` with you the same way.

**This copy is a rehearsal, not your Monday workspace.** Monday you open the cloned repo itself as your Codex project, and the `operator/` inside it is the one you actually fill in. Anything you type into the smoke folder's copy between now and then stays behind — so read these templates here, and save the writing for Monday.

Now serve the site. This one keeps running until you stop it:

```powershell
cd "$env:USERPROFILE\Documents\HarnessBootcamp\AI_Harness_Bootcamp"
python -m http.server 8080
```

Open <http://localhost:8080/site/>. Stop with `Ctrl+C`.

- [ ] Repo cloned
- [ ] `operator/` now listed inside `prework-smoke`
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

If you do install it, the `OPENCODE_DISABLE_CLAUDE_CODE` variable from step 8 is what keeps the two apart. Claude Code writes a `CLAUDE.md` that OpenCode would otherwise read as its own standing instructions.

```powershell
irm https://claude.ai/install.ps1 | iex
```

New terminal, then `claude --version`. If not found, it installed to the same `%USERPROFILE%\.local\bin` that goose uses — re-run the guarded PATH block from section 10, which is safe whether or not that folder is already there.

It reads `ANTHROPIC_API_KEY` on its own and asks you to approve the key once.

```powershell
cd "$env:USERPROFILE\Documents\HarnessBootcamp\prework-smoke"
claude --bare -p "Use the Write tool to create from-claude-optional.txt containing exactly: claude works" --allowedTools "Write"
Get-Content .\from-claude-optional.txt
```

Use the command-line tool, **not** the Claude desktop app — the desktop app's Code tab requires a subscription and will not accept your key.

---

## 14b. Optional — local model (non-blocking stretch prep)

**Skip freely.** This is **not** required for Monday GREEN, the install clinic, or course pass. It only saves time if you want Thursday’s **endpoint wall** stretch (`mission_flesh/p6/local_endpoint_notes.md`).

A **model pin** (tag + minimum RAM) may be posted in the channel. If one is, use it — these downloads are several gigabytes, and picking your own tag on hotel Wi‑Fi is how you spend an evening on a model your laptop can't hold. If none appears, ask before pulling anything large.

1. Install Ollama — it is the path here, and LM Studio is only for a pin that names it:

   ```powershell
   winget install -e --id Ollama.Ollama --accept-package-agreements --accept-source-agreements
   ```

   Without winget, download the Windows installer from [ollama.com](https://ollama.com) and accept the defaults. If the pin names [LM Studio](https://lmstudio.ai) instead, install it from that page.
2. New PowerShell: `ollama --version`. LM Studio has no version command — start its local server instead (the **Developer** tab, or `lms server start`) and confirm it reports listening, usually on `http://localhost:1234`.
3. Once you have a tag, set it once and pull it:

   ```powershell
   $env:HB_LOCAL_MODEL = 'paste the tag from the LOCAL PIN line'
   [Environment]::SetEnvironmentVariable('HB_LOCAL_MODEL', $env:HB_LOCAL_MODEL, 'User')
   ollama pull $env:HB_LOCAL_MODEL
   ```
4. Smoke: `ollama run $env:HB_LOCAL_MODEL "Reply with exactly: local-brain-ok"`.
5. On LM Studio: set the same variable, download **only** the pinned tag, load it so the running server is not empty, and send `Reply with exactly: local-brain-ok` in the chat pane.
6. Note free RAM and whether the smoke worked in your setup log.

If pull fails or the machine thrashes, stop and write YELLOW. Cloud goose remains the Thursday floor.

---

## 15. Pack for Monday (final roll-up)

You already verified each tool when you installed it. This section only gathers the evidence in one place for the Monday clinic.

```powershell
Get-ChildItem "$env:USERPROFILE\Documents\HarnessBootcamp\prework-smoke\from-*.txt"
```

- [ ] `from-codex.txt`, `from-opencode.txt`, `from-pi.txt`, `from-goose.txt` all present in Explorer
- [ ] Setup log has at least one real failure and fix
- [ ] OpenCode version and Codex sandbox mode written in the log
- [ ] You know which step, if any, is still yellow — and what you will try in clinic

One more thing to carry: the course repo from section 13. Monday morning you open `%USERPROFILE%\Documents\HarnessBootcamp\AI_Harness_Bootcamp` as your Codex app project — the week's missions read from `operator/` and `mission_flesh/` inside it, and the smoke folder was install proof only. If the clone never happened, run section 13 before Monday, or make it your first fix in clinic.

There is **no separate health-check checklist** to run. If something fails later, re-run that section’s verify. Optional full re-test sheet (rescue only): `HEALTH_CHECK.md`.

---

## Rescue paths

| Symptom | Cause | Fix |
|---|---|---|
| A command that should work doesn't | Wrong terminal | Run `$PSVersionTable.PSVersion`. A version means PowerShell; an error means Command Prompt or Git Bash. See the table in section 1. |
| `'x' is not recognized` after a clean install | Terminal read PATH when it opened | Close **every** terminal, open a new one. Nine times in ten this is it. |
| Still not recognized after two new windows | Installer didn't update PATH | Add the tool's folder (usually `%USERPROFILE%\.local\bin`) to User PATH |
| `running scripts is disabled on this system` | Execution policy | Section 1. If `MachinePolicy`/`UserPolicy` are set, IT owns it — ticket them. Stopgap: `cmd /c npm install n8n -g` |
| Tool won't authenticate | Key missing in this window, wrong prefix, or wrong key for that tool | Re-run the section 5 check; confirm prefix. The Codex app is the exception — it ignores the variable entirely and uses the key you pasted into *Sign in another way*. |
| Codex app keeps asking you to sign in with ChatGPT | It was signed in to an account, or the key was never accepted | Profile menu → log out, then sign back in via *Sign in another way*. Confirm `forced_login_method = "api"` sits in `%USERPROFILE%\.codex\config.toml` **above** any `[table]` header — re-running section 7's four-line command puts it there safely — then restart the app. |
| Codex app won't install — Store or `winget ... msstore` blocked | Group Policy blocks Microsoft app distribution | Download the Store-signed package directly: `https://persistent.oaistatic.com/codex-app-prod/ChatGPT-x64.msix`, then `Add-AppxPackage .\ChatGPT-x64.msix`. There is no plain MSI or EXE. If that is blocked too, it is an IT ticket. |
| Worked yesterday, now `429` / quota / spend limit | Key hit its cap | Nothing a reinstall fixes — the key needs raising at the console end. Post which key and what you ran. |
| Tool claims it wrote a file that isn't there | Believe the folder, not the chat | `Get-Location`, `Get-ChildItem`. On OpenCode this is a known Windows defect — report version and exact wording. |
| goose installed but is a database tool | winget package name collision | Uninstall it; use the `aaif-goose` installer in section 10 |
| `goose --version` exits with `-1073741515` / `0xC0000135`, or mentions `MSVCP140.dll` | Microsoft Visual C++ runtime is missing; Goose crashes before its CLI starts | Install `Microsoft.VCRedist.2015+.x64` (or use Microsoft's x64 installer), close every PowerShell window, then check `where.exe MSVCP140.dll`; do not reinstall goose or switch shells |
| `goose info -v` shows a blank provider or model | `HB_OPENAI_MODEL` was unset or a placeholder was saved | Set a real model id in section 5, open a new window, and rerun the Goose provider block |
| Pi: "no bash shell found" mid-exercise | Git Bash not found | Set `shellPath` in `%USERPROFILE%\.pi\agent\settings.json` |
| n8n exits on startup with a version message | Node outside 22.22–24.x | Reinstall with the `.LTS` package id |
| Stuck 30 minutes on one step | — | Post the step number, exact error, and what you tried. Move to the next section; most are independent. |

---

## Identity lock

The goal is not a pretty install. The goal is that **you can rebuild this chair** — you know where each tool keeps its credentials, what its boundaries are, and how it fails — and that you have a trail of what broke.

A recorded failure is evidence, not shame.
