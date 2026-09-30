#!/usr/bin/env python3
"""Restore one work-copy renderer from its hashed baseline."""

from __future__ import annotations

import hashlib
import os
import re
import sys
from pathlib import Path


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


def digest_ok(baseline: Path, digest_path: Path) -> bytes:
    text = digest_path.read_text(encoding="utf-8")
    if not re.fullmatch(r"[0-9a-f]{64}\n", text):
        raise Hold("HOLD: baseline digest is not a hex line")
    content = baseline.read_bytes()
    if hashlib.sha256(content).hexdigest() != text.strip():
        raise Hold("HOLD: baseline changed")
    return content


def next_attempt(attempts: Path) -> Path:
    attempts.mkdir(exist_ok=True)
    if attempts.is_symlink():
        raise Hold("HOLD: path not allowed")
    numbers = []
    for child in attempts.iterdir():
        if child.is_symlink():
            raise Hold("HOLD: path not allowed")
        if child.name.startswith("attempt-") and child.name.removeprefix("attempt-").isdigit():
            numbers.append(int(child.name.removeprefix("attempt-")))
    destination = attempts / f"attempt-{max(numbers, default=0) + 1}"
    destination.mkdir()
    return destination


def preserve(workdir: Path, renderer: Path, out_dir: Path, attempt: Path) -> None:
    (attempt / "render_review.py").write_bytes(renderer.read_bytes())
    saved = attempt / "out"
    saved.mkdir()
    found = False
    for item in sorted(out_dir.rglob("*")):
        if item.is_symlink() or not item.resolve().is_relative_to(out_dir.resolve()):
            raise Hold("HOLD: path not allowed")
        target = saved / item.relative_to(out_dir)
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        if not item.is_file():
            raise Hold("HOLD: path not allowed")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(item.read_bytes())
        found = True
    if not found:
        raise Hold("HOLD: no output to preserve")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: restore.py <workdir>", file=sys.stderr)
        return 2
    try:
        workdir = resolve_workdir(argv[1])
        renderer = require_inside(workdir / "scripts" / "render_review.py", workdir)
        baseline = require_inside(workdir / "baseline" / "render_review.py", workdir)
        digest = require_inside(workdir / "baseline" / "render_review.py.sha256", workdir)
        out_dir = require_inside(workdir / "out", workdir)
        if not renderer.is_file() or not baseline.is_file() or not digest.is_file() or not out_dir.is_dir():
            raise Hold("HOLD: missing baseline or output")
        content = digest_ok(baseline, digest)
        attempt = next_attempt(require_inside(workdir / "attempts", workdir) if (workdir / "attempts").exists() else workdir / "attempts")
        if not attempt.resolve().is_relative_to(workdir.resolve()):
            raise Hold("HOLD: path not allowed")
        preserve(workdir, renderer, out_dir, attempt)
        temporary = renderer.with_name("render_review.py.restore-tmp")
        if temporary.exists() or temporary.is_symlink():
            raise Hold("HOLD: output already exists")
        temporary.write_bytes(content)
        os.replace(temporary, renderer)
        if renderer.is_symlink() or renderer.read_bytes() != content or baseline.read_bytes() != content:
            raise Hold("HOLD: restore mismatch")
    except Hold as error:
        print(error.message, file=sys.stderr)
        return 1
    print("RESTORE OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
