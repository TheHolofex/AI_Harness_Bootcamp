#!/usr/bin/env python3
"""Module 3 oracle: reference digest, hash and containment on a disposable copy, and cross-module answer leakage."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
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
    "CONTEXT_MAP",
    "SOURCE_AS_DATA_CONTROL",
    "RELOAD_RESULT",
    "PO02_RESULT",
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


def run_hash(script: Path, target: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), str(target)],
        capture_output=True,
        text=True,
    )


ref = ROOT / "reference/REFERENCE.md"
hash_file = ROOT / "reference/REFERENCE.sha256"
expected_hash = read(hash_file).split()[0] if hash_file.exists() else ""
actual_hash = hashlib.sha256(ref.read_bytes()).hexdigest() if ref.exists() else ""
check("M3-REF", bool(expected_hash) and expected_hash == actual_hash, f"reference hash {actual_hash}")

learner_files = [
    ROOT / "README.md",
    ROOT / "shared/MODULE_03_LAB.md",
    ROOT / "shared/ACCESSIBILITY.md",
    ROOT / "assessment/PUBLIC_RUBRIC.md",
    ROOT / "shared/case/REQUEST.md",
    ROOT / "shared/tools/COMPOSED_NEGATIVE.md",
]
learner_text = "\n".join(read(path) for path in learner_files)
shared_and_start = "\n".join(
    read(path)
    for path in [ROOT / "README.md", ROOT / "assessment/PUBLIC_RUBRIC.md"]
    + list((ROOT / "shared").rglob("*.md"))
)

# Hash, escape, and revocation run only inside a disposable tree. The tool's
# case root is the parent of the directory that contains the script, so the
# copy keeps shared/tools and shared/case. Nothing here renames or writes the
# module tree, a work folder, or the real home directory.
with tempfile.TemporaryDirectory(prefix="m03-hash-") as raw_tmp:
    tmp = Path(raw_tmp)
    tools = tmp / "shared" / "tools"
    case = tmp / "shared" / "case"
    tools.mkdir(parents=True)
    case.mkdir()
    script = tools / "hash_source.py"
    designated = case / "REL-001.md"
    shutil.copyfile(ROOT / "shared/tools/hash_source.py", script)
    shutil.copyfile(ROOT / "shared/case/REL-001.md", designated)
    outside = tmp / "outside-sentinel.txt"
    outside.write_text("outside\n", encoding="utf-8")
    sibling = tmp / "shared" / "case-extra" / "sentinel.txt"
    sibling.parent.mkdir()
    sibling.write_text("sibling\n", encoding="utf-8")

    hashed = hashlib.sha256(designated.read_bytes()).hexdigest()
    allowed = run_hash(script, designated)
    check(
        "M3-HASH",
        allowed.returncode == 0 and f"sha256 {hashed}" in allowed.stdout,
        "allowed hash of a temporary case file matches its bytes",
    )

    for label, target in (
        ("outside file", outside),
        ("sibling-prefix file", sibling),
        ("traversal path", case / ".." / ".." / outside.name),
    ):
        escaped = run_hash(script, target)
        text = escaped.stdout + escaped.stderr
        check(
            "M3-ESC",
            escaped.returncode == 1 and "HOLD: path not allowed" in text,
            f"{label} is denied",
        )

    revoked = tools / "hash_source.py.revoked"
    script.rename(revoked)
    after_revoke = run_hash(script, designated)
    check(
        "M3-HASH",
        (not script.exists()) and revoked.is_file() and after_revoke.returncode != 0,
        "renamed .revoked script is not runnable at the original path",
    )
    revoked.unlink()
    after_missing = run_hash(script, designated)
    check(
        "M3-HASH",
        (not script.exists()) and (not revoked.exists()) and after_missing.returncode != 0,
        "missing script is not a runnable capability",
    )

# Independence and answer-leak safety
for token in MODULE01_SOURCES:
    check("M3-INDEP", token not in learner_text, f"learner files omit {token}")
for token in OTHER_PRODUCTS:
    check("M3-INDEP", token not in learner_text, f"learner files omit {token}")

for token in ("246 kg", "1,404 kg", "3 minutes late"):
    check("M3-BAN", token not in shared_and_start, f"learner scan omits {token}")
    for path in learner_files:
        check("M3-BAN", token not in read(path), f"no protected conclusion leaked in {path.name}")

for token in ("VERIFY:", "CUSTODY:", "PO0"):
    check("M3-TOKEN", token not in shared_and_start, f"learner scan omits {token}")

print(f"PASS {len(PASS)}")
for item in PASS:
    print("  PASS", item)
print(f"FAIL {len(FAIL)}")
for item in FAIL:
    print("  FAIL", item)
sys.exit(1 if FAIL else 0)
