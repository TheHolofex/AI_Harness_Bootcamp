# Module 0 protected-acceptance custody contract

This file defines what the course implementation must protect. It contains no case, expected answer, or checker logic.

Module 0 is scored on the supplied case. Integrity does not come from the learner not knowing the case — the case, the request, the changed input, and the practice checker are all published to the learner in full. It comes from the deciding control living somewhere the learner and the learner's AI tools cannot reach, and being run by someone other than the producer.

## Roles

- **Control custodian:** holds the protected acceptance control, its expected material facts, and its version history outside the student repository and off every learner-reachable system.
- **Evaluator:** starts the attempt, receives the learner's work, runs the protected acceptance control on evaluator-held infrastructure, and scores the public rubric.
- **Facilitator:** teaches and supports practice. The facilitator does not run the protected control and does not describe its logic.
- **Learner:** receives the supplied case, the request, the changed input, the practice checker in full, an allowed workspace, the public rubric, and the time limit.

One person may hold more than one staff role only when the access log and the release control for the protected acceptance control remain intact.

## Required controls

1. The protected acceptance control is never committed to the student repository, embedded in a client-delivered application, or copied onto a learner machine.
2. The producing AI cannot list, read, edit, or invoke the control that will judge its output.
3. The learner sees the whole public rubric and the whole practice checker. The protected control's logic and its expected material facts stay off-machine.
4. Every scored result is produced by an evaluator run of the protected control. A learner-reported result is evidence of practice, never a score.
5. Each version of the protected control has a unique ID, version, release date, owner, and retirement status.
6. If the protected control's logic is disclosed in class or in support, it is revised and re-versioned before any further result is scored against it.
7. Raw learner output and the protected control's result are preserved before any coaching or correction.
8. A control update creates a new version. Prior scores retain the prior control ID.
9. Staff run one passing and at least three failing specimens through the protected control before release.
10. Reassessment reruns the same supplied case through the protected control. Both results are preserved, each with its control ID.
11. At 200 learners the control stays off-machine and evaluator-run. Scale does not justify shipping it to learners or delegating the run to them.

## Evidence record

```text
Learner pseudonymous ID:
Supplied case ID and version:
Rubric version:
Start and end timestamps:
First checked result: location and timestamp
Practice-check result reported by the learner (evidence, not a score):
Protected control ID and result:
Evaluator:
Coaching before completion: none / describe
Final result: PASS / HOLD
```

## Prohibited shortcuts

- placing the protected control, or anything it can be reconstructed from, on a learner machine;
- a model-generated self-score used as the grade;
- reusing the practice checker as the deciding control;
- accepting a screenshot in place of the underlying file;
- replacing independent operation with facilitator narration;
- changing the rubric after reading the learner's result;
- deleting failed first attempts.
