# Module 7 protected-case custody contract

The deciding hard-gate copy is protected. Learners may read `shared/controls/hard_gates.py`. That file is not the graded copy.

## Staff roles

- **Case custodian:** stores graded pairs outside the learner repository.
- **Evaluator:** selects pairs, records policy/result/restore order, and scores the public rubric.
- **Facilitator:** teaches the visible pairs. The facilitator does not reveal graded defects.

## Required controls

1. Graded pairs stay outside the student repository and producing model context.
2. The learner sees the public rubric and the visible gates.
3. Each case rotates which pair carries which defect.
4. The producer cannot edit the deciding gate.
5. Reassessment uses new pairs and retains both attempts.

## Compromise rules

- A policy change after results invalidates the attempt.
- Averaging two pairs into a quality score fails the gate.
- A missing accessible equivalent holds the assessment.
