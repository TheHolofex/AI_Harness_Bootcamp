#!/usr/bin/env python3
"""Mutation corpus: each item must make test_module_02.py FAIL its named cid."""

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



def flip_ref_hash(root: Path) -> None:
    p = root / "reference/REFERENCE.sha256"
    text = p.read_text(encoding="utf-8")
    if not text or text[0] not in "0123456789abcdefABCDEF":
        raise AssertionError("REFERENCE.sha256 missing a leading hex digit")
    flipped = format(int(text[0], 16) ^ 0xF, "x")
    if text[0].isupper():
        flipped = flipped.upper()
    p.write_text(flipped + text[1:], encoding="utf-8")



def neuter_guard(root: Path) -> None:
    p = root / "shared/case/guard.py"
    text = p.read_text(encoding="utf-8")
    new, n = re.subn(r"return 0 if ok else 1", "return 0", text)
    if n == 0:
        raise AssertionError("guard exit expression not found")
    p.write_text(new, encoding="utf-8")


MUTATIONS: list[Mutation] = [
    Mutation("M2-REF", "flip first hex digit of REFERENCE.sha256", flip_ref_hash),
    Mutation("M2-GUARD", "force screen to accept every file", neuter_guard),
    Mutation("M2-INDEP", "leak S07_ into README.md", append("README.md", "\nS07_\n")),
    Mutation("M2-BAN", "leak 246 kg into README.md", append("README.md", "\n246 kg\n")),
    Mutation("M2-TOKEN", "leak VERIFY: into README.md", append("README.md", "\nVERIFY:\n")),
]
