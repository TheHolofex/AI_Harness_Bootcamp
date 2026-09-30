# Module 9 · Transfer a package someone else can operate

A runnable package lets its recipient recover the purpose, inputs, controls, result, stop condition, and restore action without the author's chat history. You will freeze a package, move only its declared files to a fresh location, and operate it from a new terminal. Then an eligible independent recipient can be assessed on a private task.

The Last Count case is fictional: South Store, Clinic R-12, movement W-9, and oral rehydration salts. A quantity-support result is not permission to release or dispatch anything. Allow about three hours for preparation, source inspection, operation, and handoff; this is a planning target, not a measured completion time.

## Prepare separate work and transfer locations

Use the verified checkout and Python from [setup](../../module-00-setup/README.md). `W` is the authoring work copy, `E` is the separate evidence directory, and `F` is the future received package. The commands work from any directory. Do not create `F` until the transfer step.

**Terminal: Bash or zsh, ordinary user.**

```bash
R="$HOME/AI_Harness_Bootcamp"
PY="$(for candidate in python3.12 python3 python; do "$candidate" -c 'import sys; sys.exit(1) if sys.version_info < (3, 12) else print(sys.executable)' 2>/dev/null && break; done)"
M="$R/reformation/AI_Harness_Bootcamp_2/module-09-capstone"
RUN="$(date -u +%Y%m%dT%H%M%SZ)-$$"
BASE="$HOME/course-evidence/module-09-$RUN"
W="$BASE/work"
E="$BASE/evidence"
F="$BASE/received package"
"$PY" "$R/reformation/shared/prepare_work.py" 09 "$W" &&
"$PY" -c "from pathlib import Path; import sys; e,f=map(Path,sys.argv[1:]); (f.exists() or f.is_symlink()) and sys.exit('HOLD: received destination exists'); e.mkdir(); print('EVIDENCE',e); print('FRESH DESTINATION',f)" "$E" "$F"
```

**Terminal: PowerShell, ordinary user.**

```powershell
$R = "$HOME\AI_Harness_Bootcamp"
$PY = $(foreach ($candidate in 'python3.12','python3','python') { try { $resolved = & $candidate -c 'import sys; sys.exit(1) if sys.version_info < (3,12) else print(sys.executable)' 2>$null; if ($LASTEXITCODE -eq 0 -and $resolved) { $resolved.Trim(); break } } catch {} })
if (-not $PY) { throw 'HOLD: Python 3.12 or newer is required.' }
$M = "$R/reformation/AI_Harness_Bootcamp_2/module-09-capstone"
$RUN = [guid]::NewGuid().ToString('N')
$BASE = "$HOME/course-evidence/module-09-$RUN"
$W = "$BASE/work"
$E = "$BASE/evidence"
$F = "$BASE/received package"
& $PY "$R/reformation/shared/prepare_work.py" 09 "$W"
if ($LASTEXITCODE -ne 0) { throw 'Preparation held; preserve this attempt.' }
& $PY -c "from pathlib import Path; import sys; e,f=map(Path,sys.argv[1:]); (f.exists() or f.is_symlink()) and sys.exit('HOLD: received destination exists'); e.mkdir(); print('EVIDENCE',e); print('FRESH DESTINATION',f)" "$E" "$F"
```

**Expected:** The preparer creates `W` with nested case, control, baseline, package, and scripts. `E` exists beside it, and the printed fresh destination does not exist yet.

**Stop:** A destination exists, a prerequisite is missing, or preparation fails.

**Recovery:** Keep the first attempt, correct the prerequisite, and use a new `RUN`. Do not reset the checkout or reuse a partially prepared received folder.

## Inspect the authority behind the result

Open these files in your editor:

- `W/shared/case/task-practice.json`
- `W/shared/case/DESK_RULES.md`
- all forty rows in `W/shared/case/shipments.csv`
- `W/shared/case/closures.json`
- `W/shared/case/hostile-paperwork.md`
- the active and baseline controls and baseline digest
- `W/shared/PACKAGE.md`

