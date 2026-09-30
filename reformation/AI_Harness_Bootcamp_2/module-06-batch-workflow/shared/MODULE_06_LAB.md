# Module 6 · Predict the effect of one saved-rule change and prove the exact delta

You can already derive a bounded check from fixed inputs. Now you will predict the exact effect of changing one line in a saved workflow, run it on two 80-lot waves, and prove which receipt rows moved while all others stayed byte-identical. Allow about two hours for inspection, prediction, runs, and notes; this is a planning target, not a measured completion time.

The fictional movement is Icehouse Depot to Clinic I-6. The files are authored practice data. Nothing here authorizes a real movement.

A **saved workflow** is the supplied `route.py` together with the `RULE.md` that sits beside it. A **receipt** is the CSV the workflow writes. Its columns are `lot`, `route`, and `status`. The router decides in this order: RACK_CONFLICT first, then exact permit match, then the single configuration line. Gate-window text and input disposition never change routing.

## Prepare a separate attempt

Use the verified Python and checkout from [setup](../../module-00-setup/README.md). Open an ordinary terminal. These commands work from any directory and leave earlier attempts intact. `W` is your work folder; `E` holds your records outside it.

**Terminal: Bash or zsh, ordinary user.**

```bash
R="$HOME/AI_Harness_Bootcamp"
PY="$(for candidate in python3.12 python3 python; do "$candidate" -c 'import sys; sys.exit(1) if sys.version_info < (3, 12) else print(sys.executable)' 2>/dev/null && break; done)"
M="$R/reformation/AI_Harness_Bootcamp_2/module-06-batch-workflow"
RUN="$(date -u +%Y%m%dT%H%M%SZ)-$$"
W="$HOME/course-evidence/module-06-$RUN/work"
E="$HOME/course-evidence/module-06-$RUN/evidence"
"$PY" "$R/reformation/shared/prepare_work.py" 06 "$W" &&
"$PY" -c "from pathlib import Path; import sys; Path(sys.argv[1]).mkdir(parents=True, exist_ok=False)" "$E"
```

**Terminal: PowerShell, ordinary user.**

```powershell
$R = "$HOME\AI_Harness_Bootcamp"
$PY = $(foreach ($candidate in 'python3.12','python3','python') { try { $resolved = & $candidate -c 'import sys; sys.exit(1) if sys.version_info < (3,12) else print(sys.executable)' 2>$null; if ($LASTEXITCODE -eq 0 -and $resolved) { $resolved.Trim(); break } } catch {} })
if (-not $PY) { throw 'No Python >= 3.12 found' }
$M = "$R\reformation\AI_Harness_Bootcamp_2\module-06-batch-workflow"
$RUN = [guid]::NewGuid().ToString('N')
$W = "$HOME\course-evidence\module-06-$RUN\work"
$E = "$HOME\course-evidence\module-06-$RUN\evidence"
& $PY "$R\reformation\shared\prepare_work.py" 06 "$W"
if ($LASTEXITCODE -ne 0) { throw 'Preparation stopped; preserve this attempt.' }
& $PY -c "from pathlib import Path; import sys; Path(sys.argv[1]).mkdir(parents=True, exist_ok=False)" "$E"
```

**Expected:** The preparer prints `PASS: created` followed by the absolute work path. `W` contains `shared/batch`, `shared/workflow`, `shared/baseline`, `scripts/restore_rule.py`, and an empty `out/` directory. `E` is a sibling evidence directory.

**Stop:** A command fails, a destination already exists, Python is not the verified 3.12-or-newer interpreter, or you already followed the preparer's suggested route command and created a receipt.

**Recovery:** Keep the existing attempt. Correct the prerequisite through setup, then repeat this block with a new `RUN`. Do not reset the checkout or delete an old work folder.

If you open a new terminal later, repeat only the variable assignments. Do not prepare a second folder unless this attempt has stopped.

The prepare script prints a suggested next command that runs the router on wave 1. Do not run it yet.

## Read the packet and write a prediction before any run

In your editor, open these files under `W`:

- `shared/batch/wave1.csv`
- `shared/batch/wave2.csv`
- `shared/batch/wave2-revised.csv`
- `shared/workflow/RULE.md`
- `shared/baseline/RULE.md`

