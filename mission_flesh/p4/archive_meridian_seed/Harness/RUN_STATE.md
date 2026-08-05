# Run State

This file carries the run across a fresh context. Update it after each material stage.

- Run ID: [REPLACE: stable identifier for this run]
- Goal: [REPLACE: the current bounded goal]
- Phase: [REPLACE: BUILDING, AWAITING_HUMAN_AUDIT, RESUMED, AWAITING_CANDIDATE_CHECK, EVALUATING, or TERMINAL]
- Status: [REPLACE: COMPLETE or HAND_BACK]
- Completed: [REPLACE: semicolon-separated completed stages with artifact pointers]
- Open: [REPLACE: unresolved work or NONE]
- Next permitted action: [REPLACE: one bounded next action, or NONE with the reason]
- Terminal reason: [REPLACE: SUCCESS, NEEDS_EVIDENCE, BUDGET_STOP, ERROR_CEILING, NO_PROGRESS, or HUMAN_HAND_BACK]
- Artifact pointers: [REPLACE: include Answers/Q1 Risks.md; Answers/Q2 Blocked Decision.md; Audit.md; Morning_Brief.md; Harness/EVAL.md]

During the run, `Status` may describe the active phase. At release, `SUCCESS` pairs with `COMPLETE`; every other terminal reason pairs with `HAND_BACK`.
