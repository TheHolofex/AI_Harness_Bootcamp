#!/usr/bin/env python3
"""Mutation corpus: each item must make test_module_04.py FAIL its named cid."""

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


MUTATIONS: list[Mutation] = [
    Mutation("M4-REF", "flip first hex digit of REFERENCE.sha256", flip_ref_hash),
    Mutation("M4-CARD", "change ledger row identity",
             sub("shared/case/ledger.json", r"BK-200", "BK-000")),
    Mutation("M4-CLEAN", "drop permit_status emission from the clean renderer",
             sub("scripts/render_review.py", r'if "permit_status" not in OMIT_FIELDS:\n        lines.append\(f"permit_status: \{permit\}"\)\n', "")),
    Mutation("M4-DROP", "break fault placement marker",
             sub("scripts/place_practice_fault.py", r'VARIANTS = \{"A": "permit_status", "B": "gate_time_mdt"\}', 'VARIANTS = {}')),
    Mutation("M4-RESTORE", "stop restore from replacing",
             sub("scripts/restore.py", r'os.replace\(temporary, renderer\)', "pass")),
    Mutation("M4-PROBE", "misclassify a dropped field as rendered",
             sub("scripts/probe_fields.py", r'return "renderer_omission"', 'return "rendered"')),
    Mutation("M4-VERSION", "ignore source revisions when comparing inputs",
             sub("scripts/probe_fields.py", r'identity_differs = selected_versions != intended_versions', 'identity_differs = selected != intended')),
    Mutation("M4-READ", "let malformed UTF-8 escape as a traceback",
             sub("scripts/probe_fields.py", r'except \(OSError, UnicodeError\) as error:', 'except OSError as error:')),
]
