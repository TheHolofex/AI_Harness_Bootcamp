#!/usr/bin/env python3
"""Behavior and integrity checks; synthetic failures never count as live calls."""
from __future__ import annotations

import contextlib
import csv
import hashlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
FAILURES = []


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def command(script, *args):
    return subprocess.run([sys.executable, str(script), *map(str, args)], capture_output=True, text=True, env={**os.environ, "OPENROUTER_API_KEY": ""}, timeout=30)


def copied_work(base):
    work = base / "work with spaces"
    for name in ("cases", "controls", "baseline"):
        shutil.copytree(ROOT / "shared" / name, work / "shared" / name)
    (work / "scripts").mkdir()
    for name in ("restore_baseline.py", "evaluate_pairs.py"):
        shutil.copyfile(ROOT / "scripts" / name, work / "scripts" / name)
    return work


def reference():
    expected = (ROOT / "reference/REFERENCE.sha256").read_text().split()[0]
    assert digest(ROOT / "reference/REFERENCE.md") == expected


def evaluated_pairs():
    with tempfile.TemporaryDirectory() as temp:
        out = Path(temp) / "results.csv"
        result = command(ROOT / "scripts/evaluate_pairs.py", ROOT / "shared/cases", ROOT / "shared/controls/policy.json", out)
        assert result.returncode == 0, result.stderr
        with out.open(newline="") as stream:
            rows = list(csv.DictReader(stream))
        expected = {(f"PC-{number:02d}", variant) for number in range(1, 41) for variant in ("baseline", "candidate-a", "candidate-b")}
        assert len(rows) == len(expected) and {(row["case_id"], row["variant"]) for row in rows} == expected
        failures = {variant: set() for variant in ("baseline", "candidate-a", "candidate-b")}
        for row in rows:
            case = ROOT / "shared/cases" / row["case_id"]
            assert row["source_sha256"] == digest(case / "sources.json")
            assert row["brief_sha256"] == digest(case / f"{row['variant']}.md")
            assert row["config_sha256"] == digest(ROOT / "shared/controls" / f"{row['variant']}.json")
            if row["passed"] == "false":
                failures[row["variant"]].add(row["case_id"])
                assert row["reason"] == ("sourced_mass" if row["variant"] == "candidate-a" else "labeled_gate_time")
        assert failures == {"baseline": set(), "candidate-a": {"PC-03", "PC-11", "PC-27"}, "candidate-b": {"PC-02", "PC-14", "PC-35"}}
        before = out.read_bytes()
        again = command(ROOT / "scripts/evaluate_pairs.py", ROOT / "shared/cases", ROOT / "shared/controls/policy.json", out)
        assert again.returncode == 1 and out.read_bytes() == before


def malformed_and_cell_boundaries():
    with tempfile.TemporaryDirectory() as temp:
        case = Path(temp)
        shutil.copyfile(ROOT / "shared/cases/PC-01/sources.json", case / "sources.json")
        original = (ROOT / "shared/cases/PC-01/baseline.md").read_text()
        source = json.loads((case / "sources.json").read_text())
        examples = [
            original.replace(" | SB-PC-01#payload", ""),
            original.replace("2211 kg |", "2211 kg | extra |"),
            original + "This is released for dispatch.\n",
            original.replace("13:05 MDT", "13:05"),
            original.replace("SB-PC-01#payload", "SB-PC-01#payload-s14"),
            original.replace("# Slope Brief — PC-01", "# Slope Brief — PC-010"),
        ]
        # The title spelling is not the contract; change the actual ID wherever it appears.
        examples[-1] = original.replace("PC-01", "PC-010")
        for text in examples:
            (case / "brief.md").write_text(text)
            result = command(ROOT / "shared/controls/hard_gates.py", case / "brief.md")
            assert result.returncode == 1 and "HOLD" in result.stdout + result.stderr and "Traceback" not in result.stderr
        (case / "brief.md").write_text(original)
        source["sources"]["SB-PC-01#payload"]["text"] = "The stated mass is 12211 kg."
        (case / "sources.json").write_text(json.dumps(source))
        result = command(ROOT / "shared/controls/hard_gates.py", case / "brief.md")
        assert result.returncode == 1 and "sourced_mass" in result.stdout


def frozen_identity_refusal():
    with tempfile.TemporaryDirectory() as temp:
        work = copied_work(Path(temp))
        policy = work / "shared/controls/policy.json"
        value = json.loads(policy.read_text())
        value["config_sha256"]["baseline"] = "0" * 64
        policy.write_text(json.dumps(value))
        output = work / "out/bad.csv"
        result = command(work / "scripts/evaluate_pairs.py", work / "shared/cases", policy, output)
        assert result.returncode == 1 and not output.exists()


