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
import re
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
    "producer-rebuttal.md",
]
CHALLENGE_TOKENS = (
    "RCPT-8821",
    "accepted for processing",
    "R-17",
    "VX-240",
    "SYSTEM OVERRIDE",
)
PHASES = ("ingest", "register", "ledger", "challenge", "rebuttal", "packet", "change")


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


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def inbox_map() -> list[dict[str, str]]:
    return load_json(ROOT / "shared/case/INBOX_MAP.json")["sources"]


def course_manifest() -> list[dict[str, str]]:
    return load_json(ROOT / "shared/case/SOURCE_MANIFEST.json")["sources"]


def inbox_markdown(work: Path) -> list[Path]:
    folder = work / "inbox"
    return sorted(folder.glob("*.md")) if folder.is_dir() else []


def expected_hashes() -> dict[str, str]:
    by_id = {entry["id"]: entry["sha256"] for entry in course_manifest()}
    return {entry["inbox"]: by_id[entry["id"]] for entry in inbox_map()}


def load_register(work: Path) -> list[dict[str, str]]:
    with (work / "source-register.csv").open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def check_ingest(work: Path, check) -> None:
    files = inbox_markdown(work)
    check("inbox markdown count", len(files) == 9)
    wanted = expected_hashes()
    for name, digest in wanted.items():
        path = work / "inbox" / name
        actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ""
        source_id = next(entry["id"] for entry in inbox_map() if entry["inbox"] == name)
        check(f"source hash:{source_id}", path.exists() and actual == digest)


def check_register(work: Path, check) -> None:
    try:
        rows = load_register(work)
    except Exception:
        check("source register readable", False)
        return
    inbox_names = {path.name for path in inbox_markdown(work)}
    register_files = {row.get("file", "") for row in rows}
    check("nine inbox markdown files", len(inbox_names) == 9)
    check("source register covers all nine sources", inbox_names <= register_files)
    wanted = expected_hashes()
    for row in rows:
        name = row.get("file", "")
        path = work / "inbox" / name
        check(f"register file exists:{name}", bool(name) and path.exists())
        if name in wanted and path.exists():
            check(
                f"register hash:{name}",
                hashlib.sha256(path.read_bytes()).hexdigest() == wanted[name],
            )


def check_ledger(work: Path, check) -> None:
    try:
        baseline = load_rows(work / "thread-ledger.csv")
        changed = load_rows(work / "changed-thread-ledger.csv")
    except Exception as exc:
        print(f"HOLD: cannot read ledger — {exc}")
        raise
    steps = {row["step"] for row in baseline}
    for step in EXPECTED_STEPS:
        check(f"step:{step}", step in steps)
    check("all statement types allowed", all(row["statement_type"] in ALLOWED_TYPES for row in baseline + changed))
    check("all results allowed", all(row["result"] in ALLOWED_RESULTS for row in baseline + changed))
    check("unique baseline claim IDs", len({r["claim_id"] for r in baseline}) == len(baseline))
    check("source trace fields present", all(r["source_id"] and r["source_version"] and r["locator"] and r["source_excerpt"] and r["warrant"] for r in baseline if r["statement_type"] == "SOURCE FACT"))
    try:
        register_ids = {row.get("source_id", "") for row in load_register(work)}
        baseline_ids = {row["source_id"] for row in baseline if row.get("source_id")}
        changed_ids = {row["source_id"] for row in changed if row.get("source_id")}
        check("baseline source_ids appear in register", baseline_ids <= register_ids)
        changed_sources = set(register_ids)
        if "S10" in changed_ids:
            try:
                release = load_json(work / "change-release.json")
                change = work / "REVEALED_CHANGE.md"
                if (release.get("change_file") == change.name
                        and hashlib.sha256(change.read_bytes()).hexdigest() == release.get("change_sha256")):
                    changed_sources.add("S10")
            except (OSError, ValueError):
                pass
        check("changed source_ids have registered or revealed sources", changed_ids <= changed_sources)
    except Exception:
        check("source register readable", False)

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


def check_challenge(work: Path, check) -> None:
    path = work / "challenge-matrix.md"
    if not path.exists():
        check("challenge-matrix.md exists", False)
        return
    text = path.read_text(encoding="utf-8")
    for token in CHALLENGE_TOKENS:
        check(f"challenge:{token}", token in text)
    check("challenge:confidence", "96%" in text or "confidence" in text)


def check_rebuttal(work: Path, check) -> None:
    path = work / "producer-rebuttal.md"
    check("producer-rebuttal.md exists", path.exists())
    matrix = work / "challenge-matrix.md"
    text = matrix.read_text(encoding="utf-8") if matrix.exists() else ""
    check("challenge names producer-rebuttal", "producer-rebuttal" in text)

