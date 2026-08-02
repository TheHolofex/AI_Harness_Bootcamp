# P8 same-day Home/Open comparison — course instrument

**When:** Friday AM, inside P8
**Purpose:** Capture Home and Open on D01–D05 under matched run conditions, then make one
evidence-backed endpoint decision. Plan for about 35–45 minutes for both captures and scoring.

## What stays fixed

| Fixed for both endpoints | Value |
|---|---|
| Day | The same Friday session |
| Project | `Documents\HarnessBootcamp\AI_Harness_Bootcamp` |
| Track | The track chosen in P3: `engineering` or `mission_ops` |
| Cases | D01–D05, unchanged |
| Dispatch | Exact same prompt |
| Isolation | One fresh read-only subagent per case |
| Concurrency | No more than two open threads; close completed threads before the next batch |
| Scoring | Same hidden `GRADER.md`, opened only after all ten raw files exist |

The only intended change is the endpoint and displayed model.

## Student flow

1. Write and save the AUP before the first open-model request.
2. In a fresh Home parent chat on `gpt-5.6-terra`, select **Read only** and run the canonical dispatch from the P8 page.
3. After all five subagents finish, switch that same parent to **Ask for approval** and save the exact returned blocks under `runs/<track>/home/`. Do not rerun a case in the save turn.
4. Re-point to the posted Open endpoint and verify it with the allowed smoke request.
5. In a fresh Open parent chat, select **Read only** and paste the exact same dispatch.
6. In a separate **Ask for approval** turn, save those exact blocks under `runs/<track>/open/`.
7. Confirm D01–D05 exist under both endpoint folders. Only then open `GRADER.md` and score both columns once in `SCORE_SHEET.md`.
8. Compute Hold, Degrade, Improve, and Fail/fail. Give every non-hold an evidence-backed layer, next discriminating test, and owner.

## Raw evidence layout

```text
runs/<track>/
├── home/
│   ├── D01.md … D05.md
│   └── RUN_RECORD.md
└── open/
    ├── D01.md … D05.md
    └── RUN_RECORD.md
```

The execution turn cannot write because the parent is in **Read only**. The following save
turn may write only the exact returned answers and run record. This separates endpoint work
from evidence handling without creating ten manual case chats.

## Where the pass conditions live

Each case file contains only its input and task. The five pass conditions live in
`../endpoint_case_suite/<track>/GRADER.md`. Neither endpoint parent nor any subagent may read it.
The operator opens it only after the two raw sets exist, then applies the same condition to
the matching Home and Open files. A failed case is evidence; do not coach or retry it.

## Completion evidence

The paired run is complete when `SCORE_SHEET.md` names the P3 track, both run records, ten raw
paths, five Home scores, five Open scores, four comparison counts, and a root-cause row for
every non-hold.