The input columns are `lot`, `permit`, `gate_window`, `input_disposition`, `resource_exception`. `input_disposition` is provenance only. `CANCELLED` rows carry permit `WITHDRAWN`. The exception column is empty or exactly `RACK_CONFLICT`.

The saved rule contains one configuration line: `pending_status: OPEN`. The router applies rules in this order:

1. If `resource_exception` is `RACK_CONFLICT`, output `hold,RESOURCE_CONFLICT` before the permit is considered.
2. Otherwise, if permit is exactly `AUTHORIZED`, output `pass,READY`.
3. Otherwise, if permit is exactly `PENDING`, output `hold,OPEN` while the line says `OPEN`, or `reject,NOT_AUTHORIZED` when the line says `NOT_AUTHORIZED`.
4. Every other supplied permit value becomes `hold,OPEN`.

The permit match is case-sensitive. A lowercase or shortened lookalike is not `PENDING`. Text inside gate windows, including any received, released, or superseded wording, is not a routing input.

Create `E/prediction.md`. From the CSVs, list every lot whose `permit` or `resource_exception` you expect to affect routing under the current rule. Then predict exactly which lots will change if the only edit is the configuration line to `pending_status: NOT_AUTHORIZED`. For each such lot write the baseline receipt row and the changed receipt row. Name the rack claimants and state that they stay `hold,RESOURCE_CONFLICT`. State that every other serialized row remains byte-for-byte identical to its baseline. Do the same prediction for wave 2 using its own permit and exception columns. Save the note before you run the workflow on any input.

**Expected:** Your prediction file names the exact cells that drive each row you expect to move and states the byte-identity requirement for the rest.

**Stop:** A required file is missing, a header differs from the description, the baseline and active rule are not byte-identical three-line files, or you cannot point to the permit and exception cells behind each predicted row.

**Recovery:** Return to the fresh work folder and read the cells again. Do not fill the prediction from memory after a run, and do not edit a receipt to match a guess.

## Run both waves on the unchanged rule

A successful route prints nothing on stdout or stderr and exits 0. It creates the named receipt only when that path does not already exist. A held run prints a `HOLD:` message on standard error and exits 1. Wrong argument count prints `HOLD: usage` and exits 2. Keep any held output; a hold is an observation.

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" "$W/shared/workflow/route.py" "$W/shared/batch/wave1.csv" "$W/out/wave1-baseline.csv" &&
"$PY" "$W/shared/workflow/route.py" "$W/shared/batch/wave2.csv" "$W/out/wave2-baseline.csv" &&
"$PY" -c "
from pathlib import Path
import sys
left = Path(sys.argv[1]).read_bytes()
right = Path(sys.argv[2]).read_bytes()
same = left == right
print('BYTE MATCH' if same else 'HOLD: bytes differ')
sys.exit(0 if same else 1)
" "$W/out/wave1-baseline.csv" "$W/out/wave2-baseline.csv"
```

**Terminal: PowerShell, ordinary user.**

```powershell
& $PY "$W\shared\workflow\route.py" "$W\shared\batch\wave1.csv" "$W\out\wave1-baseline.csv"
if ($LASTEXITCODE -ne 0) { throw 'Wave 1 baseline held; preserve the attempt.' }
& $PY "$W\shared\workflow\route.py" "$W\shared\batch\wave2.csv" "$W\out\wave2-baseline.csv"
if ($LASTEXITCODE -ne 0) { throw 'Wave 2 baseline held; preserve the attempt.' }
@'
from pathlib import Path
import sys
left = Path(sys.argv[1]).read_bytes()
right = Path(sys.argv[2]).read_bytes()
same = left == right
print('BYTE MATCH' if same else 'HOLD: bytes differ')
sys.exit(0 if same else 1)
'@ | & $PY - "$W\out\wave1-baseline.csv" "$W\out\wave2-baseline.csv"
if ($LASTEXITCODE -ne 0) { throw 'Byte match check held; preserve the receipts.' }
```

**Expected:** Both route commands exit 0 with no output. Each receipt contains a header row and 80 data rows. The comparison prints `BYTE MATCH`. Open the receipts and confirm their rows match the baseline half of your prediction.

**Stop:** Either route exits non-zero, a receipt is missing or contains fewer than 80 data rows, the comparison does not print `BYTE MATCH`, or any receipt row disagrees with the permit and exception cells you inspected.

**Recovery:** Preserve both receipts and the error text. Correct the path or the prediction in a new prepared folder. Do not delete, overwrite, or hand-edit a receipt.

## Change exactly one line in the rule

In your editor, edit only `W/shared/workflow/RULE.md`. Change the configuration line to `pending_status: NOT_AUTHORIZED`. Leave the two comment lines untouched. Do not edit `shared/baseline/RULE.md`, either wave file, or any receipt. Do not add a second `pending_status` line.

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" -c "
from pathlib import Path
import sys
w = Path(sys.argv[1])
base_lines = (w / 'shared/baseline/RULE.md').read_text(encoding='utf-8').splitlines()
active_lines = (w / 'shared/workflow/RULE.md').read_text(encoding='utf-8').splitlines()
diff = [(i+1, a, b) for i, (a, b) in enumerate(zip(base_lines, active_lines)) if a != b]
ok = len(base_lines) == len(active_lines) and diff == [(3, 'pending_status: OPEN', 'pending_status: NOT_AUTHORIZED')]
print('ONE LINE CHANGE' if ok else 'HOLD: rule edit is not the single pending_status line')
sys.exit(0 if ok else 1)
" "$W"
```