def check_packet(work: Path, check) -> None:
    path = work / "review.html"
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    check("review.html exists", path.exists())
    check("decision target", 'id="decision"' in text)


def check_change(work: Path, check) -> None:
    try:
        baseline = load_rows(work / "thread-ledger.csv")
        changed = load_rows(work / "changed-thread-ledger.csv")
    except Exception as exc:
        print(f"HOLD: cannot read ledger — {exc}")
        raise
    base_text = (work / "baseline-verdict.md").read_text(encoding="utf-8") if (work / "baseline-verdict.md").exists() else ""
    changed_text = (work / "changed-verdict.md").read_text(encoding="utf-8") if (work / "changed-verdict.md").exists() else ""
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

    prediction = (work / "change-prediction.md").read_text(encoding="utf-8") if (work / "change-prediction.md").exists() else ""
    for phrase in ("Fields that should change", "must not change", "still block", "Unexpected change"):
        check(f"prediction:{phrase}", phrase in prediction)

    route_rows = [row for row in changed if row["step"] == "Route window met"]
    check("v6 source present", any(re.search(r"\bv6\b", row["source_version"]) for row in route_rows))
    check("new closure present", any(
        "21:20Z" in row["claim"] + row["source_excerpt"] + row["calculation"]
        for row in route_rows
    ))
    check("permit remains pending", "Unchanged blockers:" in changed_text and "PENDING" in changed_text.upper())
    check("delivery remains unobserved", "Later event not yet observed:" in changed_text and "delivery" in changed_text.lower())

    baseline_by_id = {row["claim_id"]: row for row in baseline}
    changed_by_id = {row["claim_id"]: row for row in changed}
    check("claim ID set preserved", set(baseline_by_id) == set(changed_by_id))
    changed_route_ids = {
        claim_id for claim_id in baseline_by_id.keys() & changed_by_id.keys()
        if baseline_by_id[claim_id]["step"] == "Route window met"
        and baseline_by_id[claim_id] != changed_by_id[claim_id]
    }
    route_references = changed_route_ids | {"S10", "R71-2026-1006-v6"}
    route_columns = set(LEDGER_COLUMNS) - {"claim_id", "step", "statement_type"}
    explanation_columns = {"warrant", "uncertainty"}
    for claim_id in sorted(set(baseline_by_id) & set(changed_by_id)):
        before = baseline_by_id[claim_id]
        after = changed_by_id[claim_id]
        changed_columns = {column for column in LEDGER_COLUMNS if before[column] != after[column]}
        if not changed_columns:
            continue
        route_row = before["step"] == "Route window met"
        check(f"allowed step delta:{claim_id}", before["step"] == after["step"])
        allowed = route_columns if route_row else explanation_columns
        check(f"allowed column delta:{claim_id}", changed_columns <= allowed)
        if not route_row:
            explanation = " ".join(after[column] for column in changed_columns & explanation_columns)
            check(f"downstream revision citation:{claim_id}", any(
                re.search(rf"(?<!\w){re.escape(reference)}(?!\w)", explanation)
                for reference in route_references
            ))
    print("REVIEW: check current claims against their sources; quoted history and rejected identities are not automatically stale support.")


PHASE_CHECKS = {
    "ingest": check_ingest,
    "register": check_register,
    "ledger": check_ledger,
    "challenge": check_challenge,
    "rebuttal": check_rebuttal,
    "packet": check_packet,
    "change": check_change,
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workdir", type=Path)
    parser.add_argument("--phase", choices=[*PHASES, "all"], default="all")
    args = parser.parse_args()
    work = args.workdir.resolve()
    failed: list[str] = []
    passed: list[str] = []

    def check(name: str, condition: bool) -> None:
        (passed if condition else failed).append(name)

    selected = list(PHASES) if args.phase == "all" else [args.phase]
    if args.phase == "all":
        for name in REQUIRED_FILES:
            check(f"file:{name}", (work / name).exists())
        check_ingest(work, check)
        if failed:
            for name in failed:
                print(f"FAIL: {name}")
            print("HOLD: required practice files are missing")
            return 1
        selected = [phase for phase in PHASES if phase != "ingest"]

    try:
        for phase in selected:
            PHASE_CHECKS[phase](work, check)
    except Exception:
        return 1

    for name in passed:
        print(f"PASS: {name}")
    for name in failed:
        print(f"FAIL: {name}")
    if failed:
        print("HOLD: visible practice requirements failed; this is not the graded result")
        return 1
    if args.phase == "all":
        print("PASS: visible practice requirements passed; protected grading is still required")
    else:
        print(f"PASS: phase {args.phase}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
