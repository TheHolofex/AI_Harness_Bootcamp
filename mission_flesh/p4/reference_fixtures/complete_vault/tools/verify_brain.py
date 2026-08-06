#!/usr/bin/env python3
"""Verify a completed P4 second-brain vault against the course contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

REQUIRED_ROOT = (
    "AGENTS.md",
    "MOC.md",
    "Mission_Brief.md",
    "Audit.md",
    "Retrieval/Answers.md",
    "Retrieval/Repair_Check.md",
    "Evidence/PERMISSIONS.json",
    "Evidence/MCP_RECEIPTS.jsonl",
    "Harness/HARNESS_CARD.md",
    "Harness/RUN_STATE.md",
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
ALLOWED_ROUTE_LEGS = {"la_origin", "rail", "road", "port", "sealift", "taiwan", "cross_cutting"}
ALLOWED_MODES = {"rail", "road", "port", "sealift", "air", "multimodal"}
ALLOWED_FACTORS = {"physical", "legal", "operational", "economic", "political", "protection"}
ALLOWED_THREAT_CLASSES = {"none", "protection", "interdiction_history", "chokepoint_context"}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}
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
MANIFEST_SOURCE_FIELDS = (
    "original_url",
    "publisher",
    "document_date",
    "retrieval_date",
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
DEFENSIVE_END_RE = re.compile(r"\b(protect|detect|recover)\b", re.I)
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
    except ImportError:
        yaml = None
    if yaml is not None:
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError as error:
            raise BrainError(f"Invalid YAML front matter: {error}") from error
        if not isinstance(data, dict):
            raise BrainError("YAML front matter must be a mapping")
        return data

    if "\t" in text:
        raise BrainError("YAML front matter must use spaces, not tabs")

    # Fallback: very small subset (key: value, lists with - )
    data: Dict[str, Any] = {}
    current_list: Optional[List[Any]] = None
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
                    if ":" not in nline:
                        raise BrainError(f"Unsupported YAML line: {nline}")
                    nk, _, nv = nline.partition(":")
                    obj[nk.strip()] = _parse_scalar(nv.strip())
                    j += 1
                current_list.append(obj)
                i = j
                continue
            current_list.append(_parse_scalar(item_text))
            i += 1
            continue
        if indent != 0:
            raise BrainError(f"Unexpected YAML indentation: {line}")
        if ":" not in line:
            raise BrainError(f"Unsupported YAML line: {line}")
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if key in data:
            raise BrainError(f"Duplicate YAML key: {key}")
        if val == "" or val == "|" or val == ">":
            current_list = []
            data[key] = current_list
        else:
            current_list = None
            data[key] = _parse_scalar(val)
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


def load_corpus_manifest(corpus_root: Path) -> Dict[str, Dict[str, Any]]:
    manifest_path = corpus_root / "MANIFEST.json"
    if not manifest_path.is_file() or manifest_path.is_symlink():
        raise BrainError(f"Corpus MANIFEST.json missing: {manifest_path}")
    try:
        rows = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise BrainError(f"Corpus MANIFEST.json invalid: {error.msg}") from error
    if not isinstance(rows, list):
        raise BrainError("Corpus MANIFEST.json must be a list")
    manifest: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("source_id"), str):
            raise BrainError("Corpus MANIFEST.json has an invalid row")
        source_id = row["source_id"]
        if source_id in manifest:
            raise BrainError(f"Corpus MANIFEST.json has duplicate source_id: {source_id}")
        manifest[source_id] = row
    return manifest


def validate_source(
    src: Mapping[str, Any],
    note_path: str,
    corpus_root: Path,
    manifest: Mapping[str, Mapping[str, Any]],
) -> None:
    for key in SOURCE_KEYS:
        if key not in src:
            raise BrainError(f"{note_path}: source missing key {key}")
    digest = str(src.get("sha256", ""))
    if not SHA256_RE.match(digest):
        raise BrainError(f"{note_path}: source sha256 invalid")
    for key in SOURCE_KEYS:
        if key == "contradictions":
            continue
        value = src.get(key)
        if not isinstance(value, str) or not value.strip():
            raise BrainError(f"{note_path}: source {key} must be a non-empty string")
    excerpt = str(src.get("excerpt", "")).strip()
    if len(excerpt) < 12:
        raise BrainError(f"{note_path}: source excerpt too short")
    confidence = str(src.get("confidence", "")).lower()
    if confidence not in ALLOWED_CONFIDENCE:
        raise BrainError(f"{note_path}: source confidence invalid: {confidence!r}")
    source_id = str(src["source_id"])
    row = manifest.get(source_id)
    if row is None:
        raise BrainError(f"{note_path}: source_id not found in MANIFEST: {source_id}")
    manifest_path = str(row.get("path", "")).replace("\\", "/").lstrip("./")
    raw_path = str(src["raw_path"]).replace("\\", "/").lstrip("./")
    allowed_paths = {
        manifest_path,
        f"raw_corpus/{manifest_path}",
        f"mission_flesh/p4/raw_corpus/{manifest_path}",
    }
    if raw_path not in allowed_paths:
        raise BrainError(f"{note_path}: raw_path does not match MANIFEST for {source_id}")
    manifest_digest = str(row.get("sha256", ""))
    if digest != manifest_digest:
        raise BrainError(f"{note_path}: source sha256 does not match MANIFEST for {source_id}")
    for key in MANIFEST_SOURCE_FIELDS:
        if str(src.get(key, "")) != str(row.get(key, "")):
            raise BrainError(f"{note_path}: source {key} does not match MANIFEST for {source_id}")
    source_file = corpus_root / manifest_path
    if not source_file.is_file() or source_file.is_symlink():
        raise BrainError(f"{note_path}: corpus source file missing for {source_id}")
    actual_digest = hashlib.sha256(source_file.read_bytes()).hexdigest()
    if actual_digest != manifest_digest:
        raise BrainError(f"{note_path}: corpus file sha256 does not match MANIFEST for {source_id}")


def validate_string_list(
    meta: Mapping[str, Any], key: str, allowed: Set[str], note_path: str
) -> List[str]:
    values = meta.get(key)
    if not isinstance(values, list) or not values:
        raise BrainError(f"{note_path}: {key} must be a non-empty list")
    normalized = [str(value) for value in values]
    invalid = sorted(set(normalized) - allowed)
    if invalid:
        raise BrainError(f"{note_path}: invalid {key}: {invalid}")
    return normalized


def validate_note(
    path: Path,
    root: Path,
    corpus_root: Path,
    manifest: Mapping[str, Mapping[str, Any]],
) -> Dict[str, Any]:
    rel = path.relative_to(root).as_posix()
    text = path.read_text(encoding="utf-8")
    meta, body = split_front_matter(text)
    for key in NOTE_KEYS:
        if key not in meta:
            raise BrainError(f"{rel}: missing front matter key {key}")
    for key in ("note_id", "title"):
        value = meta.get(key)
        if not isinstance(value, str) or not value.strip():
            raise BrainError(f"{rel}: {key} must be a non-empty string")
    validate_string_list(meta, "route_legs", ALLOWED_ROUTE_LEGS, rel)
    validate_string_list(meta, "modes", ALLOWED_MODES, rel)
    validate_string_list(meta, "factors", ALLOWED_FACTORS, rel)
    threat = str(meta.get("threat_class", "")).lower()
    if threat not in ALLOWED_THREAT_CLASSES:
        raise BrainError(f"{rel}: invalid threat_class: {threat!r}")
    confidence = str(meta.get("confidence", "")).lower()
    if confidence not in ALLOWED_CONFIDENCE:
        raise BrainError(f"{rel}: invalid confidence: {confidence!r}")
    sources = meta.get("sources")
    if not isinstance(sources, list) or not sources:
        raise BrainError(f"{rel}: sources must be a non-empty list")
    for src in sources:
        if not isinstance(src, dict):
            raise BrainError(f"{rel}: each source must be a mapping")
        validate_source(src, rel, corpus_root, manifest)
    if not wikilinks(body) and not wikilinks(text):
        raise BrainError(f"{rel}: body must include at least one wikilink")
    if FORBIDDEN_RE.search(body):
        raise BrainError(f"{rel}: forbidden offensive tradecraft language")
    if threat != "none" and not DEFENSIVE_RE.search(body):
        raise BrainError(f"{rel}: threat note must include defensive implications language")
    if threat != "none" and not DEFENSIVE_END_RE.search(body.rstrip()[-500:]):
        raise BrainError(f"{rel}: threat note must end in protect/detect/recover implications")
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
    retriever = data.get("retriever") or data.get("agents", {}).get("retriever")
    if not isinstance(director, dict):
        raise BrainError("PERMISSIONS.json missing director block")
    mcp = director.get("mcp") or {}
    if not isinstance(mcp, dict):
        raise BrainError("director MCP policy must be an object")
    if str(mcp.get("read", "")).lower() != "allow":
        raise BrainError("director MCP read policy must be allow")
    write_policy = str(mcp.get("write") or mcp.get("write_policy") or "").lower()
    if write_policy not in {"ask", "approve", "ask-for-approval"}:
        raise BrainError("director MCP write policy must be ask/approve")
    for key in ("delete", "move", "copy", "active_file", "command"):
        if str(mcp.get(key, "")).lower() != "deny":
            raise BrainError(f"director MCP {key} policy must be deny")
    if str(director.get("filesystem_vault", "")).lower() != "deny":
        raise BrainError("director filesystem_vault policy must be deny")
    if str(director.get("web", "")).lower() != "deny":
        raise BrainError("director web policy must be deny")
    if researchers is None:
        raise BrainError("PERMISSIONS.json missing researchers block")
    if not isinstance(researchers, dict):
        raise BrainError("PERMISSIONS.json researchers block must be an object")
    if str(researchers.get("mcp", "")).lower() != "deny":
        raise BrainError("researchers MCP policy must be deny")
    if str(researchers.get("web", "")).lower() != "deny":
        raise BrainError("researchers web policy must be deny")
    if str(researchers.get("filesystem_write", "")).lower() != "deny":
        raise BrainError("researchers filesystem_write policy must be deny")
    if str(researchers.get("raw_corpus", "")).lower() != "read":
        raise BrainError("researchers raw_corpus policy must be read")
    if not isinstance(retriever, dict):
        raise BrainError("PERMISSIONS.json missing retriever block")
    if str(retriever.get("project", "")).replace("/", "\\").lower() != (
        "documents\\p4-cold-query"
    ):
        raise BrainError("retriever project must be Documents\\p4-cold-query")
    retriever_mcp = retriever.get("mcp") or {}
    if not isinstance(retriever_mcp, dict):
        raise BrainError("retriever MCP policy must be an object")
    if str(retriever_mcp.get("read", "")).lower() != "allow":
        raise BrainError("retriever MCP read policy must be allow")
    if str(retriever_mcp.get("write", "")).lower() != "ask":
        raise BrainError("retriever MCP write policy must be ask")
    if str(retriever.get("filesystem", "")).lower() != "deny":
        raise BrainError("retriever filesystem policy must be deny")
    if str(retriever.get("web", "")).lower() != "deny":
        raise BrainError("retriever web policy must be deny")


def validate_mcp_receipts(root: Path) -> Dict[str, Any]:
    path = require_file(root, "Evidence/MCP_RECEIPTS.jsonl")
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines:
        raise BrainError("MCP_RECEIPTS.jsonl is empty")
    writes = 0
    director_paths: Set[str] = set()
    retriever_paths: Set[str] = set()
    for idx, line in enumerate(lines, start=1):
        try:
            event = json.loads(line)
        except json.JSONDecodeError as error:
            raise BrainError(f"MCP_RECEIPTS.jsonl line {idx}: {error.msg}") from error
        if not isinstance(event, dict):
            raise BrainError(f"MCP_RECEIPTS.jsonl line {idx}: not an object")
        required = {"ts", "agent", "tool", "action", "path", "ok"}
        missing = sorted(required - set(event))
        if missing:
            raise BrainError(f"MCP_RECEIPTS.jsonl line {idx}: missing keys {missing}")
        for key in ("ts", "agent", "tool", "action", "path"):
            if not isinstance(event.get(key), str) or not str(event.get(key)).strip():
                raise BrainError(
                    f"MCP_RECEIPTS.jsonl line {idx}: {key} must be a non-empty string"
                )
        if not isinstance(event.get("ok"), bool):
            raise BrainError(f"MCP_RECEIPTS.jsonl line {idx}: ok must be true or false")
        raw_receipt_path = str(event["path"])
        posix_path = PurePosixPath(raw_receipt_path.replace("\\", "/"))
        windows_path = PureWindowsPath(raw_receipt_path)
        if (
            posix_path.is_absolute()
            or windows_path.is_absolute()
            or bool(windows_path.drive)
            or bool(windows_path.root)
            or ".." in posix_path.parts
            or ".." in windows_path.parts
        ):
            raise BrainError(f"MCP_RECEIPTS.jsonl line {idx}: path must stay inside the vault")
        receipt_path = posix_path.as_posix()
        tool = str(event.get("tool") or event.get("name") or event.get("method") or "").lower()
        action = str(event.get("action") or event.get("op") or "").lower()
        is_write = action in {"write", "append", "patch", "create", "put"}
        is_obsidian_tool = "obsidian" in tool and any(
            token in tool for token in ("write", "append", "patch")
        )
        agent = str(event.get("agent", "")).lower()
        if event.get("ok") is True and is_write and is_obsidian_tool:
            writes += 1
            if agent == "director":
                director_paths.add(receipt_path)
            elif agent == "retriever":
                retriever_paths.add(receipt_path)
    if not director_paths:
        raise BrainError("MCP_RECEIPTS.jsonl needs at least one write/append/patch event")
    required_director = {"Audit.md", "MOC.md"}
    missing_director = sorted(required_director - director_paths)
    if missing_director:
        raise BrainError(
            "MCP_RECEIPTS.jsonl missing director MCP write receipts: "
            + ", ".join(missing_director)
        )
    required_retriever = {
        "Harness/RUN_STATE.md",
        "Mission_Brief.md",
        "Retrieval/Answers.md",
        "Retrieval/Repair_Check.md",
    }
    missing_retriever = sorted(required_retriever - retriever_paths)
    if missing_retriever:
        raise BrainError(
            "MCP_RECEIPTS.jsonl missing retriever MCP write receipts: "
            + ", ".join(missing_retriever)
        )
    return {
        "write_count": writes,
        "director_paths": director_paths,
        "retriever_paths": retriever_paths,
    }


def resolve_wikilink(root: Path, target: str) -> Optional[Path]:
    normalized = target.strip().replace("\\", "/").strip("/")
    if not normalized or ".." in Path(normalized).parts:
        return None
    direct = root / normalized
    candidates = [direct] if direct.suffix == ".md" else [direct.with_suffix(".md"), direct]
    for candidate in candidates:
        if candidate.is_file() and not candidate.is_symlink():
            try:
                candidate.resolve().relative_to(root)
            except ValueError:
                return None
            return candidate
    if "/" not in normalized:
        matches = [
            path
            for path in root.rglob(f"{normalized}.md")
            if path.is_file() and not path.is_symlink()
        ]
        if len(matches) == 1:
            return matches[0]
    return None


def validate_wikilinks(root: Path, relative: str, minimum: int = 1) -> List[str]:
    text = read_text(root, relative)
    links = wikilinks(text)
    if len(links) < minimum:
        raise BrainError(f"{relative} needs at least {minimum} wikilinks")
    for target in links:
        if resolve_wikilink(root, target) is None:
            raise BrainError(f"{relative}: unresolved wikilink {target!r}")
    return links


def required_labeled_field(text: str, artifact: str, label: str) -> str:
    pattern = re.compile(
        rf"^[ \t]*(?:[-*+][ \t]+)?{re.escape(label)}[ \t]*:[ \t]*(.*?)[ \t]*$",
        re.I | re.M,
    )
    matches = pattern.findall(text)
    if not matches:
        raise BrainError(f"{artifact} missing {label}:")
    if len(matches) != 1:
        raise BrainError(f"{artifact} must contain exactly one {label}: field")
    value = matches[0].strip()
    if not value:
        raise BrainError(f"{artifact} field {label} must be non-empty")
    return value


def resolve_repaired_path(root: Path, artifact: str, value: str) -> Path:
    candidate = value.strip()
    inline_code = re.fullmatch(r"`([^`]+)`", candidate)
    wikilink = re.fullmatch(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]", candidate)
    if inline_code:
        candidate = inline_code.group(1).strip()
    elif wikilink:
        candidate = wikilink.group(1).strip()
    resolved = resolve_wikilink(root, candidate)
    if resolved is None or resolved.suffix.lower() != ".md":
        raise BrainError(
            f"{artifact} Repaired path does not resolve to a vault note: {value!r}"
        )
    return resolved.resolve()


def validate_retrieval(root: Path) -> None:
    text = read_text(root, "Retrieval/Answers.md")
    for label in ("Q1", "Q2", "Q3", "Q4"):
        if label not in text:
            raise BrainError(f"Retrieval/Answers.md missing {label}")
    validate_wikilinks(root, "Retrieval/Answers.md", 4)


def validate_repair_proof(root: Path, director_receipt_paths: Set[str]) -> None:
    audit_artifact = "Audit.md"
    audit = read_text(root, audit_artifact)
    if not re.search(r"\b(support|accept)\b", audit, re.I):
        raise BrainError("Audit.md must record at least one supported finding")
    audit_path = resolve_repaired_path(
        root,
        audit_artifact,
        required_labeled_field(audit, audit_artifact, "Repaired path"),
    )
    audit_before = required_labeled_field(audit, audit_artifact, "Before")
    audit_after = required_labeled_field(audit, audit_artifact, "After")
    required_labeled_field(audit, audit_artifact, "Expected retrieval effect")
    if audit_before == audit_after:
        raise BrainError("Audit.md Before and After must describe different states")

    repair_artifact = "Retrieval/Repair_Check.md"
    repair = read_text(root, "Retrieval/Repair_Check.md")
    repair_path = resolve_repaired_path(
        root,
        repair_artifact,
        required_labeled_field(repair, repair_artifact, "Repaired path"),
    )
    repair_before = required_labeled_field(repair, repair_artifact, "Before")
    repair_after = required_labeled_field(repair, repair_artifact, "After")
    verdict = required_labeled_field(repair, repair_artifact, "Verdict")
    if verdict.upper() != "PASS":
        raise BrainError("Retrieval/Repair_Check.md missing Verdict: PASS")
    if repair_before == repair_after:
        raise BrainError(
            "Retrieval/Repair_Check.md Before and After must describe different states"
        )
    if audit_path != repair_path:
        raise BrainError(
            "Retrieval/Repair_Check.md repaired path must match Audit.md"
        )
    repaired_relative = repair_path.relative_to(root).as_posix()
    if repaired_relative not in director_receipt_paths:
        raise BrainError(
            "Audit.md applied repair needs a director MCP write receipt: "
            + repaired_relative
        )

    links = validate_wikilinks(root, repair_artifact, 2)
    linked_paths = {
        linked.resolve()
        for target in links
        if (linked := resolve_wikilink(root, target)) is not None
    }
    if repair_path not in linked_paths:
        relative = repair_path.relative_to(root).as_posix()
        raise BrainError(
            f"Retrieval/Repair_Check.md must wikilink the repaired path: {relative}"
        )


def validate_brief_and_audit(root: Path) -> None:
    validate_wikilinks(root, "Mission_Brief.md", 3)


def validate_navigation(root: Path) -> None:
    links = {
        target[:-3] if target.lower().endswith(".md") else target
        for target in validate_wikilinks(root, "MOC.md", 6)
    }
    required = {
        "Notes/Modes",
        "Notes/Nodes",
        "Notes/Constraints",
        "Notes/Threats",
        "Notes/Sources",
        "Notes/Route/Spine",
    }
    missing = sorted(required - links)
    if missing:
        raise BrainError(f"MOC.md missing required hub wikilinks: {missing}")
    for relative in (
        "Notes/Modes.md",
        "Notes/Nodes.md",
        "Notes/Constraints.md",
        "Notes/Threats.md",
        "Notes/Route/Spine.md",
    ):
        validate_wikilinks(root, relative)


def validate_harness_ready(root: Path) -> None:
    card = read_text(root, "Harness/HARNESS_CARD.md")
    if not re.search(r"\bMCP\b", card) or not re.search(r"\bdirector\b", card, re.I):
        raise BrainError("HARNESS_CARD.md must record the director MCP write boundary")
    state = read_text(root, "Harness/RUN_STATE.md")
    if not re.search(r"^\s*-?\s*Phase:\s*READY_FOR_VERIFY\s*$", state, re.I | re.M):
        raise BrainError("RUN_STATE.md must record Phase READY_FOR_VERIFY")
    if not re.search(r"^\s*-?\s*Status:\s*READY\s*$", state, re.I | re.M):
        raise BrainError("RUN_STATE.md must record Status READY")
    if not re.search(r"Next permitted action:.*course verifier", state, re.I):
        raise BrainError("RUN_STATE.md must send the next action to the course verifier")


def verify_brain(root: Path, corpus_root: Optional[Path] = None) -> Dict[str, Any]:
    resolved = requested_root(root)
    corpus = (
        corpus_root.expanduser().resolve()
        if corpus_root is not None
        else Path(__file__).resolve().parents[2] / "raw_corpus"
    )
    manifest = load_corpus_manifest(corpus)
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
        meta = validate_note(path, resolved, corpus, manifest)
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
    receipt_summary = validate_mcp_receipts(resolved)
    validate_retrieval(resolved)
    validate_repair_proof(resolved, receipt_summary["director_paths"])
    validate_brief_and_audit(resolved)
    validate_navigation(resolved)
    validate_harness_ready(resolved)

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
        "mcp_write_events": receipt_summary["write_count"],
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vault_root", nargs="?", default=".")
    parser.add_argument(
        "--corpus-root",
        help="raw_corpus path (defaults to the course P4 raw_corpus beside this verifier)",
    )
    args = parser.parse_args(argv)
    try:
        corpus_root = Path(args.corpus_root) if args.corpus_root else None
        result = verify_brain(Path(args.vault_root), corpus_root)
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
