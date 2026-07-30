# AI Mission Architect — Day / Project / Harness Table

**Course identity:** an **operator’s school** for **deep operator mastery of AI direction and cothinking**.  
Project memory: `MEMORY.md` (authoritative identity and standard).

Working platform: **vanilla Windows 11** (no WSL required).  
Working tool all week: **Codex app** — course shorthand for Codex mode in the **ChatGPT desktop app**, which is the only Codex surface used. Second harness: **OpenCode** (Grok) — comparator on P3, permissions contrast on P5. **Claude Code optional**.

Geometry: **Pre-work module** (student-owned install, verify-as-you-go) + Monday–Thursday full days; Friday morning only. Monday AM opens with an **install clinic** (~2 hours expected, no hard wall) then First Light. Tue/Wed/Thu AM each end with a **45-minute harness case talk** (30 present + 15 discuss) before lunch. Thursday **after lunch**: **30-minute lead browser → deck demo** (watch only), then P7. Contact = clinic + 8 projects + three case talks + one browser→deck demo.

| Day | Block | Project | Brief description | Learning objectives | Harness / tools | AI thinking & mastery goals |
|---|---|---|---|---|---|---|
| **Mon** | **Block 0 AM** | **Install clinic + First Light** | **Clinic (~2 hr expected, no hard boundary):** finish install gaps, re-run per-step verifies, four-agent smoke files, setup log. Then meet the Assistant in the Codex app and turn a messy folder of synthetic mission reports into a live interactive browser map (timeline, filters) that updates when new files drop. | Own the chair under staff eyes · close remaining install blockers · direct AI from messy data to a working tool · name the **harness loop** after First Light works · state mission outcome with acceptance criteria | **Codex app** (primary). Four required from pre-work/clinic: Codex app, OpenCode, Pi, goose (Claude optional) | **Mastery:** stand up a working instrument from raw operational mess—so the bottleneck shifts from “can this be built?” to “what should exist, and how will we know it’s right?” **Thinking:** inhabit act→observe→correct before naming it; you set the goal, AI loops inside tool guardrails |
| **Mon** | **P1 PM** | **The Daily Status Brief** | Direct the Assistant to build a **rerunnable** cited daily brief from a report corpus; accept only after delta reports update citations correctly. | Specify format + acceptance checks · verify citations against real sources · distinguish a tool from a one-shot chat answer · accept/reject with evidence | **Codex app** | **Mastery:** turn recurring judgment products—status, rollups, cited briefs—into systems you own, so when the world changes you regenerate truth instead of rebuilding the argument from scratch. **Thinking:** “build the machine that makes the answer”; independent evidence beats the model’s self-assessment |
| **Tue** | **P2 AM** | **The hot-rod morning** | Stock reveal → measure on a dyno sheet → one instruction change → authored tests → memory that survives restart → skill that can fire unprompted. | Improve harness config with measured deltas · author machine-checkable test cases · install durable memory · package craft as a skill · start the 30-60-90 | **Codex app** (pack: project instructions, skills/memory templates) | **Mastery:** encode standards, tests, memory, and skills so the thinking machine carries your craft forward—competence compounds across days instead of resetting every session. **Thinking:** same harness loop, better walls—loop quality tracks instructions/tests/memory/skills, proven on the dyno sheet |
| **Tue** | **AM case talk** | **Harness case talk** | Lead presents one real problem they solved with harnessed AI (how the harness helped, what the experience was). 30 min talk + 15 min discussion before lunch. | Hear operator craft under fire · map harness moves to real work · seed Transfer from a lived story | Lead live · student discussion | **Mastery:** connect morning craft to a desk that is not the classroom. **Thinking:** harness value is proven in scars and evidence, not brand names |
| **Tue** | **P3 PM** | **The twin-engine intel desk** | Normalize frozen OSINT sources, deterministic watchlist join, then run the **same extraction brief** in Codex app and OpenCode; adjudicate disagreements; one-command watch report + delta rerun. **Stretch — Many Minds:** after MVP, parallel Codex **subagents** on `instruments/p3_multi_agent/` (optional worktree isolation). | Stand up multi-source normalizers · provenance without model judgment on joins · dispatch a second harness under one brief · **declare or clear the context each engine carries before calling the delta evidence** · personal adjudication · “agreement ≠ truth” · *(stretch)* commander owns subagent merge/kills | **Codex app** (commander) + **OpenCode** (second harness / Grok, run clean); stretch: Codex subagents/worktrees | **Mastery:** stop treating any single model’s voice as reality; run the same demand through independent minds, use disagreement as a sensor, and spend human judgment where it changes the outcome. **Thinking:** AI as a callable component; underspecified briefs fail both engines; you own the verdict; *subagent ≠ second engine ≠ second human* |
| **Wed** | **P4 AM** | **The director’s second brain** | Seeded Obsidian vault: organize inbox into linked notes, answer cross-vault questions with clickable note-link citations, generate a Morning Brief note. | Scope Assistant access to a vault · direct organization/synthesis of linked knowledge · verify citations by navigation · keep a personal knowledge system | **Codex app** + **Obsidian** (interface) | **Mastery:** make institutional and personal knowledge a system a thinking machine can work inside with you—so answers span many sources with trails you can walk, instead of living only in your head or a disposable chat. **Thinking:** retrieval as agentic search over *your* structure; director questions span many notes with traceable links |
| **Wed** | **AM case talk** | **Harness case talk** | Same 45-minute pattern: real problem, harness role, experience; 30 + 15 before lunch. Theme pairs with knowledge/trails (or poison near-miss). | Same as Tue case talk, knowledge-shaped | Lead live · student discussion | Same as Tue case talk |
| **Wed** | **P5 PM** | **The poisoned corpus** | Rigged intake hits the vault: false citation, field contradiction, hostile instruction—detect all three mechanically and prove containment. | Detect poisoned/hostile intake · use triage discipline · confirm catches personally · compare how another harness expresses the same bound — **OpenCode resolves permission rules last-match-wins, so a later `allow` overrides an earlier `deny`**; read a rule set and predict what it permits before you trust it | **Codex app** (permission mode) + **OpenCode** (`permission` rules in `opencode.json`; Claude optional extra) | **Mastery:** keep a powerful knowledge aide without surrendering your picture of the world—detect falsehood, contradiction, and hostile instruction before they become your operating picture. **Thinking:** verdicts are non-delegable; containment is absence of the hostile effect, not a chat promise |
| **Thu** | **P6 AM** | **The watch officer** | Adapt `watch_officer.yaml` over a local feeder; write a two-column autonomy contract whose **tool** column names real goose levers (recipe, extensions, mode/max turns, retry, schedule); stop/restart; exception drill; schedule or honest block; Pi bare-loop contrast. **Stretch — endpoint wall:** same recipe on staff-pinned **Ollama/LM Studio**; hold/degrade vs cloud. | Own a **harness loop** under contract · map tool-enforced vs procedure-enforced · prove stop/restart · unattended path honesty · name rails missing in Pi · *(stretch)* endpoint as harness wall | **goose** (recipe + levers; CLI default) + **Codex app** (support) + **Pi** (no-rails demo); stretch: local provider | **Mastery:** design work that continues under a contract you wrote—so your attention moves to command, exceptions, and stop authority, not babysitting every step of a capable machine. **Thinking:** autonomy = loop + bounds you wrote; goose’s tool column is levers you turned on, not brand safety; local is a wall you measure, not a vibe |
| **Thu** | **AM case talk** | **Harness case talk** | Same 45-minute pattern before lunch. Theme pairs with autonomy under contract / stop authority. | Same as Tue case talk, autonomy-shaped | Lead live · student discussion | Same as Tue case talk |
| **Thu** | **After lunch** | **Browser → deck lead demo** | 30 min staff-only live demo: built-in browser pulls scoped public facts and collates a short slideshow; verify one claim; stop a runaway expand. Students watch — no plugin install, no Chrome extension. | Name `@Browser` / `@Chrome` / `@Computer` · scoped sources · `browse ≠ verified · deck ≠ truth` · stop authority | **Codex app** on **staff** machine only (`lead/BROWSER_DECK_DEMO.md`) | **Mastery:** keep contract + evidence language when an agent can browse and ship a polished deck. **Thinking:** pretty slides are still draft; site allow-lists and your interrupt are the bounds; not a pipeline |
| **Thu** | **P7 PM** | **The automation line** | Visual n8n flow: rows/reports → AI classify/extract → validate → master sheet; exceptions hold at a human-approval node. Opens after the browser → deck demo. | Build pipeline automation with AI inside · keep a human gate · contrast agent loop vs fixed path · extend 30-60-90 (which work becomes agent vs pipeline) | **n8n** + AI API step; **Codex app** (support) | **Mastery:** choose the right machine for the job—adaptive agent versus fixed path with a human gate—so volume work scales without forcing you into either chaos or rubber-stamp automation. **Thinking:** this is **not** a harness loop—one pass, designed path; different machine, same need to keep judgment on the exceptions |
| **Fri** | **P8 AM** | **Operator-governed open model** | Write AUP before touch; re-point pack + frozen suite to hosted open model; measure hold/degrade and whether the loop still closes; legitimate-but-refused task under your policy; 90s defense; finalize 30-60-90. | Author endpoint policy first · measure model dependence as numbers · locate failure layers · defend accept/reject · transfer plan you can run at work | **Codex app** (re-pointed) + **Starzl-hosted open model** | **Mastery:** make the week’s method survive vendor, model, and policy change—so the thinking aide is an operating capability you transfer, not a rental that dies when one product or endpoint moves. **Thinking:** guardrails moved to you; capability tax is measured loop completion, not vibe; instructions outlive session, agent, and model |

