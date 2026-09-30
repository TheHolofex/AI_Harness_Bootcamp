# Module 3 protected-case custody contract

This contract protects the assessment without hiding the performance standard.

Learners may read `shared/tools/hash_source.py`. The deciding check is a protected copy the producer cannot edit.

## Staff roles

- **Case custodian:** stores graded notes, the protected hash tool, answer keys, and retirement records outside the learner repository.
- **Evaluator:** selects a case, records decision/hash/revoke order, receives raw work, and scores the public rubric.
- **Facilitator:** teaches the visible yard-window case and may help operate supplied commands. The facilitator does not reveal graded hashes, the supported position, or the six-concern answer key.

## Required controls

1. Graded notes, tool hashes, answers, and decisive checks stay outside the student repository and producing model context.
2. The learner sees the public rubric, work schema, time limit, and allowed tools.
3. Each case rotates exact hours, address wording, and override text while preserving difficulty.
4. Both branches are scored. A supported `no-release` does not replace the connection branch.
5. The source producer and AI system cannot enumerate, select, edit, bypass, or score the cases.
6. The evaluator preserves the first output and all note/tool versions.
7. If a case or answer leaks, retire it for the cohort.
8. Reassessment uses a new case and retains both attempts.
9. At least one passing and four failing specimens test every checker revision.
10. At 200 learners, case and checker custody do not weaken; capacity shortfall creates `HOLD` or delayed assessment.

## Protected evidence record

```text
Learner pseudonymous ID:
Case ID and note version:
Public rubric version:
Start time:
Decision hash time:
Hash-run time:
Revoke time:
Protected tool ID:
Position:
Six-concern completeness:
Hash match:
Path-escape result:
Composed-negative result:
Revoke result:
Human rationale score:
Coaching before completion: none / describe
Final result: PASS / HOLD
Case status: reusable / retired
```

## Compromise rules

- A learner-visible answer key invalidates the case.
- A model self-score is never the grade.
- A producer-edited tool cannot score the attempt.
- A facilitator-supplied `no-release` rationale makes the attempt guided practice.
- A hash run used as a substitute for the decision branch invalidates that gate.
- A missing accessible equivalent holds the assessment.
