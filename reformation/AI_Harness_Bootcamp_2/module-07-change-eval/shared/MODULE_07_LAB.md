# Module 7 · Evaluate a change without hiding variation

You can already predict a bounded change and restore its baseline. Now you will decide whether a candidate deserves adoption when individual failures matter more than an average. You will freeze the decision rule before inspecting outcomes, compare the same cases, and distinguish observed variation from an instruction's effect.

The fictional movement carries heater-fuel cans from Ridge Depot to Clinic T-8 on vehicle SB-4. The forty case packets and their three briefs are authored practice data, not records of OpenRouter calls. Nothing here authorizes a real load sheet or movement.

A **hard gate** is a condition that cannot be traded against a better score elsewhere. Here, an unsourced mass or a missing time-zone label defeats a candidate. A **paired comparison** uses the same source packet for each condition.

## Prepare a separate attempt

Use the verified Python and checkout from [setup](../../module-00-setup/README.md). Open an ordinary terminal. These commands work from any directory and leave earlier attempts intact. `W` is your work folder; `E` holds your records outside it. Do not open candidate briefs yet.

**Terminal: Bash or zsh, ordinary user.**

```bash
R="$HOME/AI_Harness_Bootcamp"
PY="$(for candidate in python3.12 python3 python; do "$candidate" -c 'import sys; sys.exit(1) if sys.version_info < (3, 12) else print(sys.executable)' 2>/dev/null && break; done)"
M="$R/reformation/AI_Harness_Bootcamp_2/module-07-change-eval"
RUN="$(date -u +%Y%m%dT%H%M%SZ)-$$"
W="$HOME/course-evidence/module-07-$RUN/work"
E="$HOME/course-evidence/module-07-$RUN/evidence"
"$PY" "$R/reformation/shared/prepare_work.py" 07 "$W" &&
"$PY" -c "from pathlib import Path; import sys; Path(sys.argv[1]).mkdir(parents=True, exist_ok=False)" "$E"
```

**Terminal: PowerShell, ordinary user.**

```powershell
$R = "$HOME\AI_Harness_Bootcamp"
$PY = $(foreach ($candidate in 'python3.12','python3','python') { try { $resolved = & $candidate -c 'import sys; sys.exit(1) if sys.version_info < (3,12) else print(sys.executable)' 2>$null; if ($LASTEXITCODE -eq 0 -and $resolved) { $resolved.Trim(); break } } catch {} })
if (-not $PY) { throw 'HOLD: Python 3.12 or newer is required.' }
$M = "$R\reformation\AI_Harness_Bootcamp_2\module-07-change-eval"
$RUN = [guid]::NewGuid().ToString('N')
$W = "$HOME\course-evidence\module-07-$RUN\work"
$E = "$HOME\course-evidence\module-07-$RUN\evidence"
& $PY "$R\reformation\shared\prepare_work.py" 07 "$W"
if ($LASTEXITCODE -ne 0) { throw 'Preparation stopped; preserve this attempt.' }
& $PY -c "from pathlib import Path; import sys; Path(sys.argv[1]).mkdir(parents=True, exist_ok=False)" "$E"
```

**Expected:** The preparer reports the new work directory. It contains `shared/cases`, `shared/controls`, `shared/baseline`, and the two operational scripts. Your evidence folder is separate.

**Stop:** A command fails, a destination already exists, or Python is not the verified 3.12-or-newer interpreter.

**Recovery:** Keep the existing attempt. Correct the prerequisite through setup, then repeat this block with a new `RUN`; do not reset the checkout or delete an old work folder.

## Freeze your rule and input identities

In your editor, open `W/shared/controls/policy.json` and the three adjacent batch manifests. A manifest names which existing brief the evaluator will read; it is not evidence that a model generated that brief. The policy declares forty case IDs, the three material rows, both gates, no exclusions, and `any_violation_rejects`.