## Cross-cutting

- **School type:** operator’s school — deep operator mastery of AI direction and cothinking (`MEMORY.md`)
- **Lead posture:** live operate-along on screen · talk-through + side lectures · real-time AI for depth/diagrams · students still run their own pulse (`MEMORY.md` Teaching posture)
- **Delivery medium:** **course site** holds all exercises and materials — not a deck series (`MEMORY.md` Delivery medium)
- **Site look:** Starzl paper + mark (PDF system) and starzl.com altitude — `site/VISUAL_SYSTEM.md`
- **Learner voice:** warm guide-beside — complete, plain explanations; define concepts when needed (`MEMORY.md`)
- **Primary Assistant home:** Codex app — Codex mode in the **ChatGPT desktop app** (desktop only; no CLI)
- **Required install set:** Codex app · **OpenCode** · Pi · goose
- **Optional:** Claude Code (alternate/third engine — not required for GREEN or course pass)
- **Platform baseline:** Windows 11, no WSL required; student-owned install via **pre-work module** (`prework/`) — not a golden image
- **Pre-work:** students install Codex app · **OpenCode** · Pi · goose · Git/Node/Python · Obsidian · n8n; **verify at the end of each setup step** (no separate health-check pass). Claude Code optional. Monday AM **install clinic** closes gaps.
- **Harness case talks:** Tue/Wed/Thu AM, last ~45 minutes before lunch (30 present + 15 discuss). Guide: `lead/HARNESS_CASE_TALKS.md`.
- **Browser → deck lead demo:** Thursday after lunch, 30 minutes, before P7. Staff Windows machine only; students do not install. Script: `lead/BROWSER_DECK_DEMO.md` (default: `@Browser` → `slideshow.html`; optional PPTX via Computer Use).
- **Many Minds stretch (P3):** `mission_flesh/p3/MANY_MINDS.md` + `instruments/p3_multi_agent/` — subagents after twin-engine MVP; not GREEN.
- **Local endpoint stretch (P6→P8):** `mission_flesh/p6/local_endpoint_notes.md` — staff-pinned Ollama/LM Studio; hold/degrade; not clinic GREEN.
- **Harness-loop arc:** Mon name it → Tue improve the harness → Thu bound / bare / non-loop → Fri does the loop still close
- **Mastery north star:** a thinking machine as a durable work partner under your judgment—systems you can direct, verify, bound, and transfer—not clever chat and not speed for its own sake
- **Cothinking standard:** human owns mission, bounds, and verdict; machine proposes and executes inside the harness; evidence beats self-assessment
- **Operator ritual (every block):** co-write `DIRECTION_BRIEF.md` with AI before the run (status LIVE) · mission in a build chat · co-write `OPERATOR_LOG.md` after · separate Codex chat `Operator — Direction & Log` · AI interviews/drafts/challenges; operator owns verdict · ≤5 min dialogue pre / post
- **Adversarial review (every block):** new chat `Adversarial — [block]` · frozen prompt in `operator/ADVERSARIAL_REVIEW.md` · attacks verdict + MVP claims · log stood/wounded/failed · in-course substitute for peer challenge; human challenger remains a transfer seed
- **Measurement spine (every block):** `operator/MEASUREMENT_SPINE.md` after adversarial · ritual health · mission accomplishment · work quality · time to result · student board + thin facilitator rollup
- **Course instruments:** `instruments/` — shared P2 dyno · P3 frozen brief · P3 multi-agent (Many Minds stretch) · P8 hold/degrade; tracks `engineering` | `mission_ops` (choose once); P8 reuses P2 IDs D01–D05
- **Pass bars:** `operator/PASS_BARS.md` — mastery-floor MVP per cap 1–9 (not “it ran”); stretch + side-quests; student+AI stress-check after log; distinction = floor + depth on ≥4 including P2/P5/P8
- **Transfer outer loop:** own chat `Operator — Transfer 30-60-90` · interactive AI session **after every AM and PM** · `TRANSFER_30_60_90.md` living file · deep seeds P2/P3/P5/P6/P7 · **SEALED** at P8 · not a Friday worksheet
- **Default surface:** app UI (project folder → permission mode → brief → accept/reject). Terminal is support/stretch, not the default chair

