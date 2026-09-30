#!/usr/bin/env python3
"""Behavioral oracle for Module 06: fixed workflow with one-rule delta and restore."""

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


def check(cid: str, condition: bool, detail: str) -> None:
    (PASS if condition else FAIL).append(f"{cid}: {detail}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def read_bytes(path: Path) -> bytes:
    return path.read_bytes() if path.exists() else b""


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(cwd))


# Required files map (used for wave/stretch/REF/leakage scans)
required = {
    "start": ROOT / "README.md",
    "lab": ROOT / "shared/MODULE_06_LAB.md",
    "accessibility": ROOT / "shared/ACCESSIBILITY.md",
    "runbook": ROOT / "facilitator/RUNBOOK.md",
    "rubric": ROOT / "assessment/PUBLIC_RUBRIC.md",
    "custody": ROOT / "assessment/CUSTODY_CONTRACT.md",
    "wave1": ROOT / "shared/batch/wave1.csv",
    "wave2": ROOT / "shared/batch/wave2.csv",
    "wave2rev": ROOT / "shared/batch/wave2-revised.csv",
    "baseline_rule": ROOT / "shared/baseline/RULE.md",
    "baseline_digest": ROOT / "shared/baseline/RULE.md.sha256",
    "router": ROOT / "shared/workflow/route.py",
    "restore": ROOT / "scripts/restore_rule.py",
    "reference": ROOT / "reference/REFERENCE.md",
    "gauntlet": ROOT / "reference/GAUNTLET_PROMPT.md",
}

# Reference hash still valid (contract integrity)
ref = required["reference"]
hash_file = ROOT / "reference/REFERENCE.sha256"
expected_hash = read(hash_file).split()[0] if hash_file.exists() else ""
actual_hash = hashlib.sha256(ref.read_bytes()).hexdigest() if ref.exists() else ""
check("M6-REF", bool(expected_hash) and expected_hash == actual_hash, f"reference hash {actual_hash}")


w1_text = read(required["wave1"])
w1_lines = [ln for ln in w1_text.splitlines() if ln.startswith("LW-")]
check("M6-WAVE", len(w1_lines) == 80, "wave1 has 80 lots")
check("M6-WAVE", "LW-12,PENDING," in w1_text and "LW-28,PENDING," in w1_text and "LW-41,PENDING," in w1_text, "three pending present")
check("M6-WAVE", "RACK_CONFLICT" in w1_text, "rack conflict present")
check("M6-WAVE", "WITHDRAWN" in w1_text, "cancelled WITHDRAWN present")

# Wave2 has same permit/exc for routing identity
w2_text = read(required["wave2"])
check("M6-WAVE", "CHANGED" in w2_text, "wave2 uses changed disposition for non-key")
# but key permits same
for ln in ["LW-12,PENDING,", "LW-19,AUTHORIZED,", "LW-55,PENDING,"]:
    check("M6-WAVE", ln in w1_text and ln in w2_text, f"key permit same in w1 w2: {ln}")

# Stretch changes predicate set
w2r_text = read(required["wave2rev"])
check("M6-STRETCH", "LW-12,AUTHORIZED," in w2r_text, "stretch moves LW-12 out of pending")
check("M6-STRETCH", "LW-44,PENDING," in w2r_text and "LW-60,PENDING," in w2r_text, "stretch adds two new pending")

# No banned cross-module tokens, no answer leaks -- scans use the tested clone's files (ROOT under copy in adequacy)
MODULE01_SOURCES = tuple(f"S0{n}_" for n in range(1, 10))
OTHER_PRODUCTS = (
    "FIRST_RESULT", "MIN_SCREEN", "INTERNAL_ARTIFACT", "PO00_RESULT",
    "SOURCE_EVIDENCE", "DISCERNMENT_RESULT", "STANDING_RULE", "PO01_RESULT",
    "CONTEXT_MAP", "SOURCE_AS_DATA_CONTROL", "RELOAD_RESULT", "PO02_RESULT",
    "RELEASE_DECISION", "AUTHORITY_BOUNDARY", "COMPOSED_NEGATIVE", "REVOCATION_RESULT", "PO03_RESULT",
    "LOCALIZATION_RESULT", "RECOVERY_RESULT", "PO04_RESULT",
    "SAMPLE_MANIFEST", "PREDICATE_SPEC", "PROTECTED_CONTROL_RESULT", "PO05_RESULT",
    "PRE_RESULT_POLICY", "CHANGE_DECISION", "COST_PROXY", "RESTORED_BASELINE", "PO07_RESULT",
    "RUNNABLE_PACKAGE", "PO08_RESULT", "QUALIFICATION_RESULT",
)
BANNED = ("246 kg", "1,404 kg", "3 minutes late")
learner_files = [required[k] for k in ("start", "lab", "accessibility", "rubric")]
learner_text = "\n".join(read(p) for p in learner_files)
shared_and_start = "\n".join(
    read(p) for p in [required["start"], required["rubric"]] + list((ROOT / "shared").rglob("*.md"))
)
for token in MODULE01_SOURCES:
    check("M6-INDEP", token not in learner_text, f"learner files omit {token}")
