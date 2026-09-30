# Module 6 facilitator runbook

## What the harness changes
The harness actually processes the full 80-lot pile. It forces exact byte comparison of serialized receipts, refuses existing outputs, enforces the one-line pending_status rule with rack precedence first, and requires digest-checked restore from a distinct baseline. Learner hand-patches and prose authority are visible failures.

## Session result
The learner runs the saved path on two waves (and the stretch revision), changes only the one `pending_status` line in `RULE.md`, proves the exact three (or revised-set) rows move while rack stays held, records zero manual repair, and restores the baseline rule from its distinct hashed copy using the workdir command. All receipts are produced by the supplied adapter; no hand edit is accepted.

## Before class
1. From a fresh work copy created by `prepare_work.py 06 ...`, run the printed first command to produce wave1 baseline receipt. Confirm 80 rows and the key lots reach the states described in the lab.
2. Run wave2 to a different out file. Confirm the two baseline receipts are byte-identical.
3. Edit only the `RULE.md` line to `pending_status: NOT_AUTHORIZED`, rerun wave1 to a new file. Confirm exactly the current pending lots moved to reject/NOT_AUTHORIZED and rack lots stayed RESOURCE_CONFLICT.
4. Run `python3 scripts/restore_rule.py <the-workdir>` . Confirm it prints `RESTORE OK` and a re-run of wave1 matches the original baseline bytes.
5. Run the stretch file under the changed rule. Confirm the predicted membership delta.
6. Put graded batches and their deciding receipts outside the learner repository.

## Coaching boundary
You may point to a file, read a header, or help run a supplied command with its printed arguments. You may not supply the list of which lots are pending in the graded batch, edit a receipt, change `route.py`, or tell the learner the delta before they have run it. If you cross that line, mark the work as guided practice.

## `HOLD` conditions
Use `HOLD` when:
- a lot misses a terminal receipt (OPEN, READY, NOT_AUTHORIZED, or RESOURCE_CONFLICT)
- an unexpected row changes between baseline and changed under the same rule
- a receipt is hand-patched (byte diff from clean re-run on same input)
- restore fails or does not produce a byte-identical baseline receipt
- the rule file is missing, has duplicate or unknown pending_status, or the baseline digest does not match
- the workdir argument is omitted from restore or the target escapes the work tree
- the stretch membership change is not isolated from the policy effect
