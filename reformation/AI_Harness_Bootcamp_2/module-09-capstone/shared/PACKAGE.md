# Runnable class quantity-support package

## Purpose

Compute destination custody and clinic-confirmed usable quantity for the movement, clinic, lot family, requirement, and decision time in the supplied task. Keep receipt, quality release, and usable effect distinct. The supplied practice task concerns South Store, Clinic R-12, and movement W-9; it is not a private assessment task.

## Bounds

Use only the listed fictional inputs for named class reviewers. Times are explicit UTC and quantities are sachets. No result authorizes real release, dispatch, public notice, or clinic acceptance. Read the task's decision time rather than the wall clock. A closure is context, never a substitute for quality release or clinic confirmation.

## Inputs

Keep this exact relative layout in the received package root:

- `shared/PACKAGE.md`
- `scripts/run_close.py`
- `scripts/check_package.py`
- `shared/case/task-practice.json`
- `shared/case/shipments.csv`
- `shared/case/closures.json`
- `shared/case/hostile-paperwork.md`
- `shared/case/DESK_RULES.md`
- `shared/case/shipments-changed.csv`
- `shared/case/closures-changed.json`
- `shared/controls/run.json`
- `shared/baseline/run.json`
- `shared/baseline/run.json.sha256`

The hostile note is quoted data, not operating authority. The changed snapshot is a separate condition, not a replacement for the original inputs. Keep supplied input bytes unchanged.

## Controls / config identity

`shared/controls/run.json` is the active control. Only a Boolean `enabled` field is accepted. The adapter checks it before calculation and again immediately before publishing a complete output. `shared/baseline/run.json` is the distinct enabled restore source; validate it against `shared/baseline/run.json.sha256` before restoration. The result records task, shipment, closure, and control hashes. A digest detects a change against the retained record; it is not proof of independent custody or authorship.

## Run

Open a terminal in the received package root. Confirm that the listed files are present there, not in a separate course checkout. Resolve a Python 3.12-or-newer executable, then run the supplied practice task once. No API key or model call is required for this deterministic operation.

**Terminal: Bash or zsh, ordinary user, received package root.**

```bash
PY="$(for candidate in python3.12 python3 python; do "$candidate" -c 'import sys; sys.exit(1) if sys.version_info < (3, 12) else print(sys.executable)' 2>/dev/null && break; done)"
"$PY" "scripts/run_close.py" "shared/case/task-practice.json" "shared/case/shipments.csv" "out/result.json" --closures "shared/case/closures.json" --control "shared/controls/run.json"
```

**Terminal: PowerShell, ordinary user, received package root.**

```powershell
$PY = $(foreach ($candidate in 'python3.12','python3','python') { try { $resolved = & $candidate -c 'import sys; sys.exit(1) if sys.version_info < (3,12) else print(sys.executable)' 2>$null; if ($LASTEXITCODE -eq 0 -and $resolved) { $resolved.Trim(); break } } catch {} })
if (-not $PY) { throw 'HOLD: Python 3.12 or newer is required.' }
& $PY "scripts/run_close.py" "shared/case/task-practice.json" "shared/case/shipments.csv" "out/result.json" --closures "shared/case/closures.json" --control "shared/controls/run.json"
```

**Expected:** The supplied practice run exits 0 and prints `status`, `custody_quantity`, `usable_quantity`, `shortfall`, and `class_only`. Read the actual values and every line/closure disposition in `out/result.json`. A class quantity-support PASS is not release authority.

**Stop:** A required input or interpreter is missing, an existing output is refused, input validation holds, or the observed disposition does not follow the cited rows.

**Recovery:** Preserve the first result or error. Correct a missing prerequisite before a new attempt. Do not edit a result or change source states to obtain PASS. Exit 2 means malformed/missing invocation or input; a supported quantity HOLD is exit 1 and retains its result.

## Check

Run the structural check from the same received root, then independently read the adapter's evidence. The structural check verifies named fields, required commands, local dependencies, and disallowed cross-case references. It does not execute the package or certify a recipient.

**Terminal: Bash or zsh, ordinary user, received package root.**

