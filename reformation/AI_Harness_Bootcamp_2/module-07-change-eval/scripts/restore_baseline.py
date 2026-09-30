#!/usr/bin/env python3
"""Restore the active instruction and baseline briefs from frozen hashes.

Usage: restore_baseline.py <workdir>
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hold(message: str) -> int:
    print(f"HOLD: {message}", file=sys.stderr)
    return 1


def inside(root: Path, path: Path) -> bool:
    try:
        root = root.resolve()
        current = path.absolute()
        if not current.is_relative_to(root):
            return False
        while current != root:
            if current.is_symlink():
                return False
            current = current.parent
        return path.resolve().is_relative_to(root)
    except (OSError, ValueError):
        return False


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: restore_baseline.py <workdir>", file=sys.stderr)
        return 2
    work = Path(argv[1]).expanduser().resolve()
    if not work.is_dir():
        return hold("workdir is missing")
    baseline = work / "shared" / "baseline"
    digest_path = baseline / "hashes.json"
    if not digest_path.is_file() or digest_path.is_symlink():
        return hold("frozen baseline digest is missing")
    try:
        digest = json.loads(digest_path.read_text(encoding="utf-8"))
        files = digest.get("files") if isinstance(digest, dict) else None
        if not isinstance(digest, dict) or digest.get("schema_version") != 1 or not isinstance(files, dict) or not files:
            return hold("frozen baseline digest is malformed")
        planned: list[tuple[Path, Path, str]] = []
        for relative, expected in files.items():
            if not isinstance(relative, str) or not isinstance(expected, str):
                return hold("frozen baseline digest is malformed")
            if relative.startswith(("/", "\\")) or ".." in Path(relative).parts:
                return hold("frozen baseline path escapes the baseline directory")
            source = baseline / relative
            if not source.is_file() or source.is_symlink() or not inside(baseline, source):
                return hold(f"frozen baseline file is missing or linked: {relative}")
            actual = sha256(source)
            if actual != expected:
                return hold(f"frozen baseline hash mismatch: {relative}")
            if relative == "active-instruction.md":
                destination = work / "shared" / "controls" / "active-instruction.md"
            elif relative.startswith("briefs/") and relative.endswith(".md"):
                case_id = Path(relative).stem
                destination = work / "shared" / "cases" / case_id / "baseline.md"
            else:
                return hold(f"frozen baseline path is not a restorable file: {relative}")
            if destination.is_symlink() or not inside(work, destination):
                return hold(f"restore target is linked or outside work: {relative}")
            planned.append((source, destination, actual))
        expected_cases = {f"briefs/PC-{number:02d}.md" for number in range(1, 41)}
        if set(files) != expected_cases | {"active-instruction.md"}:
            return hold("frozen baseline does not contain the instruction and all forty briefs")
        for source, destination, _hash in planned:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(source.read_bytes())
        for source, destination, expected in planned:
            if destination.is_symlink() or sha256(destination) != expected or destination.read_bytes() != source.read_bytes():
                return hold("restored bytes do not match the frozen baseline")
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return hold(str(error))
    print("RESTORE OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