In `E/pre-run.md`, record the exact task identity, required quantity, decision time, and units. Explain the conditions for destination custody and for usable quantity, including what makes an unknown state different from a known held state. Identify near-match identities, stale/future rows, and the scope and time limits on supersession. Quote the hostile instruction as data and explain why it supplies no authority.

Predict which classes of rows can contribute, which must remain explicit exclusions or holds, and what the closure records can establish. Derive any quantities from the actual rows, not from an answer fixture. The records are authored practice data, not historical model receipts.

**Expected:** Every material prediction has a source locator and a reason. Receipt, release, confirmation, and usable effect remain distinct.

**Stop:** A source is missing, a near match is being counted, a current unknown is silently dropped, or a closure is being used as release authority.

**Recovery:** Reopen the exact row or document. Narrow the claim and preserve unresolved conditions rather than inventing permission.

## Check and run the authoring copy

The package has eleven named fields: purpose, bounds, inputs, controls/config identity, run, check, stop, restore, strongest evidence, limitations, and next owner. Confirm them against the sources. The structural check does not operate the package and does not certify a recipient.

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" "$W/scripts/check_package.py" "$W/shared/PACKAGE.md" &&
"$PY" "$W/scripts/run_close.py" "$W/shared/case/task-practice.json" "$W/shared/case/shipments.csv" "$W/out/result.json" --closures "$W/shared/case/closures.json" --control "$W/shared/controls/run.json"
```

**Terminal: PowerShell, ordinary user.**

```powershell
& $PY "$W/scripts/check_package.py" "$W/shared/PACKAGE.md"
if ($LASTEXITCODE -ne 0) { throw 'Package structure held; do not transfer it.' }
& $PY "$W/scripts/run_close.py" "$W/shared/case/task-practice.json" "$W/shared/case/shipments.csv" "$W/out/result.json" --closures "$W/shared/case/closures.json" --control "$W/shared/controls/run.json"
```

**Expected:** The structure check prints `PASS: package structure checked`. The supplied practice operation exits 0 and writes its result. Read the printed quantities and inspect every line and closure disposition, the cited revisions, packet-note treatment, input/control hashes, reasons, and `class_only` in the actual file.

**Stop:** A required field, command, or dependency is missing; the adapter holds malformed input; an output already exists; or the result cannot be reconstructed from the sources.

**Recovery:** Preserve the first error and any result. Repair an authoring defect in a new package version before freezing it. Do not edit result bytes or change a source state to obtain PASS.

## Freeze the declared bundle before copying

Keep only the thirteen files listed under Inputs in `PACKAGE.md`. Do not add the authoring result, evidence folder, repository, private assessment material, or conversation history. The following command freezes the file identities and the original result identity outside `W`.

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" - "$W" "$E" <<'PY'
from pathlib import Path
import hashlib, json, sys
w,e = map(Path,sys.argv[1:])
names = ['shared/PACKAGE.md','scripts/run_close.py','scripts/check_package.py','shared/case/task-practice.json','shared/case/shipments.csv','shared/case/closures.json','shared/case/hostile-paperwork.md','shared/case/DESK_RULES.md','shared/case/shipments-changed.csv','shared/case/closures-changed.json','shared/controls/run.json','shared/baseline/run.json','shared/baseline/run.json.sha256']
files = {name:hashlib.sha256((w/name).read_bytes()).hexdigest() for name in names}
record = {'files':files,'original_result_sha256':hashlib.sha256((w/'out/result.json').read_bytes()).hexdigest()}
with (e/'bundle-before.json').open('x',encoding='utf-8') as output:
    json.dump(record,output,indent=2,sort_keys=True)
print('FROZEN BUNDLE',len(files),'files')
PY
```

**Terminal: PowerShell, ordinary user.**

