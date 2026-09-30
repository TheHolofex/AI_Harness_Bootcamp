# Module 4 facilitator runbook

## Session result

The learner prepares W with prepare_work, verifies restore from the hashed baseline, has a public fault placed, localizes with the probe, makes one authorized replace, and proves recovery with three distinct runs.

Desk knowledge is not graded. If learners need facts that are not in the packet, the case is defective.

## What the harness changes

The harness forces explicit ledger input to the renderer, a digest-checked baseline restore before any edit, public fault placement on the work copy, and a read-only probe that uses the renderer's classify on current rows only. Source omissions correctly prevent render; the probe diagnoses them from the ledger. Three recovery proofs are distinct: required-field probe, complete render, and fresh-folder process from unrelated cwd. The 80-row pile with near misses, supersession, hostile notes, future records, and condition collisions is processed end to end.

PUT 9:15:
 ## Before class
 :
1. Using R/PY/M from setup, run the prepare for 04 into a throwaway W and confirm "$PY" "$W/scripts/render_review.py" "$W/shared/case/ledger.json" "$W/out/baseline.md" succeeds with both fields.
2. Confirm "$PY" "$W/scripts/restore.py" "$W" prints RESTORE OK on a throwaway copy.
3. Confirm the public "$PY" "$M/scripts/place_practice_fault.py" "$W" --variant A and the probe run from source paths with absolute M and W.
4. Keep graded cases outside the learner repository and model context.
5. Print or provide the public rubric.

## Before class

1. Run the prepare_work for 04 into a throwaway and confirm the next render command succeeds with both fields.
2. Confirm python scripts/restore.py <workdir> against a throwaway copy prints RESTORE OK.
3. Confirm the public place_practice_fault.py and probe_fields.py run from source paths.
4. Keep graded cases outside the learner repository and model context.
5. Print or provide the public rubric.

## Three-hour route

| Time | Facilitator action | Learner result |
|---|---|---|
| 0:00–0:20 | Introduce restore-first and the ledger | Learner prepares W and sees both fields |
| 0:20–0:40 | Learner runs the clean renderer and restore | RESTORE OK |
| 0:40–0:45 | Place the prepared work copy using public place script | Work copy drops one field |
| 0:45–1:20 | Learner seals the first miss with probe | Sealed record before replace |
| 1:20–1:50 | Learner runs one restore replace | Single RESTORE OK |
| 1:50–2:30 | Learner reruns three ways (incl. fresh-process) | Both fields present in each |
| 2:30–3:00 | Collect the handoff | Reconstruction without coaching, or HOLD |

## Coaching boundary

You may:

- define a term already stated in the packet;
- point to the current step or file;
- help open a file or run a supplied command;
- place the prepared work copy after restore is proved.

You may not supply:

- the name of the missing field;
- the reason it dropped;
- a hand-edited review.md; or
- the replace command wording.

If you cross that line, mark the work as guided practice. Use a new protected case for scoring. Select the examples yourself when you ask a learner to defend the sealed miss.

## HOLD conditions

Use HOLD when restore fails, the first miss is not sealed, more than one change is made, a decisive field is inaccessible, or the learner attempts consequential use.

A well-documented HOLD can complete practice. It does not pass the graded outcome.

## Collect

- clean render;
- restore output;
- sealed first miss + probe output;
- replace record;
- three reruns;
- handoff; and
- protected result or reason for HOLD.

Do not collect credentials, private local files, outside operational details, or model chat history unrelated to the case.
