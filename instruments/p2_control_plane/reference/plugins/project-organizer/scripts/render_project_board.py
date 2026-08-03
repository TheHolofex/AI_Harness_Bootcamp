#!/usr/bin/env python3
"""Render the P2 visual project board and its evidence-bound release files."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import html
import json
import os
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
MCP_DIRECTORY = PLUGIN_ROOT / "mcp"
LIB_DIRECTORY = PLUGIN_ROOT / "lib"
if str(MCP_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(MCP_DIRECTORY))
if str(LIB_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(LIB_DIRECTORY))

from query_ledger import TOOL_NAMES, dispatch  # noqa: E402
import ledger_verifier  # noqa: E402


STATE_NAME = "PROJECT_STATE.json"
BOARD_NAME = "PROJECT_BOARD.html"
RECEIPT_NAME = "RUN_RECEIPT.json"
GATE_NAME = "project-organizer-release"
EVIDENCE_DIRECTORY = Path(".project-organizer") / "evidence"
WORKER_REPORT_FILES = {
    "scope_mapper": "scope_mapper.json",
    "dependency_planner": "dependency_planner.json",
}


class RenderError(RuntimeError):
    """Raised when a truthful, complete board cannot be rendered."""


def load_verifier(project_root: Path):
    del project_root
    return ledger_verifier


def json_bytes(value: Mapping[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def atomic_write(path: Path, content: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(str(temporary), str(path))
    except Exception:
        if temporary.exists():
            temporary.unlink()
        raise


def load_previous_repairs(project_root: Path) -> int:
    receipt_path = project_root / RECEIPT_NAME
    if receipt_path.is_symlink() or not receipt_path.is_file():
        return 0
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        repairs = receipt.get("measured_observations", {}).get("repairs", 0)
        return repairs if isinstance(repairs, int) and not isinstance(repairs, bool) and repairs >= 0 else 0
    except (OSError, json.JSONDecodeError, AttributeError):
        return 0


def load_json_report(path: Path) -> Tuple[Dict[str, Any], bytes]:
    if path.is_symlink() or not path.is_file():
        raise RenderError(f"Missing regular agent report: {path}")
    content = path.read_bytes()
    try:
        report = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RenderError(f"Agent report must be one UTF-8 JSON object: {path.name}") from error
    if not isinstance(report, dict):
        raise RenderError(f"Agent report must be one JSON object: {path.name}")
    return report, content


def validate_findings(findings: Any, source_ids: Sequence[str], role: str) -> None:
    if not isinstance(findings, list) or not 1 <= len(findings) <= 4:
        raise RenderError(f"{role} must return one to four material findings")
    allowed = set(source_ids)
    for finding in findings:
        if not isinstance(finding, dict) or set(finding) != {"summary", "source_ids"}:
            raise RenderError(f"{role} findings require only summary and source_ids")
        summary = finding["summary"]
        cited = finding["source_ids"]
        if not isinstance(summary, str) or len(summary.strip()) < 20:
            raise RenderError(f"{role} finding summary is too short to guide work")
        if not isinstance(cited, list) or not cited or len(cited) != len(set(cited)):
            raise RenderError(f"{role} finding needs distinct source IDs")
        if not set(cited).issubset(allowed):
            raise RenderError(f"{role} finding cites an unknown source ID")


def load_worker_reports(
    root: Path,
    snapshot: Mapping[str, Any],
    ready: Mapping[str, Any],
    dependency: Mapping[str, Any],
    decisions: Mapping[str, Any],
) -> Dict[str, Dict[str, Any]]:
    control_root = root / EVIDENCE_DIRECTORY.parent
    evidence_root = root / EVIDENCE_DIRECTORY
    for directory in (control_root, evidence_root):
        if directory.is_symlink() or not directory.is_dir():
            raise RenderError(f"Evidence folder must be a regular directory, not a link: {directory}")
    source_ids = [item["source_id"] for item in snapshot["sources"]]
    reports: Dict[str, Dict[str, Any]] = {}
    for role, filename in WORKER_REPORT_FILES.items():
        report, content = load_json_report(evidence_root / filename)
        if report.get("role") != role or report.get("verdict") != "PASS":
            raise RenderError(f"{role} report must identify its role and return verdict PASS")
        if report.get("source_fingerprint") != snapshot["source_fingerprint"]:
            raise RenderError(f"{role} report is stale for the current source fingerprint")
        validate_findings(report.get("findings"), source_ids, role)
        reports[role] = {"sha256": sha256_bytes(content), "report": report}

    scope = reports["scope_mapper"]["report"]
    expected_scope_keys = {
        "role", "verdict", "source_fingerprint", "tools_used", "project_id",
        "deliverable_ids", "decision_ids", "unknown_ids", "findings",
    }
    if set(scope) != expected_scope_keys:
        raise RenderError("scope_mapper report fields differ from the course contract")
    if scope["tools_used"] != ["get_project_snapshot", "get_decision_queue"]:
        raise RenderError("scope_mapper must own only snapshot and decision-queue tools")
    if scope["project_id"] != snapshot["project"]["project_id"]:
        raise RenderError("scope_mapper project_id disagrees with the ledger")
    if scope["deliverable_ids"] != [item["deliverable_id"] for item in snapshot["deliverables"]]:
        raise RenderError("scope_mapper deliverable IDs disagree with the ledger")
    if scope["decision_ids"] != [item["decision_id"] for item in decisions["decisions"]]:
        raise RenderError("scope_mapper decision IDs disagree with the current queue")
    if scope["unknown_ids"] != [item["field"] for item in snapshot["unknowns"]]:
        raise RenderError("scope_mapper unknown IDs disagree with the source record")

    planner = reports["dependency_planner"]["report"]
    expected_planner_keys = {
        "role", "verdict", "source_fingerprint", "tools_used", "ready_ids",
        "launch_path_ids", "blocked_ids", "findings",
    }
    if set(planner) != expected_planner_keys:
        raise RenderError("dependency_planner report fields differ from the course contract")
    if planner["tools_used"] != ["get_ready_work", "get_dependency_path"]:
        raise RenderError("dependency_planner must own only ready-work and dependency-path tools")
    if planner["ready_ids"] != [item["deliverable_id"] for item in ready["ready_work"]]:
        raise RenderError("dependency_planner ready IDs disagree with the ledger")
    if planner["launch_path_ids"] != [item["deliverable_id"] for item in dependency["launch_path"]]:
        raise RenderError("dependency_planner launch path disagrees with the ledger")
    if planner["blocked_ids"] != [
        item["deliverable_id"] for item in dependency["launch_path"] if item["status"] == "blocked"
    ]:
        raise RenderError("dependency_planner blocked IDs disagree with the launch path")
    reported_tools = scope["tools_used"] + planner["tools_used"]
    if len(reported_tools) != len(TOOL_NAMES) or set(reported_tools) != set(TOOL_NAMES):
        raise RenderError("worker reports must partition the exact four-tool MCP contract")
    return reports


def build_state(
    project_root: Path,
    *,
    elapsed_seconds: int,
    repairs: int,
    generated_at: str,
) -> Dict[str, Any]:
    requested_root = project_root.expanduser().absolute()
    if requested_root.is_symlink() or not requested_root.is_dir():
        raise RenderError(f"Project root must be a regular directory, not a link: {requested_root}")
    root = requested_root.resolve()
    verifier = load_verifier(root)
    verification = verifier.verify_ledger(root)
    snapshot = dispatch(root, "get_project_snapshot", {})
    ready = dispatch(root, "get_ready_work", {})
    dependency = dispatch(root, "get_dependency_path", {"deliverable_id": "DLV-004"})
    decisions = dispatch(root, "get_decision_queue", {"limit": 10})
    if snapshot["source_fingerprint"] != verification["source_fingerprint"]:
        raise RenderError("MCP snapshot and ledger verifier disagree on source fingerprint")
    fingerprints = {
        snapshot["source_fingerprint"],
        ready["source_fingerprint"],
        dependency["source_fingerprint"],
        decisions["source_fingerprint"],
    }
    if fingerprints != {verification["source_fingerprint"]}:
        raise RenderError("The four MCP tool results do not share the current source fingerprint")
    if not snapshot["unknowns"]:
        raise RenderError("The consequential source gap is missing from the project snapshot")
    worker_reports = load_worker_reports(root, snapshot, ready, dependency, decisions)
    return {
        "schema_version": "1.0",
        "board_status": "CANDIDATE",
        "ledger_status": "PASS",
        "schema_status": "PASS",
        "generated_at": generated_at,
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
        "evidence_observations": {
            "worker_reports_bound": 2,
            "mcp_tools_reported": list(TOOL_NAMES),
            "mcp_tools_basis": "two validated worker reports",
            "usage_visibility": "not exposed",
        },
        "measured_observations": {
            "elapsed_seconds": max(0, int(elapsed_seconds)),
            "elapsed_basis": "project_ledger.sqlite3 mtime to board render",
            "repairs": max(0, int(repairs)),
            "repairs_basis": "release-gate HOLD requests carried by RUN_RECEIPT.json",
        },
    }


def e(value: Any) -> str:
    return html.escape(str(value), quote=True)


def status_class(status: str) -> str:
    return {
        "complete": "good",
        "in_progress": "active",
        "ready": "ready",
        "blocked": "bad",
        "planned": "muted",
    }.get(status, "muted")


def render_path(
    items: Sequence[Mapping[str, Any]],
    dependencies: Sequence[Mapping[str, Any]],
) -> str:
    by_pair = {
        (item["predecessor_deliverable_id"], item["successor_deliverable_id"]): item
        for item in dependencies
    }
    cards = []
    for index, item in enumerate(items):
        connector = ""
        if index:
            predecessor = items[index - 1]["deliverable_id"]
            edge = by_pair[(predecessor, item["deliverable_id"])]
            connector = f'''<article class="path-edge">
                <span aria-hidden="true">→</span>
                <b>{e(edge['dependency_id'])} · {e(edge['source_id'])}</b>
                <small>{e(edge['condition'])}</small>
                <em>{e(edge['status'])}</em>
              </article>'''
        cards.append(
            connector
            + f'''<article class="path-card {status_class(item['status'])}">
                <span class="eyebrow">{e(item['deliverable_id'])} · {e(item['source_id'])}</span>
                <strong>{e(item['title'])}</strong>
                <span>{e(item['owner'])}</span>
                <b>{e(item['status'].replace('_', ' '))}</b>
              </article>'''
        )
    return "".join(cards)


def render_html(state: Mapping[str, Any]) -> str:
    project = state["project"]
    now = state["now"] or {}
    next_item = state["next"] or {}
    now_update_source = (now.get("latest_update") or {}).get("source_id")
    now_sources = " · ".join(
        source for source in (now.get("source_id"), now_update_source) if source
    ) or "No source"
    blocked_cards = "".join(
        f'''<article class="alert-card">
          <span class="eyebrow">{e(item['deliverable_id'])} · {e(item['source_id'])} · {e(item['owner'])}</span>
          <h3>{e(item['title'])}</h3>
          <p>{e(item['blocked_reason'])}</p>
          <p class="commitment"><b>Next commitment</b> {e(item['next_commitment'])}</p>
        </article>'''
        for item in state["blocked_work"]
    ) or '<p class="empty">No blocked deliverables.</p>'
    decision_cards = "".join(
        f'''<article class="decision-card">
          <div><span class="eyebrow">{e(item['decision_id'])} · {e(item['source_id'])} · needed {e(item['needed_by'])}</span>
          <h3>{e(item['title'])}</h3></div>
          <p>{e(item['question'])}</p>
          <dl><div><dt>Owner</dt><dd class="{'unknown-text' if item['decision_owner'] == 'Not assigned in source' else ''}">{e(item['decision_owner'])}</dd></div>
          <div><dt>Recommendation</dt><dd>{e(item['recommendation'])}</dd></div></dl>
          <p class="impact"><b>If delayed:</b> {e(item['consequence_of_delay'])}</p>
        </article>'''
        for item in state["decision_queue"]
    )
    unknown_cards = "".join(
        f'''<article class="unknown-card">
          <span class="eyebrow">UNKNOWN · {e(item['source_id'])}</span>
          <h3>{e(item['field'])}</h3>
          <p class="unknown-text">{e(item['value'])}</p>
          <p>{e(item['impact'])}</p>
          <b>Needed by {e(item['needed_by'])}</b>
        </article>'''
        for item in state["unknowns"]
    )
    deliverable_cards = "".join(
        f'''<article class="deliverable-card {status_class(item['status'])}">
          <div class="card-top"><span class="eyebrow">{e(item['deliverable_id'])}</span><span class="pill">{e(item['status'].replace('_', ' '))}</span></div>
          <h3>{e(item['title'])}</h3>
          <p><b>{e(item['owner'])}</b> · review by {e(item['reviewer'])}</p>
          <p>{e(item['acceptance_condition'])}</p>
          <p class="commitment"><b>Next</b> {e(item['next_commitment'])}</p>
          <span class="source-line">{e(item['source_id'])} · {e(' · '.join(item['source_inputs']))}</span>
        </article>'''
        for item in state["deliverables"]
    )
    ready_cards = "".join(
        f'''<article class="ready-card">
          <span class="eyebrow">{e(item['deliverable_id'])} · {e(item['source_id'])}</span>
          <h3>{e(item['title'])}</h3>
          <p><b>{e(item['owner'])}</b> can move now because every declared predecessor is complete.</p>
          <p class="commitment"><b>Next commitment</b> {e(item['next_commitment'])}</p>
          <span class="source-line"><b>Readiness evidence</b> {e(' · '.join(
              f"{fact['dependency_id']} {fact['dependency_source_id']} · {fact['predecessor_deliverable_id']} {fact['predecessor_status']} {fact['predecessor_source_id']}"
              for fact in item['readiness_evidence']
          ) or f"No declared predecessors · {item['source_id']}")}</span>
        </article>'''
        for item in state["ready_work"]
    ) or '<p class="empty">No deliverable is ready now.</p>'
    source_cards = "".join(
        f'''<li><b>{e(item['source_id'])}</b><span>{e(item['title'])}</span><code>{e(item['path'])}</code></li>'''
        for item in state["sources"]
    )
    worker_cards = "".join(
        f'''<article class="worker-card">
          <span class="eyebrow">{e(role.replace('_', ' '))}</span>
          <h3>{len(bundle['report']['findings'])} material findings</h3>
          {''.join(f'<p><b>{e(" · ".join(finding["source_ids"]))}</b><br>{e(finding["summary"])}</p>' for finding in bundle['report']['findings'])}
          <span class="source-line">Evidence report {e(bundle['sha256'][:12])} · {e(bundle['report']['verdict'])}</span>
        </article>'''
        for role in WORKER_REPORT_FILES
        for bundle in (state["worker_reports"][role],)
    )
    evidence = state["evidence_observations"]
    measured = state["measured_observations"]
    fingerprint = state["source_fingerprint"]
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="generator" content="AI Harness Bootcamp Project Organizer 1.0">
  <meta name="project-state-sha256" content="{sha256_bytes(json_bytes(state))}">
  <title>{e(project['name'])} · Project Board</title>
  <style>
    :root {{ --ink:#132629; --paper:#f3f0e8; --white:#fffdf8; --teal:#215c66; --aqua:#9bd1ce; --blue:#37718e; --orange:#d9763d; --red:#a84235; --green:#34745b; --line:#c9c3b8; --muted:#687579; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; color:var(--ink); background:linear-gradient(135deg,#e5ece8 0%,var(--paper) 38%,#efe1d3 100%); font:16px/1.45 Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif; }}
    main {{ width:min(1440px,calc(100% - 32px)); margin:16px auto 56px; }}
    .hero {{ padding:clamp(28px,5vw,68px); border-radius:30px; color:white; background:radial-gradient(circle at 90% 10%,#377d86 0,transparent 34%),linear-gradient(120deg,#102f35,#215c66 62%,#173f48); box-shadow:0 24px 60px #173c4430; }}
    .eyebrow {{ display:block; font-size:.72rem; font-weight:850; letter-spacing:.12em; text-transform:uppercase; color:inherit; opacity:.78; }}
    h1 {{ max-width:980px; margin:.28em 0 .22em; font-size:clamp(2.2rem,5vw,5.2rem); line-height:.94; letter-spacing:-.055em; }}
    .outcome {{ max-width:1020px; margin:18px 0 28px; font-size:clamp(1.08rem,2vw,1.55rem); }}
    .success {{ max-width:940px; padding:16px 18px; border-left:4px solid var(--aqua); background:#ffffff12; border-radius:0 12px 12px 0; }}
    .status-row,.measure-row {{ display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin-top:28px; }}
    .status-chip,.measure {{ padding:16px; border:1px solid #ffffff30; border-radius:15px; background:#ffffff10; }}
    .status-chip b,.measure b {{ display:block; font-size:1.2rem; }}
    .section {{ margin-top:18px; padding:clamp(20px,3vw,38px); border:1px solid #ffffff; border-radius:24px; background:#fffdf8df; box-shadow:0 15px 45px #293c3d10; }}
    .section-head {{ display:flex; justify-content:space-between; gap:20px; align-items:end; margin-bottom:18px; }}
    h2 {{ margin:0; font-size:clamp(1.55rem,3vw,2.7rem); letter-spacing:-.04em; }} h3 {{ margin:.32em 0; font-size:1.18rem; }} p {{ margin:.48em 0; }}
    .focus-grid {{ display:grid; grid-template-columns:1.35fr 1fr; gap:14px; }}
    .focus-card {{ padding:clamp(22px,4vw,42px); border-radius:20px; background:#dcebea; }}
    .focus-card.next {{ background:#f4dcc9; }} .focus-card h3 {{ font-size:clamp(1.4rem,3vw,2.35rem); }}
    .path {{ display:flex; align-items:stretch; gap:8px; overflow-x:auto; padding:5px 2px 12px; }}
    .path-card {{ min-width:210px; flex:1; padding:18px; border-top:7px solid var(--muted); border-radius:14px; background:white; box-shadow:0 8px 24px #20373914; }}
    .path-card.good {{ border-color:var(--green); }} .path-card.active {{ border-color:var(--blue); }} .path-card.bad {{ border-color:var(--red); }}
    .path-card strong,.path-card span,.path-card b {{ display:block; margin-bottom:7px; }} .path-edge {{ align-self:center; min-width:180px; padding:12px; border-radius:12px; color:#6d3b20; background:#f4dcc9; }} .path-edge span,.path-edge b,.path-edge small,.path-edge em {{ display:block; margin-bottom:5px; }} .path-edge span {{ font-size:1.4rem; }}
    .split {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; }}
    .alert-card,.unknown-card {{ padding:22px; border-radius:18px; background:#f6ded6; border-left:7px solid var(--red); }}
    .unknown-card {{ background:#fff0c9; border-color:#b37a16; }} .unknown-text {{ color:#8e4d0f; font-weight:850; }}
    .decision-grid,.deliverable-grid,.ready-grid,.worker-grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:14px; }}
    .decision-card,.deliverable-card,.ready-card,.worker-card {{ padding:22px; border:1px solid var(--line); border-radius:18px; background:white; }}
    .ready-card {{ border-left:7px solid var(--green); background:#e8f2eb; }}
    .worker-card {{ border-top:7px solid var(--blue); }} .worker-card p {{ padding:10px; border-radius:10px; background:#edf3f5; }}
    dl {{ margin:14px 0; }} dl div {{ display:grid; grid-template-columns:125px 1fr; gap:10px; padding:7px 0; border-top:1px solid #e3ded4; }} dt {{ color:var(--muted); }} dd {{ margin:0; font-weight:650; }}
    .impact,.commitment {{ padding:10px 12px; border-radius:10px; background:#f1eee7; }}
    .deliverable-card {{ border-top:7px solid var(--muted); }} .deliverable-card.good {{ border-top-color:var(--green); }} .deliverable-card.active {{ border-top-color:var(--blue); }} .deliverable-card.bad {{ border-top-color:var(--red); }}
    .card-top {{ display:flex; justify-content:space-between; gap:10px; }} .pill {{ padding:5px 9px; border-radius:99px; background:#edf1ef; font-size:.78rem; font-weight:800; text-transform:uppercase; }}
    .source-line {{ display:block; margin-top:12px; color:var(--muted); font-size:.78rem; }}
    .source-grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; padding:0; list-style:none; }} .source-grid li {{ display:grid; grid-template-columns:80px 1fr; gap:4px 12px; padding:13px; border:1px solid var(--line); border-radius:12px; background:white; }} .source-grid code {{ grid-column:2; color:var(--muted); overflow-wrap:anywhere; }}
    .measure-row {{ margin:0; }} .measure {{ color:var(--ink); border-color:var(--line); background:white; }} .measure b {{ font-size:1.55rem; color:var(--teal); }}
    footer {{ margin-top:18px; padding:18px 4px; color:#43575b; font-size:.82rem; overflow-wrap:anywhere; }}
    @media (max-width:850px) {{ .status-row,.measure-row,.focus-grid,.split,.decision-grid,.deliverable-grid,.ready-grid,.source-grid,.worker-grid {{ grid-template-columns:1fr; }} .path {{ flex-direction:column; }} }}
    @media print {{ body {{ background:white; }} main {{ width:100%; margin:0; }} .hero,.section {{ break-inside:avoid; box-shadow:none; }} }}
  </style>
</head>
<body>
<main>
  <header class="hero">
    <span class="eyebrow">Project Organizer · {e(project['source_id'])} · as of {e(state['as_of'])} · generated {e(state['generated_at'])}</span>
    <h1>{e(project['name'])}</h1>
    <p class="outcome">{e(project['outcome'])}</p>
    <p class="success"><b>Success looks like</b><br>{e(project['success_measure'])}</p>
    <div class="status-row" aria-label="Release status">
      <div class="status-chip"><span class="eyebrow">Board</span><b>{e(state['board_status'])}</b><span>check RUN_RECEIPT.json</span></div>
      <div class="status-chip"><span class="eyebrow">Ledger</span><b>{e(state['ledger_status'])}</b></div>
      <div class="status-chip"><span class="eyebrow">Schema</span><b>{e(state['schema_status'])}</b></div>
      <div class="status-chip"><span class="eyebrow">Target</span><b>{e(project['target_date'])}</b></div>
    </div>
  </header>

  <section class="section">
    <div class="section-head"><div><span class="eyebrow">Orientation</span><h2>Now and next</h2></div><b>{e(project['current_phase'])}</b></div>
    <div class="focus-grid">
      <article class="focus-card"><span class="eyebrow">Now · {e(now.get('deliverable_id','No active item'))} · {e(now_sources)}</span><h3>{e(now.get('title','No active work'))}</h3><p>{e((now.get('latest_update') or {}).get('summary','No current update supplied.'))}</p><p><b>Owner</b> {e(now.get('owner','Not assigned in source'))}</p></article>
      <article class="focus-card next"><span class="eyebrow">Next commitment · {e(next_item.get('source_id','No source'))}</span><h3>{e(next_item.get('commitment','No next commitment supplied.'))}</h3><p><b>{e(next_item.get('owner','Not assigned in source'))}</b> · due {e(next_item.get('due_date','Not assigned in source'))}</p></article>
    </div>
  </section>

  <section class="section"><div class="section-head"><div><span class="eyebrow">Ready now</span><h2>Work that can move without waiting</h2></div><b>{len(state['ready_work'])} ready</b></div><div class="ready-grid">{ready_cards}</div></section>

  <section class="section"><div class="section-head"><div><span class="eyebrow">Sequence</span><h2>Longest declared launch path</h2><p>Longest predecessor chain in the supplied relationships—not a duration-based critical-path calculation.</p></div><b>{len(state['launch_path'])} deliverables</b></div><div class="path">{render_path(state['launch_path'], state['launch_dependencies'])}</div></section>

  <div class="split">
    <section class="section"><div class="section-head"><div><span class="eyebrow">Blocked work</span><h2>What cannot move</h2></div><b>{len(state['blocked_work'])}</b></div>{blocked_cards}</section>
    <section class="section"><div class="section-head"><div><span class="eyebrow">Unknowns</span><h2>What the record does not say</h2></div><b>{len(state['unknowns'])}</b></div>{unknown_cards}</section>
  </div>

  <section class="section"><div class="section-head"><div><span class="eyebrow">Decision queue</span><h2>Choices that control the work</h2></div><b>{len(state['decision_queue'])} open</b></div><div class="decision-grid">{decision_cards}</div></section>
  <section class="section"><div class="section-head"><div><span class="eyebrow">Work system</span><h2>Four accountable deliverables</h2></div><b>{state['counts']['complete']} complete · {state['counts']['blocked']} blocked</b></div><div class="deliverable-grid">{deliverable_cards}</div></section>

  <section class="section"><div class="section-head"><div><span class="eyebrow">Analysis</span><h2>Scope and sequence findings</h2><p>What the two read-only analysis passes found before the board was built.</p></div><b>2/2 PASS</b></div><div class="worker-grid">{worker_cards}</div></section>

  <section class="section"><div class="section-head"><div><span class="eyebrow">Source coverage</span><h2>{state['source_coverage']['represented']}/{state['source_coverage']['declared']} declared sources represented</h2></div><b>{e(state['source_coverage']['status'])}</b></div><ul class="source-grid">{source_cards}</ul></section>

  <section class="section"><div class="section-head"><div><span class="eyebrow">Run receipt inputs</span><h2>What this run exposed</h2></div><b>reported ≠ independently proved</b></div>
    <div class="measure-row">
      <div class="measure"><span class="eyebrow">Elapsed</span><b>{e(measured['elapsed_seconds'])} sec</b><span>measured</span></div>
      <div class="measure"><span class="eyebrow">Worker reports</span><b>{e(evidence['worker_reports_bound'])}/2</b><span>hash bound</span></div>
      <div class="measure"><span class="eyebrow">Repairs</span><b>{e(measured['repairs'])}</b><span>gate HOLD requests</span></div>
      <div class="measure"><span class="eyebrow">Usage</span><b>not exposed</b><span>local harness</span></div>
      <div class="measure"><span class="eyebrow">MCP tools reported</span><b>{len(evidence['mcp_tools_reported'])}/4</b><span>worker reports</span></div>
    </div>
  </section>
  <footer>Generated at <b>{e(state['generated_at'])}</b> · source fingerprint <b>{e(fingerprint)}</b> · {len(state['sources'])} declared sources · no external data · generated locally</footer>
</main>
</body>
</html>
'''


def build_receipt(
    state: Mapping[str, Any],
    state_content: bytes,
    board_content: bytes,
    *,
    status: str,
    gate_status: str,
    checks: Sequence[Mapping[str, str]],
    reviewer_report_sha256: Optional[str] = None,
) -> Dict[str, Any]:
    worker_hashes = {
        role: bundle["sha256"] for role, bundle in state["worker_reports"].items()
    }
    return {
        "gate": GATE_NAME,
        "status": status,
        "gate_status": gate_status,
        "board_status": "RELEASE" if status == "PASS" else state["board_status"],
        "ledger_status": state["ledger_status"],
        "schema_status": state["schema_status"],
        "source_fingerprint": state["source_fingerprint"],
        "state_sha256": sha256_bytes(state_content),
        "board_sha256": sha256_bytes(board_content),
        "measured_observations": state["measured_observations"],
        "evidence": {
            "worker_report_sha256": worker_hashes,
            "reviewer_report_sha256": reviewer_report_sha256 or "not available",
            "agent_reports_bound": 3 if reviewer_report_sha256 else 2,
            "mcp_tools_reported": state["evidence_observations"]["mcp_tools_reported"],
            "mcp_tools_basis": "validated worker reports",
            "usage_visibility": "not exposed",
        },
        "checks": list(checks),
    }


def render_project(
    project_root: Path,
    *,
    elapsed_seconds: Optional[int] = None,
) -> Dict[str, Any]:
    requested_root = project_root.expanduser().absolute()
    if requested_root.is_symlink() or not requested_root.is_dir():
        raise RenderError(f"Project root must be a regular directory, not a link: {requested_root}")
    root = requested_root.resolve()
    ledger = root / "project_ledger.sqlite3"
    if ledger.is_symlink() or not ledger.is_file():
        raise RenderError(f"Missing regular ledger: {ledger}")
    measured_elapsed = max(0, int(time.time() - ledger.stat().st_mtime)) if elapsed_seconds is None else elapsed_seconds
    repairs = load_previous_repairs(root)
    state = build_state(
        root,
        elapsed_seconds=measured_elapsed,
        repairs=repairs,
        generated_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    )
    state_content = json_bytes(state)
    board_content = render_html(state).encode("utf-8")
    receipt = build_receipt(
        state,
        state_content,
        board_content,
        status="PENDING",
        gate_status="PENDING",
        checks=[{"check": "renderer", "status": "PASS", "detail": "state and board written from verified read-only queries"}],
    )
    atomic_write(root / STATE_NAME, state_content)
    atomic_write(root / BOARD_NAME, board_content)
    atomic_write(root / RECEIPT_NAME, json_bytes(receipt))
    return receipt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        render_project(Path(args.project_root))
    except Exception as error:
        print(f"HOLD Project Organizer render: {error}")
        return 1
    print(f"Wrote candidate {STATE_NAME}, {BOARD_NAME}, and pending {RECEIPT_NAME} (receipt last)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
