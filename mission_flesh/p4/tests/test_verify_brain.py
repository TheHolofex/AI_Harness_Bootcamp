#!/usr/bin/env python3
"""Tests for P4 second-brain verifiers."""

from __future__ import annotations

import json
import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

P4_ROOT = Path(__file__).resolve().parents[1]
SEED_TOOLS = P4_ROOT / "vault_seed" / "tools"
REF = P4_ROOT / "reference_fixtures" / "complete_vault"
VERIFY_BRAIN = SEED_TOOLS / "verify_brain.py"
VERIFY_BASE = SEED_TOOLS / "verify_baseline.py"
VERIFY_VAULT = SEED_TOOLS / "verify_vault.py"


def run_py(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        check=False,
        capture_output=True,
        text=True,
    )


class VerifyBrainTests(unittest.TestCase):
    def test_reference_vault_passes(self) -> None:
        self.assertTrue(REF.is_dir(), "reference vault missing — run build_seed_and_reference.py")
        result = run_py(VERIFY_BRAIN, str(REF))
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("PASS brain", result.stdout)

    def test_unsourced_note_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "vault"
            shutil.copytree(REF, root)
            bad = root / "Notes" / "Content" / "Unsourced.md"
            bad.write_text(
                """---
note_id: "NOTE-BAD"
title: "Bad"
route_legs: ["rail"]
modes: ["rail"]
factors: ["physical"]
threat_class: "none"
confidence: "high"
sources: []
---

# Bad
[[Notes/Modes]]
""",
                encoding="utf-8",
            )
            result = run_py(VERIFY_BRAIN, str(root))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("HOLD brain", result.stderr)

    def test_invalid_note_enum_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "vault"
            shutil.copytree(REF, root)
            note = root / "Notes" / "Content" / "MBT_Envelope.md"
            text = note.read_text(encoding="utf-8").replace(
                'modes: ["rail", "road", "multimodal"]',
                'modes: ["rail", "road", "teleport"]',
            )
            note.write_text(text, encoding="utf-8")
            result = run_py(VERIFY_BRAIN, str(root))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("invalid modes", result.stderr)

    def test_source_hash_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "vault"
            shutil.copytree(REF, root)
            note = root / "Notes" / "Content" / "MBT_Envelope.md"
            text = note.read_text(encoding="utf-8")
            text = text.replace(
                'sha256: "f6fdfed5ca307cc074f525f7b0b4b15df9bb4bb0418e073a7bf4abbcbfe6b033"',
                'sha256: "' + ("0" * 64) + '"',
            )
            note.write_text(text, encoding="utf-8")
            result = run_py(VERIFY_BRAIN, str(root))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("source sha256 does not match MANIFEST", result.stderr)

    def test_source_manifest_metadata_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "vault"
            shutil.copytree(REF, root)
            note = root / "Notes" / "Content" / "MBT_Envelope.md"
            text = note.read_text(encoding="utf-8").replace(
                'publisher: "Course logistics reference desk"',
                'publisher: "Invented publisher"',
                1,
            )
            note.write_text(text, encoding="utf-8")
            result = run_py(VERIFY_BRAIN, str(root))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("source publisher does not match MANIFEST", result.stderr)

    def test_researcher_mcp_allow_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "vault"
            shutil.copytree(REF, root)
            permissions = root / "Evidence" / "PERMISSIONS.json"
            data = json.loads(permissions.read_text(encoding="utf-8"))
            data["researchers"]["mcp"] = "allow"
            permissions.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            result = run_py(VERIFY_BRAIN, str(root))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("researchers MCP policy must be deny", result.stderr)

    def test_retriever_filesystem_allow_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "vault"
            shutil.copytree(REF, root)
            permissions = root / "Evidence" / "PERMISSIONS.json"
            data = json.loads(permissions.read_text(encoding="utf-8"))
            data["retriever"] = {
                "project": "Documents\\p4-cold-query",
                "mcp": {"read": "allow", "write": "ask"},
                "filesystem": "allow",
                "web": "deny",
            }
            permissions.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            result = run_py(VERIFY_BRAIN, str(root))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("retriever filesystem policy must be deny", result.stderr)

    def test_fabricated_mcp_receipt_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "vault"
            shutil.copytree(REF, root)
            receipts = root / "Evidence" / "MCP_RECEIPTS.jsonl"
            receipts.write_text('{"action":"write"}\n', encoding="utf-8")
            result = run_py(VERIFY_BRAIN, str(root))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing keys", result.stderr)

    def test_broken_retrieval_link_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "vault"
            shutil.copytree(REF, root)
            answers = root / "Retrieval" / "Answers.md"
            text = answers.read_text(encoding="utf-8").replace(
                "[[Notes/Content/Rail_Clearance]]",
                "[[Notes/Content/Does_Not_Exist]]",
                1,
            )
            answers.write_text(text, encoding="utf-8")
            result = run_py(VERIFY_BRAIN, str(root))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unresolved wikilink", result.stderr)

    def test_incomplete_run_state_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "vault"
            shutil.copytree(REF, root)
            state = root / "Harness" / "RUN_STATE.md"
            text = state.read_text(encoding="utf-8").replace("Status: SUCCESS", "Status: HOLD")
            state.write_text(text, encoding="utf-8")
            result = run_py(VERIFY_BRAIN, str(root))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("RUN_STATE.md must record Status SUCCESS", result.stderr)

    def test_baseline_detects_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "vault"
            shutil.copytree(REF, root)
            external = Path(tmp) / "baseline.json"
            freeze = run_py(
                VERIFY_BASE,
                str(root),
                "--write-manifest",
                "--external",
                str(external),
            )
            self.assertEqual(freeze.returncode, 0, freeze.stderr)
            check = run_py(VERIFY_VAULT, str(root), "--check-manifest", str(external))
            self.assertEqual(check.returncode, 0, check.stderr + check.stdout)
            (root / "MOC.md").write_text(
                (root / "MOC.md").read_text(encoding="utf-8") + "\nmutated\n",
                encoding="utf-8",
            )
            check2 = run_py(VERIFY_VAULT, str(root), "--check-manifest", str(external))
            self.assertNotEqual(check2.returncode, 0)
            self.assertIn("HOLD baseline", check2.stderr)

    def test_corpus_manifest_size(self) -> None:
        manifest_path = P4_ROOT / "raw_corpus" / "MANIFEST.json"
        self.assertTrue(manifest_path.is_file())
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(manifest), 300)
        self.assertLessEqual(len(manifest), 600)
        slice_path = P4_ROOT / "raw_corpus" / "ASSESSED_SLICE.json"
        assessed = json.loads(slice_path.read_text(encoding="utf-8"))
        self.assertGreaterEqual(assessed["count"], 60)
        self.assertLessEqual(assessed["count"], 120)
        for key in (
            "worker_conus_rail_road",
            "worker_port_sealift_taiwan",
            "worker_constraints",
            "worker_protection",
        ):
            self.assertIn(key, assessed["partitions"])
            self.assertGreater(len(assessed["partitions"][key]), 0)
        assigned = [
            source_id
            for source_ids in assessed["partitions"].values()
            for source_id in source_ids
        ]
        self.assertEqual(len(assigned), len(set(assigned)), "worker partitions overlap")
        self.assertEqual(set(assigned), set(assessed["source_ids"]))
        rows = {row["source_id"]: row for row in manifest}
        planted = [
            source_id
            for source_id in assessed["source_ids"]
            if rows[source_id].get("planted_contradiction") == "rail_speed_45_vs_40"
        ]
        self.assertEqual(len(planted), 1, "assessed slice must contain one planted 45 mph notice")
        self.assertIn(planted[0], assessed["partitions"]["worker_constraints"])

        facts = json.loads(
            (P4_ROOT / "raw_corpus" / "CANONICAL_FACTS.json").read_text(encoding="utf-8")
        )
        self.assertEqual(facts["combat_weight_stons"], 73.6)
        self.assertEqual(facts["rail_max_speed_loaded_mph"], 40)
        self.assertEqual(facts["preferred_taiwan_port"], "Kaohsiung")

    def test_corpus_builder_uses_the_fixed_snapshot_date(self) -> None:
        manifest = json.loads(
            (P4_ROOT / "raw_corpus" / "MANIFEST.json").read_text(encoding="utf-8")
        )
        manifest_dates = {row["retrieval_date"] for row in manifest}
        self.assertEqual(len(manifest_dates), 1)

        script = P4_ROOT / "scripts" / "build_corpus.py"
        spec = importlib.util.spec_from_file_location("p4_build_corpus", script)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual({module.RETRIEVAL}, manifest_dates)


if __name__ == "__main__":
    unittest.main()
