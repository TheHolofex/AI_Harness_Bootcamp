# Health check — pre-work gate

Run on the student machine **before Monday**.  
Bring proof to Block 0 verification.

**Primary path:** `site/checklists/prework-health.html`

Mark each line **PASS** / **FAIL**. FAIL without a written unblock = not ready.

---

## A. Baseline

| Check | PASS/FAIL | Proof |
|---|---|---|
| Windows 11 | | `winver` note |
| Git on PATH | | `git --version` |
| Git Bash present | | path |
| Node + npm | | versions |
| Python | | version |
| PowerShell scripts allowed (user) | | execution policy |

---

## B. Four **required** agents — same temp project

Create: `Documents\HarnessBootcamp\prework-smoke\`  

Each **required** tool must create a uniquely named file you can see in Explorer:

| Tool | File to create | PASS/FAIL | Notes |
|---|---|---|---|
| Codex app | `from-codex.txt` | | |
| **OpenCode** | `from-opencode.txt` | | Grok or staff-pinned model |
| Pi | `from-pi.txt` | | |
| goose | `from-goose.txt` | | |

**PASS only if all four files exist on disk** (not “the chat said it did”).

### Optional (does not block GREEN)

| Tool | File | PASS/FAIL |
|---|---|---|
| Claude Code (optional) | `from-claude-optional.txt` | |

---

## C. Seats and modes

| Check | PASS/FAIL | Notes |
|---|---|---|
| Codex signed in | | |
| Codex approval/sandbox understood | | |
| **OpenCode** configured (Grok or staff pin) | | version logged |
| OpenCode can run a task on smoke folder | | |
| goose provider configured | | |
| Obsidian launches | | |
| n8n UI loads once | | |
| *(Optional)* Claude Code works | | not required |

---

## D. Operator pack awareness

| Check | PASS/FAIL |
|---|---|
| Know where `operator/` templates live in Codex project | |
| Know threads: Direction & Log · Adversarial · Transfer | |
| Know twin-engine pair: **Codex + OpenCode** | |
| Setup log has at least one real failure + fix | |

---

## Gate result

- [ ] **GREEN** — A + four required agent files + required seats/modes. Ready for Block 0.  
- [ ] **YELLOW** — minor FAIL with staff-approved workaround documented.  
- [ ] **RED** — required four-agent proof incomplete or required seats missing. Stay in pre-work/support.

**Student name:** ________  
**Date/time green:** ________  
**Machine name:** ________  
**OpenCode version / model:** ________  
