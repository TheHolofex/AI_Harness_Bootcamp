#!/usr/bin/env python3
"""Mutation corpus: each item must make test_module_06.py FAIL its named cid."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class Mutation:
    cid: str
    what: str
    apply: Callable[[Path], None]


def append(rel: str, text: str) -> Callable[[Path], None]:
    def go(root: Path) -> None:
        p = root / rel
        p.write_text(p.read_text(encoding="utf-8") + text, encoding="utf-8")
    return go


def sub(rel: str, pattern: str, repl: str, required: bool = True, count: int = 0) -> Callable[[Path], None]:
    def go(root: Path) -> None:
        p = root / rel
        text = p.read_text(encoding="utf-8")
        new, n = re.subn(pattern, repl, text, count=count, flags=re.M)
        if required and n == 0:
            raise AssertionError(f"mutation anchor {pattern!r} not found in {rel}")
        p.write_text(new, encoding="utf-8")
    return go



def flip_ref_hash(root: Path) -> None:
    p = root / "reference/REFERENCE.sha256"
    text = p.read_text(encoding="utf-8")
    if not text or text[0] not in "0123456789abcdefABCDEF":
        raise AssertionError("REFERENCE.sha256 missing a leading hex digit")
    flipped = format(int(text[0], 16) ^ 0xF, "x")
    if text[0].isupper():
        flipped = flipped.upper()
    p.write_text(flipped + text[1:], encoding="utf-8")

def allow_overwrite(root: Path) -> None:
    """Disable every refusal that keeps an existing output from being replaced."""
    path = root / "shared/workflow/route.py"
    text = path.read_text(encoding="utf-8")
    exists = "if os.path.lexists(str(path)):"
    exclusive = "os.O_CREAT | os.O_EXCL | os.O_WRONLY"
    if exists not in text or exclusive not in text:
        raise AssertionError("overwrite guards not found in shared/workflow/route.py")
    text = text.replace(exists, "if False:", 1)
    text = text.replace(exclusive, "os.O_CREAT | os.O_WRONLY | os.O_TRUNC", 1)
    path.write_text(text, encoding="utf-8")





MUTATIONS: list[Mutation] = [
    Mutation("M6-REF", "flip first hex digit of REFERENCE.sha256", flip_ref_hash),
    Mutation("M6-WAVE", "remove a pending lot from wave1",
             sub("shared/batch/wave1.csv", r"LW-12,PENDING,.*\n", "")),
    Mutation("M6-BASE", "break baseline route so AUTHORIZED is hold",
             sub("shared/workflow/route.py", r'return "pass", "READY"', 'return "hold", "OPEN"')),
    Mutation("M6-CHG", "break changed rule handling",
             sub("shared/workflow/route.py", r"NOT_AUTHORIZED", "IGNORED")),
    Mutation("M6-DELTA", "make a non-pending row also differ under policy change",
             sub("shared/workflow/route.py", r'if permit == "PENDING":', 'if True:')),
    Mutation("M6-REPAIR", "overwrite an existing output", allow_overwrite),
    Mutation("M6-HOLD", "make bad rule succeed and write",
             sub("shared/workflow/route.py", r'raise Hold\("HOLD: pending_status unknown"\)', 'pass')),
    Mutation("M6-RESTORE", "skip the restore write",
             sub("scripts/restore_rule.py", r"active\.write_bytes\(baseline_bytes\)", "pass")),
    Mutation("M6-STRETCH", "remove a new pending from stretch file",
             sub("shared/batch/wave2-revised.csv", r"LW-44,PENDING,.*\n", "")),
    Mutation("M6-INDEP", "leak S07_ into README.md", append("README.md", "\nS07_\n")),
    Mutation("M6-BAN", "leak 246 kg into README.md", append("README.md", "\n246 kg\n")),
    Mutation("M6-TOKEN", "leak VERIFY: into README.md", append("README.md", "\nVERIFY:\n")),
]
