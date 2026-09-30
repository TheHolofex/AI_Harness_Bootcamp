#!/usr/bin/env python3
"""Hash exactly one file under shared/case/. Never write."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

CASE_ROOT = Path(__file__).resolve().parent.parent / "case"


def allowed(path: Path) -> bool:
    try:
        resolved = path.resolve()
        root = CASE_ROOT.resolve()
        resolved.relative_to(root)
    except (OSError, ValueError):
        return False
    return resolved.is_file()


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: hash_source.py <path>", file=sys.stderr)
        return 1
    path = Path(argv[1])
    if not allowed(path):
        print("HOLD: path not allowed", file=sys.stderr)
        return 1
    resolved = path.resolve()
    digest = hashlib.sha256(resolved.read_bytes()).hexdigest()
    print(f"sha256 {digest} {resolved.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
