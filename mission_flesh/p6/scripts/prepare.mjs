import { existsSync, mkdirSync, readdirSync, rmSync } from "node:fs";
import { join, resolve } from "node:path";
import {
  P6_ROOT,
  copyFile,
  copyTree,
  isMain,
  parseArgs,
  requireRunRoot,
  writeText,
} from "./p6-lib.mjs";
import { verifyRun } from "./verify.mjs";

function startHere() {
  return `# P6 Overnight Watch — RED\n\nWave: 1\nAs-of: 06:30Z\n\nFour mixed overnight feeds are waiting under \`incoming/\`. Together they contain 14 labeled evidence items, a conflict, a stale reading, a duplicate transmission, deadlines, people, and one mobile power unit that cannot serve two places at once.\n\n## Mission\n\nUse the evidence to make a defensible provisional MPU-1 decision and build the 06:30 operating picture. Write exactly two outputs in this directory:\n\n- \`command_center.html\`\n- \`mission_state.json\`\n\nThe page must be useful at a glance and the JSON must account for every EV-### item. Run \`node tools/verify.mjs --run-root .\`, repair every HOLD finding, and finish only at PASS.\n`;
}

export function prepareRun(runRootValue) {
  const runRoot = requireRunRoot(runRootValue);
  const defaultCurrent = resolve(P6_ROOT, "runs", "current");
  if (existsSync(runRoot) && readdirSync(runRoot).length > 0) {
    if (resolve(runRoot) !== defaultCurrent) {
      throw new Error(`Run root already exists and is not empty: ${runRoot}`);
    }
    rmSync(runRoot, { recursive: true, force: true });
  }
  mkdirSync(runRoot, { recursive: true });

  // Goose's Developer extension honors .ignore files. This negation makes the
  // prepared workspace visible even though runs/ is intentionally Git-ignored.
  writeText(join(runRoot, ".ignore"), "!**\n");
  writeText(join(runRoot, "START_HERE.md"), startHere());
  copyFile(join(P6_ROOT, "clear_overnight_watch.yaml"), join(runRoot, "mission.yaml"));
  copyTree(join(P6_ROOT, "scenario", "wave-1", "incoming"), join(runRoot, "incoming"));
  copyFile(join(P6_ROOT, "scripts", "verify.mjs"), join(runRoot, "tools", "verify.mjs"));

  const initial = verifyRun(runRoot, 1, { quiet: true });
  if (initial.ok) throw new Error("Fresh Wave 1 unexpectedly passed before Goose built the command center.");

  console.log(`P6 PREP PASS wave=1 evidence=14 run=${runRoot}`);
  return { runRoot };
}

if (isMain(import.meta.url)) {
  try {
    const args = parseArgs(process.argv.slice(2), ["--run-root"]);
    prepareRun(args["run-root"]);
  } catch (error) {
    console.error(`P6 PREP HOLD: ${error.message}`);
    process.exitCode = 1;
  }
}
