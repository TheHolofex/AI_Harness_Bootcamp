# Ground Truth: P7 spreadsheet-control fixture

Spec: "Use one visible n8n graph to read a local Excel workbook, structure every work request with AI, route each row through a workstream policy, and write the enriched rows back to the same workbook; change one policy once and watch every matching spreadsheet row change; add 20 rows and rerun the same graph."

Verified on 2026-08-05 before and during implementation:

- Target runtime: `n8n@2.33.4`, with `n8n-nodes-base@2.33.1`, `n8n-workflow@2.33.1`, and `@n8n/n8n-nodes-langchain@2.33.2`. The exact npm packages were inspected locally under `/Users/ravistarzl/.npm/_npx/60548950ea9934f6/node_modules`.
- Workflow import shape: an n8n workflow JSON object with `name`, `id`, `nodes`, `connections`, and `settings`. The generated workflow is checked with `n8n@2.33.4 import:workflow`.
- `n8n-nodes-base.readWriteFile` v1.1 supports local binary file reads through `fileSelector` and writes through `fileName` plus `dataPropertyName`. Windows read selectors use forward slashes after placeholder expansion.
- `n8n-nodes-base.extractFromFile` v1.1 supports `operation: "xlsx"`, binary field `data`, `sheetName`, `range`, `includeEmptyCells`, and `headerRow`. The P7 node reads sheet `AI Workboard`, includes empty result cells, and uses the header row.
- XLSX date cells are emitted by the underlying spreadsheet reader as Excel serial numbers in this configuration. **Map Spreadsheet Rows** therefore normalizes numeric serials with the Excel 1900 epoch before the policy nodes calculate `target_by`.
- `n8n-nodes-base.convertToFile` v1.1 supports `operation: "xlsx"` with binary field name, compression, file name, header row, and sheet name. The P7 node creates one sheet named `AI Workboard`; the downstream local-file node overwrites the active `workboard.xlsx`.
- Local XLSX read and write require no Google, Microsoft, or other spreadsheet-cloud credential. The workbook must be closed in Excel before n8n overwrites it.
- `@n8n/n8n-nodes-langchain.chainLlm` v1.9 supports a defined per-item prompt, structured-output parser input, and batching. P7 uses five source records per model item, batch size 3, and 400 ms between batches.
- `@n8n/n8n-nodes-langchain.lmChatXAiGrok` v1 supports credential type `xAiApi`, a model ID, temperature, retries, token limit, and timeout. P7 uses temperature 0, max tokens 1200, timeout 360000 ms, and two retries. The repository contains no API key.
- `@n8n/n8n-nodes-langchain.outputParserStructured` v1.3 accepts a manual JSON Schema. P7 requires `id`, `workstream`, `priority`, `summary`, and `next_action`; workstream and priority are enumerated.
- `n8n-nodes-base.merge` v3.2 supports combining source and AI items by `id` and a four-input append fan-in.
- `n8n-nodes-base.switch` v3.4 supports four expression-mode outputs. P7 maps `OPERATIONS`, `FINANCE`, `PEOPLE`, and `TECHNOLOGY` to outputs 0–3.
- `n8n-nodes-base.code` v2 supports JavaScript `runOnceForAllItems` and `$input.all()`.
- Workbook fixtures were authored with bundled `@oai/artifact-tool@2.8.39`. The generated files were inspected for the exact `AI Workboard` sheet, 14-column header, 60/80 source row counts, eight blank result columns, tables, frozen panes, distinct source/result styling, and formula errors. Preview PNGs were rendered and visually inspected.
- A disposable n8n 2.33.4 profile proved that the imported workflow, whole-canvas view, and real node parameter panels can be captured in the local editor at 1280×720. The disposable profile contained no funded credential and performed no model execution.

## Assumptions and pilot boundary

- The course pre-work installs the current stable n8n channel rather than a repository-pinned package. This fixture is validated against n8n 2.33.4; a cohort machine on another version still needs one pilot.
- `HB_XAI_MODEL` is populated by pre-work and injected into the generated import file. The learner attaches one local `xAiApi` credential after import.
- Wave 1 makes 12 model calls and the 80-row run makes 16. The documented rate-limit fallback groups ten records, uses batch size 2, and waits 1200 ms.
- Import compatibility, node schemas, local XLSX parsing, workbook authoring, and editor visuals are verified offline. A funded Windows/xAI pilot is still required to confirm current model availability, end-to-end latency and rate limits, structured-output consistency across all batches, PowerShell 5.1 behavior, overwrite behavior while Excel is closed, and the appearance of the final populated workbook.
- The XLSX converter rebuilds the `AI Workboard` sheet from row data; it does not promise to preserve the styled table from the blank fixture. The content and columns are the contract. Learners can enable Excel filtering with **Ctrl+Shift+L** after the run.

## Post-build verification record

Completed 2026-08-06:

- Imported `P7-production-line.template.json` successfully with the n8n 2.33.4 CLI in a disposable profile: `Successfully imported 1 workflow.`
- Passed all 17 tests in `mission_flesh/p7/tests`, including workbook structure, node parameters, JavaScript parsing, policy propagation, writeback, helper contracts, and removal of the old bundle architecture.
- Rebuilt, inspected, and rendered both blank workbook fixtures with `@oai/artifact-tool@2.8.39`. The Wave 1 preview shows the headers and first source rows; the Wave 2 preview shows final IDs `INT-074` through `INT-080` with `wave = 2` and blank result cells.
- Captured 13 real editor screenshots from a disposable local n8n 2.33.4 instance: whole canvas; workbook read/extract; AI prompt, batching, model, and schema; route and Operations policy; merge and fan-in; XLSX conversion and workbook write.
- Passed `node scripts/verify-resources.mjs` with zero warnings and `git diff --check` with no whitespace errors.
- Inspected the rendered lesson in the in-app browser at 1280×720 and 390×844. Both widths had zero page-level horizontal overflow; staged scrolling loaded each figure it reached without error; there were no duplicate IDs, missing in-page anchors, or browser console errors, and the resource verifier resolved all 15 local figure paths. A visible lesson-outcome checkbox changed progress from `0 / 11 · 0%` to `1 / 11 · 9%` and reset correctly.
- A funded model execution was not performed. The Windows/xAI pilot boundary above remains explicit and is not represented as complete.
