#!/usr/bin/env python3
"""Match two configured substrings in one run file.

A match means both literals occur in the file text. It is not a release
decision. The characters RELEASED occur inside UNRELEASED, so this check
cannot tell those stamps apart.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def parse_invocation(argv: list[str]) -> tuple[str, str] | None:
    args = argv[1:]
    if len(args) != 3:
        return None
    if args[1] == "--config" and _is_path(args[0]) and _is_path(args[2]):
        return args[0], args[2]
    if args[0] == "--config" and _is_path(args[1]) and _is_path(args[2]):
        return args[2], args[1]
    return None


def _is_path(value: str) -> bool:
    return bool(value) and not value.startswith("-")


def _pairs(items: list[tuple[str, object]]) -> dict:
    seen: set[str] = set()
    result = {}
    for key, value in items:
        if key in seen:
            raise ValueError("duplicate key")
        seen.add(key)
        result[key] = value
    return result


def load_literals(path: Path) -> tuple[str, str]:
    if not path.is_file():
        raise ValueError("HOLD: malformed config")
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("HOLD: malformed config") from error
    if not text.strip():
        raise ValueError("HOLD: malformed config")
    try:
        data = json.loads(text, object_pairs_hook=_pairs)
    except (json.JSONDecodeError, ValueError) as error:
        raise ValueError("HOLD: malformed config") from error
    if not isinstance(data, dict) or set(data) != {"all_present"}:
        raise ValueError("HOLD: malformed config")
    values = data["all_present"]
    if (
        not isinstance(values, list)
        or len(values) != 2
        or not all(isinstance(item, str) and item != "" for item in values)
        or values[0] == values[1]
    ):
        raise ValueError("HOLD: malformed config")
    return values[0], values[1]


def run(path: Path, literals: tuple[str, str]) -> int:
    if not path.is_file():
        print("HOLD: missing input", file=sys.stderr)
        return 1
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError, PermissionError):
        print("HOLD: unreadable input", file=sys.stderr)
        return 1
    first, second = literals
    if first in text and second in text:
        print("MATCH: both literals present")
        return 1
    print("PASS: at least one literal absent")
    return 0


def main(argv: list[str]) -> int:
    parsed = parse_invocation(argv)
    if parsed is None:
        print(
            "HOLD: usage: predicate.py <run-file> --config <predicate.json>",
            file=sys.stderr,
        )
        return 2
    run_file, config_file = parsed
    try:
        literals = load_literals(Path(config_file))
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    return run(Path(run_file), literals)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
