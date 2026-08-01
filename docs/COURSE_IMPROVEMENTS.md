# Course improvements — theater vs. teaching

**Internal design document. Course owner only.** Design rationale is the point of this
file; it is not learner-facing and nothing in it should be lifted into a block page.

Synthesized from four independent audits, deduplicated, and verified line-by-line
against the repo at commit `fb66ca5`. Every count, path, and quotation below was
checked; claims that did not survive checking were dropped or corrected, and the
corrections are named.

---

## The honest verdict

**What this course does better than almost any technical course:** it has a real
adversary. `operator/ADVERSARIAL_REVIEW.md` puts a frozen, hostile prompt in a fresh
chat after every block, and the protocol's step 3 forces a per-claim
`SURVIVES / WOUNDED / DEAD` ruling on bars the student already marked met. That is an
activity a student can lose. Paired with `operator/PASS_BARS.md:36` — *"Not evidence:
'looks good,' model self-praise, screenshots of chat enthusiasm"* — and with the
Direction Brief's field 2, *"Observable checks only (open, run, compare, count). If it
can't be checked, it isn't a criterion"* (`operator/DIRECTION_BRIEF.md:20`), the course
holds an evidence standard most professional training never attempts. The instruments
are real too: P2's dyno cases each open with an externally authored `Pass if:` line,
P5's intake batch is genuinely unlabeled, and P3 runs one frozen brief across two model
families.

**Where it spends attention on ceremony:** the course has 225 checkboxes across nine
block pages. Of those, 76 mark mission work and 8 are stretch. The remaining 141 (63%)
are the operator pulse (63), the mastery floor (69), and block closure (9). The pulse
is where the ceremony concentrates. Of its seven beats, two can take something away
from the student — the adversarial, and the log verdict when honestly set to REJECT.
Three are transcription of facts already recorded elsewhere. Two are forecasts that
nobody ever scores, and those two become the strongest beats in the course the moment
they are scored.