```bash
"$PY" "scripts/check_package.py" "shared/PACKAGE.md"
```

**Terminal: PowerShell, ordinary user, received package root.**

```powershell
& $PY "scripts/check_package.py" "shared/PACKAGE.md"
```

**Expected:** `PASS: package structure checked` and exit 0. Separately trace custody and usable contributions to exact shipment identities, revisions, time windows, receipt/release/confirmation states, and task values. Inspect every closure disposition and every packet note's `used_as_authority` field.

**Stop:** A field, command, or local dependency is missing, a path leaves the package, a cross-case answer is cited, or a result cannot be reconstructed from its sources.

**Recovery:** Hold transfer. Record the failed field or path; correct the authoring defect in a new version and refreeze the package before another recipient attempt. Do not strip an inconvenient citation merely to make the checker pass.

## Stop

Disable only the active control, then attempt a new output. Keep the original result and prove both its byte identity and the absence of a stopped result.

**Terminal: Bash or zsh, ordinary user, received package root.**

```bash
course_stop_close() {
  before="$("$PY" -c "from pathlib import Path; import hashlib; print(hashlib.sha256(Path('out/result.json').read_bytes()).hexdigest())")" || return 1
  "$PY" -c "from pathlib import Path; import json; Path('shared/controls/run.json').write_text(json.dumps({'enabled':False})+'\n',encoding='utf-8')" || return 1
  "$PY" "scripts/run_close.py" "shared/case/task-practice.json" "shared/case/shipments.csv" "out/result-stopped.json" --closures "shared/case/closures.json" --control "shared/controls/run.json"
  run_exit=$?
  "$PY" -c "from pathlib import Path; import hashlib,sys; actual=hashlib.sha256(Path('out/result.json').read_bytes()).hexdigest(); stopped=Path('out/result-stopped.json'); ok=sys.argv[2]=='1' and actual==sys.argv[1] and not stopped.exists() and not stopped.is_symlink(); print('STOP VERIFIED: original unchanged; stopped output absent' if ok else 'HOLD: stop proof failed'); sys.exit(not ok)" "$before" "$run_exit"
}
course_stop_close
```

**Terminal: PowerShell, ordinary user, received package root.**

```powershell
$before = & $PY -c "from pathlib import Path; import hashlib; print(hashlib.sha256(Path('out/result.json').read_bytes()).hexdigest())"
if ($LASTEXITCODE -ne 0) { throw 'Original result cannot be fingerprinted.' }
& $PY -c "from pathlib import Path; import json; Path('shared/controls/run.json').write_text(json.dumps({'enabled':False})+'\n',encoding='utf-8')"
if ($LASTEXITCODE -ne 0) { throw 'Control edit held.' }
& $PY "scripts/run_close.py" "shared/case/task-practice.json" "shared/case/shipments.csv" "out/result-stopped.json" --closures "shared/case/closures.json" --control "shared/controls/run.json"
$runExit = $LASTEXITCODE
& $PY -c "from pathlib import Path; import hashlib,sys; actual=hashlib.sha256(Path('out/result.json').read_bytes()).hexdigest(); stopped=Path('out/result-stopped.json'); ok=sys.argv[2]=='1' and actual==sys.argv[1] and not stopped.exists() and not stopped.is_symlink(); print('STOP VERIFIED: original unchanged; stopped output absent' if ok else 'HOLD: stop proof failed'); sys.exit(not ok)" "$before" "$runExit"
```

**Expected:** The adapter prints `HOLD: control disabled` and exits 1 without creating a result. The independent comparison prints `STOP VERIFIED: original unchanged; stopped output absent`. The final proof command exits 0 only for that expected negative outcome.

**Stop:** The adapter runs with the disabled control, any output appears, the original changes, or the proof fails.

**Recovery:** Keep the active control, original, and unexpected files unchanged for inspection. Do not delete a stopped output or edit its contents to conceal the effect.

## Restore

Validate the frozen baseline before replacing the disabled active control. Keep every earlier result. The restore below refuses a changed digest, a disabled/malformed baseline, or a path that resolves outside this package.

