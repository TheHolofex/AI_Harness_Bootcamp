#!/usr/bin/env python3
"""Create a new Module 1 work folder without overwriting an existing attempt."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "shared/templates"
CASE = ROOT / "shared/case"
FILES = {
    "source-register.csv": TEMPLATES / "source-register.csv",
    "thread-ledger.csv": TEMPLATES / "thread-ledger.csv",
    "changed-thread-ledger.csv": TEMPLATES / "thread-ledger.csv",
}
MARKDOWN = [
    "challenge-matrix.md", "corrected-brief.md", "baseline-verdict.md",
    "change-prediction.md", "changed-brief.md", "changed-verdict.md", "handoff.md",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    destination = args.destination.expanduser().resolve()
    if destination.exists():
        print(f"HOLD: destination already exists: {destination}")
        return 1
    destination.mkdir(parents=True)
    for name, source in FILES.items():
        shutil.copyfile(source, destination / name)
    for name in MARKDOWN:
        (destination / name).write_text(f"# {name.removesuffix('.md').replace('-', ' ').title()}\n\n", encoding="utf-8")
    packet = destination / "case-packet"
    shutil.copytree(CASE, packet)
    print(f"PASS: created {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
