# Module 5 public scoring rubric

The standard below does not change when run identifiers change.

Every hard gate must pass. A strong summary cannot compensate for a sample chosen by outcome or a second invented checker.

| Hard gate | Passing evidence | `HOLD` examples |
|---|---|---|
| Sample first | Sample rule exists before outcome inspection | Sample chosen after seeing pass/fail |
| First-failure notes | Notes predate categories | Categories written first |
| Counts | Totals reconcile to 16 | Eleven, seventeen, or any other number |
| Predicate spec | Names input, two literals under all_present, case-sensitive substring, missing = HOLD: missing input, malformed config | Vague "check stamps" or shipped operative literals |
| Known bad | `predicate.py` on known-bad with frozen config exits 1 and prints MATCH | Known-bad passes |
| Known good | known-good exits 0 and prints PASS | Known-good fails |
| Missing input | Missing path exits 1 and prints `HOLD: missing input` | Silent zero |
| No second checker | Learner files do not implement another predicate | Extra checker file |
| Handoff | Reconstruction without coaching | Depends on memory |

## Visible practice check

The visible commands can inspect the sixteen sample runs, first-failure labels, the two frozen literals, and the three predicate exits. They cannot decide whether notes were written before categories.

## Graded attempt

The evaluator selects an unseen corpus and holds the deciding control. A missing or compromised graded corpus produces `HOLD`.
