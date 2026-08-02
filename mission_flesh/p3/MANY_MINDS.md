# Many Minds, One Commander

**Block:** P3 stretch (Tuesday PM)  
**Time:** about 50–70 minutes for the full mastery path; do not skip the baseline
**Home tool:** Codex app with `gpt-5.6-terra`<br>
**Pack:** `instruments/p3_multi_agent/`  
**Pass bar home:** `operator/PASS_BARS.md` · P3 Stretch  

This guide stands beside you at the keyboard. You already finished the twin-engine desk. Now you will build a source-backed review of a small service pack with **several specialist runs under one human commander**, then decide from the saved baseline and delta whether the added parallel spend improved the work.

---

## What this is for (read before any click)

When one chat does everything — explore, test, security, write-up — the useful signal gets buried under noise. The room fills up. Later answers get worse even though the model is the same. People call that **context pollution** (good facts drowned) and **context rot** (performance slides as the chat fills with less relevant detail).

A **subagent** is a specialist Codex starts for one bounded job. It works in its own agent thread, then returns a **summary** to your main chat. You stay the commander: you write the brief, you choose the lenses, you wait for all, and you own the merge and every disposition.

That is not the same craft as P3’s twin-engine work:

| Craft | What differs | What stays yours |
|---|---|---|
| **Second engine** (OpenCode) | Different product / model family; separate run context | Brief frozen; shared corpus; adjudication against sources |
| **MCP server** | Reusable access to a bounded data or tool surface | Permission, provenance, source verification; never another opinion |
| **Subagent** (Codex) | Same product; parallel specialists; summaries return to one chat | Division of labor; wait-for-all; synthesis; disposition of claims |
| **Second human** | Another person with real judgment | You still own the operational call when you are commander |

If someone calls all of this “cowork,” gently correct them. **Cowork** is a different product name on a subscription path this course does not use. Here the words are **subagent** and **commander**.

### The mastery move (why this is not a feature tour)

Anyone can paste “spawn three agents.” Mastery is:

1. **Baseline first** — one commander, no subagents, same pack, written findings.  
2. **Parallel second** — three lenses, wait-for-all, synthesis on disk.  
3. **Delta** — what parallel added, missed, or invented, in a table you can defend.  
4. **Evidence-backed dispositions** — keep, demote, or discard every specialist claim using **corpus evidence**; zero discards is valid when the corpus supports them all.

If you only have the synthesis file, you ran the product. The baseline and defended delta are what show whether parallel added value.

---

## Map of the hour

| Part | About | You leave with |
|---|---|---|
| 1. Baseline (required) | Single-chat review, no subagents | `out/baseline_single.md` |
| 2. Subagent run | Three lenses, wait-for-all, synthesis | `out/many_minds_synthesis.md` |
| 3. Delta + decision review | Compare baseline vs parallel; resolve real uncertainties | `out/many_minds_delta.md` |
| 4. Close | Log + transfer seed | Stretch claimed only with evidence |

Permission mode stays **Ask for approval**. Subagents inherit the parent’s permission mode and sandbox. Set the mode **before** you ask to spawn.

Every Codex chat in this stretch uses **GPT-5.6 Terra** (`gpt-5.6-terra`) with the OpenAI API key stored in Codex sign-in. Do not leave a chat on Default or Sol. This stretch does not use an Anthropic key.

Where a chat name shows `[TODAY'S DATE]`, replace it with today's date in `YYYY-MM-DD` form, without brackets. Use the same date throughout P3.

Spend note: each subagent does its own model and tool work. Parallel is richer and **more expensive**. Cap at three specialists in class.

Notice what kind of cap “three” is. It lives in the wording of a prompt, which makes it **procedure-enforced** — it holds because the model cooperates and you are watching. Codex also has a real setting, `agents.max_concurrent_threads_per_session`, which caps concurrent spawned threads whether the prompt cooperates or not. That one is **tool-enforced**. You will name that distinction formally on Thursday; today you are living on the procedural side of it, so keep an eye on the thread count yourself.

Prefer **read-only** review today so you do not invent merge conflicts for sport.

---

## Before you start

- [ ] Twin-engine MVP is done or within a few minutes of done (do not skip the floor for this stretch)
- [ ] `p3_evidence` is disabled in `p3_desk\.codex\config.toml`; the Many Minds baseline must not inherit the MCP path
- [ ] Codex app open; sign-in uses the **OpenAI API key stored in Codex**; model is **GPT-5.6 Terra** (`gpt-5.6-terra`)
- [ ] Permission mode: **Ask for approval**
- [ ] You are in the **course repo root** (the folder that contains `instruments/` and `mission_flesh/`)
- [ ] You can browse `instruments/p3_multi_agent/corpus/` in Explorer

```powershell
# From the course repo root
New-Item -ItemType Directory -Force -Path ".\instruments\p3_multi_agent\out" | Out-Null
```

---

## Part 1 · Baseline — single commander, no subagents (required · about 15–20 minutes)

