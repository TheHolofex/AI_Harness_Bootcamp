# Project Memory — AI Harness Bootcamp

## What this is

This is an **operator’s school**.

Not a prompt class. Not a tool tour. Not a productivity seminar.

It trains **deep operator mastery of AI direction and cothinking**: the human sets outcomes, bounds, and standards of evidence; a thinking machine works inside that frame as a durable partner.

AI here is treated as what it is — a thinking machine that can aide real work. Science-fiction capability. The course exists so that capability is not squandered on clever chat, demo theater, or speed for its own sake.

## Identity (non-negotiable)

- **Operator’s school** — people leave able to *run* harnessed AI at work, not merely talk about it.
- **Deep operator mastery** — judgment under a harness: direct, observe, correct, accept/reject, bound, transfer.
- **AI direction** — the human owns the mission, acceptance criteria, and verdict. The machine loops inside guardrails.
- **Cothinking** — shared cognitive work with trails: the machine proposes and executes; the operator verifies, adjudicates, and decides. Partnership, not delegation of responsibility.
- **Mastery over novelty** — tools rotate; the operator craft stays. Instructions, tests, memory, skills, contracts, and evidence outlive any single app or model.


## Teaching posture (lead instructor)

The lead does **not** abstract into a distant lecturer. The lead **runs the exercises live** with students watching the screen — same tools, same pulse, same failure modes.

| Mode | What it looks like |
|---|---|
| **Live operate** | Instructor does the block work on-screen (brief, mission, log, adversarial, measure, transfer) so the room sees real direction and cothinking |
| **Talk-through** | Continuous narration: why this accept/reject, what evidence counts, where the harness is weak, what they’d do at work |
| **Side lectures** | Short, experience-grounded asides — only when they sharpen the exercise, not as a separate slide course |
| **AI as depth instrument** | Instructor interacts with the AI **in real time** to go deeper: explain, challenge, diagram, unpack concepts while the room watches the cothinking |
| **Students still own the chair** | Watching is not substituting; students run their own pulse and artifacts. Demo is model + insight, not “copy my output” |

### Implications for materials

- Prefer prompts, instruments, and rituals the lead can **drive live** without a separate teacher deck as the main path.
- Diagrams and deep explanations can be **produced in-session with the AI** when useful; pre-baked slides are support, not the spine.
- Facilitator notes assume a lead who can show judgment under fire — including REJECT, wounded adversarial, and install scars — not only a polished happy path.
- Tone in the room: standing beside operators, concrete, experience-rich; not corporate training voice and not mystical AI priesthood.



## Learner-facing voice — guide-beside

All **student-facing** site copy, pre-work, block pages, instrument READMEs, and in-flow help use **guide-beside** voice:

A calm expert standing next to the reader at the keyboard — not lecturing from the front, not patting them on the head. The reader is capable; they are doing something unfamiliar, right now.

| Do | Don't |
|---|---|
| Purpose before procedure; map before territory | Jargon walls and glossary dumps |
| Complete sentences; plain professional warmth | Staccato marketing fragments; chummy hype |
| Define terms at first need, in the breath | “You don’t need to understand this” |
| Explain related concepts when they unlock the step | Assume prior AI-native fluency |
| Honest about failure; recovery path in the same breath | “You can’t break anything” overclaim |
| One idea per sentence in procedures | Deck slogans (“level up your AI journey”) |

**Warmth:** welcoming, contracted (“you’ll,” “don’t”), never fawning.  
**Completeness:** enough mechanism that a technical-but-not-developer operator can follow alone — and enough concept that “why” is clear when it matters.  
**Lead live talk-through** may go denser and more experiential; **written site path** stays guide-beside so the room can re-read without the lead.

Full recipe: guide-beside-voice skill. Visual chrome stays Starzl paper/field; **voice** is what makes pages feel human and learnable.

## Delivery medium — the course site

This bootcamp is **not a series of slide decks**.  

All exercises, instruments, pre-work, operator rituals, and supporting material **live on a course site** (the canonical learner surface). The lead still operate-alongs on screen; students open the same site and run their own chair.

| Is the course | Is not the course |
|---|---|
| A site holding the week’s spine, blocks, kits, and pulse | A PowerPoint/Google-Slides spine with optional links |
| Durable pages students return to during and after class | Deck theater that evaporates when the projector dies |
| Repo/content that can publish into the site | Orphan PDFs as the system of record |

### Implications

- Author materials as **site-ready pages** (clear hierarchy, block pages, linked instruments) — decks only if a thin support aid is truly needed.
- Student path: site → pre-work → block page → instruments → operator templates.
- Lead path: same site on the projector/share, plus live AI depth — not a private teacher deck that students never see.
- This repo is the content source of truth until/unless a separate site app is wired; structure should not assume “export to 40 slides.”

