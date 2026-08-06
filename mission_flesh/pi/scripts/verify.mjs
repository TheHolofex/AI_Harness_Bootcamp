import { readdir, readFile } from "node:fs/promises";
import { resolve } from "node:path";

const expected = Array.from({ length: 10 }, (_, index) => String(index + 1).padStart(2, "0"));
const runsDir = resolve("runs");
const files = (await readdir(runsDir)).filter((name) => name.endsWith(".json"));

for (const id of expected) {
  const matches = files.filter((name) => name.startsWith(`${id}-`));
  if (matches.length !== 1) {
    throw new Error(`Pattern ${id}: expected one result file, found ${matches.length}.`);
  }
  const payload = JSON.parse(await readFile(resolve(runsDir, matches[0]), "utf8"));
  if (payload.id !== id || !payload.title || !Array.isArray(payload.trace) || payload.trace.length < 2 || !payload.output) {
    throw new Error(`Pattern ${id}: result file is incomplete.`);
  }
}

console.log("PI LAB VERIFY PASS patterns=10");
