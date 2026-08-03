#!/usr/bin/env python3
"""End-to-end and mutation tests for the P2 Project Organizer reference."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence


REFERENCE = Path(__file__).resolve().parents[1]
KIT = REFERENCE.parent
STARTER = KIT / "starter"
PLUGIN = REFERENCE / "plugins" / "project-organizer"
PYTHON = Path(sys.executable).resolve()
CHECKED_SECTIONS = [
    "outcome", "now_next", "ready_work", "launch_path", "blocked_work",
    "decision_queue", "unknowns", "source_coverage", "worker_reconciliation",
]


def run(
    args: Sequence[object],
    *,
    cwd: Path,
    input_text: str | None = None,
    expected: int = 0,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [str(value) for value in args],
        cwd=cwd,
        input=input_text,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    if result.returncode != expected:
        raise AssertionError(
            f"command returned {result.returncode}, expected {expected}: {args!r}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def copytree(source: Path, destination: Path) -> None:
    shutil.copytree(
        source,
        destination,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("node_modules", "__pycache__", "*.pyc"),
    )


def assemble(root: Path) -> None:
    copytree(STARTER, root)
    for filename in ("schema.sql", "build_project_ledger.py", "verify_project_ledger.py", "configure_project_organizer.ps1"):
        shutil.copy2(REFERENCE / filename, root / filename)
    copytree(PLUGIN, root / "plugins" / "project-organizer")
    copytree(REFERENCE / ".codex" / "agents", root / ".codex" / "agents")
    shutil.copy2(
        REFERENCE / ".agents" / "plugins" / "marketplace.json",
        root / ".agents" / "plugins" / "marketplace.json",
    )


def build(root: Path, *, rebuild: bool = False, expected: int = 0) -> subprocess.CompletedProcess[str]:
    args: list[object] = [PYTHON, root / "build_project_ledger.py", "--project-root", root]
    if rebuild:
        args.append("--rebuild")
    return run(args, cwd=root, expected=expected)


def verify(root: Path, *, expected: int = 0) -> subprocess.CompletedProcess[str]:
    return run([PYTHON, root / "verify_project_ledger.py", "--project-root", root], cwd=root, expected=expected)


def query(root: Path, tool: str, arguments: Mapping[str, Any]) -> Dict[str, Any]:
    result = run(
        [
            PYTHON,
            root / "plugins" / "project-organizer" / "mcp" / "query_ledger.py",
            root,
            tool,
            json.dumps(arguments),
        ],
        cwd=root,
    )
    return json.loads(result.stdout)


def write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def release_and_evidence_snapshot(root: Path) -> Dict[str, Any]:
    relative_paths = (
        "PROJECT_STATE.json",
        "PROJECT_BOARD.html",
        "RUN_RECEIPT.json",
        ".project-organizer/evidence/scope_mapper.json",
        ".project-organizer/evidence/dependency_planner.json",
        ".project-organizer/evidence/board_reviewer.json",
    )
    snapshot: Dict[str, Any] = {}
    for relative in relative_paths:
        path = root / relative
        if not path.exists():
            snapshot[relative] = None
            continue
        content = path.read_bytes()
        snapshot[relative] = {
            "sha256": hashlib.sha256(content).hexdigest(),
            "content": content,
        }
    return snapshot


def create_worker_reports(root: Path, *, verdict: str = "PASS") -> str:
    snapshot = query(root, "get_project_snapshot", {})
    ready = query(root, "get_ready_work", {})
    dependency = query(root, "get_dependency_path", {"deliverable_id": "DLV-004"})
    decisions = query(root, "get_decision_queue", {"limit": 10})
    fingerprint = snapshot["source_fingerprint"]
    assert {
        fingerprint,
        ready["source_fingerprint"],
        dependency["source_fingerprint"],
        decisions["source_fingerprint"],
    } == {fingerprint}
    evidence = root / ".project-organizer" / "evidence"
    write_json(evidence / "scope_mapper.json", {
        "role": "scope_mapper",
        "verdict": verdict,
        "source_fingerprint": fingerprint,
        "tools_used": ["get_project_snapshot", "get_decision_queue"],
        "project_id": snapshot["project"]["project_id"],
        "deliverable_ids": [item["deliverable_id"] for item in snapshot["deliverables"]],
        "decision_ids": [item["decision_id"] for item in decisions["decisions"]],
        "unknown_ids": [item["field"] for item in snapshot["unknowns"]],
        "findings": [{
            "summary": "The active tabletop controls the blocked launch kit and keeps one threshold owner explicitly unknown.",
            "source_ids": ["SRC-002", "SRC-004", "SRC-005"],
        }],
    })
    write_json(evidence / "dependency_planner.json", {
        "role": "dependency_planner",
        "verdict": verdict,
        "source_fingerprint": fingerprint,
        "tools_used": ["get_ready_work", "get_dependency_path"],
        "ready_ids": [item["deliverable_id"] for item in ready["ready_work"]],
        "launch_path_ids": [item["deliverable_id"] for item in dependency["launch_path"]],
        "blocked_ids": [
            item["deliverable_id"] for item in dependency["launch_path"] if item["status"] == "blocked"
        ],
        "findings": [{
            "summary": "Complete the tabletop, resolve the fallback, and then practice before the go-live review can move.",
            "source_ids": ["SRC-002", "SRC-003"],
        }],
    })
    return fingerprint


def render(root: Path, *, expected: int = 0) -> subprocess.CompletedProcess[str]:
    return run(
        [
            PYTHON,
            root / "plugins" / "project-organizer" / "scripts" / "render_project_board.py",
            "--project-root",
            root,
        ],
        cwd=root,
        expected=expected,
    )


def create_reviewer(root: Path, fingerprint: str, *, review: str = "REVIEW: PASS") -> Path:
    findings = []
    if review == "REVIEW: HOLD":
        findings = [{
            "severity": "blocker",
            "summary": "The candidate hides the open threshold decision needed for the go-live review.",
            "source_ids": ["SRC-004"],
        }]
    path = root / ".project-organizer" / "evidence" / "board_reviewer.json"
    write_json(path, {
        "role": "board_reviewer",
        "review": review,
        "source_fingerprint": fingerprint,
        "state_sha256": sha256(root / "PROJECT_STATE.json"),
        "board_sha256": sha256(root / "PROJECT_BOARD.html"),
        "checked_sections": CHECKED_SECTIONS,
        "findings": findings,
    })
    return path


def manual_check(root: Path, *, expected: int = 0, hook: Path | None = None) -> subprocess.CompletedProcess[str]:
    hook_path = hook or (root / "plugins" / "project-organizer" / "hooks" / "release_gate.py")
    return run(
        [
            PYTHON,
            hook_path,
            "--check",
            "--project-root",
            root,
        ],
        cwd=root,
        expected=expected,
    )


def automatic_gate(
    root: Path,
    *,
    stop_hook_active: bool = False,
    hook: Path | None = None,
) -> Dict[str, Any]:
    hook_path = hook or (root / "plugins" / "project-organizer" / "hooks" / "release_gate.py")
    result = run(
        [PYTHON, hook_path],
        cwd=root,
        input_text=json.dumps({"cwd": str(root), "stop_hook_active": stop_hook_active}),
    )
    return json.loads(result.stdout)


def built_project(parent: Path, name: str) -> Path:
    root = parent / name
    root.mkdir()
    assemble(root)
    result = build(root)
    assert "Built project_ledger.sqlite3" in result.stdout
    assert verify(root).stdout.startswith("PASS project ledger:")
    return root


def test_happy_path(parent: Path) -> None:
    root = built_project(parent, "happy")
    fingerprint = create_worker_reports(root)
    render(root)
    state = json.loads((root / "PROJECT_STATE.json").read_text(encoding="utf-8"))
    receipt = json.loads((root / "RUN_RECEIPT.json").read_text(encoding="utf-8"))
    board = (root / "PROJECT_BOARD.html").read_text(encoding="utf-8")
    assert state["board_status"] == "CANDIDATE"
    assert receipt["status"] == "PENDING" and receipt["evidence"]["agent_reports_bound"] == 2
    for marker in (
        "Ready now", "Source coverage", "Generated at", "SRC-002 · SRC-005",
        "DEP-001 · SRC-003", "Scope and sequence findings", "Not assigned in source",
    ):
        assert marker in board, marker
    reviewer = create_reviewer(root, fingerprint)
    assert automatic_gate(root) == {}
    receipt = json.loads((root / "RUN_RECEIPT.json").read_text(encoding="utf-8"))
    assert (receipt["status"], receipt["gate_status"], receipt["board_status"]) == ("PASS", "PASS", "RELEASE")
    assert receipt["evidence"]["agent_reports_bound"] == 3
    assert receipt["evidence"]["reviewer_report_sha256"] == sha256(reviewer)
    assert receipt["evidence"]["mcp_tools_reported"] == [
        "get_project_snapshot", "get_ready_work", "get_dependency_path", "get_decision_queue",
    ]
    assert receipt["evidence"]["usage_visibility"] == "not exposed"


def test_manual_check_is_non_mutating(parent: Path) -> None:
    root = built_project(parent, "manual-check")
    fingerprint = create_worker_reports(root)
    render(root)
    create_reviewer(root, fingerprint)

    before_pass = release_and_evidence_snapshot(root)
    passed = manual_check(root)
    assert "not release authority" in passed.stdout
    assert release_and_evidence_snapshot(root) == before_pass
    receipt = json.loads((root / "RUN_RECEIPT.json").read_text(encoding="utf-8"))
    assert receipt["status"] == "PENDING" and receipt["gate_status"] == "PENDING"

    board = root / "PROJECT_BOARD.html"
    board.write_text(board.read_text(encoding="utf-8").replace("Ready now", "Work", 1), encoding="utf-8")
    before_failure = release_and_evidence_snapshot(root)
    failed = manual_check(root, expected=1)
    assert "no artifacts changed; not release authority" in failed.stdout
    assert release_and_evidence_snapshot(root) == before_failure

    absent_root = built_project(parent, "manual-check-no-receipt")
    absent_fingerprint = create_worker_reports(absent_root)
    render(absent_root)
    create_reviewer(absent_root, absent_fingerprint)
    (absent_root / "RUN_RECEIPT.json").unlink()
    before_absent = release_and_evidence_snapshot(absent_root)
    absent = manual_check(absent_root, expected=1)
    assert "RUN_RECEIPT.json" in absent.stdout
    assert release_and_evidence_snapshot(absent_root) == before_absent
    assert not (absent_root / "RUN_RECEIPT.json").exists()


def test_builder_and_schema_mutations(parent: Path) -> None:
    root = built_project(parent, "mutations")
    assert "Refusing to overwrite" in build(root, expected=1).stdout

    deliverables = root / "source_packet" / "02_deliverables.csv"
    original = deliverables.read_text(encoding="utf-8")
    deliverables.write_text(original.replace("in_progress,P0", "invented,P0", 1), encoding="utf-8")
    enum_failure = build(root, rebuild=True, expected=1).stdout
    assert "02_deliverables.csv record DLV-002" in enum_failure
    deliverables.write_text(original, encoding="utf-8")

    database = root / "project_ledger.sqlite3"
    with sqlite3.connect(database) as connection:
        connection.execute("UPDATE deliverables SET owner = ? WHERE deliverable_id = ?", ("Invented Owner", "DLV-002"))
    assert "deliverables values differ" in verify(root, expected=1).stdout
    build(root, rebuild=True)

    with sqlite3.connect(database) as connection:
        connection.execute("DROP INDEX idx_decisions_queue")
    assert "Required index is missing" in verify(root, expected=1).stdout
    build(root, rebuild=True)

    with sqlite3.connect(database) as connection:
        connection.execute("PRAGMA user_version = 0")
    assert "user_version must be 1" in verify(root, expected=1).stdout


def test_freshness_and_links(parent: Path) -> None:
    root = built_project(parent, "freshness")
    charter = root / "source_packet" / "01_project_charter.md"
    charter.write_text(charter.read_text(encoding="utf-8") + "\nchanged after build\n", encoding="utf-8")
    query_result = run(
        [
            PYTHON, root / "plugins" / "project-organizer" / "mcp" / "query_ledger.py",
            root, "get_project_snapshot", "{}",
        ],
        cwd=root,
        expected=1,
    )
    assert "Ledger/source verification failed" in query_result.stderr

    link_root = built_project(parent, "evidence-link")
    fingerprint = create_worker_reports(link_root)
    evidence = link_root / ".project-organizer" / "evidence"
    outside = parent / "outside-evidence"
    shutil.copytree(evidence, outside)
    shutil.rmtree(link_root / ".project-organizer")
    try:
        os.symlink(parent / "outside-evidence", link_root / ".project-organizer", target_is_directory=True)
    except (OSError, NotImplementedError):
        return
    failure = render(link_root, expected=1).stdout
    assert "Evidence folder must be a regular directory" in failure
    assert fingerprint


def test_reports_gate_and_repair_boundary(parent: Path) -> None:
    hold_root = built_project(parent, "review-hold")
    hold_fingerprint = create_worker_reports(hold_root)
    render(hold_root)
    reviewer = create_reviewer(hold_root, hold_fingerprint, review="REVIEW: HOLD")
    assert automatic_gate(hold_root).get("decision") == "block"
    receipt = json.loads((hold_root / "RUN_RECEIPT.json").read_text(encoding="utf-8"))
    assert receipt["evidence"]["reviewer_report_sha256"] == sha256(reviewer)
    assert receipt["evidence"]["agent_reports_bound"] == 3

    root = built_project(parent, "repair-boundary")
    fingerprint = create_worker_reports(root)
    render(root)
    create_reviewer(root, fingerprint)
    board = root / "PROJECT_BOARD.html"
    board.write_text(
        board.read_text(encoding="utf-8")
        .replace("Source coverage", "Sources", 1)
        .replace("</body>", '<script src="https://example.invalid/board.js"></script></body>'),
        encoding="utf-8",
    )
    first = automatic_gate(root, stop_hook_active=False)
    assert first.get("decision") == "block"
    receipt = json.loads((root / "RUN_RECEIPT.json").read_text(encoding="utf-8"))
    assert receipt["measured_observations"]["repairs"] == 1
    assert receipt["ledger_status"] == "PASS" and receipt["schema_status"] == "PASS"
    assert any("scripts" in item["detail"] or "external" in item["detail"] for item in receipt["checks"])

    render(root)
    create_reviewer(root, fingerprint)
    board.write_text(board.read_text(encoding="utf-8").replace("Source coverage", "Sources", 1), encoding="utf-8")
    second = automatic_gate(root, stop_hook_active=False)
    assert "decision" not in second and "No second repair loop" in second.get("systemMessage", "")
    receipt = json.loads((root / "RUN_RECEIPT.json").read_text(encoding="utf-8"))
    assert receipt["measured_observations"]["repairs"] == 1


def test_hook_never_executes_root_verifier(parent: Path) -> None:
    root = built_project(parent, "trust")
    fingerprint = create_worker_reports(root)
    render(root)
    create_reviewer(root, fingerprint)
    installed = parent / "installed-project-organizer"
    copytree(PLUGIN, installed)
    sentinels = []
    poison_targets = [
        root / "verify_project_ledger.py",
        root / "plugins" / "project-organizer" / "lib" / "ledger_verifier.py",
        root / "plugins" / "project-organizer" / "scripts" / "render_project_board.py",
        root / "plugins" / "project-organizer" / "hooks" / "release_gate.py",
    ]
    for index, target in enumerate(poison_targets, start=1):
        sentinel = root / f"LEARNER_CODE_EXECUTED_{index}"
        sentinels.append(sentinel)
        target.write_text(
            f"from pathlib import Path\nPath({str(sentinel)!r}).write_text('bad')\n",
            encoding="utf-8",
        )
    assert automatic_gate(root, hook=installed / "hooks" / "release_gate.py") == {}
    assert not any(path.exists() for path in sentinels), "installed Stop gate executed learner-owned Python"


def test_exact_render_requires_reviewed_plugin_refresh(parent: Path) -> None:
    root = built_project(parent, "render-refresh")
    fingerprint = create_worker_reports(root)
    render(root)
    create_reviewer(root, fingerprint)
    installed_old = parent / "installed-old"
    copytree(PLUGIN, installed_old)

    project_renderer = root / "plugins" / "project-organizer" / "scripts" / "render_project_board.py"
    original = project_renderer.read_text(encoding="utf-8")
    assert "--teal:#215c66" in original
    project_renderer.write_text(original.replace("--teal:#215c66", "--teal:#1f5a64", 1), encoding="utf-8")
    render(root)
    create_reviewer(root, fingerprint)
    old_check = manual_check(
        root,
        hook=installed_old / "hooks" / "release_gate.py",
        expected=1,
    )
    assert "differs from the deterministic trusted render" in old_check.stdout

    installed_updated = parent / "installed-updated"
    copytree(root / "plugins" / "project-organizer", installed_updated)
    updated_check = manual_check(
        root,
        hook=installed_updated / "hooks" / "release_gate.py",
    )
    assert updated_check.stdout.startswith("PASS Project Organizer source-package diagnosis")
    assert automatic_gate(root, hook=installed_updated / "hooks" / "release_gate.py") == {}


def test_inert_and_static_contract(parent: Path) -> None:
    root = parent / "inert"
    root.mkdir()
    assemble(root)
    hook = root / "plugins" / "project-organizer" / "hooks" / "release_gate.py"
    result = run([PYTHON, hook], cwd=root, input_text="not-json")
    assert json.loads(result.stdout) == {}
    result = run([PYTHON, hook], cwd=root, input_text=json.dumps({"cwd": str(root)}))
    assert json.loads(result.stdout) == {}

    assert not list(KIT.rglob(".mcp.json"))
    assert not (STARTER / "plugins").exists()
    assert not (STARTER / "project_ledger.sqlite3").exists()
    assert "reference" not in (KIT / "bootstrap.ps1").read_text(encoding="utf-8").split("$RequiredStarterFiles", 1)[1].split(")", 1)[0]
    manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert "hooks" not in manifest and "mcpServers" not in manifest
    package = json.loads((PLUGIN / "package.json").read_text(encoding="utf-8"))
    assert package["engines"]["node"] == ">=22.22 <25"
    assert package["dependencies"] == {"@modelcontextprotocol/server": "2.0.0", "zod": "4.4.3"}
    assert not ({"preinstall", "install", "postinstall", "prepare"} & set(package.get("scripts", {})))
    for agent in (REFERENCE / ".codex" / "agents").glob("*.toml"):
        text = agent.read_text(encoding="utf-8")
        assert 'model = "gpt-5.6-terra"' in text and 'sandbox_mode = "read-only"' in text


def run_installed_validators() -> None:
    system_skills = Path.home() / ".codex" / "skills" / ".system"
    plugin_validator = system_skills / "plugin-creator" / "scripts" / "validate_plugin.py"
    skill_validator = system_skills / "skill-creator" / "scripts" / "quick_validate.py"
    if plugin_validator.is_file():
        run([PYTHON, plugin_validator, PLUGIN], cwd=KIT)
    if skill_validator.is_file():
        run([PYTHON, skill_validator, PLUGIN / "skills" / "project-organizer"], cwd=KIT)


def main() -> int:
    run_installed_validators()
    with tempfile.TemporaryDirectory(prefix="p2-project-organizer-reference-") as temporary:
        parent = Path(temporary)
        test_happy_path(parent)
        test_manual_check_is_non_mutating(parent)
        test_builder_and_schema_mutations(parent)
        test_freshness_and_links(parent)
        test_reports_gate_and_repair_boundary(parent)
        test_hook_never_executes_root_verifier(parent)
        test_exact_render_requires_reviewed_plugin_refresh(parent)
        test_inert_and_static_contract(parent)
    print(
        "PASS P2 Project Organizer reference: source parity, read-only MCP, "
        "evidence-bound agents, visual candidate, and one-repair release gate"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
