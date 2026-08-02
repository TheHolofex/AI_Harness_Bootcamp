#!/usr/bin/env python3
"""Bounded Stop hook for the P2 daily-brief release contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any


CONFIG_NAME = "P2_CONTROL_PLANE.json"
GATE_NAME = "p2-release-control"
FALLBACK_RECEIPT = "out/QUALITY_GATE_RECEIPT.json"
SOURCE_MANIFEST = "inputs/p1/SOURCE_MANIFEST.md"

MANDATORY_EVIDENCE = (
    SOURCE_MANIFEST,
    "inputs/p1/AUDIT.md",
    "inputs/p1/RELEASE_RECORD.md",
    "out/PLUGIN_REVIEW.md",
    "out/EVIDENCE_MAP.md",
    "out/CONFIG_EVIDENCE.md",
    "out/DECISION_REVIEW.md",
    "out/RUN_RECEIPT.md",
)
MANDATORY_SECRET_PATTERNS = (
    r"sk-[A-Za-z0-9_-]{16,}",
    r"xai-[A-Za-z0-9_-]{16,}",
)
CANONICAL_CITATION_RE = re.compile(r"\[(C[1-9][0-9]*)\]", flags=re.IGNORECASE)
MANIFEST_ID_RE = re.compile(r"(?<![A-Za-z0-9_])(C[1-9][0-9]*)(?![A-Za-z0-9_])", flags=re.IGNORECASE)


def emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, separators=(",", ":")))


def redact_secret_text(text: str) -> str:
    redacted = text
    for pattern in MANDATORY_SECRET_PATTERNS:
        redacted = re.sub(pattern, "[REDACTED KEY]", redacted, flags=re.IGNORECASE)
    return redacted


def hold(event: dict[str, Any], reason: str) -> None:
    safe_reason = redact_secret_text(reason)
    if event.get("stop_hook_active") is True:
        emit(
            {
                "systemMessage": safe_reason
                + " The one automatic repair pass is spent; leave the release on HOLD and ask the operator what to do."
            }
        )
    else:
        emit({"decision": "block", "reason": safe_reason})


def checked_at() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_relative_path(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty relative path")
    if "\x00" in value:
        raise ValueError(f"{label} contains a null byte")

    posix = PurePosixPath(value)
    windows = PureWindowsPath(value)
    if posix.is_absolute() or windows.anchor:
        raise ValueError(f"{label} must be relative: {value}")
    if ".." in posix.parts or ".." in windows.parts:
        raise ValueError(f"{label} cannot contain '..': {value}")

    normalized = value.replace("\\", "/")
    normalized_path = PurePosixPath(normalized)
    if normalized_path.is_absolute() or ".." in normalized_path.parts:
        raise ValueError(f"{label} must stay inside the project: {value}")
    return normalized_path.as_posix()


def inside(root: Path, value: Any, label: str) -> tuple[str, Path]:
    relative = normalize_relative_path(value, label)
    candidate = (root / relative).resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError(f"{label} leaves the project: {relative}")
    return relative, candidate


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path.name} must contain one JSON object")
    return data


def required_file_values(config: dict[str, Any]) -> list[str]:
    configured = config.get("required_files", [])
    if not isinstance(configured, list) or not all(isinstance(item, str) for item in configured):
        raise ValueError("required_files must be a list of relative paths")

    values: list[str] = []
    seen: set[str] = set()
    for raw in (*MANDATORY_EVIDENCE, *configured):
        relative = normalize_relative_path(raw, "required file")
        if relative not in seen:
            seen.add(relative)
            values.append(relative)
    return values


def prepare_contract(
    root: Path, config: dict[str, Any]
) -> tuple[str, Path, list[tuple[str, Path]], str, Path]:
    deliverable_value, deliverable = inside(root, config.get("deliverable"), "deliverable")

    required_files = [
        inside(root, relative, "required file") for relative in required_file_values(config)
    ]

    receipt_value, receipt = inside(root, config.get("receipt"), "receipt")
    receipt_relative = PurePosixPath(receipt_value)
    if receipt_relative.parent != PurePosixPath("out") or receipt_relative.suffix.lower() != ".json":
        raise ValueError("receipt must be a direct out/*.json path")

    protected = {root / CONFIG_NAME, deliverable, *(path for _, path in required_files)}
    protected = {path.resolve() for path in protected}
    if receipt in protected:
        raise ValueError("receipt must not overlap the contract, deliverable, or required evidence")

    return deliverable_value, deliverable, required_files, receipt_value, receipt


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            json.dump(payload, temporary, indent=2)
            temporary.write("\n")
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_path, path)
        temporary_path = None
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink()
            except FileNotFoundError:
                pass


def best_effort_protected_paths(root: Path, config: dict[str, Any] | None) -> set[Path]:
    protected = {(root / CONFIG_NAME).resolve()}
    if config is None:
        return protected

    raw_values: list[Any] = [config.get("deliverable")]
    configured_required = config.get("required_files")
    if isinstance(configured_required, list):
        raw_values.extend(configured_required)
    raw_values.extend(MANDATORY_EVIDENCE)
    for raw in raw_values:
        try:
            _, path = inside(root, raw, "protected path")
        except (OSError, ValueError):
            continue
        protected.add(path)
    return protected


def fallback_receipt(
    event: dict[str, Any],
    root: Path,
    reason: str,
    config: dict[str, Any] | None = None,
) -> Path:
    protected = best_effort_protected_paths(root, config)
    candidates: list[Path] = []
    for index in range(100):
        relative = FALLBACK_RECEIPT if index == 0 else f"out/QUALITY_GATE_HOLD_{index}.json"
        _, candidate = inside(root, relative, "fallback receipt")
        candidates.append(candidate)

    receipt_path = next((path for path in candidates if path not in protected), None)
    if receipt_path is None:
        raise ValueError("no non-overlapping fallback receipt path is available")

    payload = {
        "gate": GATE_NAME,
        "status": "HOLD",
        "checked_at": checked_at(),
        "hook_event": event.get("hook_event_name", "Stop"),
        "model": event.get("model"),
        "deliverable": None,
        "sha256": None,
        "results": [
            {
                "check": "quality gate configuration and I/O",
                "status": "FAIL",
                "detail": redact_secret_text(reason)[:2000],
            }
        ],
    }
    write_json_atomic(receipt_path, payload)
    return receipt_path


def hold_with_fallback(
    event: dict[str, Any],
    root: Path,
    reason: str,
    config: dict[str, Any] | None = None,
) -> None:
    safe_reason = redact_secret_text(reason)
    try:
        path = fallback_receipt(event, root, safe_reason, config)
        safe_reason += f" HOLD receipt: {path.relative_to(root).as_posix()}."
    except (OSError, ValueError) as error:
        safe_reason += f" Could not write the fallback HOLD receipt: {redact_secret_text(str(error))}."
    hold(event, safe_reason)


def add_result(results: list[dict[str, Any]], name: str, passed: bool, detail: str) -> None:
    results.append(
        {
            "check": name,
            "status": "PASS" if passed else "FAIL",
            "detail": redact_secret_text(detail),
        }
    )


def validate_citation_pattern(config: dict[str, Any]) -> None:
    value = config.get("citation_pattern")
    if not isinstance(value, str) or not value:
        raise ValueError("citation_pattern must be a regular expression for complete [C#] tags")
    pattern = re.compile(value, flags=re.IGNORECASE)
    valid_samples = ("[C1]", "[C42]", "[C999]")
    invalid_samples = ("C1", "[C0]", "[C01]", "[X1]", "prefix [C1]", "[C1] suffix", "[C1][C2]")
    if not all(pattern.fullmatch(sample) for sample in valid_samples) or any(
        pattern.fullmatch(sample) for sample in invalid_samples
    ):
        raise ValueError("citation_pattern must match one complete [C#] tag and nothing broader")


def identifier_sort(identifier: str) -> tuple[int, str]:
    return int(identifier[1:]), identifier


def validate(
    config: dict[str, Any],
    event: dict[str, Any],
    deliverable_value: str,
    deliverable: Path,
    required_files: list[tuple[str, Path]],
) -> tuple[dict[str, Any], list[str]]:
    results: list[dict[str, Any]] = []
    failures: list[str] = []

    required_by_name = dict(required_files)
    for relative, path in required_files:
        present = path.is_file()
        add_result(results, f"required file: {relative}", present, "present" if present else "missing")
        if not present:
            failures.append(f"missing required file {relative}")

    if not deliverable.is_file():
        add_result(results, "deliverable exists", False, deliverable_value)
        failures.append(f"missing deliverable {deliverable_value}")
        text = ""
        digest = None
    else:
        raw = deliverable.read_bytes()
        text = raw.decode("utf-8-sig")
        digest = hashlib.sha256(raw).hexdigest()
        add_result(results, "deliverable exists", True, deliverable_value)

    headings = config.get("required_headings", [])
    if not isinstance(headings, list) or not all(isinstance(item, str) and item.strip() for item in headings):
        raise ValueError("required_headings must be a list of non-empty strings")
    for heading in headings:
        found = (
            re.search(
                rf"^##+\s+{re.escape(heading)}\s*$",
                text,
                flags=re.IGNORECASE | re.MULTILINE,
            )
            is not None
        )
        add_result(results, f"heading: {heading}", found, "found" if found else "missing")
        if not found:
            failures.append(f"missing heading {heading}")

    validate_citation_pattern(config)
    minimum_citations = config.get("minimum_citations", 0)
    if type(minimum_citations) is not int or minimum_citations < 0:
        raise ValueError("minimum_citations must be a non-negative integer")

    cited_ids = sorted(
        {match.group(1).upper() for match in CANONICAL_CITATION_RE.finditer(text)},
        key=identifier_sort,
    )
    citations_pass = len(cited_ids) >= minimum_citations
    add_result(
        results,
        "distinct citation count",
        citations_pass,
        f"{len(cited_ids)} found ({', '.join(cited_ids) or 'none'}); {minimum_citations} required",
    )
    if not citations_pass:
        failures.append(f"only {len(cited_ids)} distinct citations; need {minimum_citations}")

    manifest = required_by_name[SOURCE_MANIFEST]
    declared_ids: list[str] = []
    if manifest.is_file():
        manifest_text = manifest.read_text(encoding="utf-8-sig")
        declared_ids = sorted(
            {match.group(1).upper() for match in MANIFEST_ID_RE.finditer(manifest_text)},
            key=identifier_sort,
        )
    manifest_has_ids = bool(declared_ids)
    add_result(
        results,
        "source manifest declares citation IDs",
        manifest_has_ids,
        ", ".join(declared_ids) if declared_ids else "no C-number IDs found",
    )
    if not manifest_has_ids:
        failures.append("source manifest declares no C-number IDs")

    unknown_ids = sorted(set(cited_ids) - set(declared_ids), key=identifier_sort)
    citations_declared = manifest_has_ids and not unknown_ids
    add_result(
        results,
        "citations declared in source manifest",
        citations_declared,
        "all declared" if citations_declared else f"undeclared: {', '.join(unknown_ids) or 'manifest unavailable'}",
    )
    if unknown_ids:
        failures.append(f"undeclared citation IDs: {', '.join(unknown_ids)}")

    max_lines = config.get("maximum_nonblank_lines")
    if type(max_lines) is not int or max_lines < 1:
        raise ValueError("maximum_nonblank_lines must be a positive integer")
    line_count = sum(1 for line in text.splitlines() if line.strip())
    length_pass = line_count <= max_lines
    add_result(results, "nonblank line limit", length_pass, f"{line_count} found; maximum {max_lines}")
    if not length_pass:
        failures.append(f"{line_count} nonblank lines; maximum {max_lines}")

    configured_forbidden = config.get("forbidden_patterns", [])
    if not isinstance(configured_forbidden, list) or not all(
        isinstance(item, str) and item for item in configured_forbidden
    ):
        raise ValueError("forbidden_patterns must be a list of non-empty regular expressions")
    forbidden = list(dict.fromkeys((*configured_forbidden, *MANDATORY_SECRET_PATTERNS)))
    for pattern_value in forbidden:
        pattern = re.compile(pattern_value, flags=re.IGNORECASE)
        found = pattern.search(text) is not None
        add_result(
            results,
            f"forbidden pattern: {pattern_value}",
            not found,
            "absent" if not found else "found and redacted",
        )
        if found:
            failures.append(f"forbidden pattern found: {pattern_value}")

    receipt = {
        "gate": GATE_NAME,
        "status": "PASS" if not failures else "FAIL",
        "checked_at": checked_at(),
        "hook_event": event.get("hook_event_name", "Stop"),
        "model": event.get("model"),
        "deliverable": deliverable_value,
        "sha256": digest,
        "cited_ids": cited_ids,
        "manifest_ids": declared_ids,
        "results": results,
    }
    return receipt, failures


def run(event: dict[str, Any]) -> int:
    root = Path(event.get("cwd") or os.getcwd()).resolve()
    config_path = root / CONFIG_NAME
    if not config_path.is_file():
        emit({})
        return 0

    try:
        config = load_json(config_path)
    except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        hold_with_fallback(event, root, f"P2 quality gate cannot read its contract: {error}")
        return 0

    if config.get("enabled") is not True:
        emit({})
        return 0

    receipt_path: Path | None = None
    try:
        deliverable_value, deliverable, required_files, _receipt_value, receipt_path = prepare_contract(
            root, config
        )
        receipt, failures = validate(
            config,
            event,
            deliverable_value,
            deliverable,
            required_files,
        )
        write_json_atomic(receipt_path, receipt)
    except (OSError, ValueError, re.error, UnicodeDecodeError) as error:
        hold_with_fallback(
            event,
            root,
            f"P2 quality gate configuration or read failed: {error}",
            config,
        )
        return 0

    if not failures:
        emit({})
        return 0

    reason = (
        "P2 release is on HOLD: "
        + "; ".join(failures[:8])
        + ". Repair only these failures, then stop once more."
    )
    hold(event, reason)
    return 0


def parse_event() -> dict[str, Any]:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError as error:
        raise ValueError(f"hook input is not valid JSON: {error}") from error
    if not isinstance(data, dict):
        raise ValueError("hook input must be one JSON object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="run a manual Stop check in the current directory")
    args = parser.parse_args()
    try:
        event = (
            {
                "cwd": os.getcwd(),
                "hook_event_name": "Stop",
                "stop_hook_active": False,
                "model": "manual-check",
            }
            if args.check
            else parse_event()
        )
    except ValueError as error:
        hold({"stop_hook_active": False}, str(error))
        return 0
    return run(event)


if __name__ == "__main__":
    raise SystemExit(main())