Create `W/decision.md` in your editor. Before opening any candidate, state what would reject either candidate, what counts as a failed case, and why a faster result cannot excuse an unsupported material claim. Do not enter an adoption decision yet.

Freeze the bytes without displaying the candidate contents. The record includes the policy, manifests, cases, gates, instructions, and restore copies.

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" -c "import hashlib,json,sys; from pathlib import Path; w=Path(sys.argv[1]); files=sorted(p for p in (w/'shared').rglob('*') if p.is_file() and p.suffix in ('.json','.md','.py')); hashes={p.relative_to(w).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}; f=Path(sys.argv[2]).open('x',encoding='utf-8'); json.dump({'rule':'any_violation_rejects','sha256':hashes},f,indent=2); f.close(); print('FROZEN',len(hashes),'input/control files')" "$W" "$E/pre-result.json"
```

**Terminal: PowerShell, ordinary user.**

```powershell
& $PY -c "import hashlib,json,sys; from pathlib import Path; w=Path(sys.argv[1]); files=sorted(p for p in (w/'shared').rglob('*') if p.is_file() and p.suffix in ('.json','.md','.py')); hashes={p.relative_to(w).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}; f=Path(sys.argv[2]).open('x',encoding='utf-8'); json.dump({'rule':'any_violation_rejects','sha256':hashes},f,indent=2); f.close(); print('FROZEN',len(hashes),'input/control files')" "$W" "$E\pre-result.json"
```

**Expected:** `E/pre-result.json` contains the identities of the files you are about to compare. Your decision rule was recorded before outcomes.

**Stop:** The record already exists, an input is missing, or you have already selected cases based on their results.

**Recovery:** Preserve the first attempt and begin a new one. A new filename does not turn a post-result decision rule into a pre-result rule.

## Check the baseline, then evaluate every pair

Each case has `sources.json`, a three-row form, and baseline/A/B briefs. The two source-backed gates check each value and its own locator. A zone word elsewhere cannot repair an unlabeled clock value. A number is not wrong merely because it appeared in a previous failure; its source support decides.

Run every baseline first. Both shell versions retain a failure even if a later case passes.

**Terminal: Bash or zsh, ordinary user.**

```bash
baseline_failed=0
for case_dir in "$W"/shared/cases/PC-*; do
  "$PY" "$W/shared/controls/hard_gates.py" "$case_dir/baseline.md" || baseline_failed=1
done
[ "$baseline_failed" -eq 0 ]
```

**Terminal: PowerShell, ordinary user.**

```powershell
$baselineFailed = $false
foreach ($caseDir in Get-ChildItem "$W\shared\cases" -Directory) {
  & $PY "$W\shared\controls\hard_gates.py" "$($caseDir.FullName)\baseline.md"
  if ($LASTEXITCODE -ne 0) { $baselineFailed = $true }
}
if ($baselineFailed) { throw 'A baseline failed; do not evaluate adoption.' }
```

**Expected:** All forty baseline checks pass. This establishes a usable reference, not a claim that either candidate is good.

**Stop:** Any baseline holds or the loop cannot read all cases.

**Recovery:** Save the failed output. Check the named input against your frozen record; do not hand-repair a brief to force a passing baseline.

Now run the supplied evaluator from any directory.

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" "$W/scripts/evaluate_pairs.py" "$W/shared/cases" "$W/shared/controls/policy.json" "$W/out/results.csv"
```

**Terminal: PowerShell, ordinary user.**

```powershell
& $PY "$W\scripts\evaluate_pairs.py" "$W\shared\cases" "$W\shared\controls\policy.json" "$W\out\results.csv"
```

**Expected:** `EVALUATED 120` means all forty cases have a baseline, A, and B row. It does not mean the candidates passed. Open `W/out/results.csv` in your editor or a spreadsheet. Inspect `format_ok`, `mass_gate`, `zone_gate`, `passed`, `reason`, and the three identity columns.

**Stop:** A case is missing, an identity differs, the evaluator holds, or the output destination already exists.

