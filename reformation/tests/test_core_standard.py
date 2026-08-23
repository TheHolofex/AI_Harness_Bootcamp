#!/usr/bin/env python3
"""Standard-tier static oracle for the bounded Reformation core skeleton.

The core is nine independent modules. The script checks structure, ownership, module
independence, supplied-input discipline, scope boundaries, and required semantic markers.
Criteria requiring delivery or contextual judgment are emitted as MANUAL and are not
silently promoted to PASS.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
REFERENCE = REPO / "docs/analysis/2026-08-09-reformation-core-standard-reference.md"
REFERENCE_SHA256 = "419a41a094673ac7cdc775b03c643ff8d8f6e50a680dc11ed8dea019713d0fc1"
SOURCE_LOG = REPO / "docs/analysis/gauntlet-standard/source-access-log.txt"
README = ROOT / "README.md"
MAP = ROOT / "COURSE_MAP.md"
OBJECTIVES = ROOT / "LEARNING_OBJECTIVES.md"
GUIDE = ROOT / "AUTHORING_GUIDE.md"
CORE_DIR = ROOT / "modules/core"

SUPPLY_PREFIXES = ("VERIFY:", "CUSTODY:")

FAILURES: list[str] = []
PASSES: list[str] = []
MANUAL: list[str] = []


def passed(cid: str, message: str) -> None:
    PASSES.append(f"{cid}: {message}")


def fail(cid: str, message: str) -> None:
    FAILURES.append(f"{cid}: {message}")


def require(cid: str, condition: bool, message: str) -> None:
    (passed if condition else fail)(cid, message)


def read(path: Path) -> str:
    if not path.exists():
        fail("S25", f"missing authoritative file {path.relative_to(REPO)}")
        return ""
    return path.read_text(encoding="utf-8")


def field(body: str, name: str) -> str | None:
    match = re.search(rf"^\*\*{re.escape(name)}:\*\*\s*(.+?)\s*$", body, re.MULTILINE)
    return match.group(1).strip() if match else None


def integer(value: str | None) -> int | None:
    if value is None:
        return None
    match = re.search(r"\d+", value)
    return int(match.group()) if match else None


def tokens(value: str | None) -> list[str]:
    if value is None:
        return []
    return [item.strip() for item in value.split(";") if item.strip()]


def broken_links(path: Path) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    body = read(path)
    for match in re.finditer(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", body):
        raw = match.group(1).split("#", 1)[0]
        if not raw or "://" in raw or raw.startswith("mailto:"):
            continue
        if not (path.parent / raw).resolve().exists():
            result.append((body.count("\n", 0, match.start()) + 1, match.group(1)))
    return result


# S01 — frozen Reference.
if REFERENCE.exists():
    digest = hashlib.sha256(REFERENCE.read_bytes()).hexdigest()
    require("S01", digest == REFERENCE_SHA256, f"Reference digest unchanged ({digest})")
else:
    fail("S01", "Standard Reference is missing")

readme = read(README)
course_map = read(MAP)
objectives = read(OBJECTIVES)
guide = read(GUIDE)
modules = sorted(CORE_DIR.glob("[0-9][0-9]-*.md")) if CORE_DIR.exists() else []
all_core = "\n".join((readme, course_map, objectives, guide, *(read(module) for module in modules)))

# S02 — bounded audience and role.
for phrase in ("professional domain user", "nondeveloper", "harness operator", "adapter", "builder"):
    require("S02", phrase in readme.lower() or phrase in guide.lower(), f"core names role {phrase!r}")

# S03 — primary-source field coverage and access log.
reference = read(REFERENCE)
official_links = set(re.findall(r"https://[^)\s]+", reference))
require("S03", len(official_links) >= 12, f"Reference links ≥12 official exemplars (found {len(official_links)})")
source_log = read(SOURCE_LOG) if SOURCE_LOG.exists() else ""
accessible = sum(1 for line in source_log.splitlines() if "\t200\t" in line)
require("S03", accessible >= 12, f"source access log records ≥12 HTTP 200 sources (found {accessible})")
for marker in ("Published contribution", "Confidence", "survey inferences"):
    require("S03", marker.lower() in reference.lower(), f"Reference separates/labels {marker}")

# S04/S05 — objective ownership and bounded module structure.
required_outcome_terms = {
    "delegation": ("delegate", "human"),
    "direction": ("direction", "constraints"),
    "source discernment": ("source", "verify", "inspect"),
    "context/control": ("context", "authority", "independent check"),
    "responsibility/tools": ("privacy", "copyright", "fairness", "affected", "authority"),
    "recovery": ("first failing", "recover"),
    "observed-run improvement": ("samples observed runs", "protected"),
    "fixed workflow": ("fixed workflow", "blast radius"),
    "variation-aware evaluation": ("variation", "repeated"),
    "transfer": ("clean-session", "independent person"),
}
for name, terms_required in required_outcome_terms.items():
    require("S04", all(term in objectives.lower() for term in terms_required), f"program outcomes cover {name}")
require("S04", objectives.lower().count("**evidence:**") >= len(modules), "all program outcomes name evidence")
require("S05", 1 <= len(modules) <= 10, f"core has 1–10 modules (found {len(modules)})")

primary: list[str] = []
facilitated = 0
practice = 0
module_lines = 0
produced: set[str] = set()
consumed: set[str] = set()
for module in modules:
    body = read(module)
    lines = len(body.splitlines())
    module_lines += lines
    require("S05", lines <= 110, f"{module.name} has ≤110 lines (found {lines})")
    po = field(body, "Primary objective")
    require("S05", po is not None, f"{module.name} has a Primary objective")
    if po:
        primary.append(po)
    enabling = re.findall(r"^\d+\.\s+", body, re.MULTILINE)
    require("S05", len(enabling) <= 3, f"{module.name} has ≤3 enabling objectives (found {len(enabling)})")
    h = integer(field(body, "Facilitated time"))
    p = integer(field(body, "Practice time"))
    require("S06", h is not None and p is not None, f"{module.name} declares facilitated/practice time")
    facilitated += h or 0
    practice += p or 0
    for manifest in ("Practical work", "Performance evidence", "Failure / HOLD", "Scope boundary", "Handoff", "Consumes", "Produces"):
        require("S19" if manifest in ("Performance evidence",) else "S14", field(body, manifest) is not None, f"{module.name} declares {manifest}")
    # Modules are independent: every consumed input is supplied from outside the core
    # and carries a prefix naming who confirms it.
    for item in tokens(field(body, "Consumes")):
        require("S14", item.startswith(SUPPLY_PREFIXES), f"{module.name} consumes only supplied input {item!r}")
        consumed.add(item)
    for item in tokens(field(body, "Produces")):
        require("S14", item not in produced, f"{module.name} uniquely produces {item!r}")
        produced.add(item)
    # A product must be created by graded work, not merely declared in a header or a
    # handoff sentence. The module's own claim result is established by its Gate.
    evidence_text = field(body, "Performance evidence") or ""
    gate_text = body.split("## Gate", 1)[-1] if "## Gate" in body else ""
    for item in tokens(field(body, "Produces")):
        if re.fullmatch(r"PO\d\d_RESULT", item):
            continue
        require("S14", item in evidence_text or item in gate_text,
                f"{module.name} evidences produced product {item!r}")

require("S05", len(primary) == len(set(primary)), "primary objective ownership is unique")
require("S05", module_lines <= 900, f"module skeleton totals ≤900 lines (found {module_lines})")
require("S14", not (produced & consumed), "no module consumes another module's product")

# Course-map product columns must exactly mirror module manifests. This closes the
# seam where a pretty map and individually valid modules can describe different courses.
map_rows = {
    match.group(1): (re.findall(r"`([^`]+)`", match.group(2)), re.findall(r"`([^`]+)`", match.group(3)))
    for match in re.finditer(
        r"^\|\s*(\d{2})\s*\|[^\n]*?\|\s*\d+h\s*/\s*\d+h\s*\|([^|]+)\|([^|]+)\|",
        course_map,
        re.MULTILINE,
    )
}
require("S14", len(map_rows) == len(modules), f"course map has one product row per module (found {len(map_rows)})")
for module in modules:
    mid = module.name[:2]
    map_consumes, map_produces = map_rows.get(mid, ([], []))
    require("S14", map_consumes == tokens(field(read(module), "Consumes")), f"{module.name} map/module Consumes agree")
    require("S14", map_produces == tokens(field(read(module), "Produces")), f"{module.name} map/module Produces agree")

# Machinery no learner can bring must arrive as a declared supply edge, not as an
# unstated assumption inside the consuming module.
required_verifications = {
    "VERIFY:PREFLIGHT", "VERIFY:CASE", "VERIFY:PROTECTED_ACCEPTANCE", "VERIFY:SOURCE_FIXTURES",
    "VERIFY:PROTECTED_GUARD", "VERIFY:CAPABILITY", "VERIFY:RESTORE_PATH", "VERIFY:RUN_SAMPLE",
    "VERIFY:PROTECTED_CONTROL", "VERIFY:BATCH_WORKLOAD", "VERIFY:SAVED_WORKFLOW",
    "VERIFY:BASELINE_CONFIG", "VERIFY:CANDIDATE", "VERIFY:PO_LEDGER",
}
require("S14", required_verifications.issubset(consumed), "adapter-supplied machinery has explicit verification edges")
# Items the learner must never inspect are custody, not learner checks.
required_custody = {"CUSTODY:HIDDEN_FAULT_ENV", "CUSTODY:CAPSTONE_CASES", "CUSTODY:RECIPIENT"}
require("S14", required_custody.issubset(consumed), "hidden and protected items are evaluator custody, not learner checks")
UNIVERSAL_ENTRY = {"VERIFY:PREFLIGHT", "VERIFY:CASE"}
for module in modules:
    body = read(module)
    work = (field(body, "Practical work") or "").lower()
    hold = (field(body, "Failure / HOLD") or "").lower()
    for item in tokens(field(body, "Consumes")):
        if not item.startswith("VERIFY:") or item in UNIVERSAL_ENTRY:
            continue
        words = [w for w in item.split(":", 1)[1].lower().split("_") if len(w) >= 4]
        require("S14", any(w in work for w in words), f"{module.name} performs its {item} check in Practical work")
        require("S14", "missing" in hold or "no supplied" in hold, f"{module.name} holds when its supplied input is absent")

# S06 — time design; empirical claims remain manual.
require("S06", 24 <= facilitated <= 35, f"facilitated time is 24–35 hours (found {facilitated})")
ratio = practice / facilitated if facilitated else 0
require("S06", ratio >= 0.60, f"practice is ≥60% (found {ratio:.1%})")
require("S06", "including practice" in course_map.lower(), "course map states practice is included in facilitated time")
require("S06", "within 60 minutes" in course_map.lower(), "first checked artifact is designed within 60 minutes")

# S07 — responsibility must precede consequential release. Modules 00-02 are pre-gate.
for early in modules[:3]:
    body = read(early).lower()
    denial = any(phrase in body for phrase in (
        "does not authorize consequential release",
        "no consequential release claim",
        "not consequential release",
    ))
    require("S07", "consequential release" not in body or denial, f"{early.name} does not permit consequential release")
    if "release" in body:
        require("S07", "bounded internal" in body or "minimum responsibility" in body or denial, f"{early.name} bounds any early release language")
require("S07", "minimum responsibility screen" in guide.lower() and "before" in guide.lower(), "guide requires minimum responsibility screen before release")

# S08/S09 — surfaces and progression.
for surface in ("communication artifact", "research/source", "structured-data/batch"):
    require("S08", surface in objectives.lower() and surface in course_map.lower(), f"surface {surface!r} has ledger coverage")
for stage in ("guided", "independent", "adversarial", "transferred"):
    require("S09", stage in course_map.lower(), f"progression names {stage}")
for invalid in ("file presence cannot", "simulation", "producer self-assessment"):
    require("S09", invalid in all_core.lower(), f"core rejects substitute evidence: {invalid}")

# S10 — complete, contextual responsible use.
for concern in ("privacy", "security", "copyright", "fairness", "transparency", "affected-person", "recourse", "human accountability"):
    require("S10", concern in objectives.lower() and concern in course_map.lower(), f"responsible release includes {concern}")
require("S10", "generic checklist" in all_core.lower() or "generic ethics" in all_core.lower(), "core rejects generic checklist/ethics evidence")
require("S10", "does not" in course_map.lower() and "legal" in course_map.lower(), "core disclaims universal legal conclusion")

# S11 — refusal is a decision claim; operation is mandatory and cannot be replaced by it.
m03 = read(modules[3]) if len(modules) > 3 else ""
for phrase in ("no-use", "no-release", "no-tool", "connection branch", "decision branch"):
    require("S11", phrase in m03.lower() or phrase in course_map.lower(), f"conditional decision/operation contract includes {phrase}")
require("S11", "every learner" in course_map.lower() and "connection branch" in course_map.lower(),
        "every learner completes the connection branch")
for phrase in ("does not satisfy", "does not replace"):
    require("S11", phrase in m03.lower() or phrase in course_map.lower(),
            f"supported refusal {phrase} the operation claim")

# S12/S13 — no hidden builder work; fixed flow is top of core.
for forbidden in ("learner implements", "learner builds an api", "learner builds an mcp", "learner builds a rag", "learner deploys"):
    require("S12", forbidden not in all_core.lower(), f"core omits required action {forbidden!r}")
for phrase in ("adapter implements", "learner specifies", "supplied protected control"):
    require("S12", phrase in all_core.lower(), f"core makes ownership explicit: {phrase}")
require("S13", "fixed workflow is the highest" in course_map.lower(), "fixed workflow is highest mandatory operation")
for mechanism in ("persistent state operation", "adaptive flow operation", "multi-agent operation"):
    require("S13", mechanism in course_map.lower() and "advanced" in course_map.lower(), f"{mechanism} is advanced")

# S15 — localization-only cannot complete recovery.
m04 = read(modules[4]) if len(modules) > 4 else ""
require("S15", "localization-only" in m04.lower() and "hold" in m04.lower(), "localization-only is held")
require("S15", all(term in m04.lower() for term in ("focused", "end-to-end", "clean")), "full recovery requires focused/end-to-end/clean evidence")

# S16 — learner specifies/configures; adapter owns dynamic implementation.
m05 = read(modules[5]) if len(modules) > 5 else ""
for phrase in ("mechanically decidable predicate", "configures", "adapter implements", "arbitrary semantic"):
    require("S16", phrase in m05.lower() or phrase in guide.lower(), f"observed-run boundary includes {phrase}")

# S17 — variation-aware exact delta and comparison.
m06 = read(modules[6]) if len(modules) > 6 else ""
m07 = read(modules[7]) if len(modules) > 7 else ""
require("S17", "deterministic outer" in m06.lower(), "workflow exact delta is scoped to deterministic outer state")
for phrase in ("variation", "repeated control", "before results"):
    require("S17", phrase in m07.lower() or phrase in objectives.lower(), f"change evaluation includes {phrase}")

# S18 — composed untrusted-content/tool-authority negative, performed by every learner.
for phrase in ("untrusted content", "tool authority", "unauthorized action", "authority expansion"):
    require("S18", phrase in m03.lower(), f"Module 03 composed negative includes {phrase}")

# S19 — protected evidence and tamper rule.
for module in modules:
    evidence = (field(read(module), "Performance evidence") or "").lower()
    require("S19", "protected" in evidence or "independent" in evidence, f"{module.name} names protected/independent evidence")
require("S19", all(term in all_core.lower() for term in ("cannot edit", "bypass", "select away")), "producer cannot edit/bypass/select away decisive checks")
require("S19", "independent or protected" in guide.lower(), "guide defines independent/protected evidence")

# S20/S21 — qualification closure and transfer separation.
m08 = read(modules[8]) if len(modules) > 8 else ""
for phrase in ("every program outcome", "reassessed", "continued participation", "final qualification"):
    require("S20", phrase in m08.lower() or phrase in course_map.lower(), f"qualification closure includes {phrase}")
require("S20", "VERIFY:PO_LEDGER" in tokens(field(m08, "Consumes")), "qualification verifies the outcome ledger")
require("S20", "RUNNABLE_PACKAGE" in tokens(field(m08, "Produces")), "capstone produces the transfer package")
require("S20", "unseen" in course_map.lower(), "reassessment uses an unseen protected case")
for phrase in ("clean-session", "independent-person", "cannot substitute", "first attempt", "no author coaching"):
    require("S21", phrase in m08.lower() or phrase in course_map.lower(), f"transfer contract includes {phrase}")
require("S21", "evaluator" in course_map.lower() and "has not completed this core" in course_map.lower(),
        "evaluator and recipient roles are defined")

# S22/S23 — degraded and scale policies (feasibility is manual).
for missing in ("model", "tool", "source", "protected fixture", "recipient", "accessible", "restore"):
    require("S22", missing in course_map.lower(), f"degraded policy names missing {missing}")
require("S22", "substitution record" in guide.lower(), "a substituted dependency leaves a record")
for phrase in ("double-scoring", "moderation", "appeals", "recipient capacity"):
    require("S23", phrase in course_map.lower(), f"10x policy accounts for {phrase}")

# S24/S25 — parsimony and internal integrity.
require("S24", "one evidence bundle per module" in readme.lower(), "one evidence bundle per module")
for banned in ("brier", "calibration series", "evidence ladder"):
    require("S24", banned not in all_core.lower(), f"core omits duplicate system {banned!r}")
require("S24", "PARTIAL" not in all_core, "claim states are PASS or HOLD only")
for path in (README, MAP, OBJECTIVES, GUIDE, *modules):
    require("S24", "Serves oracle" in read(path), f"{path.name} names served oracle criteria")
valid_ids = set(re.findall(r"\*\*(S\d\d)\*\*", reference))
for path in (README, MAP, OBJECTIVES, GUIDE, *modules):
    claimed = set(re.findall(r"S\d\d", (field(read(path), "Serves oracle") or "")))
    require("S24", claimed <= valid_ids, f"{path.name} claims only real oracle criteria ({sorted(claimed - valid_ids)})")
links: list[str] = []
for path in (README, MAP, OBJECTIVES, GUIDE, *modules):
    links.extend(f"{path.relative_to(REPO)}:{line}->{target}" for line, target in broken_links(path))
require("S25", not links, "zero broken relative links" + (": " + "; ".join(links) if links else ""))
ids = [p.name[:2] for p in modules]
require("S25", ids == [f"{i:02d}" for i in range(len(modules))], f"contiguous module IDs (found {ids})")
require("S25", all((field(read(p), "Primary objective") or "") in objectives for p in modules), "module primary objective strings appear in objective ledger")

# S26 — empirical honesty.
for phrase in ("provisional", "pilot", "unmeasured", "median", "p90", "agreement"):
    require("S26", phrase in course_map.lower(), f"budget policy labels/defines {phrase}")

MANUAL.extend([
    "S03 research judge: verify source facts/inferences and ≥12 materially distinct primary exemplars",
    "S04 curriculum judge: score every outcome observable, bounded, and singly owned",
    "S07 curriculum judge: confirm responsibility precedes consequential release",
    "S10 responsible-use judge: apply composed rights/affected-person/disclosure/authority case",
    "S11 curriculum judge: verify refusal is studied and operation is still performed by every learner",
    "S12 scope judge: classify every learner action and find zero builder/engineer requirements",
    "S14 prerequisite seam judge: confirm each supplied case makes its module's first action runnable alone",
    "S17 evaluation judge: review stochastic/repeated-control rules for the named decisions",
    "S18 adversarial judge: execute composed untrusted-content/tool-authority procedure when adapter exists",
    "S21 recipient judge: execute protected six-field first-attempt rubric when adapter exists",
    "S22/S23 scale-degradation judge: trace missing dependencies and 20/200 cohort policy",
    "S26 budget judge: declarations remain provisional until telemetry and agreement evidence exist",
])

print(f"PASS {len(PASSES)}")
for item in PASSES:
    print("  PASS", item)
print(f"MANUAL {len(MANUAL)}")
for item in MANUAL:
    print("  MANUAL", item)
print(f"FAIL {len(FAILURES)}")
for item in FAILURES:
    print("  FAIL", item)

sys.exit(1 if FAILURES else 0)
