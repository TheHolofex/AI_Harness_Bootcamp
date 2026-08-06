import { existsSync } from "node:fs";
import { join } from "node:path";
import {
  P6_ROOT,
  copyFile,
  isMain,
  parseArgs,
  requireRunRoot,
  writeText,
} from "./p6-lib.mjs";
import { verifyRun } from "./verify.mjs";

function updatedStartHere() {
  return `# P6 Overnight Watch — CHANGED\n\nWave: 2\nAs-of: 06:48Z\n\nA late update and the learner's intent have arrived. The current command center and machine state are the baseline to revise.\n\n## Mission\n\nRead \`incoming/late_update.md\` and \`operator_intent.txt\`. Reconcile them with the original feeds, then revise the same two outputs in place:\n\n- \`command_center.html\`\n- \`mission_state.json\`\n\nKeep what remains true. Visibly mark what is NEW, CHANGED, CANCELLED, and UNCHANGED, include a concise before/after section, and preserve the learner's intent verbatim in the machine state. Run \`node tools/verify.mjs --run-root .\`, repair every HOLD finding, and finish only at PASS.\n`;
}

export function updateRun(runRootValue, intentValue) {
  const runRoot = requireRunRoot(runRootValue);
  if (!existsSync(join(runRoot, "START_HERE.md"))) {
    throw new Error(`P6 run is missing START_HERE.md: ${runRoot}`);
  }
  if (typeof intentValue !== "string" || !intentValue.trim()) {
    throw new Error("--intent must contain the learner's operating intent.");
  }

  const latePath = join(runRoot, "incoming", "late_update.md");
  const changed = !existsSync(latePath);
  if (changed) {
    const waveOne = verifyRun(runRoot, 1, { quiet: true });
    if (!waveOne.ok) {
      const summary = waveOne.findings.slice(0, 5).map((finding) => `${finding.code}: ${finding.message}`).join(" | ");
      throw new Error(`Wave 1 must pass before the late update is revealed. ${summary}`);
    }
    copyFile(join(P6_ROOT, "scenario", "wave-2", "late_update.md"), latePath);
  }

  writeText(join(runRoot, "operator_intent.txt"), intentValue);
  writeText(join(runRoot, "START_HERE.md"), updatedStartHere());

  const initial = verifyRun(runRoot, 2, { quiet: true });
  if (initial.ok && changed) {
    throw new Error("Wave 2 unexpectedly passed before Goose revised the command center.");
  }

  console.log(`P6 UPDATE READY wave=2 evidence=18 intent=${join(runRoot, "operator_intent.txt")}`);
  return { runRoot, changed, intent: intentValue };
}

if (isMain(import.meta.url)) {
  try {
    const args = parseArgs(process.argv.slice(2), ["--run-root", "--intent"]);
    updateRun(args["run-root"], args.intent);
  } catch (error) {
    console.error(`P6 UPDATE HOLD: ${error.message}`);
    process.exitCode = 1;
  }
}
