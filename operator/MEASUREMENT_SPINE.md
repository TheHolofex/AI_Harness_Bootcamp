# Measurement spine — Move 4

**Ultra-light week scoreboard.** Living Markdown in the Codex app project.  
Updated **once per block, after that block&#x27;s review boundary**. P2 uses its built-in `REVIEW:` line and receipt. P4 uses its human raw-source audit, configured read-only evaluator receipt, deterministic verifier, resume receipt, and terminal state. Neither adds a separate adversarial chat.

The live HTML module page is authoritative for whether this row is part of the learner flow and which exact module-specific closeout chat to use.

Not a second curriculum. Not a metrics religion.  
Four entries that answer: *Was the contract I wrote any good, how much of the first-pass claim survived review, what did accepted completion cost in time, and what will I change next?*

```text
Brief accuracy · Overclaim · Time to result · Lesson reflection
```

---

## Purpose

| Audience | Use |
|---|---|
| **Student** | See the week as one circuit; watch overclaim fall block by block |
| **Facilitator** | Thin rollup (`FACILITATOR_ROLLUP.md`) — who is claiming more than the evidence carries |
| **Transfer** | 30-day rhythm inherits the same four entries on one real workload |

---

## How it lives

| Rule | Detail |
|---|---|
| **Where** | `operator/MEASUREMENT_SPINE.md` in the Codex app project |
| **Chat** | Use the exact closeout chat named on the module page. The generic direction-chat pattern is `[MODULE] — Direction & Closeout`; replace `[MODULE]` with the current module code. The saved file, not chat history, carries the row forward |
| **When** | **End of every block only**, after the `ADVERSARIAL:` line exists |
| **How** | Interactive with AI: you paste the facts, the AI counts overclaim from the rulings and refuses “the brief was fine” |
| **Weight** | Four short entries and a deep mark on the lessons that carry one. More than two or three minutes means you are over-measuring |

### Position in the lesson

```text
Brief → Lesson work → Log + lesson-outcome check
  → Independent review (new chat)
  → Measurement spine row (this file)
  → Dated transfer seed in the module closeout for P1–P7
  → Shared P7–P8 plan chat only when the P7 or P8 page directs it
```

---

## The four entries (every lesson)

### 1. Brief accuracy — was the brief you wrote before the run any good?

Two parts. Both are required, and the second is the one that teaches.

**First, the artifact against the criteria.** Did what you shipped meet the *Done looks like* checks you wrote **before** the mission started, as written?

| Mark | Meaning |
|---|---|
| **HIT** | The artifact meets the checks the brief listed, on the terms the brief set |
| **PARTIAL** | Something shipped; one or more brief checks not met — name which |
| **MISS** | The outcome is not there. Honest fail |

Judge the artifact and the state, not the effort, and not the stretch goals.

**Second, name the field you would rewrite.** The Direction Brief has five fields — **Outcome**, **Done looks like**, **Bounds**, **Evidence standard**, **Stop / hand-back**. Name **one** of them you would write differently now that you have seen what the run produced, and say in a clause what you would write instead.

Naming a field is required. If nothing needs rewriting, the only accepted way to say so is to name the field that carried the run and why:

```text
none — Bounds held better than expected, because the "no writes outside the mission folder"
line is what made the stop proof cheap to produce.
```

“The brief was fine” is not an entry. A brief you cannot improve after watching what it produced is a brief you did not read back against the artifact, and the AI you paste into is told to send that answer straight back to you.

A worked example of the whole entry:

```text
PARTIAL — the map loads but the filter check was never observable.
Done looks like: I wrote "filters work"; I would write "select one region and the row
count changes, and I can name the new count".
```

### 2. Overclaim — how much of what you marked complete did the review change?

Write it as `n/m`, for example `2/7`.

| Symbol | What it is | Where it comes from |
|---|---|---|
| **m** | How many lesson outcomes you marked **complete** | Your outcome check, counted **before** the review boundary |
| **n** | How many of *those same outcomes* the reviewer rejected on first pass | The saved per-criterion ruling from the module&#x27;s required review boundary |

Counting rules, in order:

