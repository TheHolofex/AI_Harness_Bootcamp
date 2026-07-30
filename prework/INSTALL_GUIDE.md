# Install guide — student-owned workstation

Platform: **vanilla Windows 11**. **No WSL required** for this course.

Work in order. After each section, tick the box in your `SETUP_LOG.md` and note failures.

> Seat credentials (ChatGPT/Codex, Claude, any class API keys, hosted open-model access) come from the course. Install the apps even if seat login waits on issued credentials — then finish sign-in as soon as seats land.

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
# See current policy
Get-ExecutionPolicy -List

# Typical fix if scripts are blocked (user scope — prefer this over machine-wide)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

- [ ] `Get-ExecutionPolicy -Scope CurrentUser` is `RemoteSigned` or less restrictive  

**If blocked by group policy:** note the error in setup log; contact support before Monday.

---

## 2. Git for Windows

```powershell
winget install --id Git.Git -e --source winget
```

Close and reopen PowerShell, then:

```powershell
git --version
# Confirm bash exists (default path often):
Test-Path "C:\Program Files\Git\bin\bash.exe"
```

- [ ] `git --version` works  
- [ ] Git Bash path known (you will point Pi at it if needed)

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
- [ ] Python and pip respond (`py -3 --version` OK if `python` is aliased oddly)

---

## 4. OpenAI Codex app (primary home)

1. Install via official Windows path (Microsoft Store / OpenAI Windows app instructions current for the course date).  
2. Sign in with **course-issued** ChatGPT/Codex seat when available.  
3. Create or open a test folder, e.g. `Documents\HarnessBootcamp\prework-smoke`.  
4. Confirm the agent can see the folder and run a trivial action you approve (e.g. create `hello.txt`).

- [ ] App launches  
- [ ] Signed in  
- [ ] Native Windows agent mode (not requiring WSL)  
- [ ] Sandbox/approval prompts understood (Ask vs higher access — know what you clicked)  
- [ ] Write proof: `hello.txt` exists from agent action  

**Setup log:** note any sandbox elevated/unelevated failure and workaround.

---

## 5. Claude Desktop + Code tab (second engine)

1. Install Claude Desktop for Windows from official download.  
2. Sign in with course-issued seat.  
3. Open **Code** tab.  
4. Select Local + a test folder (can reuse `prework-smoke`).  
5. Confirm Git is detected; restart Claude after Git install if needed.  
6. Run a trivial approved edit/create in the test folder.

- [ ] Code tab available (not paywalled/403)  
- [ ] Local session works  
- [ ] Permission mode visible (Manual / Accept edits / etc.)  
- [ ] Write proof in test folder  

---

## 6. Pi (bare-loop tool)

Follow current [Pi Windows docs](https://pi.dev/docs/latest/windows): bash required (Git Bash is the default path).

- [ ] Pi installed  
- [ ] `shellPath` or auto-detect points at Git Bash if needed  
- [ ] Pi starts and can run a trivial command in a project dir  

**Setup log:** exact install method + bash path.

---

## 7. goose

Install Windows desktop and/or CLI per current goose docs (PowerShell or Git Bash install path).

- [ ] `goose` or desktop app launches  
- [ ] Provider configured with course-approved credentials  
- [ ] One sample/recipe or session runs once successfully  

**Setup log:** desktop vs CLI; provider name; first error you hit.

---

## 8. Obsidian + n8n

**Obsidian**

- [ ] Installed from official site  
- [ ] Opens; you can create a local vault (class vault may replace this on Wed)

**n8n**

- [ ] Installed via course-approved method (local npm/desktop/docker-free path as specified for the cohort)  
- [ ] UI loads once on localhost (or approved host)  
- [ ] You know how to start/stop it  

---

## 9. Course repo / operator pack (when issued)

When the bootcamp materials link is available:

- [ ] Clone or download `AI_Harness_Bootcamp` student pack  
- [ ] Copy `operator/` standing files into your working Codex project  
- [ ] Skim `student_pack/README.md` so Monday pulse is not a surprise  

---

## 10. Health check gate

Complete `HEALTH_CHECK.md` end-to-end.

- [ ] All checks green **or** red items have a written unblock plan with support  

**You are not done until health check is green or explicitly waived in writing by staff.**

---

## Rescue paths (common)

| Symptom | Try |
|---|---|
| `winget` missing | Update App Installer / install packages from official .exe and log it |
| Execution policy blocked | `CurrentUser` RemoteSigned; else corporate GPO → support |
| Codex sandbox fails elevated | Try unelevated / document; still prove folder write |
| Claude Code 403 / no Code tab | Seat tier / sign-in; restart after Git install |
| Pi can’t find bash | Set shell path to `C:\Program Files\Git\bin\bash.exe` |
| goose keyring errors | Env var / disable keyring per goose Windows notes; log it |
| No admin rights | Early ticket — do not wait for Monday AM |

---

## Identity lock

The goal is not a pretty install.  
The goal is: **you can rebuild this chair** and you have a trail of what broke.
