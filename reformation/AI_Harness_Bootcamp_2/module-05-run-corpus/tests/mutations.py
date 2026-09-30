#!/usr/bin/env python3
"""Mutation corpus: each item must make test_module_05.py FAIL its named cid."""

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


def drop(rel: str) -> Callable[[Path], None]:
    def go(root: Path) -> None:
        (root / rel).unlink()

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


def widen_match(root: Path) -> None:
    p = root / "shared/controls/predicate.py"
    text = p.read_text(encoding="utf-8")
    old = "if first in text and second in text:"
    new = "if f' {first} ' in f' {text} ' and f' {second} ' in f' {text} ':"
    if old not in text:
        raise AssertionError("substring conjunction not found in predicate.py")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


def accept_malformed(root: Path) -> None:
    p = root / "shared/controls/predicate.py"
    text = p.read_text(encoding="utf-8")
    old = "HOLD: malformed config"
    if old not in text:
        raise AssertionError("malformed-config hold not found in predicate.py")
    p.write_text(text.replace(old, "accepted config"), encoding="utf-8")


def add_sixth_promotion(root: Path) -> None:
    p = root / "shared/corpus/R-003.md"
    p.write_text(p.read_text(encoding="utf-8") + "\nRELEASED\nsource_status: RECEIVED\n", encoding="utf-8")


LAB = "shared/MODULE_05_LAB.md"
RUBRIC = "assessment/PUBLIC_RUBRIC.md"

MUTATIONS: list[Mutation] = [
    Mutation("M5-REF", "flip first hex digit of REFERENCE.sha256", flip_ref_hash),
    Mutation("M5-RUNS", "delete R-016.md from sample", drop("shared/corpus/R-016.md")),
    Mutation("M5-HDR", "add forbidden outcome header to a sample run",
             append("shared/corpus/R-003.md", "\noutcome: fail\n")),
    Mutation("M5-PRED", "make a promo fail the match by removing one literal",
             sub("shared/corpus/R-002.md", r"RELEASED", "STAMPED")),
    Mutation("M5-MISS", "delete missing-input handling from predicate",
             sub("shared/controls/predicate.py", r"HOLD: missing input", "no hold")),
    Mutation("M5-CFG", "accept malformed configs instead of holding", accept_malformed),
    Mutation("M5-SUBSTR", "require spaces around literals so UNRELEASED hides RELEASED", widen_match),
    Mutation("M5-PROMO", "add a sixth sample promotion", add_sixth_promotion),
    Mutation("M5-SECOND", "add a second def run to the lab",
             append(LAB, "\ndef run(path):\n    return 0\n")),
    Mutation("M5-INDEP", "leak S07_ into README.md", append("README.md", "\nS07_\n")),
    Mutation("M5-BAN", "leak 246 kg into README.md", append("README.md", "\n246 kg\n")),
    Mutation("M5-TOKEN", "leak VERIFY: into README.md", append("README.md", "\nVERIFY:\n")),
]
