import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const p7Root = process.env.P7_WORKBOOK_ROOT
  ? path.resolve(process.env.P7_WORKBOOK_ROOT)
  : path.resolve(scriptDir, "..");
const inputsDir = path.join(p7Root, "inputs");
const assetsDir = path.resolve(p7Root, "../../site/assets/blocks/p7");
const qaDir = path.resolve(p7Root, "../../outputs/p7_spreadsheet_workbook_20260805");

const resultHeaders = [
  "workstream",
  "priority",
  "summary",
  "next_action",
  "branch_policy",
  "policy_value",
  "sla_hours",
  "target_by",
];

const sourceWidths = [13, 29, 20, 12, 66, 9];
const resultWidths = [18, 11, 31, 42, 32, 57, 12, 27];

function combineCsv(wave1Text, wave2Text) {
  const secondWaveRows = wave2Text.trim().split(/\r?\n/).slice(1);
  return `${wave1Text.trim()}\n${secondWaveRows.join("\n")}\n`;
}

async function buildWorkbook(
  csvText,
  rowCount,
  templateName,
  previewName,
  previewRange = "A1:N7",
) {
  const workbook = await Workbook.fromCSV(csvText, { sheetName: "AI Workboard" });
  const sheet = workbook.worksheets.getItem("AI Workboard");
  const lastRow = rowCount + 1;

  sheet.getRange("G1:N1").values = [resultHeaders];
  sheet.getRange(`G2:N${lastRow}`).values = Array.from(
    { length: rowCount },
    () => Array(8).fill(null),
  );

  const table = sheet.tables.add(`A1:N${lastRow}`, true, "AIWorkboardTable");
  table.style = "TableStyleMedium2";
  table.showFilterButton = true;
  table.showBandedColumns = false;

  sheet.showGridLines = false;
  sheet.freezePanes.freezeRows(1);
  sheet.freezePanes.freezeColumns(2);

  const used = sheet.getRange(`A1:N${lastRow}`);
  used.format = {
    font: { name: "Aptos", size: 10, color: "#24272C" },
    verticalAlignment: "top",
  };
  sheet.getRange(`A2:N${lastRow}`).format = {
    wrapText: true,
    rowHeight: 38,
    verticalAlignment: "top",
    borders: { preset: "all", style: "thin", color: "#D9DCE1" },
  };
  sheet.getRange(`G2:N${lastRow}`).format = {
    fill: "#FFF4F2",
    wrapText: true,
    verticalAlignment: "top",
    borders: { preset: "all", style: "thin", color: "#E4C9C4" },
  };
  sheet.getRange(`B2:B${lastRow}`).format.numberFormat = 'yyyy-mm-dd"T"hh:mm:ss"Z"';
  sheet.getRange("A1:F1").format = {
    fill: "#20242A",
    font: { name: "Aptos", size: 10, bold: true, color: "#FFFFFF" },
    rowHeight: 32,
    verticalAlignment: "center",
  };
  sheet.getRange("G1:N1").format = {
    fill: "#B42318",
    font: { name: "Aptos", size: 10, bold: true, color: "#FFFFFF" },
    rowHeight: 32,
    verticalAlignment: "center",
  };

  sourceWidths.forEach((width, index) => {
    sheet.getRangeByIndexes(0, index, lastRow, 1).format.columnWidth = width;
  });
  resultWidths.forEach((width, index) => {
    sheet.getRangeByIndexes(0, index + 6, lastRow, 1).format.columnWidth = width;
  });

  await fs.mkdir(inputsDir, { recursive: true });
  await fs.mkdir(assetsDir, { recursive: true });
  await fs.mkdir(qaDir, { recursive: true });

  const xlsx = await SpreadsheetFile.exportXlsx(workbook);
  await xlsx.save(path.join(inputsDir, templateName));
  await xlsx.save(path.join(qaDir, templateName));

  const preview = await workbook.render({
    sheetName: "AI Workboard",
    range: previewRange,
    scale: 1,
    format: "png",
  });
  const previewBytes = new Uint8Array(await preview.arrayBuffer());
  await fs.writeFile(path.join(assetsDir, previewName), previewBytes);
  await fs.writeFile(path.join(qaDir, previewName), previewBytes);

  const inspection = await workbook.inspect({
    kind: "workbook,sheet,table,region,formula",
    sheetId: "AI Workboard",
    range: `A1:N${Math.min(lastRow, 8)}`,
    maxChars: 9000,
    tableMaxRows: 8,
    tableMaxCols: 14,
    options: { maxResults: 100 },
  });
  await fs.writeFile(
    path.join(qaDir, `${templateName}.inspection.txt`),
    `${inspection.ndjson ?? String(inspection)}\n`,
    "utf8",
  );

  // artifact-tool may emit a detailed inspect sidecar beside each exported XLSX.
  // Keep the bounded QA report above, not the multi-hundred-kilobyte sidecars.
  await fs.rm(path.join(inputsDir, `${templateName}.inspect.ndjson`), { force: true });
  await fs.rm(path.join(qaDir, `${templateName}.inspect.ndjson`), { force: true });

  return { templateName, rowCount, inspection: inspection.ndjson ?? String(inspection) };
}

const wave1Text = await fs.readFile(path.join(inputsDir, "wave1.csv"), "utf8");
const wave2Text = await fs.readFile(path.join(inputsDir, "wave2.csv"), "utf8");

const results = [];
results.push(
  await buildWorkbook(
    wave1Text,
    60,
    "workboard_60_blank.xlsx",
    "p7-workboard-60-blank.png",
  ),
);
results.push(
  await buildWorkbook(
    combineCsv(wave1Text, wave2Text),
    80,
    "workboard_80_blank.xlsx",
    "p7-workboard-80-blank.png",
    "A75:N81",
  ),
);

for (const result of results) {
  if (/#[A-Z0-9/]+[!?]?\b/.test(result.inspection)) {
    throw new Error(`${result.templateName} contains a spreadsheet formula error`);
  }
  console.log(`BUILT ${result.templateName}: ${result.rowCount} source rows, 8 blank AI columns`);
}
console.log(`QA ${qaDir}`);
