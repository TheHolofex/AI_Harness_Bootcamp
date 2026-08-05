#!/usr/bin/env python3
"""Full-tree staging inventory before/after exposure. Fail closed on unexpected delta."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Dict, List

# Only these files may be created after the freeze. No directory prefix is an
# allowlist: `out/evil.txt` must fail just like a top-level surprise file.
ALLOWED_AFTER_EXACT = {
    "out/triage_candidate.json",
    "out/session.json",
    "triage_record.md",
    "review_table.md",
}
# Never treat these as protected freeze roots if missing at freeze time is ok
SKIP_DIR_NAMES = {".git", "__pycache__", ".DS_Store"}


def iter_all_files(root: Path) -> List[Path]:
    out: List[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() and not path.is_symlink():
            continue
        if any(part in SKIP_DIR_NAMES for part in path.relative_to(root).parts):
            continue
        out.append(path)
    return sorted(out, key=lambda p: p.relative_to(root).as_posix())


def snapshot(root: Path) -> Dict[str, dict]:
    snap: Dict[str, dict] = {}
    for p in iter_all_files(root):
        rel = p.relative_to(root).as_posix()
        if p.is_symlink():
            target = p.readlink().as_posix().encode("utf-8")
            snap[rel] = {
                "kind": "symlink",
                "bytes": len(target),
                "sha256": hashlib.sha256(target).hexdigest(),
            }
        else:
            data = p.read_bytes()
            snap[rel] = {
                "kind": "file",
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
    return snap


def is_allowed_added(rel: str) -> bool:
    return rel in ALLOWED_AFTER_EXACT


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("staging_root", type=Path)
    ap.add_argument("--write", type=Path, required=True)
    ap.add_argument("--check", type=Path, default=None)
    args = ap.parse_args(argv)
    root = args.staging_root.expanduser().resolve()
    if not root.is_dir():
        print(f"HOLD inventory: missing {root}", file=sys.stderr)
        return 1
    snap = snapshot(root)
    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps({"files": snap}, indent=2) + "\n", encoding="utf-8")
    if not args.check:
        if len(snap) == 0:
            print("HOLD inventory: freeze captured zero files", file=sys.stderr)
            return 1
        print(f"PASS staging inventory freeze: {len(snap)} files -> {args.write}")
        return 0

    prior = json.loads(Path(args.check).read_text(encoding="utf-8"))["files"]
    if not prior:
        print("HOLD inventory: prior snapshot empty", file=sys.stderr)
        return 1
    missing = sorted(set(prior) - set(snap))
    added = sorted(set(snap) - set(prior))
    changed = sorted(
        k for k in set(prior) & set(snap)
        if prior[k]["sha256"] != snap[k]["sha256"] or prior[k]["bytes"] != snap[k]["bytes"]
    )
    # Anything present at freeze time is immutable, including a stale output.
    bad_changed = changed
    bad_added = [a for a in added if not is_allowed_added(a)]
    bad_missing = missing

    if bad_missing or bad_changed or bad_added:
        print(
            "HOLD staging inventory: "
            f"missing={bad_missing[:12]} changed={bad_changed[:12]} bad_added={bad_added[:12]}",
            file=sys.stderr,
        )
        return 1
    print(
        f"PASS staging inventory: {len(prior)} frozen stable; "
        f"allowed_delta added={len(added)} changed={len([c for c in changed if is_allowed_added(c)])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