**Recovery:** Preserve the output and error. Resolve the input problem before starting a fresh attempt. Do not drop the difficult case or replace a previous result.

## Make the bounded adoption decision

For each failed row, open that brief and its adjacent `sources.json`. Trace the material value to its exact authoritative locator. Record the case, candidate, gate, and source evidence in `decision.md`. Apply your original rule even if most cases pass.

For each candidate, report the number of distinct cases requiring repair. Keep that **cost proxy** separate from measured time, tokens, and money. These authored outputs provide no observed API cost or model-to-model superiority evidence.

Check that your frozen inputs still match before accepting the comparison.

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" -c "import hashlib,json,sys; from pathlib import Path; w=Path(sys.argv[1]); record=json.loads(Path(sys.argv[2]).read_text()); changed=[name for name,digest in record['sha256'].items() if hashlib.sha256((w/name).read_bytes()).hexdigest()!=digest]; print('FROZEN IDENTITY PASS' if not changed else 'HOLD: '+', '.join(changed)); sys.exit(bool(changed))" "$W" "$E/pre-result.json"
```

**Terminal: PowerShell, ordinary user.**

```powershell
& $PY -c "import hashlib,json,sys; from pathlib import Path; w=Path(sys.argv[1]); record=json.loads(Path(sys.argv[2]).read_text()); changed=[name for name,digest in record['sha256'].items() if hashlib.sha256((w/name).read_bytes()).hexdigest()!=digest]; print('FROZEN IDENTITY PASS' if not changed else 'HOLD: '+', '.join(changed)); sys.exit(bool(changed))" "$W" "$E\pre-result.json"
```

**Expected:** `FROZEN IDENTITY PASS` supports comparison under the recorded inputs and rule. Your decision cites the actual failures without averaging them away.

**Stop:** The identity check fails or the decision depends on a rule changed after inspection.

**Recovery:** Hold adoption and retain the mismatch. Repair the process in a new attempt, not the already observed result.

## Demonstrate restoration

Select the checked instruction as the active condition, retaining the previous active file, then invoke the supplied restore. This deliberately changes a control; it does not edit a candidate brief.

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" -c "from pathlib import Path; import sys; w=Path(sys.argv[1]); active=w/'shared/controls/active-instruction.md'; backup=Path(sys.argv[2]).open('xb'); backup.write(active.read_bytes()); backup.close(); active.write_bytes((w/'shared/controls/candidate-checked-instruction.md').read_bytes())" "$W" "$E/active-before-selection.md" &&
"$PY" "$W/scripts/restore_baseline.py" "$W" &&
"$PY" "$W/scripts/evaluate_pairs.py" "$W/shared/cases" "$W/shared/controls/policy.json" "$W/out/restored-results.csv" &&
"$PY" -c "from pathlib import Path; import sys; w=Path(sys.argv[1]); same=(w/'out/results.csv').read_bytes()==(w/'out/restored-results.csv').read_bytes(); print('RESTORED RESULTS MATCH' if same else 'HOLD: results differ'); sys.exit(not same)" "$W"
```

**Terminal: PowerShell, ordinary user.**

```powershell
& $PY -c "from pathlib import Path; import sys; w=Path(sys.argv[1]); active=w/'shared/controls/active-instruction.md'; backup=Path(sys.argv[2]).open('xb'); backup.write(active.read_bytes()); backup.close(); active.write_bytes((w/'shared/controls/candidate-checked-instruction.md').read_bytes())" "$W" "$E\active-before-selection.md"
if ($LASTEXITCODE -ne 0) { throw 'Selection stopped; preserve the attempt.' }
& $PY "$W\scripts\restore_baseline.py" "$W"
if ($LASTEXITCODE -ne 0) { throw 'Restore held; do not continue.' }
& $PY "$W\scripts\evaluate_pairs.py" "$W\shared\cases" "$W\shared\controls\policy.json" "$W\out\restored-results.csv"
if ($LASTEXITCODE -ne 0) { throw 'Restored evaluation held.' }
& $PY -c "from pathlib import Path; import sys; w=Path(sys.argv[1]); same=(w/'out/results.csv').read_bytes()==(w/'out/restored-results.csv').read_bytes(); print('RESTORED RESULTS MATCH' if same else 'HOLD: results differ'); sys.exit(not same)" "$W"
```

