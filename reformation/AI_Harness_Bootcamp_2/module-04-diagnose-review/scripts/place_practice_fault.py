#!/usr/bin/env python3
"""Place an inspectable practice fault on a validated work-copy renderer."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from pathlib import Path

MARKER = "OMIT_FIELDS: frozenset[str] = frozenset()"
VARIANTS = {"A": "permit_status", "B": "gate_time_mdt"}


class Hold(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def reject_raw(raw: str) -> None:
    if not raw or "\x00" in raw or "://" in raw or raw.startswith("\\\\") or raw.startswith("//"):
        raise Hold("HOLD: path not allowed")
    if len(raw) >= 2 and raw[1] == ":" and (len(raw) < 3 or raw[2] not in "\\/"):
        raise Hold("HOLD: path not allowed")


def resolve_workdir(raw: str) -> Path:
    reject_raw(raw)
    path = Path(raw).expanduser()
    if path.is_symlink():
        raise Hold("HOLD: path not allowed")
    resolved = path.resolve()
    if not resolved.is_dir():
        raise Hold("HOLD: missing work folder")
    return resolved


def require_inside(path: Path, root: Path) -> Path:
    try:
        lexical = path.relative_to(root)
    except ValueError as error:
        raise Hold("HOLD: path not allowed") from error
    if ".." in lexical.parts:
        raise Hold("HOLD: path not allowed")
    probe = root
    for part in lexical.parts:
        probe = probe / part
        if probe.is_symlink():
            raise Hold("HOLD: path not allowed")
    if probe.exists() and not probe.resolve().is_relative_to(root.resolve()):
        raise Hold("HOLD: path not allowed")
    return probe


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Place practice variant A or B.")
    parser.add_argument("workdir")
    parser.add_argument("--variant", required=True, choices=tuple(VARIANTS))
    try:
        args = parser.parse_args(argv[1:])
    except SystemExit as error:
        return int(error.code) if isinstance(error.code, int) else 2
    try:
        workdir = resolve_workdir(args.workdir)
        renderer = require_inside(workdir / "scripts" / "render_review.py", workdir)
        baseline = require_inside(workdir / "baseline" / "render_review.py", workdir)
        digest = require_inside(workdir / "baseline" / "render_review.py.sha256", workdir)
        if not renderer.is_file() or not baseline.is_file() or not digest.is_file():
            raise Hold("HOLD: missing baseline")
        text = digest.read_text(encoding="utf-8")
        if not re.fullmatch(r"[0-9a-f]{64}\n", text):
            raise Hold("HOLD: baseline digest is not a hex line")
        baseline_bytes = baseline.read_bytes()
        if hashlib.sha256(baseline_bytes).hexdigest() != text.strip():
            raise Hold("HOLD: baseline changed")
        if renderer.read_bytes() != baseline_bytes:
            raise Hold("HOLD: work copy is not the clean baseline")
        source = baseline_bytes.decode("utf-8")
        if source.count(MARKER) != 1:
            raise Hold("HOLD: clean renderer has no omission marker")
        field = VARIANTS[args.variant]
        updated = source.replace(MARKER, f'OMIT_FIELDS: frozenset[str] = frozenset({{"{field}"}})', 1)
        temporary = renderer.with_name("render_review.py.fault-tmp")
        if temporary.exists() or temporary.is_symlink():
            raise Hold("HOLD: output already exists")
        temporary.write_text(updated, encoding="utf-8")
        os.replace(temporary, renderer)
        if baseline.read_bytes() != baseline_bytes or digest.read_text(encoding="utf-8") != text:
            raise Hold("HOLD: baseline changed")
    except Hold as error:
        print(error.message, file=sys.stderr)
        return 1
    print(f"FAULT PLACED {args.variant}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
