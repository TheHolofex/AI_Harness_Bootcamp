import { createHash } from "node:crypto";
import {
  existsSync,
  lstatSync,
  readFileSync,
  readdirSync,
} from "node:fs";
import { dirname, isAbsolute, join, relative, resolve, sep } from "node:path";
import { isDeepStrictEqual } from "node:util";
import { fileURLToPath } from "node:url";

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const COURSE_ROOT = resolve(SCRIPT_DIR, "..");
const HAS_COURSE_SOURCE = existsSync(join(COURSE_ROOT, "scenario", "wave-1", "incoming"));
const WAVE_ONE_FILES = ["dispatch.json", "handoff.md", "message_dump.txt", "telemetry.csv"];
const ALL_IDS = Array.from({ length: 18 }, (_, index) => `EV-${String(index + 1).padStart(3, "0")}`);
const DISPOSITIONS = {
  1: {
    "EV-005": ["SUPERSEDED", "EV-001"],
    "EV-012": ["DUPLICATE", "EV-001"],
  },
  2: {
    "EV-003": ["SUPERSEDED", "EV-016"],
    "EV-004": ["SUPERSEDED", "EV-015"],
    "EV-005": ["SUPERSEDED", "EV-001"],
    "EV-007": ["SUPERSEDED", "EV-016"],
    "EV-011": ["SUPERSEDED", "EV-017"],
    "EV-012": ["DUPLICATE", "EV-001"],
    "EV-018": ["DUPLICATE", "EV-017"],
  },
};
const SITUATION_STATUS = {
  1: {
    "RELAY-KESTREL": "OFFLINE",
    "WATER-PLANT-EAST": "DECLINING",
    "COLD-STORE-7": "AT_RISK",
    "ROUTE-BRAVO": "CLOSED",
    "BRIDGE-FOXTROT": "INSPECTION_PENDING",
    "DATA-HUB-NORTH": "DEGRADED_WATCH",
    "CLINIC-JUNIPER": "DELIVERY_DUE",
  },
  2: {
    "RELAY-KESTREL": "OFFLINE",
    "WATER-PLANT-EAST": "DECLINING",
    "COLD-STORE-7": "STABLE_FIXED_GENERATOR",
    "ROUTE-BRAVO": "REOPENED_LIGHT_ONLY",
    "BRIDGE-FOXTROT": "PRIORITY_CLEARANCE",
    "DATA-HUB-NORTH": "DEGRADED_WATCH",
    "CLINIC-JUNIPER": "DELIVERY_DUE",
  },
};
const EXPECTED_ASSIGNMENT_BY_INTENT = new Map([
  ["Clear the ambulance route first, even if relay restoration slips.", "BRIDGE-FOXTROT"],
  ["Protect the regional coordination window; keep bridge clearance moving manually.", "RELAY-KESTREL"],
]);

function finding(findings, code, message) {
  findings.push({ code, message });
}

function text(path) {
  return readFileSync(path, "utf8").replace(/^\uFEFF/, "");
}

function json(path) {
  return JSON.parse(text(path));
}

function sha256(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function inside(root, target) {
  const rel = relative(resolve(root), resolve(target));
  return rel === "" || (!rel.startsWith(`..${sep}`) && rel !== ".." && !isAbsolute(rel));
}

function safeRoot(value) {
  const root = resolve(String(value ?? ""));
  if (!value || root === resolve(root, sep)) throw new Error("Unsafe or missing run root.");
  return root;
}

function regularFile(path, findings, label) {
  if (!existsSync(path)) {
    finding(findings, "MISSING", `${label} is missing.`);
    return false;
  }
  const info = lstatSync(path);
  if (!info.isFile() || info.isSymbolicLink()) {
    finding(findings, "FILE_TYPE", `${label} must be a regular file.`);
    return false;
  }
  return true;
}

function requireObject(value, findings, label) {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    finding(findings, "SCHEMA", `${label} must be an object.`);
    return false;
  }
  return true;
}

function requireFields(value, fields, findings, label) {
  if (!requireObject(value, findings, label)) return false;
  for (const field of fields) {
    if (!(field in value)) finding(findings, "SCHEMA", `${label} is missing '${field}'.`);
  }
  return true;
}

