import assert from "node:assert/strict";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { Client } from "@modelcontextprotocol/client";
import { StdioClientTransport } from "@modelcontextprotocol/client/stdio";

import { MAX_SPAN_LINES, SERVER_INSTRUCTIONS, TOOL_NAMES } from "./server.mjs";

const moduleDirectory = dirname(fileURLToPath(import.meta.url));
const serverPath = join(moduleDirectory, "server.mjs");
const CORPUS = resolve(moduleDirectory, "../../mission_flesh/tuesday/need/corpus");

const GAUGE = "hydrology/BASIN_GAUGE_SERIES_2022-2026.csv";
const SENSORS = "met/ESTATE_SURFACE_SENSORS_2024-2026.csv";
const FERRY = "movement/MOV-2026-069_ferry_crossing_log.csv";
const RERATING = "engineering/ENG-2026-003_selwyn_bridge_rerating.md";

// 10-25 September, the rotation window.
const WINDOW_DAYS = 16;
const sepWindow = (year) => ({ from: `${year}-09-10`, to: `${year}-09-25` });

let checks = 0;
function check(label, condition, detail = "") {
  checks += 1;
  assert.ok(condition, `${label}${detail ? ` — ${detail}` : ""}`);
  process.stdout.write(`  ok  ${label}\n`);
}

async function withClient(sourceTypes, run) {
  const args = [serverPath, "--root", CORPUS];
  if (sourceTypes) args.push("--source-types", sourceTypes);
  const client = new Client({ name: "northwind-smoke", version: "2.0.0" });
  const transport = new StdioClientTransport({
    command: process.execPath,
    args,
    cwd: moduleDirectory,
    stderr: "pipe",
  });
  let stderr = "";
  transport.stderr?.on("data", (chunk) => {
    stderr += chunk.toString();
  });
  try {
    await client.connect(transport);
    await run(client);
  } finally {
    await client.close().catch(() => {});
    await transport.close().catch(() => {});
  }
  assert.equal(stderr.trim(), "", `server wrote to stderr: ${stderr}`);
}

const call = (client, name, args) => client.callTool({ name, arguments: args });

/* ------------------------------------------------- protocol and surface --- */

async function testSurfaceAndProtocol() {
  process.stdout.write("\nprotocol and surface\n");
  await withClient(null, async (client) => {
    check("instructions are the server's own", client.getInstructions() === SERVER_INSTRUCTIONS);

    const { tools } = await client.listTools();
    const names = tools.map((t) => t.name).sort();
    check("exactly five tools", names.length === 5, names.join(", "));
    check("tool names are the declared five", names.join(",") === [...TOOL_NAMES].sort().join(","));
    check(
      "every tool is annotated read-only and non-destructive",
      tools.every((t) => t.annotations?.readOnlyHint === true && t.annotations?.destructiveHint === false),
    );

    const listed = await call(client, "list_sources", {});
    check("list_sources returns the whole corpus", listed.structuredContent.file_count === 104);
    check("list_sources exposes 12 source types", listed.structuredContent.surface.length === 12);
    check(
      "list_sources returns no file contents",
      listed.structuredContent.files.every((f) => !("content" in f) && !("text" in f)),
    );
    check(
      "tables carry columns and a row count",
      listed.structuredContent.files
        .filter((f) => f.kind === "table")
        .every((f) => Array.isArray(f.columns) && typeof f.rows === "number"),
    );
    check(
      "every file carries a digest",
      listed.structuredContent.files.every((f) => /^[0-9a-f]{64}$/.test(f.sha256)),
    );
  });
}

/* ------------------------------------------------------ route boundaries --- */

async function testRouteBoundaries() {
  process.stdout.write("\nroute boundaries are a property of the surface\n");
  await withClient("hydrology,met", async (client) => {
    const listed = await call(client, "list_sources", {});
    check("restricted surface exposes only its two source types", listed.structuredContent.surface.join(",") === "hydrology,met");
    check("restricted surface exposes 14 files", listed.structuredContent.file_count === 14);

    const offSurface = await call(client, "read_span", {
      path: RERATING,
      start_line: 1,
      line_count: 5,
    });
    check("a file outside the route cannot be read", offSurface.isError === true);
    check("the refusal names the reason", offSurface.structuredContent.error === "not_on_surface");

    const offSearch = await call(client, "search_sources", { query: "derate", source_type: "engineering" });
    check("a source type outside the route cannot be searched", offSearch.isError === true);

    const escape = await call(client, "read_span", {
      path: "../../inbound/records/current_roster.csv",
      start_line: 1,
    });
    check("a path escape is refused", escape.isError === true);
  });
}

/* --------------------------------------------------------------- reading --- */

async function testBoundedReads() {
  process.stdout.write("\nreads are bounded\n");
  await withClient(null, async (client) => {
    const span = await call(client, "read_span", { path: RERATING, start_line: 1, line_count: 12 });
    check("read_span returns exactly the lines asked for", span.structuredContent.returned_lines === 12);
    check("read_span numbers the lines", span.structuredContent.lines[0].line === 1);
    check("read_span carries the file digest", /^[0-9a-f]{64}$/.test(span.structuredContent.sha256));

    const overrun = await call(client, "read_span", {
      path: SENSORS,
      start_line: 1,
      line_count: MAX_SPAN_LINES,
    });
    check(
      "a 20,000-line export cannot be read whole",
      overrun.structuredContent.returned_lines === MAX_SPAN_LINES &&
        overrun.structuredContent.total_lines > 20000,
      `${overrun.structuredContent.returned_lines} of ${overrun.structuredContent.total_lines} lines`,
    );

    const past = await call(client, "read_span", { path: FERRY, start_line: 9999 });
    check("a span past the end of a file is refused", past.isError === true);

    const prose = await call(client, "query_table", { path: RERATING });
    check("prose cannot be queried as a table", prose.isError === true);
    check("the refusal says to search instead", prose.structuredContent.error === "not_a_table");
  });
}

