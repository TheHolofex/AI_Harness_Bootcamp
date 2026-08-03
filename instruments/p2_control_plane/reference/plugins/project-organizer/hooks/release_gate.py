#!/usr/bin/env python3
"""Deterministic Stop gate for the complete P2 Project Organizer release trio."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIRECTORY = PLUGIN_ROOT / "scripts"
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

from render_project_board import (  # noqa: E402
    BOARD_NAME,
    GATE_NAME,
    RECEIPT_NAME,
    STATE_NAME,
    TOOL_NAMES,
    EVIDENCE_DIRECTORY,
    atomic_write,
    build_receipt,
    dispatch,
    json_bytes,
    load_worker_reports,
    load_verifier,
    render_html,
    sha256_bytes,
)


TRIO = (STATE_NAME, BOARD_NAME, RECEIPT_NAME)
HEX_64 = re.compile(r"^[a-f0-9]{64}$")
UTC_TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
REVIEWER_REPORT_FILE = "board_reviewer.json"
REVIEWER_CHECKED_SECTIONS = [
    "outcome",
    "now_next",
    "ready_work",
    "launch_path",
    "blocked_work",
    "decision_queue",
    "unknowns",
    "source_coverage",
    "worker_reconciliation",
]


def regular_bytes(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"{path.name} must be a regular file, not a link")
    return path.read_bytes()


def load_object(content: bytes, name: str) -> Dict[str, Any]:
    try:
        value = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"{name} must be one UTF-8 JSON object") from error
    if not isinstance(value, dict):
        raise ValueError(f"{name} must contain one JSON object")
    return value


def validate_state_evidence(state: Mapping[str, Any]) -> List[str]:
    reports = state.get("worker_reports")
    if not isinstance(reports, dict) or set(reports) != {"scope_mapper", "dependency_planner"}:
        return ["worker_reports must bind the two required worker reports"]
    hashes: Dict[str, str] = {}
    for role, bundle in reports.items():
        if not isinstance(bundle, dict) or set(bundle) != {"sha256", "report"}:
            return [f"{role} worker report bundle has the wrong fields"]
        digest = bundle.get("sha256")
        if not isinstance(digest, str) or not HEX_64.fullmatch(digest):
            return [f"{role} worker report hash is invalid"]
        hashes[role] = digest
    expected = {
        "worker_reports_bound": 2,
        "mcp_tools_reported": list(TOOL_NAMES),
        "mcp_tools_basis": "two validated worker reports",
        "usage_visibility": "not exposed",
    }
    return [] if state.get("evidence_observations") == expected else [
        "evidence_observations must describe two hash-bound reports and the exact four-tool contract"
    ]


def validate_reviewer_report(
    root: Path,
    state: Mapping[str, Any],
    state_content: bytes,
    board_content: bytes,
) -> Tuple[Optional[str], List[str]]:
    control_root = root / EVIDENCE_DIRECTORY.parent
    evidence_root = root / EVIDENCE_DIRECTORY
    for directory in (control_root, evidence_root):
        if directory.is_symlink() or not directory.is_dir():
            return None, [f"Evidence folder must be a regular directory, not a link: {directory}"]
    path = evidence_root / REVIEWER_REPORT_FILE
    try:
        content = regular_bytes(path)
        report = load_object(content, REVIEWER_REPORT_FILE)
    except (OSError, ValueError) as error:
        return None, [str(error)]
    digest = sha256_bytes(content)
    expected_keys = {
        "role", "review", "source_fingerprint", "state_sha256", "board_sha256",
        "checked_sections", "findings",
    }
    failures: List[str] = []
    if set(report) != expected_keys:
        failures.append("board_reviewer report fields differ from the course contract")
    if report.get("role") != "board_reviewer":
        failures.append("board_reviewer report role is wrong")
    review = report.get("review")
    if review not in ("REVIEW: PASS", "REVIEW: HOLD"):
        failures.append("board_reviewer review must be REVIEW: PASS or REVIEW: HOLD")
    if report.get("source_fingerprint") != state.get("source_fingerprint"):
        failures.append("board_reviewer report is stale for the source fingerprint")
    if report.get("state_sha256") != sha256_bytes(state_content):
        failures.append("board_reviewer state hash does not bind the current candidate")
    if report.get("board_sha256") != sha256_bytes(board_content):
        failures.append("board_reviewer board hash does not bind the current candidate")
    if report.get("checked_sections") != REVIEWER_CHECKED_SECTIONS:
        failures.append("board_reviewer did not check the exact required board sections")
    findings = report.get("findings")
    source_ids = {
        item.get("source_id") for item in state.get("sources", []) if isinstance(item, dict)
    }
    blockers = 0
    if not isinstance(findings, list) or len(findings) > 4:
        failures.append("board_reviewer findings must be an array of zero to four items")
    else:
        for finding in findings:
            if not isinstance(finding, dict) or set(finding) != {"severity", "summary", "source_ids"}:
                failures.append("board_reviewer findings have the wrong fields")
                continue
            if finding.get("severity") not in ("blocker", "note"):
                failures.append("board_reviewer finding severity must be blocker or note")
            if finding.get("severity") == "blocker":
                blockers += 1
            summary = finding.get("summary")
            cited = finding.get("source_ids")
            if not isinstance(summary, str) or len(summary.strip()) < 20:
                failures.append("board_reviewer finding summary is too short to guide work")
            if (
                not isinstance(cited, list)
                or not cited
                or len(cited) != len(set(cited))
                or not set(cited).issubset(source_ids)
            ):
                failures.append("board_reviewer finding needs distinct declared source IDs")
    if review == "REVIEW: PASS" and blockers:
        failures.append("REVIEW: PASS cannot contain blocker findings")
    if review == "REVIEW: HOLD" and not blockers:
        failures.append("REVIEW: HOLD requires at least one blocker finding")
    valid_for_binding = not failures
    if review == "REVIEW: HOLD":
        failures.append("board_reviewer returned REVIEW: HOLD")
    return (digest if valid_for_binding else None), failures


def validate_measured_observations(value: Any) -> List[str]:
    if not isinstance(value, dict):
        return ["measured_observations must be an object"]
    failures = []
    for field in ("elapsed_seconds", "repairs"):
        item = value.get(field)
        if isinstance(item, bool) or not isinstance(item, int) or item < 0:
            failures.append(f"{field} must be a nonnegative measured integer")
    if value.get("elapsed_basis") != "project_ledger.sqlite3 mtime to board render":
        failures.append("elapsed_basis is missing or changed")
    if value.get("repairs_basis") != "release-gate HOLD requests carried by RUN_RECEIPT.json":
        failures.append("repairs_basis is missing or changed")
    return failures


def validate_state_parity(root: Path, state: Mapping[str, Any]) -> List[str]:
    failures: List[str] = []
    try:
        verification = load_verifier(root).verify_ledger(root)
        snapshot = dispatch(root, "get_project_snapshot", {})
        ready = dispatch(root, "get_ready_work", {})
        dependency = dispatch(root, "get_dependency_path", {"deliverable_id": "DLV-004"})
        decisions = dispatch(root, "get_decision_queue", {"limit": 10})
        fingerprints = {
            verification["source_fingerprint"], snapshot["source_fingerprint"],
            ready["source_fingerprint"], dependency["source_fingerprint"],
            decisions["source_fingerprint"],
        }
        if len(fingerprints) != 1:
            return ["the verifier and four MCP views do not share one source fingerprint"]
        worker_reports = load_worker_reports(root, snapshot, ready, dependency, decisions)
    except Exception as error:
        return [f"trusted state parity failed: {error}"]

    exact_fields = {
        "schema_version", "board_status", "ledger_status", "schema_status", "generated_at",
        "source_fingerprint", "as_of", "project", "counts", "now", "next",
        "launch_path", "launch_dependencies", "blocked_work", "decision_queue",
        "unknowns", "ready_work", "deliverables", "sources", "source_coverage",
        "mcp_tool_contract", "worker_reports", "evidence_observations", "measured_observations",
    }
    if set(state) != exact_fields:
        failures.append("PROJECT_STATE.json fields differ from the fixed candidate contract")
    expected_values = {
        "source_fingerprint": snapshot["source_fingerprint"],
        "as_of": snapshot["as_of"],
        "project": snapshot["project"],
        "counts": snapshot["counts"],
        "now": snapshot["now"],
        "next": snapshot["next"],
        "launch_path": dependency["launch_path"],
        "launch_dependencies": dependency["dependencies"],
        "blocked_work": [item for item in snapshot["deliverables"] if item["status"] == "blocked"],
        "decision_queue": decisions["decisions"],
        "unknowns": snapshot["unknowns"],
        "ready_work": ready["ready_work"],
        "deliverables": snapshot["deliverables"],
        "sources": snapshot["sources"],
        "source_coverage": {
            "declared": len(snapshot["sources"]),
            "represented": len(snapshot["sources"]),
            "status": "PASS",
        },
        "mcp_tool_contract": list(TOOL_NAMES),
        "worker_reports": worker_reports,
    }
    for field, expected in expected_values.items():
        if state.get(field) != expected:
            failures.append(f"PROJECT_STATE.json {field} differs from current verified data")
    return failures


def validate_board_markers(state: Mapping[str, Any], state_content: bytes, board_content: bytes) -> List[str]:
    try:
        board = board_content.decode("utf-8")
    except UnicodeDecodeError:
        return ["PROJECT_BOARD.html is not UTF-8"]
    failures: List[str] = []
    forbidden = (
        (r"<\s*script\b", "embedded scripts"),
        (r"<\s*(?:iframe|object|embed|link|base)\b", "external-loading HTML elements"),
        (r"\b(?:src|href)\s*=\s*['\"]\s*(?:https?:|//|data:|javascript:)", "external or executable references"),
        (r"@import\b", "CSS imports"),
        (r"url\s*\(", "CSS URL assets"),
        (r"http-equiv\s*=\s*['\"]?refresh", "automatic navigation"),
    )
    for pattern, label in forbidden:
        if re.search(pattern, board, flags=re.IGNORECASE):
            failures.append(f"PROJECT_BOARD.html cannot contain {label}")
    expected_board = render_html(state).encode("utf-8")
    if board_content != expected_board:
        failures.append("PROJECT_BOARD.html differs from the deterministic trusted render of PROJECT_STATE.json")
    required = [
        f'<meta name="project-state-sha256" content="{sha256_bytes(state_content)}">',
        "Ready now",
        "Source coverage",
        "Now and next",
        "Longest declared launch path",
        "Blocked work",
        "Decision queue",
        "Unknowns",
        "Scope and sequence findings",
        html.escape(str(state.get("generated_at", "")), quote=True),
        html.escape(str(state.get("project", {}).get("name", "")), quote=True),
        html.escape(str(state.get("project", {}).get("outcome", "")), quote=True),
    ]
    for collection in ("deliverables", "decision_queue", "unknowns", "sources", "launch_dependencies"):
        for item in state.get(collection, []):
            if not isinstance(item, dict):
                continue
            for key in ("deliverable_id", "decision_id", "source_id", "dependency_id"):
                if key in item:
                    required.append(html.escape(str(item[key]), quote=True))
    missing = sorted({value for value in required if value and value not in board})
    failures.extend(
        f"PROJECT_BOARD.html is missing required candidate marker: {value}" for value in missing
    )
    return failures


def independent_component_status(root: Path) -> Tuple[Dict[str, str], List[str]]:
    statuses = {"ledger_status": "UNKNOWN", "schema_status": "UNKNOWN", "board_status": "UNKNOWN"}
    failures: List[str] = []
    database = root / "project_ledger.sqlite3"
    try:
        if database.is_symlink() or not database.is_file():
            raise ValueError("project_ledger.sqlite3 must be a regular file")
        with sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True) as connection:
            connection.row_factory = sqlite3.Row
            connection.execute("PRAGMA query_only = ON")
            load_verifier(root).verify_schema(connection)
            integrity = connection.execute("PRAGMA integrity_check").fetchone()
            foreign_keys = connection.execute("PRAGMA foreign_key_check").fetchall()
        if tuple(integrity) != ("ok",) or foreign_keys:
            raise ValueError("SQLite integrity or foreign-key check failed")
        statuses["schema_status"] = "PASS"
    except (OSError, sqlite3.Error, ValueError) as error:
        statuses["schema_status"] = "FAIL"
        failures.append(f"schema verification failed: {error}")
    try:
        load_verifier(root).verify_ledger(root)
        statuses["ledger_status"] = "PASS"
    except Exception as error:
        statuses["ledger_status"] = "FAIL"
        failures.append(f"ledger verification failed: {error}")
    return statuses, failures


def validate_release(project_root: Path) -> Tuple[
    List[Dict[str, str]], List[str], Optional[Dict[str, Any]], bytes, bytes,
    Optional[Dict[str, Any]], Dict[str, str], Optional[str],
]:
    root = project_root
    checks: List[Dict[str, str]] = []
    failures: List[str] = []
    state: Optional[Dict[str, Any]] = None
    receipt: Optional[Dict[str, Any]] = None
    state_content = b""
    board_content = b""
    reviewer_report_sha256: Optional[str] = None
    component_status, component_failures = independent_component_status(root)
    failures.extend(component_failures)
    if component_status["schema_status"] == "PASS":
        checks.append({"check": "schema", "status": "PASS", "detail": "exact tables, integrity, and foreign keys pass"})
    if component_status["ledger_status"] == "PASS":
        checks.append({"check": "ledger", "status": "PASS", "detail": "source hashes and project relationships pass"})

    try:
        state_content = regular_bytes(root / STATE_NAME)
        state = load_object(state_content, STATE_NAME)
        checks.append({"check": "state JSON", "status": "PASS", "detail": "regular UTF-8 JSON object"})
    except (OSError, ValueError) as error:
        failures.append(str(error))
    try:
        board_content = regular_bytes(root / BOARD_NAME)
        board_content.decode("utf-8")
        checks.append({"check": "board HTML", "status": "PASS", "detail": "regular UTF-8 file"})
    except (OSError, UnicodeDecodeError, ValueError) as error:
        failures.append(f"{BOARD_NAME}: {error}")
    try:
        receipt_content = regular_bytes(root / RECEIPT_NAME)
        receipt = load_object(receipt_content, RECEIPT_NAME)
        checks.append({"check": "receipt JSON", "status": "PASS", "detail": "regular UTF-8 JSON object"})
    except (OSError, ValueError) as error:
        failures.append(str(error))

    if state is not None:
        expected_statuses = {"board_status": "CANDIDATE", "ledger_status": "PASS", "schema_status": "PASS"}
        for field, expected in expected_statuses.items():
            if state.get(field) != expected:
                failures.append(f"{field} must be {expected}")
        if state.get("schema_version") != "1.0":
            failures.append("schema_version must be 1.0")
        if not isinstance(state.get("generated_at"), str) or not UTC_TIMESTAMP.fullmatch(state["generated_at"]):
            failures.append("generated_at must be a second-precision UTC timestamp")
        coverage = state.get("source_coverage")
        if coverage != {"declared": 6, "represented": 6, "status": "PASS"}:
            failures.append("source_coverage must show all six declared sources represented")
        if state.get("mcp_tool_contract") != list(TOOL_NAMES):
            failures.append("mcp_tool_contract must contain exactly the four read-only tools")
        failures.extend(validate_state_evidence(state))
        failures.extend(validate_measured_observations(state.get("measured_observations")))
        unknowns = state.get("unknowns")
        if not isinstance(unknowns, list) or not any(
            isinstance(item, dict)
            and item.get("field") == "DEC-002.decision_owner"
            and item.get("value") == "Not assigned in source"
            for item in unknowns
        ):
            failures.append("the explicit DEC-002 decision-owner unknown is missing")
        parity_failures = validate_state_parity(root, state)
        failures.extend(parity_failures)
        if not parity_failures:
            checks.append({"check": "ledger parity", "status": "PASS", "detail": "state matches current trusted data queries"})
        if board_content:
            board_failures = validate_board_markers(state, state_content, board_content)
            if board_failures:
                failures.extend(board_failures)
                component_status["board_status"] = "HOLD"
            else:
                component_status["board_status"] = "CANDIDATE"
                checks.append({
                    "check": "board bindings",
                    "status": "PASS",
                    "detail": "HTML exactly matches the deterministic trusted render and contains no network surface",
                })

    if state is not None and state_content and board_content:
        reviewer_report_sha256, reviewer_failures = validate_reviewer_report(
            root, state, state_content, board_content
        )
        failures.extend(reviewer_failures)
        if not reviewer_failures:
            checks.append({
                "check": "board review",
                "status": "PASS",
                "detail": "current REVIEW: PASS binds the exact candidate hashes",
            })

    if receipt is not None and state is not None and board_content:
        if receipt.get("gate") != GATE_NAME:
            failures.append("receipt gate name is wrong")
        if receipt.get("status") not in ("PENDING", "PASS", "HOLD"):
            failures.append("receipt status must be PENDING, PASS, or HOLD")
        if receipt.get("gate_status") not in ("PENDING", "PASS", "FAIL"):
            failures.append("receipt gate_status must be PENDING, PASS, or FAIL")
        if receipt.get("state_sha256") != sha256_bytes(state_content):
            failures.append("receipt state_sha256 does not bind the current state bytes")
        if receipt.get("board_sha256") != sha256_bytes(board_content):
            failures.append("receipt board_sha256 does not bind the current board bytes")
        if receipt.get("status") in ("PENDING", "PASS"):
            expected_board_status = "RELEASE" if receipt.get("status") == "PASS" else state.get("board_status")
            if receipt.get("board_status") != expected_board_status:
                failures.append("receipt board_status does not match its release phase")
            for field in ("ledger_status", "schema_status", "source_fingerprint"):
                if receipt.get(field) != state.get(field):
                    failures.append(f"receipt {field} does not match state")
            if receipt.get("measured_observations") != state.get("measured_observations"):
                failures.append("receipt measured_observations do not match state")
            worker_hashes = {
                role: bundle["sha256"] for role, bundle in state.get("worker_reports", {}).items()
                if isinstance(bundle, dict) and isinstance(bundle.get("sha256"), str)
            }
            expected_evidence = {
                "worker_report_sha256": worker_hashes,
                "reviewer_report_sha256": (
                    reviewer_report_sha256 if receipt.get("status") == "PASS" else "not available"
                ),
                "agent_reports_bound": 3 if receipt.get("status") == "PASS" else 2,
                "mcp_tools_reported": list(TOOL_NAMES),
                "mcp_tools_basis": "validated worker reports",
                "usage_visibility": "not exposed",
            }
            if receipt.get("evidence") != expected_evidence:
                failures.append("receipt evidence does not bind the current worker and reviewer reports")
        elif receipt.get("gate_status") != "FAIL":
            failures.append("a HOLD receipt must have gate_status FAIL")
        if not failures:
            checks.append({"check": "receipt bindings", "status": "PASS", "detail": "hashes and observations match current artifacts"})

    if component_status["board_status"] == "UNKNOWN" and any(
        "BOARD" in failure or "board" in failure or "state" in failure
        for failure in failures
    ):
        component_status["board_status"] = "HOLD"
    return (
        checks, failures, state, state_content, board_content, receipt,
        component_status, reviewer_report_sha256,
    )


def failure_fingerprint(failures: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(sorted(failures)).encode("utf-8")).hexdigest()


def hold_receipt(
    root: Path,
    state: Optional[Mapping[str, Any]],
    state_content: bytes,
    board_content: bytes,
    prior: Optional[Mapping[str, Any]],
    failures: Sequence[str],
    component_status: Mapping[str, str],
    request_repair: bool,
    reviewer_report_sha256: Optional[str],
) -> Dict[str, Any]:
    previous_measured = (prior or {}).get("measured_observations", {})
    state_measured = (state or {}).get("measured_observations", {})
    repairs = previous_measured.get("repairs", state_measured.get("repairs", 0))
    if isinstance(repairs, bool) or not isinstance(repairs, int) or repairs < 0:
        repairs = 0
    fingerprint = failure_fingerprint(failures)
    if request_repair and repairs == 0:
        repairs = 1
    elapsed = state_measured.get("elapsed_seconds", previous_measured.get("elapsed_seconds", 0))
    if isinstance(elapsed, bool) or not isinstance(elapsed, int) or elapsed < 0:
        elapsed = 0
    source_fingerprint = (state or {}).get("source_fingerprint", "not available")
    if not isinstance(source_fingerprint, str) or not HEX_64.fullmatch(source_fingerprint):
        source_fingerprint = "not available"
    return {
        "gate": GATE_NAME,
        "status": "HOLD",
        "gate_status": "FAIL",
        "board_status": component_status.get("board_status", "UNKNOWN"),
        "ledger_status": component_status.get("ledger_status", "UNKNOWN"),
        "schema_status": component_status.get("schema_status", "UNKNOWN"),
        "source_fingerprint": source_fingerprint,
        "state_sha256": sha256_bytes(state_content) if state_content else "not available",
        "board_sha256": sha256_bytes(board_content) if board_content else "not available",
        "evidence": {
            "worker_report_sha256": {
                role: bundle.get("sha256")
                for role, bundle in (state or {}).get("worker_reports", {}).items()
                if isinstance(bundle, dict) and isinstance(bundle.get("sha256"), str)
            },
            "reviewer_report_sha256": reviewer_report_sha256 or "not available",
            "agent_reports_bound": (
                3 if reviewer_report_sha256 else
                (2 if isinstance((state or {}).get("worker_reports"), dict) else 0)
            ),
            "mcp_tools_reported": list(TOOL_NAMES),
            "mcp_tools_basis": "validated worker reports" if state else "not available",
            "usage_visibility": "not exposed",
        },
        "measured_observations": {
            "elapsed_seconds": elapsed,
            "elapsed_basis": "project_ledger.sqlite3 mtime to board render",
            "repairs": repairs,
            "repairs_basis": "release-gate HOLD requests carried by RUN_RECEIPT.json",
        },
        "failure_fingerprint": fingerprint,
        "checks": [
            {"check": "release", "status": "FAIL", "detail": failure}
            for failure in failures
        ],
    }


def trio_present(root: Path) -> bool:
    return all((root / name).exists() or (root / name).is_symlink() for name in TRIO)


def resolve_unlinked_root(value: str) -> Path:
    requested = Path(value).expanduser().absolute()
    if requested.is_symlink() or not requested.is_dir():
        raise ValueError(f"Project root must be a regular directory, not a link: {requested}")
    return requested.resolve()


def run_gate(root: Path, *, request_repair: bool) -> Tuple[bool, List[str]]:
    (
        checks, failures, state, state_content, board_content, prior,
        component_status, reviewer_report_sha256,
    ) = validate_release(root)
    if failures:
        receipt = hold_receipt(
            root,
            state,
            state_content,
            board_content,
            prior,
            failures,
            component_status,
            request_repair,
            reviewer_report_sha256,
        )
        atomic_write(root / RECEIPT_NAME, json_bytes(receipt))
        return False, failures
    assert state is not None
    pass_receipt = build_receipt(
        state,
        state_content,
        board_content,
        status="PASS",
        gate_status="PASS",
        checks=checks,
        reviewer_report_sha256=reviewer_report_sha256,
    )
    atomic_write(root / RECEIPT_NAME, json_bytes(pass_receipt))
    return True, []


def automatic_main() -> int:
    raw = sys.stdin.read()
    try:
        event = json.loads(raw) if raw.strip() else {}
        if not isinstance(event, dict) or not isinstance(event.get("cwd"), str):
            print("{}")
            return 0
        root = resolve_unlinked_root(event["cwd"])
    except (json.JSONDecodeError, OSError, ValueError):
        print("{}")
        return 0
    if not trio_present(root):
        print("{}")
        return 0
    prior_repairs = 0
    try:
        prior_receipt = load_object(regular_bytes(root / RECEIPT_NAME), RECEIPT_NAME)
        value = prior_receipt.get("measured_observations", {}).get("repairs", 0)
        if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
            prior_repairs = value
    except (OSError, ValueError, AttributeError):
        pass
    stop_hook_active = event.get("stop_hook_active") is True
    passed, failures = run_gate(root, request_repair=not stop_hook_active)
    if passed:
        print("{}")
        return 0
    reason = "Project Organizer is on HOLD: " + "; ".join(failures[:4])
    if stop_hook_active or prior_repairs >= 1:
        print(json.dumps({"systemMessage": reason + ". No second repair loop was started."}))
    else:
        print(json.dumps({"decision": "block", "reason": reason + ". Repair the listed release issue, rerender, and check once."}))
    return 0


def manual_main(project_root: str) -> int:
    try:
        root = resolve_unlinked_root(project_root)
        _, failures, _, _, _, _, _, _ = validate_release(root)
    except (OSError, ValueError) as error:
        print(
            "HOLD Project Organizer source-package diagnosis; "
            f"no artifacts changed; not release authority: {error}"
        )
        return 1
    if not failures:
        print(
            "PASS Project Organizer source-package diagnosis; "
            "no artifacts changed; not release authority"
        )
        return 0
    print(
        "HOLD Project Organizer source-package diagnosis; "
        "no artifacts changed; not release authority"
    )
    for failure in failures:
        print(f"- {failure}")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Diagnose the source package without writing artifacts or claiming installed release",
    )
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()
    return manual_main(args.project_root) if args.check else automatic_main()


if __name__ == "__main__":
    raise SystemExit(main())
