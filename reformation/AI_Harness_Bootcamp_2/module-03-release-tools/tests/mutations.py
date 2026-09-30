#!/usr/bin/env python3
"""Mutation corpus: each item must make test_module_03.py FAIL its named cid.

M3-PACKET (delete NB-NOTE-17 from REL-001) and M3-01 (delete a lab page) are
not in this catalog. Those mutants did not change hash, containment, revocation,
reference integrity, or cross-module leakage. Do not retarget them to new wording.
"""

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


def allow_any_path(root: Path) -> None:
    p = root / "shared/tools/hash_source.py"
    text = p.read_text(encoding="utf-8")
    new, n = re.subn(r"resolved\.relative_to\(root\)", "True", text)
    if n == 0:
        raise AssertionError("relative_to check not found")
    p.write_text(new, encoding="utf-8")
REQUIRED_COVERAGE = frozenset({
    "M3-REF",
    "M3-HASH",
    "M3-ESC",
    "M3-INDEP",
    "M3-BAN",
    "M3-TOKEN",
})

MUTATIONS: list[Mutation] = [
    Mutation("M3-REF", "flip first hex digit of REFERENCE.sha256", flip_ref_hash),
    Mutation("M3-HASH", "print a fake hash",
             sub("shared/tools/hash_source.py", r"digest = hashlib\.sha256\(resolved\.read_bytes\(\)\)\.hexdigest\(\)", 'digest = "0" * 64')),
    Mutation("M3-ESC", "allow any existing path", allow_any_path),
    Mutation("M3-INDEP", "leak S07_ into README.md", append("README.md", "\nS07_\n")),
    Mutation("M3-BAN", "leak 246 kg into README.md", append("README.md", "\n246 kg\n")),
    Mutation("M3-TOKEN", "leak VERIFY: into README.md", append("README.md", "\nVERIFY:\n")),
]