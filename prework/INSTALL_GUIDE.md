# Install guide — student-owned workstation

Platform: **vanilla Windows 11**. **No WSL required** for this course.

Work in order. After each section, tick the box in your `SETUP_LOG.md` and note failures.

> Seat credentials (ChatGPT/Codex, OpenCode/Grok keys, any class API keys) come from the course. Install apps even if login waits on issued credentials — then finish sign-in as soon as seats land.

**Primary path:** interactive checklist at `site/checklists/prework-install.html` (same steps, check-off UI).

---

## 0. Baseline machine

- [ ] Windows 11, updated  
- [ ] Disk space free (recommend ≥25 GB free before agent tooling)  
- [ ] You can run installers (admin rights as needed)  
- [ ] Browser works; you can complete OAuth sign-ins  

**Record in setup log:** Windows version (`winver`), username, admin yes/no.

---

## 1. PowerShell readiness

Open **PowerShell** (user session).

```powershell
Get-ExecutionPolicy -List
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Get-ExecutionPolicy -Scope CurrentUser
```

- [ ] CurrentUser policy is `RemoteSigned` or less restrictive  

**If blocked by group policy:** note the error; contact support before Monday.

---

## 2. Git for Windows

```powershell
winget install --id Git.Git -e --source winget
```

Close and reopen PowerShell:

```powershell
git --version
Test-Path "C:\Program Files\Git\bin\bash.exe"
```

- [ ] `git --version` works  
- [ ] Git Bash path known (Pi may need it)

---

## 3. Node LTS + Python

```powershell
winget install --id OpenJS.NodeJS.LTS -e --source winget
winget install --id Python.Python.3.12 -e --source winget
```

New terminal:

```powershell
node -v
npm -v
python --version
pip --version
```

- [ ] Node and npm respond  
- [ ] Python and pip respond (`py -3 --version` OK if needed)

---

## 4. OpenAI Codex app (primary home)

1. Install via official Windows path (Microsoft Store / OpenAI Windows app instructions current for the course date).  
2. Sign in with **course-issued** ChatGPT/Codex seat when available.  
3. Create `Documents\HarnessBootcamp\prework-smoke`.  
4. Confirm native Windows agent (this course does not require WSL).  
5. Have the agent create `from-codex.txt` (or `hello.txt`) — **file must exist in Explorer**.

- [ ] App launches · signed in · write proof on disk  
- [ ] Sandbox/approval mode understood (log what you clicked)

---

## 5. OpenCode — required second engine

OpenCode is the course **second harness** for twin-engine work (typically backed by **Grok** or the model staff pin for your cohort).

### 5a. Install

Use the **current official OpenCode install path for Windows** from [opencode.ai](https://opencode.ai) / project docs at course date. Common patterns (verify against live docs — commands change):

```powershell
# Example patterns only — prefer the official Windows instructions staff link in the cohort channel
# winget, installer, or npm/npx global as documented upstream
```

Staff will post the **pinned install one-liner or installer link** for your cohort in the pre-work channel. Use that pin if it differs from generic web instructions.

- [ ] OpenCode installed (CLI and/or desktop per staff pin)  
- [ ] `opencode --version` or app About shows a version (record it)

### 5b. Configure Grok (or course-pinned model)

1. Open OpenCode config / provider setup for your install flavor.  
2. Add **Grok** (xAI) with the API key or seat staff issued — **or** the exact provider staff name if the cohort is pinned to a different OpenCode model.  
3. Set that model as selectable default for class work.  
4. Open project folder `Documents\HarnessBootcamp\prework-smoke`.  
5. Run a trivial task that creates `from-opencode.txt` on disk.

- [ ] Provider/model configured (Grok or staff pin)  
- [ ] Project folder opens  
- [ ] **Explorer proof:** `from-opencode.txt` exists  

**Setup log:** install method · version · provider name · first error and fix.

### 5c. Know what “second engine” means

During the week you will run the **same frozen brief** on Codex and on OpenCode, then adjudicate. OpenCode is not a toy side app — it is required for P3 MVP.

---

## 6. Pi (bare-loop tool)

Follow current [Pi Windows docs](https://pi.dev/docs/latest/windows): bash required (Git Bash default).

- [ ] Pi installed  
- [ ] bash path configured if needed (`C:\Program Files\Git\bin\bash.exe`)  
- [ ] Pi runs a trivial command; prefer write proof `from-pi.txt` in smoke folder  

---

## 7. goose

Install Windows desktop and/or CLI per current goose docs.

- [ ] goose launches  
- [ ] Provider configured with course-approved credentials  
- [ ] One sample recipe/session runs; prefer `from-goose.txt` write proof  

---

## 8. Obsidian + n8n

- [ ] Obsidian installed and opens  
- [ ] n8n installed via course-approved method; UI loads once; you know how to stop it  

---

## 9. Course repo / operator pack

- [ ] Clone/download `AI_Harness_Bootcamp`  
- [ ] Copy `operator/` into your Codex working project  
- [ ] Skim site (`python3 -m http.server 8080` → `http://localhost:8080/site/`)  

---

## 10. Optional — Claude Code (not required)

Only if you already have access or want a third mind:

- [ ] *(Optional)* Claude Desktop with **Code** tab, or Claude Code CLI  
- [ ] *(Optional)* Local session can write `from-claude-optional.txt`  

**Claude Code is optional.** It is **not** part of the GREEN four-agent set (Codex, OpenCode, Pi, goose). Skipping Claude does not block pre-work pass.

---

## 11. Health check gate

Complete `HEALTH_CHECK.md` or `site/checklists/prework-health.html` end-to-end.

- [ ] GREEN or YELLOW with documented workaround  

---

## Rescue paths (common)

| Symptom | Try |
|---|---|
| `winget` missing | App Installer update / official .exe installers |
| Execution policy GPO | Ticket early with error text |
| Codex sandbox elevated fail | Unelevated / document; still prove write |
| OpenCode auth/model missing | Confirm Grok/staff key; re-run provider setup; staff pin |
| Pi can’t find bash | Set path to Git `bash.exe` |
| goose keyring errors | Env var / disable keyring per goose Windows notes |
| No admin | Early ticket |

---

## Identity lock

The goal is not a pretty install.  
The goal is: **you can rebuild this chair** and you have a trail of what broke.
