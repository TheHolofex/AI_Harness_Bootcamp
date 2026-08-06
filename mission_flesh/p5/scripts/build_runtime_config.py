#!/usr/bin/env python3
"""Build the deny-by-default OpenCode config used by the P5 exposed session."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

READ_ALLOWLIST = (
    "intake/**",
    "reference_corpus/**",
    "EXPECTED_INTAKE_FILES.json",
    "TRIAGE_CANDIDATE_SCHEMA.md",
)
WRITE_ALLOWLIST = ("out/triage_candidate.json",)


def build_config(disabled_mcp: list[str]) -> dict[str, Any]:
    """Return only keys accepted by the pinned OpenCode config schema."""
    read = {"*": "deny"}
    read.update({path: "allow" for path in READ_ALLOWLIST})
    edit = {"*": "deny"}
    edit.update({path: "allow" for path in WRITE_ALLOWLIST})
    return {
        "$schema": "https://opencode.ai/config.json",
        "mcp": {name: {"enabled": False} for name in sorted(set(disabled_mcp))},
        "permission": {
            "*": "deny",
            "read": read,
            "glob": "deny",
            "grep": "deny",
            "list": "deny",
            "edit": edit,
            "bash": "deny",
            "task": "deny",
            "skill": "deny",
            "webfetch": "deny",
            "websearch": "deny",
            "external_directory": "deny",
            "doom_loop": "deny",
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--staging-root", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument(
        "--disable-mcp",
        action="append",
        default=[],
        metavar="NAME",
        help="MCP server name discovered in the resolved config; may be repeated",
    )
    args = parser.parse_args(argv)

    staging = args.staging_root.expanduser().resolve()
    if not staging.is_dir():
        print(f"HOLD runtime config: staging root missing: {staging}", file=sys.stderr)
        return 1
    out_dir = args.out_dir.expanduser().resolve()
    try:
        out_dir.relative_to(staging)
    except ValueError:
        print("HOLD runtime config: out-dir must be inside staging", file=sys.stderr)
        return 1
    out_dir.mkdir(parents=True, exist_ok=True)

    config = build_config(args.disable_mcp)
    encoded = (json.dumps(config, indent=2) + "\n").encode("utf-8")
    config_path = out_dir / "opencode.json"
    config_path.write_bytes(encoded)
    digest = hashlib.sha256(encoded).hexdigest()
    (out_dir / "runtime_config.sha256").write_text(digest + "\n", encoding="utf-8")

    print(f"PASS runtime config: {config_path}")
    print(f"SHA256 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