1. **Fix `m` before you paste.** Count the lesson outcomes you marked complete, write the number down, and put it in the review paste pack. A denominator chosen after the verdict is not a denominator.
2. **Count `n` from the rulings, not from the summary.** The `ADVERSARIAL:` line grades the lesson *stood / wounded / failed*; overclaim is counted one outcome at a time from the evidence audit. Two different resolutions, and only the per-outcome one goes here.
3. **`SURVIVES` does not count.** Neither does an outcome you left incomplete — if the reviewer challenges it anyway, that is a real finding for the log, but it is outside this number.
4. **An outcome the reviewer would not rule on is unfinished business.** Give it the evidence requested and ask again. Do not score around a missing ruling in either direction.
5. **`m = 0` is not a score; it means the outcome check was skipped.** Marking nothing to protect the ratio leaves every lesson outcome incomplete.

**Why this is the number to trust:** a number you cannot award yourself is worth more than two you can, because only a number someone else rules on is able to come back wrong — and a mark that cannot be wrong cannot teach.

Expect overclaim to be highest early. It is the one line in this file that should **fall** across the week, and a falling line is the first hard evidence you get that your own read of your own evidence is getting better.

### 3. Time to result — how long from live contract to terminal review evidence?

Record **minutes** (integer):

`time_to_result = clock from the saved contract becoming active → the module&#x27;s terminal review evidence`

If timing needs context, keep it in this field: `42 min — setup drag`, `35 min — clean run`.

No stopwatch theater: an honest estimate is fine; fiction is not.

**What this number is for.** It is read **across operators on one block**, never across blocks on one operator. The blocks differ in shape, length, and instrument, so your P4 minutes and your P6 minutes are not on the same axis and their difference means nothing. When several people run long on the same block, the finding belongs to that block — it was scoped too wide, and the fix is to narrow the data. Your own pace is not a grade here and never becomes one.

### 4. Lesson reflection — what changes because of this run?

Answer the question printed in the **Lesson reflection** panel on the current lesson page. Use one sentence. Name the test, comparison, failure, or decision that changed what you will require next time. A summary of the activity is not a reflection.

---

## Block rows (fill every block)

| Block | Brief accuracy (HIT/PARTIAL/MISS + field named) | Overclaim `n/m` | Time (min) | Lesson reflection (one sentence) |
|---|---|---|---|---|
| B1 | | | | |
| P1 | | | | |
| P2 | | | | |
| P3 | | | | |
| P4 | | | | |
| P5 | | | | |
| P6 | | | | |
| P7 | | | | |
| P8 | | | | |

For P2, read the row from `normalized/intake_receipt.json` and the generated lists. Put sources normalized as `n/4` and people normalized in the first cell, with the damaged file's refusal `Y/N`. In the second, record capabilities asserted with a named record, unresolved count, and lists regenerated as `n/5`. Count a hook as enforcing only when it is trusted in `/hooks` and has actually refused something you tried; a hook that has never refused anything is untested, not narrow. Record the lookalike files fired on as `n/4` — the target is zero — and the package's local-path and credential counts, both of which should be zero. Do not add an overclaim exercise.

For P4, read the first-pass and final criterion tables from `Harness/EVAL.md` and the run facts from `Harness/RUN_TRACE.md`. In the overclaim cell, put `n/m`, where `m` is the number of criteria the generator presented as ready on first pass and `n` is the number the fresh evaluator returned HOLD. Preserve that first-pass result even when the one permitted repair clears it. Time ends at the explicit PASS/HOLD terminal record, not at the later transfer edit.

Nine rows is the whole scoreboard. Do not average them and do not add a totals line: a median across nine unlike missions has no referent, because the missions are not repeats of one another. The reading that carries a decision is the **shape of the overclaim column down the page**, and you get that by looking at it.

---

## Deep marks (only on the block that creates them — still one line)

Ultra-light continuity for the big instruments. Fill **only when that block runs**; don’t invent parallel scorecards.

