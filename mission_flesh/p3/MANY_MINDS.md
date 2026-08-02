# Many Minds, One Commander

**Block:** P3 stretch (Tuesday PM)  
**Time:** about 75–100 minutes for the full mastery path; do not skip the baseline  
**Home tool:** Codex app with `gpt-5.6-terra`<br>
**Pack:** `instruments/p3_multi_agent/`  
**Pass bar home:** `operator/PASS_BARS.md` · P3 Stretch  

This guide stands beside you at the keyboard. You already finished (or nearly finished) the twin-engine desk. Now you will practice a different kind of “many”: not two vendors, but **several specialist runs under one human commander** — and you will **measure** whether parallel actually helped.

---

## What this is for (read before any click)

When one chat does everything — explore, test, security, write-up — the useful signal gets buried under noise. The room fills up. Later answers get worse even though the model is the same. People call that **context pollution** (good facts drowned) and **context rot** (performance slides as the chat fills with less relevant detail).

A **subagent** is a specialist Codex starts for one bounded job. It works in its own agent thread, then returns a **summary** to your main chat. You stay the commander: you write the brief, you choose the lenses, you wait for all, you own the merge and the kills.

That is not the same craft as P3’s twin-engine work:

| Craft | What differs | What stays yours |
|---|---|---|
| **Second engine** (OpenCode) | Different product / model family; independent context | Brief frozen; adjudication; kill bad claims |
| **Subagent** (Codex) | Same product; parallel specialists; summaries return to one chat | Division of labor; wait-for-all; synthesis; kill bad claims |
| **Second human** | Another person with real judgment | You still own the operational call when you are commander |

If someone calls all of this “cowork,” gently correct them. **Cowork** is a different product name on a subscription path this course does not use. Here the words are **subagent**, **worktree**, and **handoff**.

### The mastery move (why this is not a feature tour)

Anyone can paste “spawn three agents.” Mastery is:

1. **Baseline first** — one commander, no subagents, same pack, written findings.  
2. **Parallel second** — three lenses, wait-for-all, synthesis on disk.  
3. **Delta** — what parallel added, missed, or invented, in a table you can defend.  
4. **Earned kill** — discard at least one specialist claim using **corpus evidence**, not “felt weak.”  

If you only have the synthesis file and a polite kill, you ran the product. You did not yet prove the craft.

---

## Map of the hour

| Part | About | You leave with |
|---|---|---|
| 1. Orientation | Why parallel; naming lock | One sentence you can say cold |
| 2. Baseline (required) | Single-chat review, no subagents | `out/baseline_single.md` |
| 3. Subagent run | Three lenses, wait-for-all, synthesis | `out/many_minds_synthesis.md` |
| 4. Delta + pressure | Compare baseline vs parallel; adversarial seeds | `out/many_minds_delta.md` |
| 5. Worktree (optional deeper) | Isolation when writes would collide | Proof or honest block |
| 6. Close | Log + transfer seed | Stretch claimed only with evidence |

Permission mode stays **Ask for approval**. Subagents inherit the parent’s permission mode and sandbox. Set the mode **before** you ask to spawn.

Every Codex chat in this stretch uses **GPT-5.6 Terra** (`gpt-5.6-terra`) with the OpenAI API key stored in Codex sign-in. Do not leave a chat on Default or Sol. This stretch does not use an Anthropic key.

Spend note: each subagent does its own model and tool work. Parallel is richer and **more expensive**. Cap at three specialists in class.

Notice what kind of cap “three” is. It lives in the wording of a prompt, which makes it **procedure-enforced** — it holds because the model cooperates and you are watching. Codex also has a real setting, `agents.max_concurrent_threads_per_session`, which caps concurrent spawned threads whether the prompt cooperates or not. That one is **tool-enforced**. You will name that distinction formally on Thursday; today you are living on the procedural side of it, so keep an eye on the thread count yourself.

Prefer **read-only** review today so you do not invent merge conflicts for sport.

---

## Before you start

- [ ] Twin-engine MVP is done or within a few minutes of done (do not skip the floor for this stretch)
- [ ] Codex app open; sign-in uses the **OpenAI API key stored in Codex**; model is **GPT-5.6 Terra** (`gpt-5.6-terra`)
- [ ] Permission mode: **Ask for approval**
- [ ] You are in the **course repo root** (the folder that contains `instruments/` and `mission_flesh/`)
- [ ] You can browse `instruments/p3_multi_agent/corpus/` in Explorer

