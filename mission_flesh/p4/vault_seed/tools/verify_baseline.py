#!/usr/bin/env python3
"""Freeze or check a P4 vault tree by path, size, and sha256."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

SCHEMA_VERSION = 1
SKIPPED_DIRS = {".obsidian", "__pycache__", ".git"}
INTERNAL_MANIFEST = "Harness/BASELINE_MANIFEST.json"
SHA256_RE = __import__("re").compile(r"^[0-9a-f]{64}$")


class BaselineError(RuntimeError):
    """Raised when baseline freeze or check fails."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(64 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def requested_root(path: Path) -> Path:
    candidate = path.expanduser().absolute()
    if candidate.is_symlink() or not candidate.is_dir():
        raise BaselineError(f"Vault root must be a regular directory, not a link: {candidate}")
    return candidate.resolve()


def iter_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        rel_parts = path.relative_to(root).parts
        if any(part in SKIPPED_DIRS for part in rel_parts):
            continue
        yield path


def manifest_files(
    root: Path, *, exclude_internal_manifest: bool = False
) -> List[Dict[str, Any]]:
    files: List[Dict[str, Any]] = []
    for path in iter_files(root):
        rel = path.relative_to(root).as_posix()
        # Only the legacy internal mode excludes its own output. External P4
        # snapshots cover every in-scope vault file, including a stale copy of
        # the old internal manifest.
        if exclude_internal_manifest and rel == INTERNAL_MANIFEST:
            continue
        data = path.read_bytes()
        files.append(
            {
                "path": rel,
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    files.sort(key=lambda item: item["path"])
    return files


def manifest_fingerprint(files: Sequence[Mapping[str, Any]]) -> str:
    lines = [f"{item['path']}:{item['sha256']}" for item in files]
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def build_payload(
    root: Path, *, exclude_internal_manifest: bool = False
) -> Dict[str, Any]:
    files = manifest_files(root, exclude_internal_manifest=exclude_internal_manifest)
    return {
        "schema_version": SCHEMA_VERSION,
        "vault_root": ".",
        "root_fingerprint": manifest_fingerprint(files),
        "verification": {
            "tool": "verify_baseline",
            "file_count": len(files),
        },
        "files": files,
    }


def write_manifest(root: Path, destination: Optional[Path] = None) -> Dict[str, Any]:
    resolved = requested_root(root)
    target = destination if destination is not None else resolved / "Harness" / "BASELINE_MANIFEST.json"
    target = target.expanduser()
    if not target.is_absolute():
        target = Path.cwd() / target
    target_was_symlink = target.is_symlink()
    target = target.resolve()
    if destination is not None:
        try:
            target.relative_to(resolved)
        except ValueError:
            pass
        else:
            raise BaselineError("External integrity path must be outside the vault")
        if target_was_symlink or target.exists():
            raise BaselineError(f"External integrity path already exists: {target}")
    payload = build_payload(
        resolved,
        exclude_internal_manifest=destination is None,
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def load_manifest(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as error:
        raise BaselineError(f"Invalid baseline JSON: {error.msg}") from error
    if not isinstance(payload, dict):
        raise BaselineError("Baseline root must be an object")
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise BaselineError(f"Unsupported schema_version: {payload.get('schema_version')!r}")
    files = payload.get("files")
    if not isinstance(files, list) or not files:
        raise BaselineError("Baseline files must be a non-empty list")
    seen = set()
    for item in files:
        if not isinstance(item, dict):
            raise BaselineError("Each baseline file entry must be an object")
        path_value = item.get("path")
        bytes_value = item.get("bytes")
        digest = item.get("sha256")
        if not isinstance(path_value, str) or not path_value:
            raise BaselineError("Baseline file path must be a non-empty string")
        if not isinstance(bytes_value, int) or bytes_value < 0:
            raise BaselineError(f"Baseline bytes invalid for {path_value}")
        if not isinstance(digest, str) or not SHA256_RE.match(digest):
            raise BaselineError(f"Baseline sha256 invalid for {path_value}")
        if path_value in seen:
            raise BaselineError(f"Duplicate baseline path: {path_value}")
        seen.add(path_value)
    return payload


def check_manifest(root: Path, manifest_path: Path) -> Dict[str, Any]:
    resolved = requested_root(root)
    manifest_file = manifest_path.expanduser()
    if not manifest_file.is_absolute():
        manifest_file = Path.cwd() / manifest_file
    if not manifest_file.is_file() or manifest_file.is_symlink():
        raise BaselineError(f"Baseline manifest missing: {manifest_file}")
    manifest_file = manifest_file.resolve()
    expected = load_manifest(manifest_file)
    internal_target = (resolved / INTERNAL_MANIFEST).resolve()
    actual_files = {
        item["path"]: item
        for item in manifest_files(
            resolved,
            exclude_internal_manifest=manifest_file == internal_target,
        )
    }
    expected_files = {item["path"]: item for item in expected["files"]}

    missing = sorted(set(expected_files) - set(actual_files))
    added = sorted(set(actual_files) - set(expected_files))
    changed: List[str] = []
    for path_key in sorted(set(expected_files) & set(actual_files)):
        exp = expected_files[path_key]
        act = actual_files[path_key]
        if exp["sha256"] != act["sha256"] or exp["bytes"] != act["bytes"]:
            changed.append(path_key)

    if missing or added or changed:
        parts = []
        if missing:
            parts.append("missing=" + ",".join(missing[:12]))
        if added:
            parts.append("added=" + ",".join(added[:12]))
        if changed:
            parts.append("changed=" + ",".join(changed[:12]))
        raise BaselineError("Baseline mismatch: " + "; ".join(parts))

    actual_fp = manifest_fingerprint(list(actual_files.values()))
    expected_fp = expected.get("root_fingerprint")
    if expected_fp and expected_fp != actual_fp:
        raise BaselineError("Baseline root_fingerprint mismatch")

    return {
        "file_count": len(actual_files),
        "root_fingerprint": actual_fp,
        "manifest": str(manifest_file),
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vault_root", nargs="?", default=".")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument(
        "--write-manifest",
        action="store_true",
        help="write an integrity manifest; --external keeps the write outside the vault",
    )
    modes.add_argument(
        "--check-manifest",
        metavar="MANIFEST_PATH",
        help="compare vault against an external frozen baseline",
    )
    parser.add_argument(
        "--external",
        metavar="PATH",
        help="with --write-manifest, write only this external path",
    )
    args = parser.parse_args(argv)
    root = Path(args.vault_root)
    try:
        if args.check_manifest:
            result = check_manifest(root, Path(args.check_manifest))
            print(
                "PASS baseline check: "
                f"{result['file_count']} files; fingerprint {result['root_fingerprint']}"
            )
            return 0
        if args.write_manifest:
            destination = Path(args.external) if args.external else None
            payload = write_manifest(root, destination)
            print(
                "PASS baseline freeze: "
                f"{payload['verification']['file_count']} files; "
                f"fingerprint {payload['root_fingerprint']}"
            )
            return 0
        # Default: freeze to stdout summary without writing (dry inventory)
        resolved = requested_root(root)
        payload = build_payload(resolved)
        print(
            "PASS baseline inventory: "
            f"{payload['verification']['file_count']} files; "
            f"fingerprint {payload['root_fingerprint']}"
        )
        return 0
    except BaselineError as error:
        print(f"HOLD baseline: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