## What “done” means for this course

A graduate can:

1. Direct a harness from messy operational reality to a working instrument with stated acceptance criteria.
2. Build machines that regenerate judgment products (briefs, rollups, watches) instead of one-shot answers.
3. Improve a harness with measured craft — instructions, tests, durable memory, skills.
4. Run the same demand through more than one engine and own the verdict when they disagree.
5. Put a thinking machine inside *their* knowledge system with citations they can walk.
6. Detect poison and hostile instruction; prove containment by absence of effect.
7. Write an autonomy contract; run work under bounds; stop and restart on authority.
8. Choose agent loop vs fixed pipeline with a human gate — the right machine for the job.
9. Transfer the method across vendor, model, and policy change.


## Authentication posture — API keys only

**The course is taught entirely from API keys. No subscription logins anywhere.**

Staff issue **three keys per student**, one per provider, each project/workspace-scoped with a hard spend cap so it can be capped and revoked individually. Never a shared cohort key.

| Key | Variable | Drives |
|---|---|---|
| OpenAI (`sk-proj-`) | `OPENAI_API_KEY` | Codex (home), n8n LLM step |
| xAI (`xai-`) | `XAI_API_KEY` | OpenCode (second engine, Grok) |
| Anthropic (`sk-ant-api03-`) | `ANTHROPIC_API_KEY` | Claude Code (optional), alternate provider for Pi and goose |

Consequences that must survive into every learner-facing page:

- Several tools offer a subscription login and an API key option on the same screen. Materials always name the API key path explicitly.
- **Codex cloud/web is unavailable** — it requires ChatGPT sign-in. CLI, IDE extension, and the GUI inside the **ChatGPT desktop app** all accept a bare key.
- **The Claude desktop app's Code tab is unavailable** — subscription only. Claude Code means the CLI.
- A capped key fails as a `429`/quota error that reads like an auth failure. Every troubleshooting path must name this, or students will reinstall instead of asking.

## Required tool stack (Windows 11, 64-bit — no WSL, no ARM64)

| Role | Tool | Required? |
|---|---|---|
| Primary home all week | **Codex** (CLI; GUI via ChatGPT desktop app) | Required |
| Second engine (twin-engine, compares) | **OpenCode** with **Grok** on the xAI key | Required |
| Bare loop demo | **Pi** | Required |
| Bound autonomy / recipes | **goose** | Required |
| Knowledge UI | **Obsidian** | Required (Wed) |
| Pipeline UI | **n8n** | Required (Thu) |
| Alternate second / third engine | **Claude Code** (CLI only) | **Optional** |

Twin-engine pedagogy (P3) uses **Codex + OpenCode**. Students may add Claude as an extra comparator; it is not required for GREEN pre-work or course pass.

### Stack facts that rot fast — re-verify before each cohort

Checked 2026-07-30. These are the ones that silently break a room:

- **goose moved** to `aaif-goose/goose` (Agentic AI Foundation); docs at `goose-docs.ai`. Old `block/goose` URLs are stale. **No winget package** — the winget `goose` is an unrelated database tool.
- **OpenCode Windows support regresses between releases.** Staff must pin and smoke-test a version per cohort. Its `curl` installer is bash-only; no PowerShell equivalent exists.
- **`codex login --api-key` is retired** — use `--with-api-key` (reads stdin). `OPENAI_API_KEY` alone does *not* authenticate Codex; it only pre-fills the setup screen. Pin with `forced_login_method = "api"`.
- **Node must be `OpenJS.NodeJS.LTS`**, landing in 22.22–24.x. Plain `OpenJS.NodeJS` installs a release too new for n8n.
- **xAI keys are deny-by-default** — a new key does nothing until ACLs are attached. Verify one end to end before issuing.
- **Model ids rotate.** Never hardcode them in handouts; staff post the cohort pin.

## North star

> A thinking machine as a durable work partner under your judgment — systems you can direct, verify, bound, and transfer.

## How to work on this repo

When building curriculum, materials, images, scripts, or docs:

