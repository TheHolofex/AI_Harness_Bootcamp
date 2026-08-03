#!/usr/bin/env python3
"""Verify a completed P4 Director Loop vault and freeze or check its baseline."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import Counter, defaultdict, deque
from pathlib import Path, PurePosixPath
from typing import Any, Counter as CounterType, Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple


ANSWER_PATHS = ("Answers/Q1 Risks.md", "Answers/Q2 Blocked Decision.md")
HUB_PATHS = ("People.md", "Systems.md", "Events.md", "Decisions.md")
EVIDENCE_ROOTS = ("00_Inbox", "00_Inbox/processed", "Source_Packet")
EVALUATOR_CRITERIA = (
    "Required artifacts exist",
    "Personal rules visibly affect the output",
    "Answer claims cite direct manifested evidence",
    "Audit excerpts and dispositions are grounded",
    "Retrieval is earned and inside its budget",
    "Normalized notes retain lineage and graph reachability",
    "Morning Brief uses audited support only",
    "Resume, state, and trace agree",
)
CONTROL_ONLY_EVALUATOR_CRITERIA = {
    "Retrieval is earned and inside its budget",
    "Resume, state, and trace agree",
}
REQUIRED_QUESTIONS = (
    "What are the top operational risks this week and which notes support each?",
    "What decision is blocked and what evidence is missing?",
)
REQUIRED_CANDIDATE_ARTIFACTS = (
    "AGENTS.md",
    ".agents/skills/director-loop/SKILL.md",
    ".codex/agents/director_evaluator.toml",
    "Harness/HARNESS_CARD.md",
    "Harness/RUN_STATE.md",
    "Harness/RUN_TRACE.md",
    "Harness/RESUME_RECEIPT.md",
    "Harness/SOURCE_MANIFEST.json",
    "Answers/Q1 Risks.md",
    "Answers/Q2 Blocked Decision.md",
    "Audit.md",
    "Morning_Brief.md",
    "MOC.md",
) + HUB_PATHS + ("tools/verify_vault.py",)
REQUIRED_FINAL_ARTIFACTS = REQUIRED_CANDIDATE_ARTIFACTS + (
    "Harness/EVAL.md",
    "Harness/HANDOFF_RECEIPT.md",
)
OUTPUT_PATHS = ANSWER_PATHS + (
    "Audit.md",
    "Morning_Brief.md",
    "Harness/EVAL.md",
    "Harness/RESUME_RECEIPT.md",
    "Harness/HANDOFF_RECEIPT.md",
    "Harness/CANDIDATE_CHECK_FIRST.txt",
    "Harness/DIRECTOR_EVALUATOR_FIRST.json",
)
ALLOWED_DISPOSITIONS = {"support", "partial", "not supported"}
ALLOWED_TERMINAL_REASONS = {
    "SUCCESS",
    "NEEDS_EVIDENCE",
    "BUDGET_STOP",
    "ERROR_CEILING",
    "NO_PROGRESS",
    "HUMAN_HAND_BACK",
}
PLACEHOLDER_RE = re.compile(r"\[REPLACE:\s*[^\]\n]+\]", re.IGNORECASE)
WIKILINK_RE = re.compile(r"(?<!!)\[\[([^\]\n]+)\]\]")
CLAIM_BULLET_RE = re.compile(r"^\s*[-*]\s+\[([A-Z][A-Z0-9]*-\d{2})\]\s+(.+?)\s*$")
SHA256_RE = re.compile(r"[0-9a-f]{64}")
PROVENANCE_RE = re.compile(
    r"^\s*Provenance:\s*vault only;\s*audited sources only\s*$",
    re.IGNORECASE | re.MULTILINE,
)
MANIFEST_PATH = PurePosixPath("Harness/BASELINE_MANIFEST.json")
TRUSTED_SEED_ROOT = Path(__file__).resolve().parents[1]
SKIPPED_MANIFEST_DIRS = {".obsidian", "__pycache__"}
RESERVED_TOP_LEVEL = {".agents", ".codex", "00_Inbox", "Answers", "Harness", "Source_Packet", "tools"}
RESERVED_ROOT_NOTES = {
    "AGENTS.md",
    "Audit.md",
    "Morning_Brief.md",
    "MOC.md",
    *HUB_PATHS,
}
TRUSTED_CONTRACT_PATHS = (
    ".agents/skills/director-loop/SKILL.md",
    ".codex/agents/director_evaluator.toml",
    "tools/verify_vault.py",
)
TRACE_CLOSEOUT = (
    "\n\n## Closeout after evaluation\n\n"
    "- Final trusted candidate check: PASS.\n"
    "- Final fresh read-only evaluator: PASS.\n"
    "- Scoped handoff completed with accepted artifacts and residual risk.\n\n"
    "Terminal reason: SUCCESS\n"
)


class VerificationError(RuntimeError):
    """Raised when the vault does not meet the P4 completion contract."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(64 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def requested_root(path: Path) -> Path:
    candidate = path.expanduser().absolute()
    if candidate.is_symlink() or not candidate.is_dir():
        raise VerificationError(f"Vault root must be a regular directory, not a link: {candidate}")
    return candidate.resolve()


def require_external_course_verifier(root: Path) -> None:
    if root == TRUSTED_SEED_ROOT:
        raise VerificationError(
            "Refusing self-verification: run the untouched course-repository verifier against the copied vault"
        )


def verify_trusted_contract_copies(root: Path) -> None:
    for relative in TRUSTED_CONTRACT_PATHS:
        trusted = regular_path(TRUSTED_SEED_ROOT, relative)
        candidate = regular_path(root, relative)
        if sha256_file(candidate) != sha256_file(trusted):
            raise VerificationError(
                f"Copied contract differs from untouched course version: {relative}"
            )


def regular_path(root: Path, relative: str) -> Path:
    path = root / PurePosixPath(relative)
    if path.is_symlink() or not path.is_file():
        raise VerificationError(f"Missing required artifact or not a regular file: {relative}")
    return path


def read_regular_text(root: Path, relative: str) -> str:
    path = regular_path(root, relative)
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise VerificationError(f"Required artifact is not UTF-8 text: {relative}") from error
    if not text.strip():
        raise VerificationError(f"Required artifact is empty: {relative}")
    return text


def read_regular_json(root: Path, relative: str) -> Any:
    text = read_regular_text(root, relative)
    try:
        return json.loads(text)
    except json.JSONDecodeError as error:
        raise VerificationError(f"Invalid JSON in {relative}: {error.msg}") from error


def clean_token(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("`", "").replace("*", "").strip()).casefold()


def clean_path_cell(value: str) -> str:
    return value.strip().strip("`").replace("\\", "/")


def candidate_finding_is_control_only(finding: str) -> bool:
    normalized = clean_token(finding)
    markers = (
        "harness/run_state.md",
        "harness/run_trace.md",
        "fixed inbox inventory",
        "retrieval ledger",
        "retrieval row",
        "unearned retrieval",
        "adaptive retrieval",
        "terminal reason mismatch",
    )
    return any(marker in normalized for marker in markers)


def list_field(text: str, label: str, artifact: str) -> str:
    match = re.search(
        r"^\s*[-*]\s+" + re.escape(label) + r":\s*(.+?)\s*$",
        text,
        re.IGNORECASE | re.MULTILINE,
    )
    if match is None or not match.group(1).strip():
        raise VerificationError(f"{artifact} is missing a populated '{label}' field")
    return match.group(1).strip()


def colon_field(text: str, label: str, artifact: str) -> str:
    match = re.search(
        r"^\s*(?:[-*]\s+)?" + re.escape(label) + r":\s*(.+?)\s*$",
        text,
        re.IGNORECASE | re.MULTILINE,
    )
    if match is None or not match.group(1).strip():
        raise VerificationError(f"{artifact} is missing a populated '{label}' field")
    return match.group(1).strip()


def last_colon_field(text: str, label: str, artifact: str) -> str:
    matches = re.findall(
        r"^\s*(?:[-*]\s+)?" + re.escape(label) + r":\s*(.+?)\s*$",
        text,
        re.IGNORECASE | re.MULTILINE,
    )
    if not matches or not matches[-1].strip():
        raise VerificationError(f"{artifact} is missing a populated final '{label}' field")
    return matches[-1].strip()


def integer_field(text: str, label: str, artifact: str) -> int:
    raw = list_field(text, label, artifact)
    if not re.fullmatch(r"\d+", raw.strip()):
        raise VerificationError(f"{artifact} field '{label}' must be a non-negative integer")
    return int(raw)


def split_table_row(line: str) -> List[str]:
    stripped = line.strip()
    if not stripped.startswith("|"):
        return []
    stripped = stripped[1:-1] if stripped.endswith("|") else stripped[1:]
    sentinel = "\u0000P4PIPE\u0000"
    stripped = stripped.replace(r"\|", sentinel)
    return [cell.replace(sentinel, "|").strip() for cell in stripped.split("|")]


def is_separator_row(cells: Sequence[str]) -> bool:
    return bool(cells) and all(bool(re.fullmatch(r":?-{3,}:?", cell.strip())) for cell in cells)


def table_rows(text: str, headers: Sequence[str], artifact: str) -> List[Dict[str, str]]:
    lines = text.splitlines()
    wanted = [header.casefold() for header in headers]
    for index in range(len(lines) - 1):
        found = [clean_token(cell) for cell in split_table_row(lines[index])]
        separator = split_table_row(lines[index + 1])
        if found != wanted or not is_separator_row(separator):
            continue
        rows: List[Dict[str, str]] = []
        for line in lines[index + 2 :]:
            cells = split_table_row(line)
            if not cells:
                break
            if len(cells) != len(headers):
                raise VerificationError(f"{artifact} has a malformed row in the {headers[0]} table")
            if all(not cell for cell in cells):
                continue
            rows.append(dict(zip(headers, cells)))
        return rows
    raise VerificationError(f"{artifact} is missing the required table: {' | '.join(headers)}")


def require_fragments(text: str, artifact: str, fragments: Iterable[str]) -> None:
    folded = text.casefold()
    missing = [fragment for fragment in fragments if fragment.casefold() not in folded]
    if missing:
        raise VerificationError(f"{artifact} is missing required content: {', '.join(missing)}")