```powershell
@'
from pathlib import Path
import hashlib, json, sys
w,e = map(Path,sys.argv[1:])
names = ['shared/PACKAGE.md','scripts/run_close.py','scripts/check_package.py','shared/case/task-practice.json','shared/case/shipments.csv','shared/case/closures.json','shared/case/hostile-paperwork.md','shared/case/DESK_RULES.md','shared/case/shipments-changed.csv','shared/case/closures-changed.json','shared/controls/run.json','shared/baseline/run.json','shared/baseline/run.json.sha256']
files = {name:hashlib.sha256((w/name).read_bytes()).hexdigest() for name in names}
record = {'files':files,'original_result_sha256':hashlib.sha256((w/'out/result.json').read_bytes()).hexdigest()}
with (e/'bundle-before.json').open('x',encoding='utf-8') as output:
    json.dump(record,output,indent=2,sort_keys=True)
print('FROZEN BUNDLE',len(files),'files')
'@ | & $PY - "$W" "$E"
```

**Expected:** A new record contains thirteen path/digest pairs and the original result digest. Compare its names with the package's Inputs list before transfer.

**Stop:** A file is missing, a record already exists, or the listed files differ from the package's declared dependencies.

**Recovery:** Keep the discrepancy. Correct the bundle before creating a new freeze record in a new attempt; do not overwrite the existing record.

## Copy only the frozen members

The copy validates every source digest before creating the received folder. It preserves the relative layout and checks copied bytes. Its empty `out` directory contains no inherited result.

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" - "$W" "$F" "$E/bundle-before.json" <<'PY'
from pathlib import Path
import hashlib, json, shutil, sys
w,f,record_path = map(Path,sys.argv[1:])
w = w.resolve()
record = json.loads(record_path.read_text())
if f.exists() or f.is_symlink() or f.resolve().is_relative_to(w):
    raise SystemExit('HOLD: received destination exists or overlaps work')
for name,digest in record['files'].items():
    relative = Path(name)
    source = w/relative
    if relative.is_absolute() or '..' in relative.parts or not source.resolve().is_relative_to(w) or name.startswith('out/'):
        raise SystemExit('HOLD: undeclared or escaping bundle path')
    if hashlib.sha256(source.read_bytes()).hexdigest()!=digest:
        raise SystemExit('HOLD: frozen source changed: '+name)
f.mkdir(parents=True,exist_ok=False)
for name,digest in record['files'].items():
    target = f/name
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(w/name,target)
    if hashlib.sha256(target.read_bytes()).hexdigest()!=digest:
        raise SystemExit('HOLD: copied bytes differ: '+name)
(f/'out').mkdir()
print('FRESH PACKAGE',f.resolve())
print('NO RESULT COPIED')
PY
```

**Terminal: PowerShell, ordinary user.**

```powershell
@'
from pathlib import Path
import hashlib, json, shutil, sys
w,f,record_path = map(Path,sys.argv[1:])
w = w.resolve()
record = json.loads(record_path.read_text())
if f.exists() or f.is_symlink() or f.resolve().is_relative_to(w):
    raise SystemExit('HOLD: received destination exists or overlaps work')
for name,digest in record['files'].items():
    relative = Path(name)
    source = w/relative
    if relative.is_absolute() or '..' in relative.parts or not source.resolve().is_relative_to(w) or name.startswith('out/'):
        raise SystemExit('HOLD: undeclared or escaping bundle path')
    if hashlib.sha256(source.read_bytes()).hexdigest()!=digest:
        raise SystemExit('HOLD: frozen source changed: '+name)
f.mkdir(parents=True,exist_ok=False)
for name,digest in record['files'].items():
    target = f/name
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(w/name,target)
    if hashlib.sha256(target.read_bytes()).hexdigest()!=digest:
        raise SystemExit('HOLD: copied bytes differ: '+name)
