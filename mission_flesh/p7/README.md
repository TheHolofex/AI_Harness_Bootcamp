# P7 — AI Controls the Workboard

This fixture makes the spreadsheet the operating surface:

```text
workboard.xlsx → n8n reads AI Workboard → AI fills eight columns
→ four policy branches → n8n writes workboard.xlsx back
```

Wave 1 starts with 60 source rows and eight blank AI/policy columns. The first run fills the workbook. One edit in the Operations branch changes every matching spreadsheet row from a 24-hour SLA to an 8-hour SLA. Wave 2 replaces the active workbook with an 80-row template; the same saved graph fills all 80 rows.

No Google Sheets or Microsoft 365 credential is required. n8n reads and writes the local XLSX file. The only external credential is the funded xAI model.

## The workbook contract

The active workbook is:

```text
mission_flesh\p7\workboard.xlsx
```

The sheet name is **AI Workboard**. Its columns are:

```text
id, received_at, requester, channel, text, wave,
workstream, priority, summary, next_action,
branch_policy, policy_value, sla_hours, target_by
```

The first six columns are source data. n8n writes the last eight.

**Close Excel before every n8n execution.** Excel can lock the file while it is open, and the final n8n node deliberately overwrites `workboard.xlsx`.

## Prepare Wave 1

From the repository root in Windows PowerShell:

```powershell
.\mission_flesh\p7\scripts\Prepare-P7.ps1
```

The helper:

1. requires the course model in `HB_XAI_MODEL`;
2. copies `inputs\workboard_60_blank.xlsx` to `workboard.xlsx`;
3. clears the known verifier evidence;
4. replaces the local path and model placeholders in the portable workflow;
5. writes `workflow\P7-production-line.json`;
6. sets `N8N_RESTRICT_FILE_ACCESS_TO` for an n8n process started from the same window.

Open `workboard.xlsx` first. Confirm 60 rows, the sheet name **AI Workboard**, and blank cells from `workstream` through `target_by`. Then close Excel.

Start n8n in the same PowerShell window:

```powershell
n8n start
```

Import `workflow\P7-production-line.json`. Open **xAI Model — attach credential here**, select the funded course credential, confirm the model printed by the preparation helper, and save the workflow. The workflow JSON contains no API key.

## Read the visual line

The saved workflow is named **P7 — AI Controls the Workboard**. Read it left to right:

1. **Read workboard.xlsx** reads the local file into n8n's binary field `data`.
2. **Extract AI Workboard sheet** reads XLSX, sheet `AI Workboard`, with the header row and empty cells included.
3. **Map Spreadsheet Rows** keeps the six source columns and normalizes Excel date values.
4. **Group into 5-Record Model Calls** creates 12 model items for Wave 1 or 16 for the 80-row run.
5. **AI Structure Station** asks for workstream, priority, summary, and next action. It runs three calls at a time with a 400 ms delay.
6. **Structured Output Contract** restricts workstream to four values and priority to P1/P2/P3.
7. **Merge Source + AI by ID** returns the AI result to its source row.
8. **Route by Workstream** sends each row through one of four visible policy branches.
9. **Fan In — AI Workboard** recombines the branches.
10. **Convert rows to workboard.xlsx** creates one XLSX sheet named `AI Workboard`.
11. **Write workboard.xlsx — close Excel first** overwrites the active workbook.
12. The same fan-in also writes `out\AI_workboard.csv` and `out\run_receipt.json` for the offline verifier.

The graph groups five source rows per model call. If the classroom key returns `429` or quota wording, change `RECORDS_PER_MODEL_CALL = 5` to `10` in **Group into 5-Record Model Calls**, then set the AI station's batch size to `2` and delay to `1200` ms. That keeps every spreadsheet row while reducing model calls.

## Run and inspect Wave 1

With Excel closed, click **Execute workflow**. When the graph finishes, open `workboard.xlsx`. The eight result columns should now be populated for all 60 rows.

Use Excel's filter control, or select the header row and press **Ctrl+Shift+L**, to inspect one workstream at a time.

Run the verifier:

```powershell
.\mission_flesh\p7\scripts\Verify-P7.ps1
```

The final line starts:

```text
P7 SPREADSHEET CONTROL VERIFIED: 60 rows
```

The CSV and JSON in `out` are verifier evidence. The workbook is the learner-facing product.

## Change one rule across the spreadsheet

After the 24-hour run, close Excel and save a comparison copy:

```powershell
Copy-Item .\mission_flesh\p7\workboard.xlsx .\mission_flesh\p7\out\workboard_24h.xlsx -Force
```

Open **POLICY — Operations SLA 24h**. Change only:

```javascript
const OPERATIONS_SLA_HOURS = 24;
```

to:

```javascript
const OPERATIONS_SLA_HOURS = 8;
```

Save and rerun with Excel closed. Open `out\workboard_24h.xlsx` beside the current `workboard.xlsx`. Filter both sheets to `OPERATIONS`. The same row IDs should show changes in:

- `branch_policy`
- `policy_value`
- `sla_hours`
- `target_by`

No spreadsheet row is edited by hand.

## Reveal Wave 2

Close Excel, then run:

```powershell
.\mission_flesh\p7\scripts\Add-P7Wave2.ps1
```

The helper replaces the active workbook with the immutable 80-row template. Open `workboard.xlsx` long enough to confirm rows `INT-061` through `INT-080` and blank AI columns. Close Excel, then rerun the same saved n8n graph.

Run the verifier again. Its final line starts:

```text
P7 SPREADSHEET CONTROL VERIFIED: 80 rows
```

## Maintainer notes

- `workflow\P7-production-line.template.json` is the portable source. Do not import it directly.
- `inputs\workboard_60_blank.xlsx` and `inputs\workboard_80_blank.xlsx` are immutable workbook fixtures.
- `scripts\build_workbooks.mjs` regenerates those XLSX fixtures and their preview images with the bundled artifact-tool runtime.
- `workboard.xlsx`, `workflow\P7-production-line.json`, and `out\*` are generated run files and are ignored by Git.
- `GROUND_TRUTH.md` records the node APIs and funded Windows/xAI pilot boundary.
- Offline fixture tests use only Python's standard library:

```powershell
python -m unittest discover mission_flesh/p7/tests -v
```
