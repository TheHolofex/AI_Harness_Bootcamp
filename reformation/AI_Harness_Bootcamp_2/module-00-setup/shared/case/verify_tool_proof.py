#!/usr/bin/env python3
"""Check the three files the AI tools were asked to write.

Content alone is not evidence. `printf 'codex works' > from-codex.txt` produces a file
with the right bytes and proves nothing about whether a tool ran. So each proof file
must carry the run token this run issued, and must have been written after the token
existed. A file created before the token, or carrying a different token, is rejected.

What this proves: the file appeared during this run, after the token was issued.
What it does not prove: that a model rather than a person put it there. Nothing running
on your own machine can prove that, which is why it is not what decides your result.

Usage:  python3 verify_tool_proof.py <proof-dir> <token-file>
"""

from __future__ import annotations

import sys
from pathlib import Path

EXPECTED = {
    "from-codex.txt": "codex works",
    "from-opencode.txt": "opencode works",
    "from-goose.txt": "goose works",
}


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    token_file = Path(sys.argv[2]) if len(sys.argv) > 2 else root.parent / "run-token.txt"

    if not token_file.exists():
        print(f"HOLD: no run token at {token_file}")
        print("      Re-run the step that creates the token before the tool commands.")
        return 1
    token = token_file.read_text(encoding="utf-8").strip()
    issued = token_file.stat().st_mtime
    if not token:
        print(f"HOLD: the run token at {token_file} is empty")
        return 1

    failed = False
    for name, phrase in EXPECTED.items():
        path = root / name
        if not path.exists():
            print(f"FAIL: {name} — the tool reported success but no file exists here")
            failed = True
            continue

        observed = path.read_text(encoding="utf-8").strip()
        want = f"{phrase} {token}"
        if observed != want:
            if observed == phrase:
                print(f"FAIL: {name} — carries no run token, so it cannot be tied to this run")
            else:
                print(f"FAIL: {name} — content is {observed[:60]!r}; expected {want!r}")
            failed = True
            continue

        if path.stat().st_mtime < issued - 1:
            print(f"FAIL: {name} — written before this run's token was issued")
            failed = True
            continue

        print(f"PASS: {name} — correct content, this run's token")

    if failed:
        print("\nTOOL PROOF HOLD")
        return 1
    print("\nTOOL PROOF PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
