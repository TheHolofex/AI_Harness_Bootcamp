#!/usr/bin/env python3
"""Mutation corpus: each item must make test_module_01.py FAIL its named cid."""

from __future__ import annotations

import json
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


def drop_line_containing(rel: str, needle: str) -> Callable[[Path], None]:
    def go(root: Path) -> None:
        p = root / rel
        lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
        kept = [line for line in lines if needle not in line]
        if len(kept) == len(lines):
            raise AssertionError(f"{needle!r} not found in {rel}")
        p.write_text("".join(kept), encoding="utf-8")
    return go


def drop_sentence_containing(rel: str, needle: str) -> Callable[[Path], None]:
    def go(root: Path) -> None:
        p = root / rel
        text = p.read_text(encoding="utf-8")
        if needle not in text:
            raise AssertionError(f"{needle!r} not found in {rel}")
        new, n = re.subn(rf"[^.!?\n]*{re.escape(needle)}[^.!?]*[.!]?\s*", "", text)
        if n == 0:
            raise AssertionError(f"sentence containing {needle!r} not removed from {rel}")
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


def mutate_case_id(root: Path) -> None:
    p = root / "shared/case/SOURCE_MANIFEST.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["case_id"] = "MUTATED"
    p.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def drop_lab_link(root: Path) -> None:
    p = root / "README.md"
    text = p.read_text(encoding="utf-8")
    new, n = re.subn(r"\[[^\]]*\]\(shared/MODULE_01_LAB\.md\)", "", text)
    if n == 0:
        raise AssertionError("lab markdown link not found in README.md")
    p.write_text(new, encoding="utf-8")


LAB = "shared/MODULE_01_LAB.md"
RUBRIC = "assessment/PUBLIC_RUBRIC.md"

MUTATIONS: list[Mutation] = [
    Mutation("M1-REF", "flip first hex digit of REFERENCE.sha256", flip_ref_hash),
    Mutation("M1-01", "delete the Module 1 lab", drop(LAB)),
    Mutation("M1-LINK", "remove the start-page lab link", drop_lab_link),
    Mutation("M1-02", "set practice case_id to MUTATED", mutate_case_id),
    Mutation("M1-06", "delete the Requirement defined line",
             drop_line_containing(LAB, "Requirement defined")),
    Mutation("M1-08", "replace stop decomposing with keep expanding",
             sub(LAB, r"Stop decomposing|stop decomposing", "keep expanding")),
    Mutation("M1-16", "delete the independent-evidence sentence",
             drop_sentence_containing(LAB, "independent evidence")),
    Mutation("M1-19", "delete every freeze_baseline.py occurrence",
             sub(LAB, r"freeze_baseline\.py", "")),
    Mutation("M1-15", "delete SYSTEM OVERRIDE from S07",
             sub("shared/case/sources/S07_VENDOR_VX-240.md", r"SYSTEM OVERRIDE", "")),
    Mutation("M1-05", "leak PO-01 into README.md", append("README.md", "\nPO-01\n")),
    Mutation("M1-03", "add out-of-scope dispatch phrase to README.md",
             append("README.md", "\ndispatch a real\n")),
    Mutation("M1-18", "delete hard gate from the rubric",
             sub(RUBRIC, r"(?i)hard gate", "")),
    Mutation("M1-23", "delete the word practice from the rubric",
             sub(RUBRIC, r"(?i)practice", "")),
    Mutation("M1-26", "delete may not from the runbook",
             sub("facilitator/RUNBOOK.md", r"may not", "")),
    Mutation("M1-24", "delete HOLD/hold from accessibility",
             sub("shared/ACCESSIBILITY.md", r"HOLD|hold", "")),
    Mutation("M1-28", "delete coaching from the handoff",
             sub("shared/NEXT_MODULE.md", r"coaching", "")),
    Mutation("M1-07", "delete thread walk from the lab",
             sub(LAB, r"thread walk", "")),
    Mutation("M1-12", "delete claim defense and falsify from the lab",
             lambda root: (sub(LAB, r"claim defense", "")(root),
                           sub(LAB, r"falsify", "")(root))),
    Mutation("M1-14", "force scanned_kits to 0",
             sub("scripts/compute_thread.py",
                 r'"scanned_kits": scanned_totes \* kits_per_tote',
                 '"scanned_kits": 0')),
    Mutation("M1-CODE", "break start_work.py so py_compile fails",
             append("scripts/start_work.py", "\ndef (\n")),
    Mutation("M1-ANSWER", "leak 246 kg into README.md",
             append("README.md", "\n246 kg\n")),
]
