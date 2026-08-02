# P8 same-day Home/Open score sheet

- **Track chosen in P3:** engineering / mission_ops
- **Student:** ________
- **Run date:** ________
- **Course-repository project:** `Documents\HarnessBootcamp\AI_Harness_Bootcamp`
- **Home model:** `gpt-5.6-terra`
- **Open/re-pointed model:** ________
- **Policy/AUP version:** ________

## Run identity

- Home run record: `instruments/p8_hold_degrade/runs/[TRACK]/home/RUN_RECORD.md`
- Open run record: `instruments/p8_hold_degrade/runs/[TRACK]/open/RUN_RECORD.md`
- Both endpoint parents executed in **Read only**: Y / N
- The Home and Open dispatch text was exact: Y / N
- Each endpoint used one fresh subagent per D01–D05 case: Y / N
- Maximum open subagent threads was two, with completed threads closed before the next batch: Y / N
- All ten raw files existed before `GRADER.md` was opened: Y / N

Replace `[TRACK]` with the track recorded in P3. A `N` makes the paired comparison invalid
until the exact problem is resolved and recorded.

## Paired results

| ID | Home raw output | Home P/F | Home scoring evidence | Open raw output | Open P/F | Open scoring evidence | Comparison |
|---|---|---|---|---|---|---|---|
| D01 | `runs/[TRACK]/home/D01.md` | | | `runs/[TRACK]/open/D01.md` | | | |
| D02 | `runs/[TRACK]/home/D02.md` | | | `runs/[TRACK]/open/D02.md` | | | |
| D03 | `runs/[TRACK]/home/D03.md` | | | `runs/[TRACK]/open/D03.md` | | | |
| D04 | `runs/[TRACK]/home/D04.md` | | | `runs/[TRACK]/open/D04.md` | | | |
| D05 | `runs/[TRACK]/home/D05.md` | | | `runs/[TRACK]/open/D05.md` | | | |
| **Total PASS** | | **__/5** | | | **__/5** | | |

**Scoring rule:** keep `GRADER.md` closed until both five-file raw sets exist. Then score
Home and Open once against the same matching track condition. The models never see the
grader, do not score themselves, and do not receive a coached retry.

Write `Hold` for P/P, `Degrade` for P/F, `Improve` for F/P, or `Fail/fail` for F/F.

- **Hold count:** ____
- **Degrade count:** ____
- **Improve count:** ____
- **Fail/fail count:** ____

## Root-cause register

Add one row for every result that is not a hold.

| Case | Layer | Evidence | Next discriminating test | Owner |
|---|---|---|---|---|
| | model / instructions / tests / environment / brief | | | |

## Endpoint decision evidence

- **Legitimate refuse under policy:** ________

- **Loop still closes on core path?** Y / N — path: ________

- **90-second defense notes:** ________
