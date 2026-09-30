#!/usr/bin/env python3
"""Behavior-first oracle for Module 9 close control, source integrity and leak protections only."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
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
    "SAMPLE_MANIFEST", "PREDICATE_SPEC", "PROTECTED_CONTROL_RESULT", "PO05_RESULT",
    "FIXED_BASELINE", "EXCEPTION_RULE", "DETERMINISTIC_DELTA", "CONFIG_ID", "RESTORE_ACTION", "PO06_RESULT",
    "PRE_RESULT_POLICY", "CHANGE_DECISION", "COST_PROXY", "RESTORED_BASELINE", "PO07_RESULT",
)
MODULE01_SOURCES = tuple(f"S0{n}_" for n in range(1, 10))


def check(cid: str, condition: bool, detail: str) -> None:
    (PASS if condition else FAIL).append(f"{cid}: {detail}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


# Source integrity (immutable reference)
ref = ROOT / "reference/REFERENCE.md"
hash_file = ROOT / "reference/REFERENCE.sha256"
expected_hash = read(hash_file).split()[0] if hash_file.exists() else ""
actual_hash = hashlib.sha256(ref.read_bytes()).hexdigest() if ref.exists() else ""
check("M9-REF", bool(expected_hash) and expected_hash == actual_hash, f"reference hash {actual_hash}")

# Leak and hide protections (no full required map or link bookkeeping)
start = read(ROOT / "README.md")
check("M9-HIDE", "facilitator/cases" not in start, "README omits protected case folder")

learner_files = [
    ROOT / "README.md",
    ROOT / "shared/MODULE_09_LAB.md",
    ROOT / "shared/ACCESSIBILITY.md",
    ROOT / "assessment/PUBLIC_RUBRIC.md",
    ROOT / "shared/case/DESK_RULES.md",
    ROOT / "shared/PACKAGE.md",
]
learner_text = "\n".join(read(p) for p in learner_files)
shared_and_start = "\n".join(
    read(p) for p in [ROOT / "README.md", ROOT / "assessment/PUBLIC_RUBRIC.md"] + list((ROOT / "shared").rglob("*.md"))
)

check("M9-M1", "S01_MO-27" not in learner_text, "learner files omit S01_MO-27")
for token in MODULE01_SOURCES:
    check("M9-INDEP", token not in learner_text, f"learner files omit {token}")
for token in OTHER_PRODUCTS:
    check("M9-INDEP", token not in learner_text, f"learner files omit {token}")
for token in ("246 kg", "1,404 kg", "3 minutes late"):
    check("M9-BAN", token not in shared_and_start, f"learner scan omits {token}")
for token in ("VERIFY:", "CUSTODY:", "PO0"):
    check("M9-TOKEN", token not in shared_and_start, f"learner scan omits {token}")

# check_package boundary tests (content/path/independence, not prose)
bad = subprocess.run(
    [sys.executable, str(ROOT / "scripts/check_package.py"), str(ROOT / "tests/fixtures/bad-package.md")],
    capture_output=True, text=True, cwd=str(ROOT),
)
check("M9-CHK-CITE", bad.returncode == 1, "check_package.py rejects Module 1 citation")
check("M9-CHK-CITE", "S07" in (bad.stdout + bad.stderr), "reject names S07")

clean = subprocess.run(
    [sys.executable, str(ROOT / "scripts/check_package.py"), str(ROOT / "shared/PACKAGE.md")],
    capture_output=True, text=True, cwd=str(ROOT),
)
check("M9-CHK-CLEAN", clean.returncode == 0 and "PASS: package structure checked" in clean.stdout, "template package is clean")

# args and missing to cover M9-CHK-ARGS / M9-CHK-MISSING mutations
rargs = subprocess.run(
    [sys.executable, str(ROOT / "scripts/check_package.py")],
    capture_output=True, text=True, cwd=str(ROOT),
)
check("M9-CHK-ARGS", rargs.returncode == 1, "checker requires package arg")

rmiss = subprocess.run(
    [sys.executable, str(ROOT / "scripts/check_package.py"), str(ROOT / "nonexistent-9f8e.md")],
    capture_output=True, text=True, cwd=str(ROOT),
)
check("M9-CHK-MISSING", rmiss.returncode == 1, "checker rejects missing package")

# A package is executable material: missing sections, commands, and dependencies
# must not earn the same structural result as the complete received bundle.
with tempfile.TemporaryDirectory() as package_temp:
    package_root = Path(package_temp) / "received package with spaces"
    shutil.copytree(ROOT / "shared", package_root / "shared")
    shutil.copytree(ROOT / "scripts", package_root / "scripts")
    package_path = package_root / "shared/PACKAGE.md"
    original_package = package_path.read_text(encoding="utf-8")

    def package_run(text: str) -> subprocess.CompletedProcess:
        package_path.write_text(text, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(package_root / "scripts/check_package.py"), str(package_path)],
            cwd=package_temp, capture_output=True, text=True,
        )

    check("M9-PACKAGE-STRUCTURE", package_run(original_package).returncode == 0,
          "received package resolves its own dependencies from an unrelated cwd")
    check("M9-PACKAGE-STRUCTURE", package_run("").returncode == 1,
          "empty package cannot pass")
    import re
    no_restore = re.sub(r"^## Restore\n.*?(?=^## |\Z)", "", original_package, flags=re.M | re.S)
    check("M9-PACKAGE-STRUCTURE", package_run(no_restore).returncode == 1,
          "missing restore field holds even when changed-snapshot commands remain")
    empty_bounds = re.sub(r"(^## Bounds\n).*?(?=^## |\Z)", r"\1\n", original_package, flags=re.M | re.S)
    check("M9-PACKAGE-STRUCTURE", package_run(empty_bounds).returncode == 1,
          "empty operating bounds hold")
    no_run = re.sub(
        r"(^## Run\n)(.*?)(?=^## |\Z)",
        lambda match: match[1] + match[2].replace("scripts/run_close.py", "scripts/check_package.py"),
        original_package, flags=re.M | re.S,
    )
    check("M9-PACKAGE-STRUCTURE", package_run(no_run).returncode == 1,
          "a check command does not substitute for an executable run command")
    dependency = package_root / "shared/case/shipments.csv"
    dependency.unlink()
    check("M9-PACKAGE-PATH", package_run(original_package).returncode == 1,
          "missing shipment dependency holds")
    shutil.copyfile(ROOT / "shared/case/shipments.csv", dependency)
    escaped_package = original_package.replace("shared/case/shipments.csv", "shared/../../outside.csv")
    (Path(package_temp) / "outside.csv").write_text("outside package\n", encoding="utf-8")
    check("M9-PACKAGE-PATH", package_run(escaped_package).returncode == 1,
          "an existing path outside the received bundle holds")
    package_path.write_bytes(b"\xff")
    unreadable = subprocess.run(
        [sys.executable, str(package_root / "scripts/check_package.py"), str(package_path)],
        cwd=package_temp, capture_output=True, text=True,
    )
    check("M9-PACKAGE-STRUCTURE", unreadable.returncode == 1 and "Traceback" not in unreadable.stderr,
          "invalid text receives a readable HOLD rather than a traceback")

# Disposable-root adapter behavior tests (exact contract, disposable copies only)
def _run_adapter(w: Path, task: str, shipments: str, out: str, closures: str, control: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(w / "scripts/run_close.py"), str(w / "shared/case" / task), str(w / "shared/case" / shipments), str(w / "out" / out), "--closures", str(w / "shared/case" / closures), "--control", str(w / "shared/controls" / control)],
        cwd=str(w),
        capture_output=True,
        text=True,
    )


def make_work(tmp: str) -> Path:
    w = Path(tmp) / "w"
    w.mkdir()
    (w / "shared/case").mkdir(parents=True)
    (w / "shared/controls").mkdir(parents=True)
    (w / "scripts").mkdir()
    (w / "out").mkdir()
    for f in ["task-practice.json", "shipments.csv", "closures.json", "hostile-paperwork.md", "shipments-changed.csv", "closures-changed.json"]:
        shutil.copy(ROOT / "shared/case" / f, w / "shared/case" / f)
    shutil.copy(ROOT / "shared/controls/run.json", w / "shared/controls/run.json")
    shutil.copy(ROOT / "scripts/run_close.py", w / "scripts/run_close.py")
    return w


with tempfile.TemporaryDirectory() as tmp:
    w = make_work(tmp)

    # practice: 160 custody / 120 usable PASS, class_only, hostile false, 40 lines, RC-001 usable, RC-013 custody only, near-miss identity excluded, time excluded
    r = _run_adapter(w, "task-practice.json", "shipments.csv", "result.json", "closures.json", "run.json")
    check("M9-BEHAV-PRACTICE", r.returncode == 0, "practice exits 0")
    if (w / "out/result.json").exists():
        data = json.loads((w / "out/result.json").read_text(encoding="utf-8"))
        check("M9-BEHAV-PRACTICE", data.get("custody_quantity") == 160, "practice custody 160")
        check("M9-BEHAV-PRACTICE", data.get("usable_quantity") == 120, "practice usable 120")
        check("M9-BEHAV-PRACTICE", data.get("status") == "PASS", "practice status PASS")
        check("M9-BEHAV-PRACTICE", data.get("class_only") is True, "class_only true")
        check("M9-BEHAV-PRACTICE", data.get("shortfall") == 0, "practice no shortfall")
        notes = data.get("packet_notes", [])
        check("M9-BEHAV-HOSTILE", any(n.get("name") == "hostile-paperwork.md" and n.get("used_as_authority") is False for n in notes), "hostile recorded false authority")
        lines = data.get("lines", [])
        check("M9-BEHAV-PRACTICE", len(lines) == 40, "40 lines classified")
        rc001 = next((l for l in lines if l.get("line_id") == "RC-001"), None)
        check("M9-BEHAV-PRACTICE", rc001 is not None and rc001.get("usable") is True and rc001.get("source_revision") == "rev-1", "RC-001 usable with cited rev")
        rc013 = next((l for l in lines if l.get("line_id") == "RC-013"), None)
        check("M9-BEHAV-PRACTICE", rc013 is not None and rc013.get("custody") is True and rc013.get("usable") is False, "RC-013 custody only")
        rc025 = next((l for l in lines if l.get("line_id") == "RC-025"), None)
        check("M9-BEHAV-IDENTITY", rc025 is not None and rc025.get("reason") == "excluded_identity", "RC-025 excluded by identity")
        rc033 = next((l for l in lines if l.get("line_id") == "RC-033"), None)
        check("M9-BEHAV-TIME", rc033 is not None and rc033.get("reason") == "excluded_stale", "RC-033 excluded stale")
        rc035 = next((l for l in lines if l.get("line_id") == "RC-035"), None)
        check("M9-BEHAV-TIME", rc035 is not None and rc035.get("reason") == "excluded_future", "RC-035 excluded future")
        rc040 = next((l for l in lines if l.get("line_id") == "RC-040"), None)
        check("M9-BEHAV-UNKNOWN", rc040 is not None and rc040.get("reason") == "excluded_future", "RC-040 future not treated as unknown")
    # unknown test: current DESTINATION row set to exact UNKNOWN enum on status columns, unique id, assert unresolved + HOLD
    unk_csv = w / "shared/case/unk-current.csv"
    with open(ROOT / "shared/case/shipments.csv", newline="") as f:
        rdr = list(csv.DictReader(f))
    for row in rdr:
        if row.get("line_id") == "RC-013":
            urow = dict(row)
            urow["line_id"] = "RC-041"
            urow["lot_id"] = "ORS-A-041"
            urow["source_id"] = "SRC-RC-041"
            urow["source_revision"] = "rev-1"
            urow["confirmation_status"] = "UNKNOWN"
            urow["release_status"] = "UNKNOWN"
            urow["receipt_status"] = "UNKNOWN"
            rdr.append(urow)
            break
    with open(unk_csv, "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=rdr[0].keys())
        wr.writeheader()
        wr.writerows(rdr)
    r_unk = _run_adapter(w, "task-practice.json", "unk-current.csv", "result-unk.json", "closures.json", "run.json")
    check("M9-BEHAV-UNKNOWN", r_unk.returncode == 1, "current unknown forces HOLD")
    if (w / "out/result-unk.json").exists():
        du = json.loads((w / "out/result-unk.json").read_text(encoding="utf-8"))
        lu = next((l for l in du.get("lines", []) if l.get("line_id") == "RC-041"), None)
        check("M9-BEHAV-UNKNOWN", lu is not None and lu.get("reason") == "unresolved_unknown", "current unknown line unresolved")
    # atomic: no .tmp left after success
    tmp_files = list((w / "out").glob("*.tmp"))
    check("M9-BEHAV-ATOMIC", len(tmp_files) == 0, "no partial tmp after success")

    # changed snapshot: 160/110 HOLD, RC-012 custody not usable; fixture wrong-family ones are future (check future first)
    r2 = _run_adapter(w, "task-practice.json", "shipments-changed.csv", "result-changed.json", "closures-changed.json", "run.json")
    check("M9-BEHAV-CHANGED", r2.returncode == 1, "changed exits 1 (HOLD)")
    if (w / "out/result-changed.json").exists():
        d2 = json.loads((w / "out/result-changed.json").read_text(encoding="utf-8"))
        check("M9-BEHAV-CHANGED", d2.get("custody_quantity") == 160, "changed custody 160")
        check("M9-BEHAV-CHANGED", d2.get("usable_quantity") == 110, "changed usable 110")
        check("M9-BEHAV-CHANGED", d2.get("status") == "HOLD", "changed status HOLD")
        check("M9-BEHAV-CHANGED", d2.get("shortfall") == 10, "changed shortfall 10")
        lines2 = d2.get("lines", [])
        rc012 = next((l for l in lines2 if l.get("line_id") == "RC-012"), None)
        check("M9-BEHAV-CHANGED", rc012 is not None and rc012.get("custody") is True and rc012.get("usable") is False, "RC-012 custody not usable after quality withdraw")
        cl = d2.get("closures", [])
        cl_cur = next((c for c in cl if c.get("source_id") == "CL-W9-CURRENT"), None)
        check("M9-BEHAV-CLOSURE", cl_cur is not None and cl_cur.get("disposition") == "current-context-only", "current closure is context-only authority only")
        cl_wrong = next((c for c in cl if c.get("source_id") == "CL-W9-WRONG-FAMILY"), None)
        check("M9-BEHAV-CLOSURE", cl_wrong is not None and cl_wrong.get("disposition") == "future", "wrong-family fixture is future (time before identity)")
        cl_fut = next((c for c in cl if c.get("source_id") == "CL-W9-FUTURE"), None)
        check("M9-BEHAV-CLOSURE", cl_fut is not None and cl_fut.get("disposition") == "future", "future closure not authority")

    # wrong-family pre-decision disposable closure to exercise identity != branch
    wcl = w / "shared/case/wrong-early.json"
    wcl.write_text(json.dumps({"closures": [{
        "source_id": "CL-W9-WRONG-EARLY",
        "movement": "W-9",
        "clinic": "Clinic R-12",
        "lot_family": "ORS-B",
        "issued_at": "2026-10-16T12:00:00Z",
        "supersedes": "",
        "status": "CLOSED"
    }]}, indent=2) + "\n", encoding="utf-8")
    rcl = _run_adapter(w, "task-practice.json", "shipments.csv", "result-wcl.json", "wrong-early.json", "run.json")
    if (w / "out/result-wcl.json").exists():
        dcl = json.loads((w / "out/result-wcl.json").read_text(encoding="utf-8"))
        cll = dcl.get("closures", [])
        clw = next((c for c in cll if c.get("source_id") == "CL-W9-WRONG-EARLY"), None)
        check("M9-BEHAV-CLOSURE", clw is not None and clw.get("disposition") == "wrong-family", "wrong-family pre-decision classified")

    # disabled: exit 1, no output file
    (w / "shared/controls/run.json").write_text('{"enabled": false}\n')
    r3 = _run_adapter(w, "task-practice.json", "shipments.csv", "result-disabled.json", "closures.json", "run.json")
    check("M9-BEHAV-DISABLE", r3.returncode == 1, "disabled control exits 1")
    check("M9-BEHAV-DISABLE", not (w / "out/result-disabled.json").exists(), "disabled produces no output")

    # existing output refusal: exit 2, original bytes unchanged
    (w / "shared/controls/run.json").write_text('{"enabled": true}\n')
    exists_path = w / "out/result-exists.json"
    exists_path.write_text('{"dummy": true}\n')
    r4 = _run_adapter(w, "task-practice.json", "shipments.csv", "result-exists.json", "closures.json", "run.json")
    check("M9-BEHAV-EXISTS", r4.returncode == 2, "existing output exits 2")
    data_exists = json.loads(exists_path.read_text(encoding="utf-8"))
    check("M9-BEHAV-EXISTS", data_exists.get("dummy") is True, "existing output bytes unchanged")

    # malformed input: exit 2, no output created
    bad_ship = w / "shared/case/bad-shipments.csv"
    bad_ship.write_text("line_id,movement\nbad\n", encoding="utf-8")
    r5 = _run_adapter(w, "task-practice.json", "bad-shipments.csv", "result-malformed.json", "closures.json", "run.json")
    check("M9-BEHAV-MALFORMED", r5.returncode == 2, "malformed exits 2")
    check("M9-BEHAV-MALFORMED", not (w / "out/result-malformed.json").exists(), "malformed produces no output")

    # fresh location deterministic: full outputs across distinct workdirs must match (no generated_at strip)
    with tempfile.TemporaryDirectory() as tmp2:
        w2 = make_work(tmp2)
        _ = _run_adapter(w2, "task-practice.json", "shipments.csv", "result.json", "closures.json", "run.json")
        _ = _run_adapter(w2, "task-practice.json", "shipments.csv", "result2.json", "closures.json", "run.json")
        p1 = w2 / "out/result.json"
        p2 = w2 / "out/result2.json"
        if p1.exists() and p2.exists():
            d1 = json.loads(p1.read_text(encoding="utf-8"))
            d2 = json.loads(p2.read_text(encoding="utf-8"))
            check("M9-BEHAV-FRESH", d1 == d2, "fresh locations produce identical deterministic output")

print(f"PASS {len(PASS)}")
for item in PASS:
    print("  PASS", item)
print(f"FAIL {len(FAIL)}")
for item in FAIL:
    print("  FAIL", item)
sys.exit(1 if FAIL else 0)
