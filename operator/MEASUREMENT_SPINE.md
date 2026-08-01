# Measurement spine — Move 4

**Ultra-light week scoreboard.** Living Markdown in the Codex app project.  
Updated **once per block, after adversarial review**.

Not a second curriculum. Not a metrics religion.  
Three entries that answer: *Was the brief I wrote any good, how much of what I claimed survived attack, and what did the block cost in time?*

```text
Brief accuracy · Overclaim · Time to result
```

---

## Purpose

| Audience | Use |
|---|---|
| **Student** | See the week as one circuit; watch overclaim fall block by block |
| **Facilitator** | Thin rollup (`FACILITATOR_ROLLUP.md`) — who is claiming more than the evidence carries |
| **Transfer** | 30-day rhythm inherits the same three entries on one real workload |

---

## How it lives

| Rule | Detail |
|---|---|
| **Where** | `operator/MEASUREMENT_SPINE.md` in the Codex app project |
| **Chat** | Prefer a short update in `Operator — Direction & Log` after adversarial (or a dedicated `Operator — Measurement` chat if the log chat is crowded) |
| **When** | **End of every block only**, after the `ADVERSARIAL:` line exists |
| **How** | Interactive with AI: you paste the facts, the AI counts overclaim from the rulings and refuses “the brief was fine” |
| **Weight** | Three entries, one note, and a deep mark on the blocks that carry one. More than two or three minutes means you are over-measuring |

### Pulse position

```text
Brief → Mission → Log + PASS_BARS draft
  → Adversarial (new chat)
  → Measurement spine row (this file)
  → Transfer chat at B0, P7 and P8; a dated seed line at the other blocks
```

---

## The three entries (every block)

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

### 2. Overclaim — how much of what you claimed did the attack take away?

Write it as `n/m`, for example `2/7`.

| Symbol | What it is | Where it comes from |
|---|---|---|
| **m** | How many MVP bars you marked **met** | Your pass-bar draft, counted **before** the adversarial chat opened |
| **n** | How many of *those same bars* came back **WOUNDED** or **DEAD** | Step 3 of the frozen prompt in `ADVERSARIAL_REVIEW.md` — the per-claim `SURVIVES / WOUNDED / DEAD` ruling |

Counting rules, in order:

1. **Fix `m` before you paste.** Count the bars you marked met, write the number down, and put it in the adversarial paste pack. A denominator chosen after the verdict is not a denominator.
2. **Count `n` from the rulings, not from the summary.** The `ADVERSARIAL:` line grades the block *stood / wounded / failed*; overclaim is counted one bar at a time from the evidence audit. Two different resolutions, and only the per-bar one goes here.
3. **`SURVIVES` does not count.** Neither does a bar you never marked met — if the reviewer attacks something you left unticked, it is a real finding for the log, but it is outside this number.
4. **A bar it refused to rule on is unfinished business.** Give it the evidence it asked for and ask again. Do not score around a missing ruling in either direction.
5. **`m = 0` is not a score, it is a skipped beat.** Claiming nothing to protect the ratio leaves the mastery floor empty, and an empty floor is *not yet* on every bar.

**Why this is the number to trust:** a number you cannot award yourself is worth more than two you can, because only a number someone else rules on is able to come back wrong — and a mark that cannot be wrong cannot teach.

Expect overclaim to be highest early. It is the one line in this file that should **fall** across the week, and a falling line is the first hard evidence you get that your own read of your own evidence is getting better.

### 3. Time to result — how long from live brief to adversarial line?

Record **minutes** (integer):

`time_to_result = clock from Direction Brief status LIVE → ADVERSARIAL line written`

Optional note (≤5 words): e.g. `setup drag`, `rabbit hole`, `clean run`.

No stopwatch theater: an honest estimate is fine; fiction is not.

**What this number is for.** It is read **across operators on one block**, never across blocks on one operator. The blocks differ in shape, length, and instrument, so your P4 minutes and your P6 minutes are not on the same axis and their difference means nothing. When several people run long on the same block, the finding belongs to that block — it was scoped too wide, and the fix is to narrow the data. Your own pace is not a grade here and never becomes one.

---

## Block rows (fill every block)

