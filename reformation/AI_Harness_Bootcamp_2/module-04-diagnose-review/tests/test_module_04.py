#!/usr/bin/env python3
"""Structural, semantic, and safety oracle for Module 4."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tempfile
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PASS: list[str] = []
FAIL: list[str] = []



def check(cid: str, condition: bool, detail: str) -> None:
    (PASS if condition else FAIL).append(f"{cid}: {detail}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


ref = ROOT / "reference/REFERENCE.md"
hash_file = ROOT / "reference/REFERENCE.sha256"
expected_hash = read(hash_file).split()[0] if hash_file.exists() else ""
actual_hash = hashlib.sha256(ref.read_bytes()).hexdigest() if ref.exists() else ""
check("M4-REF", bool(expected_hash) and expected_hash == actual_hash, f"reference hash {actual_hash}")

required = {
    "ledger": ROOT / "shared/case/ledger.json",
    "clean": ROOT / "scripts/render_review.py",
    "restore": ROOT / "scripts/restore.py",
    "place": ROOT / "scripts/place_practice_fault.py",
    "probe": ROOT / "scripts/probe_fields.py",
}

# M4-CARD: ledger volume and identity (no old thin values)
ledger = {}
try:
    ledger = json.loads(read(required["ledger"]))
except Exception:
    pass
check("M4-CARD", isinstance(ledger.get("rows"), list) and len(ledger["rows"]) == 80, "ledger 80 rows")
check("M4-CARD", any(r.get("row_id") == "BK-200" for r in ledger.get("rows", [])), "ledger has BK-200")
check("M4-CARD", ledger.get("clinic") == "Clinic F-9", "ledger clinic Clinic F-9")

with tempfile.TemporaryDirectory() as tmp:
    # clean render with explicit ledger (disposable)
    dest = Path(tmp) / "review.md"
    clean_run = subprocess.run(
        [sys.executable, str(required["clean"]), str(required["ledger"]), str(dest)],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    rendered = read(dest)
    check("M4-CLEAN", clean_run.returncode == 0, "clean renderer runs")
    check("M4-CLEAN", "permit_status" in rendered and "gate_time_mdt" in rendered, "clean renderer emits both fields")

    # drop via place on disposable W structure (source fixture not mock)
    w = Path(tmp) / "w"
    (w / "scripts").mkdir(parents=True)
    (w / "baseline").mkdir(parents=True)
    (w / "shared/case").mkdir(parents=True)
    (w / "out").mkdir()
    (w / "out/dummy.txt").write_text("x\n")
    clean_bytes = required["clean"].read_bytes()
    (w / "scripts/render_review.py").write_bytes(clean_bytes)
    (w / "baseline/render_review.py").write_bytes(clean_bytes)
    sha = hashlib.sha256(clean_bytes).hexdigest() + "\n"
    (w / "baseline/render_review.py.sha256").write_text(sha, encoding="utf-8")
    (w / "shared/case/ledger.json").write_bytes(required["ledger"].read_bytes())
    place_run = subprocess.run(
        [sys.executable, str(required["place"]), str(w), "--variant", "A"],
        capture_output=True,
        text=True,
    )
    check("M4-DROP", place_run.returncode == 0, "place runs")
    fault_dest = Path(tmp) / "fault.md"
    fault_run = subprocess.run(
        [sys.executable, str(w / "scripts/render_review.py"), str(w / "shared/case/ledger.json"), str(fault_dest)],
        capture_output=True,
        text=True,
        cwd=str(w),
    )
    fault_text = read(fault_dest)
    check("M4-DROP", fault_run.returncode == 0, "faulty work renderer runs")
    check("M4-DROP", "permit_status" not in fault_text, "faulty omits permit_status")
    # test B
    wB = Path(tmp) / "wB"
    (wB / "scripts").mkdir(parents=True)
    (wB / "baseline").mkdir(parents=True)
    (wB / "shared/case").mkdir(parents=True)
    (wB / "out").mkdir()
    (wB / "scripts/render_review.py").write_bytes(clean_bytes)
    (wB / "baseline/render_review.py").write_bytes(clean_bytes)
    (wB / "baseline/render_review.py.sha256").write_text(sha, encoding="utf-8")
    (wB / "shared/case/ledger.json").write_bytes(required["ledger"].read_bytes())
    placeB = subprocess.run([sys.executable, str(required["place"]), str(wB), "--variant", "B"], capture_output=True, text=True)
    check("M4-DROP", placeB.returncode == 0, "place B runs")
    destB = Path(tmp) / "faultB.md"
    runB = subprocess.run([sys.executable, str(wB / "scripts/render_review.py"), str(wB / "shared/case/ledger.json"), str(destB)], capture_output=True, text=True, cwd=str(wB))
    textB = read(destB)
    check("M4-DROP", runB.returncode == 0, "B renderer runs")
    check("M4-DROP", "gate_time_mdt" not in textB, "B omits gate")
    check("M4-DROP", "permit_status" in textB, "B keeps permit")
    # probe boundary tests (current rows, causes)
    probe_runA = subprocess.run(
        [sys.executable, str(required["probe"]), str(w / "shared/case/ledger.json"), "--review", str(fault_dest)],
        capture_output=True, text=True
    )
    poutA = probe_runA.stdout + probe_runA.stderr
    check("M4-PROBE", "renderer_omission" in poutA, "probe reports renderer_omission")
    check("M4-PROBE", "selected_source_ids" in poutA, "probe reports selected ids from classify")
    check("M4-PROBE", "review_present yes" in poutA, "probe reports review present")
    # source omission (stretch has empty on current; render would HOLD)
    stretch = ROOT / "shared/case/ledger-stretch.json"
    if stretch.exists():
        psrc = subprocess.run([sys.executable, str(required["probe"]), str(stretch)], capture_output=True, text=True)
        ps = psrc.stdout + psrc.stderr
        check("M4-PROBE", "source_omission" in ps, "probe reports source_omission on current empty")
    # wrong input version (stale vs intended identity)
    intendedp = ROOT / "shared/case/ledger-intended.json"
    stalep = ROOT / "shared/case/ledger-stale.json"
    if intendedp.exists() and stalep.exists():
        pver = subprocess.run([sys.executable, str(required["probe"]), str(stalep), "--intended", str(intendedp)], capture_output=True, text=True)
        pv = pver.stdout + pver.stderr
        check("M4-PROBE", "wrong_input_version" in pv, "probe reports wrong_input_version on selected identity diff")
        check("M4-PROBE", "intended_source_ids" in pv, "probe prints intended ids")
    # restore on disposable (state transition)
    bad = w / "scripts/render_review.py"
    bad.write_text("broken\n", encoding="utf-8")
    restore_run = subprocess.run(
        [sys.executable, str(required["restore"]), str(w)],
        capture_output=True,
        text=True,
    )
    check(
        "M4-RESTORE",
        restore_run.returncode == 0 and "RESTORE OK" in restore_run.stdout,
        "restore prints RESTORE OK",
    )
    check("M4-RESTORE", bad.read_bytes() == clean_bytes, "restore makes files identical")
    # tamper
    tw = Path(tmp)/"tw"
    for d in ["scripts","baseline","shared/case","out"]: (tw/d).mkdir(parents=True)
    (tw/"scripts/render_review.py").write_bytes(clean_bytes)
    (tw/"baseline/render_review.py").write_bytes(clean_bytes)
    (tw/"baseline/render_review.py.sha256").write_text("0"*64+"\n",encoding="utf-8")
    (tw/"shared/case/ledger.json").write_bytes(required["ledger"].read_bytes())
    trun = subprocess.run([sys.executable,str(required["place"]),str(tw),"--variant","A"],capture_output=True,text=True)
    check("M4-RESTORE",trun.returncode!=0,"tamper fails")
    check("M4-RESTORE","HOLD" in trun.stdout+trun.stderr,"tamper HOLD")
    # symlink
    sw = Path(tmp)/"sw"
    rs = Path(tmp)/"rs"
    rs.mkdir()
    (rs/"render_review.py").write_bytes(clean_bytes)
    for d in ["baseline","shared/case","out"]: (sw/d).mkdir(parents=True)
    (sw/"baseline/render_review.py").write_bytes(clean_bytes)
    (sw/"baseline/render_review.py.sha256").write_text(sha,encoding="utf-8")
    (sw/"shared/case/ledger.json").write_bytes(required["ledger"].read_bytes())
    os.symlink(str(rs), str(sw/"scripts"))
    srun = subprocess.run([sys.executable,str(required["restore"]),str(sw)],capture_output=True,text=True)
    check("M4-RESTORE",srun.returncode!=0,"symlink fails")
    check("M4-RESTORE","HOLD" in srun.stdout+srun.stderr,"symlink HOLD")

    later = json.loads(json.dumps(ledger))
    later["rows"][0]["source_revision"] = "2"
    later_path = Path(tmp) / "same-id-later-revision.json"
    later_path.write_text(json.dumps(later), encoding="utf-8")
    version_probe = subprocess.run(
        [sys.executable, str(required["probe"]), str(required["ledger"]), "--intended", str(later_path)],
        capture_output=True, text=True,
    )
    check("M4-VERSION", version_probe.returncode == 0 and version_probe.stdout.count("wrong_input_version") == 2,
          "a later revision under the same source ID is not mistaken for the intended input")
    unreadable = Path(tmp) / "unreadable-review.md"
    unreadable.write_bytes(b"\xff")
    unreadable_probe = subprocess.run(
        [sys.executable, str(required["probe"]), str(required["ledger"]), "--review", str(unreadable)],
        capture_output=True, text=True,
    )
    check("M4-READ", unreadable_probe.returncode == 1 and "HOLD:" in unreadable_probe.stderr
          and "Traceback" not in unreadable_probe.stderr, "an unreadable review holds without a false omission diagnosis")

print(f"PASS {len(PASS)}")
for item in PASS:
    print("  PASS", item)
print(f"FAIL {len(FAIL)}")
for item in FAIL:
    print("  FAIL", item)
sys.exit(1 if FAIL else 0)