- Keep the **operator’s school** frame in every learner-facing line.
- Prefer **mastery** language over productivity slogans, hype, or tool worship.
- Design for **vanilla Windows 11** (64-bit, no WSL, no ARM64), mixed backgrounds, **API keys only — never a subscription login** (Codex home; **OpenCode + Grok** as required second engine; Pi; goose). **Claude Code (CLI) is optional** alternate/third engine.
- **Student-owned install** via `prework/` module before contact week — **no golden image** as the default path. Block 0 verifies the gate, then First Light.
- Every project must force **direction + evidence + judgment**, not passive watching.
- Honor **MVP pass bars** in `operator/PASS_BARS.md`; do not dilute them for convenience.
- **Every block:** new adversarial review thread using `operator/ADVERSARIAL_REVIEW.md` (frozen prompt); log stood/wounded/failed before transfer.
- **Every block after adversarial:** update `operator/MEASUREMENT_SPINE.md` (ritual · mission · quality · time); then transfer pulse.
- After **every AM and PM** block: interactive transfer session in thread `Operator — Transfer 30-60-90` (`operator/TRANSFER_30_60_90.md`); seal at P8 — never invent cold on Friday.
- Protect the spine: First Light → machine-that-makes-the-answer → hot-rod craft → twin-engine verdict → knowledge → poison → autonomy contract → pipeline contrast → transferable method.
- MVP and stretch lanes are allowed; watering down the operator standard is not.
- Epic is the feeling after a real dyno win — not an adjective on the syllabus.

## Anti-patterns (reject these)

- Chat fluency as the goal
- “Ship faster” as the whole point
- Brand loyalty to one model or app
- Acceptance by vibe or model self-assessment
- Autonomy without a written contract and stop authority
- Knowledge systems without citation trails and containment
- Friday theater instead of measured hold/degrade and transfer
- Golden image as a substitute for student-owned workstation setup (pre-work exists so install is learned, not skipped)
- Teacher-deck theater while students only watch — lead operates live; students still own their chair and artifacts
- Deck-first course design — the site holds exercises and materials; slides are optional aides only
- Cold expert walls *or* chummy hype on learner pages — guide-beside only for student-facing copy

## Operator ritual (every block)

Standing files in `operator/` (copied into the student Codex project):

- `operator/DIRECTION_BRIEF.md` — five fields, **before** the run
- `operator/OPERATOR_LOG.md` — five fields, **after** the run

Produced **interactively** in Codex thread `Operator — Direction & Log`.  
The AI interviews, drafts, and challenges vagueness or weak evidence; the operator accepts wording and assigns the verdict.  
Build/mission work stays in other threads. Ultra-light: under five minutes dialogue pre, under five post.  
**After** log/pass-bar each AM and PM: open a **new** `Adversarial — [block]` thread with `operator/ADVERSARIAL_REVIEW.md` frozen prompt; update log if the attack lands.  
**Then** update `MEASUREMENT_SPINE.md` (four headlines). **Then** `Operator — Transfer 30-60-90` outer-loop pulse (Move 3).  
One stable brief/log template all week — cothinking muscle memory; adversarial review is the in-course verdict challenger; transfer file carries the job half of the circuit.

## Pass bars (every block)

MVP vs stretch/side-quest live in `operator/PASS_BARS.md`, mapped 1:1 to the nine graduate capabilities.  
MVP is the **mastery floor** — the least that still proves the capability (direction, evidence, owned verdict). Not “it ran.”  
Same-day clearable with serious work; not clearable by demo-watching or vibe. Student + AI stress-test claims in the operator thread after the log.  
Course floor = MVP on all nine with peer-auditable log evidence. Distinction = floor + stretch or side-quest on ≥4 blocks including P2, P5, P8.

## Transfer outer loop (living 30-60-90)

The week’s inner circuit ends incomplete unless transfer runs after Friday.  
`operator/TRANSFER_30_60_90.md` is the **outer half of the circuit**.  
Maintained **interactively with the AI in its own Codex thread** (`Operator — Transfer 30-60-90`) **after every morning and every afternoon block** — not collapsed into Direction/Log, not a Friday worksheet.  
Session log proves the pulse; major seeds deepen on P2/P3/P5/P6/P7; **SEALED** only at P8. Monthly review keeps the loop closed on the job.

## Measurement spine (every block)

`operator/MEASUREMENT_SPINE.md` — ultra-light living scoreboard updated **after adversarial**, before transfer.  
Four headlines only: **ritual health** (brief/log/adversarial) · **mission accomplishment** · **work quality** (evidence under fire) · **time to result**.  
Student scoreboard + thin facilitator rollup (`operator/FACILITATOR_ROLLUP.md`). Continuity without KPI bloat; deep one-liners only on P2/P3/P5/P6/P8.

## Living artifacts

- `DAY_PROJECT_TABLE.md` — day spine, projects, tool rotation
- `prework/` — student-owned workstation install module + health check (before Monday)
- `instruments/` — shared course kits: P2 dyno, P3 frozen brief, P8 hold/degrade (engineering + mission_ops tracks)
- `todo1.md` — circuit completeness analysis (outer loops to close)
- `operator/` — Direction Brief + Log (Move 1) · Pass bars (Move 2) · Transfer 30-60-90 (Move 3)
- Course **site** (`site/`) — canonical learner surface; visual system from starzl.com + Starzl PDF courseware
- This file — course identity and operator standard for anyone (human or agent) working here

When these conflict with a trendy framing, **this memory wins**.
