#!/usr/bin/env python3
"""Verify a completed P4 second-brain vault against the course contract."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

REQUIRED_ROOT = (
    "AGENTS.md",
    "MOC.md",
    "Mission_Brief.md",
    "Audit.md",
    "Retrieval/Answers.md",
    "Evidence/PERMISSIONS.json",
    "Evidence/MCP_RECEIPTS.jsonl",
    "Harness/HARNESS_CARD.md",
    "Harness/RUN_STATE.md",
    "Harness/HANDOFF_RECEIPT.md",
    "Notes/Modes.md",
    "Notes/Nodes.md",
    "Notes/Constraints.md",
    "Notes/Threats.md",
    "Notes/Sources.md",
    "Notes/Route/Spine.md",
    "tools/verify_brain.py",
    "tools/verify_baseline.py",
    "tools/verify_vault.py",
)

HUB_NAMES = {"Modes", "Nodes", "Constraints", "Threats", "Sources", "Spine", "MOC"}
CONTENT_NOTE_MIN = 8
REQUIRED_MODES = {"rail", "road", "port", "sealift"}
REQUIRED_FACTORS = {"physical", "legal", "operational", "protection"}
ROUTE_GROUPS = (
    {"la_origin", "rail"},
    {"port", "sealift"},
    {"taiwan", "cross_cutting"},
)
SOURCE_KEYS = (
    "source_id",
    "raw_path",
    "sha256",
    "original_url",
    "publisher",
    "document_date",
    "retrieval_date",
    "locator",
    "excerpt",
    "claim",
    "confidence",
    "uncertainty",
    "contradictions",
)
NOTE_KEYS = (
    "note_id",
    "title",
    "route_legs",
    "modes",
    "factors",
    "threat_class",
    "confidence",
    "sources",
)
WIKILINK_RE = re.compile(r"(?<!!)\[\[([^\]\|#]+)")
FRONT_MATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
DEFENSIVE_RE = re.compile(r"\b(protect|harden|redundant|monitor|detect|recover|surveillance|escort)\b", re.I)
FORBIDDEN_RE = re.compile(
    r"\b(how to sabotage|step[- ]by[- ]step attack|target ranking|access method to destroy)\b",
    re.I,
)


class BrainError(RuntimeError):
    """Raised when the vault fails the second-brain contract."""


def requested_root(path: Path) -> Path:
    candidate = path.expanduser().absolute()
    if candidate.is_symlink() or not candidate.is_dir():
        raise BrainError(f"Vault root must be a regular directory: {candidate}")
    return candidate.resolve()


def require_file(root: Path, relative: str) -> Path:
    path = root / relative
    if path.is_symlink() or not path.is_file():
        raise BrainError(f"Missing required artifact: {relative}")
    return path


def read_text(root: Path, relative: str) -> str:
    path = require_file(root, relative)
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise BrainError(f"Required artifact is empty: {relative}")
    return text


def parse_simple_yaml(text: str) -> Dict[str, Any]:
    """Minimal YAML subset parser for note front matter."""
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text)
        if isinstance(data, dict):
            return data
    except Exception:
        pass

    # Fallback: very small subset (key: value, lists with - )
    data: Dict[str, Any] = {}
    current_list_key: Optional[str] = None
    current_list: Optional[List[Any]] = None
    obj_stack: List[Dict[str, Any]] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        if not raw.strip() or raw.strip().startswith("#"):
            i += 1
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if line.startswith("- "):
            item_text = line[2:].strip()
            if current_list is None:
                raise BrainError("List item without key in front matter")
            if ":" in item_text and not item_text.startswith("{"):
                # start of nested mapping in list
                key, _, val = item_text.partition(":")
                obj: Dict[str, Any] = {key.strip(): _parse_scalar(val.strip())}
                # consume deeper indented key lines
                j = i + 1
                while j < len(lines):
                    nxt = lines[j]
                    if not nxt.strip():
                        j += 1
                        continue
                    nindent = len(nxt) - len(nxt.lstrip(" "))
                    if nindent <= indent:
                        break
                    nline = nxt.strip()
                    if nline.startswith("- "):
                        break
                    if ":" in nline:
                        nk, _, nv = nline.partition(":")
                        obj[nk.strip()] = _parse_scalar(nv.strip())
                    j += 1
                current_list.append(obj)
                i = j
                continue
            current_list.append(_parse_scalar(item_text))
            i += 1
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if val == "" or val == "|" or val == ">":
                # list or nested follows
                current_list_key = key
                current_list = []
                data[key] = current_list
            else:
                current_list_key = None
                current_list = None
                data[key] = _parse_scalar(val)
            i += 1
            continue
        i += 1
    return data


def _parse_scalar(value: str) -> Any:
    if value == "" or value == "null" or value == "~":
        return None
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(part.strip()) for part in inner.split(",")]
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    try:
        return int(value)
    except ValueError:
        pass
    return value


def split_front_matter(text: str) -> Tuple[Dict[str, Any], str]:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        raise BrainError("Content note missing YAML front matter")
    meta = parse_simple_yaml(match.group(1))
    body = text[match.end() :]
    return meta, body


def wikilinks(text: str) -> List[str]:
    return [m.group(1).strip() for m in WIKILINK_RE.finditer(text)]


def content_note_paths(root: Path) -> List[Path]:
    notes_root = root / "Notes"
    if not notes_root.is_dir():
        raise BrainError("Notes/ directory missing")
    paths: List[Path] = []
    for path in sorted(notes_root.rglob("*.md")):
        if path.is_symlink() or not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if rel in {
            "Notes/Modes.md",
            "Notes/Nodes.md",
            "Notes/Constraints.md",
            "Notes/Threats.md",
            "Notes/Sources.md",
            "Notes/Route/Spine.md",
        }:
            continue
        paths.append(path)
    return paths


def validate_source(src: Mapping[str, Any], note_path: str) -> None:
    for key in SOURCE_KEYS:
        if key not in src:
            raise BrainError(f"{note_path}: source missing key {key}")
    digest = str(src.get("sha256", ""))
    if not SHA256_RE.match(digest):
        raise BrainError(f"{note_path}: source sha256 invalid")
    excerpt = str(src.get("excerpt", "")).strip()
    claim = str(src.get("claim", "")).strip()
    raw_path = str(src.get("raw_path", "")).strip()
    if not excerpt or not claim or not raw_path:
        raise BrainError(f"{note_path}: source requires excerpt, claim, and raw_path")
    if len(excerpt) < 12:
        raise BrainError(f"{note_path}: source excerpt too short")


def validate_note(path: Path, root: Path) -> Dict[str, Any]:
    rel = path.relative_to(root).as_posix()
    text = path.read_text(encoding="utf-8")
    meta, body = split_front_matter(text)
    for key in NOTE_KEYS:
        if key not in meta:
            raise BrainError(f"{rel}: missing front matter key {key}")
    sources = meta.get("sources")
    if not isinstance(sources, list) or not sources:
        raise BrainError(f"{rel}: sources must be a non-empty list")
    for src in sources:
        if not isinstance(src, dict):
            raise BrainError(f"{rel}: each source must be a mapping")
        validate_source(src, rel)
    if not wikilinks(body) and not wikilinks(text):
        raise BrainError(f"{rel}: body must include at least one wikilink")
    if FORBIDDEN_RE.search(body):
        raise BrainError(f"{rel}: forbidden offensive tradecraft language")
    threat = str(meta.get("threat_class", "none"))
    if threat != "none" and not DEFENSIVE_RE.search(body):
        raise BrainError(f"{rel}: threat note must include defensive implications language")
    return meta


def validate_permissions(root: Path) -> None:
    raw = read_text(root, "Evidence/PERMISSIONS.json")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as error:
        raise BrainError(f"PERMISSIONS.json invalid: {error.msg}") from error
    if not isinstance(data, dict):
        raise BrainError("PERMISSIONS.json must be an object")
    director = data.get("director") or data.get("agents", {}).get("director")
    researchers = data.get("researchers") or data.get("agents", {}).get("researchers")
    if not isinstance(director, dict):
        raise BrainError("PERMISSIONS.json missing director block")
    mcp = director.get("mcp") or {}
    write_policy = str(mcp.get("write") or mcp.get("write_policy") or "").lower()
    if write_policy not in {"ask", "approve", "ask-for-approval"}:
        raise BrainError("director MCP write policy must be ask/approve")
    if researchers is None:
        raise BrainError("PERMISSIONS.json missing researchers block")
    # researchers may be list or dict
    blob = json.dumps(researchers).lower()
    if "deny" not in blob and '"mcp": false' not in blob and "mcp_deny" not in blob:
        # accept explicit mcp: "deny"
        if '"mcp": "off"' not in blob and "no_mcp" not in blob:
            raise BrainError("researchers must deny MCP (record mcp deny/false/off)")


def validate_mcp_receipts(root: Path) -> int:
    path = require_file(root, "Evidence/MCP_RECEIPTS.jsonl")
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        raise BrainError("MCP_RECEIPTS.jsonl is empty")
    writes = 0
    for idx, line in enumerate(lines, start=1):
        try:
            event = json.loads(line)
        except json.JSONDecodeError as error:
            raise BrainError(f"MCP_RECEIPTS.jsonl line {idx}: {error.msg}") from error
        if not isinstance(event, dict):
            raise BrainError(f"MCP_RECEIPTS.jsonl line {idx}: not an object")
        tool = str(event.get("tool") or event.get("name") or event.get("method") or "").lower()
        action = str(event.get("action") or event.get("op") or "").lower()
        if any(token in tool or token in action for token in ("write", "append", "patch", "create", "put")):
            writes += 1
    if writes < 1:
        raise BrainError("MCP_RECEIPTS.jsonl needs at least one write/append/patch event")
    return writes


def validate_retrieval(root: Path) -> None:
    text = read_text(root, "Retrieval/Answers.md")
    for label in ("Q1", "Q2", "Q3", "Q4"):
        if label not in text:
            raise BrainError(f"Retrieval/Answers.md missing {label}")
    links = wikilinks(text)
    if len(links) < 4:
        raise BrainError("Retrieval/Answers.md needs wikilinks into the brain (min 4)")


def validate_brief_and_audit(root: Path) -> None:
    brief = read_text(root, "Mission_Brief.md")
    links = wikilinks(brief)
    if len(links) < 3:
        raise BrainError("Mission_Brief.md must wikilink at least three vault notes")
    audit = read_text(root, "Audit.md")
    if not re.search(r"\b(support|partial|not supported|reject|accept|repair)\b", audit, re.I):
        raise BrainError("Audit.md must record at least one disposition")


def verify_brain(root: Path) -> Dict[str, Any]:
    resolved = requested_root(root)
    for relative in REQUIRED_ROOT:
        require_file(resolved, relative)

    notes = content_note_paths(resolved)
    if len(notes) < CONTENT_NOTE_MIN:
        raise BrainError(f"Need at least {CONTENT_NOTE_MIN} content notes, found {len(notes)}")

    metas: List[Dict[str, Any]] = []
    note_ids: Set[str] = set()
    modes: Set[str] = set()
    factors: Set[str] = set()
    legs: Set[str] = set()
    threat_notes = 0
    for path in notes:
        meta = validate_note(path, resolved)
        nid = str(meta.get("note_id"))
        if nid in note_ids:
            raise BrainError(f"Duplicate note_id: {nid}")
        note_ids.add(nid)
        for item in meta.get("modes") or []:
            modes.add(str(item))
        for item in meta.get("factors") or []:
            factors.add(str(item))
        for item in meta.get("route_legs") or []:
            legs.add(str(item))
        if str(meta.get("threat_class", "none")) != "none":
            threat_notes += 1
        metas.append(meta)

    missing_modes = REQUIRED_MODES - modes
    if missing_modes:
        raise BrainError(f"Missing required modes across notes: {sorted(missing_modes)}")
    missing_factors = REQUIRED_FACTORS - factors
    if missing_factors:
        raise BrainError(f"Missing required factors across notes: {sorted(missing_factors)}")
    for group in ROUTE_GROUPS:
        if not (legs & group):
            raise BrainError(f"Missing route coverage for group {sorted(group)}")
    if threat_notes < 1:
        raise BrainError("Need at least one defensive threat/protection note")

    validate_permissions(resolved)
    write_events = validate_mcp_receipts(resolved)
    validate_retrieval(resolved)
    validate_brief_and_audit(resolved)

    # Hubs should not be empty stubs
    for hub in (
        "Notes/Modes.md",
        "Notes/Nodes.md",
        "Notes/Constraints.md",
        "Notes/Threats.md",
        "Notes/Sources.md",
        "Notes/Route/Spine.md",
        "MOC.md",
    ):
        text = read_text(resolved, hub)
        if len(text.strip()) < 40:
            raise BrainError(f"{hub} is too thin")

    return {
        "content_notes": len(notes),
        "modes": sorted(modes),
        "factors": sorted(factors),
        "route_legs": sorted(legs),
        "threat_notes": threat_notes,
        "mcp_write_events": write_events,
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vault_root", nargs="?", default=".")
    args = parser.parse_args(argv)
    try:
        result = verify_brain(Path(args.vault_root))
        print(
            "PASS brain: "
            f"{result['content_notes']} notes; "
            f"modes={','.join(result['modes'])}; "
            f"threat_notes={result['threat_notes']}; "
            f"mcp_writes={result['mcp_write_events']}"
        )
        return 0
    except BrainError as error:
        print(f"HOLD brain: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