**Terminal: PowerShell, ordinary user.**

```powershell
@'
from pathlib import Path
import sys
w = Path(sys.argv[1])
base_lines = (w / 'shared/baseline/RULE.md').read_text(encoding='utf-8').splitlines()
active_lines = (w / 'shared/workflow/RULE.md').read_text(encoding='utf-8').splitlines()
diff = [(i+1, a, b) for i, (a, b) in enumerate(zip(base_lines, active_lines)) if a != b]
ok = len(base_lines) == len(active_lines) and diff == [(3, 'pending_status: OPEN', 'pending_status: NOT_AUTHORIZED')]
print('ONE LINE CHANGE' if ok else 'HOLD: rule edit is not the single pending_status line')
sys.exit(0 if ok else 1)
'@ | & $PY - "$W"
if ($LASTEXITCODE -ne 0) { throw 'Rule line check held; preserve the attempt.' }
```

**Expected:** The check prints `ONE LINE CHANGE`. The baseline file remains the original three-line rule.

**Stop:** The check prints a `HOLD` message, or the baseline file changed.

**Recovery:** Correct only the active rule in the editor until the check passes. If the baseline changed, stop this attempt and prepare a new folder. Do not copy a receipt backward into the rule.

## Prove the full serialized delta for both waves

Run the workflow again to new receipt names. Then compare every serialized row against its baseline receipt.

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" "$W/shared/workflow/route.py" "$W/shared/batch/wave1.csv" "$W/out/wave1-changed.csv" &&
"$PY" "$W/shared/workflow/route.py" "$W/shared/batch/wave2.csv" "$W/out/wave2-changed.csv" &&
"$PY" -c "
from pathlib import Path
import sys
def get_lines(p): return p.read_bytes().splitlines(keepends=True)
pairs = [(sys.argv[1], sys.argv[2]), (sys.argv[3], sys.argv[4])]
for left, right in pairs:
    bl = get_lines(Path(left))
    cl = get_lines(Path(right))
    if len(bl) != len(cl) or bl[0] != cl[0]:
        print('HOLD: receipt shape')
        sys.exit(1)
    diffs = [i for i in range(1, len(bl)) if bl[i] != cl[i]]
    print(Path(left).name, 'CHANGED', len(diffs))
    print('UNCHANGED', len(bl) - 1 - len(diffs))
    for i in diffs:
        print(bl[i].decode('utf-8', errors='replace').rstrip(), '->', cl[i].decode('utf-8', errors='replace').rstrip())
    if len(diffs) != 3:
        print('HOLD: unexpected delta')
        sys.exit(1)
    print('SERIALIZED BYTE DELTA OK')
