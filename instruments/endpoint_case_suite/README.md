# Endpoint comparison case suite

This directory holds the frozen D01–D05 cases and operator-only scoring conditions used by
P8's same-day Home/Open comparison. No P2 work depends on this suite.

## Tracks

- `engineering/`: software and platform operations
- `mission_ops/`: fictional mission and watch operations

Use the track recorded in the learner's P3 comparator. Both P8 endpoint runs use that same
track, the same course-repository project, and the exact same dispatch prompt.

## Boundary

Each case file contains an `Input` and a `Task`, and nothing else. The matching
`GRADER.md` contains one pass condition per case. Home and Open parents and their subagents
may read case files, but they may not read the grader.

The operator opens `GRADER.md` only after all ten raw endpoint outputs exist under
`../p8_hold_degrade/runs/<track>/`. The operator then scores both columns once against the
same conditions in `../p8_hold_degrade/SCORE_SHEET.md`.

## Integrity rules

- Do not edit D01–D05 between endpoints.
- Run one fresh read-only subagent per case.
- Keep no more than two subagent threads open and close completed threads before the next batch.
- Use the exact same parent dispatch for Home and Open.
- Do not expose a grader, coach a result, or retry a failed case.
- FAIL is valid endpoint evidence.