for token in OTHER_PRODUCTS:
    check("M6-INDEP", token not in learner_text, f"learner files omit {token}")
for token in BANNED:
    check("M6-BAN", token not in shared_and_start, f"learner scan omits {token}")
for token in ("VERIFY:", "CUSTODY:", "PO0"):
    check("M6-TOKEN", token not in shared_and_start, f"learner scan omits {token}")

# Now behavioral runs in disposable copies
with tempfile.TemporaryDirectory() as tmp:
    work = Path(tmp) / "work"
    shutil.copytree(ROOT / "shared", work / "shared")
    (work / "scripts").mkdir()
    shutil.copyfile(ROOT / "scripts" / "restore_rule.py", work / "scripts" / "restore_rule.py")
    (work / "out").mkdir()

    router = work / "shared" / "workflow" / "route.py"
    restore = work / "scripts" / "restore_rule.py"
    w1 = work / "shared" / "batch" / "wave1.csv"
    w2 = work / "shared" / "batch" / "wave2.csv"
    w2r = work / "shared" / "batch" / "wave2-revised.csv"
    baseline_r = work / "shared" / "baseline" / "RULE.md"
    active_r = work / "shared" / "workflow" / "RULE.md"
    out1 = work / "out" / "wave1-base.csv"
    out2 = work / "out" / "wave2-base.csv"
    out1c = work / "out" / "wave1-chg.csv"
    out2c = work / "out" / "wave2-chg.csv"
    outstr = work / "out" / "stretch.csv"

    # Baseline run both waves -> byte identical receipts (only routing fields matter)
    r1 = run([sys.executable, str(router), str(w1), str(out1)], work)
    r2 = run([sys.executable, str(router), str(w2), str(out2)], work)
    check("M6-BASE", r1.returncode == 0 and r2.returncode == 0, "baseline runs succeed")
    check("M6-BASE", read_bytes(out1) == read_bytes(out2), "wave1 and wave2 baseline receipts byte-identical")

    # Key behaviors in baseline
    base_text = read(out1)
    check("M6-BASE", "LW-01,pass,READY" in base_text, "authorized -> pass READY")
    check("M6-BASE", "LW-12,hold,OPEN" in base_text and "LW-28,hold,OPEN" in base_text and "LW-41,hold,OPEN" in base_text, "pending -> hold OPEN")
    check("M6-BASE", "LW-19,hold,RESOURCE_CONFLICT" in base_text and "LW-55,hold,RESOURCE_CONFLICT" in base_text, "rack first -> RESOURCE_CONFLICT")
    check("M6-BASE", "LW-08,hold,OPEN" in base_text, "cancelled/witdrawn -> hold OPEN")
    check("M6-BASE", "LW-02,hold,OPEN" in base_text, "near-miss lowercase pending -> hold OPEN")
    check("M6-BASE", "LW-20,hold,OPEN" in base_text, "case mismatch -> hold OPEN")

    # Change rule to NOT_AUTHORIZED, rerun -> only the three pending change; rack unchanged
    active_r.write_text("pending_status: NOT_AUTHORIZED\n", encoding="utf-8")
    rc1 = run([sys.executable, str(router), str(w1), str(out1c)], work)
    rc2 = run([sys.executable, str(router), str(w2), str(out2c)], work)
    check("M6-CHG", rc1.returncode == 0 and rc2.returncode == 0, "changed rule runs")
    chg_text = read(out1c)
    check("M6-CHG", "LW-12,reject,NOT_AUTHORIZED" in chg_text and "LW-28,reject,NOT_AUTHORIZED" in chg_text and "LW-41,reject,NOT_AUTHORIZED" in chg_text, "pending become reject NOT_AUTHORIZED")
    check("M6-CHG", "LW-19,hold,RESOURCE_CONFLICT" in chg_text, "rack still RESOURCE even under changed rule")
    # byte diff only the three
    base_lines = {ln for ln in base_text.splitlines() if ln.startswith("LW-")}
    chg_lines = {ln for ln in chg_text.splitlines() if ln.startswith("LW-")}
    pending_lots = {"LW-12", "LW-28", "LW-41"}
    only_pending_diff = all(
        (ln.split(",")[0] in pending_lots) == (ln not in base_lines)
        for ln in chg_lines if ln not in base_lines or ln.split(",")[0] in pending_lots
    )
    check("M6-DELTA", len([l for l in chg_lines if l not in base_lines]) == 3, "exactly 3 rows differ")
    check("M6-DELTA", "LW-55,hold,RESOURCE_CONFLICT" in chg_text, "LW-55 rack unchanged by policy")

    # Existing output refused
    r_dup = run([sys.executable, str(router), str(w1), str(out1c)], work)
    check("M6-REPAIR", r_dup.returncode != 0 and "output exists" in (r_dup.stderr or ""), "existing output refused")

    # dangling symlink output refused (lexists catches symlinks too)
    sym = work / "out" / "dangle.csv"
    sym.symlink_to(str(work / "no-such-target"))
    r_dangle = run([sys.executable, str(router), str(w1), str(sym)], work)
    check("M6-REPAIR", r_dangle.returncode != 0 and "output exists" in (r_dangle.stderr or ""), "dangling symlink output refused")


    # Bad config holds, no output created
    bad_rule = work / "out" / "bad.rule"
    bad_rule.write_text("pending_status: FOO\n", encoding="utf-8")
    shutil.copyfile(bad_rule, active_r)
    bad_out = work / "out" / "bad.csv"
    r_bad = run([sys.executable, str(router), str(w1), str(bad_out)], work)
    check("M6-HOLD", r_bad.returncode != 0 and "HOLD" in (r_bad.stderr or ""), "bad pending_status holds")
    check("M6-HOLD", not bad_out.exists(), "no output on hold")

    # reset rule so input validation (not rule) is tested for extra cols
    active_r.write_text("pending_status: OPEN\n", encoding="utf-8")


    # extra CSV columns refused (header must match exactly)
    extra_in = work / "shared/batch/extra-col.csv"
    extra_in.write_text(
        "lot,permit,gate_window,input_disposition,resource_exception,extra\n"
        "LW-01,AUTHORIZED,09:10-10:00 MDT,UNCHANGED,,x\n",
        encoding="utf-8"
    )
    extra_out = work / "out" / "extra.csv"
    r_extra = run([sys.executable, str(router), str(extra_in), str(extra_out)], work)
    check("M6-HOLD", r_extra.returncode != 0 and "malformed input" in (r_extra.stderr or "").lower(), "extra CSV columns refused")


    # Restore: use workdir, from distinct baseline+digest
    # First put changed back? reset to changed, then restore
    active_r.write_text("pending_status: NOT_AUTHORIZED\n", encoding="utf-8")
    rs = run([sys.executable, str(restore), str(work)], work)
    check("M6-RESTORE", rs.returncode == 0 and "RESTORE OK" in rs.stdout, "restore prints RESTORE OK")
    # after restore, baseline receipts again
    rest_out = work / "out" / "restored.csv"
    rr = run([sys.executable, str(router), str(w1), str(rest_out)], work)
    check("M6-RESTORE", rr.returncode == 0 and read_bytes(rest_out) == read_bytes(out1), "restored receipts match baseline bytes")
    # baseline digest match check is inside restore

    # Modified baseline refused by digest
    bad_base = work / "shared" / "baseline" / "RULE.md"
    bad_base.write_text("pending_status: OPEN\njunk\n", encoding="utf-8")
    # recompute wrong digest to simulate tamper? but to test, corrupt digest
    bad_dig = work / "shared" / "baseline" / "RULE.md.sha256"
    bad_dig.write_text("deadbeef  shared/baseline/RULE.md\n", encoding="utf-8")
    rs_bad = run([sys.executable, str(restore), str(work)], work)
    check("M6-RESTORE", rs_bad.returncode != 0 and ("digest mismatch" in (rs_bad.stderr or "") or "malformed baseline digest" in (rs_bad.stderr or "")), "tampered baseline digest refused")

    # Stretch: run revised, only new pending set move, old ones do not
    # reset to NOT_AUTH
    active_r.write_text("pending_status: NOT_AUTHORIZED\n", encoding="utf-8")
    rs = run([sys.executable, str(router), str(w2r), str(outstr)], work)
    check("M6-STRETCH", rs.returncode == 0, "stretch wave runs")
    str_text = read(outstr)
    check("M6-STRETCH", "LW-44,reject,NOT_AUTHORIZED" in str_text and "LW-60,reject,NOT_AUTHORIZED" in str_text, "new pending rejected")
    check("M6-STRETCH", "LW-12,pass,READY" in str_text, "former pending now authorized passes")
    check("M6-STRETCH", "LW-19,hold,RESOURCE_CONFLICT" in str_text and "LW-55,hold,RESOURCE_CONFLICT" in str_text, "rack still held in stretch")
    # only the predicted delta: the membership change ones
    # (LW-12 no longer pending, 44+60 now are; others same as w2 under same rule)

    # Hand patch detection: alter a receipt, different from fresh run
    patch = work / "out" / "patch.csv"
    shutil.copyfile(out1, patch)
    txt = patch.read_text()
    patch.write_text(txt.replace("LW-01,pass,READY", "LW-01,hold,OPEN"), encoding="utf-8")
    fresh = work / "out" / "fresh.csv"
    run([sys.executable, str(router), str(w1), str(fresh)], work)
    check("M6-REPAIR", read_bytes(patch) != read_bytes(fresh), "hand-patched receipt differs from clean run")

print(f"PASS {len(PASS)}")
for item in PASS:
    print("  PASS", item)
print(f"FAIL {len(FAIL)}")
for item in FAIL:
    print("  FAIL", item)
sys.exit(1 if FAIL else 0)
