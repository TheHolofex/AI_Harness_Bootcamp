#!/usr/bin/env python3
"""Route one lot batch with the adjacent saved rule. Practice control, not a dispatch tool."""

from __future__ import annotations

import csv
import io
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RULE = ROOT / "RULE.md"
INPUT_FIELDS = [
    "lot",
    "permit",
    "gate_window",
    "input_disposition",
    "resource_exception",
]
OUTPUT_FIELDS = ["lot", "route", "status"]
DISPOSITIONS = {"NEW", "CHANGED", "CANCELLED", "UNCHANGED"}
PENDING_LINES = {
    "pending_status: OPEN": "OPEN",
    "pending_status: NOT_AUTHORIZED": "NOT_AUTHORIZED",
}


class Hold(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def decide(permit: str, resource_exception: str, pending_status: str) -> tuple[str, str]:
    if resource_exception == "RACK_CONFLICT":
        return "hold", "RESOURCE_CONFLICT"
    if permit == "AUTHORIZED":
        return "pass", "READY"
    if permit == "PENDING":
        if pending_status == "NOT_AUTHORIZED":
            return "reject", "NOT_AUTHORIZED"
        return "hold", "OPEN"
    return "hold", "OPEN"


def pending_status(rule_text: str) -> str:
    found = [line.strip() for line in rule_text.splitlines() if line.strip().startswith("pending_status:")]
    if len(found) != 1:
        raise Hold("HOLD: pending_status missing or duplicate")
    status = PENDING_LINES.get(found[0])
    if status is None:
        raise Hold("HOLD: pending_status unknown")
    return status


def load_rows(csv_path: Path) -> list[dict[str, str]]:
    if csv_path.is_symlink() or not csv_path.is_file():
        raise Hold("HOLD: missing input")
    try:
        raw = csv_path.read_bytes()
    except OSError as exc:
        raise Hold("HOLD: unreadable input") from exc
    if raw.startswith(b"\xef\xbb\xbf"):
        raise Hold("HOLD: malformed input")
    try:
        decoded = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Hold("HOLD: malformed input") from exc
    reader = csv.DictReader(io.StringIO(decoded, newline=""))
    if list(reader.fieldnames or []) != INPUT_FIELDS:
        raise Hold("HOLD: malformed input")
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in reader:
        if row.get(None):
            raise Hold("HOLD: malformed input")
        if any(row.get(field) is None for field in INPUT_FIELDS):
            raise Hold("HOLD: malformed input")
        values = {field: row[field] for field in INPUT_FIELDS}
        lot = values["lot"]
        if not lot or lot in seen or any(mark in lot for mark in (",", '"', "\n", "\r", "\x00")):
            raise Hold("HOLD: malformed input")
        seen.add(lot)
        if values["input_disposition"] not in DISPOSITIONS:
            raise Hold("HOLD: malformed input")
        if values["resource_exception"] not in {"", "RACK_CONFLICT"}:
            raise Hold("HOLD: malformed input")
        if values["input_disposition"] == "CANCELLED" and values["permit"] != "WITHDRAWN":
            raise Hold("HOLD: malformed input")
        rows.append(values)
    if not rows:
        raise Hold("HOLD: malformed input")
    return rows


def write_exclusive(path: Path, payload: bytes) -> None:
    if os.path.lexists(str(path)):
        raise Hold("HOLD: output exists")
    if not path.parent.is_dir() or path.parent.is_symlink():
        raise Hold("HOLD: missing output directory")
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    except FileExistsError as exc:
        raise Hold("HOLD: output exists") from exc
    except OSError as exc:
        raise Hold("HOLD: unreadable output path") from exc
    try:
        os.write(fd, payload)
    except OSError as exc:
        raise Hold("HOLD: unreadable output path") from exc
    finally:
        os.close(fd)


def route(csv_path: Path, out_path: Path) -> None:
    if RULE.is_symlink() or not RULE.is_file():
        raise Hold("HOLD: missing rule")
    try:
        rule_text = RULE.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise Hold("HOLD: unreadable rule") from exc
    status = pending_status(rule_text)
    rows = load_rows(csv_path)
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(OUTPUT_FIELDS)
    for row in rows:
        route_name, route_status = decide(row["permit"], row["resource_exception"], status)
        writer.writerow([row["lot"], route_name, route_status])
    write_exclusive(out_path, buffer.getvalue().encode("utf-8"))


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: route.py <input.csv> <out/receipts.csv>", file=sys.stderr)
        print("HOLD: usage", file=sys.stderr)
        return 2
    try:
        route(Path(argv[1]), Path(argv[2]))
    except Hold as exc:
        print(exc.message, file=sys.stderr)
        return 1
    except (OSError, UnicodeError):
        print("HOLD: unreadable input", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