" "$W/out/wave1-baseline.csv" "$W/out/wave1-changed.csv" "$W/out/wave2-baseline.csv" "$W/out/wave2-changed.csv"
```

**Terminal: PowerShell, ordinary user.**

```powershell
& $PY "$W\shared\workflow\route.py" "$W\shared\batch\wave1.csv" "$W\out\wave1-changed.csv"
if ($LASTEXITCODE -ne 0) { throw 'Changed wave 1 held; preserve the attempt.' }
& $PY "$W\shared\workflow\route.py" "$W\shared\batch\wave2.csv" "$W\out\wave2-changed.csv"
if ($LASTEXITCODE -ne 0) { throw 'Changed wave 2 held; preserve the attempt.' }
@'
from pathlib import Path
import sys
def get_lines(p): return p.read_bytes().splitlines(keepends=True)
pairs = [(sys.argv[1], sys.argv[2]), (sys.argv[3], sys.argv[4])]
for left, right in pairs:
    bl = get_lines(Path(left))
    cl = get_lines(Path(right))
    if len(bl) != len(cl) or bl[0] != cl[0]:
        print('HOLD: receipt shape')
        sys.exit(1)
    diffs = [i for i in range(1, len(bl)) if bl[i] != cl[i]]
    print(Path(left).name, 'CHANGED', len(diffs))
    print('UNCHANGED', len(bl) - 1 - len(diffs))
    for i in diffs:
        print(bl[i].decode('utf-8', errors='replace').rstrip(), '->', cl[i].decode('utf-8', errors='replace').rstrip())
    if len(diffs) != 3:
        print('HOLD: unexpected delta')
        sys.exit(1)
    print('SERIALIZED BYTE DELTA OK')
'@ | & $PY - "$W\out\wave1-baseline.csv" "$W\out\wave1-changed.csv" "$W\out\wave2-baseline.csv" "$W\out\wave2-changed.csv"
if ($LASTEXITCODE -ne 0) { throw 'Serialized delta check held; preserve the receipts.' }
```

**Expected:** Both route commands exit 0. For each wave the comparison prints one `CHANGED` count and one `UNCHANGED` count that add to 80. The printed moves are exactly the lots you predicted under the changed rule; each moves from `hold,OPEN` to `reject,NOT_AUTHORIZED`. No rack row appears in the changed list. No other row is printed.

**Stop:** A route holds, a changed lot was not in your prediction, a predicted lot is missing from the list, a rack row moves, or any other serialized row differs. Record `HOLD: unexpected delta` together with the printed lines.

**Recovery:** Preserve all four receipts and the comparison text. Do not patch a receipt or add a routing rule. If the one-line check did not pass, correct only that line and repeat the section in a new prepared folder so the old receipts remain as evidence.

## Restore the baseline rule and prove the full reruns

The baseline rule lives in `shared/baseline/RULE.md` with matching digest. Use the supplied restore that takes the workdir.

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" "$W/scripts/restore_rule.py" "$W" &&
"$PY" -c "
from pathlib import Path
import sys
w = Path(sys.argv[1])
same = (w / 'shared/workflow/RULE.md').read_bytes() == (w / 'shared/baseline/RULE.md').read_bytes()
print('RULE BYTES MATCH' if same else 'HOLD: rule bytes differ')
sys.exit(0 if same else 1)
" "$W" &&
"$PY" "$W/shared/workflow/route.py" "$W/shared/batch/wave1.csv" "$W/out/wave1-restored.csv" &&
"$PY" "$W/shared/workflow/route.py" "$W/shared/batch/wave2.csv" "$W/out/wave2-restored.csv" &&
"$PY" -c "
from pathlib import Path
import sys
pairs = [(sys.argv[1], sys.argv[2]), (sys.argv[3], sys.argv[4])]
ok = all(Path(a).read_bytes() == Path(b).read_bytes() for a,b in pairs)
print('RESTORED WAVES MATCH' if ok else 'HOLD: restored waves differ')
sys.exit(0 if ok else 1)
" "$W/out/wave1-baseline.csv" "$W/out/wave1-restored.csv" "$W/out/wave2-baseline.csv" "$W/out/wave2-restored.csv"
```

