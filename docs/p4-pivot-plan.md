# P4 pivot: Second brain via Obsidian MCP (OpenCode only)
## Status
**Conditional go.** Educational pivot approved. Integration design revised before build. Do not curate the large corpus until the Windows MCP/permissions spike and a 12-document vertical slice pass.

> **Current P4 setup:** The live vault is `%USERPROFILE%\Vaults\p4-vault`. The setup launcher copies vault content but excludes `.opencode` and `.obsidian`; it does not change Windows ACLs or folder attributes. Older `Documents\p4-vault` references below are design history.
## Problem
P4 currently treats Obsidian as a **human viewer** on a folder Codex edits as normal files. The approved pivot is different: Obsidian is the **AI second brain**, the agent reaches it through **Obsidian Local REST API’s built-in MCP**, and the **only agent harness for P4 is OpenCode** — no Codex in this module.
Title **Second brain** is accurate. New capability is **not** “parallel OpenCode on a big local corpus” (P3 + PG already teach that). New capability is: **MCP as the only sanctioned write path into a persistent store**, plus **structuring that store so a cold session answers from it**.
## Host decision (locked)
* **OpenCode only** for all agent work in P4 (interactive + any scripted runs).
* **No Codex** chats, projects, `/goal`, or Codex MCP config in P4 stages.
* **Obsidian** remains the human vault UI for audit and navigation — outside the OpenCode project.
* **Python verifiers** seal the brain and the baseline (new code; not a light adapt of the MERIDIAN verifier).
* Model: course xAI path already used with OpenCode (`$env:HB_XAI_MODEL`), unless a later decision changes it.
* **Boundary stack (not “MCP alone”):** project topology + OpenCode per-agent permissions + denied FS/shell tools + MCP tool-specific permissions + human approval + observable MCP tool receipts.
## Current state (repo facts)
* Live page: `site/blocks/p4.html` — Codex-centric director harness, Obsidian as viewer, Python verifier, baseline for P5.
* Seed vault: `mission_flesh/p4/vault_seed/` (inbox, Source_Packet, Harness, MOC, AGENTS.md, tools).
* Verifier: `mission_flesh/p4/vault_seed/tools/verify_vault.py` (~1920 lines) welded to MERIDIAN (claim IDs, Morning_Brief, People/Systems/Events/Decisions hubs, Answers/Q1|Q2, `.codex/agents/director_evaluator.toml`). **Replacement, not adaptation.**
* Schedule in `site/js/registry.js`: **PG = Tuesday PM** (Unattended workers); **P4 = Wednesday AM**; P3 Tuesday PM already uses large local evidence + citations. Journey board places PG before P4.
* Prework installs Obsidian; OpenCode + xAI already required for PG (before P4).
* Tuesday MCP briefings teach connect / primitive / bound authority — P4 applies that method on OpenCode against one real product brain.
* **P4 role (corrected):** attended **consolidation after PG** — apply known parallel OpenCode skill to MCP-backed second brain + retrieval design + human audit. Not the first OpenCode comfort block.
* **P5 depends on P4:** path `Documents\p4-vault`, external `operator/evidence/P4_BASELINE_[TODAY].json`, student check for `MOC.md` **and** `Morning_Brief.md` (`p5.html` ~167–173), seed verifier before/after hostile intake, hostile file `intake_06_directors_update.md` targets Morning_Brief/Systems. **P5 edits are required**, not optional. Keep path `Documents\p4-vault`.
## Teaching delta (what is actually new at P4)
* MCP write path into a persistent product brain with tool-level deny/ask.
* Vault outside OpenCode project; workers never hold vault write.
* Note schema + hubs + route spine designed for retrieval.
* Cold session answers graded queries from the brain only.
* Human audit sample + one MCP repair cycle.
* Execution evidence (MCP receipts + permission config) proves write path; Markdown alone cannot.
* Parallel dispatch is a **short applied step** with one-line callback to PG — not a full teaching stage.
## Domain content (locked)
**Mission question the second brain must support:**
What does open-source evidence say about the **logistical challenge of moving a main battle tank from the Los Angeles area to Taiwan**, end to end — and what **adversarial interference** (ambush, sabotage, interdiction) matters at **tactical and theater** levels along that path?
**Not** a generic OSINT wiki, and **not** the old MERIDIAN inbox/Morning Brief packet as primary corpus.
### Scope the brain must cover
**Movement & modes (all that apply, not rail-only):**
* Origin handling in/near Los Angeles (depot/railhead/port interfaces).
* **Rail** inland: loading gauge, heavy-duty flatcars, route clearances, bridges/tunnels, speed, escorts, commercial vs military rail practice (public sources).
* **Road** drayage/oversize heavy-haul where rail does not reach.
* **Port / terminal** ops: heavy-lift, roll-on/roll-off vs lift-on/lift-off, staging, dwell.
* **Sealift** across the Pacific: vessel types, embarkation, lashing/stability, convoy vs commercial charter framing (public doctrine/logistics lit).
* **Air** only where relevant as contrast (usually not primary for a tank) — note limits honestly.
* **Last leg into Taiwan:** port of entry, inland rail/road, bed-down — public infrastructure and policy sources only.
**Factor bases (all that matter):**
* **Physical:** weight/dimensions, route clearances, climate, sea state seasonality, infrastructure capacity, time-distance.
* **Legal / regulatory:** export/import controls, customs, hazardous/oversized movement rules, host-nation and U.S. public statutes/regs, sanctions/ITAR-adjacent public guidance (no classified).
* **Operational:** scheduling, handoffs between modes, contracting, force protection logistics, C2 of the move, spare/recovery, fuel/POL touchpoints where public.
* **Economic / commercial:** carriers, market constraints, cost/time tradeoffs from open reporting.
* **Political / strategic context:** publicly discussed theater access, chokepoints, crisis closure of sea lanes (analysis, not secret intel).
**Adversarial / threat layer (defensive only):**
* Open-source **published vulnerability classes** and historical interdiction/sabotage patterns for rail, ports, and sealift (doctrine, history, professional journals, reputable OSINT) — framed as **protection requirements**.
* What doctrine/public analysis says must be **hardened, redundant, or monitored** along a heavy LA→Taiwan move; how delays cascade if a node fails.
* Notes terminate in **defensive implications** (protect / detect / recover), not attack geometry or targeting studies.
* Separate notes: claim vs source, confidence, uncertainty, contradictions.
### Safety / classroom posture (tightened)
* Public, legal sources only. No classified, no credential stuffing, no live targeting of private individuals.
* Explicit prohibitions in briefs and schema: target ranking; precise exploitable weak points; access methods, timing, or evasion; stepwise sabotage instructions; optimization of attack effects; operational targeting of real infrastructure.
* Prefer authoritative logistics/doctrine/history over “how to sabotage” scrapes.
* Student product is a **cited second brain + brief from the brain**, not an ops order to execute harm.
### Two stores (locked)
1. **Raw corpus warehouse (pre-built):** versioned release archive of curated public docs for tank LA→Taiwan logistics + defensive threat material. Built by authors after the contract spike. Students do **not** live-crawl in class. Download in **prework**, not Wednesday AM.
2. **Second brain (Obsidian vault, thin scaffold at start):** students’ agents process a **fixed assessed slice** of the warehouse and write structured notes **only through sanctioned MCP tools**.
Graded path = transform assessed raw slice → brain, not collect from the internet tomorrow.
### Corpus scale (revised)
* Warehouse target: **~300–600 curated, tagged documents** (not padded thousands). Quality over bulk; avoid near-duplicate noise and multi-GB wifi events.
* **Assessed mission slice:** fixed **60–120 documents** selected from MANIFEST with stratified quotas (mode, factor, geography, source type, threat/defensive). Four workers process this slice in class.
* Ship as **versioned release archive + SHA-256**; prefer release asset over Git LFS for classroom reliability. Manifest includes **redistribution-rights** field (publicly accessible ≠ redistributable).
* Optional larger warehouse breadth only after timed pilot passes.
### How the vault gets filled
* Parallel OpenCode **research workers** read **assigned assessed-slice paths only** (no web, no MCP, no general FS write).
* Each returns structured bundles with the **full citation schema** (below).
* **Director** merges into Obsidian **only via allowed MCP tools** (writes = ask/approve).
* Human audits a sample in Obsidian; rejects unsourced/overconfident notes.
* Capture **OpenCode MCP tool events + permission config** as execution evidence for “write path used.”
* Optional stretch: one live web refresh — not required for outcomes.
### Citation schema (required on worker output and vault notes)
* Stable source ID
* Raw path
* Source-file SHA-256
* Original URL
* Publisher and document date
* Retrieval date
* Page / section / paragraph locator
* Exact supporting excerpt
* Agent claim or paraphrase
* Confidence and uncertainty basis
* Contradictions or missing evidence
* Route leg, mode, factor, and threat/defensive tags
### Why pre-build the raw pack (agreed)
* Classroom reliability (no mass rate-limits / empty results / 3-hour crawls).
* Shared ground truth for grading and for parallel agents.
* Separates **collection** (build time) from **second-brain engineering** (student job).
* Safer source control and redistribution review.
* Matches P3 pattern: big corpus on disk, agents work a bounded surface — with a **graded slice** so runtime fits.
## Target teaching arc
**Spine:** (PG assumed) → Obsidian + Local REST MCP up → bound brain tools → short parallel process of **assessed raw slice** → director MCP-writes second brain → structure for retrieval → human audit → cold query from brain only → seal baseline for P5.
Protect under time pressure: **MCP write boundary + retrieval design + audit/cold query**. Compress parallel dispatch.
### Stage 1 concept map (new P4)
1. **Frame** — Build a second brain for heavy armor LA→Taiwan logistics (all modes, all factor bases) plus **defensive** adversary/vulnerability material. OpenCode directs; Obsidian stores; MCP is the only sanctioned write path.
2. **Orient** — Deliverable = linked logistics/defensive vault + proof you can brief from it without re-reading the warehouse; prereqs (PG done; OpenCode known; corpus downloaded in prework); no Codex.
3. **Ideas**
    * Second brain vs chat scrap.
    * Attended consolidation after PG (callback only — not re-teach parallel workers).
    * Single-writer merge contract + director-only MCP writes.
    * Boundary stack: topology, permissions, denied tools, MCP tool allow/deny/ask, receipts, human approval.
    * Multi-factor logistics must not collapse into one “rail only” note.
    * Threat notes end in protection requirements — not targeting studies.
    * Retrieval design: hubs Modes, Nodes, Constraints, Threats (defensive), Sources; route spine.