def source_errors_are_not_candidate_failures():
    for condition in ("malformed_source", "wrong_case", "malformed_candidate"):
        with tempfile.TemporaryDirectory() as temp:
            work = copied_work(Path(temp))
            case = work / "shared/cases/PC-01"
            if condition == "malformed_source":
                source = json.loads((case / "sources.json").read_text())
                source["sources"]["SB-PC-01#payload"]["authoritative"] = "true"
                (case / "sources.json").write_text(json.dumps(source))
            elif condition == "wrong_case":
                (case / "sources.json").write_bytes((work / "shared/cases/PC-02/sources.json").read_bytes())
            else:
                (case / "candidate-a.md").write_text("The candidate omitted the required table.\n")
            output = work / "out/results.csv"
            result = command(work / "scripts/evaluate_pairs.py", work / "shared/cases", work / "shared/controls/policy.json", output)
            if condition != "malformed_candidate":
                assert result.returncode == 1 and "HOLD:" in result.stderr and not output.exists(), result.stdout + result.stderr
                assert "Traceback" not in result.stderr
            else:
                assert result.returncode == 0, result.stderr
                with output.open(newline="") as stream:
                    rows = list(csv.DictReader(stream))
                failed = next(row for row in rows if row["case_id"] == "PC-01" and row["variant"] == "candidate-a")
                baseline = next(row for row in rows if row["case_id"] == "PC-01" and row["variant"] == "baseline")
                assert failed["format_ok"] == "false" and failed["reason"] == "format"
                assert baseline["passed"] == "true"


def restore_boundaries():
    with tempfile.TemporaryDirectory() as temp:
        work = copied_work(Path(temp))
        active = work / "shared/controls/active-instruction.md"
        baseline = work / "shared/cases/PC-01/baseline.md"
        candidate = work / "shared/cases/PC-03/candidate-a.md"
        candidate_before = candidate.read_bytes()
        active.write_text("changed instruction")
        baseline.write_text("changed baseline")
        result = command(work / "scripts/restore_baseline.py", work)
        assert result.returncode == 0, result.stderr
        hashes = json.loads((work / "shared/baseline/hashes.json").read_text())["files"]
        for name, expected in hashes.items():
            target = active if name == "active-instruction.md" else work / "shared/cases" / Path(name).stem / "baseline.md"
            assert digest(target) == expected
        assert candidate.read_bytes() == candidate_before
        frozen = work / "shared/baseline/active-instruction.md"
        frozen.write_text("tampered restore authority")
        before = active.read_bytes()
        result = command(work / "scripts/restore_baseline.py", work)
        assert result.returncode == 1 and active.read_bytes() == before and "HOLD" in result.stderr


def paid_batch_fail_closed():
    spec = importlib.util.spec_from_file_location("slope_test_batch", ROOT / "scripts/stretch_runner.py")
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    with tempfile.TemporaryDirectory() as temp:
        base = Path(temp)
        work = copied_work(base)
        destination = base / "comparison"
        result = command(ROOT / "scripts/stretch_runner.py", work, destination)
        assert result.returncode == 2 and "OPENROUTER_API_KEY unavailable" in result.stderr and not destination.exists()
        calls = []
        def failed_child(argv, **kwargs):
            calls.append(argv)
            child_work = Path(argv[argv.index("--workdir") + 1])
            (child_work / "brief.md").write_text("Incomplete file left by a failed child.")
            return subprocess.CompletedProcess(argv, 1, "HOLD: synthetic provider failure", "")
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "synthetic-test-only"}), patch.object(runner.subprocess, "run", side_effect=failed_child), contextlib.redirect_stdout(io.StringIO()):
            status = runner.main([str(work), str(destination)])
        report = json.loads((destination / "comparison.json").read_text())
        assert status == 1 and report["status"] == "HOLD" and report["recorded_attempts"] == 1 and len(calls) == 1
        assert (destination / "attempt-01/work/brief.md").read_text() == "Incomplete file left by a failed child."
        assert not (destination / "attempt-01/receipts").exists()
        assert report["checked_instruction_decision"] == "HOLD"


def no_answer_leakage():
    paths = [ROOT / "README.md", ROOT / "assessment/PUBLIC_RUBRIC.md", *list((ROOT / "shared").rglob("*.md"))]
    text = "\n".join(path.read_text() for path in paths)
    assert not any(value in text for value in ("246 kg", "1,404 kg", "3 minutes late", "S07_VENDOR_VX-240", "VERIFY:", "CUSTODY:"))


def main():
    tests = {"M7-REF": reference, "M7-EVAL": evaluated_pairs, "M7-GATE": malformed_and_cell_boundaries, "M7-FREEZE": frozen_identity_refusal, "M7-SOURCE": source_errors_are_not_candidate_failures, "M7-RESTORE": restore_boundaries, "M7-LIVE-HOLD": paid_batch_fail_closed, "M7-LEAK": no_answer_leakage}
    for identifier, test in tests.items():
        try:
            test()
        except Exception as error:
            FAILURES.append(identifier)
            print(f"FAIL {identifier}: {type(error).__name__}: {error}")
        else:
            print(f"PASS {identifier}: {test.__name__}")
    return bool(FAILURES)


if __name__ == "__main__":
    raise SystemExit(main())