| Block | Brief accuracy (HIT/PARTIAL/MISS + field named) | Overclaim `n/m` | Time (min) | One-line note |
|---|---|---|---|---|
| B0 | | | | |
| P1 | | | | |
| P2 | | | | |
| P3 | | | | |
| P4 | | | | |
| P5 | | | | |
| P6 | | | | |
| P7 | | | | |
| P8 | | | | |

Nine rows is the whole scoreboard. Do not average them and do not add a totals line: a median across nine unlike missions has no referent, because the missions are not repeats of one another. The reading that carries a decision is the **shape of the overclaim column down the page**, and you get that by looking at it.

---

## Deep marks (only on the block that creates them — still one line)

Ultra-light continuity for the big instruments. Fill **only when that block runs**; don’t invent parallel scorecards.

| Block | Deep mark (one line) |
|---|---|
| **P2** | Case suite: baseline → after on `instruments/p2_test_suite` D01–D05 (`n/5`) |
| **P3** | Comparator on `BRIEF-v1`: disagreements `n` · kills `n` · verdict |
| **P5** | Containment: 3/3 catches · absence-of-effect proof pointer |
| **P6** | Contract: stop/restart · exception drill pass/fail |
| **P8** | Hold-degrade: open `n/5` vs home `n/5`; refuse: Y/N; transfer SEALED: Y/N |

B0, P1, P4 and P7 carry no deep mark — for those blocks the three entries and the note are the whole row.

---

## End-of-block prompt (paste after adversarial)

```text
Measurement spine update. Read operator/MEASUREMENT_SPINE.md.
Block: [B0/P1/…].
Adversarial line: [paste ADVERSARIAL: …].
Per-claim rulings from the adversarial: [PASTE THE SURVIVES / WOUNDED / DEAD LIST].
Bars I marked met before the attack: [n].
Brief LIVE at: [time or "approx"].
Adversarial done at: [time or "approx"].
Mission outcome path(s): [paths].
Fill this block's row:
1. Brief accuracy — did the artifact match the "done looks like" I wrote before the
   run, and which one of the five brief fields would I write differently now?
   Refuse "the brief was fine": make me name a field, or say none and name what
   held better than expected.
2. Overclaim n/m — count the bars I marked met that came back WOUNDED or DEAD,
   over the number I marked met. Count from the rulings I pasted, not from my summary.
3. Time to result in minutes.
4. One-line note.
5. Deep mark if this block has one.
Do not score ritual health and do not give a quality label. Neither is in this row.
Do not start transfer until this row is written.
```

---

## Facilitator rollup

Thin view lives in `FACILITATOR_ROLLUP.md`. One rule travels with the number: **overclaim is never read without the met-count beside it.** One wounded bar out of nine claimed and one out of two are different students, and the ratio alone cannot tell you which you are looking at.

---

## How to read the spine (student)

| Pattern | Likely issue |
|---|---|
| Brief accuracy HIT, overclaim high | You are shipping the artifact and over-reading the evidence. The attack is doing its job |
| Overclaim near zero, bars-met falling week on week | You are protecting the ratio by claiming less. Unticked bars are still *not yet* and still hold the floor open |
| Overclaim near zero, bars-met rising, no fix list ever | Check the paste pack before you believe it. A reviewer handed thin evidence has nothing to attack |
| The same brief field named every block | That is where your brief-writing needs the work. *Done looks like* and *Evidence standard* are the usual two |
| “None held better than expected” nine times running | Not credible across nine missions. You are defending the brief rather than scoring it |
| Overclaim falling B0 → P8 | Your self-assessment is calibrating. This is the line to want |
| Long times scattered across people and blocks | Individual pace. Not a finding |
| Long times clustered on one block | That block is scoped too wide. A finding about the block |

---

## Transfer bridge

At P7 and P8, carry the same three entries into the 30-day rhythm for **one real workload**:

- **Brief accuracy:** did the work match the criteria you set before starting, and which criterion do you now write differently
- **Overclaim:** what you claimed was done that a reviewer took back
- **Time:** time-to-accept or time-to-result on that workload

Same spine, smaller world. The party who rules on your overclaim at work is a colleague, a check, or a customer — pick one before you leave.

---

## Identity lock

If the spine grows past three entries and a note, cut it back.  
If rows are filled before adversarial, delete them — measurement follows attack.  
If overclaim is counted from your own summary instead of the rulings, it is a self-awarded number again and this file has lost its only teeth.  
If facilitators grade people on speed, the school has betrayed mastery.
