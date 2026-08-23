#!/usr/bin/env python3
"""End-to-end tests for the visible Module 1 practice workflow."""

from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
COLUMNS = [
    "step", "claim_id", "statement_type", "exact_entity", "entry_condition",
    "claim", "source_id", "source_version", "locator", "source_excerpt",
    "warrant", "calculation", "output_condition", "next_handoff",
    "uncertainty", "result",
]
STEPS = [
    "Requirement defined", "Cargo received", "Cargo released", "Vehicle made ready",
    "Movement authorized", "Route window met", "Cargo delivered", "Usable effect confirmed",
]
CHALLENGES = [
    "Warehouse receipt offered as proof of usable inventory",
    "Accepted-for-processing receipt offered as permit approval",
    "Archived route bulletin offered as current",
    "R-17 community page offered for R-71",
    "VX-240 note offered for VX-204",
    "Instruction embedded inside a source",
    "Producer confidence and self-review",
]


def run(script: str, *args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)], text=True, capture_output=True)


class WorkflowTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.work = Path(self.tmp.name) / "work"
        result = run("start_work.py", self.work)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write_ledger(self, path: Path, changed: bool = False, unrelated_delta: bool = False) -> None:
        rows = []
        for index, step in enumerate(STEPS, start=1):
            source = f"S{min(index, 6):02d}"
            version = "v6" if changed and step == "Route window met" else "v5" if step == "Route window met" else "current"
            claim = "North Gate closes at 21:20Z" if changed and step == "Route window met" else "North Gate closes at 20:50Z" if step == "Route window met" else f"{step} checked"
            if unrelated_delta and step == "Cargo received":
                claim = "Cargo received was changed without dependency"
            rows.append({
                "step": step,
                "claim_id": f"C{index:02d}",
                "statement_type": "SOURCE FACT",
                "exact_entity": "MO-27 / VX-204 / R-71 / H-17",
                "entry_condition": "prior step supported" if index > 1 else "request supplied",
                "claim": claim,
                "source_id": source,
                "source_version": version,
                "locator": "named section",
                "source_excerpt": claim,
                "warrant": "The applicable source states this exact condition.",
                "calculation": "none",
                "output_condition": "checked",
                "next_handoff": STEPS[index] if index < len(STEPS) else "human decision",
                "uncertainty": "delivery not yet observed" if index > 6 else "none",
                "result": "NOT YET OCCURRED" if index > 6 else "SUPPORTED",
            })

        # Six required practice calculations (lab section 5)
        gate_z = "21:20Z" if changed else "20:50Z"
        gate_mdt = "15:20 MDT" if changed else "14:50 MDT"
        gate_margin = "27 min" if changed else "-3 min"
        route_version = "v6" if changed else "v5"
        rows.extend([
            {"step": "Cargo received", "claim_id": "C09", "statement_type": "CALCULATION",
             "exact_entity": "scanned kit count", "entry_condition": "S02 tote scan",
             "claim": "216 scanned kits", "source_id": "S02", "source_version": "RCPT-8821",
             "locator": "tote and lot count", "source_excerpt": "12 totes scanned",
             "warrant": "Scanned count from warehouse receipt.",
             "calculation": "12 totes x 18 kits/tote = 216 kits",
             "output_condition": "scanned identity frozen", "next_handoff": "release decision",
             "uncertainty": "none", "result": "SUPPORTED"},
            {"step": "Cargo released", "claim_id": "C10", "statement_type": "CALCULATION",
             "exact_entity": "usable kit count", "entry_condition": "S03 QA release",
             "claim": "180 usable kits", "source_id": "S03", "source_version": "QA-661",
             "locator": "release count", "source_excerpt": "10 totes released",
             "warrant": "Released count from QA release.",
             "calculation": "10 released totes x 18 kits/tote = 180 kits",
             "output_condition": "usable count frozen", "next_handoff": "vehicle readiness",
             "uncertainty": "none", "result": "SUPPORTED"},
            {"step": "Vehicle made ready", "claim_id": "C11", "statement_type": "CALCULATION",
             "exact_entity": "mission payload mass", "entry_condition": "S04 rack requirement",
             "claim": "1404 kg mission payload", "source_id": "S04", "source_version": "r7",
             "locator": "rack mass", "source_excerpt": "84 kg required rack",
             "warrant": "Released mass plus required rack from fleet spec.",
             "calculation": "1320 kg released mass + 84 kg rack = 1404 kg",
             "output_condition": "payload within limit", "next_handoff": "authorization",
             "uncertainty": "none", "result": "SUPPORTED"},
            {"step": "Vehicle made ready", "claim_id": "C12", "statement_type": "CALCULATION",
             "exact_entity": "payload margin", "entry_condition": "S04 payload limit",
             "claim": "246 kg margin; 18 kg overage if all scanned loaded",
             "source_id": "S04", "source_version": "r7",
             "locator": "payload limit", "source_excerpt": "1650 kg limit",
             "warrant": "Limit from fleet spec.",
             "calculation": "1650 - 1404 = 246 kg margin; 1668 - 1650 = 18 kg overage",
             "output_condition": "margin positive", "next_handoff": "authorization",
             "uncertainty": "none", "result": "SUPPORTED"},
            {"step": "Route window met", "claim_id": "C13", "statement_type": "CALCULATION",
             "exact_entity": "gate closure and margin", "entry_condition": "S05 route bulletin",
             "claim": f"Gate closes {gate_mdt}; margin {gate_margin}",
             "source_id": "S05", "source_version": route_version,
             "locator": "North Gate closure", "source_excerpt": f"North Gate closes {gate_z}",
             "warrant": "Closure time from current route bulletin.",
             "calculation": f"{gate_z} - 6 h = {gate_mdt}; {gate_z} - 14:53Z = {gate_margin}",
             "output_condition": "gate open on arrival" if changed else "gate closed before arrival",
             "next_handoff": "delivery", "uncertainty": "none" if changed else "gate already closed",
             "result": "SUPPORTED"},
            {"step": "Route window met", "claim_id": "C14", "statement_type": "CALCULATION",
             "exact_entity": "travel schedule", "entry_condition": "S01 step durations",
             "claim": "Depart 14:25, gate 14:53, clinic 15:33 MDT",
             "source_id": "S01", "source_version": "r4",
             "locator": "step durations", "source_excerpt": "20 min depart, 28 min gate, 40 min clinic",
             "warrant": "Durations from mission requirement.",
             "calculation": "14:05 + 20 min = 14:25; + 28 min = 14:53; + 40 min = 15:33",
             "output_condition": "schedule feasible" if changed else "schedule infeasible at baseline gate",
             "next_handoff": "delivery", "uncertainty": "counterfactual at baseline gate",
             "result": "SUPPORTED"},
        ])

        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(rows)

    def prepare(self, unrelated_delta: bool = False) -> None:
        shutil.copyfile(ROOT / "shared/templates/source-register.csv", self.work / "source-register.csv")
        with (self.work / "source-register.csv").open("a", encoding="utf-8") as handle:
            for row in (
                "S01,S01_MO-27_r4.md,North Basin Mission Control,r4,2026-10-06 13:50 MDT,MO-27,requirements,delivery,APPLICABLE\n",
                "S02,S02_WMS_RCPT-8821.md,Red Mesa Warehouse Management,RCPT-8821,2026-10-06 13:42 MDT,WMS totes and lots,custody and identity,usable inventory,APPLICABLE\n",
                "S03,S03_QA_RELEASE-661.md,North Basin Quality Office,QA-661,2026-10-06 13:48 MDT,QA release,quality release status,permit approval,APPLICABLE\n",
                "S04,S04_FLEET_VX-204_r7.md,North Basin Fleet Engineering,r7,2026-10-01 00:00 MDT,VX-204,payload and rack,VX-240,APPLICABLE\n",
                "S05,S05_R71_BULLETINS.md,North Basin Road Authority,v5 current,2026-10-06 19:55Z,R-71,route closure,R-17,SUPERSEDED\n",
                "S06,S06_PERMIT_PR-4418.md,North Basin Movement Registry,snapshot 14:02,2026-10-06 14:02 MDT,PR-4418,permit status,authorization,APPLICABLE\n",
                "S07,S07_VENDOR_VX-240.md,Alpine Bodyworks,2026-09-12,2026-09-12,VX-240,packing dimensions,VX-204,IRRELEVANT\n",
                "S08,S08_R17_COMMUNITY_UPDATE.md,Pine County Community Desk,2026-10-06 14:00,2026-10-06 14:00 MDT,R-17,R-17 status,R-71,IRRELEVANT\n",
                "S09,S09_AI_DISPATCH_DRAFT.md,AI producer,draft 14:05,2026-10-06 14:05 MDT,AI brief,none,verification,OUTPUT_TO_CHECK\n",
            ):
                handle.write(row)
        self.write_ledger(self.work / "thread-ledger.csv")
        (self.work / "baseline-verdict.md").write_text("# Baseline verdict\n\nVerdict: HOLD\nStanding rule: Use the exact current source.\n", encoding="utf-8")
        (self.work / "change-prediction.md").write_text("# Prediction\n\nFields that should change\nClaims that should change\nFields that must not change\nCondition that would still block\nUnexpected change\n", encoding="utf-8")
        (self.work / "challenge-matrix.md").write_text("\n".join(f"## {x}\n\nRejected with reason.\n" for x in CHALLENGES), encoding="utf-8")
        (self.work / "corrected-brief.md").write_text("# Corrected brief\n\nInternal class review.\n", encoding="utf-8")
        (self.work / "handoff.md").write_text("# Handoff\n\nCurrent result and sources.\n", encoding="utf-8")

        freeze = run("freeze_baseline.py", self.work)
        self.assertEqual(freeze.returncode, 0, freeze.stdout + freeze.stderr)
        reveal = run("reveal_change.py", self.work)
        self.assertEqual(reveal.returncode, 0, reveal.stdout + reveal.stderr)

        self.write_ledger(self.work / "changed-thread-ledger.csv", changed=True, unrelated_delta=unrelated_delta)
        (self.work / "changed-brief.md").write_text("# Changed brief\n\nR-71 v6 closes at 21:20Z. Permit remains PENDING.\n", encoding="utf-8")
        (self.work / "changed-verdict.md").write_text("# Changed verdict\n\nVerdict: HOLD\nChanged source: R71-2026-1006-v6\nChanged fields: route closure and gate margin\nUnchanged blockers: permit remains PENDING\nLater event not yet observed: delivery\nWhy the overall verdict did not change: authorization is unresolved.\nNew closure: 21:20Z\n", encoding="utf-8")
        render = run("render_review.py", self.work)
        self.assertEqual(render.returncode, 0, render.stdout + render.stderr)

    def test_complete_visible_practice_passes(self) -> None:
        self.prepare()
        result = run("check_work.py", self.work)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("protected grading is still required", result.stdout)

    def test_unrelated_changed_step_holds(self) -> None:
        self.prepare(unrelated_delta=True)
        result = run("check_work.py", self.work)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL: allowed step delta:C02", result.stdout)

    def test_tampered_baseline_holds(self) -> None:
        self.prepare()
        with (self.work / "thread-ledger.csv").open("a", encoding="utf-8") as handle:
            handle.write("tamper\n")
        result = run("check_work.py", self.work)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL: frozen:thread-ledger.csv", result.stdout)

    def test_tampered_copied_source_holds(self) -> None:
        self.prepare()
        source = self.work / "case-packet/sources/S03_QA_RELEASE-661.md"
        source.write_text(source.read_text(encoding="utf-8") + "\ntamper\n", encoding="utf-8")
        result = run("check_work.py", self.work)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL: source hash:S03", result.stdout)

    def test_tampered_revealed_change_holds(self) -> None:
        self.prepare()
        change = self.work / "REVEALED_CHANGE.md"
        change.write_text(change.read_text(encoding="utf-8") + "\ntamper\n", encoding="utf-8")
        result = run("check_work.py", self.work)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL: revealed change hash", result.stdout)

    def test_incomplete_source_register_holds(self) -> None:
        self.prepare()
        register = self.work / "source-register.csv"
        lines = register.read_text(encoding="utf-8").splitlines()
        kept = [line for line in lines if not line.startswith("S05,")]
        register.write_text("\n".join(kept) + "\n", encoding="utf-8")
        result = run("check_work.py", self.work)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL: source register covers all nine sources", result.stdout)

    def test_blank_calculation_holds(self) -> None:
        self.prepare()
        ledger = self.work / "thread-ledger.csv"
        with ledger.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            if row["statement_type"] == "CALCULATION":
                row["calculation"] = ""
                break
        with ledger.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        result = run("check_work.py", self.work)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL: calculations have explicit formulas", result.stdout)

    def test_reveal_before_freeze_holds(self) -> None:
        other = Path(self.tmp.name) / "unfrozen"
        self.assertEqual(run("start_work.py", other).returncode, 0)
        result = run("reveal_change.py", other)
        self.assertEqual(result.returncode, 1)
        self.assertIn("freeze baseline", result.stdout)

    def test_wrong_scanned_count_holds(self) -> None:
        self.prepare()
        ledger = self.work / "thread-ledger.csv"
        with ledger.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            for field in ("calculation", "claim", "result"):
                row[field] = row[field].replace("216", "215")
            if row["statement_type"] == "CALCULATION" and "12" in row["calculation"]:
                row["calculation"] = "12*18=215"
        with ledger.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        result = run("check_work.py", self.work)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL: practice scanned count 216", result.stdout)

    def test_stale_closure_in_changed_ledger_holds(self) -> None:
        self.prepare()
        ledger = self.work / "changed-thread-ledger.csv"
        with ledger.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            if row["step"] == "Route window met":
                row["claim"] = f"{row['claim']} 20:50Z"
                break
        with ledger.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(rows)
        result = run("check_work.py", self.work)
        self.assertEqual(result.returncode, 1)
        self.assertIn("20:50Z", result.stdout)
        self.assertIn("stale", result.stdout)

    def test_changed_accept_holds(self) -> None:
        self.prepare()
        path = self.work / "changed-verdict.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace("Verdict: HOLD", "Verdict: ACCEPT"),
            encoding="utf-8",
        )
        result = run("check_work.py", self.work)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL: changed verdict is HOLD", result.stdout)

    def test_baseline_revise_holds(self) -> None:
        self.prepare()
        path = self.work / "baseline-verdict.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace("Verdict: HOLD", "Verdict: REVISE"),
            encoding="utf-8",
        )
        result = run("check_work.py", self.work)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL: baseline verdict is HOLD", result.stdout)



if __name__ == "__main__":
    unittest.main()