```powershell
# From the course repo root
New-Item -ItemType Directory -Force -Path ".\instruments\p3_multi_agent\out" | Out-Null
```

---

## Part 1 · Orientation (about 8 minutes)

### 1.1 Say the distinction out loud

> Second engine means a different product I adjudicate. Subagent means specialists under one commander in one product. I still own the brief and the kill list.

If you cannot say that without hedging, stay here until you can.

### 1.2 Why parallel helps (and when it hurts)

**Helps when:** the work is **read-heavy** and splits cleanly into lenses on the same frozen files.

**Hurts when:** two writers edit the same files at once, or you spawn agents without wait-for-all and synthesis, or you flood the main chat with every raw log anyway, or you skip the baseline and cannot tell whether parallel did anything.

Today is read-heavy on purpose. The baseline exists so “helps” is measured.

---

## Part 2 · Baseline — single commander, no subagents (required · about 15–20 minutes)

Do this **before** any spawn. If you skip it, the stretch is not yet under the mastery bar — only under a demo bar.

### 2.1 Open a baseline chat

```text
P3 — Many Minds baseline (no subagents)
```

Create this chat in Codex and select **GPT-5.6 Terra** (`gpt-5.6-terra`) before you paste the baseline prompt.

### 2.2 Frozen baseline brief (paste exactly)

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

### 2.3 Baseline evidence checklist

- [ ] `out/baseline_single.md` exists in Explorer  
- [ ] Every finding has **corpus evidence** (file + symbol or quote)  
- [ ] You did **not** spawn subagents in this chat  

If the model spawns anyway, stop and restart the baseline chat. The comparison is ruined if parallel leaks into the baseline.

---

## Part 3 · Subagent run (about 25–35 minutes)

### 3.1 Open a commander chat

```text
P3 — Many Minds commander
```

Create this chat in Codex and select **GPT-5.6 Terra** (`gpt-5.6-terra`). Keep baseline and twin-engine work in other chats.

### 3.2 Point at the pack

```text
Working pack (read-only):
instruments/p3_multi_agent/corpus/
  service_snippet.py
  tests_snippet.py
  NOTES_ops.md

Write only under:
instruments/p3_multi_agent/out/
```

### 3.3 Frozen multi-agent brief (paste exactly)

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
  C) Kills: at least one specialist finding you discard — reason must cite corpus evidence or clear out-of-scope (not “low vibes”)
  D) Operator still owns: one paragraph on what a human must still decide
  E) One sentence: subagent ≠ second engine (OpenCode) ≠ second human
  F) Do not read or mention baseline_single.md

Begin. Wait for all subagents. Then write the synthesis file.
```

### 3.4 While it runs

| Moment | What it means |
|---|---|
| Subagent threads appear | Specialists off the main chat |
| You open a subagent thread | Inspect raw work; watch for lens bleed |
| Commander writes to disk | Orchestration counts only if Explorer shows the file |
| Approval prompts | Same sandbox story — you still gate the chair |

If Codex edits the Python files, **stop** and restate: read-only; synthesis only.

### 3.5 Synthesis evidence checklist

- [ ] Three lenses ran (three threads or three clear returned blocks)  
- [ ] `out/many_minds_synthesis.md` on disk  
- [ ] Merge shows **dedupe** (not nine raw lines pasted)  
- [ ] ≥1 **earned kill** with corpus-based reason  
- [ ] Naming sentence present  
- [ ] Your own one-line agree/disagree on the merge in the operator log  

---

## Part 4 · Delta sheet + pressure (required · about 15–20 minutes)

This is the stretch’s measurement moment. Without it, parallel is a story.

### 4.1 Build the delta (you may use a short Codex assist, but you own the cells)

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

## False friends / noise parallel introduced
| Claim from a specialist | Why killed or demoted | Corpus evidence |
|---|---|---|

## Verdict (pick one and defend in 3–5 sentences)
- [ ] Parallel improved coverage with acceptable noise
- [ ] Parallel mostly duplicated baseline (not worth spend today)
- [ ] Parallel added noise that would have misled a supervisor without a human kill pass

## Spend / time (honest estimate)
Baseline minutes: __ · Parallel minutes: __ · Would I pay this again for this pack size? yes/no — why
```

Fill every section. Empty “unique to baseline” with a written search note is allowed only if you truly compared line by line.

### 4.2 Adversarial seeds (paste into `Adversarial — P3` or a scratch attack)

Use at least two:

