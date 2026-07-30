# Health check — pre-work gate

Run on the laptop you are **bringing Monday**, from a **freshly opened terminal**, **before Monday**.
Allow about thirty minutes. Bring the result to Block 0.

**Primary path:** `site/checklists/prework-health.html`

Mark each line **PASS** / **FAIL**. A FAIL without a written unblock is not ready — and saying so now is a complete answer.

> Start from a new **PowerShell** window. A window left open since installing may carry variables that won't exist on Monday, which would let a broken setup pass.
>
> Confirm it is PowerShell and not Command Prompt or Git Bash — a version number means you are in the right window, an error means you are somewhere else:
>
> ```powershell
> $PSVersionTable.PSVersion
> ```

---

## A. Foundations

```powershell
[Environment]::Is64BitOperatingSystem
$env:PROCESSOR_ARCHITECTURE
git --version
node -v
npm -v
python --version
(Get-Command python).Source
Test-Path "C:\Program Files\Git\bin\bash.exe"
Get-ExecutionPolicy -List
```

| Check | PASS/FAIL | Proof / note |
|---|---|---|
| Windows 11, 64-bit | | `winver` |
| **Not** ARM64 | | `AMD64` expected |
| Git on PATH | | version |
| Git Bash present | | path recorded |
| Node **22.22–24.x** | | version |
| npm answers | | version |
| Python answers, **not** a `\WindowsApps\` path | | resolved path |
| `CurrentUser` policy `RemoteSigned` | | |
| `MachinePolicy` and `UserPolicy` both `Undefined` | | GPO override check |

ARM64, or a policy row that is set, is a blocker to raise with staff rather than work around.

---

## B. Your three API keys

```powershell
'OPENAI_API_KEY','XAI_API_KEY','ANTHROPIC_API_KEY' | ForEach-Object {
  '{0}: user={1} session={2}' -f $_,
    [Environment]::GetEnvironmentVariable($_,'User').Length,
    (Get-Item "env:$_" -EA SilentlyContinue).Value.Length
}
```

| Check | PASS/FAIL |
|---|---|
| `OPENAI_API_KEY` — user and session both non-zero | |
| `XAI_API_KEY` — user and session both non-zero | |
| `ANTHROPIC_API_KEY` — user and session both non-zero | |

Run in a **fresh window** — that is what Monday will be. Only lengths print, never the keys, so this is safe on a shared screen.

`user=0` means it never saved. `session=0` means this window predates it.

**Spend caps:** if a tool that worked during install now fails with `429`, or a quota or spend-limit message, the key has hit its cap rather than broken. That is a staff fix, not a reinstall.

---

## C. Four required agents — files on disk

**Delete the old proof files and regenerate them.** Do not accept files made days ago on a machine state you no longer have.

```powershell
cd "$env:USERPROFILE\Documents\HarnessBootcamp\prework-smoke"
Remove-Item from-*.txt -ErrorAction SilentlyContinue
```

Re-run the four write commands from `INSTALL_GUIDE.md` sections 7–10, then:

```powershell
codex login status
opencode --version
goose info -v
Get-ChildItem from-*.txt
```

| Tool | File | PASS/FAIL | Also confirm |
|---|---|---|---|
| Codex | `from-codex.txt` | | `codex login status` reports **API key**, not a ChatGPT account |
| **OpenCode** | `from-opencode.txt` | | version recorded — Monday asks by name |
| Pi | `from-pi.txt` | | `bash-check.txt` also present (proves it reaches Git Bash) |
| goose | `from-goose.txt` | | `goose info -v` shows the intended provider and model |

**PASS only if all four files exist on disk** — not "the chat said it did". Open the folder in Explorer and look.

Missing any one is **not GREEN**.

If OpenCode reports success but writes no file, that is the known Windows defect: record version and exact wording, tell staff, stop retrying.

### Optional (does not affect your colour)

| Tool | File | PASS/FAIL |
|---|---|---|
| Claude Code (optional) | `from-claude-optional.txt` | |

---

## D. Supporting tools

```powershell
(Invoke-WebRequest http://localhost:5678/healthz -UseBasicParsing).StatusCode   # with n8n running
Get-ChildItem -Force "$env:USERPROFILE\Documents\HarnessBootcamp\vault"
```

| Check | PASS/FAIL | Note |
|---|---|---|
| Obsidian opens the vault, no login | | `.obsidian` folder present |
| n8n starts, `/healthz` returns 200, stops cleanly | | owner email + password recorded |
| Course repo cloned; site serves on 8080 | | |
| You can find `mission_flesh/b0/reports/` | | Monday's mission data |

---

## E. Operator readiness

| Check | PASS/FAIL |
|---|---|
| `operator/` templates are **in your working project**, and you can name them | |
| You can state the twin-engine pair: **Codex** (OpenAI key) + **OpenCode** (xAI key) | |
| You know what to do if a key leaks — tell staff, then re-run `codex login --with-api-key` after reissue | |
| Setup log holds at least one real failure and its fix | |

If genuinely nothing broke, write that, and note the one step you would least want to repeat from memory. A blank log is the one answer that doesn't hold up.

---

## Gate result

- [ ] **GREEN** — foundations pass, three keys verified in a fresh window, four agent files regenerated and present, supporting tools launch.
- [ ] **YELLOW** — one thing unresolved, you know exactly what it is, and you've written where it stops.
- [ ] **RED** — a required agent can't write a file, a key doesn't work, or you haven't been able to start. Say so **before** Monday.

YELLOW declared Saturday is a better position than GREEN claimed on a step you skipped. The colour is information, not a grade.

**Student name:** ________
**Machine:** ________
**Date/time reached:** ________
**OpenCode version:** ________
**Codex sandbox mode (elevated / unelevated):** ________
