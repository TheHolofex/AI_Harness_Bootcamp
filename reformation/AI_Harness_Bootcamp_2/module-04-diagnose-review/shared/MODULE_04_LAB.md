# Module 4 · Diagnose and recover

When a duty card drops a field, you need to locate the loss before changing anything. You will preserve the first miss, replace only the faulty renderer, and prove recovery without relying on the original process or working directory.

The case is fictional. Your work stays inside the class. You are not planning or authorizing a real movement.

## Prepare a separate attempt

Use the verified Python and checkout from setup. Open an ordinary terminal. These commands work from any directory and leave earlier attempts intact. `W` is your work folder; `E` holds your records outside it.

**Terminal: Bash or zsh, ordinary user.**

```bash
R="$HOME/AI_Harness_Bootcamp"
PY="$(for candidate in python3.12 python3 python; do "$candidate" -c 'import sys; sys.exit(1) if sys.version_info < (3, 12) else print(sys.executable)' 2>/dev/null && break; done)"
M="$R/reformation/AI_Harness_Bootcamp_2/module-04-diagnose-review"
RUN="$(date -u +%Y%m%dT%H%M%SZ)-$$"
W="$HOME/course-evidence/module-04-$RUN/work"
E="$HOME/course-evidence/module-04-$RUN/evidence"
"$PY" "$R/reformation/shared/prepare_work.py" 04 "$W" &&
"$PY" -c "from pathlib import Path; import sys; Path(sys.argv[1]).mkdir(parents=True, exist_ok=False)" "$E"
```

**Terminal: PowerShell, ordinary user.**

```powershell
$R = "$HOME\AI_Harness_Bootcamp"
$PY = $(foreach ($candidate in 'python3.12','python3','python') { try { $resolved = & $candidate -c 'import sys; sys.exit(1) if sys.version_info < (3,12) else print(sys.executable)' 2>$null; if ($LASTEXITCODE -eq 0 -and $resolved) { $resolved.Trim(); break } } catch {} })
if (-not $PY) { throw 'No Python >= 3.12 found' }
$M = "$R\reformation\AI_Harness_Bootcamp_2\module-04-diagnose-review"
$RUN = [guid]::NewGuid().ToString('N')
$W = "$HOME\course-evidence\module-04-$RUN\work"
$E = "$HOME\course-evidence\module-04-$RUN\evidence"
& $PY "$R\reformation\shared\prepare_work.py" 04 "$W"
if ($LASTEXITCODE -ne 0) { throw 'Preparation stopped; preserve this attempt.' }
& $PY -c "from pathlib import Path; import sys; Path(sys.argv[1]).mkdir(parents=True, exist_ok=False)" "$E"
```

**Expected:** The preparer prints `PASS: created` followed by the absolute work path. `W` contains `scripts/render_review.py`, `scripts/restore.py`, `baseline/`, `shared/case/ledger.json` (and the stretch ledgers), and an empty `out/` directory. `E` is a sibling evidence directory.

**Stop:** A command fails, a destination already exists, Python is not the verified 3.12-or-newer interpreter, or you already followed the preparer's suggested route command and created a review.

**Recovery:** Keep the existing attempt. Correct the prerequisite through setup, then repeat this block with a new `RUN`. Do not reset the checkout or delete an old work folder.

If you open a new terminal later, repeat only the variable assignments. Do not prepare a second folder unless this attempt has stopped.

The prepare script prints a suggested next command. Do not run it yet.


## 1. Confirm the clean render

From any shell with the variables set, render the duty card using the explicit ledger path.

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" "$W/scripts/render_review.py" "$W/shared/case/ledger.json" "$W/out/baseline.md"
```

**Terminal: PowerShell, ordinary user.**

```powershell
& $PY "$W\scripts\render_review.py" "$W\shared\case\ledger.json" "$W\out\baseline.md"
```

Open `$W/out/baseline.md`. It must contain both `permit_status` and `gate_time_mdt`, plus current_rows and near_miss_ids.

**Expected:** Both required fields are present, and the card shows the scanned quantity and near-miss count.

**Stop:** Either field is missing or the command fails with HOLD.

**Recovery:** Confirm the variables and that `ledger.json` exists under `W`. Keep any output already written; use a new output filename when you repeat the command.

Read the one-page duty card for the rules:

[shared/case/DUTY_CARD.md](case/DUTY_CARD.md)

## 2. Verify restore before any swap

Restore copies the baseline renderer onto the work copy only after the digest matches and preserves any prior failed renderer and out/ into attempts/.

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" "$W/scripts/restore.py" "$W"
```

