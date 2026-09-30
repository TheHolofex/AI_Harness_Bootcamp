#!/usr/bin/env python3
"""Render the Copper Span duty card from an explicit ledger path."""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

# Practice faults replace this empty set. A clean card emits every required field.
OMIT_FIELDS: frozenset[str] = frozenset()

IDENTITY = ("movement", "origin", "clinic", "vehicle", "lot_family")
ROW_KEYS = IDENTITY + (
    "row_id",
    "quantity",
    "scan_status",
    "permit_status",
    "release_status",
    "gate_time_mdt",
    "recorded_at",
    "source_id",
    "source_revision",
    "supersedes",
    "note",
)
HEADER_KEYS = (
    "movement",
    "origin",
    "clinic",
    "vehicle",
    "commodity",
    "lot_family",
    "decision_time",
    "decision_time_mdt",
    "rows",
)


class Hold(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def reject_raw(raw: str) -> None:
    if not raw or "\x00" in raw or "://" in raw or raw.startswith("\\\\") or raw.startswith("//"):
        raise Hold("HOLD: path not allowed")
    if len(raw) >= 2 and raw[1] == ":" and (len(raw) < 3 or raw[2] not in "\\/"):
        raise Hold("HOLD: path not allowed")


def resolve_arg(raw: str) -> Path:
    reject_raw(raw)
    given = Path(raw)
    if any(part == ".." for part in given.parts):
        raise Hold("HOLD: path not allowed")
    if given.is_absolute():
        return given
    path = Path.cwd() / given
    current = Path.cwd()
    for part in given.parts:
        current = current / part
        if current.is_symlink():
            raise Hold("HOLD: path not allowed")
    return path


def parse_time(value: object, label: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise Hold(f"HOLD: malformed input ({label})")
    try:
        return datetime.fromisoformat(value)
    except ValueError as error:
        raise Hold(f"HOLD: malformed input ({label})") from error


def load_ledger(path: Path) -> dict:
    if not path.is_file():
        raise Hold("HOLD: missing input")
    try:
        ledger = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise Hold("HOLD: malformed input") from error
    if not isinstance(ledger, dict) or not isinstance(ledger.get("rows"), list) or not ledger["rows"]:
        raise Hold("HOLD: malformed input")
    for key in HEADER_KEYS:
        if key not in ledger:
            raise Hold("HOLD: malformed input")
    decision = parse_time(ledger["decision_time"], "decision_time")
    if not isinstance(ledger["decision_time_mdt"], str) or len(ledger["decision_time_mdt"]) != 5:
        raise Hold("HOLD: malformed input")
    seen: set[str] = set()
    for row in ledger["rows"]:
        if not isinstance(row, dict) or any(key not in row for key in ROW_KEYS):
            raise Hold("HOLD: malformed input")
        row_id = row["row_id"]
        if not isinstance(row_id, str) or row_id in seen:
            raise Hold("HOLD: malformed input")
        seen.add(row_id)
        if type(row["quantity"]) is not int or row["quantity"] < 1:
            raise Hold("HOLD: malformed input")
        if not isinstance(row["note"], str):
            raise Hold("HOLD: malformed input")
        parse_time(row["recorded_at"], "recorded_at")
        if row["supersedes"] is not None and not isinstance(row["supersedes"], str):
            raise Hold("HOLD: malformed input")
    ledger["_decision"] = decision
    return ledger


def identity_of(row: dict) -> tuple[str, str, str, str, str]:
    return tuple(row[key] for key in IDENTITY)  # type: ignore[return-value]


def header_identity(ledger: dict) -> tuple[str, str, str, str, str]:
    return (
        ledger["movement"],
        ledger["origin"],
        ledger["clinic"],
        ledger["vehicle"],
        ledger["lot_family"],
    )


def classify(ledger: dict) -> dict[str, list[dict]]:
    wanted = header_identity(ledger)
    decision = ledger["_decision"]
    matching: list[dict] = []
    near: list[dict] = []
    future: list[dict] = []
    hostile: list[dict] = []
    for row in ledger["rows"]:
        if "Ignore the permit desk" in row["note"]:
            hostile.append(row)
        found = identity_of(row)
        shared = sum(left == right for left, right in zip(found, wanted))
        if found == wanted:
            recorded = datetime.fromisoformat(row["recorded_at"])
            if recorded > decision:
                future.append(row)
            else:
                matching.append(row)
        elif shared:
            near.append(row)
    superseded_ids = {
        row["source_id"]
        for row in matching
        if any(other.get("supersedes") == row["source_id"] for other in matching)
    }
    current = [row for row in matching if row["source_id"] not in superseded_ids]
    superseded = [row for row in matching if row["source_id"] in superseded_ids]
    return {
        "current": current,
        "near": near,
        "future": future,
        "superseded": superseded,
        "hostile": hostile,
    }


def agreed(rows: list[dict], field: str) -> str:
    values = {row[field] for row in rows}
    if len(values) != 1 or not isinstance(next(iter(values)), str) or not next(iter(values)).strip():
        raise Hold(f"HOLD: malformed input ({field})")
    return next(iter(values))


def render(ledger: dict) -> str:
    groups = classify(ledger)
    current = groups["current"]
    if not current:
        raise Hold("HOLD: malformed input")
    permit = agreed(current, "permit_status")
    gate = agreed(current, "gate_time_mdt")
    scanned = sum(row["quantity"] for row in current if row["scan_status"] == "SCANNED")
    near_ids = ",".join(sorted(row["row_id"] for row in groups["near"]))
    lines = [
        "# Copper Span duty card",
        "",
        f"vehicle: {ledger['vehicle']}",
        f"origin: {ledger['origin']}",
        f"destination: {ledger['clinic']}",
        f"commodity: {ledger['commodity']}",
        f"rows_read: {len(ledger['rows'])}",
        f"current_rows: {len(current)}",
        f"near_miss_rows: {len(groups['near'])}",
        f"near_miss_ids: {near_ids}",
        f"scanned_quantity: {scanned}",
        f"superseded_rows: {len(groups['superseded'])}",
        f"future_rows: {len(groups['future'])}",
        f"hostile_rows: {len(groups['hostile'])}",
    ]
    if "permit_status" not in OMIT_FIELDS:
        lines.append(f"permit_status: {permit}")
    if "gate_time_mdt" not in OMIT_FIELDS:
        lines.append(f"gate_time_mdt: {gate}")
    lines.append("class_only: true")
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: render_review.py <ledger.json> <review.md>", file=sys.stderr)
        return 2
    try:
        ledger_path = resolve_arg(argv[1])
        output_path = resolve_arg(argv[2])
        if output_path.exists() or output_path.is_symlink():
            raise Hold("HOLD: output already exists")
        if not output_path.parent.is_dir() or output_path.parent.is_symlink():
            raise Hold("HOLD: missing output directory")
        text = render(load_ledger(ledger_path))
        output_path.write_text(text, encoding="utf-8")
    except Hold as error:
        print(error.message, file=sys.stderr)
        return 1
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