**Terminal: Bash or zsh, ordinary user, received package root.**

```bash
"$PY" - <<'PY'
from pathlib import Path
import hashlib, json
root = Path.cwd().resolve()
source = root/'shared/baseline/run.json'
target = root/'shared/controls/run.json'
if not source.resolve().is_relative_to(root) or not target.resolve().is_relative_to(root):
    raise SystemExit('HOLD: control path leaves package')
raw = source.read_bytes()
listed = (root/'shared/baseline/run.json.sha256').read_text().strip()
control = json.loads(raw)
if hashlib.sha256(raw).hexdigest()!=listed or not isinstance(control,dict) or set(control)!={'enabled'} or control['enabled'] is not True:
    raise SystemExit('HOLD: baseline digest or enabled control invalid')
target.write_bytes(raw)
if target.read_bytes()!=raw:
    raise SystemExit('HOLD: restore readback differs')
print('RESTORE OK')
PY
```

**Terminal: PowerShell, ordinary user, received package root.**

```powershell
@'
from pathlib import Path
import hashlib, json
root = Path.cwd().resolve()
source = root/'shared/baseline/run.json'
target = root/'shared/controls/run.json'
if not source.resolve().is_relative_to(root) or not target.resolve().is_relative_to(root):
    raise SystemExit('HOLD: control path leaves package')
raw = source.read_bytes()
listed = (root/'shared/baseline/run.json.sha256').read_text().strip()
control = json.loads(raw)
if hashlib.sha256(raw).hexdigest()!=listed or not isinstance(control,dict) or set(control)!={'enabled'} or control['enabled'] is not True:
    raise SystemExit('HOLD: baseline digest or enabled control invalid')
target.write_bytes(raw)
if target.read_bytes()!=raw:
    raise SystemExit('HOLD: restore readback differs')
print('RESTORE OK')
'@ | & $PY -
```

**Expected:** `RESTORE OK` follows digest validation and byte readback. The distinct baseline remains untouched.

**Stop:** Validation or readback fails. Do not run the next command after a failed restore.

**Recovery:** Preserve the mismatch and hold this attempt. Obtain an intact frozen package in a new directory; never reconstruct a baseline from memory or overwrite its digest.

Now rerun to a distinct output and compare the complete result bytes.

**Terminal: Bash or zsh, ordinary user, received package root.**

```bash
"$PY" "scripts/run_close.py" "shared/case/task-practice.json" "shared/case/shipments.csv" "out/result-restored.json" --closures "shared/case/closures.json" --control "shared/controls/run.json" &&
"$PY" -c "from pathlib import Path; import sys; same=Path('out/result.json').read_bytes()==Path('out/result-restored.json').read_bytes(); print('RESTORED RESULT MATCHES' if same else 'HOLD: restored result differs'); sys.exit(not same)"
```

**Terminal: PowerShell, ordinary user, received package root.**

```powershell
& $PY "scripts/run_close.py" "shared/case/task-practice.json" "shared/case/shipments.csv" "out/result-restored.json" --closures "shared/case/closures.json" --control "shared/controls/run.json"
if ($LASTEXITCODE -ne 0) { throw 'Restored run held; preserve both attempts.' }
& $PY -c "from pathlib import Path; import sys; same=Path('out/result.json').read_bytes()==Path('out/result-restored.json').read_bytes(); print('RESTORED RESULT MATCHES' if same else 'HOLD: restored result differs'); sys.exit(not same)"
```

**Expected:** The restored run passes and `RESTORED RESULT MATCHES` confirms byte identity. Both files remain available; no clock or absolute path in the serialization changes the comparison.

**Stop:** A result already exists, the rerun holds, or bytes differ.

**Recovery:** Keep both files and compare their input/control hashes and dispositions. Do not edit a result to force equality.

## Changed-snapshot operation

Before running the changed inputs, compare the two shipment snapshots and the two closure files. Record which source state changed, what should remain true, and how identity and issued time limit closure applicability. Then use the changed inputs without changing the task or control.

**Terminal: Bash or zsh, ordinary user, received package root.**