function nonEmpty(value) {
  return typeof value === "string" && value.trim().length > 0;
}

const BRACKETED_PLACEHOLDER = /\[(?:OWNER|DATE|DUE|TIME|NAME|QUEUE|TEAM|PERSON|ROLE|REPLACE[^\]]*|INSERT[^\]]*|PASTE[^\]]*|YOUR[^\]]*|TODO|TBD|TBC|UNKNOWN|UNASSIGNED)\]/i;
const STANDALONE_PLACEHOLDER = /^\s*(?:OWNER|DATE|DUE|TBD|TBC|TODO|UNKNOWN|UNASSIGNED|N\/A|NOT SET)\s*$/i;
const INSTRUCTIONAL_PLACEHOLDER = /\b(?:replace|insert|paste|fill in)\b.{0,80}\b(?:owner|date|due|field|value|placeholder|bracket)\b/i;

function unfinishedMarker(value) {
  if (typeof value !== "string") return null;
  for (const pattern of [BRACKETED_PLACEHOLDER, STANDALONE_PLACEHOLDER, INSTRUCTIONAL_PLACEHOLDER]) {
    const match = pattern.exec(value);
    if (match) return match[0].trim();
  }
  return null;
}

function validateNoPlaceholders(value, findings, path = "mission_state") {
  if (typeof value === "string") {
    const marker = unfinishedMarker(value);
    if (marker) finding(findings, "PLACEHOLDER", `${path} contains unfinished template text: ${marker}.`);
    return;
  }
  if (Array.isArray(value)) {
    value.forEach((item, index) => validateNoPlaceholders(item, findings, `${path}[${index}]`));
    return;
  }
  if (value && typeof value === "object") {
    for (const [key, item] of Object.entries(value)) validateNoPlaceholders(item, findings, `${path}.${key}`);
  }
}

function unique(values) {
  return Array.isArray(values) && new Set(values).size === values.length;
}

function hasValue(values, expected) {
  return Array.isArray(values) && values.includes(expected);
}

function expectedIds(wave) {
  return ALL_IDS.slice(0, wave === 1 ? 14 : 18);
}

function dispositionFor(id, wave) {
  return DISPOSITIONS[wave][id] ?? ["ACTIVE", id];
}

function compareAuthoritativeInputs(runRoot, wave, findings) {
  const ignorePath = join(runRoot, ".ignore");
  if (regularFile(ignorePath, findings, ".ignore") && text(ignorePath) !== "!**\n") {
    finding(findings, "WORKSPACE", ".ignore must contain exactly !** so Goose can see the prepared workspace.");
  }
  const expectedNames = [...WAVE_ONE_FILES, ...(wave === 2 ? ["late_update.md"] : [])].sort();
  const incomingRoot = join(runRoot, "incoming");
  if (!existsSync(incomingRoot) || !lstatSync(incomingRoot).isDirectory()) {
    finding(findings, "INPUT", "incoming/ is missing.");
    return;
  }
  const incomingEntries = readdirSync(incomingRoot, { withFileTypes: true });
  const actualNames = incomingEntries.map((entry) => entry.name).sort();
  if (!isDeepStrictEqual(actualNames, expectedNames)) {
    finding(findings, "INPUT_SET", `incoming/ must contain exactly: ${expectedNames.join(", ")}.`);
  }
  for (const entry of incomingEntries) {
    if (!entry.isFile()) finding(findings, "FILE_TYPE", `incoming/${entry.name} must be a regular file.`);
  }
  for (const name of expectedNames) {
    const runtime = join(incomingRoot, name);
    if (!regularFile(runtime, findings, `incoming/${name}`)) continue;
    if (HAS_COURSE_SOURCE) {
      const source = name === "late_update.md"
        ? join(COURSE_ROOT, "scenario", "wave-2", name)
        : join(COURSE_ROOT, "scenario", "wave-1", "incoming", name);
      if (!existsSync(source) || sha256(runtime) !== sha256(source)) {
        finding(findings, "INPUT_CHANGED", `incoming/${name} differs from the prepared evidence.`);
      }
    }
  }
  const evidenceText = expectedNames.map((name) => existsSync(join(incomingRoot, name)) ? text(join(incomingRoot, name)) : "").join("\n");
  for (const id of expectedIds(wave)) {
    if (!evidenceText.includes(id)) finding(findings, "INPUT_EVIDENCE", `${id} is missing from the current feeds.`);
  }
  const unknown = [...new Set(evidenceText.match(/EV-\d{3}/g) ?? [])].filter((id) => !expectedIds(wave).includes(id));
  if (unknown.length) finding(findings, "INPUT_EVIDENCE", `Unexpected evidence IDs: ${unknown.join(", ")}.`);

  if (HAS_COURSE_SOURCE) {
    for (const [runtime, source, label] of [
      [join(runRoot, "mission.yaml"), join(COURSE_ROOT, "clear_overnight_watch.yaml"), "mission.yaml"],
      [join(runRoot, "tools", "verify.mjs"), fileURLToPath(import.meta.url), "tools/verify.mjs"],
    ]) {
      if (!regularFile(runtime, findings, label) || sha256(runtime) !== sha256(source)) {
        finding(findings, "TOOL_COPY", `${label} differs from the prepared course copy.`);
      }
    }
  }
}

