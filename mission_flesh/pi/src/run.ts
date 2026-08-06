import { mkdir, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { PiRuntime } from "./pi-runtime.js";
import { patterns } from "./patterns/index.js";

const requested = process.argv[2]?.padStart(2, "0");
if (!requested || !patterns[requested]) {
  throw new Error(`Choose one pattern from ${Object.keys(patterns).sort().join(", ")}.`);
}

const runtime = await PiRuntime.create();
const result = await patterns[requested](runtime);
const runsDir = resolve("runs");
await mkdir(runsDir, { recursive: true });
await writeFile(
  resolve(runsDir, `${result.id}-${result.slug}.json`),
  `${JSON.stringify({ ...result, completedAt: new Date().toISOString() }, null, 2)}\n`,
  "utf8",
);

console.log(`PATTERN ${result.id} · ${result.title.toUpperCase()}`);
for (const step of result.trace) console.log(`  ${step}`);
console.log(`RESULT · ${result.output}`);
console.log(`PI PATTERN ${result.id} PASS`);