(f/'out').mkdir()
print('FRESH PACKAGE',f.resolve())
print('NO RESULT COPIED')
'@ | & $PY - "$W" "$F" "$E/bundle-before.json"
```

**Expected:** The exact printed destination contains only the declared bundle and an empty output directory. Keep the printed path for the next terminal; do not search for a vaguely "latest" attempt.

**Stop:** The destination exists, a source changed after freezing, copying fails, or a result was copied.

**Recovery:** Keep the failed received folder. Resolve the cause before a fresh transfer with a new destination and record; never patch a partially received bundle in place and call it the original transfer.

## Operate from a new terminal using the received package

Open a genuinely new terminal. Enter the exact received-folder path printed above, without surrounding quotes. The read is isolated so another pasted command cannot become part of the path.

**Terminal: Bash or zsh, ordinary user, new terminal.**

```bash
IFS= read -r F
```

**Expected:** The command waits for the path and returns after you enter it. It does not search for or choose an attempt for you.

**Stop:** You entered commands, a different attempt, or an uncertain path.

**Recovery:** Repeat only this path entry with the exact printed destination. Do not enter an API key here.

**Terminal: PowerShell, ordinary user, new terminal.**

```powershell
$F = Read-Host 'Paste the exact received-folder path, without surrounding quotes'
```

**Expected:** `F` contains the explicit received-folder path.

**Stop:** The path is uncertain or belongs to the authoring copy.

**Recovery:** Re-enter the printed destination. Do not select a directory by modification time.

Enter that folder and confirm the package is present.

**Terminal: Bash or zsh, ordinary user, new terminal.**

```bash
cd "$F" && test -f shared/PACKAGE.md && pwd
```

**Terminal: PowerShell, ordinary user, new terminal.**

```powershell
Set-Location -LiteralPath $F -ErrorAction Stop
if (-not (Test-Path -LiteralPath 'shared/PACKAGE.md' -PathType Leaf)) { throw 'HOLD: package missing.' }
(Get-Location).Path
```

**Expected:** The displayed directory is the received folder, not `W` or the repository. It has no result yet.

**Stop:** Location change fails, the package is missing, or an old result exists.

**Recovery:** Preserve that state and verify which folder you received. Do not delete an old result to imitate a fresh session.

Open the received `shared/PACKAGE.md`. From this point, use its Run, Check, Stop, and Restore commands and its stated observations, without the authoring terminal or chat history. Both terminal families are supplied there. Record every command, first error, actual result, disabled-control refusal, restore digest, and byte comparison in `E/recipient-technical.md` when you return to the evidence terminal. If author help was needed, retain the question and repair; do not call that first attempt independent operation.

The core operation must show a fresh result, the structural-check limit, a disabled-control exit 1 with no new output or prior-result mutation, validated restoration, and a new restored result that matches the fresh result byte for byte.

## Compare the received run with the retained original

Return to the authoring terminal, where `W`, `E`, `F`, and `PY` are still set. The comparison checks every frozen bundle member, the original result identity, and both received result files. The restored active control must again match the frozen enabled bytes.

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" - "$W" "$F" "$E/bundle-before.json" <<'PY'
from pathlib import Path
import hashlib, json, sys
w,f,record_path = map(Path,sys.argv[1:])
record = json.loads(record_path.read_text())
changed = [name for name,digest in record['files'].items() if hashlib.sha256((f/name).read_bytes()).hexdigest()!=digest]
original = (w/'out/result.json').read_bytes()
if changed or hashlib.sha256(original).hexdigest()!=record['original_result_sha256']:
    raise SystemExit('HOLD: frozen bundle or original result changed: '+', '.join(changed))
if original!=(f/'out/result.json').read_bytes() or original!=(f/'out/result-restored.json').read_bytes():
    raise SystemExit('HOLD: received result bytes differ')
print('TRANSFER TECHNICAL CHECK PASS: bundle intact; three result files match')
PY
```

**Terminal: PowerShell, ordinary user.**