**Terminal: PowerShell, ordinary user.**

```powershell
& $PY "$W\scripts\restore.py" "$W"
```

**Expected:** RESTORE OK is printed and the scripts/render_review.py bytes now match the baseline.

**Stop:** RESTORE OK is not printed or the files differ.

**Recovery:** Do not continue. Record the error and start with a new prepare_work destination.

## 3. Seal the first miss

Ask the facilitator to place the fault using the public source script.

Facilitator command:

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" "$M/scripts/place_practice_fault.py" "$W" --variant A
```

**Terminal: PowerShell, ordinary user.**

```powershell
& $PY "$M\scripts\place_practice_fault.py" "$W" --variant A
```

**Expected:** FAULT PLACED A

From the variables, render with the now-faulty work copy:

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" "$W/scripts/render_review.py" "$W/shared/case/ledger.json" "$W/out/miss.md"
```

**Terminal: PowerShell, ordinary user.**

```powershell
& $PY "$W\scripts\render_review.py" "$W\shared\case\ledger.json" "$W\out\miss.md"
```

Use the read-only probe (run from the source module path so a faulty work copy cannot disable it):

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" "$M/scripts/probe_fields.py" "$W/shared/case/ledger.json" --review "$W/out/miss.md"
```

**Terminal: PowerShell, ordinary user.**

```powershell
& $PY "$M\scripts\probe_fields.py" "$W\shared\case\ledger.json" --review "$W\out\miss.md"
```

Write sealed-first-miss.md before you replace anything:

```markdown
# Sealed first miss

Command:
Observed output (first 20 lines):
Probe output:
  selected_source_ids ...
  review_present yes
  permit_status ...
  gate_time_mdt ...
First missing field:
Still present:
```

**Expected:** The probe identifies renderer_omission (or source_omission for the stretch) for the dropped field. The first missing field matches the variant. The selected_source_ids line shows the renderer-chosen current rows.

**Stop:** You cannot name the earliest missing field from the probe output, or more than one field is affected before localization.

**Recovery:** Record HOLD. Do not replace until the probe has shown a one-way failure on the known miss.

## 4. One authorized replace

Replace only the work-copy renderer from the clean copy. The restore command preserves the failed renderer and out/ in attempts/ first.

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" "$W/scripts/restore.py" "$W"
```

**Terminal: PowerShell, ordinary user.**

```powershell
& $PY "$W\scripts\restore.py" "$W"
```

Write replace-record.md with the command and the RESTORE OK line.

**Expected:** RESTORE OK and the work copy now matches the baseline bytes.

**Stop:** More than one change, or the replace happens before the miss is sealed.

**Recovery:** Record the error. Start over with a fresh prepare_work destination.

## 5. Prove recovery three ways

Prove the repair in three distinct ways. A repository-only clean render is not enough. Use the required-field probe as the focused check, a complete named render, and a fresh-folder fresh-process run from an unrelated cwd.

1. Focused (required-field probe after restore):

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" "$W/scripts/render_review.py" "$W/shared/case/ledger.json" "$W/out/focused.md" &&
"$PY" "$M/scripts/probe_fields.py" "$W/shared/case/ledger.json" --review "$W/out/focused.md"
```

**Terminal: PowerShell, ordinary user.**

```powershell
& $PY "$W\scripts\render_review.py" "$W\shared\case\ledger.json" "$W\out\focused.md"
if ($LASTEXITCODE -ne 0) { throw 'Focused render held.' }
& $PY "$M\scripts\probe_fields.py" "$W\shared\case\ledger.json" --review "$W\out\focused.md"
```

2. Complete render (full explicit from W):

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" "$W/scripts/render_review.py" "$W/shared/case/ledger.json" "$W/out/complete.md"
```

**Terminal: PowerShell, ordinary user.**

```powershell
& $PY "$W\scripts\render_review.py" "$W\shared\case\ledger.json" "$W\out\complete.md"
```

3. Fresh-process (unrelated cwd, fresh dir, fresh process):

