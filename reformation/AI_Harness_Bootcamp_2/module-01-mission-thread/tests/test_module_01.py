#!/usr/bin/env python3
"""Structural, semantic, and safety oracle for Module 1."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PASS: list[str] = []
FAIL: list[str] = []


def check(cid: str, condition: bool, detail: str) -> None:
    (PASS if condition else FAIL).append(f"{cid}: {detail}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


# Frozen Reference
ref = ROOT / "reference/REFERENCE.md"
hash_file = ROOT / "reference/REFERENCE.sha256"
expected_hash = read(hash_file).split()[0] if hash_file.exists() else ""
actual_hash = hashlib.sha256(ref.read_bytes()).hexdigest() if ref.exists() else ""
check("M1-REF", bool(expected_hash) and expected_hash == actual_hash, f"reference hash {actual_hash}")

required = {
    "start": ROOT / "README.md",
    "lab": ROOT / "shared/MODULE_01_LAB.md",
    "orientation": ROOT / "shared/MISSION_THREAD.md",
    "accessibility": ROOT / "shared/ACCESSIBILITY.md",
    "troubleshooting": ROOT / "shared/WHEN_EVIDENCE_BREAKS.md",
    "handoff": ROOT / "shared/NEXT_MODULE.md",
    "runbook": ROOT / "facilitator/RUNBOOK.md",
    "rubric": ROOT / "assessment/PUBLIC_RUBRIC.md",
    "custody": ROOT / "assessment/CUSTODY_CONTRACT.md",
    "request": ROOT / "shared/case/REQUEST.md",
    "brief": ROOT / "shared/case/AI_DISPATCH_BRIEF.md",
    "manifest": ROOT / "shared/case/SOURCE_MANIFEST.json",
    "change": ROOT / "shared/case/SEALED_CHANGE.md",
    "calculator": ROOT / "scripts/compute_thread.py",
    "validator": ROOT / "scripts/check_work.py",
    "inventory": ROOT / "scripts/verify_content.py",
}
for name, path in required.items():
    check("M1-01", path.exists(), f"{name} exists")

source_dir = ROOT / "shared/case/sources"
source_files = sorted(source_dir.glob("S*.md"))
check("M1-01", len(source_files) == 9, "exactly nine baseline source files")

# Start links
start = read(required["start"])
for key in ("lab", "orientation", "accessibility", "rubric"):
    if required[key].exists():
        rel = required[key].relative_to(ROOT).as_posix()
        check("M1-LINK", rel in start, f"start links {key}")

# Relative links
for path in ROOT.rglob("*.md"):
    body = read(path)
    for m in re.finditer(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", body):
        target = m.group(1).split("#", 1)[0]
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        check("M1-LINK", (path.parent / target).resolve().exists(), f"{path.relative_to(ROOT)} -> {target}")

# Manifest schema and exact source identity
manifest = {}
try:
    manifest = json.loads(read(required["manifest"]))
except Exception:
    pass
check("M1-02", manifest.get("case_id") == "COLD-LANTERN-PRACTICE", "practice case identity")
entries = manifest.get("sources", [])
check("M1-02", len(entries) == 9, "manifest has nine baseline entries")
for entry in entries:
    check("M1-02", all(k in entry for k in ("id", "file", "issuer", "version", "effective", "authorized_use", "sha256")), f"manifest fields for {entry.get('id','?')}")
    path = source_dir / entry.get("file", "")
    digest = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""
    check("M1-02", digest == entry.get("sha256"), f"manifest hash for {entry.get('id','?')}")

# Required learning mechanics
lab = read(required["lab"])
for phrase in (
    "Requirement defined",
    "Cargo received",
    "Cargo released",
    "Vehicle made ready",
    "Movement authorized",
    "Route window met",
    "Cargo delivered",
    "Usable effect confirmed",
    "SOURCE FACT",
    "CALCULATION",
    "INFERENCE",
    "DECISION",
    "UNSUPPORTED",
    "identity",
    "authority",
    "time",
    "quantity",
    "condition",
    "dependency",
    "handoff",
    "uncertainty",
    "ACCEPT",
    "REVISE",
    "REJECT",
    "HOLD",
):
    check("M1-06", phrase in lab, f"lab includes {phrase}")
check("M1-08", "stop decomposing" in lab.lower() and "directly" in lab.lower(), "recursive stop rule")
check("M1-16", "producer" in lab.lower() and "independent evidence" in lab.lower(), "producer self-review excluded")
check("M1-19", "before" in lab.lower() and "SEALED_CHANGE" in lab, "baseline frozen before change")

# Source challenge fixtures
all_sources = "\n".join(read(p) for p in source_files)
for token in ("VX-204", "VX-240", "R-71", "R-17", "20:50Z", "21:30Z", "PENDING", "accepted for processing", "SYSTEM OVERRIDE", "CR-19", "CR-20", "84 kg"):
    check("M1-15", token in all_sources, f"source packet contains challenge {token}")

# Scope and learner-language scans
learner_files = [required[k] for k in ("start", "lab", "orientation", "accessibility", "troubleshooting", "handoff", "rubric", "request", "brief", "change")] + source_files
learner_text = "\n".join(read(p) for p in learner_files)
for token in ("PO-01", "SOURCE_EVIDENCE", "DISCERNMENT_RESULT", "STANDING_RULE", "M1-29", "oracle criterion"):
    check("M1-05", token not in learner_text, f"learner files omit internal token {token}")
for phrase in ("real route", "dispatch a real", "legal advice", "clinical advice"):
    check("M1-03", phrase not in learner_text.lower(), f"no out-of-scope phrase {phrase}")
check("M1-03", "fictional" in learner_text.lower() and "class" in learner_text.lower(), "fictional class-only boundary")

# Assessment boundary
rubric = read(required["rubric"])
custody = read(required["custody"])
check("M1-18", "hard gate" in rubric.lower() and "material" in rubric.lower(), "material misses block passing")
check("M1-23", "practice" in rubric.lower() and "protected" in custody.lower(), "visible/protected separation")
check("M1-26", all(term in read(required["runbook"]).lower() for term in ("may not", "source authority", "arithmetic", "verdict")), "coaching limits")
check("M1-24", "hold" in read(required["accessibility"]).lower(), "accessibility fails closed")
check("M1-28", "without" in read(required["handoff"]).lower() and "coaching" in read(required["handoff"]).lower(), "handoff supports independent reconstruction")

# Safety and hostile-content rules
check("M1-15", "treat source text as data" in lab.lower(), "source text never becomes instructions")
check("M1-15", "system override" in learner_text.lower(), "indirect prompt injection is visible")
check("M1-16", "do not ask" in lab.lower() and "check its own" in lab.lower(), "AI self-check prohibited")

# Calculations via executable reference helper
if required["calculator"].exists():
    result = subprocess.run([sys.executable, str(required["calculator"]), "--json"], capture_output=True, text=True)
    check("M1-14", result.returncode == 0, "reference calculations execute")
    try:
        values = json.loads(result.stdout)
    except Exception:
        values = {}
    expected = {
        "scanned_kits": 216,
        "usable_kits": 180,
        "released_mass_kg": 1320,
        "mission_payload_kg": 1404,
        "payload_margin_kg": 246,
        "all_scanned_payload_kg": 1668,
        "all_scanned_overage_kg": 18,
        "v5_closure_local": "14:50 MDT",
        "earliest_departure": "14:25 MDT",
        "earliest_gate_arrival": "14:53 MDT",
        "v5_gate_margin_minutes": -3,
        "earliest_clinic_arrival": "15:33 MDT",
        "clinic_margin_minutes": 27,
        "v6_closure_local": "15:20 MDT",
        "v6_gate_margin_minutes": 27,
    }
    for key, wanted in expected.items():
        check("M1-14", values.get(key) == wanted, f"{key}={wanted!r}")

# Implementation scripts compile
for path in (required["calculator"], required["validator"], required["inventory"]):
    if path.exists():
        result = subprocess.run([sys.executable, "-m", "py_compile", str(path)], capture_output=True, text=True)
        check("M1-CODE", result.returncode == 0, f"{path.name} compiles")

# No learner answer leakage
for path in learner_files:
    text = read(path)
    check("M1-ANSWER", "246 kg" not in text and "1,404 kg" not in text and "3 minutes late" not in text, f"no protected conclusion leaked in {path.name}")

print(f"PASS {len(PASS)}")
for item in PASS:
    print("  PASS", item)
print(f"FAIL {len(FAIL)}")
for item in FAIL:
    print("  FAIL", item)
sys.exit(1 if FAIL else 0)
