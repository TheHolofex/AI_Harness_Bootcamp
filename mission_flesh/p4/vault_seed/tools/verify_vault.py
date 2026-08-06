#!/usr/bin/env python3
"""P4 vault entrypoint: verify semantics, then write or check integrity."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Sequence

TOOLS = Path(__file__).resolve().parent


def _run(script_name: str, argv: Sequence[str]) -> int:
    script = TOOLS / script_name
    completed = subprocess.run([sys.executable, str(script), *argv], check=False)
    return int(completed.returncode)


def main(argv: Optional[Sequence[str]] = None) -> int:
    raw: List[str] = list(sys.argv[1:] if argv is None else argv)
    if raw and raw[0] in {"brain", "baseline"}:
        mode = raw.pop(0)
        if mode == "baseline":
            return _run("verify_baseline.py", raw)
        return _run("verify_brain.py", raw)
    if "--write-manifest" in raw:
        if "--external" not in raw:
            print(
                "HOLD baseline: P4 course snapshot creation requires --external PATH",
                file=sys.stderr,
            )
            return 1
        brain_args = [raw[0]] if raw and not raw[0].startswith("-") else []
        brain_result = _run("verify_brain.py", brain_args)
        if brain_result != 0:
            return brain_result
        return _run("verify_baseline.py", raw)
    if "--check-manifest" in raw:
        return _run("verify_baseline.py", raw)
    return _run("verify_brain.py", raw)


if __name__ == "__main__":
    raise SystemExit(main())