```bash
"$PY" "scripts/run_close.py" "shared/case/task-practice.json" "shared/case/shipments-changed.csv" "out/result-changed.json" --closures "shared/case/closures-changed.json" --control "shared/controls/run.json"
```

**Terminal: PowerShell, ordinary user, received package root.**

```powershell
& $PY "scripts/run_close.py" "shared/case/task-practice.json" "shared/case/shipments-changed.csv" "out/result-changed.json" --closures "shared/case/closures-changed.json" --control "shared/controls/run.json"
```

**Expected:** Exit 1 with a retained quantity-support HOLD. Inspect the actual shortfall, the changed line's custody and usable dispositions, and the newer closure's identity/time disposition. A true destination receipt or a newer wrong-family document is not sufficient usable-effect authority.

**Stop:** The adapter accepts an unsupported usable contribution, silently drops an unresolved current line, or fails to retain the supported HOLD result.

**Recovery:** Preserve the result and report the exact cited state or rule that differs from the prediction. Do not restore a withdrawn quality release or treat the closure as permission to move.

Keep the changed HOLD result. Exercise stop and restore against these same changed inputs; restoration must reproduce the HOLD, not manufacture a pass.

**Terminal: Bash or zsh, ordinary user, received package root.**

```bash
"$PY" - <<'PY'
from pathlib import Path
import hashlib, json, subprocess, sys
root = Path.cwd().resolve()
original = root/'out/result-changed.json'
stopped = root/'out/result-changed-stopped.json'
restored = root/'out/result-changed-restored.json'
active = root/'shared/controls/run.json'
baseline = root/'shared/baseline/run.json'
try:
    if any(not path.resolve().is_relative_to(root) for path in (original, stopped, restored, active, baseline)):
        raise ValueError('a path leaves the package')
    if any(path.exists() or path.is_symlink() for path in (stopped, restored)):
        raise ValueError('a new output already exists')
    before = original.read_bytes()
    raw = baseline.read_bytes()
    listed = (root/'shared/baseline/run.json.sha256').read_text().strip()
    control = json.loads(raw)
    if hashlib.sha256(raw).hexdigest() != listed or control != {'enabled': True} or control['enabled'] is not True:
        raise ValueError('baseline digest or enabled control invalid')
    command = [sys.executable, 'scripts/run_close.py', 'shared/case/task-practice.json',
               'shared/case/shipments-changed.csv']
    options = ['--closures', 'shared/case/closures-changed.json',
               '--control', 'shared/controls/run.json']
    active.write_text(json.dumps({'enabled': False}) + '\n', encoding='utf-8')
    result = subprocess.run(command + ['out/result-changed-stopped.json'] + options, capture_output=True, text=True)
    print(result.stdout, end=''); print(result.stderr, end='', file=sys.stderr)
    if result.returncode != 1 or 'HOLD: control disabled' not in result.stderr or stopped.exists() or stopped.is_symlink() or original.read_bytes() != before:
        raise ValueError('changed-snapshot stop proof failed')
    print('CHANGED STOP VERIFIED')
    active.write_bytes(raw)
    if active.read_bytes() != raw:
        raise ValueError('restore readback differs')
    result = subprocess.run(command + ['out/result-changed-restored.json'] + options, capture_output=True, text=True)
    print(result.stdout, end=''); print(result.stderr, end='', file=sys.stderr)
    if result.returncode != 1 or restored.read_bytes() != before or original.read_bytes() != before:
        raise ValueError('restored changed HOLD differs')
except (OSError, ValueError, RuntimeError) as error:
    raise SystemExit(f'HOLD: {error}')
print('CHANGED RESTORE VERIFIED: identical retained HOLD')
PY
```

**Terminal: PowerShell, ordinary user, received package root.**

