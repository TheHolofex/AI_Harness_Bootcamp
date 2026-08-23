# Module 1 protected-case custody contract

This contract protects the assessment without hiding the performance standard.

## Staff roles

- **Case custodian:** stores graded packets, answer keys, allowed-delta manifests, and retirement records outside the learner repository.
- **Evaluator:** selects a case, records start/reveal/end order, receives raw work, and scores the public rubric.
- **Facilitator:** teaches the visible Cold Lantern case and may help operate supplied tools. The facilitator does not reveal graded source authority, arithmetic premises, rejection reasons, changed fields, or verdict.

## Required controls

1. Graded cases, source hashes, answers, and decisive checks stay outside the student repository and producing model context.
2. The learner sees the public rubric, work schema, time limit, and allowed tools.
3. Each case rotates exact identities, values, source order, distractor location, and sealed source change while preserving difficulty.
4. The evaluator releases the changed source only after baseline files, prediction, and verdict are preserved.
5. The source producer and AI system cannot enumerate, select, edit, bypass, or score the cases.
6. The evaluator preserves the first output and all source/check versions.
7. If a case or answer leaks, retire it for the cohort.
8. Reassessment uses a new case and retains both attempts.
9. At least one passing and four failing specimens test every checker revision.
10. At 200 learners, case and checker custody do not weaken; capacity shortfall creates `HOLD` or delayed assessment.

## Protected evidence record

```text
Learner pseudonymous ID:
Case ID and source-set version:
Public rubric version:
Start time:
Baseline hash time:
Change-release time:
Changed-result time:
Protected checker ID:
Material trace result:
Challenge result:
Allowed-delta result:
Review-surface result:
Evaluator-selected thread-walk pair and result:
Evaluator-selected claim row and defense result:
Human rationale score:
Coaching before completion: none / describe
Final result: PASS / HOLD
Case status: reusable / retired
```

## Compromise rules

- A learner-visible answer key invalidates the case.
- A model self-score is never the grade.
- A citation-presence check cannot replace semantic source review.
- A facilitator-supplied rejection rationale makes the attempt guided practice.
- A changed source opened before prediction invalidates that gate.
- A missing accessible equivalent holds the assessment.