**Terminal: Bash or zsh, ordinary user.**

```bash
FRESH="$HOME/course-evidence/module-04-$RUN/fresh"
"$PY" -c "
from pathlib import Path
import sys
p = Path(sys.argv[1])
if p.exists() or p.is_symlink(): sys.exit(1)
p.mkdir(parents=True)
" "$FRESH" &&
cp "$W/scripts/render_review.py" "$FRESH/" &&
cp "$W/shared/case/ledger.json" "$FRESH/" &&
cd "$HOME" &&
"$PY" "$FRESH/render_review.py" "$FRESH/ledger.json" "$FRESH/review.md"
```

**Terminal: PowerShell, ordinary user.**

```powershell
$FRESH = "$HOME\course-evidence\module-04-$RUN\fresh"
& $PY -c "
from pathlib import Path
import sys
p = Path(sys.argv[1])
if p.exists() or p.is_symlink(): sys.exit(1)
p.mkdir(parents=True)
" "$FRESH"
if ($LASTEXITCODE -ne 0) { throw 'Fresh dir exists.' }
Copy-Item "$W\scripts\render_review.py" "$FRESH\"
Copy-Item "$W\shared\case\ledger.json" "$FRESH\"
Set-Location "$HOME"
& $PY "$FRESH\render_review.py" "$FRESH\ledger.json" "$FRESH\review.md"
```

**Expected:** The focused probe reports both fields as `rendered`. The complete and fresh review files contain both `permit_status` and `gate_time_mdt`. The fresh run used a new directory and an unrelated working directory. A probe exit of 0 means the diagnosis completed; read its field classifications rather than treating that exit as a completeness check.

**Stop:** Any proof is missing a required field or the restore was not re-proved.

**Recovery:** Keep the failed output. Correct the diagnosed path problem and use unused output names for another proof. If you need another renderer replacement, start a fresh attempt rather than erase the first intervention.

Save the three outputs (including the focused probe result) and the sealed miss.

Confirm that quoting also works when your work path contains a space. This separate check preserves your original attempt. Render the baseline before testing restore: restore needs an actual output to preserve.

**Terminal: Bash or zsh, ordinary user.**

```bash
SPACE_WORK="$HOME/course-evidence/module-04-$RUN/work with space"
"$PY" "$R/reformation/shared/prepare_work.py" 04 "$SPACE_WORK" &&
"$PY" "$SPACE_WORK/scripts/render_review.py" "$SPACE_WORK/shared/case/ledger.json" "$SPACE_WORK/out/baseline.md" &&
"$PY" "$SPACE_WORK/scripts/restore.py" "$SPACE_WORK" &&
"$PY" "$SPACE_WORK/scripts/render_review.py" "$SPACE_WORK/shared/case/ledger.json" "$SPACE_WORK/out/focused.md" &&
"$PY" "$M/scripts/probe_fields.py" "$SPACE_WORK/shared/case/ledger.json" --review "$SPACE_WORK/out/focused.md"
```

**Terminal: PowerShell, ordinary user.**

```powershell
$SPACE_WORK = "$HOME\course-evidence\module-04-$RUN\work with space"
& $PY "$R\reformation\shared\prepare_work.py" 04 "$SPACE_WORK"
if ($LASTEXITCODE -ne 0) { throw 'Spaced work preparation held.' }
& $PY "$SPACE_WORK\scripts\render_review.py" "$SPACE_WORK\shared\case\ledger.json" "$SPACE_WORK\out\baseline.md"
if ($LASTEXITCODE -ne 0) { throw 'Baseline render held.' }
& $PY "$SPACE_WORK\scripts\restore.py" "$SPACE_WORK"
if ($LASTEXITCODE -ne 0) { throw 'Restore held.' }
& $PY "$SPACE_WORK\scripts\render_review.py" "$SPACE_WORK\shared\case\ledger.json" "$SPACE_WORK\out\focused.md"
if ($LASTEXITCODE -ne 0) { throw 'Focused render held.' }
& $PY "$M\scripts\probe_fields.py" "$SPACE_WORK\shared\case\ledger.json" --review "$SPACE_WORK\out\focused.md"
```

**Expected:** Preparation and both renders succeed, restore prints `RESTORE OK`, and the probe reports both fields as `rendered`.