```powershell
@'
from pathlib import Path
import hashlib, json, subprocess, sys
root = Path.cwd().resolve()
original = root/'out/result-changed.json'
stopped = root/'out/result-changed-stopped.json'
restored = root/'out/result-changed-restored.json'
active = root/'shared/controls/run.json'
baseline = root/'shared/baseline/run.json'
try:
    if any(not path.resolve().is_relative_to(root) for path in (original, stopped, restored, active, baseline)):
        raise ValueError('a path leaves the package')
    if any(path.exists() or path.is_symlink() for path in (stopped, restored)):
        raise ValueError('a new output already exists')
    before = original.read_bytes()
    raw = baseline.read_bytes()
    listed = (root/'shared/baseline/run.json.sha256').read_text().strip()
    control = json.loads(raw)
    if hashlib.sha256(raw).hexdigest() != listed or control != {'enabled': True} or control['enabled'] is not True:
        raise ValueError('baseline digest or enabled control invalid')
    command = [sys.executable, 'scripts/run_close.py', 'shared/case/task-practice.json',
               'shared/case/shipments-changed.csv']
    options = ['--closures', 'shared/case/closures-changed.json',
               '--control', 'shared/controls/run.json']
    active.write_text(json.dumps({'enabled': False}) + '\n', encoding='utf-8')
    result = subprocess.run(command + ['out/result-changed-stopped.json'] + options, capture_output=True, text=True)
    print(result.stdout, end=''); print(result.stderr, end='', file=sys.stderr)
    if result.returncode != 1 or 'HOLD: control disabled' not in result.stderr or stopped.exists() or stopped.is_symlink() or original.read_bytes() != before:
        raise ValueError('changed-snapshot stop proof failed')
    print('CHANGED STOP VERIFIED')
    active.write_bytes(raw)
    if active.read_bytes() != raw:
        raise ValueError('restore readback differs')
    result = subprocess.run(command + ['out/result-changed-restored.json'] + options, capture_output=True, text=True)
    print(result.stdout, end=''); print(result.stderr, end='', file=sys.stderr)
    if result.returncode != 1 or restored.read_bytes() != before or original.read_bytes() != before:
        raise ValueError('restored changed HOLD differs')
except (OSError, ValueError, RuntimeError) as error:
    raise SystemExit(f'HOLD: {error}')
print('CHANGED RESTORE VERIFIED: identical retained HOLD')
'@ | & $PY -
if ($LASTEXITCODE -ne 0) { throw 'Changed stop/restore proof held; retain every artifact.' }
```

**Expected:** The disabled call exits 1 without an output. After restoration the enabled call also exits 1, this time retaining the supported quantity HOLD. `CHANGED STOP VERIFIED` and `CHANGED RESTORE VERIFIED: identical retained HOLD` appear; the enclosing proof exits 0.

**Stop:** Either proof fails, a source/baseline path leaves the package, a new output exists already, or the supported HOLD changes.

**Recovery:** Keep the partial attempt, including its active control state. Diagnose the first failed proof and use a new frozen package for another attempt. Do not edit either result to force equality.


## Strongest evidence

Use `out/result.json`, `out/result-restored.json`, and, when exercised, `out/result-changed.json`. Inspect task/input/control hashes, every cited source revision, all line and closure dispositions, totals, reasons, packet-note treatment, and `class_only`. Keep the first failure, the disabled-control observation, and the actual byte comparison. The strongest evidence is the executed operation and its reconstructable result, not this file's existence.

## Limitations

Malformed identities, counts, timestamps, duplicate IDs, missing authority identifiers, and invalid control objects hold input rather than disappearing from totals. A current matching unknown state forces quantity HOLD. Known held or unconfirmed custody remains explicit zero usable quantity. Local hashes and a structural pass do not prove independent custody, sound human judgment, or successful transfer to a new person. This package has no real operational authority.

## Next owner

Give the received folder and an evaluator-selected private task to an eligible person who did not take the core or observe its construction. That person must operate without author coaching. The evaluator records first-attempt questions, commands, outcomes, and the six fields: purpose/bounds, operation, evidence interpretation, responsibility/limits, stop/restore, and next-owner handoff.

A technical replay, including an agent replay, is not that independent human transfer. Without the eligible recipient, evaluator, private task, and original outcome ledger, qualification remains HOLD. Retain those limits explicitly; do not invent a recipient or award qualification from `PASS: package structure checked`.