## Tool rotation (compact)

| Day | Working tool | Joins / comparison |
|---|---|---|
| Mon | Codex app | Install clinic closes stack · then First Light |
| Tue | Codex app | **OpenCode** (P3 second engine / Grok) |
| Wed | Codex app | Obsidian + OpenCode (bounds/permissions compare on P5) |
| Thu | Codex app | goose + Pi (AM) · **lead browser→deck demo after lunch** · n8n (PM) |
| Fri | Codex app | Hosted operator-governed open model |

## Pre-work module (before Monday) — student-owned install

**No golden image.** Students install and configure their own workstation. See `prework/`.

| Artifact | Purpose |
|---|---|
| `prework/README.md` | Module overview and done criteria |
| `prework/INSTALL_GUIDE.md` | Step-by-step install with **per-step verification** (Windows 11, no WSL) |
| `prework/SETUP_LOG.md` | Failure/fix trail (operator evidence) |
| `prework/FACILITATOR_NOTES.md` | Support window, Monday clinic, rescue |
| `lead/COHORT_PIN.md` | Staff pin sheet (versions, models, LOCAL PIN, cold-smoke) |
| `lead/HARNESS_CASE_TALKS.md` | Tue/Wed/Thu AM case-talk shape |

### Pre-work done when
1. Stack installed and configured against your three keys  
2. Each major setup step’s **verify** checks passed (fresh terminal where PATH changed)  
3. Setup log records at least one real failure and fix  
4. Four agents each created a file in `prework-smoke` you can see in Explorer  

(Optional offline sheet `prework/HEALTH_CHECK.md` exists only as a rescue re-test — not the primary path.)

### Monday AM contact hours
- **Install clinic** (~2 hours expected, **no hard boundary**): finish gaps, re-verify, smoke four agents under staff eyes  
- Then operator pulse + **First Light** mission  
- Still RED after clinic → parallel rescue; do not redefine the school as imaging  
- Do not burn the whole morning re-teaching winget from zero for people who skipped pre-work — clinic is finish-and-prove, not replace pre-work