function validateEvidence(state, wave, findings) {
  if (!Array.isArray(state.evidence)) {
    finding(findings, "EVIDENCE", "mission_state evidence must be an array.");
    return new Set();
  }
  const ids = state.evidence.map((entry) => entry?.id);
  if (!unique(ids) || !isDeepStrictEqual([...ids].sort(), expectedIds(wave))) {
    finding(findings, "EVIDENCE_SET", `Evidence must account for every ${wave === 1 ? 14 : 18} EV item exactly once.`);
  }
  const active = new Set();
  for (const id of expectedIds(wave)) {
    const entry = state.evidence.find((candidate) => candidate?.id === id);
    if (!entry) continue;
    requireFields(entry, ["id", "disposition", "canonical_id", "used_in"], findings, `evidence ${id}`);
    const [expectedDisposition, expectedCanonical] = dispositionFor(id, wave);
    if (entry.disposition !== expectedDisposition || entry.canonical_id !== expectedCanonical) {
      finding(findings, "DISPOSITION", `${id} must be ${expectedDisposition} with canonical_id ${expectedCanonical}.`);
    }
    if (!Array.isArray(entry.used_in) || !unique(entry.used_in) || entry.used_in.some((item) => !nonEmpty(item))) {
      finding(findings, "EVIDENCE_USAGE", `${id} needs unique, non-empty used_in entries.`);
    }
    if (expectedDisposition === "ACTIVE") {
      active.add(id);
      if (!entry.used_in?.length) finding(findings, "EVIDENCE_USAGE", `${id} must be used in the operating picture.`);
    } else if (!hasValue(entry.used_in, "evidence-ledger") || entry.used_in.length !== 1) {
      finding(findings, "EVIDENCE_USAGE", `${id} may appear only in the evidence-ledger.`);
    }
  }
  return active;
}

function validateSources(items, active, findings, label) {
  for (const item of items) {
    if (!Array.isArray(item?.source_ids) || !unique(item.source_ids) || item.source_ids.length === 0) {
      finding(findings, "SOURCE", `${label} ${item?.id ?? item?.action_id ?? "item"} needs unique source_ids.`);
      continue;
    }
    const invalid = item.source_ids.filter((id) => !active.has(id));
    if (invalid.length) finding(findings, "SOURCE", `${label} ${item?.id ?? item?.action_id ?? "item"} uses non-current evidence: ${invalid.join(", ")}.`);
  }
}