**Stop:** Any command holds or either field is absent.

**Recovery:** Preserve this directory. Correct the named problem, then choose a new spaced destination rather than reuse an existing output.

## 6. Finish the handoff

Write handoff.md:

```markdown
# Module 4 handoff

First missing field:
Probe output that showed it:
  (include selected_source_ids, review_present, and the cause line)
Replace command:
Focused probe result:
Complete render file:
Fresh-process rerun file:
What the next person should inspect first:
```

A classmate who did not watch you work should be able to reconstruct the result without coaching.

## Stretch: competing causes on a second case

<details markdown="1">
<summary>Optional stretch: distinguish source omission, wrong input version, and renderer omission</summary>

Separate missing source evidence from the wrong input version and a renderer that drops a supplied field. Before running these checks, write your predicted cause and the evidence that would distinguish it in `E/stretch-prediction.md`. Keep the core evidence unchanged.

### Inspect missing source evidence

Use the clean renderer with the supplied second ledger. If the renderer holds, inspect the selected source rows with the probe; do not fill a source gap by changing code.

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" "$W/scripts/render_review.py" "$W/shared/case/ledger-stretch.json" "$W/out/source-omission.md"
SOURCE_EXIT=$?
if [ "$SOURCE_EXIT" -eq 1 ]; then
  "$PY" "$M/scripts/probe_fields.py" "$W/shared/case/ledger-stretch.json"
else
  printf '%s\n' 'HOLD: expected a malformed-source refusal; inspect the actual result.'
  false
fi
```

**Terminal: PowerShell, ordinary user.**

```powershell
& $PY "$W\scripts\render_review.py" "$W\shared\case\ledger-stretch.json" "$W\out\source-omission.md"
if ($LASTEXITCODE -ne 1) { throw 'Expected a malformed-source refusal; inspect the actual result.' }
& $PY "$M\scripts\probe_fields.py" "$W\shared\case\ledger-stretch.json"
```

**Expected:** The renderer reports `HOLD: malformed input`. The probe reports `source_omission` and the selected row IDs with missing values.

**Stop:** The renderer accepts the incomplete source, or you cannot locate the missing values in the named rows.

**Recovery:** Keep the refusal and probe output. Obtain complete source evidence from its owner; restoring a renderer cannot create it.

### Compare the intended input

Check the stale ledger against the supplied intended ledger. Source IDs and their revisions identify the selected inputs; matching IDs alone do not establish matching versions.

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" "$M/scripts/probe_fields.py" "$W/shared/case/ledger-stale.json" --intended "$W/shared/case/ledger-intended.json"
```

**Terminal: PowerShell, ordinary user.**

```powershell
& $PY "$M\scripts\probe_fields.py" "$W\shared\case\ledger-stale.json" --intended "$W\shared\case\ledger-intended.json"
```

**Expected:** The probe reports `wrong_input_version` and prints both selections and their revisions.

**Stop:** You cannot explain which intended source replaces the stale selection.

**Recovery:** Record the input-selection error and identify the correct snapshot. Do not replace a working renderer to conceal a wrong input.

### Localize the other renderer omission

