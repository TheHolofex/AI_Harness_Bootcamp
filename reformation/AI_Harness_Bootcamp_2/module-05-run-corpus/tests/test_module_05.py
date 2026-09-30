#!/usr/bin/env python3
"""Structural, semantic, and safety oracle for Module 5 Blue Gauge."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PASS: list[str] = []
FAIL: list[str] = []

OTHER_PRODUCTS = (
    "FIRST_RESULT", "MIN_SCREEN", "INTERNAL_ARTIFACT", "PO00_RESULT",
    "SOURCE_EVIDENCE", "DISCERNMENT_RESULT", "STANDING_RULE", "PO01_RESULT",
    "CONTEXT_MAP", "SOURCE_AS_DATA_CONTROL", "RELOAD_RESULT", "PO02_RESULT",
    "RELEASE_DECISION", "AUTHORITY_BOUNDARY", "COMPOSED_NEGATIVE", "REVOCATION_RESULT", "PO03_RESULT",
    "LOCALIZATION_RESULT", "RECOVERY_RESULT", "PO04_RESULT",
    "FIXED_BASELINE", "EXCEPTION_RULE", "DETERMINISTIC_DELTA", "CONFIG_ID", "RESTORE_ACTION", "PO06_RESULT",
    "PRE_RESULT_POLICY", "CHANGE_DECISION", "COST_PROXY", "RESTORED_BASELINE", "PO07_RESULT",
)
MODULE01_SOURCES = tuple(f"S0{n}_" for n in range(1, 10))
BANNED = ("246 kg", "1,404 kg", "3 minutes late", "20:50Z")
STAFF_PROMO_IDS = {2,5,9,12,16}


def check(cid: str, condition: bool, detail: str) -> None:
    (PASS if condition else FAIL).append(f"{cid}: {detail}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


ref = ROOT / "reference/REFERENCE.md"
hash_file = ROOT / "reference/REFERENCE.sha256"
expected_hash = read(hash_file).split()[0] if hash_file.exists() else ""
actual_hash = hashlib.sha256(ref.read_bytes()).hexdigest() if ref.exists() else ""
check("M5-REF", bool(expected_hash) and expected_hash == actual_hash, f"reference hash {actual_hash}")

required = {
    "start": ROOT / "README.md",
    "lab": ROOT / "shared/MODULE_05_LAB.md",
    "accessibility": ROOT / "shared/ACCESSIBILITY.md",
    "runbook": ROOT / "facilitator/RUNBOOK.md",
    "rubric": ROOT / "assessment/PUBLIC_RUBRIC.md",
    "custody": ROOT / "assessment/CUSTODY_CONTRACT.md",
    "spec": ROOT / "shared/controls/PREDICATE_SPEC.md",
    "predicate": ROOT / "shared/controls/predicate.py",
    "reference": ROOT / "reference/REFERENCE.md",
    "gauntlet": ROOT / "reference/GAUNTLET_PROMPT.md",
    "verdict": ROOT / "evidence/REVIEW_VERDICT.md",
}
corpus = ROOT / "shared/corpus"
runs = sorted(corpus.glob("R-*.md"))
check("M5-RUNS", len(runs) == 80, "corpus has eighty R- files")
sample = [corpus / f"R-{n:03d}.md" for n in range(1, 17)]
check("M5-RUNS", all(p.exists() for p in sample), "sample R-001 to R-016 present")
check("M5-RUNS", not (corpus / "run-missing.md").exists() and not any(p.name.startswith("run-") for p in corpus.iterdir()), "no old run-*.md names")

# No outcome headers or old first_failure in new raw notes
for p in sample:
    text = read(p)
    check("M5-HDR", "outcome:" not in text and "first_failure:" not in text, f"{p.name} is raw note without old headers")

pred = required["predicate"]

# Disposable configs and notes for cfg/substr tests. Use corpus for M5-PRED to keep mutation kill.
with tempfile.TemporaryDirectory() as tmpd:
    tmp = Path(tmpd)
    cfg = tmp / "predicate.json"
    cfg.write_text(json.dumps({"all_present": ["RELEASED", "source_status: RECEIVED"]}), encoding="utf-8")
    collision = tmp / "collision.txt"
    collision.write_text("UNRELEASED\nsource_status: RECEIVED\n", encoding="utf-8")
    lower = tmp / "lower.txt"
    lower.write_text("unreleased\nsource_status: received\n", encoding="utf-8")

    # M5-PRED uses real corpus files so the corpus mutation on R-002 kills M5-PRED
    promo = corpus / "R-002.md"
    non = corpus / "R-001.md"
    bad = subprocess.run([sys.executable, str(pred), str(promo), "--config", str(cfg)], capture_output=True, text=True)
    good = subprocess.run([sys.executable, str(pred), str(non), "--config", str(cfg)], capture_output=True, text=True)
    missing = subprocess.run([sys.executable, str(pred), str(tmp / "absent.txt"), "--config", str(cfg)], capture_output=True, text=True)
    missing_dir = subprocess.run([sys.executable, str(pred), str(tmp), "--config", str(cfg)], capture_output=True, text=True)

    check("M5-PRED", bad.returncode == 1 and "MATCH" in (bad.stdout + bad.stderr), "both literals exit 1 with MATCH")
    check("M5-PRED", good.returncode == 0 and "PASS" in (good.stdout + good.stderr), "absent literal exits 0 with PASS")
    check("M5-MISS", missing.returncode == 1 and "HOLD: missing input" in (missing.stdout + missing.stderr), "missing path exits 1 and prints HOLD: missing input")
    check("M5-MISS", missing_dir.returncode == 1 and "HOLD: missing input" in (missing_dir.stdout + missing_dir.stderr) and "MATCH" not in missing_dir.stdout, "directory path is missing input, not a match")

    def hold_cfg(name: str, body: str) -> None:
        path = tmp / name
        path.write_text(body, encoding="utf-8")
        result = subprocess.run([sys.executable, str(pred), str(non), "--config", str(path)], capture_output=True, text=True)
        text = result.stdout + result.stderr
        check("M5-CFG", result.returncode != 0 and "malformed config" in text.lower() and "MATCH" not in result.stdout, f"{name} holds as malformed config")

    hold_cfg("one.json", '{"all_present": ["a"]}')
    hold_cfg("empty-list.json", '{"all_present": []}')
    hold_cfg("empty-strings.json", '{"all_present": ["", "RELEASED"]}')
    hold_cfg("dup.json", '{"all_present": ["a", "a"]}')
    hold_cfg("three.json", '{"all_present": ["a", "b", "c"]}')
    hold_cfg("extra.json", '{"all_present": ["a", "b"], "extra": 1}')
    hold_cfg("not-json.json", "{")
    hold_cfg("blank.json", "   \n")
    check("M5-CFG", subprocess.run([sys.executable, str(pred), str(non), "--config", str(tmp / "no-config.json")], capture_output=True, text=True).returncode != 0, "missing config file is nonzero")

    unrun = subprocess.run([sys.executable, str(pred), str(collision), "--config", str(cfg)], capture_output=True, text=True)
    check("M5-SUBSTR", unrun.returncode == 1 and "MATCH" in unrun.stdout, "RELEASED matches inside UNRELEASED when the other literal is present")
    lowrun = subprocess.run([sys.executable, str(pred), str(lower), "--config", str(cfg)], capture_output=True, text=True)
    check("M5-SUBSTR", lowrun.returncode == 0 and "PASS" in lowrun.stdout, "lowercase released does not match RELEASED")
    corpus_hit = subprocess.run([sys.executable, str(pred), str(corpus / "R-052.md"), "--config", str(cfg)], capture_output=True, text=True)
    check("M5-SUBSTR", corpus_hit.returncode == 1 and "MATCH" in corpus_hit.stdout, "corpus collision note matches RELEASED as a substring")

# no wording pins on spec content; only existence and behavior above

# literal not leaked in learner files
learner_files = [required[k] for k in ("start", "lab", "accessibility", "rubric", "spec")] + list(sample)
learner_text = "\n".join(read(p) for p in learner_files)
shared_and_start = "\n".join(read(p) for p in [required["start"], required["rubric"]] + list((ROOT / "shared").rglob("*.md")))

check("M5-SECOND", "def run" not in learner_text, "learner files omit a second predicate implementation")
extra_py = [p for p in (ROOT / "shared").rglob("*.py") if p.resolve() != pred.resolve()]
check("M5-SECOND", extra_py == [], "no second python checker in shared/")

for token in MODULE01_SOURCES:
    check("M5-INDEP", token not in learner_text, f"learner files omit {token}")
for token in OTHER_PRODUCTS:
    check("M5-INDEP", token not in learner_text, f"learner files omit {token}")
for token in BANNED:
    check("M5-BAN", token not in shared_and_start, f"learner scan omits {token}")
for token in ("VERIFY:", "CUSTODY:", "PO0"):
    check("M5-TOKEN", token not in shared_and_start, f"learner scan omits {token}")


# Classify ALL 16 sample; verify exactly the 5 IDs and no extras
matches = 0
matched_ids = []
for n in range(1, 17):
    t = read(corpus / f"R-{n:03d}.md")
    if "RELEASED" in t and "source_status: RECEIVED" in t:
        matches += 1
        matched_ids.append(n)
check("M5-PROMO", matches == 5, f"exactly five promotions in all 16 sample (got {matches})")
check("M5-PROMO", set(matched_ids) == STAFF_PROMO_IDS, f"exact promotion IDs {STAFF_PROMO_IDS} (got {matched_ids})")

print(f"PASS {len(PASS)}")
for item in PASS:
    print("  PASS", item)
print(f"FAIL {len(FAIL)}")
for item in FAIL:
    print("  FAIL", item)
sys.exit(1 if FAIL else 0)
