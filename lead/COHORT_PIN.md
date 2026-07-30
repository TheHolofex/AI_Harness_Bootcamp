# Cohort pin sheet (staff only)

**One sheet. One source of truth.** Fill this before the pre-work window opens.
Post the filled values into the pre-work channel. Re-run the verifies the week of contact.

Do **not** hardcode model ids or OpenCode builds in learner handouts — point students at the channel pin.

---

## How to use this sheet

1. Run rotting-facts (any machine, no keys):

   ```bash
   python3 .github/scripts/verify-stack-facts.py
   ```

2. On a **Windows 11 x64** candidate laptop, run install/start smoke (no keys required for the automated half):

   ```powershell
   powershell -ExecutionPolicy Bypass -File .github\scripts\prework-verify.ps1
   ```

   Review `prework-verify-results.md` next to the script (or under the path you passed).

3. Complete the **human** proofs below (GUI, funded keys, browser→deck, xAI ACL).

4. Copy the **Post this** block into the student channel. Keep this file (or a dated copy) with the cohort record.

5. Re-run steps 1–3 the Sunday before contact week if more than a few days have passed.

---

## Pin table (fill every cell)

| Pin | Value (fill) | Notes |
|---|---|---|
| **Cohort id / dates** | _e.g. 2026-W32 · contact Mon–Fri_ | |
| **OpenCode channel** | `winget` **or** `npm` | **Required.** winget `SST.opencode` and npm `opencode-ai` drift; a version alone is ambiguous. |
| **OpenCode version** | _e.g. 1.18.7_ | Must match the channel you smoke-tested. Write proof must create a real file on disk. |
| **OpenCode winget id** | `SST.opencode` | Do not “fix” to Anomaly — package id is still SST. |
| **Node winget id** | `OpenJS.NodeJS.LTS` | Must land **22.22–24.x** for n8n. Never plain `OpenJS.NodeJS`. |
| **Node version observed** | _e.g. v24.18.1_ | From candidate machine after install. |
| **Git winget id** | `Git.Git` | Git Bash expected at `C:\Program Files\Git\bin\bash.exe`. |
| **OpenAI model id** | _paste current id_ | Drives Codex app pin + Pi/goose default (`HB_OPENAI_MODEL`). Confirm week-of. |
| **xAI / Grok model id** | _paste current id_ | OpenCode second engine (`HB_XAI_MODEL`). |
| **Anthropic model id** (optional path) | _paste or n/a_ | Only if optional Claude Code is supported this cohort. |
| **goose provider/model defaults** | `openai` / _same as OpenAI pin_ | Pre-work smoke: `GOOSE_PROVIDER` + `GOOSE_MODEL`. P6 may teach `approve` mode. |
| **LOCAL PIN** (P6/P8 stretch) | `Ollama · <tag> · min RAM · tool-call yes/weak/no` | Not clinic GREEN. Cold-smoke `goose run` once on staff Windows. Alt: LM Studio if named. |
| **P8 hosted endpoint** (if any) | _URL + auth posture or n/a_ | Friday hold/degrade only if the cohort uses one. |
| **Codex app package** | Store `9PLM9XGG6VKS` / MSIX rescue | Screen Store/MSIX block **before** cohort start. |
| **Codex sandbox default** | elevated preferred; unelevated OK | Collect per chair at Monday clinic. |
| **`OPENCODE_DISABLE_CLAUDE_CODE`** | must be `1` (User env) | Clinic check; protects P3 independence. |

### Post this (student channel)

Copy, fill, paste:

```text
COHORT PIN — use these, not “latest”

OpenCode: <channel> @ <version>
  winget: winget install --id SST.opencode --exact ...
  npm fallback only if staff say so: npm install -g opencode-ai@<version>

Node: OpenJS.NodeJS.LTS (expect 22.22–24.x) — observed staff: <version>
Models (env names from install guide):
  HB_OPENAI_MODEL=<id>
  HB_XAI_MODEL=<id>
OPENCODE_DISABLE_CLAUDE_CODE=1   (User env — install guide §8)

LOCAL PIN (optional stretch only, not Monday GREEN):
  <Ollama|LM Studio> · <tag> · min RAM · tool-call yes|weak|no
  HB_LOCAL_MODEL=<tag> when you pull

Do not freestyle model ids. If a tool asks for “latest,” use this pin.
```

---

## Cold-smoke checklist (staff machine)

Mark each row. Automated scripts do **not** replace the human rows.

### A. Any machine — rotting facts

| # | Check | Pass? |
|---|---|---|
| A1 | `python3 .github/scripts/verify-stack-facts.py` exit 0 (warnings OK if understood) | |
| A2 | OpenCode npm vs winget drift noted on this sheet (channel chosen deliberately) | |
| A3 | Node LTS still inside course band (or MEMORY/n8n note updated) | |

### B. Windows x64 — install/start (no keys)

| # | Check | Pass? |
|---|---|---|
| B1 | `prework-verify.ps1` exit 0 or documented YELLOW | |
| B2 | Git Bash path exists | |
| B3 | `opencode --version` matches **channel + version** pin | |
| B4 | Fresh terminal: `$env:OPENCODE_DISABLE_CLAUDE_CODE` → `1` after set | |
| B5 | `node -v` in LTS band; `python --version` not WindowsApps stub | |
| B6 | goose / pi binaries start (`--version` or equivalent) | |

### C. Human + funded keys (blocks students if skipped)

| # | Check | Pass? |
|---|---|---|
| C1 | OpenAI project key: Codex **Sign in another way** + `from-codex.txt` on disk | |
| C2 | xAI key: ACLs attached; OpenCode model list non-empty; `from-opencode.txt` on disk | |
| C3 | Anthropic key (if offering optional Claude): CLI write proof once | |
| C4 | Pi write + bash-check files on disk | |
| C5 | goose write proof with pinned provider/model | |
| C6 | Hard spend caps set (not alerts-only) on all three providers | |
| C7 | Store/MSIX screen done for managed laptops; rescue path known | |

### D. Contact-week lead surfaces

| # | Check | Pass? |
|---|---|---|
| D1 | Thursday lunch: `@Browser` → four-slide `slideshow.html` cold-smoke (`lead/BROWSER_DECK_DEMO.md`) | |
| D2 | Fallback path in demo script still valid if browser tool dead | |
| D3 | LOCAL PIN cold-smoke: one `goose run` on staff Windows with local tag (or YELLOW lead-demo only) | |
| D4 | Many Minds answer key remains staff-only (`lead/MANY_MINDS_ANSWER_KEY.md`) | |

---

## Discipline (why this sheet exists)

Staff pins decide room quality more than any single curriculum paragraph:

- **Channel + version** for OpenCode, or mixed winget/npm rooms are not one build.
- **Model ids rotate** — handouts stay generic; the channel carries numbers.
- **xAI deny-by-default** and **Store-only Codex** fail as “install is fine, nothing works.”
- **LOCAL PIN** and **browser→deck** are lead loads; students do not discover them in clinic.

If the pin is late, pre-work still runs on guide defaults — but clinic becomes pin-and-repair instead of finish-and-prove.

---

## Related paths

| Path | Role |
|---|---|
| `prework/FACILITATOR_NOTES.md` | Keys, clinic, stretch facilitation |
| `prework/INSTALL_GUIDE.md` | Student procedure |
| `.github/scripts/verify-stack-facts.py` | Rotting facts / CI |
| `.github/scripts/prework-verify.ps1` | Windows smoke |
| `lead/BROWSER_DECK_DEMO.md` | Thu after-lunch demo |
| `mission_flesh/p6/local_endpoint_notes.md` | Endpoint-wall stretch |
| `MEMORY.md` | Stack facts that rot |