**Terminal: PowerShell, ordinary user.**

```powershell
& $PY "$W\scripts\restore_rule.py" "$W"
if ($LASTEXITCODE -ne 0) { throw 'Restore held; preserve the attempt.' }
@'
from pathlib import Path
import sys
w = Path(sys.argv[1])
same = (w / 'shared/workflow/RULE.md').read_bytes() == (w / 'shared/baseline/RULE.md').read_bytes()
print('RULE BYTES MATCH' if same else 'HOLD: rule bytes differ')
sys.exit(0 if same else 1)
'@ | & $PY - "$W"
if ($LASTEXITCODE -ne 0) { throw 'Restored rule bytes differ.' }
& $PY "$W\shared\workflow\route.py" "$W\shared\batch\wave1.csv" "$W\out\wave1-restored.csv"
if ($LASTEXITCODE -ne 0) { throw 'Restored wave 1 held.' }
& $PY "$W\shared\workflow\route.py" "$W\shared\batch\wave2.csv" "$W\out\wave2-restored.csv"
if ($LASTEXITCODE -ne 0) { throw 'Restored wave 2 held.' }
@'
from pathlib import Path
import sys
pairs = [(sys.argv[1], sys.argv[2]), (sys.argv[3], sys.argv[4])]
ok = all(Path(a).read_bytes() == Path(b).read_bytes() for a,b in pairs)
print('RESTORED WAVES MATCH' if ok else 'HOLD: restored waves differ')
sys.exit(0 if ok else 1)
'@ | & $PY - "$W\out\wave1-baseline.csv" "$W\out\wave1-restored.csv" "$W\out\wave2-baseline.csv" "$W\out\wave2-restored.csv"
if ($LASTEXITCODE -ne 0) { throw 'Restored waves check held; preserve the receipts.' }
```

**Expected:** `RESTORE OK` on stdout. The rule bytes check prints `RULE BYTES MATCH`. The restored receipts are byte-identical to the original baseline receipts.

**Stop:** Restore exits non-zero, rule bytes differ, a route holds, or the restored receipts differ from baselines. Record `HOLD: restore failed`.

**Recovery:** Preserve the error and receipts. Do not hand-copy a rule over a mismatched baseline digest. Record the damaged file, then use a newly prepared folder if the frozen baseline is no longer intact.

Append the comparison output to `E/prediction.md` without replacing the original prediction. Write `W/handoff.md` with the work path, rule before and after, receipt paths, complete row comparison, and restore evidence. State that input disposition was never used as a route.

<details markdown="1">
<summary>Optional stretch: separate an input revision from the policy change</summary>

The stretch file keeps the same saved workflow and rule format. It changes which rows meet the existing exact-`PENDING` predicate and also changes some non-routing text.

Before any stretch command, add a new prediction section to `E/prediction.md`. Compare `wave2.csv` with `wave2-revised.csv`. List every lot whose `permit` or `resource_exception` changes, and predict its receipt under the restored `OPEN` line and the proposed `NOT_AUTHORIZED` line. Separate input-revision effects from policy effects. Predict which full receipt rows remain identical, including both rack claimants. Save this prediction before running either condition.

**Stop:** You cannot point to the two input cells for each predicted difference, or a revised receipt already exists.

**Recovery:** Return to the two CSVs and finish the list. Choose new output names if a previous stretch file exists; do not delete it.

