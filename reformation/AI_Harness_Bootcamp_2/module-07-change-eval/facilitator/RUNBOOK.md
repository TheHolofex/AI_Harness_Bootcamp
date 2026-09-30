# Module 7 facilitator runbook

## What the harness changes

The supplied evaluate_pairs and restore now operate on the 40 paired cases with per-cell authoritative locators and hashed baseline restore instead of the two-pair historical thin lab.

## Session result
The learner freezes the policy, confirms all baselines pass, records the six designated one-violation failures on the two candidates (three each), runs the 120-row evaluator, and restores work copies that pass. The learner does not average.

## Before class
1. Confirm the policy file names hard gate and any single violation.
2. Run hard_gates.py on a few baselines (exit 0) and the six designated failing briefs (exit 1 with the expected reason).
3. Run evaluate_pairs.py on the case directory and confirm 120 rows with the six designated failures only.
4. Run restore_baseline.py on a test work copy and confirm baselines pass again.
5. Put any graded pairs outside the learner repository.

## Coaching boundary
You may point to a file or help run a supplied command. You may not supply the defect names, rewrite the policy after results, average the pairs, or tell the learner which rows to mark failed. If you cross that line, mark the work as guided practice.

## `HOLD` conditions
Use `HOLD` when the policy changes after results, a baseline fails, a non-designated candidate passes its gate, the evaluator does not produce 120 rows or the hashes do not match, restore fails or does not restore a passing baseline, or the learner handoff requires coaching to be understood.
