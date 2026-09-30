# Module 2 protected-case custody contract

This contract protects the assessment without hiding the performance standard.

The screen is public and inspectable. Learners may read `shared/case/guard.py`. Graded screens and notes remain outside the learner repository.

## Staff roles

- **Case custodian:** stores graded notes, graded screen copies, answer keys, and retirement records outside the learner repository.
- **Evaluator:** selects a case, records start/reload/end order, receives raw work, and scores the public rubric.
- **Facilitator:** teaches the visible Ledger Pike case and may help operate supplied commands. The facilitator does not reveal graded screen patterns, rejection reasons, or the remaining-bypass answer key.

## Required controls

1. Graded notes, screen hashes, answers, and decisive checks stay outside the student repository and producing model context.
2. The learner sees the public rubric, work schema, time limit, and allowed tools.
3. Each case rotates exact identifiers, quoted override wording, and distractor location while preserving difficulty.
4. The evaluator confirms the graded screen, not the learner-visible copy, produced the scored result.
5. The source producer and AI system cannot enumerate, select, edit, bypass, or score the cases.
6. The evaluator preserves the first output and all note/screen versions.
7. If a case or answer leaks, retire it for the cohort.
8. Reassessment uses a new case and retains both attempts.
9. At least one passing and four failing specimens test every checker revision.
10. At 200 learners, case and checker custody do not weaken; capacity shortfall creates `HOLD` or delayed assessment.

## Protected evidence record

```text
Learner pseudonymous ID:
Case ID and note-set version:
Public rubric version:
Start time:
Prediction hash time:
Screen-run time:
Load receipt time:
Second-session time:
Negative-load time:
Graded screen ID:
Clean note result:
Hostile note result:
Load receipt hashes match:
Second session identity match:
Negative stopped before contact:
Bypass statement present:
Human rationale score:
Coaching before completion: none / describe
Final result: PASS / HOLD
Case status: reusable / retired
```

## Compromise rules

- A learner-visible answer key invalidates the case.
- A model self-score is never the grade.
- A producer-edited screen cannot score the attempt.
- A facilitator-supplied rejection rationale makes the attempt guided practice.
- A screen run opened before prediction invalidates that gate.
- A missing accessible equivalent holds the assessment.
- A load receipt that does not match the frozen rule or appears after a provider request holds the load gate.
