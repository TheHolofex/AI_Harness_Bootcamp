# Pre-work — facilitator notes

## Design choice

**No golden image.** Students install and configure their own vanilla Windows workstation as a **pre-work module** before contact hours.

Why:

- Operators own the chair at work; install is part of literacy
- Avoids "lab magic" that won't transfer
- Moves most install pain before contact week without removing the experience
- Monday still opens with an **install clinic** so remaining blockers die under staff eyes

## Staff actions required BEFORE the pre-work window opens

The course now runs entirely on API keys. These are staff jobs, and every one of them blocks students if it slips.

### 1. Provision keys — one per student, per provider

Three providers: OpenAI, xAI, Anthropic. **One key per student, never a shared cohort key** — a shared key can't be revoked for one person, gives no per-student usage attribution, and turns one leak into twenty.

Wrap each key in the provider's isolation unit so a cap and a kill switch exist per student:

| Provider | Isolation unit | Console | Prefix |
|---|---|---|---|
| OpenAI | Project | platform.openai.com | `sk-proj-` |
| xAI | Team + per-key ACLs | console.x.ai | `xai-` |
| Anthropic | Workspace | platform.claude.com | `sk-ant-api03-` |

**Fund every account before day one.** All three are prepaid; none will serve a coding model at a zero balance, and the failure surfaces as an authentication-looking error rather than a bill.

**Set hard spend limits, not alerts.** On OpenAI the distinction is explicit: an alert notifies and lets traffic continue, a hard limit returns `429`. An alert alone will not stop a runaway agent loop.

**xAI keys are deny-by-default.** A freshly minted `xai-` key has access to nothing until you attach ACLs (`api-key:model:…`, `api-key:endpoint:chat`). A key that looks valid and does nothing will strand the whole OpenCode section — verify one end to end before issuing.

Budget roughly $100 per student per provider for a week of heavy agent use, and set the caps there. That leaves headroom for a bad loop without leaving the door open.

### 2. Pin versions and models, then post them

**Source of truth:** fill `lead/COHORT_PIN.md` first, then post the filled values in the pre-work channel. Students are told to use the cohort pin rather than latest.

- **OpenCode version, and the channel you pinned it on.** This one matters most. OpenCode ships fast and Windows support has regressed between releases — file-writing tools failing on Windows has been a live issue. Install a candidate on one machine, run the write proof, and pin what passes.

  **The guide's two install paths do not deliver the same build.** Checked 2026-07-30: winget `SST.opencode` was on **1.18.7** while npm `opencode-ai` was on **1.18.10**. winget lags, sometimes by days. A pin that names only a version number is ambiguous — post the channel with it, or a room that mixed winget and the npm fallback is not on one build no matter what the number says.
- **Model ids** for OpenAI and xAI. Do not let handouts carry hardcoded model names; providers rotate them. Confirm current ids the week the course runs.

Two things about OpenCode that will not announce themselves:

- **The winget id is still `SST.opencode`.** The project moved from SST to Anomaly and the repo, Homebrew tap, and container images all renamed, but the winget package id did not. It is actively maintained under the old name. Do not "correct" it in the guide.
- **OpenCode reads `~/.claude/CLAUDE.md` and `.claude/skills` by default.** Any student who installs the optional Claude Code gets a second engine quietly running on the first one's standing instructions, and nothing in either tool says so. Pre-work sets `OPENCODE_DISABLE_CLAUDE_CODE=1` (install checklist step 43, section 8 in `INSTALL_GUIDE.md`); check it during clinic alongside the version. The same exposure exists on the Codex side through `AGENTS.md`, skills, and memories — students handle that one in P3 by running from a clean folder or declaring what was live.

### 2a. Re-check the rotting facts before you pin

Two harnesses exist so this is not a manual afternoon:

```bash
python3 .github/scripts/verify-stack-facts.py
```

Runs from any machine, no Windows and no keys. Confirms the winget ids still
resolve, re-tests the Node `.LTS` claim against what winget actually offers
today, and flags when the winget and npm channels have drifted apart.

```powershell
powershell -ExecutionPolicy Bypass -File .github\scripts\prework-verify.ps1
```

Run on the candidate build itself, on real Windows x64. Covers what the first
one cannot: that the tools install and start, that Git Bash is where the guide
says, and that the `OPENCODE_DISABLE_CLAUDE_CODE` round-trip survives a fresh
terminal. Writes `prework-verify-results.md` beside itself.

Neither touches the GUI steps or the key-dependent write proofs. Those still
need a person at a keyboard with a funded key. Tick the human rows on
`lead/COHORT_PIN.md` (sections C–D) after the scripts pass.

### 3. Revocation plan

Anthropic is cleanest — archiving a workspace revokes all its keys at once. OpenAI is per-project. xAI is per-key, and note that **removing a user from the team does not revoke their keys**.

## What staff provides

- Three API keys per student, funded, capped, and ACL'd, in time for the pre-work window
- Pinned OpenCode version and model ids in the pre-work channel
- This pre-work pack + support channel hours
- Monday AM **install clinic** in contact hours (~2 hr expected, no hard wall) — not a silent image drop
- Clinic is finish-and-prove on per-step verifies — not mass imaging and not re-teaching winget from zero for skipped pre-work

## What staff does not do

- Hand out a pre-baked golden laptop image as the default path
- Burn the whole Monday AM re-teaching winget from zero for students who skipped pre-work (clinic helps finishers; skippers get parallel rescue, not a redesign of the school)
- Lower First Light mastery bars because pre-work was ignored

## Escalations that cannot be fixed from the student's seat

Triage these first when someone reports being stuck; no amount of retrying helps.