**Expected:** `RESTORE OK` follows hash and byte checks of the active instruction and all forty baseline briefs. The second evaluation matches the first byte for byte; candidate attempts remain intact.

**Stop:** The frozen restore source changed, any restore check holds, or comparison bytes differ.

**Recovery:** Preserve both results and the control backup. Do not reconstruct a baseline from memory or patch a candidate. Start a fresh prepared copy only after recording what broke.

In `W/handoff.md`, name the frozen policy record, comparison results, your adoption decision, the repair proxy, and restore evidence. State the limit: a deterministic comparison of supplied briefs does not measure how a live instruction behaves over repeated runs.

<details markdown="1">
<summary>Optional stretch: separate an instruction effect from ordinary variation</summary>

## Preregister and run the live comparison

Compare the supplied baseline and checked instructions on PC-01–PC-06. Use three fresh repeats per instruction and case, alternating order. After those 36 calls, restore the baseline and run two fresh controls on PC-01 and PC-02. Do not choose replacements after seeing results.

Open both instruction files in your editor. Explain the single added check and predict where it might help, do nothing, or add work. Record that prediction in `decision.md` before running. Keep the model, source/form pair, prompt, and permissions fixed within each pair.

This is paid work. Use only your process-local OpenRouter key and the pinned Sonnet model from setup, with the provider-side per-key spending ceiling set to US$40. The runner cannot verify your account's ceiling. It runs one call at a time, never retries a failed call, and never changes the provider or model. Missing key, credit, model availability, or budget leaves this lane blocked; it is not a reason to substitute a provider.

The source-only runner freezes the schedule and identities before the first call. Each model attempt receives only `sources.json` and `form.md`, with permission to create `brief.md`. The launcher, not the batch runner, creates each receipt directory.

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" "$M/scripts/stretch_runner.py" "$W" "$E/live-comparison"
```

**Terminal: PowerShell, ordinary user.**

```powershell
& $PY "$M\scripts\stretch_runner.py" "$W" "$E\live-comparison"
```

**Expected:** With all prerequisites available, 38 independently checked attempts produce `comparison.json`, `attempts.csv`, raw receipts, tool-written briefs, and `restore.json`. `COMPLETE` means all planned observations exist, not that the checked instruction won. Without the key, the runner exits 2 before creating comparison attempts or contacting a provider.

**Stop:** Any call is incomplete, a frozen identity changes, restoration fails, the provider rejects a request, or the spending ceiling stops work. A content-gate failure is an observation to retain, not an instruction to retry until the answer passes.

**Recovery:** Preserve the entire comparison, including its first failure. Restore the missing prerequisite before considering a new preregistered attempt. Do not merge favorable rows from different attempts, exclude failures, or raise the spending ceiling to finish.

## Interpret the paired observations

Open `comparison.json` and `attempts.csv`. For each case, compare the three baseline outcomes with the three checked outcomes. Report paired disagreements and variation within each instruction, not just pooled averages. Any single checked-instruction violation rejects adoption under the frozen rule. No observed improvement is a valid result.

Report the failed-case repair proxy separately from wall time, raw usage, and SDK-estimated currency. Provider-billed cost remains unknown unless you independently observe it in your account; do not rename an SDK estimate as a bill. Inspect the two restored controls and the actual restored instruction hash.

Your stretch conclusion should explain what these six cases support, what they do not establish, and what uncertainty remains. A completed model comparison does not certify a human operator or establish general superiority.

</details>


Continue with [Module 8 · Constrain agent behavior](../../module-08-agent-safeguards/README.md).
