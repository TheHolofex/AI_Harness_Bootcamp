# P8 Hold/degrade — course instrument

**When:** Friday AM (Operator-governed open model)  
**Purpose:** Re-run **the same suite IDs as P2 (D01–D05)** after re-pointing to the hosted open (or alternate) model. Measure hold vs degrade with numbers.

## Continuity rule

| P2 | P8 |
|---|---|
| Baseline + after on commercial/home model | Open/re-pointed model on **same track & case IDs** |

Bring your P2 score sheet (after column) as the comparison baseline for “commercial/home.”  
If P2 after is missing, run commercial once Friday AM then open — still use D01–D05.

## Student flow

1. AUP/policy written **before** re-point (block MVP).  
2. Re-point pack/endpoint per the posted pin.  
3. Cold-run D01–D05 from your track’s `p2_test_suite/.../cases/`.  
4. Score on `SCORE_SHEET.md` (open model column), marking each case against your track’s `GRADER.md`.  
5. Fill hold/degrade matrix vs P2-after (or Friday commercial).  
6. Label each FAIL layer: model / instructions / tests / environment / brief.  
7. Deep mark: `Hold-degrade: open n/5 vs home n/5; refuse: Y/N; transfer SEALED: Y/N`.

## Where the pass conditions live

A case file holds an `Input` and a `Task`, and nothing else. The five pass conditions sit in
`p2_test_suite/<your track>/GRADER.md` — the same five you scored against on Tuesday,
unchanged, so both columns are marked to one standard. That file is yours to read when you
score. The re-pointed model never sees it: it is not named in the cold-run prompts, not
opened on the endpoint, and not quoted back into a case. A system that can read its own check
is not being checked — a model shown the standard writes to the standard, and hold and
degrade stop being distinguishable.

## Timing

5 cases only — finishable Friday morning with policy + defense.
