#!/usr/bin/env python3
"""P4 vault entrypoint: brain verify by default; optional baseline freeze/check."""

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
    if "--check-manifest" in raw or "--write-manifest" in raw:
        return _run("verify_baseline.py", raw)
    if raw and raw[0] in {"brain", "baseline"}:
        mode = raw.pop(0)
        if mode == "baseline":
            return _run("verify_baseline.py", raw)
        return _run("verify_brain.py", raw)
    return _run("verify_brain.py", raw)


if __name__ == "__main__":
    raise SystemExit(main())
