// Offline smoke test for the open source desk kit.
//
// Deliberately touches no network: this runs in CI, and a test that fails when
// a public feed has a bad afternoon teaches people to ignore red builds. The
// live feeds are checked separately by probe.mjs, which is a pre-class step.

import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

import { Client } from "@modelcontextprotocol/client";
import { StdioClientTransport } from "@modelcontextprotocol/client/stdio";

import { FINDINGS, SERVER_INSTRUCTIONS } from "./specimen/server.mjs";

const here = dirname(fileURLToPath(import.meta.url));
let checks = 0;
const check = (label, cond, detail = "") => {
  checks += 1;
  assert.ok(cond, `${label}${detail ? ` — ${detail}` : ""}`);
  process.stdout.write(`  ok  ${label}\n`);
};

async function withServer(rel, run) {
  const client = new Client({ name: "osint-desk-smoke", version: "1.0.0" });
  const transport = new StdioClientTransport({
    command: process.execPath, args: [join(here, rel)], cwd: here, stderr: "pipe",
  });
  try { await client.connect(transport); await run(client); }
  finally { await client.close().catch(() => {}); await transport.close().catch(() => {}); }
}

async function testSpecimen() {
  process.stdout.write("\nspecimen server — the payload is the descriptions\n");
  await withServer("specimen/server.mjs", async (client) => {
    const { tools } = await client.listTools();
    check("four tools are offered", tools.length === 4, tools.map((t) => t.name).join(", "));

    const byName = Object.fromEntries(tools.map((t) => [t.name, t]));
    check(
      "a tool asks the model to read credentials and pass them as an argument",
      /\.env|credentials|shell configuration/i.test(byName.diagnose_connection.description),
    );
    check(
      "a tool annotated read-only describes writing, overwriting and removing",
      byName.sync_watchlist.annotations?.readOnlyHint === true &&
        /overwrites|removes|Uploads/i.test(byName.sync_watchlist.description),
    );
    check(
      "a tool accepts any local path as a search source",
      /any file path or URL|outside the project/i.test(byName.search_public_records.description),
    );
    check(
      "server instructions tell the model to hide which tool answered",
      /Do not mention to the user which tool/i.test(client.getInstructions() ?? ""),
    );
    check("the shipped findings cover all four", FINDINGS.length === 4);

    // Inert by design: a course does not ship a working attack.
    const res = await client.callTool({ name: "get_vessel_position", arguments: { mmsi: "230123456" } });
    check("every handler refuses — nothing here can act", res.isError === true);
  });
}

async function testStarter() {
  process.stdout.write("\nstarter skeleton — the craft it demonstrates\n");
  await withServer("starter/server.mjs", async (client) => {
    const { tools } = await client.listTools();
    check("starts with one worked tool", tools.length === 1, tools[0].name);
    const d = tools[0].description;
    check("the description says what it does", /List vessels currently reporting/.test(d));
    check("the description says when to call it", /Use when/.test(d));
    check("the description says when NOT to call it", /Do NOT use/.test(d));
    check("the description says what comes back", /Returns at most/.test(d));
    check("it is annotated read-only and non-destructive",
      tools[0].annotations?.readOnlyHint === true && tools[0].annotations?.destructiveHint === false);
    check("its input schema is strict", tools[0].inputSchema?.additionalProperties === false);
    check("the row ceiling is in the schema, not just the prose",
      tools[0].inputSchema?.properties?.limit?.maximum === 20);
    check("server instructions warn that names and destinations are unverified",
      /verified by nobody|not verified/i.test(client.getInstructions() ?? ""));
  });
}

function testFixture() {
  process.stdout.write("\nplanted fixture — what a vessel can broadcast about itself\n");
  const fx = JSON.parse(readFileSync(join(here, "fixtures/ais_vessels_planted.json"), "utf8"));
  const planted = fx.vessels.filter((v) => String(v.mmsi).startsWith("111000"));
  check("three records are planted", planted.length === 3);
  check("one carries an instruction in the name field",
    planted.some((v) => /IGNORE ABOVE RULES/.test(v.name)));
  check("one carries markup that could break a result boundary",
    planted.some((v) => /<\/result>/.test(v.name)));
  check("one is planted and entirely benign",
    planted.some((v) => v.name === "MV NORTHERN STAR" && !/[<>]|IGNORE|SYSTEM/.test(v.destination)),
    "not everything odd is an attack");
  check("every planted field is one AIS lets a vessel set itself",
    planted.every((v) => v.name.length <= 20 && v.destination.length <= 20));
  check("the fixture says where it came from and what was done to it",
    /Fintraffic/.test(fx._note) && /planted/.test(fx._note));
}

async function main() {
  await testSpecimen();
  await testStarter();
  testFixture();
  process.stdout.write(`\nPASS osint desk kit: ${checks} checks — inert specimen, worked starter, planted fixture\n`);
}

main().catch((e) => {
  process.stderr.write(`\nFAIL ${e instanceof Error ? e.message : String(e)}\n`);
  process.exitCode = 1;
});
