# Module 4 protected-case custody contract

This contract protects the assessment without hiding the performance standard.

The hidden field drop lives only in a placed work-copy renderer after restore is proved. Learners may read scripts/render_review.py, scripts/place_practice_fault.py, and scripts/probe_fields.py. Those files are the clean and public practice copies. The producer cannot edit the deciding protected cases.

## Staff roles

- **Case custodian:** stores graded ledgers, answer keys, and retirement records outside the learner repository.
- **Evaluator:** selects a case, records restore/seal/replace order, receives raw work, and scores the public rubric.
- **Facilitator:** teaches the visible ledger and places the prepared work copy using the public place script after restore is proved. The facilitator does not reveal the dropped field or the replace command.

## Required controls

1. Graded ledgers, answer keys, and decisive checks stay outside the student repository and producing model context.
2. The learner sees the public rubric, work schema, time limit, and allowed tools.
3. Each case rotates which field drops while preserving difficulty.
4. Restore is verified before the work copy is placed.
5. The source producer and AI system cannot enumerate, select, edit, bypass, or score the cases.
6. The evaluator preserves the first sealed miss and all renderer versions.
7. If a case or answer leaks, retire it for the cohort.
8. Reassessment uses a new case and retains both attempts.
9. At least one passing and four failing specimens test every checker revision.
10. At 200 learners, case and checker custody do not weaken; capacity shortfall creates HOLD or delayed assessment.

## Protected evidence record

```text
Learner pseudonymous ID:
Case ID and ledger version:
Public rubric version:
Start time:
Restore-OK time:
Seal time:
Replace time:
Protected ledger ID:
First missing field:
Still-present field:
Replace command:
Focused result:
End-to-end result:
Fresh-process result:
Human rationale score:
Coaching before completion: none / describe
Final result: PASS / HOLD
Case status: reusable / retired
```

## Compromise rules

- A learner-visible answer key invalidates the case.
- A model self-score is never the grade.
- A producer-edited renderer cannot score the attempt.
- A facilitator-supplied first-miss name makes the attempt guided practice.
- A replace before seal invalidates that gate.
- A missing accessible equivalent holds the assessment.