4. **S01** — Create/open vault in Obsidian **outside** OpenCode project; pin Local REST API plugin; vault identity smoke test.
5. **S02** — OpenCode project topology; register Obsidian MCP; agent permission files; MCP read smoke + **ask-gated** write smoke; save permission + receipt evidence.
6. **S03** — Research brief + note/citation schema; assessed-slice assignment from MANIFEST.
7. **S04** — **Short applied step (~10 min teach / run):** dispatch parallel OpenCode researchers on assessed-slice partitions (callback to PG). Read assigned raw only; no vault write; no web.
8. **S05** — Director merges via MCP; notes carry full citation schema; link route spine; update MOC (+ any P5-required root notes per locked contract).
9. **S06** — Structure pass; cold OpenCode session answers graded queries **from the brain only** (rail constraints out of LA; sealift options; protection requirements at chokepoints; delay cascades if a node fails) with citations to vault notes.
10. **S07** — Human audit sample in Obsidian; one MCP repair cycle.
11. **S08** — Baseline freeze (`verify_baseline.py`); handoff; transfer seed.
12. **Outcomes** — MCP-path evidence; multi-mode + factor coverage; defensive threat sourcing; cold retrieval pass; baseline for P5.
### Topology and permissions (locked design intent)
* **OpenCode project:** controller files, raw corpus (or assessed slice paths), worker outputs, evidence receipts. **Not** the Obsidian vault root.
* **Obsidian vault:** `Documents\p4-vault` (keep path). Outside project. Human opens in Obsidian.
* **Researchers:** raw-corpus/slice read only; no web; no MCP; no general filesystem writes.
* **Director:** worker-output read; filesystem edit/bash **denied** for vault paths; MCP reads allowed; MCP writes **ask**; dangerous MCP tools **denied**.
* **API key:** environment variable only.
* **Local REST API MCP tool policy:** allow read/search; write/append/patch = ask; **deny** delete, move, copy, active-file writes, command execution.
### Parallel agent pattern (default)
* **Director (attended OpenCode):** brief, merge rules, all Obsidian MCP writes (ask), stop/handoff, evidence capture.
* **Workers (parallel, corpus-processors)** on assessed slice:
    1. CONUS origin + rail/road.
    2. Port + sealift + Taiwan arrival.
    3. Cross-cutting constraints (legal/regulatory, commercial, timing).
    4. Defensive threat / protection-requirements material.
