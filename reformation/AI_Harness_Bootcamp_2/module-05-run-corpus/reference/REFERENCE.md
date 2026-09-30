# Reference: Module 5 — Improve from observed failures

**Frozen on:** 2026-09-30 (revision 3)  
**Scope:** one three-hour observed-run module built around eighty fictional desk runs `R-001`–`R-080` for East Yard to Clinic O-2 oxygen cylinders  
**Course objective:** freeze an outcome-blind sample, write first-failure notes before categories, reconcile counts, infer two literal strings, and configure them in a supplied protected control that performs a case-sensitive substring conjunction

## 1. The need

Memorable failures are a poor automation agenda. First-failure notes have to exist before categories. Not every semantic miss should become a checker, and the learner does not implement the checker.

**Done (revision 1, superseded):** the learner freezes a sample of twelve runs, writes first-failure notes, reconciles counts, configures a spec whose fail token is `20:50Z`, and the supplied control fails `run-07.md`, passes `run-02.md`, and holds on a missing path.

**Revision 2 (superseded):** the learner freezes the first sixteen runs as an outcome-blind sample, writes one first-failure note per run before any category, reconciles counts to sixteen, infers two literal strings from the notes, writes them into a JSON config under `all_present`, and runs the supplied `predicate.py <run-file> --config <predicate.json>`. The control exits 1 when both literals are present as substrings and 0 otherwise. Known-bad exits 1, known-good exits 0, missing path prints `HOLD: missing input`.
**Revision 3 (current):** same procedure. Held-out practice labels (R-017–R-080) use the field `promotion_failure` (true when the run text contains a receipt-to-release promotion claim, i.e. a stamp or statement claiming release while the source scan shows RECEIVED). This is text-grounded only; it is not a claim about physical release outside the document. The canonical literals "RELEASED" and "source_status: RECEIVED" produce a false positive on UNRELEASED (substring collision) and can produce a false negative on differently phrased or cased promotion claims. Labels were relabeled from the actual run text. The schema in held-out-truth.json is now "run_id: {promotion_failure: bool, note: str}". No alias for prior field name.
## 2. Case

Synthetic thread-verification runs for the Blue Gauge movement. The sample `R-001`–`R-016` contains exactly five runs in which both literals are present (staff truth: `R-002`, `R-005`, `R-009`, `R-012`, `R-016`). The remaining eleven sample runs and the held-out `R-017`–`R-080` contain distractors, near-miss identities, three true-but-broken handoffs, supplied hostile text, a time/supersession trap, and a received/released condition-word collision (including `UNRELEASED` containing the characters of `RELEASED`).

The full pile of eighty runs is the harness input. The learner still opens at least one decisive item and writes the notes by hand.

## 3. Protected answer model

- Eighty runs exist; sample is the first sixteen.
- The frozen config contains exactly two distinct nonempty strings under the key `all_present`.
- `predicate.py` on a file containing both literals exits 1 and prints `MATCH`.
- A file containing at least one literal absent exits 0 and prints `PASS`.
- Missing path exits 1 and prints exactly `HOLD: missing input`.
- Malformed config (not exactly two distinct nonempty strings, extra keys, empty list, duplicate, non-JSON) exits nonzero and prints `HOLD: malformed config`.
- Learner files do not contain a second predicate implementation.
- Learner-facing files contain none of the staff promotion identifiers as answers and no operative literals.

## 4. Assessment

Class F / human panel remains unmeasured. Do not report timing without measurement.

This revision 3 supersedes revision 2. The digest was recomputed after the explicit contract amendment for the held-out label field and ground-truth definition. The change is adoption of the replacement scenario per the plan; the core procedure, predicate contract (exactly two distinct nonempty case-sensitive substring literals under all_present), and batch behavior are unchanged.