The main ledger supplies both fields. Place variant B, render to a new name, and inspect its first omission before authorizing a replacement.

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" "$M/scripts/place_practice_fault.py" "$W" --variant B &&
"$PY" "$W/scripts/render_review.py" "$W/shared/case/ledger.json" "$W/out/stretch-miss.md" &&
"$PY" "$M/scripts/probe_fields.py" "$W/shared/case/ledger.json" --review "$W/out/stretch-miss.md"
```

**Terminal: PowerShell, ordinary user.**

```powershell
& $PY "$M\scripts\place_practice_fault.py" "$W" --variant B
if ($LASTEXITCODE -ne 0) { throw 'Fault placement held.' }
& $PY "$W\scripts\render_review.py" "$W\shared\case\ledger.json" "$W\out\stretch-miss.md"
if ($LASTEXITCODE -ne 0) { throw 'Stretch render held.' }
& $PY "$M\scripts\probe_fields.py" "$W\shared\case\ledger.json" --review "$W\out\stretch-miss.md"
```

**Expected:** One field is `renderer_omission`; the other is `rendered`. Seal this miss and the source support in `E/sealed-stretch-miss.md` before continuing.

**Stop:** More than one field is missing, or the selected source does not supply the omitted value.

**Recovery:** Preserve the observations and diagnose the earlier cause. Do not replace anything until the evidence isolates this renderer.

### Prove the second recovery without overwriting the first

Authorize one baseline replacement for the sealed variant-B miss. Use new output names and a new fresh-process directory for its three proofs.

**Terminal: Bash or zsh, ordinary user.**

```bash
"$PY" "$W/scripts/restore.py" "$W" &&
"$PY" "$W/scripts/render_review.py" "$W/shared/case/ledger.json" "$W/out/stretch-focused.md" &&
"$PY" "$M/scripts/probe_fields.py" "$W/shared/case/ledger.json" --review "$W/out/stretch-focused.md" &&
"$PY" "$W/scripts/render_review.py" "$W/shared/case/ledger.json" "$W/out/stretch-complete.md"
```

**Terminal: PowerShell, ordinary user.**

```powershell
& $PY "$W\scripts\restore.py" "$W"
if ($LASTEXITCODE -ne 0) { throw 'Stretch restore held.' }
& $PY "$W\scripts\render_review.py" "$W\shared\case\ledger.json" "$W\out\stretch-focused.md"
if ($LASTEXITCODE -ne 0) { throw 'Stretch focused render held.' }
& $PY "$M\scripts\probe_fields.py" "$W\shared\case\ledger.json" --review "$W\out\stretch-focused.md"
if ($LASTEXITCODE -ne 0) { throw 'Stretch probe held.' }
& $PY "$W\scripts\render_review.py" "$W\shared\case\ledger.json" "$W\out\stretch-complete.md"
```

**Expected:** Restore succeeds, the focused probe reports both fields as `rendered`, and the complete output contains both values.

**Stop:** Any command holds or either field is absent.

**Recovery:** Preserve the failed proof and choose unused names for a justified new attempt. Never overwrite the core proof files.

**Terminal: Bash or zsh, ordinary user.**

```bash
FRESH="$HOME/course-evidence/module-04-$RUN/fresh-stretch"
"$PY" -c "from pathlib import Path; import sys; Path(sys.argv[1]).mkdir(parents=True, exist_ok=False)" "$FRESH" &&
cp "$W/scripts/render_review.py" "$FRESH/" &&
cp "$W/shared/case/ledger.json" "$FRESH/" &&
cd "$HOME" &&
"$PY" "$FRESH/render_review.py" "$FRESH/ledger.json" "$FRESH/review.md"
```

**Terminal: PowerShell, ordinary user.**

```powershell
$FRESH = "$HOME\course-evidence\module-04-$RUN\fresh-stretch"
& $PY -c 'from pathlib import Path; import sys; Path(sys.argv[1]).mkdir(parents=True, exist_ok=False)' "$FRESH"
if ($LASTEXITCODE -ne 0) { throw 'Fresh stretch destination already exists.' }
Copy-Item "$W\scripts\render_review.py" "$FRESH\" -ErrorAction Stop
Copy-Item "$W\shared\case\ledger.json" "$FRESH\" -ErrorAction Stop
Set-Location -LiteralPath $HOME -ErrorAction Stop
& $PY "$FRESH\render_review.py" "$FRESH\ledger.json" "$FRESH\review.md"
```

**Expected:** The new process produces a review with both fields while using only the copied renderer and ledger, from an unrelated working directory.

**Stop:** The destination exists or the copied run fails.

**Recovery:** Keep the failed directory and use a new destination after correcting the diagnosed cause. Record which source or renderer change each of the three cases actually justified; a successful replacement in one case is not a remedy for all three.

</details>

## Before you stop

Check that:

- restore printed RESTORE OK before the first swap;
- the sealed miss names exactly one earliest field using the probe output on selected rows;
- only one authorized replace was made;
- the focused proof used the probe to confirm the fields on the work-copy render, the complete render, and the fresh-process output from a new unrelated directory all show both fields;
- the work remains inside the fictional class case;

Keep the sealed misses, the source selections, each authorized replacement record, and all three recovery proofs. The next owner should be able to distinguish a source gap, a wrong version, and a dropped display field without your explanation.

Continue with [Blue Gauge](../../module-05-run-corpus/README.md).