| Block | Deep mark (one line) |
|---|---|
| **P2** | Inbound: sources normalized `n/4` · people normalized `n` · damaged file refused Y/N · capabilities asserted with a named record `n` · unresolved `n` · lists regenerated `n/5` · untraceable line refused Y/N · lookalike files fired on `n/4` · package local paths `n` · package secrets `n` |
| **P3** | Information need: terminal SATURATED/BUDGET_EXHAUSTED · rounds `n/3` · findings kept `n/12` · defeated `n` · coverage `n/m` obligations · merges run `n/2` and the reason for the one shipped · gate failures caught `n/3` planted · baseline delta stated `Y/N` |
| **P4** | Personal harness: terminal PASS/HOLD · human interventions `n` · first-pass evaluator HOLD `n/m` · trusted verifier PASS/HOLD · post-audit repairs `0/1` · mid-run resume PASS/HOLD · external manifest Y/N |
| **P5** | Containment: 3/3 catches · absence-of-effect proof pointer |
| **P6** | Contract: stop/restart · exception drill pass/fail |
| **P8** | Hold-degrade: open `n/5` vs home `n/5`; refuse: Y/N; transfer SEALED: Y/N |

B1, P1 and P7 carry no deep mark — for those blocks the four entries are the whole row.

---

## End-of-block prompt (paste after a separate adversarial review)

P2 and P4 do not use this prompt; their live pages write the row from integrated receipts.

```text
Measurement spine update. Read operator/MEASUREMENT_SPINE.md.
Block: [B1/P1/…].
Adversarial line: [paste ADVERSARIAL: …].
Per-claim rulings from the adversarial: [PASTE THE SURVIVES / WOUNDED / DEAD LIST].
Lesson outcomes I marked complete before the review: [n].
Brief LIVE at: [time or "approx"].
Adversarial done at: [time or "approx"].
Mission outcome path(s): [paths].
Fill this block's row:
1. Brief accuracy — did the artifact match the "done looks like" I wrote before the
   run, and which one of the five brief fields would I write differently now?
   Refuse "the brief was fine": make me name a field, or say none and name what
   held better than expected.
2. Overclaim n/m — count the lesson outcomes I marked complete that came back
   WOUNDED or DEAD, over the number I marked complete. Count from the rulings I
   pasted, not from my summary.
3. Time to result in minutes.
4. Lesson reflection — answer the one-sentence question on the current lesson page.
5. Deep mark if this block has one.
Do not score ritual health and do not give a quality label. Neither is in this row.
Do not start transfer until this row is written.
```

---

## Facilitator rollup

Thin view lives in `FACILITATOR_ROLLUP.md`. One rule travels with the number: **overclaim is never read without the completion count beside it.** One wounded outcome out of nine claimed and one out of two are different students, and the ratio alone cannot tell you which you are looking at.

---

## How to read the spine (student)

| Pattern | Likely issue |
|---|---|
| Brief accuracy HIT, overclaim high | You are shipping the artifact and over-reading the evidence. The independent review is finding the gap |
| Overclaim near zero, completed outcomes falling week on week | You may be protecting the ratio by claiming less. Incomplete outcomes still require work or a narrower claim |
| Overclaim near zero, completed outcomes rising, no fix list ever | Check the paste pack before you believe it. A reviewer handed thin evidence has nothing to challenge |
| The same brief field named every block | That is where your brief-writing needs the work. *Done looks like* and *Evidence standard* are the usual two |
| “None held better than expected” nine times running | Not credible across nine missions. You are defending the brief rather than scoring it |
| Overclaim falling B1 → P8 | Your self-assessment is calibrating. This is the line to want |
| Long times scattered across people and blocks | Individual pace. Not a finding |
| Long times clustered on one block | That block is scoped too wide. A finding about the block |

---

## Transfer bridge

At P7 and P8, carry the same four entries into the 30-day rhythm for **one real workload**:

- **Brief accuracy:** did the work match the criteria you set before starting, and which criterion do you now write differently
- **Overclaim:** what you claimed was done that a reviewer took back
- **Time:** time-to-accept or time-to-result on that workload
- **Lesson reflection:** the one requirement or habit you will change on the next run

Same spine, smaller world. The party who rules on your overclaim at work is a colleague, a check, or a customer — pick one before you leave.

---

## Identity lock

If the spine grows past four entries, cut it back.
If rows are filled before the independent review, delete them — measurement comes after the review.
If overclaim is counted from your own summary instead of the rulings, it is a self-awarded number again and this file has lost its only teeth.  
If facilitators grade people on speed, the course has confused pace with learning.