* Workers read **assigned paths/tags only**; return structured bundles with full citation schema.
* Optional collapse to **3 workers** if class time is tight.
* **Fan-in:** reject findings without complete citations; dedupe; one note path per kept object; link LA → rail → port → sea → Taiwan.
* **Cap:** per-worker doc caps so total fits ~165 minutes with retrieval/audit protected.
## Proposed product changes
### A. Pin Obsidian Local REST API built-in MCP (OpenCode client)
* Use **Obsidian Local REST API** plugin’s **built-in authenticated MCP endpoint** (no separate third-party bridge process).
* Pin exact plugin version + course OpenCode build + model + HTTP/TLS notes.
* API key via **env var only**; document port/TLS; OpenCode MCP registration; smoke: inspect + read + ask-gated write.
* Tool allowlist as above; deny delete/move/copy/command/active-file writes.
* Vault identity printed in every smoke test.
* Windows clean-box spike is a **gate** before corpus spend.
### B. Vault contract + verifiers (front-loaded; explicit replacement)
Replace `verify_vault.py` MERIDIAN contract with two tools:
1. **`verify_brain.py`** — note schema, source lineage, hub/spine links, coverage quotas, retrieval-answer artifacts, audit sample, **permissions + MCP receipt evidence**.
2. **`verify_baseline.py`** — generic frozen-tree manifest writer/checker consumed by P5 before/after intake (path/hash only; no Morning_Brief semantics).
Lock required-artifact set **before** corpus curation. Keep `Documents\p4-vault`. Decide which root notes P5 will name (drop or replace `Morning_Brief.md` with a second-brain equivalent such as `Mission_Brief.md` / `Retrieval_Answers.md` — pick in contract spike).
### C. Rewrite `site/blocks/p4.html`
* Rename module to **Second brain** (title, h1, registry name/title/meta).
* Full STE narrative; plain language; purpose-before-procedure.
* Strip Codex-specific UI; OpenCode-only attended flows.
* Keep block code `P4`; revise check IDs for new outcomes (MCP smoke, permissions evidence, assessed-slice process, MCP merge, cold retrieval, audit, baseline).
* Framing: Obsidian = logistics/defensive brain; MCP = sanctioned door; OpenCode = harness; parallel workers = short applied step after PG; retrieval + audit = core outcomes.
### D. Vault seed, corpus, agent files
* Thin seed: hubs (`Modes`, `Nodes`, `Constraints`, `Threats`, `Sources`, `MOC`), route spine stub, note template, research brief, harness/evidence folders.
* Stop shipping MERIDIAN inbox/Morning Brief as primary P4 load.
* OpenCode agent files: director (MCP ask-write, FS vault deny); researchers (slice read only).
* Release-asset raw warehouse + MANIFEST + assessed-slice list; thin Obsidian seed separate.
### E. P5 edits (required — concrete list)
* `site/blocks/p5.html`: orient copy that P4 built a “personal director loop” (~55); tools line if still Codex-only (~32); leave-with / before-you-start baseline language (~68, ~76); Stage 01 vault confirmation naming `Morning_Brief.md` (~167–173); any Direction brief paste that assumes MERIDIAN shape (~193+).
* `mission_flesh/p5/intake/intake_06_directors_update.md` and any other intake that targets Morning_Brief/Systems/old hubs — retarget to new root notes.
* Any recovery/capability/measurement/diagram copy that names old P4 artifacts.
* Wire P5 to **`verify_baseline.py`** (or renamed generic checker) + external `P4_BASELINE_[TODAY].json`.
* Keep trusted path **`Documents\p4-vault`** unless a later decision forces rename (default: keep).
### F. Registry, prework, cross-links
* `registry.js` P4 name/title/meta: Second brain · OpenCode + Obsidian MCP + retrieval.
* Journey/Wednesday blurb: second brain / trusted knowledge — not “personal director harness” if inaccurate.
* Prework: OpenCode already required for PG; add **corpus download + SHA-256 verify** and Local REST API plugin pin before Wednesday.
* Describe P4 as **attended consolidation after PG**, not OpenCode intro.
* Update transfer language, measurement spine, capability docs as touched.
## Out of scope unless requested
* Rebuilding Tuesday MCP lectures in full.
* Codex in P4.
* Classified/non-public collection, people-targeting, credentialed dark APIs.
* Multi-writer workers holding Obsidian MCP write tools.
* Replacing P5’s poisoned-corpus lesson (retarget intake/artifacts only).
* Reordering PG and P4 on the calendar (prefer narrative fix: consolidation after PG).
* Padding corpus to thousands for its own sake.
## Risk notes
* **Gate risk:** pinned Windows stack (Obsidian + Local REST MCP + OpenCode permissions + env key) must enforce and demonstrate write boundary in classroom time — spike first.
* Markdown cannot prove MCP path — need receipts + permission evidence in verifier.
* Students may still bypass via FS if vault is reachable — topology + denied tools + grade receipts.
* Wrong vault / wrong plugin settings = wrong brain — identity smoke required.
* Hallucinated tradecraft — full citation schema + defensive-only threat brief + reject incomplete notes.
* Workers invent outside pack — no web by default; permissions enforce.
* P5 coupling is schedule-critical — contract + baseline tool before page rewrite.
* Release-asset download failures — prework download + checksum; not Wednesday wifi.
* Timed pilot may force cut of worker count or slice size — protect retrieval/audit stages.
## Implementation order (revised — technical gate first)
1. **Windows technical spike** — pin OpenCode, Obsidian, Local REST API (MCP), model, HTTP/TLS, env API key, director/researcher permission files; prove read + ask-write + deny dangerous tools + vault-outside-project.
2. **12-document vertical slice** — worker → director MCP write → cold query → audit → `verify_brain` + `verify_baseline` → P5-style manifest check. Full workflow on tiny corpus.
3. **Lock contracts** — note/citation schema, required artifacts, MCP receipt format, permissions, P5 interface (root notes, intake retargets, baseline tool). Everything else derives from this.
4. **Corpus** — curate warehouse (~300–600) + MANIFEST (incl. redistribution-rights) + fixed assessed slice (60–120) as versioned release archive + SHA-256; prework download instructions.
5. **Rewrite content** — `p4.html`, required `p5.html` + intake targets, registry, prework, cross-links, capability/measurement copy; backup pre-pivot pages.
6. **Timed pilot** — full learner run against ~165-minute limit; cut scope if retrieval/audit slip.
7. **Scale warehouse breadth only after pilot passes.**
8. Commit only when you ask.
## Immediate next step when executing
Start with step 1–3: spike + vertical slice + propose the locked vault/P5 artifact contract for approval before any large corpus crawl.