def verify_skill(text: str) -> None:
    require_fragments(
        text,
        ".agents/skills/director-loop/SKILL.md",
        REQUIRED_QUESTIONS
        + (
            ".codex/agents/director_evaluator.toml",
            "Harness/DIRECTOR_EVALUATOR_FIRST.json",
            "Harness/DIRECTOR_EVALUATOR_FINAL.json",
            "Harness/RESUME_RECEIPT.md",
            "Harness/HANDOFF_RECEIPT.md",
            "Harness/CANDIDATE_CHECK_FIRST.txt",
            "Harness/CANDIDATE_CHECK_FINAL.txt",
            "--candidate",
            "--write-manifest",
            "--check-manifest",
            "Raw sources:",
        ),
    )


def verify_evaluator_config(text: str) -> None:
    artifact = ".codex/agents/director_evaluator.toml"
    for key, value in (
        ("name", "director_evaluator"),
        ("model", "gpt-5.6-terra"),
        ("model_reasoning_effort", "high"),
        ("sandbox_mode", "read-only"),
    ):
        pattern = r'^\s*' + re.escape(key) + r'\s*=\s*"' + re.escape(value) + r'"\s*$'
        if re.search(pattern, text, re.MULTILINE) is None:
            raise VerificationError(f"{artifact} must set {key} = {value!r}")
    require_fragments(
        text,
        artifact,
        (
            "Do not edit files",
            "Return JSON only",
            '"role": "director_evaluator"',
            '"review": "REVIEW: PASS" or "REVIEW: HOLD"',
            '"candidate_fingerprint":',
            '"content_fingerprint":',
        ) + EVALUATOR_CRITERIA,
    )


def verify_no_placeholders(contents: Mapping[str, str], paths: Iterable[str]) -> None:
    for relative in paths:
        match = PLACEHOLDER_RE.search(contents[relative])
        if match is not None:
            raise VerificationError(
                f"Unresolved personalization placeholder in {relative}: {match.group(0)}"
            )


def verify_personal_rules(text: str) -> None:
    for label in (
        "Audience",
        "Decision horizon",
        "Output priority",
        "Evidence rule",
        "Escalate when",
        "Never do",
    ):
        list_field(text, label, "AGENTS.md")


def verify_harness_card(text: str) -> None:
    artifact = "Harness/HARNESS_CARD.md"
    required = (
        "Fixed outer flow:",
        "Bounded adaptive retrieval loop:",
        "Maximum model turns:",
        "Wall-clock limit:",
        "Retry ceiling:",
        "No-progress limit:",
        "Human approval",
        "Router — rejected:",
        "Parallel worker team — rejected:",
        "Plugin — rejected:",
        "New MCP server — rejected:",
        "Reflection without an oracle — rejected:",
    ) + tuple(reason + ":" for reason in sorted(ALLOWED_TERMINAL_REASONS))
    require_fragments(text, artifact, required)

    for label in ("Maximum model turns", "Wall-clock limit", "Retry ceiling", "No-progress limit"):
        value = list_field(text, label, artifact)
        match = re.search(r"\d+", value)
        if match is None or int(match.group(0)) < 1:
            raise VerificationError(f"{artifact} requires a positive numeric budget for {label}")

    rows = table_rows(text, ("Component", "Job", "Load timing", "Cost", "Disable path"), artifact)
    if len(rows) < 7:
        raise VerificationError(f"{artifact} component register needs at least seven concrete rows")
    for row in rows:
        if any(not value.strip() for value in row.values()):
            raise VerificationError(f"{artifact} component rows need job/load/cost/disable values")


def markdown_note_index(root: Path) -> Dict[str, Any]:
    by_path: Dict[str, str] = {}
    by_name: Dict[str, List[str]] = defaultdict(list)
    all_paths: List[str] = []
    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(root)
        if any(part in SKIPPED_MANIFEST_DIRS for part in relative.parts):
            continue
        if path.is_symlink() or not path.is_file():
            raise VerificationError(f"Vault Markdown entry must be a regular file: {relative.as_posix()}")
        relative_text = relative.as_posix()
        stem_path = relative.with_suffix("").as_posix().casefold()
        by_path[stem_path] = relative_text
        by_name[relative.stem.casefold()].append(relative_text)
        all_paths.append(relative_text)
    return {"by_path": by_path, "by_name": by_name, "all_paths": all_paths}


def wikilink_targets(text: str) -> List[str]:
    return [match.group(1).strip() for match in WIKILINK_RE.finditer(text)]


def normalize_link_target(raw: str, origin: str) -> str:
    target = raw.split("|", 1)[0].split("#", 1)[0].strip().replace("\\", "/")
    if target.casefold().endswith(".md"):
        target = target[:-3]
    if target.startswith("./"):
        target = target[2:]
    pure = PurePosixPath(target)
    if not target or pure.is_absolute() or ".." in pure.parts:
        raise VerificationError(f"Unsafe or empty wikilink in {origin}: [[{raw}]]")
    return pure.as_posix()


def resolve_wikilink(raw: str, origin: str, index: Mapping[str, Any]) -> str:
    target = normalize_link_target(raw, origin)
    direct = index["by_path"].get(target.casefold())
    if direct is not None:
        return str(direct)
    candidates = index["by_name"].get(PurePosixPath(target).name.casefold(), [])
    if not candidates:
        raise VerificationError(f"Missing wikilink target in {origin}: [[{raw}]]")
    if len(candidates) > 1:
        raise VerificationError(
            f"Ambiguous wikilink target in {origin}: [[{raw}]] -> {', '.join(candidates)}"
        )
    return str(candidates[0])


def is_evidence_root(relative: str) -> bool:
    parts = PurePosixPath(relative).parts
    return bool(parts) and parts[0] in {"00_Inbox", "Source_Packet"}


def scan_evidence_files(root: Path) -> List[str]:
    found: List[str] = []
    for base in (root / "00_Inbox", root / "Source_Packet"):
        if not base.is_dir() or base.is_symlink():
            raise VerificationError(f"Missing evidence directory or linked directory: {base.relative_to(root)}")
        for path in sorted(base.rglob("*.md")):
            if path.is_symlink() or not path.is_file():
                raise VerificationError(
                    f"Evidence root must be a regular file: {path.relative_to(root).as_posix()}"
                )
            found.append(path.relative_to(root).as_posix())
    return sorted(found)