function validateSituations(state, wave, active, findings) {
  if (!Array.isArray(state.situations)) {
    finding(findings, "SITUATIONS", "mission_state situations must be an array.");
    return;
  }
  const ids = state.situations.map((item) => item?.id);
  if (!unique(ids)) finding(findings, "SITUATIONS", "Situation IDs must be unique.");
  for (const [id, expectedStatus] of Object.entries(SITUATION_STATUS[wave])) {
    const item = state.situations.find((candidate) => candidate?.id === id);
    if (!item) {
      finding(findings, "SITUATION_SET", `Missing situation ${id}.`);
      continue;
    }
    requireFields(item, ["id", "status", "summary", "source_ids"], findings, `situation ${id}`);
    if (item.status !== expectedStatus) finding(findings, "CURRENT_FACT", `${id} status must be ${expectedStatus}.`);
    if (!nonEmpty(item.summary)) finding(findings, "SITUATION", `${id} needs a summary.`);
  }
  validateSources(state.situations, active, findings, "situation");
  const requiredSources = wave === 1
    ? { "RELAY-KESTREL": ["EV-001"], "COLD-STORE-7": ["EV-003", "EV-007"], "ROUTE-BRAVO": ["EV-004"] }
    : { "RELAY-KESTREL": ["EV-001"], "COLD-STORE-7": ["EV-016"], "ROUTE-BRAVO": ["EV-015"], "BRIDGE-FOXTROT": ["EV-017"] };
  for (const [id, sources] of Object.entries(requiredSources)) {
    const item = state.situations.find((candidate) => candidate?.id === id);
    if (item && !sources.every((source) => hasValue(item.source_ids, source))) {
      finding(findings, "CURRENT_FACT", `${id} must cite ${sources.join(" and ")}.`);
    }
  }
}

function timeMinutes(value) {
  const match = /^(\d{2}):(\d{2})Z$/.exec(value ?? "");
  if (!match) return null;
  const hours = Number(match[1]);
  const minutes = Number(match[2]);
  return hours < 24 && minutes < 60 ? hours * 60 + minutes : null;
}

function validateActions(state, wave, active, findings) {
  if (!Array.isArray(state.actions) || state.actions.length < 5) {
    finding(findings, "ACTIONS", "mission_state needs at least five prioritized actions.");
    return;
  }
  const ids = state.actions.map((action) => action?.action_id);
  if (!unique(ids)) finding(findings, "ACTIONS", "Action IDs must be unique.");
  for (const action of state.actions) {
    requireFields(action, ["action_id", "priority", "owner", "due", "status", "action", "target_id", "resource_ids", "source_ids"], findings, `action ${action?.action_id ?? "unknown"}`);
    if (!["P1", "P2", "P3"].includes(action?.priority)) finding(findings, "ACTION", `${action?.action_id} priority must be P1, P2, or P3.`);
    for (const field of ["action_id", "owner", "due", "status", "action", "target_id"]) {
      if (!nonEmpty(action?.[field])) finding(findings, "ACTION", `${action?.action_id ?? "Action"} needs ${field}.`);
    }
    if (timeMinutes(action?.due) === null) finding(findings, "ACTION", `${action?.action_id ?? "Action"} due must be HH:MMZ.`);
    if (!Array.isArray(action?.resource_ids) || !unique(action.resource_ids)) finding(findings, "ACTION", `${action?.action_id ?? "Action"} resource_ids must be a unique array.`);
  }
  validateSources(state.actions, active, findings, "action");
  const coverage = wave === 1
    ? [["EV-001"], ["EV-002", "EV-006"], ["EV-003", "EV-007"], ["EV-004", "EV-014"], ["EV-011"], ["EV-013"]]
    : [["EV-001"], ["EV-002", "EV-006"], ["EV-014", "EV-015"], ["EV-016"], ["EV-017"], ["EV-013"]];
  for (const group of coverage) {
    if (!state.actions.some((action) => group.some((id) => hasValue(action?.source_ids, id)))) {
      finding(findings, "ACTION_COVERAGE", `An action must use current evidence from ${group.join(" or ")}.`);
    }
  }
  const deadlines = [["EV-001", "07:15Z"], ["EV-002", "08:00Z"], ["EV-014", "08:00Z"]];
  if (wave === 2) deadlines.push(["EV-017", "07:10Z"]);
  for (const [source, limit] of deadlines) {
    const action = state.actions.find((candidate) => hasValue(candidate?.source_ids, source));
    if (!action || timeMinutes(action.due) === null || timeMinutes(action.due) > timeMinutes(limit)) {
      finding(findings, "DEADLINE", `${source} needs an action due no later than ${limit}.`);
    }
  }
}