| Symptom | Reality |
|---|---|
| `Get-ExecutionPolicy -List` shows MachinePolicy or UserPolicy set | Group Policy overrides the student. IT ticket. |
| `$env:PROCESSOR_ARCHITECTURE` returns ARM64 | OpenCode won't start; goose has no ARM build. Different machine required. Worth a re-test each cohort: the npm package now declares `cpu: ["arm64","x64"]` and `os: [...,"win32"]`, so the metadata permits a Windows ARM64 install even though the runtime failure is what we actually observed. Metadata permitting an install is not the same as it working — confirm on hardware before relaxing this. |
| No admin rights for elevation prompts | Git, Node, and the Codex app's elevated sandbox all need one. IT ticket. Codex still runs on the `unelevated` fallback, so this is YELLOW rather than RED. |
| Microsoft Store or `winget ... -s msstore` blocked by policy | The Codex app ships only as a Store-signed package. Rescue is the direct MSIX (`ChatGPT-x64.msix`) in the install guide's rescue table; there is no MSI or standalone EXE. Screen for this before cohort start — it is the one install with no second vendor path. |
| Key returns 429 / insufficient quota | Cap or balance. Staff console fix. |
| xAI key authenticates but reaches no model | Missing ACLs on the key. Staff console fix. |

## Monday install clinic

1. Open with clinic — expect **about two hours**, **no hard boundary**. When chairs are proven, start First Light.
2. Students re-run **per-step verifies** from the install guide (not a separate health-check ritual). Staff roam; triage escalations from the table above first.
3. Still blocked after honest effort → rescue table in parallel; do not stall First Light for the whole room.
4. B0 MVP still requires four-tool write proof — pre-work should already have produced it; clinic confirms or re-runs smoke files.

Collect **OpenCode version**, **`OPENCODE_DISABLE_CLAUDE_CODE`**, and **Codex sandbox mode** during clinic. Those are what differ between machines when something behaves oddly mid-block — and the middle one is what quietly narrows Tuesday's disagreements if it is missing.

## Rescue

- YELLOW with a documented workaround: allow into First Light.
- RED that is keys-only: staff can usually unblock faster than install-from-zero.
- RED "never started": evening make-up; not a redesign of the school into an image depot.

## goose — product vs course slice (P6)

goose is a full local agent platform (CLI + Desktop + API/ACP): recipes with parameters/extensions/retry, 70+ MCP extensions, permission modes, scheduler, subagents, adversary mode, hooks. Docs: <https://goose-docs.ai>.

**Course slice (keep this altitude with students):**

```text
goose = loop + recipe + tool surface + autonomy dial + unattended path
```

| Lever | Where students touch it | Contract column |
|---|---|---|
| Recipe | `mission_flesh/p6/watch_officer.yaml` | Both (mission text + structured fields) |
| Tool surface | `extensions:` (starter: `developer` only) | Tool-enforced |
| Autonomy dial | `GOOSE_MODE`, `settings.max_turns` | Tool-enforced |
| Unattended path | Desktop Scheduler or CLI schedule; retry checks | Tool path / honest block |

**Facilitator defaults**

- CLI is the course default. Desktop is welcome for Scheduler UI; not required for MVP.
- Pre-work smoke uses `GOOSE_MODE=auto`. P6 teaching default is often `approve` so the dial is visible.
- Tool-enforced rows must name real levers — reject contracts that only say “be safe.”
- Schedule may fail on locked Windows; **honest block with exact error** is valid MVP (already in PASS_BARS).
- goose’s provider list includes ChatGPT/Copilot/Claude subscription paths — course is API keys only; steer students off those.
- Docs often prefer Claude-class models for tool calling; still run the staff OpenAI (or posted) pin and measure.
- Out of scope for MVP unless stretch is earned: subagents, MCP Apps, Adversary Mode, custom MCP servers, hooks.

Pack: `mission_flesh/p6/` (`watch_officer.yaml`, `goose_recipe_notes.md`, `feeder/`, `out/`).

## Contact-week lead posture (reminder)

Lead runs missions live on screen with talk-through and real-time AI depth. Pre-work stays student-owned. Monday is **install clinic** then First Light operate-along — finish-and-prove, not a from-zero install lecture for the room.

**Tue/Wed/Thu AM:** protect the last **45 minutes before lunch** for the harness case talk (30 present + 15 discuss). Guide: `lead/HARNESS_CASE_TALKS.md`.

**Thursday after lunch:** protect **30 minutes** for the **browser → deck lead demo** before P7 (staff Windows machine only; students watch). Cold-smoke `@Browser` → four-slide `slideshow.html` at lunch. Script + fallback: `lead/BROWSER_DECK_DEMO.md`. Not student setup; no Chrome extension.


## Stretch modules (contact week — not pre-work GREEN)

### Many Minds (P3 stretch)
- After twin-engine MVP: `mission_flesh/p3/MANY_MINDS.md` — require **three** artifacts: `baseline_single.md`, `many_minds_synthesis.md`, `many_minds_delta.md`. Spot-audit deltas first.
- Cap three read-only subagents; synthesis file on disk; correct “Cowork” language. The prompt cap is procedure-enforced — `agents.max_concurrent_threads_per_session` is the tool-enforced one, worth setting on demo or spend-sensitive machines. Answer key for the seeded defects: `lead/MANY_MINDS_ANSWER_KEY.md` (staff only; the corpus is unlabelled on purpose)
- Worktrees optional; don’t burn the block if Git/UI fights the room

### Local endpoint (P6→P8 stretch)
- Post before Thursday: `LOCAL PIN: Ollama · <tag> · min RAM · tool-call yes/weak/no`
- Cold-smoke `goose run` once on staff Windows laptop
- YELLOW/lead-demo is fine when student RAM is short
- Guide: `mission_flesh/p6/local_endpoint_notes.md`
