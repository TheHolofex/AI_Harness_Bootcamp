import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import {
  appendFileSync,
  existsSync,
  mkdtempSync,
  readFileSync,
  readdirSync,
  symlinkSync,
  unlinkSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { prepareRun } from "../scripts/prepare.mjs";
import { updateRun } from "../scripts/update.mjs";
import { writeJson } from "../scripts/p6-lib.mjs";
import { verifyRun } from "../scripts/verify.mjs";

const TEST_DIR = dirname(fileURLToPath(import.meta.url));
const P6_ROOT = join(TEST_DIR, "..");
const COURSE_ROOT = join(P6_ROOT, "..", "..");

function freshRun() {
  const parent = mkdtempSync(join(tmpdir(), "p6-clear-watch-"));
  const runRoot = join(parent, "run");
  prepareRun(runRoot);
  return runRoot;
}

function disposition(id, wave) {
  const waveOne = {
    "EV-005": ["SUPERSEDED", "EV-001"],
    "EV-012": ["DUPLICATE", "EV-001"],
  };
  const waveTwo = {
    ...waveOne,
    "EV-003": ["SUPERSEDED", "EV-016"],
    "EV-004": ["SUPERSEDED", "EV-015"],
    "EV-007": ["SUPERSEDED", "EV-016"],
    "EV-011": ["SUPERSEDED", "EV-017"],
    "EV-018": ["DUPLICATE", "EV-017"],
  };
  return (wave === 1 ? waveOne : waveTwo)[id] ?? ["ACTIVE", id];
}

function actionsFor(wave, assignment) {
  const relay = {
    action_id: "ACT-RELAY",
    priority: assignment === "RELAY-KESTREL" ? "P1" : "P2",
    owner: "Team Orbit",
    due: "07:15Z",
    status: "READY",
    action: assignment === "RELAY-KESTREL" ? "Move MPU-1 to the relay and start the bypass." : "Hold Team Orbit and report the delayed powered bypass.",
    target_id: "RELAY-KESTREL",
    resource_ids: assignment === "RELAY-KESTREL" ? ["MPU-1"] : [],
    source_ids: ["EV-001", "EV-008", "EV-009"],
  };
  const common = [
    relay,
    {
      action_id: "ACT-WATER", priority: "P1", owner: "Resupply Pump Team", due: "08:00Z", status: "READY",
      action: "Maintain service and meet the resupply pump team.", target_id: "WATER-PLANT-EAST", resource_ids: [], source_ids: ["EV-002", "EV-006"],
    },
    {
      action_id: "ACT-CLINIC", priority: "P1", owner: "Maya Chen", due: "08:00Z", status: "READY",
      action: wave === 1 ? "Use Route Delta for the medicine delivery." : "Confirm vehicle class and use the fastest permitted route.",
      target_id: "CLINIC-JUNIPER", resource_ids: [], source_ids: wave === 1 ? ["EV-004", "EV-014"] : ["EV-014", "EV-015"],
    },
    {
      action_id: "ACT-DATA", priority: "P2", owner: "Network Desk", due: "06:50Z", status: "READY",
      action: "Run the remote reset and keep the field-team threshold at 25%.", target_id: "DATA-HUB-NORTH", resource_ids: [], source_ids: ["EV-013"],
    },
  ];
  if (wave === 1) {
    common.push(
      {
        action_id: "ACT-COLD", priority: assignment === "COLD-STORE-7" ? "P1" : "P2", owner: "Cold Chain Crew", due: "07:20Z", status: "READY",
        action: assignment === "COLD-STORE-7" ? "Move MPU-1 to Cold Store 7." : "Prepare the compatible connector and monitor the fuel horizon.",
        target_id: "COLD-STORE-7", resource_ids: assignment === "COLD-STORE-7" ? ["MPU-1"] : [], source_ids: ["EV-003", "EV-007", "EV-008", "EV-010"],
      },
      {
        action_id: "ACT-BRIDGE", priority: "P3", owner: "Bridge Unit 2", due: "07:45Z", status: "READY",
        action: "Complete the routine bridge inspection.", target_id: "BRIDGE-FOXTROT", resource_ids: [], source_ids: ["EV-011"],
      },
    );
  } else {
    common.push(
      {
        action_id: "ACT-COLD", priority: "P2", owner: "Cold Chain Crew", due: "07:00Z", status: "READY",
        action: "Monitor the stable fixed generator; do not dispatch MPU-1.", target_id: "COLD-STORE-7", resource_ids: [], source_ids: ["EV-010", "EV-016"],
      },
      {
        action_id: "ACT-BRIDGE", priority: assignment === "BRIDGE-FOXTROT" ? "P1" : "P2", owner: "Bridge Unit 2", due: "07:10Z", status: "READY",
        action: assignment === "BRIDGE-FOXTROT" ? "Move MPU-1 to power the gate and inspection rig." : "Start manual clearance and warn the ambulance desk of the 07:35 estimate.",
        target_id: "BRIDGE-FOXTROT", resource_ids: assignment === "BRIDGE-FOXTROT" ? ["MPU-1"] : [], source_ids: ["EV-008", "EV-017"],
      },
    );
  }
  return common;
}

function buildState(wave, intent = "", assignment = wave === 1 ? "RELAY-KESTREL" : "BRIDGE-FOXTROT") {
  const situations = wave === 1
    ? [
      ["RELAY-KESTREL", "OFFLINE", ["EV-001"]],
      ["WATER-PLANT-EAST", "DECLINING", ["EV-002", "EV-006"]],
      ["COLD-STORE-7", "AT_RISK", ["EV-003", "EV-007"]],
      ["ROUTE-BRAVO", "CLOSED", ["EV-004"]],
      ["BRIDGE-FOXTROT", "INSPECTION_PENDING", ["EV-011"]],
      ["DATA-HUB-NORTH", "DEGRADED_WATCH", ["EV-013"]],
      ["CLINIC-JUNIPER", "DELIVERY_DUE", ["EV-014"]],
    ]
    : [
      ["RELAY-KESTREL", "OFFLINE", ["EV-001"]],
      ["WATER-PLANT-EAST", "DECLINING", ["EV-002", "EV-006"]],
      ["COLD-STORE-7", "STABLE_FIXED_GENERATOR", ["EV-016"]],
      ["ROUTE-BRAVO", "REOPENED_LIGHT_ONLY", ["EV-015"]],
      ["BRIDGE-FOXTROT", "PRIORITY_CLEARANCE", ["EV-017"]],
      ["DATA-HUB-NORTH", "DEGRADED_WATCH", ["EV-013"]],
      ["CLINIC-JUNIPER", "DELIVERY_DUE", ["EV-014", "EV-015"]],
    ];
  const actions = actionsFor(wave, assignment);
  const resourceSources = assignment === "RELAY-KESTREL"
    ? ["EV-001", "EV-008", "EV-009"]
    : assignment === "COLD-STORE-7"
      ? ["EV-003", "EV-007", "EV-008", "EV-010"]
      : ["EV-008", "EV-017"];
  const changes = wave === 1 ? [] : [
    { classification: "NEW", summary: "Ambulance clearance is now a priority.", source_ids: ["EV-017"] },
    { classification: "CHANGED", summary: "Route Bravo reopened for light vehicles.", source_ids: ["EV-015"] },
    { classification: "CANCELLED", summary: "The Cold Store mobile-power move is cancelled.", source_ids: ["EV-016"] },
    { classification: "UNCHANGED", summary: "Relay Kestrel remains offline.", source_ids: ["EV-001"] },
  ];
  const state = {
    wave,
    as_of: wave === 1 ? "06:30Z" : "06:48Z",
    readiness: {
      status: "CONSTRAINED",
      summary: wave === 1 ? "Three time-sensitive incidents compete for attention." : "The ambulance and relay now compete for mobile power.",
      source_ids: wave === 1 ? ["EV-001", "EV-002", "EV-003"] : ["EV-001", "EV-002", "EV-017"],
    },
    resource_decision: {
      resource_id: "MPU-1",
      assignment,
      provisional: wave === 1,
      rationale: wave === 1 ? "This provisional allocation best protects the current timeline." : "This allocation applies the operator's stated priority to the new conflict.",
      source_ids: resourceSources,
    },
    situations: situations.map(([id, status, source_ids]) => ({ id, status, summary: `${id} is ${status}.`, source_ids })),
    actions,
    evidence: [],
    assumptions: ["Times are UTC.", "No unreported mobile power unit is available."],
    changes,
    operator_intent: wave === 1 ? null : intent,
  };
  const count = wave === 1 ? 14 : 18;
  state.evidence = Array.from({ length: count }, (_, index) => {
    const id = `EV-${String(index + 1).padStart(3, "0")}`;
    const [kind, canonical] = disposition(id, wave);
    if (kind !== "ACTIVE") return { id, disposition: kind, canonical_id: canonical, used_in: ["evidence-ledger"] };
    const used = [];
    if (state.readiness.source_ids.includes(id)) used.push("readiness");
    if (state.resource_decision.source_ids.includes(id)) used.push("resource-decision");
    for (const item of state.situations) if (item.source_ids.includes(id)) used.push(item.id);
    for (const item of state.actions) if (item.source_ids.includes(id)) used.push(item.action_id);
    for (const item of state.changes) if (item.source_ids.includes(id)) used.push(`change-${item.classification}`);
    return { id, disposition: kind, canonical_id: canonical, used_in: [...new Set(used.length ? used : ["evidence-ledger"])] };
  });
  return state;
}

function htmlEscape(value) {
  return String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;");
}

function buildHtml(state) {
  const evidence = state.evidence.map((item) => `<li>${item.id} · ${item.disposition}</li>`).join("");
  const actions = state.actions.map((item) => `<li><strong>${item.priority}</strong> ${htmlEscape(item.action)} · ${item.owner} · ${item.due}</li>`).join("");
  const changes = state.wave === 2
    ? `<section><h2>What Changed</h2><p>Before / After</p><p>${htmlEscape(state.operator_intent)}</p>${state.changes.map((item) => `<article><strong>${item.classification}</strong> ${item.summary}</article>`).join("")}</section>`
    : "";
  const embedded = JSON.stringify(state).replaceAll("<", "\\u003c");
  return `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>06:30 Command Center</title><style>
  :root{font-family:Inter,Segoe UI,sans-serif;color:#e9f0f5;background:#08131d}body{margin:0;padding:2rem;background:linear-gradient(135deg,#08131d,#132b3a)}main{max-width:1200px;margin:auto}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}section{padding:1.2rem;border:1px solid #355468;border-radius:14px;background:#102332}h1,h2{letter-spacing:.03em}h1{font-size:2.4rem}.badge{display:inline-block;padding:.4rem .7rem;border-radius:999px;background:#efb34c;color:#15202a;font-weight:700}li{margin:.5rem 0;line-height:1.45}article{padding:.7rem;margin:.5rem 0;background:#183446;border-left:4px solid #66c2a5}@media(max-width:760px){body{padding:1rem}.grid{grid-template-columns:1fr}h1{font-size:1.8rem}}
  </style></head><body><main><h1>06:30 Command Center</h1><p class="badge">Wave ${state.wave}</p><div class="grid">
  <section><h2>Current Readiness</h2><p>${state.readiness.status}: ${state.readiness.summary}</p></section>
  <section><h2>Resource Decision</h2><p>MPU-1 → ${state.resource_decision.assignment}</p><p>${state.resource_decision.rationale}</p></section>
  <section><h2>Top Actions</h2><ol>${actions}</ol></section><section><h2>Next 90 Minutes</h2><p>06:50–08:20 coordinated execution window.</p></section>
  <section><h2>Incidents</h2>${state.situations.map((item) => `<p>${item.id}: ${item.status}</p>`).join("")}</section>
  <section><h2>Evidence</h2><ul>${evidence}</ul></section><section><h2>Assumptions</h2><ul>${state.assumptions.map((item) => `<li>${item}</li>`).join("")}</ul></section>
  ${changes}</div></main><script id="mission-state" type="application/json">${embedded}</script></body></html>`;
}

function installOutputs(runRoot, wave, intent = "", assignment = wave === 1 ? "RELAY-KESTREL" : "BRIDGE-FOXTROT") {
  const state = buildState(wave, intent, assignment);
  writeJson(join(runRoot, "mission_state.json"), state);
  writeFileSync(join(runRoot, "command_center.html"), buildHtml(state), "utf8");
  return state;
}

test("fresh Wave 1 contains exactly four mixed feeds and starts at a useful HOLD", () => {
  const runRoot = freshRun();
  assert.equal(readFileSync(join(runRoot, ".ignore"), "utf8"), "!**\n");
  assert.deepEqual(readdirSync(join(runRoot, "incoming")).sort(), ["dispatch.json", "handoff.md", "message_dump.txt", "telemetry.csv"]);
  assert.match(readFileSync(join(runRoot, "START_HERE.md"), "utf8"), /Wave: 1/);
  const result = verifyRun(runRoot, 1, { quiet: true });
  assert.equal(result.ok, false);
  assert.deepEqual(result.findings.map((item) => item.code), ["MISSING", "MISSING"]);
});

test("a coherent Wave 1 command center passes from both authoritative and workspace verifiers", () => {
  const runRoot = freshRun();
  installOutputs(runRoot, 1);
  assert.equal(verifyRun(runRoot, 1, { quiet: true }).ok, true);
  const copied = spawnSync(process.execPath, ["tools/verify.mjs", "--run-root", ".", "--wave", "1"], { cwd: runRoot, encoding: "utf8" });
  assert.equal(copied.status, 0, `${copied.stdout}\n${copied.stderr}`);
  assert.match(copied.stdout, /P6 VERIFY PASS wave=1 evidence=14 current=12 decision=RELAY-KESTREL/);
});

test("Wave 2 accepts contrasting intents that cause different MPU-1 allocations", () => {
  const cases = [
    ["Clear the ambulance route first, even if relay restoration slips.", "BRIDGE-FOXTROT"],
    ["Protect the regional coordination window; keep bridge clearance moving manually.", "RELAY-KESTREL"],
  ];
  for (const [intent, assignment] of cases) {
    const runRoot = freshRun();
    installOutputs(runRoot, 1);
    updateRun(runRoot, intent);
    const state = installOutputs(runRoot, 2, intent, assignment);
    if (assignment === "RELAY-KESTREL") {
      state.changes.push({ classification: "UNCHANGED", summary: "Water service remains on the original watch plan.", source_ids: ["EV-002"] });
      writeJson(join(runRoot, "mission_state.json"), state);
      writeFileSync(join(runRoot, "command_center.html"), buildHtml(state), "utf8");
    }
    const result = verifyRun(runRoot, 2, { quiet: true });
    assert.equal(result.ok, true, JSON.stringify(result.findings, null, 2));
    assert.equal(result.state.resource_decision.assignment, assignment);
    assert.equal("intent" in result.state.resource_decision, false);
    assert.equal(readFileSync(join(runRoot, "operator_intent.txt"), "utf8"), intent);
  }
});

test("the two paste-ready intents must drive their matching MPU-1 allocations", () => {
  const mismatches = [
    ["Clear the ambulance route first, even if relay restoration slips.", "RELAY-KESTREL"],
    ["Protect the regional coordination window; keep bridge clearance moving manually.", "BRIDGE-FOXTROT"],
  ];
  for (const [intent, wrongAssignment] of mismatches) {
    const runRoot = freshRun();
    installOutputs(runRoot, 1);
    updateRun(runRoot, intent);
    const state = installOutputs(runRoot, 2, intent, wrongAssignment);
    if (wrongAssignment === "RELAY-KESTREL") {
      state.changes.push({ classification: "UNCHANGED", summary: "Water service remains on the original watch plan.", source_ids: ["EV-002"] });
      writeJson(join(runRoot, "mission_state.json"), state);
      writeFileSync(join(runRoot, "command_center.html"), buildHtml(state), "utf8");
    }
    const result = verifyRun(runRoot, 2, { quiet: true });
    assert.equal(result.ok, false);
    assert.ok(result.findings.some((item) => item.code === "INTENT_EFFECT"));
  }
});

test("Wave 2 does not reveal late evidence before Wave 1 passes", () => {
  const runRoot = freshRun();
  assert.throws(() => updateRun(runRoot, "Prioritize the ambulance."), /Wave 1 must pass/);
  assert.equal(existsSync(join(runRoot, "incoming", "late_update.md")), false);
  assert.equal(existsSync(join(runRoot, "operator_intent.txt")), false);
});

test("Wave 2 can be rerun with revised intent without duplicating the late update", () => {
  const runRoot = freshRun();
  installOutputs(runRoot, 1);
  const firstIntent = "Clear the ambulance route first.";
  updateRun(runRoot, firstIntent);
  installOutputs(runRoot, 2, firstIntent, "BRIDGE-FOXTROT");
  const lateBefore = readFileSync(join(runRoot, "incoming", "late_update.md"), "utf8");

  const revisedIntent = "Protect the coordination window and report the bridge delay.";
  const update = updateRun(runRoot, revisedIntent);
  assert.equal(update.changed, false);
  assert.equal(readFileSync(join(runRoot, "incoming", "late_update.md"), "utf8"), lateBefore);
  assert.equal(readdirSync(join(runRoot, "incoming")).filter((name) => name === "late_update.md").length, 1);
  assert.equal(readFileSync(join(runRoot, "operator_intent.txt"), "utf8"), revisedIntent);

  installOutputs(runRoot, 2, revisedIntent, "RELAY-KESTREL");
  assert.equal(verifyRun(runRoot, 2, { quiet: true }).ok, true);
});

test("authoritative verification rejects changed, extra, and linked input files", () => {
  for (const mutation of ["changed", "extra", "linked"]) {
    const runRoot = freshRun();
    installOutputs(runRoot, 1);
    if (mutation === "changed") appendFileSync(join(runRoot, "incoming", "handoff.md"), "\nchanged\n", "utf8");
    if (mutation === "extra") writeFileSync(join(runRoot, "incoming", "notes.txt"), "extra\n", "utf8");
    if (mutation === "linked") {
      const path = join(runRoot, "incoming", "handoff.md");
      unlinkSync(path);
      symlinkSync(join(P6_ROOT, "scenario", "wave-1", "incoming", "handoff.md"), path);
    }
    const result = verifyRun(runRoot, 1, { quiet: true });
    assert.equal(result.ok, false);
    assert.ok(result.findings.some((item) => ["INPUT_CHANGED", "INPUT_SET", "FILE_TYPE"].includes(item.code)));
  }
});

test("duplicate and superseded evidence cannot drive current work", () => {
  const runRoot = freshRun();
  const state = installOutputs(runRoot, 1);
  state.actions[0].source_ids.push("EV-005");
  writeJson(join(runRoot, "mission_state.json"), state);
  writeFileSync(join(runRoot, "command_center.html"), buildHtml(state), "utf8");
  const result = verifyRun(runRoot, 1, { quiet: true });
  assert.equal(result.ok, false);
  assert.ok(result.findings.some((item) => item.code === "SOURCE"));
});

test("one mobile unit cannot be double-booked or sent to the recovered cold store in Wave 2", () => {
  const runRoot = freshRun();
  installOutputs(runRoot, 1);
  const intent = "Clear the ambulance route first.";
  updateRun(runRoot, intent);
  const state = installOutputs(runRoot, 2, intent, "BRIDGE-FOXTROT");
  state.actions[0].resource_ids = ["MPU-1"];
  state.resource_decision.assignment = "COLD-STORE-7";
  state.resource_decision.source_ids = ["EV-008", "EV-016"];
  writeJson(join(runRoot, "mission_state.json"), state);
  writeFileSync(join(runRoot, "command_center.html"), buildHtml(state), "utf8");
  const result = verifyRun(runRoot, 2, { quiet: true });
  assert.equal(result.ok, false);
  assert.ok(result.findings.some((item) => item.code === "RESOURCE"));
  assert.ok(result.findings.some((item) => item.code === "DOUBLE_BOOK"));
});

test("the command center must embed exactly the machine state and show What Changed", () => {
  const runRoot = freshRun();
  installOutputs(runRoot, 1);
  const intent = "Prioritize the ambulance.";
  updateRun(runRoot, intent);
  const state = installOutputs(runRoot, 2, intent);
  const path = join(runRoot, "command_center.html");
  writeFileSync(path, buildHtml({ ...state, as_of: "06:49Z" }).replace("What Changed", "Revision"), "utf8");
  const result = verifyRun(runRoot, 2, { quiet: true });
  assert.equal(result.ok, false);
  assert.ok(result.findings.some((item) => item.code === "EMBED"));
  assert.ok(result.findings.some((item) => item.code === "HTML_CHANGE"));
});

test("visible dashboard sections cannot hide their action detail in embedded JSON", () => {
  const runRoot = freshRun();
  const state = installOutputs(runRoot, 1);
  const path = join(runRoot, "command_center.html");
  const hollow = buildHtml(state).replace(/<section><h2>Top Actions<\/h2><ol>[\s\S]*?<\/ol><\/section>/, "<section><h2>Top Actions</h2></section>");
  writeFileSync(path, hollow, "utf8");
  const result = verifyRun(runRoot, 1, { quiet: true });
  assert.equal(result.ok, false);
  assert.ok(result.findings.some((item) => item.code === "HTML_ACTION"));
});

test("unfinished template fields cannot pass as an operating product", () => {
  const runRoot = freshRun();
  const state = installOutputs(runRoot, 1);
  state.actions[0].owner = "[OWNER]";
  state.assumptions.push("Replace every [OWNER] and the date before use.");
  writeJson(join(runRoot, "mission_state.json"), state);
  writeFileSync(join(runRoot, "command_center.html"), buildHtml(state), "utf8");
  const result = verifyRun(runRoot, 1, { quiet: true });
  assert.equal(result.ok, false);
  assert.ok(result.findings.some((item) => item.code === "PLACEHOLDER"));
});

test("visible dashboard-only placeholders cannot pass", () => {
  const runRoot = freshRun();
  const state = installOutputs(runRoot, 1);
  const path = join(runRoot, "command_center.html");
  const unfinished = buildHtml(state).replace("</main>", "<p>Replace [OWNER] and [DATE] before use.</p></main>");
  writeFileSync(path, unfinished, "utf8");
  const result = verifyRun(runRoot, 1, { quiet: true });
  assert.equal(result.ok, false);
  assert.ok(result.findings.some((item) => item.code === "PLACEHOLDER"));
});

test("malformed arrays produce named HOLD findings instead of crashing", () => {
  const runRoot = freshRun();
  const state = installOutputs(runRoot, 1);
  state.actions = [null, null, null, null, null];
  writeJson(join(runRoot, "mission_state.json"), state);
  writeFileSync(join(runRoot, "command_center.html"), buildHtml({ ...state, actions: [] }), "utf8");
  assert.doesNotThrow(() => verifyRun(runRoot, 1, { quiet: true }));
  assert.equal(verifyRun(runRoot, 1, { quiet: true }).ok, false);
});

test("object-shaped source lists produce HOLD findings instead of crashing", () => {
  const waveOneRoot = freshRun();
  const waveOne = installOutputs(waveOneRoot, 1);
  waveOne.resource_decision.source_ids = {};
  writeJson(join(waveOneRoot, "mission_state.json"), waveOne);
  writeFileSync(join(waveOneRoot, "command_center.html"), buildHtml(waveOne), "utf8");
  assert.doesNotThrow(() => verifyRun(waveOneRoot, 1, { quiet: true }));
  assert.equal(verifyRun(waveOneRoot, 1, { quiet: true }).ok, false);

  const waveTwoRoot = freshRun();
  installOutputs(waveTwoRoot, 1);
  const intent = "Put the ambulance route first.";
  updateRun(waveTwoRoot, intent);
  const waveTwo = installOutputs(waveTwoRoot, 2, intent);
  waveTwo.changes.find((item) => item.classification === "UNCHANGED").source_ids = {};
  writeJson(join(waveTwoRoot, "mission_state.json"), waveTwo);
  writeFileSync(join(waveTwoRoot, "command_center.html"), buildHtml(waveTwo), "utf8");
  assert.doesNotThrow(() => verifyRun(waveTwoRoot, 2, { quiet: true }));
  assert.equal(verifyRun(waveTwoRoot, 2, { quiet: true }).ok, false);
});

test("launchers keep the normal profile and expose only launch then plain-language update", () => {
  const start = readFileSync(join(P6_ROOT, "scripts", "Start-P6.ps1"), "utf8");
  const update = readFileSync(join(P6_ROOT, "scripts", "Update-P6.ps1"), "utf8");
  for (const launcher of [start, update]) {
    assert.match(launcher, /--recipe \.\/mission\.yaml --provider xai --model \$Model --with-builtin developer/);
    assert.doesNotMatch(launcher, /--no-profile|--max-turns|--no-session|--render-recipe|Start-Transcript|check-transcript|LAST_RUN|GetTempPath/);
    assert.match(launcher, /runs\\current/);
  }
  assert.match(start, /goose" @\("run", "--help"\)/);
  assert.match(start, /goose" @\("recipe", "validate"/);
  assert.ok(start.indexOf("\nTest-P6Runtime\n") < start.indexOf('& node (Join-Path $PSScriptRoot "prepare.mjs")'));
  assert.ok(start.indexOf("XAI_API_KEY") < start.indexOf('& node (Join-Path $PSScriptRoot "prepare.mjs")'));
  assert.match(update, /\[string\]\$Intent/);
  assert.match(update, /--intent \$Intent/);
  assert.doesNotMatch(update, /run --help|recipe", "validate/);
  assert.ok(update.indexOf("\nTest-P6Runtime\n") < update.indexOf('& node (Join-Path $P6Root "scripts\\update.mjs")'));
  assert.ok(update.indexOf("XAI_API_KEY") < update.indexOf('& node (Join-Path $P6Root "scripts\\update.mjs")'));
  assert.equal(existsSync(join(P6_ROOT, "scripts", "Add-P6Wave2.ps1")), false);
  assert.equal(existsSync(join(P6_ROOT, "scripts", "check-transcript.mjs")), false);
});

test("recipe names only the two mission outputs and does not restrict the profile", () => {
  const recipe = readFileSync(join(P6_ROOT, "clear_overnight_watch.yaml"), "utf8");
  assert.doesNotMatch(recipe, /^\s*(settings|extensions|parameters):/m);
  assert.doesNotMatch(recipe, /provider|model|run_id|schema_version|environment variables/i);
  assert.match(recipe, /command_center\.html/);
  assert.match(recipe, /mission_state\.json/);
  assert.doesNotMatch(recipe, /receipt|manifest|snapshot|transcript|deliverables\//i);
});

test("the live lesson uses complete paste-ready commands and closeout", () => {
  const lesson = readFileSync(join(COURSE_ROOT, "site", "blocks", "p6.html"), "utf8");
  for (const unfinished of [
    "YOUR ONE-SENTENCE OPERATING INTENT",
    "[PASTE THE FINAL P6 VERIFY PASS LINE]",
    "[NAME THE QUEUE]",
    "after replacing both brackets",
    "-Intent $intent",
  ]) {
    assert.equal(lesson.includes(unfinished), false, `Found unfinished learner text: ${unfinished}`);
  }
  assert.match(lesson, /-Intent "Clear the ambulance route first, even if relay restoration slips\."/);
  assert.match(lesson, /-Intent "Protect the regional coordination window; keep bridge clearance moving manually\."/);
  assert.match(lesson, /Run the P6 verifier yourself/);
  assert.match(lesson, /Use today's local date automatically/);
});