**The single most damaging finding is not ceremony at all.** All seven answer keys —
including `mission_flesh/p5/FACILITATOR_KEY.md`, which names every poisoned file, every
planted defect, and every expected catch — are tracked in git and shipped to students by
the clone command on `site/blocks/b0.html:156`. The course already diagnosed this exact
failure at P7 (commit `4336d34`: *"the (false) markers were feeding the system under
test its own answer key"*) and fixed it in one CSV without generalizing the rule to the
repo.

### Note on the second-engine audit

The independent audit at `codex_theater.md` (gpt-5.6-sol, 7,956 lines) **did not
complete**. Its transcript ends mid-tool-call during the FRACTURE phase; it never
produced the T-item list it was asked for. Cross-engine agreement is therefore
**not available** as a confidence signal for the items below — everything here rests on
direct repo verification rather than on two engines concurring.

Its one usable contribution is an arithmetic claim I independently confirmed: the pulse
timeboxes on `site/pulse.html:50-55` (brief ≤5–8, log+bars ≤5–10, adversarial 5–10,
measure 3–5, transfer 5–10) total **23–43 minutes of non-mission ritual per half-day**,
which is 3.5–6.5 hours across the nine blocks. That number frames every attention
argument below.

---

## Summary

| ID | Target | Verdict | Change | Value | Risk |
|---|---|---|---|---|---|
| **C11** | P2 dyno dispatch (`p2.html:212`) + case files' `Pass if:` line | theater dressed as measurement | Move pass conditions to a grader file the model never opens | **Highest** | Low |
| **C1** | 7 `*_KEY.md` files tracked in git; `b0.html:156` clone | theater-enabling | Remove from student clone; distribute to staff separately | **Highest** | Low |
| **C2** | P2 baseline self-grading (`p2-base`, `SCORE_SHEET.md`) | mixed | Release key as one-way calibration after baseline locks; record agreement rate | **High** | Low |
| **C3** | `MEASUREMENT_SPINE.md` headlines 1 and 3 | theater | Replace both with an overclaim count harvested from the adversarial | **High** | Low-med |
| **C4** | Cross-engine adversarial (`ADVERSARIAL_REVIEW.md:42`) | teaching, under-deployed | Make mandatory at P3 and P5 (free); P8 via the re-pointed endpoint | **High** | Low |
| **C5** | `MEASUREMENT_SPINE.md` headline 2 (Mission) | mixed | Retitle *brief accuracy*; require a named field the operator would rewrite | **High** | Med |
| **C6** | `pulse-transfer` × 9; session-log table | theater at 6 of 9 | Run at B0/P7/P8; promote in-mission seeds to floor bars; add P1 seed | **High** | Med |
| **C7** | `pulse-mission` × 9; `*-done` × 9 | theater | Delete both. 18 checkboxes | Med-high | Low |
| **C8** | `pulse-bars` AI dialogue × 9 | mixed | Dialogue at B0/P2/P5 only; floor list is the prediction elsewhere | Med | Med |
| **C9** | `p8-defense` / `mvp-90s` | mixed | Deliver to a live listener with a comprehension pass condition | Med-high | Med |
| **C10** | Running-totals table; `T` flag in rollup | theater | Delete the table; point the time flag at scope, not the operator | Low-med | Med |
| **—** | Delete the `#floor` section (69 boxes) | **ruled against** | See *Rulings against candidate items* | — | — |

---

## C1 — The answer keys ship with the student clone

**Value: highest. Risk: low. Do this first; C2 depends on it.**

### What exists today

Seven key files, all tracked by git:

```
instruments/p2_dyno/engineering/FACILITATOR_KEY.md
instruments/p2_dyno/mission_ops/FACILITATOR_KEY.md
instruments/p3_frozen_brief/engineering/FACILITATOR_KEY.md
instruments/p3_frozen_brief/mission_ops/FACILITATOR_KEY.md
instruments/p8_hold_degrade/FACILITATOR_KEY.md
lead/MANY_MINDS_ANSWER_KEY.md
mission_flesh/p5/FACILITATOR_KEY.md
```

`site/blocks/b0.html:156` instructs every student to run
`git clone https://github.com/TheHolofex/AI_Harness_Bootcamp.git`, and
`prework/INSTALL_GUIDE.md:577` repeats it. `server.py:157` blocks any filename ending
`FACILITATOR_KEY.md` or `ANSWER_KEY.md` over HTTP, so the gated site is clean — **the
clone is the unclosed door.**

The P5 key is the worst case. It sits inside `mission_flesh/p5/`, the same directory as
the intake batch, and its own header states the requirement the delivery breaks:

> **Staff only. Never link from learner-facing pages, packs, or chats.** The batch works
> only while it doesn't confess.

It then tabulates all three poisoned files by name, their planted defects, the refuting
evidence, and the expected mechanical catch — plus a "Watch-fors" section describing the
exact partial-credit failures a struggling student would otherwise discover the hard way.

The P2 keys sit one level above the cases the model is told to open. `p2.html:212`
directs the model at `instruments/p2_dyno/[TRACK]/cases/[CASE FILE]`, while
`instruments/p2_dyno/engineering/FACILITATOR_KEY.md` — *"D01 | Names redis timeout /
integration job; ... ignores npm warn as root cause"* — sits in the parent directory.
`p2.html:188` separately tells the student to open `instruments\p2_dyno` in a file
browser.

### Two corrections to the candidate claim

Both make the finding narrower but do not defuse it:

1. The P5 stage-03 citation prompt does **not** direct a broad `mission_flesh/` search.
   It scopes to `Documents\HarnessBootcamp\AI_Harness_Bootcamp\mission_flesh\p1\corpus`
   (`p5.html:296-297`). A compliant model stays out of `p5/`.
2. The P5 intake is **copied out of the repo** to `Documents\p5-staging\intake` before
   work begins (`p5.html:219-220`), so the working directory is not the key's directory.

What survives: the key is readable by any student who opens the folder, by any model
given a wider search scope, and by anyone who greps their own clone. The mitigation is
prompt discipline, which is exactly the thing the course teaches students not to trust
as a boundary — P5's own mastery claim is *"containment is absence of effect."*

### What changes

Move all seven files out of the cloned tree: either a `staff/` path added to
`.gitignore` and served only from the password-gated site, or a separate staff
repository. Extend the verification rail in the project memory
(`block-module-standard.md`) from the page surface to the repo surface — its current
staff-leak grep checks rendered pages, not tracked files.

### Cost, risk, and how to tell it worked

Cost: one repo move plus a link update. Facilitators lose one-command access from the
teaching clone and need a second checkout or the gated site — the only real friction.

How to tell: P2 baseline scores stop clustering at 5/5 (see C2 for the instrument that
measures this), and P5 catch rates stop being uniform across a cohort. Before the fix,
neither number can be interpreted at all, which is the actual damage: four blocks
currently produce data that cannot be read.

---

## C2 — Calibrate the P2 baseline against the key

**Value: high. Risk: low. Depends entirely on C1 landing first.**

### What exists today

`instruments/p2_dyno/SCORE_SHEET.md` asks the student to fill `Baseline P/F` and
`After P/F` for D01–D05 and compute a delta. Every one of those ten judgments is made by
the student, uncalibrated, by someone who wants a positive delta, and is never checked
by anyone. The dyno is the strongest instrument in the week and its grading is the
softest part of it.

The page already knows. `p2.html:236`: *"Expect fails: a clean 5/5 usually means soft
grading, not a great harness."* And the troubleshooting table at `p2.html:505` lists the
symptom (*"Baseline is 5/5"*), the cause (*"Soft grading — you read the answers as their
author's friend"*), and the remedy (*"rescore strictly"*). The failure is diagnosed and
staffed with nothing but the student's own discipline.

### What changes

After the student locks the baseline column and writes it to disk — and only then —
release the track `FACILITATOR_KEY.md` as a one-way calibration sheet. The student
re-marks their own five baseline rows against it and records a second number: **how many
of their five PASS/FAIL calls matched the key.** That agreement rate, not the delta,
becomes the P2 deep mark alongside the dyno line in `MEASUREMENT_SPINE.md:126`.

### Why

The delta is a difference of two numbers the student authored. The agreement rate has a
right answer authored by someone else. It is the cheapest way in the whole week to make
a student discover, on Tuesday morning, that they grade themselves generously — before
that habit reaches the P8 hold/degrade matrix, which reuses these same D01–D05 case IDs
(`PASS_BARS.md:56`).

### Cost, risk, and how to tell it worked

Cost: one paste and about five minutes.

Risks: (a) worthless if C1 has not landed — a calibration sheet that was readable all
along measures nothing; (b) students may treat the key as the standard for the *after*
column too, which would collapse the instrument. The release must be explicitly one-way
and after the baseline is on disk. Write that constraint into the stage, not into a
facilitator's intention.

How to tell: agreement rate is a distribution. If it comes back uniformly 5/5, either
the cohort grades well or the key leaked — check against C1. A cohort mean below ~3/5
means the *dyno delta*, which the whole block rests on, was never measuring anything, and
that is a finding worth having.

---

## C3 — Replace two spine headlines with one number the student cannot award himself

**Value: high. Risk: low-medium.**

### What exists today

`MEASUREMENT_SPINE.md` requires four headlines per block × 9 blocks.

**Headline 1, Ritual health 0–3** (lines 48–58) awards one point each for: a LIVE
Direction Brief, a complete Operator Log, and an `ADVERSARIAL:` line in the log. All
three facts are already recorded in the artifacts themselves. The field transcribes
them. It reads 3/3 for anyone who followed the block page, because the block page walks
you through earning each point.

**Headline 3, Work quality STRONG/ADEQUATE/WEAK** (lines 70–79) is a lookup table from
the adversarial line the student wrote sixty seconds earlier. The file defines STRONG as
*"Adversarial **stood**"*, ADEQUATE as *"Usable under **wounded**"*, WEAK as
*"Adversarial **failed**"*. Neither field can be wrong, so neither teaches on repetition
1, 3, or 9.

Meanwhile `ADVERSARIAL_REVIEW.md:88-89` already produces the good data — a per-claim
`SURVIVES / WOUNDED / DEAD` ruling on every bar the student marked met — and **nothing
in the course harvests it.** It is generated nine times and discarded nine times.

### What changes

Delete both fields. Replace with an **overclaim count**: of the MVP bars you marked met
in the pass-bar draft, how many did the adversarial mark WOUNDED or DEAD. The row
becomes:

```
overclaim n/m · brief accuracy · time to result · one-line note · deep mark
```

Add one field to the `pulse-adv` beat: **what the adversarial took away** — name each
WOUNDED or DEAD claim and what you did about it. An empty field is legitimate and is a
signal a facilitator can act on.

### Why

Overclaim is adjudicated by a party other than the student. It can be wrong. And it is
the only quantity in the course that should visibly *fall* from B0 to P8 — the first
evidence a student ever gets that their own self-assessment is improving. Everything
else in the spine either rises (which flatters) or is definitionally correct (which
teaches nothing).

### Cost, risk, and how to tell it worked

Cost: zero new beats. The measurement row gets shorter, not longer — likely 3–5 minutes
down to 2–3, recovering roughly 9–18 minutes across the week.

Risk: a student can suppress overclaim by marking fewer bars met before the attack. This
is partly self-correcting — unmarked bars stay "not yet" and block the floor — but the
facilitator rollup must read **overclaim alongside met-count**, never alone. Write that
into `FACILITATOR_ROLLUP.md` as a paired column, not as guidance.

How to tell: plot cohort mean overclaim by block. A downward slope B0→P8 is the course
working. A flat line near zero with a falling met-count is the gaming failure above. A
flat line near zero with a *rising* met-count means the adversarial has gone soft — which
is exactly what C4 detects.

---

## C4 — Make cross-engine adversarial mandatory where it is already free

**Value: high. Risk: low.**

### What exists today

The adversarial earns its nine repetitions: the artifact under attack differs genuinely
every block, and the beat can take a claim away. Keep all nine. But the challenger is
one model family running one frozen prompt that instructs it to *"Prefer false NOT YET
over false pass"* (`ADVERSARIAL_REVIEW.md:103`) — so NOT YET is the house output
regardless of the work — and the course has **no way to distinguish a soft review from a
strong artifact.**

`ADVERSARIAL_REVIEW.md:141` names the control and staffs it with nobody: *"Spot-check
adversarial chats: if the model is polite, students under-pasted or used the build
chat."*

Cross-engine review exists in the file twice, both times as a stretch —
`ADVERSARIAL_REVIEW.md:42` (*"Cross-engine stretch (recommended when feasible)"*) and
line 130 (*"Stretch / distinction"*). The two lines disagree about the second engine:
line 42 says OpenCode, line 130 says Claude. **It appears nowhere on the learner
surface** — a grep for "cross-engine" across all of `site/` returns nothing.

### What changes, and a correction

One candidate audit proposed P3, P5 and P8 on the grounds that OpenCode is already
running in all three. **That is wrong for P8.** Verified tool lines:

- `p3.html:32` — `Codex app + OpenCode (Grok) · instruments/p3_frozen_brief`
- `p5.html:32` — `Codex app + OpenCode bounds compare · intake pack`
- `p8.html:32` — `Codex app (re-pointed) · hosted open model · instruments/p8_hold_degrade`

P8 has no OpenCode (zero occurrences in the page). But P8 has something better: the
student has just re-pointed to a **hosted open model of a different family**, already
wired and already trusted enough to run D01–D05 against. That is the cleanest
cross-engine surface in the week.

So: mandatory cross-engine adversarial at **P3 and P5 via OpenCode** (zero setup cost —
it is already open), and at **P8 via the re-pointed open endpoint** (zero setup cost —
it is already configured). Record both verdicts side by side in the log.

### Why

`PASS_BARS.md:36` rules that model self-praise is not evidence; the pulse then makes a
model's one-word mood the top-line Quality score for the block (C3 removes that half of
the problem). A second engine on the same paste pack, at a block the student believes
they passed, is a designed wrong-discovery event: the student finds out their reviewer
had a blind spot, on evidence, in ten minutes. The course already teaches predict-then-
test at P5 and P6; this is the first time it turns that method on the operator's own
judgment.

### Cost, risk, and how to tell it worked

Cost: roughly ten minutes at three blocks. OpenCode cannot read the local files, so the
student pastes excerpts — more work at exactly the moment they are tired. Mitigate by
reusing the paste pack already assembled for the primary review rather than building a
second one.

Risk: the second engine may also say *stood*. That is still information, but a
facilitator must be ready to name what it does and does not prove rather than letting it
read as vindication. Also resolve the OpenCode/Claude contradiction between
`ADVERSARIAL_REVIEW.md:42` and `:130` in the same edit.

How to tell: the disagreement rate between engines is the number to watch. Near zero
across a cohort means the paste packs are too thin to differentiate reviewers — the
under-pasting failure the file names at line 141, finally measurable.

---

## C5 — Score the Direction Brief as a forecast

**Value: high. Risk: medium — the mechanism is one required word.**

### What exists today

The Direction Brief is the most-repeated beat in the course (`pulse-brief`, 9 of 9), and
**nothing anywhere tests whether a brief was any good.**

`MEASUREMENT_SPINE.md:60-68` marks Mission HIT/PARTIAL/MISS. HIT is defined as *"Stated
outcome exists and matches the LIVE brief's 'done looks like'"* — which does point back
at pre-registered criteria — but line 68 then frames it as outcome: *"Mission is about
**the artifact/state**, not effort."* Students read HIT as "I finished," and the field
collapses into a duplicate of the log verdict.

### What changes

Keep the field. Retitle it **brief accuracy**. Change the question from *did the outcome
exist* to: *did the artifact match the "done looks like" you wrote before the run — and
which of the five brief fields would you write differently now?* Require either a named
field or an explicit *"none held better than expected, because …"*.

The five fields are fixed and named in `DIRECTION_BRIEF.md`: Outcome, Done looks like,
Bounds, Evidence standard, Stop / hand-back. Naming one is a small, checkable act.

### Why

This makes the brief a forecast that gets scored, using a beat that already exists. The
operator discovers that their acceptance criteria were unbounded, uncheckable, or aimed
at the wrong artifact — which is precisely the failure the brief exists to prevent at
work on Monday. Field 2 already sets the standard (*"If it can't be checked, it isn't a
criterion"*); nothing currently checks whether the student met it.

### Cost, risk, and how to tell it worked

Cost: zero new beats. Slightly longer measurement dialogue, offset by C3's deletions.

Risk: it is easy to answer "the brief was fine" nine times. **The named-field
requirement is the entire mechanism.** Without it this reverts to a mark and should not
be shipped at all — a soft version of this change is worse than the status quo because it
adds prose without adding a constraint.

How to tell: tally which of the five fields gets named most often across a cohort. If
one field dominates — very likely *Done looks like* or *Evidence standard* — that is
direct curriculum evidence about where brief-writing instruction should go. If students
name no field at all in most blocks, the requirement was not enforced.

---

## C6 — Run the Transfer chat at three blocks, not nine

**Value: high. Risk: medium — the mitigation must ship in the same change.**

### What exists today

`pulse-transfer` is required at all nine blocks (verified: 1 per page × 9). It opens a
separate chat to develop a seed the mission stage just produced. The block pages say so
in their own copy:

- `p4.html` `pulse-transfer` detail: *"Develop the seed you banked in Stage 06 — read
  your Transfer Seed note back to it."*
- `p7.html` `pulse-transfer` detail: *"the machine-choice seed and draft horizons from
  Stage 06 are confirmed in place."*

`operator/TRANSFER_30_60_90.md` has circuit-seed sections for **P2 through P7 only**
(lines 130–172). There is no B0, P1, or P8 seed section. Correspondingly, in-mission
seed checks exist for exactly those six blocks: `p2-transfer`, `p3-transfer`,
`p4-transfer`, `p5-transfer`, `p6-transfer`, `p7-transfer`.

At B0 the required output is, in the file's own word, a **fingerprint** — `b0.html`
`pulse-transfer` detail: *"A session-log row is required even if the seed is small today
— every block leaves a fingerprint on this file."* A row that exists to prove the session
happened.

**One correction to the candidate claim:** P1 is *not* an empty fingerprint. Its detail
reads *"One recurring product on your real desk named as a machine candidate."* That is
real content — it simply has no in-mission check to carry it, which is why P1 needs the
seed line added rather than removed.

### What changes

Run the Transfer **chat** at three blocks: B0 (name the one real workload the week's
seeds will land on), P7 (draft 30/60/90 from the accumulated seeds), P8 (seal under
adversarial attack — `p8.html` already merges the pulse and the seal into one visit).

At P1–P6, keep only the in-mission seed line. The six checks already exist; **promote
them from stage suggestions to floor bars**, and add the equivalent one-liner to P1.
Delete the session-log table (`TRANSFER_30_60_90.md:108-112`); date the seeds instead.

### Why

At six of nine blocks the Transfer chat re-does work the mission stage just produced, in
a second conversation. The session log's stated job is defeating the Friday dump
(`TRANSFER_30_60_90.md:283`: *"Session log shows entries across the week (not a single
Friday dump)"*) — dated seeds prove exactly the same thing without a parallel table.

Recovers roughly **30–60 minutes** (six sessions at the file's own 5–10 min timebox) and
removes 6 of 63 ritual checkboxes.

### Cost, risk, and how to tell it worked

Risk, and it is the real one: the every-block cadence is defended as building the
outer-loop habit. **If the in-mission seed lines are not enforced as floor bars, the
outer loop goes empty and P8 seals over nothing.** The seed lines must move to the
mastery floor at P1–P7 *as part of this change*, not as a follow-up. If that half cannot
be done in the same edit, do not do this item.

How to tell: at P7, count seeds present per student before the horizon draft. Under six
means the promotion did not take and the cadence should come back.

---

## C7 — Delete `pulse-mission` and the nine closure checks

**Value: medium-high. Risk: low.**

### What exists today

`pulse-mission` ("Mission ran in a separate build chat") appears on all nine pages. It
cannot fail: by the time a student reads it, it is already true or already false, and no
artifact records which. B0's own copy concedes this outright —
`b0.html` `pulse-mission` detail:

> *Already true if you followed the stages: the build lived in Build — B0 First Light,
> the brief and log live in Operator — Direction & Log.*

The nine `*-done` checks (`b0-done` … `p8-done`, "Block closed under fire") are closure
ceremony with no artifact behind them.

The chat split it nominally polices is already enforced downstream by two things that
break visibly if judgment and build shared a chat: the log's evidence pointers, and the
adversarial paste pack. State lives only in browser `localStorage`
(`site/js/shell.js:293`) — no facilitator, peer, or grader ever reads either check.

### What changes

Delete both. **18 checkboxes removed.** Keep the chat-split instruction as prose at B0
and P1, where the discipline is actually taught, and fold one line into the Brief beat:
*the mission runs elsewhere; this chat holds direction and verdicts.*

### Cost, risk, and how to tell it worked

Cost: none. Risk: the chat split is a genuine discipline that new operators break in the
first two blocks — but a checkbox asserting it does not prevent that, and the prose does
the teaching. `site/js/registry.js` must be updated in the same change; its header
declares the id lists are the single source of truth and the project memory rail forbids
removing ids without it.

How to tell: log chats containing build turns are visible in the transcript. If
facilitators see more of them after the change, restore the B0 prose emphasis — not the
checkbox.

---

## C8 — Run the pass-bar AI dialogue at three blocks; let the floor list carry the rest

**Value: medium. Risk: medium.**

### What exists today

The same claim set is ticked four times per block: once as mission stages, once as floor
bars that restate them near 1:1, once in the `pulse-bars` AI dialogue, and once as the
Quality mark in the measurement row. **Only one of the four — the adversarial — can take
a claim away.**

The `pulse-bars` beat is a real dialogue with a paste prompt (`p5.html`): *"Walk the MVP
list with me one bar at a time. For each bar I answer met or not yet and give an
evidence pointer … Challenge any pointer that is vibe instead of artifact."* Its detail
text is genuinely block-specific — P5's names *"time-ordered detect → isolate → verify,
the bounds comparison, and the written rule-set prediction"* — so this is not pure
boilerplate, and the candidate audit that called it flat duplication overstated.

But the beat's real function is to produce a prediction for the attack, and the floor
list rendered on the same page already is that prediction.

### What changes

Run the AI walk-through at **B0, P2, and P5** — B0 and P2 where students are still
learning what an evidence pointer is, P5 because its bars are the most mechanically
specific in the week and the dialogue there is doing real work. At P1, P3, P4, P6, P7,
P8: the student ticks the mastery-floor list already on the page and pastes that
met-list into the adversarial as a stated prediction. The floor's existing rule — *"if
the adversarial pass wounds an item, uncheck it"* — stays and becomes the visible
consequence.

### Cost, risk, and how to tell it worked

Recovers roughly 18–30 minutes across six blocks.

Risk: the dialogue is where *"a path, not a feeling"* gets drilled. Keeping it at three
blocks, spaced across the week, preserves the drill. If students drift back to vibe
pointers mid-week the adversarial catches it, but a facilitator should spot-check P4
pointers once — that is the longest gap in the new schedule.

How to tell: C3's overclaim number is the detector. If overclaim rises at P4/P6/P7 after
this change while holding steady at P2/P5, the dialogue was load-bearing at more blocks
than three and should be restored at one more.

---

## C9 — Deliver the ninety-second defense to a human

**Value: medium-high. Risk: medium.**

### What exists today

`p8-defense` is the capstone of the week. Its audience is a language model roleplaying a
skeptical manager (`p8.html` stage 07): *"You are a skeptical manager deciding whether
this endpoint may be used, and for which work."* The student **types** the defense, takes
the critique, and is then told to *"stand up and say the fixed version out loud once
against a clock."* Failure means the model says the wording was long.

The pass condition is already written in terms of a listener — `mvp-90s` detail: *"a
skeptical manager should leave knowing whether this endpoint is fit for which work"* —
but no listener is staffed.

### What changes

Deliver the ninety seconds to a live listener — a peer, the facilitator, anyone — with a
stopwatch and one pass condition: **the listener must state, unprompted and without
asking a question, which work this endpoint is fit for and which it is not.** If they
cannot, the defense failed and the student runs it again.

### Why

A human listener who cannot restate the fitness verdict is an external referent that can
genuinely refuse to be convinced. That is exactly the transfer being claimed. The model
rehearsal stays — it is a good rehearsal — but it stops being the terminal judge of the
week's capstone.

### Cost, risk, and how to tell it worked

Cost: ninety seconds per student. The cohort is already in the room on Friday afternoon.

Risks: requires cohort time and pairing on the last block, when schedules slip most; and
a shy student may be judged on delivery nerves rather than evidence. Facilitators must
hold the pass condition to **comprehension of the verdict, not polish** — write that into
the stage text, because it will not survive as an intention.

How to tell: first-attempt pass rate. If it is near 100%, the pass condition is being
read charitably and needs the "unprompted, without asking a question" clause enforced
literally.

---

## C10 — Delete the running totals; make time load-bearing or drop it

**Value: low-medium. Risk: medium.**

### What exists today

`MEASUREMENT_SPINE.md:107-116` asks students to hand-maintain a running-totals table:
blocks logged, ritual-perfect count, HIT count, STRONG count, median time, stood/wounded/
failed counts. It is manual aggregation of fields that are themselves derived — and C3
deletes two of the six inputs outright.

**Time to result** (lines 81–89) is the only non-derived number in the spine. The file
is careful about it: *"No stopwatch theater: honest estimate is fine; fiction is not."*
And then `FACILITATOR_ROLLUP.md:28` instructs facilitators to do nothing with it:

> | `T` only, quality OK | Leave it — mastery &gt; speed |

A number honestly estimated, never calibrated, and explicitly acted on by no one is the
clean case of output nobody reads. It costs 3–5 minutes nine times.

### What changes

Delete the running-totals table. Keep time to result, and give it the one consequence it
lacks: **a time outlier triggers a facilitator question about whether the block's scope
was wrong, not about the student's speed.**

### Cost, risk, and how to tell it worked

Risk, and it is why this ranks last: attaching any consequence to time invites stopwatch
theater and speed-chasing, which the file is right to fear (`MEASUREMENT_SPINE.md:207`:
*"If facilitators grade people on speed alone, the school has betrayed mastery"*).
**Directing the consequence at the block's scope rather than the operator's pace is the
entire safeguard, so it must be written that way in the rollup — not merely intended.**
If that wording cannot be got right, delete time to result as well rather than shipping a
half-measure.

How to tell: if the same block shows outliers across many students, scope was wrong and
the block needs narrowing — that is the finding this is for. If outliers are scattered
across students and blocks, the number is measuring individual pace and should go.

---

## C11 — The dyno hands the model its own grading criteria

**Verdict: theater dressed as measurement.** This is the highest-value single fix in the
document and it was missed by three of the four audits; it is recorded here because it
was verified directly against the files.

**What exists today.** P2's baseline dispatch (`site/blocks/p2.html:212`) tells the
student to paste:

> `Open the file instruments/p2_dyno/[TRACK]/cases/[CASE FILE] and run the task in it
> exactly as written.`

The model opens the file. Line 3 of that file
(`instruments/p2_dyno/engineering/cases/D01_ci_failure.md`) reads:

> `**Pass if:** response names the failing job, the root error line/theme, and one
> concrete next action. No invented file paths.`

So the model under test reads its own rubric before answering — in the same request. The
identical dispatch is reused at Stage 03, at the cold rescore in Stage 04, and again at
P8 Stage 04 against the open endpoint.

**Why it matters more than it looks.** The course states the rule this breaks, in its own
words, two days later (`site/blocks/p7.html`): *"Feeding the answer key to the system
under test voids the test, and that rule is worth keeping long after this week: never let
the machine being checked see its own check."* P7 teaches the principle that P2 violates,
and P7 makes the student act on it by dropping the `expected_gate` column before the AI
step. A student who notices the inconsistency is right, and the course has no answer.

The measurement damage is specific. A model shown "name the failing job, the root error
line, and one concrete next action" will name those three things, so the baseline is
inflated toward PASS. That compresses the delta the whole morning exists to produce: the
wall changes have less room to move a score that was already propped up. P8 then re-runs
the same contaminated suite and reads hold/degrade off it, so the contamination reaches
Friday's capability-tax numbers too.

**The change.** Keep the externally authored pass condition — that is a genuine strength
(see *Do not touch*, item 5) and the fix does not soften it. Split where it lives:

- Give each case file an `Input` and `Task` the model may read, and move the `Pass if:`
  line into a sibling the model is never pointed at — `D01_ci_failure.grader.md`, or a
  single `GRADER.md` per track holding all five conditions.
- The student reads the grader file before scoring, exactly as they do now
  (`p2.html:190` already has them read every pass-if line up front).
- The dispatch is unchanged in shape, so the do-step stays a single paste.

**Cost.** Ten case files split into ten plus two grader files; the P2 page's Stage 02
click-list gains one line naming where the pass conditions now live; `p2_dyno/README.md`
and the P8 instrument README each gain a sentence. No `data-check-id` changes. Under an
hour of work.

**Risk.** Low. The main one is drift: a case file and its grader can fall out of sync in
a way the current single file cannot. Mitigate by keeping the grader lines in one
`GRADER.md` per track rather than ten sibling files, so the set is read as a unit.

**How to tell whether it worked.** Baseline totals should fall relative to previous
cohorts — a lower stock score is the correct outcome, not a regression — and the
before/after delta should widen. If baselines do not move at all, the models were not
leaning on the rubric and the fix cost an hour to establish that, which is still worth
knowing.

---

## Rulings against candidate items

**Deleting the `#floor` section (69 `mvp-*` checkboxes). Ruled against.** One audit
proposed keeping only four floor items and deleting the other 65. Two verified facts
defeat it:

1. **The evidence standard lives there.** Of 55 occurrences of *"Evidence looks like"*
   across the nine pages, **54 are on floor items** and 1 is on a stage item. That prose
   is the most valuable writing in the block pages — `p1.html:726`: *"Evidence looks
   like: you rerunning it in front of someone without re-prompting the mission from
   memory."* Deleting the checkboxes deletes the standard.
2. **The floor is what the adversarial attacks.** `ADVERSARIAL_REVIEW.md:63` requires the
   paste pack to include *"Your **draft** MVP self-check (which bars you think you met)"*,
   and step 3 rules per claim on that list. The floor list is the prediction. Removing it
   removes the input to the only beat that can take a claim away.

The redundancy the audit correctly identified is real, but the right cut is the
**pass-bar dialogue** (C8), not the list itself. C3's "what the adversarial took away"
field delivers the benefit the audit wanted — a field that can be empty — without
removing the standard.

The audit's duplication counts were also partly wrong. Verified floor-item counts are
b0:8, p1:6, p2:7, p3:7, p4:7, p5:8, p6:9, p7:8, p8:9 = 69. Its claims of "6 of 7 in P1"
and "6 of 7 in P2" are miscounted (P1 has 6 floor items, all duplicative; P2 has 7, all
duplicative). Its claims of "8 of 9 in P6" and "8 of 9 in P8" are correct. It also missed
a genuinely additive item: `p3` `mvp-join` is not a restatement — *"A model that invented
an ID or joined on a display name fails this bar even when the answer happens to be
right"* — and would have been deleted.

**Dropping the `ADVERSARIAL: stood/wounded/failed` line from the Operator Log. Ruled
against, partially.** One audit proposed removing it from both the log and the spine.
Remove it from the **spine** — C3 does that, replacing the Quality headline it feeds. Keep
it in the **log**: it is the scar, it costs one line, and it is the only thing a
facilitator can scan quickly. The per-claim list is the record; the summary line is the
index.

**Cross-engine at P8 via OpenCode. Corrected.** P8 does not use OpenCode (verified: zero
occurrences in `p8.html`; tool line reads *"Codex app (re-pointed) · hosted open model"*).
Use the re-pointed open endpoint instead — see C4.

**"At B0 and P1 there is no seed at all." Corrected.** True of B0, false of P1 — see C6.

**Second-engine audit findings. Unavailable.** The `codex_theater.md` run terminated
before producing its T-item list; nothing could be merged from it beyond the timebox
arithmetic, which I verified independently.

---

## DO NOT TOUCH

**1. The adversarial review, all nine repetitions.** The only beat that can take a claim
away from the student. The artifact under attack differs genuinely every block, so the
repetition builds a reflex rather than recording attendance. C4 strengthens it; nothing
should reduce its cadence.

**2. The Direction Brief, all nine repetitions.** Reflex-building, and the content
differs genuinely every block. Five fields under five minutes is the right shape. C5
scores it; it must not be cut.

**3. The Operator Log verdict, all nine repetitions.** `REJECT` with real evidence is the
best moment the course offers, and the prompt says so directly: *"Remind me: REJECT with
real evidence is a successful operator act."* A student who honestly rejects their own
work has learned the thing the week exists to teach.

**4. The P5 unlabeled intake batch.** Seven items, four clean, three poisoned, no labels
on the artifacts. This is the course's flagship falsifiable activity — the student can
simply miss a catch. The three poison classes (false citation, field contradiction,
hostile instruction) are genuinely distinct failure modes, and the absence-of-effect
proof is a real containment test. C1 exists to protect exactly this.

**5. The P2 dyno's externally authored `Pass if:` lines.** Each case opens with a
pass condition written by someone other than the student —
`instruments/p2_dyno/engineering/cases/D01_ci_failure.md`: *"Pass if: response names the
failing job, the root error line/theme, and one concrete next action. No invented file
paths."* This is the one place in the week where a criterion arrives from outside. C2
extends it; do not soften it.

**6. The block-page depth sections.** `p2.html:516` — *"a suite you always pass has
stopped measuring … An instrument is alive as long as it can still tell you something you
don't want to hear"* — is the best writing in the repo and is doing real teaching.

---

## Phased plan

### Before the next cohort — ship these

| Item | Why now |
|---|---|
| **C11** | An hour of file surgery that restores validity to the dyno, which P2 and P8 both read. Ship it first — C2's calibration and every hold/degrade number depend on a baseline the model was not coached toward. |
| **C1** | Repo move plus link update. Four blocks currently produce uninterpretable data; every other measurement change is worth less until this lands. |
| **C7** | Pure deletion. 18 checkboxes, `registry.js` updated in the same commit. No content risk. |
| **C3** | Text-only change to `MEASUREMENT_SPINE.md` and the nine embedded end-of-block prompts, plus a paired column in `FACILITATOR_ROLLUP.md`. |
| **C4** | Two lines on `p3.html` and `p5.html`, one on `p8.html`, plus resolving the OpenCode/Claude contradiction in `ADVERSARIAL_REVIEW.md`. |
| **C2** | Small stage addition at P2. **Sequence after C1 in the same release** — it is worthless before. |
| **C5** | Retitle plus the named-field requirement. Ship the requirement or do not ship the item. |

### Needs a cohort's evidence first

| Item | What to measure |
|---|---|
| **C6** | Run one cohort with the in-mission seed lines promoted to floor bars *while keeping the nine Transfer sessions*. Count seeds present at P7. If six seeds land without the chat carrying them, cut the six sessions in the following cohort. |
| **C8** | Ship C3 first, then read overclaim by block. If P4/P6/P7 overclaim holds steady across a cohort, the dialogue is safe to cut there. |
| **C10** | Ship the running-totals deletion immediately (it is derived data and C3 removes two inputs). Hold the time-outlier consequence until one cohort's time data shows whether outliers cluster by block (scope problem, actionable) or by student (pace, not actionable). |

### Bigger rewrite

**C9** changes Friday's schedule and requires facilitator training on the pass condition.
Pilot it with one cohort as an optional addition alongside the model rehearsal, holding
both, and compare what the human listener catches that the model did not. If the answer
is "nothing," the model rehearsal was sufficient and this item dies cheaply.

**The pulse's shape after all of this.** Seven beats become five at most blocks, six at
B0, P2, P5, P7 and P8. Checkbox count falls from 225 to roughly 196. Three beats run at
all nine blocks — brief, log, adversarial — and those are the portable core. The pocket
card should teach those three; measurement and transfer should be presented as *what the
core produces*, not as beats of equal standing.

This is a real cost, and it should be named: the pulse's uniformity is itself a teaching
device. The same shape nine times is what makes it portable to a desk with no course
around it, and a schedule where beats appear and disappear by block is harder to carry
home. The mitigation is the three-beat core above. If the core cannot be made to feel
like the whole sport, keep the uniform seven and take the attention cost knowingly —
but do not keep it by accident.

---

## The line: softening logistics vs. softening evidence

The recent direction of travel is right, and it is worth naming precisely so it does not
drift.

**Softening logistics and dependencies — good, keep going.** Commit `718e884` ("Soften
staff-dependency language") removed promised turnarounds and, more importantly, removed
progress gates conditional on someone else acting: `staff instructions` → `the posted
pin`, `staff-pinned Ollama` → `the pinned Ollama`, `Staff key` → `Course key`. Pre-work
had told students to wait for a pin before installing anything; every one of those now
states the preference and gives a way forward. Not one evidence bar moved. Commit
`287cb75` did the same on the other side — a learner-facing re-point runbook so a student
can execute the P8 endpoint change themselves. **The test that makes this safe: after the
edit, is the thing the student must *prove* identical?** In both commits, yes.

**Softening evidence standards — fatal, and the course has already caught itself once.**
Commit `4336d34` stripped answer-leaking annotations from `mission_flesh/p7/rows.csv`,
with the reason stated exactly right in the message:

> *The text field is what the AI step reads; the (false) markers were feeding the system
> under test its own answer key.*

That is the correct principle, correctly applied — and it was applied to one CSV and
never generalized. **C1 is the same defect at repo scale.** The same sentence describes
it: `mission_flesh/p5/FACILITATOR_KEY.md` is in the tree the student clones and the model
can search, and it is the answer key to the system under test.

The discriminator, for any future change:

- **Logistics** — who does it, when it arrives, how many steps, which button, what to do
  if a dependency has not landed. Soften freely. Friction here costs attention and buys
  nothing.
- **Evidence** — what counts as proof, who adjudicates it, whether the adjudicator can
  see the answer, whether a claim can be taken away. Never soften. If a change makes a
  bar easier to pass without making the underlying capability easier to hold, it is a
  softening of evidence wearing a logistics costume.

Two live examples of the costume, both in this document: the P2 troubleshooting row that
diagnoses soft grading and prescribes "rescore strictly" (`p2.html:505`) is a logistics
answer to an evidence problem — C2 replaces it with an adjudicator. And
`ADVERSARIAL_REVIEW.md:141`'s instruction to spot-check for polite reviews names an
evidence failure and staffs it with a facilitator's spare attention — C4 replaces it with
a second engine.

Both were written as if the standard were held. Neither held it. That is the failure mode
to watch for: not a bar being lowered, but a bar being asserted with nothing behind it.