Re-apply the exact one-line change and verify it, then run the revised input under the changed rule.

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" -c "
from pathlib import Path
import sys
w = Path(sys.argv[1])
base_lines = (w / 'shared/baseline/RULE.md').read_text(encoding='utf-8').splitlines()
active_lines = (w / 'shared/workflow/RULE.md').read_text(encoding='utf-8').splitlines()
diff = [(i+1, a, b) for i, (a, b) in enumerate(zip(base_lines, active_lines)) if a != b]
ok = len(base_lines) == len(active_lines) and diff == [(3, 'pending_status: OPEN', 'pending_status: NOT_AUTHORIZED')]
print('ONE LINE CHANGE' if ok else 'HOLD: rule edit is not the single pending_status line')
sys.exit(0 if ok else 1)
" "$W"
```

**Terminal: PowerShell, ordinary user.**

```powershell
@'
from pathlib import Path
import sys
w = Path(sys.argv[1])
base_lines = (w / 'shared/baseline/RULE.md').read_text(encoding='utf-8').splitlines()
active_lines = (w / 'shared/workflow/RULE.md').read_text(encoding='utf-8').splitlines()
diff = [(i+1, a, b) for i, (a, b) in enumerate(zip(base_lines, active_lines)) if a != b]
ok = len(base_lines) == len(active_lines) and diff == [(3, 'pending_status: OPEN', 'pending_status: NOT_AUTHORIZED')]
print('ONE LINE CHANGE' if ok else 'HOLD: rule edit is not the single pending_status line')
sys.exit(0 if ok else 1)
'@ | & $PY - "$W"
if ($LASTEXITCODE -ne 0) { throw 'Rule line check held; preserve the attempt.' }
```

**Expected:** The check prints `ONE LINE CHANGE`. The rule is now `NOT_AUTHORIZED`.

**Stop:** The check prints HOLD or the baseline changed.

**Recovery:** Correct only the active rule.

Run the revised input under the changed rule.

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" "$W/shared/workflow/route.py" "$W/shared/batch/wave2-revised.csv" "$W/out/wave2-revised-changed.csv" &&
"$PY" -c "
import csv, sys
from pathlib import Path
a = list(csv.reader(Path(sys.argv[1]).open(newline='')))
b = list(csv.reader(Path(sys.argv[2]).open(newline='')))
if a[0] != ['lot','route','status'] or b[0] != a[0] or len(a) != len(b):
    print('HOLD: receipt shape')
    sys.exit(1)
changed = [(x, y) for x, y in zip(a[1:], b[1:]) if x != y]
print('CHANGED', len(changed))
for x, y in changed:
    print(','.join(x), '->', ','.join(y))
print('UNCHANGED', len(a) - 1 - len(changed))
" "$W/out/wave2-changed.csv" "$W/out/wave2-revised-changed.csv"
```

**Terminal: PowerShell, ordinary user.**

```powershell
& $PY "$W\shared\workflow\route.py" "$W\shared\batch\wave2-revised.csv" "$W\out\wave2-revised-changed.csv"
if ($LASTEXITCODE -ne 0) { throw 'Revised changed run held; preserve the attempt.' }
@'
import csv, sys
from pathlib import Path
a = list(csv.reader(Path(sys.argv[1]).open(newline='')))
b = list(csv.reader(Path(sys.argv[2]).open(newline='')))
if a[0] != ['lot','route','status'] or b[0] != a[0] or len(a) != len(b):
    print('HOLD: receipt shape')
    sys.exit(1)
changed = [(x, y) for x, y in zip(a[1:], b[1:]) if x != y]
print('CHANGED', len(changed))
for x, y in changed:
    print(','.join(x), '->', ','.join(y))
print('UNCHANGED', len(a) - 1 - len(changed))
'@ | & $PY - "$W\out\wave2-changed.csv" "$W\out\wave2-revised-changed.csv"
if ($LASTEXITCODE -ne 0) { throw 'Revised csv check held; preserve the attempt.' }
```

**Expected:** The route exits 0. The changed rows are exactly the input-membership rows you predicted for the `NOT_AUTHORIZED` rule. Lots whose routing fields did not change are absent from the list. Both rack claimants remain `hold,RESOURCE_CONFLICT`.

**Stop:** The route holds, a printed move was not in the pre-run list, a predicted move is missing, or a rack row changes. Record `HOLD: unexpected revised delta`.

**Recovery:** Keep the original prediction, the revised receipt, and the comparison. Add an explanation of the mismatch rather than rewriting the prediction after seeing the result. Inspect the input cells and control identity before deciding whether a fresh attempt is justified.

Restore the frozen rule, run the revised input to a separate baseline-condition receipt, and distinguish the input delta from the policy delta. The comparison below prints every differing serialized row and counts the byte-identical remainder.

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" "$W/scripts/restore_rule.py" "$W" &&
"$PY" "$W/shared/workflow/route.py" "$W/shared/batch/wave2-revised.csv" "$W/out/wave2-revised-baseline.csv" &&
"$PY" - "$W" <<'PY'
from pathlib import Path
import sys
w = Path(sys.argv[1])
if (w/'shared/workflow/RULE.md').read_bytes() != (w/'shared/baseline/RULE.md').read_bytes():
    raise SystemExit('HOLD: restored rule bytes differ')