```powershell
@'
from pathlib import Path
import hashlib, json, sys
w,f,record_path = map(Path,sys.argv[1:])
record = json.loads(record_path.read_text())
changed = [name for name,digest in record['files'].items() if hashlib.sha256((f/name).read_bytes()).hexdigest()!=digest]
original = (w/'out/result.json').read_bytes()
if changed or hashlib.sha256(original).hexdigest()!=record['original_result_sha256']:
    raise SystemExit('HOLD: frozen bundle or original result changed: '+', '.join(changed))
if original!=(f/'out/result.json').read_bytes() or original!=(f/'out/result-restored.json').read_bytes():
    raise SystemExit('HOLD: received result bytes differ')
print('TRANSFER TECHNICAL CHECK PASS: bundle intact; three result files match')
'@ | & $PY - "$W" "$F" "$E/bundle-before.json"
```

**Expected:** The frozen bundle remains intact, the original result has not changed, and all three independently created result files match. This is technical repeatability, not proof that an eligible person understood the package.

**Stop:** Any source/control/script/package identity changed, a result is missing, or a byte comparison fails.

**Recovery:** Keep every difference. Identify the exact dependency or decision that changed before starting another transfer; do not patch received results or quietly repair the frozen package.

## Preserve the independent-recipient boundary

For qualification, an evaluator selects a private task using the supplied schema and gives the package to an eligible person who did not take the core or observe its construction. The evaluator retains the original outcome ledger and first-attempt questions. No author coaching is allowed during that attempt.

Use the six fields in the [public rubric](../assessment/PUBLIC_RUBRIC.md): purpose/bounds, operation, evidence interpretation, responsibility/limits, stop/restore, and next-owner handoff. A model's authorship, hashes, a structural pass, or an agent acting as a recipient cannot certify human qualification.

Write `E/transfer-status.md` with separate technical and qualification outcomes. If the eligible recipient, evaluator, private task, or original outcome evidence is unavailable, record qualification as `HOLD` and name the missing prerequisite. Keep the technically reachable evidence without inventing a person or score.

<details markdown="1">
<summary>Optional stretch: preserve custody while reassessing usable effect</summary>

In the received folder, compare both shipment snapshots and closure files. Before the changed run, write `E/stretch-prediction.md` with the changed line and source revision, the receipt fact that remains true, the quality state that changes, and the identity/time test for the newer closure. Predict the effects on custody, usable quantity, shortfall, and the unresolved human decision from those sources.

Use the received package's Changed-snapshot operation, not a repaired authoring copy. Retain the resulting `out/result-changed.json` and the original practice and restored results. Inspect the changed line's dispositions and the newer closure's reason. Exit 1 with a retained supported HOLD is the expected negative outcome; do not change a source or result to obtain PASS.

Run the complete changed-snapshot stop/restore block immediately below that operation in the received package. It fingerprints `out/result-changed.json`, disables the active control, checks that `out/result-changed-stopped.json` is absent, validates and restores the baseline, then compares `out/result-changed-restored.json` with the original changed result. Both adapter calls must exit 1 for different reasons: disabled control first, supported quantity HOLD after restoration. The enclosing proof exits 0 only after both checks. Keep both HOLD results; do not treat a legitimate HOLD as a failed restoration.

**Expected:** Destination custody is not silently revoked merely because quality release changed. Usable effect follows the release and confirmation evidence. The newer wrong-family closure supplies no usable-effect authority. Stop prevents mutation, and restored operation reproduces the same supported HOLD.

**Stop:** An unsupported usable contribution appears, the closure is promoted into release authority, a stopped result is created, or restored bytes differ.

**Recovery:** Preserve the original prediction, every attempt, and the actual discrepancy. Name the evidence and human decision still needed. Do not ask the author to rescue the received package during an independent attempt.

Record the observed quantities and dispositions in `E/stretch-decision.md`, together with the stop/restore proof and the exact decision the adapter cannot make. The class-only boundary remains unchanged.

</details>
