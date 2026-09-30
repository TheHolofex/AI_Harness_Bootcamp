#!/usr/bin/env python3
"""Structural, semantic, and safety oracle for Module 2. Meaningful behavior only; incidental source Markdown link scans and bookkeeping removed per plan."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PASS: list[str] = []
FAIL: list[str] = []

OTHER_PRODUCTS = (
    "FIRST_RESULT",
    "MIN_SCREEN",
    "INTERNAL_ARTIFACT",
    "PO00_RESULT",
    "SOURCE_EVIDENCE",
    "DISCERNMENT_RESULT",
    "STANDING_RULE",
    "PO01_RESULT",
    "RELEASE_DECISION",
    "AUTHORITY_BOUNDARY",
    "COMPOSED_NEGATIVE",
    "REVOCATION_RESULT",
    "PO03_RESULT",
    "LOCALIZATION_RESULT",
    "RECOVERY_RESULT",
    "PO04_RESULT",
    "SAMPLE_MANIFEST",
    "PREDICATE_SPEC",
    "PROTECTED_CONTROL_RESULT",
    "PO05_RESULT",
    "FIXED_BASELINE",
    "EXCEPTION_RULE",
    "DETERMINISTIC_DELTA",
    "CONFIG_ID",
    "RESTORE_ACTION",
    "PO06_RESULT",
    "PRE_RESULT_POLICY",
    "CHANGE_DECISION",
    "COST_PROXY",
    "RESTORED_BASELINE",
    "PO07_RESULT",
)

MODULE01_SOURCES = tuple(f"S0{n}_" for n in range(1, 10))


def check(cid: str, condition: bool, detail: str) -> None:
    (PASS if condition else FAIL).append(f"{cid}: {detail}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


ref = ROOT / "reference/REFERENCE.md"
hash_file = ROOT / "reference/REFERENCE.sha256"
expected_hash = read(hash_file).split()[0] if hash_file.exists() else ""
actual_hash = hashlib.sha256(ref.read_bytes()).hexdigest() if ref.exists() else ""
check("M2-REF", bool(expected_hash) and expected_hash == actual_hash, f"reference hash {actual_hash}")


learner_files = [
    ROOT / "README.md",
    ROOT / "shared/MODULE_02_LAB.md",
    ROOT / "shared/ACCESSIBILITY.md",
    ROOT / "assessment/PUBLIC_RUBRIC.md",
    ROOT / "shared/case/REQUEST.md",
    ROOT / "shared/controls/SAVED_INSTRUCTION.md",
]
learner_text = "\n".join(read(path) for path in learner_files)
shared_and_start = "\n".join(
    read(path)
    for path in [ROOT / "README.md", ROOT / "assessment/PUBLIC_RUBRIC.md"]
    + list((ROOT / "shared").rglob("*.md"))
)

# Guard behavior: clean + all 3 hostile + missing (source integrity + negative)
clean = subprocess.run(
    [sys.executable, str(ROOT / "shared/case/guard.py"), str(ROOT / "shared/case/DN-003.md")],
    capture_output=True,
    text=True,
)
h1 = subprocess.run(
    [sys.executable, str(ROOT / "shared/case/guard.py"), str(ROOT / "shared/case/DN-014.md")],
    capture_output=True,
    text=True,
)
h2 = subprocess.run(
    [sys.executable, str(ROOT / "shared/case/guard.py"), str(ROOT / "shared/case/DN-015.md")],
    capture_output=True,
    text=True,
)
h3 = subprocess.run(
    [sys.executable, str(ROOT / "shared/case/guard.py"), str(ROOT / "shared/case/DN-016.md")],
    capture_output=True,
    text=True,
)
miss = subprocess.run(
    [sys.executable, str(ROOT / "shared/case/guard.py"), str(ROOT / "shared/case/DN-999.md")],
    capture_output=True,
    text=True,
)
check("M2-GUARD", clean.returncode == 0, "screen accepts clean note")
check("M2-GUARD", h1.returncode == 1 and "hostile-instruction" in (h1.stdout + h1.stderr), "screen rejects hostile DN-014")
check("M2-GUARD", h2.returncode == 1 and "hostile-instruction" in (h2.stdout + h2.stderr), "screen rejects hostile DN-015")
check("M2-GUARD", h3.returncode == 1 and "hostile-instruction" in (h3.stdout + h3.stderr), "screen rejects hostile DN-016")
check("M2-GUARD", miss.returncode == 1 and "HOLD: missing input" in (miss.stdout + miss.stderr), "screen missing input HOLD")

for token in MODULE01_SOURCES:
    check("M2-INDEP", token not in learner_text, f"learner files omit {token}")
for token in OTHER_PRODUCTS:
    check("M2-INDEP", token not in learner_text, f"learner files omit {token}")

for token in ("246 kg", "1,404 kg", "3 minutes late"):
    check("M2-BAN", token not in shared_and_start, f"learner scan omits {token}")
    for path in learner_files:
        check("M2-BAN", token not in read(path), f"no protected conclusion leaked in {path.name}")

for token in ("VERIFY:", "CUSTODY:", "PO0"):
    check("M2-TOKEN", token not in shared_and_start, f"learner scan omits {token}")


print(f"PASS {len(PASS)}")
for item in PASS:
    print("  PASS", item)
print(f"FAIL {len(FAIL)}")
for item in FAIL:
    print("  FAIL", item)
sys.exit(1 if FAIL else 0)
