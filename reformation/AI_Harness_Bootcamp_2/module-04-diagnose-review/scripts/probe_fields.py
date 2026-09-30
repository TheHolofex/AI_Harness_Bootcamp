#!/usr/bin/env python3
"""Compare required fields on renderer-selected rows with an optional duty card.

Read-only. Selection is render_review.load_ledger and render_review.classify.
A missing card is not a renderer fault.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import render_review

FIELDS = ("permit_status", "gate_time_mdt")


class Hold(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def reject_raw(raw: str) -> None:
    if not raw or "\x00" in raw or "://" in raw or raw.startswith("\\\\") or raw.startswith("//"):
        raise Hold("HOLD: path not allowed")
    if len(raw) >= 2 and raw[1] == ":" and (len(raw) < 3 or raw[2] not in "\\/"):
        raise Hold("HOLD: path not allowed")


def open_ledger(raw: str) -> Path:
    reject_raw(raw)
    path = Path(raw).expanduser()
    if path.is_symlink() or not path.is_file():
        raise Hold("HOLD: missing input")
    return path.resolve()


def read_review(raw: str | None) -> str | None:
    if raw is None:
        return None
    reject_raw(raw)
    path = Path(raw).expanduser()
    if path.is_symlink():
        raise Hold("HOLD: path not allowed")
    if not path.exists():
        return None
    if not path.is_file():
        raise Hold("HOLD: path not allowed")
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise Hold("HOLD: cannot read review as UTF-8") from error


def selected_rows(path: Path) -> list[dict]:
    try:
        ledger = render_review.load_ledger(path)
        groups = render_review.classify(ledger)
    except render_review.Hold as error:
        raise Hold(error.message) from error
    rows = groups["current"]
    if not rows:
        raise Hold("HOLD: malformed input")
    return rows


def source_ids(rows: list[dict]) -> str:
    return ",".join(sorted(str(row["source_id"]) for row in rows))


def missing_current(rows: list[dict], field: str) -> list[str]:
    missing = []
    for row in rows:
        value = row.get(field)
        if not isinstance(value, str) or not value.strip():
            missing.append(row["row_id"])
    return sorted(missing)


def values_conflict(rows: list[dict], field: str) -> bool:
    values = {
        row[field]
        for row in rows
        if isinstance(row.get(field), str) and row[field].strip()
    }
    return len(values) > 1


def rendered(text: str, field: str) -> bool:
    return re.search(rf"^{re.escape(field)}: \S", text, flags=re.M) is not None


def classify_field(rows: list[dict], field: str, review: str | None, identity_differs: bool) -> str:
    if identity_differs:
        return "wrong_input_version"
    missing = missing_current(rows, field)
    if missing:
        return "source_omission " + " ".join(missing)
    if values_conflict(rows, field):
        return "source_conflict"
    if review is None:
        return "output_absent"
    if rendered(review, field):
        return "rendered"
    return "renderer_omission"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Compare selected ledger fields with an optional duty card.")
    parser.add_argument("ledger")
    parser.add_argument("--review")
    parser.add_argument("--intended")
    try:
        args = parser.parse_args(argv[1:])
    except SystemExit as error:
        return int(error.code) if isinstance(error.code, int) else 2
    try:
        rows = selected_rows(open_ledger(args.ledger))
        review = read_review(args.review)
        intended_rows = selected_rows(open_ledger(args.intended)) if args.intended else None
        selected = source_ids(rows)
        print(f"selected_source_ids {selected}")
        identity_differs = False
        if intended_rows is not None:
            intended = source_ids(intended_rows)
            print(f"intended_source_ids {intended}")
            selected_versions = sorted((row["source_id"], str(row["source_revision"])) for row in rows)
            intended_versions = sorted((row["source_id"], str(row["source_revision"])) for row in intended_rows)
            print("selected_source_versions " + ",".join(f"{source}@{revision}" for source, revision in selected_versions))
            print("intended_source_versions " + ",".join(f"{source}@{revision}" for source, revision in intended_versions))
            identity_differs = selected_versions != intended_versions
        print("review_present yes" if review is not None else "review_present no")
        for field in FIELDS:
            print(f"{field} {classify_field(rows, field, review, identity_differs)}")
    except Hold as error:
        print(error.message, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