Parallel helps when work is read-heavy and splits cleanly into lenses. It hurts when specialists collide on writes, return overlapping lists with no synthesis, or run without a baseline that shows whether the extra spend improved anything. This review stays read-only, and the baseline makes the value decision measurable.

Do this **before** any spawn. If you skip it, the stretch is not yet under the mastery bar — only under a demo bar.

### 1.1 Open a baseline chat

```text
P3 — Many Minds Baseline — [TODAY'S DATE]
```

Create this chat in Codex and select **GPT-5.6 Terra** (`gpt-5.6-terra`) before you paste the baseline prompt.

### 1.2 Frozen baseline brief (paste exactly)

```text
You are a single reviewer. Do NOT spawn subagents. Do NOT implement fixes. Read-only.

Pack (read only):
instruments/p3_multi_agent/corpus/
  service_snippet.py
  tests_snippet.py
  NOTES_ops.md

Write ONLY:
instruments/p3_multi_agent/out/baseline_single.md

Format:
## Findings
For each finding (max 8):
- ID: B1, B2, ...
- Claim (one sentence)
- Evidence: file + symbol or short quote from the corpus
- Severity: S1 / S2 / S3
- Lens you would have used if parallel: correctness | tests | spec-drift

## Still unsure
Bullets for anything you noticed but could not evidence.

## Stop
No edits to corpus files.
```

### 1.3 Baseline evidence checklist

- [ ] `out/baseline_single.md` exists in Explorer  
- [ ] Every finding has **corpus evidence** (file + symbol or quote)  
- [ ] You did **not** spawn subagents in this chat  

If the model spawns anyway, stop and restart the baseline chat. The comparison is ruined if parallel leaks into the baseline.

---

## Part 2 · Subagent run (about 25–35 minutes)

### 2.1 Open a commander chat

```text
P3 — Many Minds Commander — [TODAY'S DATE]
```

Create this chat in Codex and select **GPT-5.6 Terra** (`gpt-5.6-terra`). Keep baseline and twin-engine work in other chats.

### 2.2 Point at the pack

```text
Working pack (read-only):
instruments/p3_multi_agent/corpus/
  service_snippet.py
  tests_snippet.py
  NOTES_ops.md

Write only under:
instruments/p3_multi_agent/out/
```

### 2.3 Frozen multi-agent brief (paste exactly)

Do not “improve” the lenses mid-run. If you must change the job, save `MANY_MINDS-v2` and label the stretch as a variant.

```text
You are the commander. Do not implement fixes. Read-only review only.

Spawn exactly three subagents in parallel. One agent per lens. Wait for all three before you synthesize.

Lenses:
1) Correctness & edge cases — input handling, boundaries, failure behavior
2) Test gaps — what tests_snippet.py fails to prove; name missing cases
3) Spec drift — contradictions between NOTES_ops.md and the code

Rules:
- Each subagent may read files under instruments/p3_multi_agent/corpus/ only.
- No file edits. No refactors. No “while I was here” cleanups.
- Each subagent returns: up to 5 findings; each finding needs file + symbol or line cue; severity S1 (must fix) / S2 (should fix) / S3 (note).
- After all three return, you (commander) write instruments/p3_multi_agent/out/many_minds_synthesis.md with:
  A) Table: lens | finding_id | claim | severity | file cue
  B) Merge: dedupe overlapping findings; keep the strongest wording; note which lenses overlapped
  C) Dispositions: keep, demote, or discard every specialist finding — each reason must cite corpus evidence or clear out-of-scope. Do not force a discard.
  D) Operator still owns: one paragraph on what a human must still decide
  E) One sentence: MCP server ≠ engine ≠ subagent ≠ human
  F) Do not read or mention baseline_single.md

Begin. Wait for all subagents. Then write the synthesis file.
```

### 2.4 While it runs

| Moment | What it means |
|---|---|
| Subagent threads appear | Specialists off the main chat |
| You open a subagent thread | Inspect raw work; watch for lens bleed |
| Commander writes to disk | Orchestration counts only if Explorer shows the file |
| Approval prompts | Same sandbox story — you still gate the chair |

If Codex edits the Python files, **stop** and restate: read-only; synthesis only.

### 2.5 Synthesis evidence checklist

- [ ] Three lenses ran (three threads or three clear returned blocks)  
- [ ] `out/many_minds_synthesis.md` on disk  
- [ ] Merge shows **dedupe** (not nine raw lines pasted)  
- [ ] Every reported finding has a corpus-backed keep / demote / discard disposition; zero discards is valid
- [ ] Naming sentence present  
- [ ] Your own one-line agree/disagree on the merge in the operator log  

---

## Part 3 · Delta sheet + decision review (required · about 15–20 minutes)

This is the stretch’s measurement moment. Without it, parallel is a story.

### 3.1 Build the delta (you may use a short Codex assist, but you own the cells)

Create `instruments/p3_multi_agent/out/many_minds_delta.md` with this shape:

```text
# Many Minds delta

## Counts
| | Baseline (single) | Parallel (synthesis) |
|---|---|---|
| Findings kept | | |
| S1 count | | |
| Distinct file:symbol targets | | |

## Unique to baseline (parallel missed or dropped)
| ID | Claim | Why it matters that parallel missed it |
|---|---|---|

## Unique to parallel (baseline missed)
| ID | Claim | Lens | Why baseline missed it |
|---|---|---|---|

## Disputed findings / noise parallel introduced
| Claim from a specialist | Final disposition and why | Corpus evidence |
|---|---|---|

## Verdict (pick one and defend in 3–5 sentences)
- [ ] Parallel improved coverage with acceptable noise
- [ ] Parallel mostly duplicated baseline (not worth spend today)
- [ ] Parallel added noise that would have misled a supervisor without a human evidence review

## Spend / time (honest estimate)
Baseline minutes: __ · Parallel minutes: __ · Would I pay this again for this pack size? yes/no — why
```

Fill every section. If either unique-findings table is empty after the line-by-line comparison, write `none`.

### 3.2 Decision-review questions

Use only the questions that bear on a real uncertainty in your synthesis. Do not manufacture an objection to satisfy a count.

1. **Concatenation theater:** “Is the synthesis just three lists stacked? Where is the dedupe proof?”  
2. **Rubber-stamp merge:** “Did the commander disagree with any specialist, or only applaud?”  
3. **Lens bleed:** “Did the ‘tests’ agent restate correctness bugs without naming missing tests?”  
4. **Evidence-backed disposition:** “Does the disposition follow from the corpus, or from which claim was easiest to check?”
5. **Baseline skip:** “If baseline_single.md is missing, this stretch is product demo, not mastery.”  

Record any question that changes a disposition or the delta verdict. If none changes the work, record that the compared evidence left no unresolved review question.

### 3.3 Mastery evidence checklist (stretch complete)

- [ ] `baseline_single.md` + `many_minds_synthesis.md` + `many_minds_delta.md` all on disk  
- [ ] Delta has a defended verdict (not “looked fine”)  
- [ ] Every finding has a **corpus-backed** disposition; zero discards is valid
- [ ] Any review question that changed the work is recorded
- [ ] Sentence: MCP server ≠ engine ≠ subagent ≠ human

---

## Reference · Custom agents

Custom agent TOML under `%USERPROFILE%\.codex\agents\` or `.codex/agents/` (`name`, `description`, `developer_instructions`). Frozen lenses are enough for stretch credit. Pinning a security reviewer agent is a transfer seed, not a GREEN requirement.

Anthropic access is not part of P3. A late-course optional activity may add it only if the instructor confirms it.

---

## Close

### Operator log bullets

```text
MANY MINDS:
- Baseline path: instruments/p3_multi_agent/out/baseline_single.md
- Synthesis path: instruments/p3_multi_agent/out/many_minds_synthesis.md
- Delta path: instruments/p3_multi_agent/out/many_minds_delta.md
- Delta verdict: improved / duplicated / noisy — one line
- Dispositions: keep <n> · demote <n> · discard <n> — zero discard is valid
- Review question that changed the work: <question and change> / none
- Sentence: MCP server ≠ engine ≠ subagent ≠ human
```

### Transfer seed

> When a review has clean lenses, I baseline once, then spawn specialists and wait for all — I score the delta before I trust parallel, and I disposition every finding with corpus evidence.

### Pass bar

Mark P3 Stretch in `PASS_BARS.md` only if baseline + synthesis + delta survive a skeptical read. Missing baseline ⇒ not yet for the mastery stretch (product demo only).

---

## Facilitator notes (lead)

- Run after comparator discipline exists.  
- **Require the three files** on any student claiming the stretch. Spot-audit deltas first — that is where theater hides.  
- Cap three subagents; set `agents.max_concurrent_threads_per_session` on spend-sensitive machines and say it out loud (Thursday lesson early).  
- Seeded defects are unlabelled on purpose, and the key is kept out of this guide.  
- Correct “cowork” language immediately.  
- Success = three artifacts + corpus-backed dispositions + defended delta verdict.

## Failure modes

| Symptom | Likely cause | Move |
|---|---|---|
| No baseline file | Rushed to spawn | Stop parallel; run Part 1 |
| No subagent threads | Prompt never asked spawn/wait | Re-paste frozen brief |
| Synthesis is nine undedupe lines | Commander did not merge | Reject stretch; rewrite B |
| Disposition is “low confidence” only | No evidence rule | Demand a corpus reason or mark the finding unresolved |
| Delta empty | Did not compare | Force line-by-line pass |
| Edits Python | Prompt drift | Stop; read-only |
| Spend alarm | Too many agents | Cap 3; shorter retries |

---

## Identity lock

Many minds are still one operator. Parallel is a tool you **measure** — not a way to outsource the verdict, and not a second engine.