function validateResource(state, wave, active, findings) {
  const decision = state.resource_decision;
  if (!requireFields(decision, ["resource_id", "assignment", "provisional", "rationale", "source_ids"], findings, "resource_decision")) return;
  if ("intent" in decision) finding(findings, "INTENT", "Keep operator_intent only at the mission-state level, not inside resource_decision.");
  if (decision.resource_id !== "MPU-1") finding(findings, "RESOURCE", "The only mobile power unit is MPU-1.");
  const allowed = wave === 1
    ? ["RELAY-KESTREL", "COLD-STORE-7"]
    : ["RELAY-KESTREL", "BRIDGE-FOXTROT"];
  if (!allowed.includes(decision.assignment)) finding(findings, "RESOURCE", `MPU-1 assignment must be one of: ${allowed.join(", ")}.`);
  if (!nonEmpty(decision.rationale)) finding(findings, "RESOURCE", "MPU-1 needs a decision rationale.");
  const decisionSources = Array.isArray(decision.source_ids) ? decision.source_ids : [];
  if (!hasValue(decisionSources, "EV-008") || decisionSources.some((id) => !active.has(id))) {
    finding(findings, "RESOURCE", "MPU-1 rationale must cite EV-008 and only current evidence.");
  }
  if (wave === 1 && decision.provisional !== true) finding(findings, "RESOURCE", "Wave 1 MPU-1 decision must be provisional.");
  if (wave === 2 && decision.provisional !== false) finding(findings, "RESOURCE", "Wave 2 MPU-1 decision must be final.");
  const assignmentSources = {
    "RELAY-KESTREL": ["EV-001", "EV-008", "EV-009"],
    "COLD-STORE-7": ["EV-003", "EV-007", "EV-008", "EV-010"],
    "BRIDGE-FOXTROT": ["EV-008", "EV-017"],
  }[decision.assignment] ?? [];
  if (!assignmentSources.every((id) => hasValue(decisionSources, id))) {
    finding(findings, "RESOURCE", `${decision.assignment ?? "MPU-1 assignment"} must cite ${assignmentSources.join(", ")}.`);
  }
  const actions = Array.isArray(state.actions) ? state.actions : [];
  const bookings = actions.filter((action) => action?.status !== "CANCELLED" && hasValue(action?.resource_ids, "MPU-1"));
  if (bookings.length !== 1) finding(findings, "DOUBLE_BOOK", "Exactly one current action must book MPU-1.");
  if (bookings[0] && bookings[0].target_id !== decision.assignment) {
    finding(findings, "DOUBLE_BOOK", "The MPU-1 action target must match the resource decision.");
  }
}

function validateChanges(state, wave, intent, findings) {
  if (wave === 1) {
    if (!Array.isArray(state.changes) || state.changes.length !== 0) finding(findings, "CHANGES", "Wave 1 changes must be an empty array.");
    if (![null, ""].includes(state.operator_intent)) finding(findings, "INTENT", "Wave 1 operator_intent must be empty.");
    return;
  }
  if (state.operator_intent !== intent) finding(findings, "INTENT", "mission_state must preserve operator_intent.txt verbatim.");
  const expectedAssignment = EXPECTED_ASSIGNMENT_BY_INTENT.get(intent.trim());
  if (expectedAssignment && state.resource_decision?.assignment !== expectedAssignment) {
    finding(findings, "INTENT_EFFECT", `The selected operating intent requires MPU-1 assignment to ${expectedAssignment}.`);
  }
  if (!Array.isArray(state.changes)) {
    finding(findings, "CHANGES", "Wave 2 changes must be an array.");
    return;
  }
  const classes = state.changes.map((change) => change?.classification);
  const expected = ["CANCELLED", "CHANGED", "NEW", "UNCHANGED"];
  if (!expected.every((classification) => classes.includes(classification))) {
    finding(findings, "CHANGES", "Wave 2 needs NEW, CHANGED, CANCELLED, and UNCHANGED change records.");
  }
  for (const change of state.changes) {
    requireFields(change, ["classification", "summary", "source_ids"], findings, `change ${change?.classification ?? "unknown"}`);
    if (!nonEmpty(change?.summary) || !Array.isArray(change?.source_ids) || change?.source_ids.length === 0) {
      finding(findings, "CHANGES", `${change?.classification ?? "Change"} needs a summary and source_ids.`);
    }
  }
  const required = { NEW: "EV-017", CHANGED: "EV-015", CANCELLED: "EV-016" };
  for (const [classification, source] of Object.entries(required)) {
    if (!state.changes.some((change) => change?.classification === classification && hasValue(change?.source_ids, source))) {
      finding(findings, "CHANGES", `${classification} must cite ${source}.`);
    }
  }
  const unchanged = state.changes.find((change) => change?.classification === "UNCHANGED");
  if (unchanged && (!Array.isArray(unchanged.source_ids) || !unchanged.source_ids.some((id) => ["EV-001", "EV-002", "EV-006", "EV-013", "EV-014"].includes(id)))) {
    finding(findings, "CHANGES", "UNCHANGED must cite evidence that remains current from Wave 1.");
  }
  validateSources(state.changes, new Set(expectedIds(2).filter((id) => dispositionFor(id, 2)[0] === "ACTIVE")), findings, "change");
}

