# P2 case suite — course instrument

**When:** Tuesday AM (Harness craft)  
**Purpose:** Measure harness craft before/after on a **fixed** 5-case suite.  
**Tracks:** `engineering/` or `mission_ops/` (chosen once).

## Student flow

1. Confirm track folder.
2. Run the suite **baseline** on the unchanged harness in fresh Codex chats, all using `gpt-5.6-terra`.
3. Record D01–D05 on `SCORE_SHEET.md` (PASS/FAIL + note).
4. Save the baseline column, then re-mark those same five rows against your track's `GRADER.md` and record how many of your five calls matched it.
5. Make harness changes (instructions/tests/memory/skills per block MVP).
6. Restart the app and run the suite **after** in fresh Codex chats, still using `gpt-5.6-terra`.
7. Record after scores; compute delta.
8. Deep mark on measurement spine: `Case suite: baseline n/5 → after n/5`.

To run authored checks by machine, save an answer to a file and use `python checks_runner.py CHECKS.md answer.txt` (script in this folder) — one `REQUIRE <pattern>` or `FORBID <pattern>` per line, PASS/FAIL printed for each.

## Where the pass conditions live

A case file holds an `Input` and a `Task`, and nothing else. The five pass conditions sit in
`engineering/GRADER.md` or `mission_ops/GRADER.md`, one per case. That file is yours to
read when you score. The model never sees it: it is not named in any prompt you paste, not
opened in a chat, and not quoted back into a case you are running. A system that can read
its own check is not being checked — shown the standard, a model writes to the standard,
and the score stops telling you anything about the harness.

## Rules

- Do not edit case files to make scores prettier.
- Do not paste `GRADER.md` into a chat or point an assistant at it, on either run.
- Use `gpt-5.6-terra` for every baseline, spot-check, and after chat. Do not use Default or Sol.
- FAIL is useful — especially if it turns PASS after craft.

## Timing

~15–20 min baseline · craft work · ~15–20 min after. Finishable in-block.