print('RULE BYTES MATCH')
for label, before, after in (
    ('INPUT DELTA', 'wave2-baseline.csv', 'wave2-revised-baseline.csv'),
    ('POLICY DELTA', 'wave2-revised-baseline.csv', 'wave2-revised-changed.csv'),
):
    left = (w/'out'/before).read_bytes().splitlines(keepends=True)
    right = (w/'out'/after).read_bytes().splitlines(keepends=True)
    if not left or len(left) != len(right) or left[0] != right[0]:
        raise SystemExit('HOLD: receipt shape differs')
    changed = [(a,b) for a,b in zip(left[1:],right[1:]) if a != b]
    print(label, 'CHANGED', len(changed), 'UNCHANGED', len(left)-1-len(changed))
    for a,b in changed:
        print(a.decode().rstrip(), '->', b.decode().rstrip())
PY
```

**Terminal: PowerShell, ordinary user.**

```powershell
& $PY "$W\scripts\restore_rule.py" "$W"
if ($LASTEXITCODE -ne 0) { throw 'Restore held; preserve the attempt.' }
& $PY "$W\shared\workflow\route.py" "$W\shared\batch\wave2-revised.csv" "$W\out\wave2-revised-baseline.csv"
if ($LASTEXITCODE -ne 0) { throw 'Revised baseline run held.' }
@'
from pathlib import Path
import sys
w = Path(sys.argv[1])
if (w/'shared/workflow/RULE.md').read_bytes() != (w/'shared/baseline/RULE.md').read_bytes():
    raise SystemExit('HOLD: restored rule bytes differ')
print('RULE BYTES MATCH')
for label, before, after in (
    ('INPUT DELTA', 'wave2-baseline.csv', 'wave2-revised-baseline.csv'),
    ('POLICY DELTA', 'wave2-revised-baseline.csv', 'wave2-revised-changed.csv'),
):
    left = (w/'out'/before).read_bytes().splitlines(keepends=True)
    right = (w/'out'/after).read_bytes().splitlines(keepends=True)
    if not left or len(left) != len(right) or left[0] != right[0]:
        raise SystemExit('HOLD: receipt shape differs')
    changed = [(a,b) for a,b in zip(left[1:],right[1:]) if a != b]
    print(label, 'CHANGED', len(changed), 'UNCHANGED', len(left)-1-len(changed))
    for a,b in changed:
        print(a.decode().rstrip(), '->', b.decode().rstrip())
'@ | & $PY - "$W"
```

**Expected:** Restore prints `RESTORE OK`; the comparison prints `RULE BYTES MATCH`. `INPUT DELTA` accounts for input-revision effects with the policy fixed. `POLICY DELTA` accounts for the one-line policy change with the revised input fixed. Match every printed row and every unchanged row against the saved prediction. Rack conflicts retain precedence in both conditions.

**Stop:** Restore holds, rule bytes differ, a receipt already exists, a row moves for an unexplained reason, or an unchanged row is not byte-identical.

**Recovery:** Preserve all conditions and the first error. Do not patch a receipt or weaken the restore check. If a new attempt is needed, begin with a fresh folder and a new prediction that explicitly acknowledges the earlier result.

Append the observed deltas to your evidence and update the handoff. Explain one input-only change, one policy-only change, and the condition that keeps a rack claimant on hold. A matching practice receipt is not clinic movement authority.

</details>

## Before you stop

Confirm that both original waves used the same work-copy `route.py`, only the intended configuration line changed, and complete receipt comparisons support the predicted delta. The restored runs must match their respective original baselines byte for byte. Keep every attempt; do not hand-patch a receipt.

If you completed the optional stretch, retain its two revised-input conditions and the separate input/policy comparison. Leave an unrun stretch unclaimed rather than treating the core comparison as its proof.

Continue with [paired evaluation](../../module-07-change-eval/README.md).