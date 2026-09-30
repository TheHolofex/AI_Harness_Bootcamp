#!/usr/bin/env python3
"""Restore one work copy's saved rule from its distinct frozen baseline."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

HEX = set("0123456789abcdef")


class Hold(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def inside(root: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except (ValueError, OSError):
        return False
    return True


def digest_token(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise Hold("HOLD: malformed baseline digest") from exc
    except OSError as exc:
        raise Hold("HOLD: unreadable baseline digest") from exc
    tokens = text.split()
    if not tokens:
        raise Hold("HOLD: malformed baseline digest")
    token = tokens[0].lower()
    if len(token) != 64 or any(char not in HEX for char in token):
        raise Hold("HOLD: malformed baseline digest")
    return token


def restore(workdir: Path) -> None:
    if not workdir.is_dir() or workdir.is_symlink():
        raise Hold("HOLD: missing workdir")
    baseline = workdir / "shared" / "baseline" / "RULE.md"
    digest_path = workdir / "shared" / "baseline" / "RULE.md.sha256"
    active = workdir / "shared" / "workflow" / "RULE.md"
    if baseline.is_symlink() or not baseline.is_file() or not inside(workdir, baseline):
        raise Hold("HOLD: missing baseline")
    if digest_path.is_symlink() or not digest_path.is_file() or not inside(workdir, digest_path):
        raise Hold("HOLD: missing baseline digest")
    expected = digest_token(digest_path)
    try:
        baseline_bytes = baseline.read_bytes()
    except OSError as exc:
        raise Hold("HOLD: unreadable baseline") from exc
    actual = hashlib.sha256(baseline_bytes).hexdigest()
    if expected != actual:
        raise Hold("HOLD: baseline digest mismatch")
    if active.is_symlink() or not inside(workdir, active):
        raise Hold("HOLD: restore target escaped")
    if active.exists() and active.resolve() == baseline.resolve():
        raise Hold("HOLD: baseline is not distinct")
    if active.parent.is_symlink() or not active.parent.is_dir() or not inside(workdir, active.parent):
        raise Hold("HOLD: restore target escaped")
    active.write_bytes(baseline_bytes)
    if active.read_bytes() != baseline_bytes:
        raise Hold("HOLD: restore mismatch")
    print("RESTORE OK")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: restore_rule.py <workdir>", file=sys.stderr)
        print("HOLD: usage", file=sys.stderr)
        return 2
    try:
        restore(Path(argv[1]))
    except Hold as exc:
        print(exc.message, file=sys.stderr)
        return 1
    except OSError:
        print("HOLD: unreadable baseline", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