1. **Concatenation theater:** “Is the synthesis just three lists stacked? Where is the dedupe proof?”  
2. **Rubber-stamp merge:** “Did the commander disagree with any specialist, or only applaud?”  
3. **Lens bleed:** “Did the ‘tests’ agent restate correctness bugs without naming missing tests?”  
4. **Cheap kill:** “Is the discarded finding actually the weakest claim, or the one that was hardest to check?”  
5. **Baseline skip:** “If baseline_single.md is missing, this stretch is product demo, not mastery.”  

Copy the adversarial outcome into your log the same way as the block MVP.

### 4.3 Mastery evidence checklist (stretch complete)

- [ ] `baseline_single.md` + `many_minds_synthesis.md` + `many_minds_delta.md` all on disk  
- [ ] Delta has a defended verdict (not “looked fine”)  
- [ ] ≥1 kill with **corpus** reason  
- [ ] ≥2 adversarial seeds answered in the log  
- [ ] Sentence: subagent ≠ second engine ≠ second human  

---

## Part 5 · Worktree isolation (optional deeper · about 15–20 minutes)

Skip if time is short **only after** Parts 2–4 are solid. Worktree alone never replaces the delta.

### 5.1 What a worktree is

A **Git worktree** is a second checkout of the same repository: its own files on disk, shared history. In the Codex app, **Worktree** under the composer starts a chat against a managed checkout so background work does not rewrite your **Local** foreground copy.

**Handoff** moves a chat between Local and Worktree. Git allows a branch in only one worktree at a time — that is why Handoff exists.

### 5.2 Isolation proof with a real constraint

1. Note your Local path (course repo root).  
2. New Codex chat with **Worktree** and **GPT-5.6 Terra** (`gpt-5.6-terra`) selected.
3. Prompt:

```text
You are on a worktree. Do not edit tracked lesson files under instruments/ or mission_flesh/.
1) Print cwd.
2) Create ONLY instruments/p3_multi_agent/out/worktree_path.txt with:
   worktree_cwd=<cwd>
   proof=many-minds-isolation
3) Explain in one sentence why two agents editing the same tracked file on Local would need isolation or serialization.
Stop.
```

4. Confirm Local lesson files unchanged.  
5. Log: **when you would choose worktree vs subagent** (writes/isolation vs read-split/context).  

If Worktree is unavailable: honest block. Parts 2–4 still stand.

### 5.3 `.worktreeinclude`

Example at `instruments/p3_multi_agent/.worktreeinclude` — pattern for ignored files in real app repos. Knowing the seam is enough today.

---

## Part 6 · Custom agents (optional mention)

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
- Earned kill: <claim> — corpus reason: <file/symbol>
- Adversarial seeds used: <two ids>
- Worktree: done / skipped / blocked
- Sentence: subagent ≠ second engine ≠ second human
```

### Transfer seed

> When a review has clean lenses, I baseline once, then spawn specialists and wait for all — I score the delta before I trust parallel, and I kill with corpus evidence.

### Pass bar

Mark P3 Stretch in `PASS_BARS.md` only if baseline + synthesis + delta survive a skeptical read. Missing baseline ⇒ not yet for the mastery stretch (product demo only).

---

## Facilitator notes (lead)

- Run after comparator discipline exists.  
- **Require the three files** on any student claiming the stretch. Spot-audit deltas first — that is where theater hides.  
- Cap three subagents; set `agents.max_concurrent_threads_per_session` on spend-sensitive machines and say it out loud (Thursday lesson early).  
- Seeded defects are unlabelled on purpose, and the key is kept out of this guide.  
- Correct “cowork” language immediately.  
- Worktree is optional deeper; never a substitute for delta.  
- Success = three artifacts + earned kill + defended delta verdict.

## Failure modes

| Symptom | Likely cause | Move |
|---|---|---|
| No baseline file | Rushed to spawn | Stop parallel; run Part 2 |
| No subagent threads | Prompt never asked spawn/wait | Re-paste frozen brief |
| Synthesis is nine undedupe lines | Commander did not merge | Reject stretch; rewrite B |
| Kill is “low confidence” only | Cheap kill | Demand corpus reason |
| Delta empty | Did not compare | Force line-by-line pass |
| Edits Python | Prompt drift | Stop; read-only |
| Spend alarm | Too many agents | Cap 3; shorter retries |

---

## Identity lock

Many minds are still one operator. Parallel is a tool you **measure** — not a way to outsource the verdict, and not a second engine.
