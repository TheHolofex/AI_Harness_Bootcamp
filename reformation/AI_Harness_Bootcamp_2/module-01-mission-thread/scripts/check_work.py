#!/usr/bin/env python3
"""Visible mechanical checker for Module 1 practice work.

This checker does not judge source applicability, warrants, inferences, or the
professional quality of the verdict.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_STEPS = [
    "Requirement defined",
    "Cargo received",
    "Cargo released",
    "Vehicle made ready",
    "Movement authorized",
    "Route window met",
    "Cargo delivered",
    "Usable effect confirmed",
]
LEDGER_COLUMNS = [
    "step", "claim_id", "statement_type", "exact_entity", "entry_condition",
    "claim", "source_id", "source_version", "locator", "source_excerpt",
    "warrant", "calculation", "output_condition", "next_handoff",
    "uncertainty", "result",
]
ALLOWED_TYPES = {"SOURCE FACT", "CALCULATION", "INFERENCE", "DECISION", "UNSUPPORTED"}
ALLOWED_RESULTS = {"SUPPORTED", "CONTRADICTED", "UNRESOLVED", "NOT YET OCCURRED"}
REQUIRED_FILES = [
    "source-register.csv", "thread-ledger.csv", "challenge-matrix.md",
    "corrected-brief.md", "baseline-verdict.md", "change-prediction.md",
    "changed-thread-ledger.csv", "changed-brief.md", "changed-verdict.md", "handoff.md",
    "baseline-freeze.json", "change-release.json", "review.html",
]
CHALLENGES = [
    "Warehouse receipt offered as proof of usable inventory",
    "Accepted-for-processing receipt offered as permit approval",
    "Archived route bulletin offered as current",
    "R-17 community page offered for R-71",
    "VX-240 note offered for VX-204",
    "Instruction embedded inside a source",
    "Producer confidence and self-review",
]


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != LEDGER_COLUMNS:
            raise ValueError(f"wrong columns: {reader.fieldnames}")
        return list(reader)


def verdict(text: str) -> str:
    for value in ("ACCEPT", "REVISE", "REJECT", "HOLD"):
        if f"Verdict: {value}" in text:
            return value
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workdir", type=Path)
    args = parser.parse_args()
    work = args.workdir.resolve()
    failed: list[str] = []
    passed: list[str] = []

    def check(name: str, condition: bool) -> None:
        (passed if condition else failed).append(name)

    for name in REQUIRED_FILES:
        check(f"file:{name}", (work / name).exists())

    manifest_path = work / "case-packet/SOURCE_MANIFEST.json"
    manifest = {}
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for entry in manifest["sources"]:
            source = work / "case-packet/sources" / entry["file"]
            check(f"source hash:{entry['id']}", source.exists() and hashlib.sha256(source.read_bytes()).hexdigest() == entry["sha256"])
    except Exception:
        check("copied source manifest readable", False)

    if failed:
        for name in failed:
            print(f"FAIL: {name}")
        print("HOLD: required practice files are missing")
        return 1

    try:
        baseline = load_rows(work / "thread-ledger.csv")
        changed = load_rows(work / "changed-thread-ledger.csv")
    except Exception as exc:
        print(f"HOLD: cannot read ledger — {exc}")
        return 1

    steps = {row["step"] for row in baseline}
    for step in EXPECTED_STEPS:
        check(f"step:{step}", step in steps)
    check("all statement types allowed", all(row["statement_type"] in ALLOWED_TYPES for row in baseline + changed))
    check("all results allowed", all(row["result"] in ALLOWED_RESULTS for row in baseline + changed))
    check("unique baseline claim IDs", len({r["claim_id"] for r in baseline}) == len(baseline))
    check("source trace fields present", all(r["source_id"] and r["source_version"] and r["locator"] and r["source_excerpt"] and r["warrant"] for r in baseline if r["statement_type"] == "SOURCE FACT"))

    # Source-register completeness
    try:
        with (work / "source-register.csv").open(newline="", encoding="utf-8-sig") as handle:
            register_ids = {row["source_id"] for row in csv.DictReader(handle)}
        manifest_ids = {entry["id"] for entry in manifest["sources"]}
        check("source register covers all nine sources", manifest_ids <= register_ids)
    except Exception:
        check("source register readable", False)

    # Practice arithmetic — six explicit calculation records
    calc_rows = [row for row in baseline if row["statement_type"] == "CALCULATION"]
    check("six calculation records present", len(calc_rows) >= 6)
    check("calculations have explicit formulas", all(
        row["calculation"].strip()
        and row["calculation"].strip() != "none"
        and row["calculation"].strip() != row["claim"].strip()
        for row in calc_rows
    ))
    calc = subprocess.run(
        [sys.executable, str(ROOT / "scripts/compute_thread.py"), "--json"],
        capture_output=True,
        text=True,
    )
    check("reference calculations execute", calc.returncode == 0)
    practice_fields = "\n".join(
        " ".join(row.get(field, "") or "" for field in ("calculation", "claim", "result"))
        for row in baseline
    )
    check("practice scanned count 216", "216" in practice_fields)
    check("practice usable kits 180", "180" in practice_fields)
    check("practice mission payload 1404", "1404" in practice_fields or "1,404" in practice_fields)
    check("practice payload margin 246", "246" in practice_fields)
    check("practice v5 closure 14:50", "14:50" in practice_fields)
    check("practice earliest gate 14:53", "14:53" in practice_fields)

    challenge = (work / "challenge-matrix.md").read_text(encoding="utf-8")
    for heading in CHALLENGES:
        check(f"challenge:{heading}", heading in challenge)

    base_text = (work / "baseline-verdict.md").read_text(encoding="utf-8")
    changed_text = (work / "changed-verdict.md").read_text(encoding="utf-8")
    check("baseline verdict present", bool(verdict(base_text)))
    check("changed verdict present", bool(verdict(changed_text)))
    check("baseline verdict is HOLD", verdict(base_text) == "HOLD")
    check("changed verdict is HOLD", verdict(changed_text) == "HOLD")
    check("standing rule present", "Standing rule:" in base_text)

    freeze_path = work / "baseline-freeze.json"
    release_path = work / "change-release.json"
    check("baseline freeze exists", freeze_path.exists())
    check("change release exists", release_path.exists())
    freeze = {}
    release = {}
    if freeze_path.exists():
        try:
            freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
            hashes = {entry["file"]: entry["sha256"] for entry in freeze["files"]}
            for name in ("source-register.csv", "thread-ledger.csv", "challenge-matrix.md", "corrected-brief.md", "baseline-verdict.md", "change-prediction.md"):
                actual = hashlib.sha256((work / name).read_bytes()).hexdigest()
                check(f"frozen:{name}", hashes.get(name) == actual)
        except Exception:
            check("freeze record readable", False)
    if release_path.exists():
        try:
            release = json.loads(release_path.read_text(encoding="utf-8"))
            change_file = work / release["change_file"]
            check("revealed change hash", change_file.exists() and hashlib.sha256(change_file.read_bytes()).hexdigest() == release["change_sha256"])
            check("freeze precedes reveal", freeze.get("frozen_at_utc", "") < release.get("released_at_utc", ""))
        except Exception:
            check("change release record readable", False)

    prediction = (work / "change-prediction.md").read_text(encoding="utf-8")
    for phrase in ("Fields that should change", "must not change", "still block", "Unexpected change"):
        check(f"prediction:{phrase}", phrase in prediction)

    changed_brief = (work / "changed-brief.md").read_text(encoding="utf-8")
    changed_blob = "\n".join(",".join(row.values()) for row in changed) + "\n" + changed_brief + "\n" + changed_text
    check("v6 source present", "v6" in changed_blob or "R71-2026-1006-v6" in changed_blob)
    check("new closure present", "21:20Z" in changed_blob)
    changed_ledger_text = (work / "changed-thread-ledger.csv").read_text(encoding="utf-8")
    check("stale 20:50Z absent from changed ledger and conclusions", "20:50Z" not in changed_brief + changed_text + changed_ledger_text)
    check("wrong route absent from support", "R-17" not in changed_brief + changed_text)
    check("permit remains pending", "Unchanged blockers:" in changed_text and "PENDING" in changed_text.upper())
    check("delivery remains unobserved", "Later event not yet observed:" in changed_text and "delivery" in changed_text.lower())

    baseline_by_id = {row["claim_id"]: row for row in baseline}
    changed_by_id = {row["claim_id"]: row for row in changed}
    check("claim ID set preserved", set(baseline_by_id) == set(changed_by_id))
    allowed_changed_steps = {"Route window met"}
    allowed_changed_columns = {"claim", "source_id", "source_version", "locator", "source_excerpt", "warrant", "calculation", "output_condition", "uncertainty", "result"}
    for claim_id in sorted(set(baseline_by_id) & set(changed_by_id)):
        before = baseline_by_id[claim_id]
        after = changed_by_id[claim_id]
        changed_columns = {column for column in LEDGER_COLUMNS if before[column] != after[column]}
        if changed_columns:
            check(f"allowed step delta:{claim_id}", before["step"] in allowed_changed_steps and after["step"] in allowed_changed_steps)
            check(f"allowed column delta:{claim_id}", changed_columns <= allowed_changed_columns)

    for name in passed:
        print(f"PASS: {name}")
    for name in failed:
        print(f"FAIL: {name}")
    if failed:
        print("HOLD: visible practice requirements failed; this is not the graded result")
        return 1
    print("PASS: visible practice requirements passed; protected grading is still required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