/* --------------------------------------------- the decisive corpus slices --- */

async function testDecisiveSlices() {
  process.stdout.write("\nthe slices the decision turns on\n");
  await withClient(null, async (client) => {
    // F11 — the ferry crossing suspends above 3.20 m at the Ferry Point reach.
    const right = await call(client, "query_table", {
      path: GAUGE,
      where: { station_id: "SEL-04", date: sepWindow(2026), gauge_m: { gt: 3.2 } },
    });
    check("SEL-04 is above 3.20 m on 14 of the 16 window days", right.structuredContent.matched === 14);

    const allWindow = await call(client, "query_table", {
      path: GAUGE,
      where: { station_id: "SEL-04", date: sepWindow(2026) },
    });
    check("the window itself is 16 days", allWindow.structuredContent.matched === WINDOW_DAYS);
    check(
      "those rows are forecast, not observation",
      allWindow.structuredContent.rows.every((r) => r.basis === "forecast"),
    );

    // The wrong station makes the ferry look fine.
    const wrong = await call(client, "query_table", {
      path: GAUGE,
      where: { station_id: "SEL-01", date: sepWindow(2026), gauge_m: { gt: 3.2 } },
    });
    check("the wrong station says 1 of 16 — the ferry looks fine", wrong.structuredContent.matched === 1);

    // F5 — the bridge derate, provable only from precedent on 22 August.
    let hot = 0;
    for (const year of [2024, 2025]) {
      const res = await call(client, "query_table", {
        path: SENSORS,
        where: {
          sensor_id: "SLW-DECK-02",
          date: sepWindow(year),
          hour_utc: "1500",
          surface_temp_c: { gt: 38 },
        },
      });
      hot += res.structuredContent.matched;
    }
    check("SLW-DECK-02 exceeds 38 C on 32 of 32 prior-season window days", hot === 32);

    let wrongSensor = 0;
    for (const year of [2024, 2025]) {
      const res = await call(client, "query_table", {
        path: SENSORS,
        where: {
          sensor_id: "SLW-DECK-01",
          date: sepWindow(year),
          hour_utc: "1500",
          surface_temp_c: { gt: 38 },
        },
      });
      wrongSensor += res.structuredContent.matched;
    }
    check("the wrong sensor says 0 of 32 — no derate at all", wrongSensor === 0);

    // The 2026 window cannot be sliced: the export stops at the extract date.
    const future = await call(client, "query_table", {
      path: SENSORS,
      where: { sensor_id: "SLW-DECK-02", date: sepWindow(2026) },
    });
    check(
      "September 2026 returns nothing — the export stops at the decision date",
      future.structuredContent.matched === 0,
    );

    // F13 — observed ferry throughput.
    const ferry = await call(client, "query_table", { path: FERRY });
    const vehicles = ferry.structuredContent.rows.reduce((n, r) => n + Number(r.vehicles_crossed), 0);
    const hours = ferry.structuredContent.rows.reduce((n, r) => n + Number(r.hours_worked), 0);
    check("observed ferry throughput is 9.02 vehicles per hour", Math.abs(vehicles / hours - 9.02) < 0.005, `${(vehicles / hours).toFixed(2)}/h`);

    const badColumn = await call(client, "query_table", { path: GAUGE, where: { statoin_id: "SEL-04" } });
    check("a misspelled column is refused, not silently ignored", badColumn.isError === true);
    check("the refusal lists the real columns", /station_id/.test(badColumn.structuredContent.message));
  });
}

/* ------------------------------------------------------------ provenance --- */

async function testProvenance() {
  process.stdout.write("\nprovenance: structural only, and it says so\n");
  await withClient(null, async (client) => {
    const found = await call(client, "search_sources", { query: "3.20", source_type: "correspondence", max_results: 5 });
    check("search finds the suspension limit in correspondence", found.structuredContent.match_count > 0);
    const hit = found.structuredContent.matches[0];

    const good = await call(client, "resolve_citation", {
      path: hit.path,
      quote: hit.text.trim().slice(0, 40),
    });
    check("a real quotation resolves", good.structuredContent.quote_found === true);
    check("it reports the line", typeof good.structuredContent.line === "number");
    check("it carries the digest", /^[0-9a-f]{64}$/.test(good.structuredContent.sha256));
    check(
      "it states what it did not check",
      good.structuredContent.not_checked === "whether the source supports the claim built on it",
    );

    const invented = await call(client, "resolve_citation", {
      path: hit.path,
      quote: "the ferry is certified to carry the recovery vehicle without restriction",
    });
    check("an invented quotation fails", invented.structuredContent.quote_found === false);
    check("but the file is still served", invented.structuredContent.served === true);

    const missing = await call(client, "resolve_citation", {
      path: "movement/MOV-9999-nonexistent.md",
      quote: "anything at all",
    });
    check("a citation to a file that does not exist fails loudly", missing.isError === true);
    check("and reports it is not served", missing.structuredContent.served === false);
  });
}

/* ----------------------------------------------------------------- main --- */

async function main() {
  await testSurfaceAndProtocol();
  await testRouteBoundaries();
  await testBoundedReads();
  await testDecisiveSlices();
  await testProvenance();
  process.stdout.write(
    `\nPASS northwind-evidence surface: ${checks} checks — 5 read-only tools, bounded reads, ` +
      "enforced route boundaries, the decisive slices, and structural-only provenance\n",
  );
}

main().catch((error) => {
  process.stderr.write(`\nFAIL ${error instanceof Error ? error.message : String(error)}\n`);
  process.exitCode = 1;
});