def verify_source_manifest(root: Path) -> Tuple[Set[str], Dict[str, str]]:
    artifact = "Harness/SOURCE_MANIFEST.json"
    payload = read_regular_json(root, artifact)
    anchor_path = TRUSTED_SEED_ROOT / PurePosixPath(artifact)
    if anchor_path.is_symlink() or not anchor_path.is_file():
        raise VerificationError("Trusted course SOURCE_MANIFEST.json is missing or linked")
    if sha256_file(regular_path(root, artifact)) != sha256_file(anchor_path):
        raise VerificationError(
            "Copied SOURCE_MANIFEST.json bytes differ from the untouched course trust anchor"
        )
    try:
        anchor_payload = json.loads(anchor_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationError("Trusted course SOURCE_MANIFEST.json is invalid") from error
    if payload != anchor_payload:
        raise VerificationError(
            "Copied SOURCE_MANIFEST.json differs from the untouched course trust anchor"
        )
    payload = anchor_payload
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        raise VerificationError(f"{artifact} requires schema_version 1")
    if payload.get("allowed_roots") != list(EVIDENCE_ROOTS):
        raise VerificationError(f"{artifact} allowed_roots must be {list(EVIDENCE_ROOTS)!r}")
    sources = payload.get("sources")
    if not isinstance(sources, list) or not sources:
        raise VerificationError(f"{artifact} requires a non-empty sources array")

    actual_paths = scan_evidence_files(root)
    declared_paths: Set[str] = set()
    source_ids: Set[str] = set()
    texts: Dict[str, str] = {}
    for item_number, item in enumerate(sources, start=1):
        if not isinstance(item, dict) or set(item) != {"source_id", "path", "sha256"}:
            raise VerificationError(f"{artifact} source {item_number} has the wrong fields")
        source_id = item["source_id"]
        relative = item["path"]
        expected_hash = item["sha256"]
        if not isinstance(source_id, str) or not re.fullmatch(r"SRC-P4-\d{3}", source_id):
            raise VerificationError(f"{artifact} source {item_number} has an invalid source_id")
        if source_id in source_ids:
            raise VerificationError(f"{artifact} repeats source_id {source_id}")
        source_ids.add(source_id)
        if not isinstance(relative, str) or not relative.endswith(".md"):
            raise VerificationError(f"{artifact} source {source_id} has an invalid path")
        pure = PurePosixPath(relative)
        if pure.is_absolute() or ".." in pure.parts or not is_evidence_root(relative):
            raise VerificationError(f"{artifact} source {source_id} has an unsafe path")
        if not isinstance(expected_hash, str) or SHA256_RE.fullmatch(expected_hash) is None:
            raise VerificationError(f"{artifact} source {source_id} has an invalid SHA-256")
        if relative not in actual_paths:
            raise VerificationError(f"{artifact} source {source_id} is missing exact path {relative}")
        if relative in declared_paths:
            raise VerificationError(f"{artifact} repeats evidence path {relative}")
        actual_hash = sha256_file(root / PurePosixPath(relative))
        if actual_hash != expected_hash:
            raise VerificationError(f"Evidence-root hash mismatch for {relative}")
        declared_paths.add(relative)
        texts[relative] = read_regular_text(root, relative)

    undeclared = sorted(set(actual_paths) - declared_paths)
    if undeclared:
        raise VerificationError(f"Unmanifested evidence roots: {', '.join(undeclared)}")
    if declared_paths != set(actual_paths):
        raise VerificationError(f"{artifact} does not cover the exact evidence set")
    return declared_paths, texts


def generated_note_paths(index: Mapping[str, Any]) -> Set[str]:
    generated: Set[str] = set()
    for relative in index["all_paths"]:
        path = PurePosixPath(relative)
        if path.parts[0] in RESERVED_TOP_LEVEL or relative in RESERVED_ROOT_NOTES:
            continue
        generated.add(relative)
    return generated


def verify_note_graph(
    root: Path,
    index: Mapping[str, Any],
    evidence_paths: Set[str],
) -> Set[str]:
    generated = generated_note_paths(index)
    if not generated:
        raise VerificationError("The organized vault needs at least one generated normalized note")

    for relative in sorted(generated):
        text = read_regular_text(root, relative)
        lineage_lines = [
            line for line in text.splitlines() if re.match(r"^\s*Raw sources:\s*", line, re.IGNORECASE)
        ]
        lineage_links: List[str] = []
        for line in lineage_lines:
            lineage_links.extend(wikilink_targets(line))
        if not lineage_links:
            raise VerificationError(f"Generated note lacks raw-capture lineage in 'Raw sources:': {relative}")
        for raw in lineage_links:
            resolved = resolve_wikilink(raw, relative, index)
            if resolved not in evidence_paths:
                raise VerificationError(f"Generated note lineage is not a manifested evidence root: {relative}")

    moc_links = {
        resolve_wikilink(raw, "MOC.md", index)
        for raw in wikilink_targets(read_regular_text(root, "MOC.md"))
    }
    missing_hubs = sorted(set(HUB_PATHS) - moc_links)
    if missing_hubs:
        raise VerificationError(f"MOC.md must link every hub: {', '.join(missing_hubs)}")

    reachable: Set[str] = set(HUB_PATHS)
    queue = deque(HUB_PATHS)
    while queue:
        current = queue.popleft()
        text = read_regular_text(root, current)
        for raw in wikilink_targets(text):
            resolved = resolve_wikilink(raw, current, index)
            if resolved in evidence_paths or resolved in reachable:
                continue
            reachable.add(resolved)
            queue.append(resolved)
    orphaned = sorted(generated - reachable)
    if orphaned:
        raise VerificationError(
            "Generated normalized notes are not reachable MOC -> hub -> note: " + ", ".join(orphaned)
        )
    return generated


def verify_trace_rows(text: str, terminal_reason: Optional[str] = None) -> None:
    artifact = "Harness/RUN_TRACE.md"
    rows = table_rows(
        text,
        ("Step", "Observable action", "Observation or evidence", "Budget after step", "Outcome"),
        artifact,
    )
    if not rows:
        raise VerificationError(f"{artifact} needs at least one observable action row")
    for row in rows:
        if any(not value.strip() for value in row.values()):
            raise VerificationError(f"{artifact} rows must keep action, evidence, budget, and outcome")
    header_text = " ".join(rows[0].keys()).casefold()
    if "thought" in header_text or "reasoning" in header_text:
        raise VerificationError(f"{artifact} must not request hidden reasoning or chain-of-thought")
    if terminal_reason is not None:
        trace_terminal = last_colon_field(text, "Terminal reason", artifact).upper()
        if trace_terminal != terminal_reason:
            raise VerificationError(
                f"Terminal reason mismatch: RUN_STATE={terminal_reason}, RUN_TRACE={trace_terminal}"
            )


def verify_retrieval_ledger(
    text: str,
    index: Mapping[str, Any],
    evidence_paths: Set[str],
    evidence_texts: Mapping[str, str],
) -> Set[str]:
    artifact = "Harness/RUN_TRACE.md"
    fixed_rows = table_rows(
        text,
        ("Fixed inbox capture", "Observable result"),
        artifact,
    )
    required_initial = {path for path in evidence_paths if path.startswith("00_Inbox/")}
    fixed_opened: Set[str] = set()
    for row_number, row in enumerate(fixed_rows, start=1):
        links = wikilink_targets(row["Fixed inbox capture"])
        if len(links) != 1 or not row["Observable result"].strip():
            raise VerificationError(f"{artifact} fixed-inbox row {row_number} needs one capture and a result")
        resolved = resolve_wikilink(links[0], artifact, index)
        if resolved not in required_initial or resolved in fixed_opened:
            raise VerificationError(f"{artifact} fixed-inbox row {row_number} is repeated or not an inbox capture")
        fixed_opened.add(resolved)
    if fixed_opened != required_initial:
        missing = sorted(required_initial - fixed_opened)
        raise VerificationError(
            "Fixed inbox inventory must read all four captures exactly once: " + ", ".join(missing)
        )

    rows = table_rows(
        text,
        ("Open", "Evidence root", "Reference discovered in", "Observable result"),
        artifact,
    )
    if not rows or len(rows) > 6:
        raise VerificationError(f"{artifact} retrieval ledger must contain 1 to 6 opens")
    opened: List[str] = []
    adaptive_hops = 0
    for row_number, row in enumerate(rows, start=1):
        if row["Open"].strip() != str(row_number):
            raise VerificationError(f"{artifact} retrieval opens must be numbered 1 through {len(rows)}")
        roots = wikilink_targets(row["Evidence root"])
        if len(roots) != 1 or not row["Observable result"].strip():
            raise VerificationError(f"{artifact} retrieval row {row_number} needs one root and a result")
        current = resolve_wikilink(roots[0], artifact, index)
        if current not in evidence_paths or not current.startswith("Source_Packet/"):
            raise VerificationError(
                f"Retrieval row {row_number} must open a manifested Source_Packet record: {current}"
            )
        if current in opened:
            raise VerificationError(f"Retrieval ledger repeats an evidence root: {current}")

        parents = wikilink_targets(row["Reference discovered in"])
        if len(parents) != 1:
            raise VerificationError(
                f"Retrieval row {row_number} needs one fixed-inbox or previously opened evidence root"
            )
        parent = resolve_wikilink(parents[0], artifact, index)
        if parent not in fixed_opened and parent not in opened:
            raise VerificationError(
                f"Unearned retrieval open {current}: {parent} was not opened earlier"
            )
        referenced = {
            resolve_wikilink(raw, parent, index)
            for raw in wikilink_targets(evidence_texts[parent])
        }
        if current not in referenced:
            raise VerificationError(
                f"Unearned retrieval open {current}: {parent} does not reference it"
            )
        if parent in opened:
            adaptive_hops += 1
        opened.append(current)

    if adaptive_hops < 1:
        raise VerificationError(
            f"{artifact} retrieval ledger needs at least one earned Source_Packet-to-Source_Packet hop"
        )
    return fixed_opened | set(opened)


def verify_answers(
    contents: Mapping[str, str],
    index: Mapping[str, Any],
    evidence_paths: Set[str],
    opened_paths: Set[str],
) -> Tuple[CounterType[str], Dict[str, Dict[str, str]], Dict[str, List[str]]]:
    total: CounterType[str] = Counter()
    claims: Dict[str, Dict[str, str]] = {}
    per_answer: Dict[str, List[str]] = {}
    for relative in ANSWER_PATHS:
        resolved: List[str] = []
        expected_prefix = "Q1-" if relative == ANSWER_PATHS[0] else "Q2-"
        parsed_link_count = 0
        for line_number, line in enumerate(contents[relative].splitlines(), start=1):
            if not line.strip() or re.match(r"^\s*#{1,6}\s+", line):
                continue
            if not re.match(r"^\s*[-*]\s+", line):
                raise VerificationError(
                    f"{relative} line {line_number} must be a heading or stable-ID claim bullet"
                )
            match = CLAIM_BULLET_RE.match(line)
            if match is None:
                raise VerificationError(
                    f"{relative} claim bullet on line {line_number} needs a stable [Q1-##]/[Q2-##] ID"
                )
            claim_id, body = match.groups()
            if not claim_id.startswith(expected_prefix) or claim_id in claims:
                raise VerificationError(f"{relative} has a duplicate or wrong-prefix claim ID: {claim_id}")
            links = wikilink_targets(body)
            if len(links) != 1:
                raise VerificationError(f"{relative} claim {claim_id} needs exactly one direct evidence link")
            evidence = resolve_wikilink(links[0], relative, index)
            claim_text = WIKILINK_RE.sub("", body).strip()
            if not claim_text:
                raise VerificationError(f"{relative} claim {claim_id} has no wording")
            resolved.append(evidence)
            parsed_link_count += 1
            claims[claim_id] = {"answer": relative, "text": claim_text, "evidence": evidence}
        if parsed_link_count != len(wikilink_targets(contents[relative])):
            raise VerificationError(f"{relative} may place evidence links only in stable-ID claim bullets")
        invalid = sorted({item for item in resolved if item not in evidence_paths})
        if invalid:
            raise VerificationError(
                f"{relative} must cite evidence roots directly, not generated summaries: {', '.join(invalid)}"
            )
        unearned = sorted(set(resolved) - opened_paths)
        if unearned:
            raise VerificationError(
                f"{relative} cites evidence not earned in the retrieval ledger: {', '.join(unearned)}"
            )
        if len(set(resolved)) < 2:
            raise VerificationError(f"{relative} must cite at least two distinct evidence roots")
        packet_count = len({item for item in resolved if item.startswith("Source_Packet/")})
        if packet_count < 2:
            raise VerificationError(
                f"{relative} must use at least two earned Source_Packet roots so retrieval changes the answer"
            )
        total.update(resolved)
        per_answer[relative] = resolved
    return total, claims, per_answer


def verify_audit(
    text: str,
    answer_claims: Mapping[str, Mapping[str, str]],
    index: Mapping[str, Any],
    evidence_paths: Set[str],
    evidence_texts: Mapping[str, str],
    opened_paths: Set[str],
) -> Tuple[CounterType[str], Dict[str, Dict[str, str]], Set[str]]:
    artifact = "Audit.md"
    rows = table_rows(
        text,
        ("Claim ID", "Claim", "Evidence root", "Source excerpt", "Disposition", "Resolution"),
        artifact,
    )
    if not rows:
        raise VerificationError("Audit.md contains no disposition rows")
    audited: CounterType[str] = Counter()
    supported: Dict[str, Dict[str, str]] = {}
    adverse_claim_ids: Set[str] = set()
    audit_ids: Set[str] = set()
    for row_number, row in enumerate(rows, start=1):
        claim_id = row["Claim ID"].strip()
        links = wikilink_targets(row["Evidence root"])
        excerpt = row["Source excerpt"].strip()
        if (
            CLAIM_BULLET_RE.fullmatch(f"- [{claim_id}] x") is None
            or claim_id in audit_ids
            or not row["Claim"].strip()
            or len(links) != 1
            or not excerpt
        ):
            raise VerificationError(
                f"Audit.md row {row_number} needs a unique stable ID, claim, evidence root, and excerpt"
            )
        audit_ids.add(claim_id)
        resolved = resolve_wikilink(links[0], artifact, index)
        if resolved not in evidence_paths:
            raise VerificationError(f"Audit.md row {row_number} must cite a direct evidence root")
        if resolved not in opened_paths:
            raise VerificationError(f"Audit.md row {row_number} cites evidence not earned by the run")
        if excerpt not in evidence_texts[resolved]:
            raise VerificationError(
                f"Audit.md row {row_number} source excerpt is not an exact substring of {resolved}"
            )
        disposition = clean_token(row["Disposition"])
        if disposition not in ALLOWED_DISPOSITIONS:
            raise VerificationError(
                f"Invalid audit disposition on row {row_number}: {row['Disposition']!r}"
            )
        resolution = clean_token(row["Resolution"])
        if disposition != "support" and resolution in {"", "none", "n/a", "na", "—", "-"}:
            raise VerificationError(f"Audit.md row {row_number} needs a resolution for {disposition}")
        audited[resolved] += 1
        final_claim = answer_claims.get(claim_id)
        if final_claim is None:
            if disposition == "support" or not resolution.startswith("removed"):
                raise VerificationError(
                    f"Audit.md removed claim {claim_id} must be PARTIAL/NOT SUPPORTED with Resolution starting REMOVED:"
                )
        else:
            if resolved != final_claim["evidence"]:
                raise VerificationError(f"Audit.md claim {claim_id} changed its answer evidence root")
            if disposition == "not supported":
                raise VerificationError(f"Final answers must remove NOT SUPPORTED claim {claim_id}")
            if disposition == "support":
                if row["Claim"].strip() != final_claim["text"]:
                    raise VerificationError(f"Audit.md SUPPORT wording does not match final claim {claim_id}")
                supported[claim_id] = {"evidence": resolved, "text": final_claim["text"]}
            else:
                prefix = "QUALIFIED:"
                if not row["Resolution"].strip().upper().startswith(prefix):
                    raise VerificationError(
                        f"Audit.md retained PARTIAL claim {claim_id} needs Resolution 'QUALIFIED: <final wording>'"
                    )
                qualified = row["Resolution"].strip()[len(prefix) :].strip()
                if qualified != final_claim["text"]:
                    raise VerificationError(f"Audit.md qualification does not match final claim {claim_id}")
                adverse_claim_ids.add(claim_id)
        if disposition != "support":
            adverse_claim_ids.add(claim_id)

    missing_ids = sorted(set(answer_claims) - audit_ids)
    if missing_ids:
        raise VerificationError("Final answer claims lack audit rows: " + ", ".join(missing_ids))
    return audited, supported, adverse_claim_ids


def verify_brief(
    text: str,
    supported: Mapping[str, Mapping[str, str]],
    index: Mapping[str, Any],
    evidence_paths: Set[str],
) -> List[str]:
    artifact = "Morning_Brief.md"
    if PROVENANCE_RE.search(text) is None:
        raise VerificationError(
            "Morning_Brief.md must declare 'Provenance: vault only; audited sources only'"
        )
    resolved: List[str] = []
    used_ids: Set[str] = set()
    body_started = False
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip() or PROVENANCE_RE.fullmatch(line) is not None:
            continue
        if re.match(r"^\s*#{1,6}\s+", line):
            if re.match(r"^\s*##\s+", line):
                body_started = True
            continue
        if body_started and re.match(r"^\s*[-*]\s+", line):
            match = CLAIM_BULLET_RE.match(line)
            if match is None:
                raise VerificationError(
                    f"Morning_Brief.md claim bullet on line {line_number} needs a stable claim ID"
                )
            claim_id, body = match.groups()
            links = wikilink_targets(body)
            if claim_id in used_ids or len(links) != 1:
                raise VerificationError(f"Morning_Brief.md claim {claim_id} is repeated or lacks one link")
            relative = resolve_wikilink(links[0], artifact, index)
            claim_text = WIKILINK_RE.sub("", body).strip()
            support = supported.get(claim_id)
            if (
                relative not in evidence_paths
                or support is None
                or support["evidence"] != relative
                or support["text"] != claim_text
            ):
                raise VerificationError(
                    f"Morning_Brief.md claim {claim_id} lacks matching audited SUPPORT wording+root"
                )
            used_ids.add(claim_id)
            resolved.append(relative)
            continue
        raise VerificationError(
            f"Morning_Brief.md line {line_number} must be a heading, provenance line, or stable-ID claim bullet"
        )
    if len(used_ids) < 2:
        raise VerificationError("Morning_Brief.md must carry at least two distinct SUPPORT claim IDs")
    if len(resolved) != len(wikilink_targets(text)):
        raise VerificationError("Morning_Brief.md may place evidence links only in stable-ID claim bullets")
    return resolved


def verify_resume_receipt(
    root: Path,
    text: str,
    trace_text: str,
    generated_notes: Set[str],
    evidence_paths: Set[str],
    adverse_claim_ids: Set[str],
) -> Dict[str, Any]:
    artifact = "Harness/RESUME_RECEIPT.md"
    result = list_field(text, "Resume result", artifact).upper()
    prior_id = list_field(text, "Prior run ID", artifact)
    resumed_id = list_field(text, "Resumed run ID", artifact)
    saved_action = list_field(text, "Saved next permitted action", artifact)
    first_action = list_field(text, "First resumed action", artifact)
    reprocessed = integer_field(text, "Reprocessed source count", artifact)
    recreated = integer_field(text, "Recreated normalized note count", artifact)
    if result != "PASS" or prior_id == resumed_id or reprocessed != 0 or recreated != 0:
        raise VerificationError(
            f"{artifact} must prove a fresh PASS resume with zero reprocessing and zero note recreation"
        )
    if clean_token(saved_action) != clean_token(first_action):
        raise VerificationError(
            f"{artifact} first resumed action must equal the saved next permitted action"
        )

    preserved_rows = table_rows(
        text,
        ("Preserved artifact", "Before SHA-256", "After SHA-256", "Result"),
        artifact,
    )
    expected_preserved = {
        path for path in evidence_paths if path.startswith("00_Inbox/processed/")
    } | generated_notes
    recorded: Set[str] = set()
    for row_number, row in enumerate(preserved_rows, start=1):
        relative = clean_path_cell(row["Preserved artifact"])
        before = clean_token(row["Before SHA-256"])
        after = clean_token(row["After SHA-256"])
        if relative in recorded:
            raise VerificationError(f"{artifact} repeats preserved artifact {relative}")
        if relative not in expected_preserved:
            raise VerificationError(f"{artifact} row {row_number} names an unexpected preserved artifact")
        if SHA256_RE.fullmatch(before) is None or SHA256_RE.fullmatch(after) is None:
            raise VerificationError(f"{artifact} row {row_number} needs two lowercase SHA-256 values")
        if before != after or after != sha256_file(regular_path(root, relative)):
            raise VerificationError(f"{artifact} does not prove byte-identical resume for {relative}")
        if clean_token(row["Result"]) != "unchanged":
            raise VerificationError(f"{artifact} row {row_number} Result must be UNCHANGED")
        recorded.add(relative)
    if recorded != expected_preserved:
        missing = sorted(expected_preserved - recorded)
        raise VerificationError(f"{artifact} lacks preserved-artifact hashes: {', '.join(missing)}")

    answer_rows = table_rows(
        text,
        (
            "Answer artifact",
            "Saved-at-pause SHA-256",
            "Fresh-open SHA-256",
            "Final SHA-256",
            "Authorized audit finding",
        ),
        artifact,
    )
    answer_recorded: Set[str] = set()
    normalized_adverse = {clean_token(claim_id) for claim_id in adverse_claim_ids}
    for row_number, row in enumerate(answer_rows, start=1):
        relative = clean_path_cell(row["Answer artifact"])
        saved = clean_token(row["Saved-at-pause SHA-256"])
        fresh = clean_token(row["Fresh-open SHA-256"])
        final = clean_token(row["Final SHA-256"])
        authorization = clean_token(row["Authorized audit finding"])
        if relative not in ANSWER_PATHS or relative in answer_recorded:
            raise VerificationError(f"{artifact} answer row {row_number} has an invalid artifact")
        if any(SHA256_RE.fullmatch(value) is None for value in (saved, fresh, final)):
            raise VerificationError(f"{artifact} answer row {row_number} needs three SHA-256 values")
        if saved != fresh:
            raise VerificationError(
                f"{artifact} answer {relative} changed before the fresh resume action"
            )
        if final != sha256_file(regular_path(root, relative)):
            raise VerificationError(f"{artifact} answer final hash does not match {relative}")
        if saved == final:
            if authorization != "none":
                raise VerificationError(f"{artifact} unchanged answer {relative} must use authorization NONE")
        elif authorization not in normalized_adverse:
            raise VerificationError(
                f"{artifact} changed answer {relative} lacks a named PARTIAL/NOT SUPPORTED claim ID"
            )
        if authorization != "none":
            expected_prefix = "q1-" if relative == ANSWER_PATHS[0] else "q2-"
            if not authorization.startswith(expected_prefix):
                raise VerificationError(
                    f"{artifact} authorization {authorization} belongs to the other answer"
                )
        answer_recorded.add(relative)
    if answer_recorded != set(ANSWER_PATHS):
        raise VerificationError(f"{artifact} must cover both answer artifacts")
    if "resume result: pass" not in trace_text.casefold() or resumed_id.casefold() not in trace_text.casefold():
        raise VerificationError(f"Harness/RUN_TRACE.md must record the fresh resume result and resumed run ID")
    return {"result": result, "resumed_run_id": resumed_id}


def ratio(value: str, artifact: str) -> Tuple[int, int]:
    match = re.fullmatch(r"\s*(\d+)\s*/\s*(\d+)\s*", value)
    if match is None:
        raise VerificationError(f"{artifact} Overclaim must use n/m form")
    return int(match.group(1)), int(match.group(2))


def load_evaluator_receipt(root: Path, relative: str) -> Dict[str, Any]:
    payload = read_regular_json(root, relative)
    if not isinstance(payload, dict) or set(payload) != {
        "role",
        "review",
        "candidate_fingerprint",
        "content_fingerprint",
        "criteria",
        "findings",
    }:
        raise VerificationError(f"{relative} does not match the exact evaluator receipt schema")
    if payload["role"] != "director_evaluator" or payload["review"] not in {
        "REVIEW: PASS",
        "REVIEW: HOLD",
    }:
        raise VerificationError(f"{relative} has an invalid role or review")
    if (
        not isinstance(payload["candidate_fingerprint"], str)
        or SHA256_RE.fullmatch(payload["candidate_fingerprint"]) is None
    ):
        raise VerificationError(f"{relative} has an invalid candidate_fingerprint")
    if (
        not isinstance(payload["content_fingerprint"], str)
        or SHA256_RE.fullmatch(payload["content_fingerprint"]) is None
    ):
        raise VerificationError(f"{relative} has an invalid content_fingerprint")
    criteria = payload["criteria"]
    if not isinstance(criteria, list) or len(criteria) != len(EVALUATOR_CRITERIA):
        raise VerificationError(f"{relative} must contain all {len(EVALUATOR_CRITERIA)} rubric criteria")
    seen: List[str] = []
    holds: Set[str] = set()
    for row_number, row in enumerate(criteria, start=1):
        if not isinstance(row, dict) or set(row) != {
            "criterion",
            "verdict",
            "evidence_opened",
            "finding",
        }:
            raise VerificationError(f"{relative} criterion {row_number} has the wrong fields")
        criterion = row["criterion"]
        verdict = row["verdict"]
        evidence = row["evidence_opened"]
        finding = row["finding"]
        if criterion != EVALUATOR_CRITERIA[row_number - 1]:
            raise VerificationError(f"{relative} criterion order or wording changed at row {row_number}")
        if verdict not in {"PASS", "HOLD"}:
            raise VerificationError(f"{relative} criterion {row_number} has an invalid verdict")
        if not isinstance(evidence, list) or not evidence or not all(
            isinstance(item, str) and item.strip() for item in evidence
        ):
            raise VerificationError(f"{relative} criterion {row_number} lacks opened evidence")
        if len(set(evidence)) != len(evidence):
            raise VerificationError(f"{relative} criterion {row_number} repeats opened evidence")
        for opened in evidence:
            normalized = opened.replace("\\", "/")
            pure = PurePosixPath(normalized)
            if pure.is_absolute() or ".." in pure.parts or normalized != pure.as_posix():
                raise VerificationError(
                    f"{relative} criterion {row_number} has an unsafe evidence path: {opened}"
                )
            regular_path(root, normalized)
        if not isinstance(finding, str) or not finding.strip():
            raise VerificationError(f"{relative} criterion {row_number} lacks a finding")
        if verdict == "PASS" and clean_token(finding) != "none":
            raise VerificationError(f"{relative} PASS criterion {row_number} must record finding NONE")
        if verdict == "HOLD":
            if clean_token(finding) == "none":
                raise VerificationError(f"{relative} HOLD criterion {row_number} needs a finding")
            holds.add(criterion)
        seen.append(criterion)

    findings = payload["findings"]
    if not isinstance(findings, list):
        raise VerificationError(f"{relative} findings must be an array")
    blocker_by_criterion: Dict[str, str] = {}
    for item_number, item in enumerate(findings, start=1):
        if not isinstance(item, dict) or set(item) != {"criterion", "severity", "summary"}:
            raise VerificationError(f"{relative} finding {item_number} has the wrong fields")
        if item["criterion"] not in EVALUATOR_CRITERIA or item["severity"] not in {"blocker", "note"}:
            raise VerificationError(f"{relative} finding {item_number} has an invalid criterion or severity")
        if not isinstance(item["summary"], str) or not item["summary"].strip():
            raise VerificationError(f"{relative} finding {item_number} lacks a summary")
        if item["severity"] == "blocker":
            if item["criterion"] in blocker_by_criterion:
                raise VerificationError(
                    f"{relative} has duplicate blocker findings for {item['criterion']}"
                )
            blocker_by_criterion[item["criterion"]] = item["summary"]

    for row in criteria:
        if row["verdict"] == "HOLD" and blocker_by_criterion.get(row["criterion"]) != row["finding"]:
            raise VerificationError(f"{relative} must preserve each HOLD as a matching blocker finding")
    if set(blocker_by_criterion) != holds:
        raise VerificationError(f"{relative} blocker findings do not match its HOLD criteria")
    expected_review = "REVIEW: HOLD" if holds else "REVIEW: PASS"
    if payload["review"] != expected_review:
        raise VerificationError(f"{relative} review does not match its criterion verdicts")
    return payload


def load_candidate_receipt(
    root: Path, relative: str
) -> Tuple[str, str, str, str, str, int, str]:
    path = regular_path(root, relative)
    data = path.read_bytes()
    text: Optional[str] = None
    for encoding in ("utf-8-sig", "utf-16"):
        try:
            text = data.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    if text is None or not text.strip():
        raise VerificationError(f"{relative} is empty or not UTF-8/UTF-16 text")
    text = text.strip()
    if "\n" in text:
        raise VerificationError(f"{relative} must contain the exact one-line candidate checker output")
    fingerprint_match = re.search(
        r"; fingerprint ([0-9a-f]{64}); content ([0-9a-f]{64}); "
        r"stateid ([0-9a-f]{64}); trace (\d+):([0-9a-f]{64})$",
        text,
    )
    if fingerprint_match is None:
        raise VerificationError(f"{relative} lacks the candidate snapshot fingerprint")
    fingerprint = fingerprint_match.group(1)
    content_fingerprint = fingerprint_match.group(2)
    state_identity = fingerprint_match.group(3)
    trace_bytes = int(fingerprint_match.group(4))
    trace_hash = fingerprint_match.group(5)
    status_text = text[: fingerprint_match.start()]
    if status_text.startswith("PASS P4 candidate:"):
        return (
            "PASS",
            "NONE",
            fingerprint,
            content_fingerprint,
            state_identity,
            trace_bytes,
            trace_hash,
        )
    if status_text.startswith("HOLD P4 vault:"):
        finding = status_text[len("HOLD P4 vault:") :].strip()
        if not finding:
            raise VerificationError(f"{relative} HOLD output lacks its finding")
        return (
            "HOLD",
            finding,
            fingerprint,
            content_fingerprint,
            state_identity,
            trace_bytes,
            trace_hash,
        )
    raise VerificationError(f"{relative} is not exact candidate checker output")


def verify_evaluation(root: Path, text: str, trace_text: str) -> Dict[str, Any]:
    artifact = "Harness/EVAL.md"
    context = list_field(text, "Evaluator context", artifact).upper()
    access = list_field(text, "Access", artifact).upper()
    default = list_field(text, "Default", artifact).upper()
    generator_overall = list_field(text, "Generator first-pass verdict", artifact).upper()
    candidate_first = list_field(text, "Candidate verifier first-pass verdict", artifact).upper()
    candidate_finding = list_field(text, "Candidate verifier first-pass finding", artifact)
    evaluator_first = list_field(text, "Fresh evaluator first-pass verdict", artifact).upper()
    claimed = integer_field(text, "First-pass criteria claimed ready", artifact)
    held = integer_field(text, "First-pass evaluator HOLD criteria", artifact)
    overclaimed = integer_field(text, "First-pass overclaim criteria", artifact)
    overclaim_text = list_field(text, "Overclaim", artifact)
    repairs = integer_field(text, "Repair cycles used", artifact)
    repair_scope = list_field(text, "Repair scope", artifact).upper()
    repair_justification = list_field(text, "Repair justification", artifact)
    final_verifier = list_field(text, "Final candidate verifier verdict", artifact).upper()
    final_evaluator = list_field(text, "Final evaluator verdict", artifact).upper()
    verdict = list_field(text, "Verdict", artifact).upper()
    first_path = clean_path_cell(list_field(text, "First evaluator receipt", artifact))
    first_hash = clean_token(list_field(text, "First evaluator SHA-256", artifact))
    final_path = clean_path_cell(list_field(text, "Final evaluator receipt", artifact))
    final_hash = clean_token(list_field(text, "Final evaluator SHA-256", artifact))
    first_candidate_path = clean_path_cell(list_field(text, "First candidate receipt", artifact))
    first_candidate_hash = clean_token(list_field(text, "First candidate SHA-256", artifact))
    final_candidate_path = clean_path_cell(list_field(text, "Final candidate receipt", artifact))
    final_candidate_hash = clean_token(list_field(text, "Final candidate SHA-256", artifact))
    if context != "FRESH" or access != "READ_ONLY" or default != "FAIL":
        raise VerificationError(f"{artifact} requires context FRESH, access READ_ONLY, and default FAIL")
    if generator_overall not in {"READY", "NOT READY"}:
        raise VerificationError(f"{artifact} has an invalid generator first-pass verdict")
    if candidate_first not in {"PASS", "HOLD"} or evaluator_first not in {"PASS", "HOLD"}:
        raise VerificationError(f"{artifact} has an invalid first-pass verifier/evaluator verdict")
    if repairs not in {0, 1}:
        raise VerificationError(f"{artifact} permits at most one total repair cycle")
    if repair_scope not in {"NONE", "CONTENT", "CONTROL_ONLY"}:
        raise VerificationError(f"{artifact} Repair scope must be NONE, CONTENT, or CONTROL_ONLY")
    if final_verifier != "PASS" or final_evaluator != "PASS" or verdict != "PASS":
        raise VerificationError(f"{artifact} final verifier, evaluator, and overall Verdict must be PASS")
    if first_path != "Harness/DIRECTOR_EVALUATOR_FIRST.json":
        raise VerificationError(f"{artifact} must bind the first receipt at {first_path!r}")
    if SHA256_RE.fullmatch(first_hash) is None or first_hash != sha256_file(regular_path(root, first_path)):
        raise VerificationError(f"{artifact} first evaluator receipt SHA-256 does not match")
    first_receipt = load_evaluator_receipt(root, first_path)

    if first_candidate_path != "Harness/CANDIDATE_CHECK_FIRST.txt":
        raise VerificationError(f"{artifact} must bind the first candidate receipt")
    if (
        SHA256_RE.fullmatch(first_candidate_hash) is None
        or first_candidate_hash != sha256_file(regular_path(root, first_candidate_path))
    ):
        raise VerificationError(f"{artifact} first candidate receipt SHA-256 does not match")
    (
        candidate_receipt_verdict,
        candidate_receipt_finding,
        first_candidate_fingerprint,
        first_content_fingerprint,
        first_state_identity,
        first_trace_bytes,
        first_trace_hash,
    ) = load_candidate_receipt(root, first_candidate_path)
    if candidate_first != candidate_receipt_verdict:
        raise VerificationError(f"{artifact} first candidate verdict does not match its receipt")
    if clean_token(candidate_finding) != clean_token(candidate_receipt_finding):
        raise VerificationError(f"{artifact} first candidate finding does not match its receipt")

    needs_repair = candidate_first == "HOLD" or first_receipt["review"] == "REVIEW: HOLD"
    if repairs != int(needs_repair):
        raise VerificationError(f"{artifact} repair count does not match first-pass HOLD evidence")
    if candidate_first == "PASS":
        if clean_token(candidate_finding) != "none":
            raise VerificationError(f"{artifact} candidate PASS must record first-pass finding NONE")
    else:
        if clean_token(candidate_finding) in {"", "none"}:
            raise VerificationError(f"{artifact} candidate HOLD must preserve its first-pass finding")
        if candidate_finding.casefold() not in trace_text.casefold():
            raise VerificationError("Harness/RUN_TRACE.md must retain the candidate verifier HOLD finding")

    if repairs == 0:
        if final_candidate_path != first_candidate_path or final_candidate_hash != first_candidate_hash:
            raise VerificationError(f"{artifact} zero-repair run must use the first candidate receipt as final")
        if (root / "Harness" / "CANDIDATE_CHECK_FINAL.txt").exists():
            raise VerificationError("A zero-repair run must not create CANDIDATE_CHECK_FINAL.txt")
        final_candidate_verdict = candidate_receipt_verdict
        final_candidate_fingerprint = first_candidate_fingerprint
        final_content_fingerprint = first_content_fingerprint
        final_state_identity = first_state_identity
        final_trace_bytes = first_trace_bytes
        final_trace_hash = first_trace_hash
        if final_path != first_path or final_hash != first_hash:
            raise VerificationError(f"{artifact} zero-repair run must use the first receipt as final")
        if (root / "Harness" / "DIRECTOR_EVALUATOR_FINAL.json").exists():
            raise VerificationError("A zero-repair run must not create DIRECTOR_EVALUATOR_FINAL.json")
        final_receipt = first_receipt
    else:
        if final_candidate_path != "Harness/CANDIDATE_CHECK_FINAL.txt":
            raise VerificationError(f"{artifact} repaired run requires CANDIDATE_CHECK_FINAL.txt")
        if (
            SHA256_RE.fullmatch(final_candidate_hash) is None
            or final_candidate_hash != sha256_file(regular_path(root, final_candidate_path))
        ):
            raise VerificationError(f"{artifact} final candidate receipt SHA-256 does not match")
        (
            final_candidate_verdict,
            _,
            final_candidate_fingerprint,
            final_content_fingerprint,
            final_state_identity,
            final_trace_bytes,
            final_trace_hash,
        ) = load_candidate_receipt(root, final_candidate_path)
        if final_candidate_fingerprint == first_candidate_fingerprint:
            raise VerificationError(f"{artifact} repair cycle did not change the candidate fingerprint")
        if final_path != "Harness/DIRECTOR_EVALUATOR_FINAL.json":
            raise VerificationError(f"{artifact} repaired run requires DIRECTOR_EVALUATOR_FINAL.json")
        if (
            SHA256_RE.fullmatch(final_hash) is None
            or final_hash != sha256_file(regular_path(root, final_path))
        ):
            raise VerificationError(f"{artifact} final evaluator receipt SHA-256 does not match")
        final_receipt = load_evaluator_receipt(root, final_path)
    if final_candidate_verdict != "PASS":
        raise VerificationError(f"{artifact} final candidate receipt remains on HOLD")
    if final_receipt["review"] != "REVIEW: PASS":
        raise VerificationError(f"{artifact} final evaluator receipt remains on HOLD")
    if first_receipt["candidate_fingerprint"] != first_candidate_fingerprint:
        raise VerificationError(
            f"{artifact} first evaluator receipt is not bound to the candidate it was allowed to inspect"
        )
    if first_receipt["content_fingerprint"] != first_content_fingerprint:
        raise VerificationError(
            f"{artifact} first evaluator receipt is not bound to first evaluated content"
        )
    if final_receipt["candidate_fingerprint"] != final_candidate_fingerprint:
        raise VerificationError(f"{artifact} final evaluator receipt is not bound to final candidate")
    if final_receipt["content_fingerprint"] != final_content_fingerprint:
        raise VerificationError(f"{artifact} final evaluator receipt is not bound to final content")
    current_content_fingerprint = evaluated_content_fingerprint(root)
    if current_content_fingerprint != final_content_fingerprint:
        raise VerificationError(
            f"{artifact} evaluator-approved content changed after the final candidate receipt"
        )
    if final_state_identity != first_state_identity:
        raise VerificationError(f"{artifact} RUN_STATE Run ID or Goal changed during evaluation")
    current_state_identity = state_identity_fingerprint(root)
    if current_state_identity != final_state_identity:
        raise VerificationError(f"{artifact} RUN_STATE identity changed after evaluation")
    current_trace = regular_path(root, "Harness/RUN_TRACE.md").read_bytes()
    if len(current_trace) < first_trace_bytes:
        raise VerificationError(f"{artifact} RUN_TRACE.md is shorter than its first evaluated prefix")
    if sha256_bytes(current_trace[:first_trace_bytes]) != first_trace_hash:
        raise VerificationError(f"{artifact} first evaluator-approved RUN_TRACE prefix was rewritten")
    if len(current_trace) < final_trace_bytes:
        raise VerificationError(f"{artifact} RUN_TRACE.md is shorter than its evaluated prefix")
    if sha256_bytes(current_trace[:final_trace_bytes]) != final_trace_hash:
        raise VerificationError(f"{artifact} final evaluator-approved RUN_TRACE prefix was rewritten")
    closeout = current_trace[final_trace_bytes:].decode("utf-8", errors="replace")
    normalized_closeout = closeout.replace("\r\n", "\n").strip()
    if normalized_closeout != TRACE_CLOSEOUT.strip():
        raise VerificationError(
            f"{artifact} RUN_TRACE closeout must match the exact post-evaluation block"
        )

    first_blockers: List[str] = []
    if candidate_first == "HOLD":
        first_blockers.append(candidate_finding)
    first_evaluator_holds = {
        row["criterion"]: row["finding"]
        for row in first_receipt["criteria"]
        if row["verdict"] == "HOLD"
    }
    first_blockers.extend(first_evaluator_holds.values())
    if repairs == 0:
        if repair_scope != "NONE" or clean_token(repair_justification) != "none":
            raise VerificationError(f"{artifact} zero-repair run must record Repair scope and justification NONE")
    else:
        if clean_token(repair_justification) in {"", "none"}:
            raise VerificationError(f"{artifact} repaired run needs a blocker-grounded Repair justification")
        missing_justifications = [
            finding
            for finding in first_blockers
            if finding.casefold() not in repair_justification.casefold()
        ]
        if missing_justifications:
            raise VerificationError(f"{artifact} Repair justification must preserve every first blocker")
        content_changed = final_content_fingerprint != first_content_fingerprint
        if content_changed:
            if repair_scope != "CONTENT":
                raise VerificationError(f"{artifact} changed stable mission content requires Repair scope CONTENT")
        else:
            if repair_scope != "CONTROL_ONLY":
                raise VerificationError(
                    f"{artifact} unchanged stable mission content requires an explicit CONTROL_ONLY repair"
                )
            non_control_holds = set(first_evaluator_holds) - CONTROL_ONLY_EVALUATOR_CRITERIA
            if non_control_holds:
                raise VerificationError(
                    f"{artifact} evaluator content blockers require a changed stable-content fingerprint"
                )
            if candidate_first == "HOLD" and not candidate_finding_is_control_only(candidate_finding):
                raise VerificationError(
                    f"{artifact} candidate content blocker requires a changed stable-content fingerprint"
                )

    expected_evaluator_first = "HOLD" if first_receipt["review"] == "REVIEW: HOLD" else "PASS"
    if evaluator_first != expected_evaluator_first:
        raise VerificationError(f"{artifact} first-pass evaluator verdict does not match its receipt")

    rows = table_rows(
        text,
        (
            "Criterion",
            "Generator first-pass claim",
            "Evidence opened",
            "Fresh evaluator first-pass verdict",
            "Final verdict",
        ),
        artifact,
    )
    if [row["Criterion"] for row in rows] != list(EVALUATOR_CRITERIA):
        raise VerificationError(f"{artifact} criterion rows must preserve the exact evaluator rubric")
    calculated_claimed = 0
    calculated_held = 0
    calculated_overclaim = 0
    first_by_name = {row["criterion"]: row for row in first_receipt["criteria"]}
    final_by_name = {row["criterion"]: row for row in final_receipt["criteria"]}
    for row_number, row in enumerate(rows, start=1):
        criterion = row["Criterion"]
        generator_claim = row["Generator first-pass claim"].upper()
        if generator_claim not in {"READY", "NOT READY"}:
            raise VerificationError(f"{artifact} row {row_number} has an invalid generator claim")
        first_row = first_by_name[criterion]
        final_row = final_by_name[criterion]
        if row["Evidence opened"] != "; ".join(first_row["evidence_opened"]):
            raise VerificationError(f"{artifact} row {row_number} evidence does not match first receipt")
        if row["Fresh evaluator first-pass verdict"].upper() != first_row["verdict"]:
            raise VerificationError(f"{artifact} row {row_number} first verdict does not match first receipt")
        if row["Final verdict"].upper() != final_row["verdict"]:
            raise VerificationError(f"{artifact} row {row_number} final verdict does not match final receipt")
        if generator_claim == "READY":
            calculated_claimed += 1
            if first_row["verdict"] == "HOLD":
                calculated_overclaim += 1
        if first_row["verdict"] == "HOLD":
            calculated_held += 1
            if criterion.casefold() not in trace_text.casefold() or first_row["finding"].casefold() not in trace_text.casefold():
                raise VerificationError(
                    f"Harness/RUN_TRACE.md must retain first-pass HOLD criterion and finding: {criterion}"
                )
        if final_row["verdict"] != "PASS":
            raise VerificationError(f"{artifact} final criterion remains HOLD: {criterion}")

    expected_generator = "READY" if calculated_claimed == len(rows) else "NOT READY"
    if generator_overall != expected_generator:
        raise VerificationError(f"{artifact} generator first-pass verdict does not match its rows")
    if (claimed, held, overclaimed) != (calculated_claimed, calculated_held, calculated_overclaim):
        raise VerificationError(f"{artifact} first-pass counts do not match its receipt-bound rows")
    if calculated_claimed == 0:
        raise VerificationError(f"{artifact} cannot release with zero first-pass READY claims")
    if ratio(overclaim_text, artifact) != (calculated_overclaim, calculated_claimed):
        raise VerificationError(f"{artifact} Overclaim does not match first-pass receipt evidence")
    return {
        "criteria": len(rows),
        "first_pass_claimed_ready": calculated_claimed,
        "first_pass_hold": calculated_held,
        "first_pass_overclaim": calculated_overclaim,
        "repair_cycles": repairs,
        "repair_scope": repair_scope,
        "final_candidate_receipt": final_candidate_path,
        "final_receipt": final_path,
    }


def verify_state(text: str, evaluation: Mapping[str, Any]) -> Dict[str, str]:
    artifact = "Harness/RUN_STATE.md"
    fields = {
        label: list_field(text, label, artifact)
        for label in (
            "Run ID",
            "Goal",
            "Phase",
            "Status",
            "Completed",
            "Open",
            "Next permitted action",
            "Terminal reason",
            "Artifact pointers",
        )
    }
    status = fields["Status"].upper()
    phase = fields["Phase"].upper()
    terminal_reason = fields["Terminal reason"].upper()
    if status not in {"COMPLETE", "HAND_BACK"}:
        raise VerificationError(f"{artifact} Status must be COMPLETE or HAND_BACK")
    if phase != "TERMINAL":
        raise VerificationError(f"{artifact} Phase must be TERMINAL at release")
    if terminal_reason not in ALLOWED_TERMINAL_REASONS:
        raise VerificationError(f"{artifact} has an unknown Terminal reason: {terminal_reason}")
    if terminal_reason == "SUCCESS" and status != "COMPLETE":
        raise VerificationError(f"{artifact} SUCCESS requires Status COMPLETE")
    if terminal_reason != "SUCCESS" and status != "HAND_BACK":
        raise VerificationError(f"{artifact} non-success terminal reasons require Status HAND_BACK")
    pointers = fields["Artifact pointers"].replace("\\", "/")
    required_pointers = list(OUTPUT_PATHS)
    if evaluation["final_candidate_receipt"] != "Harness/CANDIDATE_CHECK_FIRST.txt":
        required_pointers.append(evaluation["final_candidate_receipt"])
    if evaluation["final_receipt"] != "Harness/DIRECTOR_EVALUATOR_FIRST.json":
        required_pointers.append(evaluation["final_receipt"])
    missing = [path for path in required_pointers if path not in pointers]
    if missing:
        raise VerificationError(f"{artifact} lacks artifact pointers: {', '.join(missing)}")
    fields["Status"] = status
    fields["Phase"] = phase
    fields["Terminal reason"] = terminal_reason
    return fields


def verify_handoff(
    text: str,
    trace_text: str,
    state: Mapping[str, str],
    evaluation: Mapping[str, Any],
    resume: Mapping[str, Any],
) -> None:
    artifact = "Harness/HANDOFF_RECEIPT.md"
    fields = {
        label: list_field(text, label, artifact)
        for label in (
            "Handoff status",
            "Terminal reason",
            "Accepted artifacts",
            "Chosen pattern",
            "Human intervention count",
            "Repair cycles used",
            "Evaluator result",
            "Candidate verifier result",
            "Residual risk",
            "Reflection",
            "Workplace trial",
            "Trial owner",
            "Trial date",
            "Trial success signal",
            "Resume result",
            "Manifest status",
        )
    }
    if fields["Handoff status"].upper() != "COMPLETE":
        raise VerificationError(f"{artifact} Handoff status must be COMPLETE")
    if fields["Terminal reason"].upper() != state["Terminal reason"]:
        raise VerificationError(f"{artifact} terminal reason does not match RUN_STATE")
    if (
        fields["Evaluator result"].upper() != "PASS"
        or fields["Candidate verifier result"].upper() != "PASS"
    ):
        raise VerificationError(f"{artifact} evaluator and candidate verifier results must be PASS")
    if fields["Resume result"].upper() != resume["result"]:
        raise VerificationError(f"{artifact} resume result does not match RESUME_RECEIPT")
    if fields["Manifest status"].upper() != "PENDING":
        raise VerificationError(f"{artifact} Manifest status must remain PENDING before baseline write")
    try:
        interventions = int(fields["Human intervention count"])
        repairs = int(fields["Repair cycles used"])
    except ValueError as error:
        raise VerificationError(f"{artifact} intervention and repair counts must be integers") from error
    if interventions < 2 or repairs != evaluation["repair_cycles"]:
        raise VerificationError(f"{artifact} must retain both human gates and the exact repair count")
    pattern = fields["Chosen pattern"].casefold()
    if "fixed outer flow" not in pattern or "bounded adaptive retrieval" not in pattern:
        raise VerificationError(f"{artifact} must name the chosen fixed-loop/adaptive-retrieval pattern")
    accepted = fields["Accepted artifacts"].replace("\\", "/")
    expected = list(OUTPUT_PATHS)
    if evaluation["final_candidate_receipt"] != "Harness/CANDIDATE_CHECK_FIRST.txt":
        expected.append(evaluation["final_candidate_receipt"])
    if evaluation["final_receipt"] != "Harness/DIRECTOR_EVALUATOR_FIRST.json":
        expected.append(evaluation["final_receipt"])
    missing = [path for path in expected if path not in accepted]
    if missing:
        raise VerificationError(f"{artifact} lacks accepted artifacts: {', '.join(missing)}")
    if "handoff" not in trace_text.casefold():
        raise VerificationError("Harness/RUN_TRACE.md must record the scoped handoff action")


def verify_evidence_work(root: Path, contents: Mapping[str, str]) -> Dict[str, Any]:
    verify_skill(contents[".agents/skills/director-loop/SKILL.md"])
    verify_evaluator_config(contents[".codex/agents/director_evaluator.toml"])
    verify_personal_rules(contents["AGENTS.md"])
    verify_harness_card(contents["Harness/HARNESS_CARD.md"])
    evidence_paths, evidence_texts = verify_source_manifest(root)
    unprocessed = sorted(
        path for path in evidence_paths if path.startswith("00_Inbox/") and not path.startswith("00_Inbox/processed/")
    )
    if unprocessed:
        raise VerificationError("Inbox captures must be retained under 00_Inbox/processed: " + ", ".join(unprocessed))
    index = markdown_note_index(root)
    generated = verify_note_graph(root, index, evidence_paths)
    verify_trace_rows(contents["Harness/RUN_TRACE.md"])
    opened = verify_retrieval_ledger(
        contents["Harness/RUN_TRACE.md"], index, evidence_paths, evidence_texts
    )
    answer_citations, answer_claims, per_answer = verify_answers(
        contents, index, evidence_paths, opened
    )
    audit_rows, supported, adverse_claim_ids = verify_audit(
        contents["Audit.md"],
        answer_claims,
        index,
        evidence_paths,
        evidence_texts,
        opened,
    )
    brief_links = verify_brief(contents["Morning_Brief.md"], supported, index, evidence_paths)
    resume = verify_resume_receipt(
        root,
        contents["Harness/RESUME_RECEIPT.md"],
        contents["Harness/RUN_TRACE.md"],
        generated,
        evidence_paths,
        adverse_claim_ids,
    )
    return {
        "answer_citations": sum(answer_citations.values()),
        "answers": {path: len(set(links)) for path, links in per_answer.items()},
        "audit_rows": sum(audit_rows.values()),
        "brief_sources": len(set(brief_links)),
        "retrieval_opens": sum(path.startswith("Source_Packet/") for path in opened),
        "generated_notes": len(generated),
        "resume": resume,
    }


def verify_candidate_state(text: str, resume: Mapping[str, Any]) -> None:
    artifact = "Harness/RUN_STATE.md"
    fields = {
        label: list_field(text, label, artifact)
        for label in (
            "Run ID",
            "Goal",
            "Phase",
            "Status",
            "Completed",
            "Open",
            "Next permitted action",
            "Terminal reason",
            "Artifact pointers",
        )
    }
    if fields["Run ID"] != resume["resumed_run_id"]:
        raise VerificationError(f"{artifact} Run ID must match RESUME_RECEIPT Resumed run ID")
    if fields["Phase"].upper() != "AWAITING_CANDIDATE_CHECK":
        raise VerificationError(f"{artifact} Phase must be AWAITING_CANDIDATE_CHECK")
    if fields["Status"].upper() != "HAND_BACK":
        raise VerificationError(f"{artifact} candidate state must use Status HAND_BACK")
    if fields["Terminal reason"].upper() != "HUMAN_HAND_BACK":
        raise VerificationError(f"{artifact} candidate state must use HUMAN_HAND_BACK")
    next_action = fields["Next permitted action"].casefold()
    next_tokens = set(re.findall(r"[a-z]+", next_action))
    if "candidate" not in next_tokens or not ({"check", "verifier"} & next_tokens):
        raise VerificationError(f"{artifact} next action must be the trusted candidate verifier")
    pointers = fields["Artifact pointers"].replace("\\", "/")
    required = ANSWER_PATHS + (
        "Audit.md",
        "Morning_Brief.md",
        "Harness/RESUME_RECEIPT.md",
    )
    missing = [path for path in required if path not in pointers]
    if missing:
        raise VerificationError(f"{artifact} candidate state lacks artifact pointers: {', '.join(missing)}")


def verify_candidate(vault_root: Path) -> Dict[str, Any]:
    root = requested_root(vault_root)
    require_external_course_verifier(root)
    verify_trusted_contract_copies(root)
    contents = {relative: read_regular_text(root, relative) for relative in REQUIRED_CANDIDATE_ARTIFACTS}
    placeholder_paths = [
        path
        for path in REQUIRED_CANDIDATE_ARTIFACTS
        if path.endswith(".md") and path != ".agents/skills/director-loop/SKILL.md"
    ]
    verify_no_placeholders(contents, placeholder_paths)
    result = verify_evidence_work(root, contents)
    verify_candidate_state(contents["Harness/RUN_STATE.md"], result["resume"])
    result["root"] = root
    return result


def verify_vault(vault_root: Path) -> Dict[str, Any]:
    root = requested_root(vault_root)
    require_external_course_verifier(root)
    verify_trusted_contract_copies(root)
    contents = {relative: read_regular_text(root, relative) for relative in REQUIRED_FINAL_ARTIFACTS}
    placeholder_paths = [
        path
        for path in REQUIRED_FINAL_ARTIFACTS
        if path.endswith(".md") and path != ".agents/skills/director-loop/SKILL.md"
    ]
    verify_no_placeholders(contents, placeholder_paths)
    result = verify_evidence_work(root, contents)
    evaluation = verify_evaluation(root, contents["Harness/EVAL.md"], contents["Harness/RUN_TRACE.md"])
    state = verify_state(contents["Harness/RUN_STATE.md"], evaluation)
    if state["Run ID"] != result["resume"]["resumed_run_id"]:
        raise VerificationError("RUN_STATE Run ID must match RESUME_RECEIPT Resumed run ID")
    verify_trace_rows(contents["Harness/RUN_TRACE.md"], state["Terminal reason"])
    verify_handoff(
        contents["Harness/HANDOFF_RECEIPT.md"],
        contents["Harness/RUN_TRACE.md"],
        state,
        evaluation,
        result["resume"],
    )
    result.update({"root": root, "terminal_reason": state["Terminal reason"], "evaluation": evaluation})
    return result


def manifest_files(root: Path) -> List[Dict[str, Any]]:
    files: List[Dict[str, Any]] = []
    for current, directory_names, file_names in os.walk(str(root), followlinks=False):
        current_path = Path(current)
        safe_directories: List[str] = []
        for name in sorted(directory_names):
            path = current_path / name
            relative = path.relative_to(root)
            if name in SKIPPED_MANIFEST_DIRS:
                continue
            if path.is_symlink():
                raise VerificationError(f"Manifest refuses linked directory: {relative.as_posix()}")
            safe_directories.append(name)
        directory_names[:] = safe_directories
        for name in sorted(file_names):
            path = current_path / name
            relative = path.relative_to(root)
            relative_text = relative.as_posix()
            if PurePosixPath(relative_text) == MANIFEST_PATH or name.endswith((".pyc", ".tmp")):
                continue
            if path.is_symlink() or not path.is_file():
                raise VerificationError(f"Manifest refuses linked or irregular file: {relative_text}")
            files.append(
                {"path": relative_text, "bytes": path.stat().st_size, "sha256": sha256_file(path)}
            )
    return sorted(files, key=lambda item: item["path"])


def manifest_fingerprint(files: Sequence[Mapping[str, Any]]) -> str:
    payload = "\n".join(f"{item['path']}:{item['sha256']}" for item in files).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def candidate_fingerprint(root: Path) -> str:
    excluded_exact = {
        "Harness/BASELINE_MANIFEST.json",
        "Harness/EVAL.md",
        "Harness/HANDOFF_RECEIPT.md",
    }
    files = [
        item
        for item in manifest_files(root)
        if item["path"] not in excluded_exact
        and not item["path"].startswith("Harness/CANDIDATE_CHECK")
        and not item["path"].startswith("Harness/DIRECTOR_EVALUATOR_")
    ]
    return manifest_fingerprint(files)


def evaluated_content_fingerprint(root: Path) -> str:
    excluded_exact = {
        "Harness/BASELINE_MANIFEST.json",
        "Harness/EVAL.md",
        "Harness/HANDOFF_RECEIPT.md",
        "Harness/RUN_STATE.md",
        "Harness/RUN_TRACE.md",
    }
    files = [
        item
        for item in manifest_files(root)
        if item["path"] not in excluded_exact
        and not item["path"].startswith("Harness/CANDIDATE_CHECK")
        and not item["path"].startswith("Harness/DIRECTOR_EVALUATOR_")
    ]
    return manifest_fingerprint(files)


def state_identity_fingerprint(root: Path) -> str:
    text = read_regular_text(root, "Harness/RUN_STATE.md")
    run_id = list_field(text, "Run ID", "Harness/RUN_STATE.md")
    goal = list_field(text, "Goal", "Harness/RUN_STATE.md")
    return sha256_bytes((run_id + "\n" + goal).encode("utf-8"))


def candidate_control_metadata(root: Path) -> Tuple[str, int, str]:
    try:
        state_identity = state_identity_fingerprint(root)
    except (VerificationError, OSError, ValueError):
        state_identity = sha256_bytes(b"MISSING OR INVALID RUN_STATE")
    trace_path = root / "Harness" / "RUN_TRACE.md"
    if trace_path.is_symlink() or not trace_path.is_file():
        trace_data = b""
    else:
        trace_data = trace_path.read_bytes()
    return state_identity, len(trace_data), sha256_bytes(trace_data)


def write_manifest(root: Path, verification: Mapping[str, Any]) -> Path:
    resolved_root = requested_root(root)
    files = manifest_files(resolved_root)
    payload = {
        "schema_version": 1,
        "vault_root": ".",
        "root_fingerprint": manifest_fingerprint(files),
        "terminal_reason": verification["terminal_reason"],
        "verification": {
            "answer_citations": verification["answer_citations"],
            "audit_rows": verification["audit_rows"],
            "brief_sources": verification["brief_sources"],
            "retrieval_opens": verification["retrieval_opens"],
            "generated_notes": verification["generated_notes"],
            "evaluation": verification["evaluation"],
        },
        "files": files,
    }
    destination = resolved_root / MANIFEST_PATH
    temporary = destination.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(destination)
    return destination


def check_manifest(
    root: Path,
    manifest_path: Optional[Path] = None,
    require_external: bool = False,
) -> Dict[str, int]:
    resolved_root = requested_root(root)
    require_external_course_verifier(resolved_root)
    selected_candidate = (
        (resolved_root / MANIFEST_PATH)
        if manifest_path is None
        else manifest_path.expanduser().absolute()
    )
    if selected_candidate.is_symlink() or not selected_candidate.is_file():
        raise VerificationError(f"Baseline manifest is missing or linked: {selected_candidate}")
    selected = selected_candidate.resolve()
    if require_external:
        try:
            selected.relative_to(resolved_root)
        except ValueError:
            pass
        else:
            raise VerificationError("--check-manifest requires a manifest outside the candidate vault")
    try:
        payload = json.loads(selected.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationError(f"Invalid baseline manifest: {selected}") from error
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        raise VerificationError("Baseline manifest requires schema_version 1")
    recorded = payload.get("files")
    if not isinstance(recorded, list):
        raise VerificationError("Baseline manifest files must be an array")
    recorded_by_path: Dict[str, Mapping[str, Any]] = {}
    for item in recorded:
        if (
            not isinstance(item, dict)
            or set(item) != {"path", "bytes", "sha256"}
            or not isinstance(item["path"], str)
            or not isinstance(item["bytes"], int)
            or not isinstance(item["sha256"], str)
            or SHA256_RE.fullmatch(item["sha256"]) is None
        ):
            raise VerificationError("Baseline manifest contains a malformed file entry")
        if item["path"] in recorded_by_path:
            raise VerificationError(f"Baseline manifest repeats path {item['path']}")
        recorded_by_path[item["path"]] = item
    current = manifest_files(resolved_root)
    current_by_path = {item["path"]: item for item in current}
    added = sorted(set(current_by_path) - set(recorded_by_path))
    deleted = sorted(set(recorded_by_path) - set(current_by_path))
    changed = sorted(
        path
        for path in set(recorded_by_path) & set(current_by_path)
        if recorded_by_path[path] != current_by_path[path]
    )
    if added or deleted or changed:
        details: List[str] = []
        if changed:
            details.append("changed: " + ", ".join(changed))
        if added:
            details.append("added: " + ", ".join(added))
        if deleted:
            details.append("deleted: " + ", ".join(deleted))
        raise VerificationError("Baseline manifest drift — " + "; ".join(details))
    if payload.get("root_fingerprint") != manifest_fingerprint(current):
        raise VerificationError("Baseline manifest root_fingerprint does not match its files")
    return {"files": len(current), "changed": 0, "added": 0, "deleted": 0}


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vault_root", nargs="?", default=".")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument(
        "--candidate",
        action="store_true",
        help="check first-pass work before evaluator receipts, final state, and handoff exist",
    )
    modes.add_argument(
        "--write-manifest",
        action="store_true",
        help="write Harness/BASELINE_MANIFEST.json only after the full release passes",
    )
    modes.add_argument(
        "--check-manifest",
        metavar="MANIFEST_PATH",
        help="compare against an external frozen baseline without rewriting it",
    )
    args = parser.parse_args(argv)
    root = Path(args.vault_root)
    try:
        if args.candidate:
            result = verify_candidate(root)
            resolved = requested_root(root)
            fingerprint = candidate_fingerprint(resolved)
            content_fingerprint = evaluated_content_fingerprint(resolved)
            state_identity, trace_bytes, trace_hash = candidate_control_metadata(resolved)
            print(
                "PASS P4 candidate: "
                f"{result['answer_citations']} answer citations, "
                f"{result['audit_rows']} audit rows, "
                f"{result['retrieval_opens']} earned retrieval opens; "
                f"fingerprint {fingerprint}; content {content_fingerprint}"
                f"; stateid {state_identity}; trace {trace_bytes}:{trace_hash}"
            )
            return 0
        if args.check_manifest is not None:
            manifest_result = check_manifest(root, Path(args.check_manifest), require_external=True)
            result = verify_vault(root)
            print(
                f"PASS P4 baseline: {manifest_result['files']} files unchanged; "
                f"terminal {result['terminal_reason']}"
            )
            return 0
        result = verify_vault(root)
        manifest_path = write_manifest(root, result) if args.write_manifest else None
    except (VerificationError, OSError, ValueError) as error:
        suffix = ""
        if args.candidate:
            try:
                resolved = requested_root(root)
                state_identity, trace_bytes, trace_hash = candidate_control_metadata(resolved)
                suffix = (
                    f"; fingerprint {candidate_fingerprint(resolved)}; "
                    f"content {evaluated_content_fingerprint(resolved)}; "
                    f"stateid {state_identity}; trace {trace_bytes}:{trace_hash}"
                )
            except (VerificationError, OSError, ValueError):
                suffix = ""
        print(f"HOLD P4 vault: {error}{suffix}")
        return 1

    evaluation = result["evaluation"]
    print(
        "PASS P4 vault: "
        f"{result['answer_citations']} answer citations, "
        f"{result['audit_rows']} audit rows, "
        f"{result['brief_sources']} brief sources, "
        f"overclaim {evaluation['first_pass_overclaim']}/{evaluation['first_pass_claimed_ready']}, "
        f"terminal {result['terminal_reason']}"
    )
    if manifest_path is not None:
        print(f"WROTE {manifest_path.relative_to(requested_root(root)).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
