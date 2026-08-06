# Facilitator rollup — thin view (Move 4)

Companion to the student `MEASUREMENT_SPINE.md`.  
Do **not** build a parallel heavy dashboard.

## When

- End of day: 5–10 min scan  
- End of P2 / P5 / P7 / P8: slightly longer (deep marks matter)

## What to collect

One row per student, read off their spine.

| Student | Blocks logged | Bars met `m` | Overclaim `n` | Brief field named most | Flags |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |

### The paired column

`m` and `n` are entered together or not at all. There is no cell in this table for an overclaim count on its own, and you should not make one.

One wounded bar out of nine claimed and one wounded bar out of two claimed are different students with the same ratio. The first is a strong operator whose reviewer found a real gap. The second is claiming almost nothing, which reads as caution and is usually an empty mastery floor wearing a good number. You can only tell them apart by reading the denominator in the same glance.

The number that matters is the **slope of `n` down the week** while `m` holds or grows. That is calibration. `n` falling because `m` is falling is not.

## Flags

| Code | Meaning |
|---|---|
| `A` | No required review-boundary evidence: `ADVERSARIAL:`, integrated reviewer result, P4 audit/MCP/verifier set, P6 two-wave PASS plus revised command center/state, or P7 Wave 1 PASS record, final Wave 2 receipt/PASS, and rule comparison |
| `B` | Brief accuracy entered with no named field — “the brief was fine” in longer words |
| `M` | Brief accuracy MISS |
| `O` | Overclaim near zero while bars-met falls — claiming less to protect the ratio |
| `R` | Overclaim near zero while bars-met rises and the second engine never disagrees — the review has gone soft on a thin paste pack |
| `S` | A circuit seed still empty or undated by P7 |
| `T` | Time outlier — see below, and read it as a question about the block |

## Interventions

| Flag | Move |
|---|---|
| `A` | Stop content. Restore the module&#x27;s real review boundary. Do not add a generic attack where the live page already integrates review. |
| `B` | Sit with the student and their brief. Make them name a field out loud and say what they would write instead. One minute, and it usually lands on *Done looks like* |
| `M` | Narrow the scope of data. Never narrow the evidence standard |
| `O` | Read the mastery floor with them. An unticked bar is *not yet*, and *not yet* holds the floor open — the ratio bought them nothing |
| `R` | Read their paste pack, not their verdict. Thin excerpts give a reviewer nothing to attack. Send them back with the full outputs, the same frozen prompt, and no softening |
| `S` | Seeds before horizons. A P7 horizon draft built on empty seeds seals over nothing at P8 |
| `T` | Do nothing to the student. See below |

## Time outliers point at the block

One student long on one block is pace, and pace is not a finding. Say nothing to them.

**Several students long on the same block is a finding about that block.** It was scoped too wide: too much data, too many cases, or an instrument that needs a smaller starting state. Record it against the block and narrow the data next time — never the judgment standard, and never the evidence pointers.

Do not compute a median across a student's nine blocks and do not rank the cohort by minutes. The blocks are not repeats of one another, so the middle of them is not a fact about anybody. A fast weak row and a slow strong row are not on the same axis.

## Cohort health (one glance)

- Mean overclaim by block, B1 → P8 — the **slope** is the reading, not any single value
- Mean bars-met by block over the same range, read beside it
- Share of rows carrying a named brief field
- Which of the five brief fields the cohort names most often
- P3 finding-defeat and terminal-rule pattern; P4 audit/cold-retrieval/verifier pattern; P5 staging-inventory drift, runtime-hash, and scope-escape evidence; P7 batch leverage and second-wave pattern; P8 two-reviewer disagreement rate

**On disagreement.** P3 has two verifiers whose only job is to defeat findings; read the dispositions and check that defeats cite a later authoritative source rather than a head count. P8 sends the same review pack through two engines; read its reviewer-disagreement rate beside the underlying pack. Near-zero is a prompt to inspect, not evidence of either cleanliness or failure by itself. P4 uses a cold retriever and a deterministic brain verifier for different jobs. P5 uses deterministic integrity receipts rather than a second model.

## Spot-checks worth the minutes

- **P4 completion evidence.** Read three students&#x27; <code>RUN_STATE.md</code>, <code>Audit.md</code>, <code>Retrieval/Answers.md</code>, <code>Retrieval/Repair_Check.md</code>, MCP receipts, brain-verifier output, and external integrity snapshot. Confirm the cold answers resolve to vault notes, the fresh check names the applied repair, the disposable mutation returns HOLD, and the untouched live vault returns PASS.
- **P6 changed-world evidence.** Read three students&#x27; recorded Wave 1 PASS, final <code>command_center.html</code>, final <code>mission_state.json</code>, and Wave 2 PASS. Confirm all 18 evidence items are accounted for, superseded and duplicate items do not drive current work, the chosen intent is preserved, and the page visibly distinguishes <code>NEW</code>, <code>CHANGED</code>, <code>CANCELLED</code>, and <code>UNCHANGED</code>.
- **P7 spreadsheet leverage.** Read three students&#x27; recorded Wave 1 verifier PASS, final Wave 2 receipt and verifier PASS, current `workboard.xlsx`, saved `workboard_24h.xlsx`, and branch-rule comparison. Confirm wave one fills eight result columns for 60 rows, the visible four-branch canvas writes those rows back to `AI Workboard`, the one-place rule change names every affected row and downstream field with zero row-by-row edits, and wave two fills 20 new rows for 80 total through the same saved graph.
- **P2 intake receipts and refusals.** Read three students&#x27; `normalized/intake_receipt.json`. Confirm the damaged partner file emitted no rows and that the check which caught it counts identifiers, not rows — a row count matches at eight and eight and proves nothing. Confirm both hooks appear trusted in `/hooks` and that each has refused something the student actually attempted. The common failure is a hook that has never fired, which looks identical to a hook that works.
- **Adversarial paste packs.** A polite reviewer means the pack was thin or the build chat was reused. Fix the pack; never soften the prompt.
- **Transfer seeds.** P1–P7 write dated seeds during their own module closeouts. Only P7 and P8 use the shared `P7–P8 — 30/60/90 Plan` chat, because both visits continue the same saved plan in the same role. At P7, count the seeds and read the dates. Seven seeds all dated the same afternoon is a Friday dump with extra steps.
- **Pass-bar dialogue.** The walk-the-list-with-the-AI beat runs at B1 and P5. P2 uses its intake refusals, its two hooks, and the run against lookalike material. P4 uses its human audit, MCP receipts, cold retrieval, fresh repair check, brain verifier, and external integrity proof. P6 uses its Wave 1 PASS, the revised command center/state, and the final Wave 2 PASS. P7 uses the recorded Wave 1 PASS, final Wave 2 receipt/PASS, and branch-rule before/after comparison. Do not add a separate attack to those blocks. At P1 and P8 the student ticks the floor before the attack. P3 checks outcomes as artifacts are produced, then uses its refuting verifiers and the planted claims against its provenance gate as the review.

If a cohort needs rescue, narrow the **scope of data**. Rescue is restoring the pulse and the evidence, not adding metrics.