function visibleText(html) {
  return html
    .replace(/<script\b[\s\S]*?<\/script>/gi, " ")
    .replace(/<style\b[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&amp;/gi, "&")
    .replace(/&lt;/gi, "<")
    .replace(/&gt;/gi, ">")
    .replace(/&quot;/gi, '"')
    .replace(/&#39;|&apos;/gi, "'")
    .replace(/&nbsp;/gi, " ")
    .replace(/&#(\d+);/g, (match, value) => {
      const codePoint = Number(value);
      return Number.isInteger(codePoint) && codePoint <= 0x10ffff ? String.fromCodePoint(codePoint) : match;
    })
    .replace(/&#x([0-9a-f]+);/gi, (match, value) => {
      const codePoint = Number.parseInt(value, 16);
      return Number.isInteger(codePoint) && codePoint <= 0x10ffff ? String.fromCodePoint(codePoint) : match;
    })
    .replace(/\s+/g, " ");
}

function normalizedVisibleValue(value) {
  return typeof value === "string" ? value.trim().replace(/\s+/g, " ") : "";
}

function validateHtml(html, state, wave, intent, findings) {
  if (html.length < 3000) finding(findings, "HTML", "command_center.html is too thin to be an operational command center.");
  if (!/<meta[^>]+name=["']viewport["']/i.test(html)) finding(findings, "HTML", "The command center needs a viewport meta tag.");
  if (!/@media\b/i.test(html)) finding(findings, "HTML", "The command center needs responsive styling.");
  const assetReferences = [...html.matchAll(/\b(?:src|href)\s*=\s*["']([^"']+)["']/gi)].map((match) => match[1]);
  const externalAsset = assetReferences.some((value) => !value.startsWith("#") && !value.startsWith("data:"));
  const cssReferences = [...html.matchAll(/url\(\s*["']?([^"')]+)["']?\s*\)/gi)].map((match) => match[1].trim());
  const externalCss = /@import\b/i.test(html) || cssReferences.some((value) => !value.startsWith("#") && !value.startsWith("data:"));
  if (externalAsset || externalCss || /<script[^>]+src=/i.test(html) || /<link\b/i.test(html)) {
    finding(findings, "HTML", "The command center must be self-contained with no external assets.");
  }
  const match = /<script\s+id=["']mission-state["']\s+type=["']application\/json["']\s*>([\s\S]*?)<\/script>/i.exec(html);
  if (!match) {
    finding(findings, "EMBED", "Missing <script id=\"mission-state\" type=\"application/json\">.");
  } else {
    try {
      const embedded = JSON.parse(match[1]);
      if (!isDeepStrictEqual(embedded, state)) finding(findings, "EMBED", "Embedded mission state differs from mission_state.json.");
    } catch (error) {
      finding(findings, "EMBED", `Embedded mission state is invalid JSON: ${error.message}`);
    }
  }
  const visible = visibleText(html);
  const visibleMarker = unfinishedMarker(visible);
  if (visibleMarker) finding(findings, "PLACEHOLDER", `Visible command center contains unfinished template text: ${visibleMarker}.`);
  for (const label of ["current readiness", "top actions", "next 90 minutes", "resource", "incidents", "evidence", "assumptions"]) {
    if (!visible.toLowerCase().includes(label)) finding(findings, "HTML_SECTION", `Visible command center is missing '${label}'.`);
  }
  for (const id of expectedIds(wave)) {
    if (!visible.includes(id)) finding(findings, "HTML_EVIDENCE", `Visible evidence ledger is missing ${id}.`);
  }
  if (!visible.includes(state.resource_decision?.assignment ?? "")) finding(findings, "HTML_RESOURCE", "Visible page is missing the MPU-1 assignment.");
  const rationale = normalizedVisibleValue(state.resource_decision?.rationale);
  if (rationale && !visible.includes(rationale)) finding(findings, "HTML_RESOURCE", "Visible page is missing the MPU-1 rationale.");
  for (const action of Array.isArray(state.actions) ? state.actions : []) {
    const values = [action?.action, action?.owner, action?.due].map(normalizedVisibleValue).filter(Boolean);
    if (values.some((value) => !visible.includes(value))) {
      finding(findings, "HTML_ACTION", `Visible page is missing action detail for ${action?.action_id ?? "an action"}.`);
    }
  }
  for (const situation of Array.isArray(state.situations) ? state.situations : []) {
    const values = [situation?.id, situation?.status].map(normalizedVisibleValue).filter(Boolean);
    if (values.some((value) => !visible.includes(value))) {
      finding(findings, "HTML_SITUATION", `Visible page is missing situation detail for ${situation?.id ?? "a situation"}.`);
    }
  }
  const readinessValues = [state.readiness?.status, state.readiness?.summary].map(normalizedVisibleValue).filter(Boolean);
  if (readinessValues.some((value) => !visible.includes(value))) finding(findings, "HTML_READINESS", "Visible page is missing readiness detail.");
  for (const assumption of Array.isArray(state.assumptions) ? state.assumptions : []) {
    const value = normalizedVisibleValue(assumption);
    if (value && !visible.includes(value)) finding(findings, "HTML_ASSUMPTION", `Visible page is missing assumption: ${value}`);
  }
  if (wave === 2) {
    if (!visible.toLowerCase().includes("what changed")) finding(findings, "HTML_CHANGE", "Wave 2 page needs a visible 'What Changed' heading.");
    for (const label of ["NEW", "CHANGED", "CANCELLED", "UNCHANGED"]) {
      if (!visible.includes(label)) finding(findings, "HTML_CHANGE", `Visible page is missing ${label}.`);
    }
    if (!/before\s*\/\s*after|before and after|before.*after/i.test(visible)) finding(findings, "HTML_CHANGE", "Wave 2 page needs a visible before/after section.");
    const visibleIntent = intent.trim().replace(/\s+/g, " ");
    if (!visible.includes(visibleIntent)) finding(findings, "HTML_INTENT", "Wave 2 page must show the learner's intent.");
    for (const change of Array.isArray(state.changes) ? state.changes : []) {
      const summary = normalizedVisibleValue(change?.summary);
      if (summary && !visible.includes(summary)) finding(findings, "HTML_CHANGE", `Visible page is missing a ${change?.classification ?? "change"} summary.`);
    }
  }
}

export function verifyRun(runRootValue, expectedWave = undefined, options = {}) {
  const runRoot = safeRoot(runRootValue);
  const findings = [];
  if (!existsSync(runRoot) || !inside(runRoot, join(runRoot, "START_HERE.md"))) throw new Error("Run root is unavailable.");
  const wave = existsSync(join(runRoot, "incoming", "late_update.md")) ? 2 : 1;
  if (expectedWave !== undefined && Number(expectedWave) !== wave) finding(findings, "WAVE", `Expected Wave ${expectedWave}, found Wave ${wave}.`);
  const expectedRootEntries = [
    ".ignore", "START_HERE.md", "command_center.html", "incoming",
    "mission.yaml", "mission_state.json", "tools",
    ...(wave === 2 ? ["operator_intent.txt"] : []),
  ].sort();
  const actualRootEntries = readdirSync(runRoot).sort();
  const unexpectedRootEntries = actualRootEntries.filter((entry) => !expectedRootEntries.includes(entry));
  if (unexpectedRootEntries.length) {
    finding(findings, "OUTPUT_SET", `Remove extra root outputs: ${unexpectedRootEntries.join(", ")}.`);
  }
  compareAuthoritativeInputs(runRoot, wave, findings);

  if (regularFile(join(runRoot, "START_HERE.md"), findings, "START_HERE.md")) {
    const start = text(join(runRoot, "START_HERE.md"));
    if (!start.includes(`Wave: ${wave}`)) finding(findings, "WAVE", `START_HERE.md must show Wave: ${wave}.`);
  }
  const intentPath = join(runRoot, "operator_intent.txt");
  const intent = wave === 2 && regularFile(intentPath, findings, "operator_intent.txt") ? text(intentPath) : "";
  if (wave === 2 && !intent.trim()) finding(findings, "INTENT", "operator_intent.txt must not be empty.");

  let state = null;
  const statePath = join(runRoot, "mission_state.json");
  if (regularFile(statePath, findings, "mission_state.json")) {
    try {
      state = json(statePath);
    } catch (error) {
      finding(findings, "JSON", error.message);
    }
  }
  if (state && requireFields(state, ["wave", "as_of", "readiness", "resource_decision", "situations", "actions", "evidence", "assumptions", "changes", "operator_intent"], findings, "mission_state.json")) {
    validateNoPlaceholders(state, findings);
    if (state.wave !== wave) finding(findings, "STATE", `wave must be ${wave}.`);
    if (state.as_of !== (wave === 1 ? "06:30Z" : "06:48Z")) finding(findings, "STATE", `as_of must be ${wave === 1 ? "06:30Z" : "06:48Z"}.`);
    requireFields(state.readiness, ["status", "summary", "source_ids"], findings, "readiness");
    if (!nonEmpty(state.readiness?.status) || !nonEmpty(state.readiness?.summary)) finding(findings, "READINESS", "Readiness needs status and summary.");
    if (!Array.isArray(state.assumptions)) finding(findings, "ASSUMPTIONS", "assumptions must be an array.");
    const active = validateEvidence(state, wave, findings);
    validateSources([state.readiness], active, findings, "readiness");
    validateSituations(state, wave, active, findings);
    validateActions(state, wave, active, findings);
    validateResource(state, wave, active, findings);
    validateChanges(state, wave, intent, findings);
    const stateBlob = JSON.stringify(state);
    for (const person of ["Team Orbit", "Maya Chen"]) {
      if (!stateBlob.includes(person)) finding(findings, "PEOPLE", `mission_state must retain ${person}.`);
    }
  }

  const htmlPath = join(runRoot, "command_center.html");
  if (regularFile(htmlPath, findings, "command_center.html") && state) {
    validateHtml(text(htmlPath), state, wave, intent, findings);
  }

  const result = { ok: findings.length === 0, wave, findings, state };
  if (!options.quiet) {
    if (result.ok) {
      const current = expectedIds(wave).filter((id) => dispositionFor(id, wave)[0] === "ACTIVE").length;
      const suffix = wave === 2 ? " intent=APPLIED" : "";
      console.log(`P6 VERIFY PASS wave=${wave} evidence=${expectedIds(wave).length} current=${current} decision=${state.resource_decision.assignment}${suffix}`);
    } else {
      for (const item of findings) console.error(`P6 VERIFY HOLD ${item.code}: ${item.message}`);
      console.error(`P6 VERIFY HOLD wave=${wave} findings=${findings.length}`);
    }
  }
  return result;
}

function parseCli(argv) {
  const result = {};
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!["--run-root", "--wave"].includes(token) || argv[index + 1] === undefined) throw new Error(`Invalid argument: ${token}`);
    result[token.slice(2)] = argv[index + 1];
    index += 1;
  }
  return result;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const args = parseCli(process.argv.slice(2));
    const result = verifyRun(args["run-root"], args.wave === undefined ? undefined : Number(args.wave));
    if (!result.ok) process.exitCode = 1;
  } catch (error) {
    console.error(`P6 VERIFY HOLD RUNTIME: ${error.message}`);
    process.exitCode = 1;
  }
}
