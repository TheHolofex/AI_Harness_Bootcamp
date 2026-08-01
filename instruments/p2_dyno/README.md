# P2 Dyno — course instrument

**When:** Tuesday AM (Hot-rod)  
**Purpose:** Measure harness craft before/after on a **fixed** 5-case suite.  
**Tracks:** `engineering/` or `mission_ops/` (chosen once).

## Student flow

1. Confirm track folder.
2. Run suite **baseline** on stock harness (new chat/session recommended).
3. Record D01–D05 on `SCORE_SHEET.md` (PASS/FAIL + note).
4. Make harness changes (instructions/tests/memory/skills per block MVP).
5. Run suite **after** cold (new chat if possible).
6. Record after scores; compute delta.
7. Deep mark on measurement spine: `Dyno: baseline n/5 → after n/5`.

To run authored checks by machine, save an answer to a file and use `python checks_runner.py CHECKS.md answer.txt` (script in this folder) — one `REQUIRE <pattern>` or `FORBID <pattern>` per line, PASS/FAIL printed for each.

## Rules

- Do not edit case files to make scores prettier.
- Same model tier for baseline and after unless told otherwise.
- FAIL is useful — especially if it turns PASS after craft.

## Timing

~15–20 min baseline · craft work · ~15–20 min after. Finishable in-block.
