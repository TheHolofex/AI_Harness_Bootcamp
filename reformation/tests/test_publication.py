#!/usr/bin/env python3
"""Workspace safety regressions; every mutation is in a disposable source tree."""
from __future__ import annotations

import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("prepare_work", ROOT / "shared/prepare_work.py")
prepare_work = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prepare_work)


class WorkspaceBehavior(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="course-work-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "checkout/reformation"
        self.boot = self.root / "AI_Harness_Bootcamp_2"
        self.boot.mkdir(parents=True)

    def module(self, module_id):
        module = self.boot / f"module-{module_id}-test"
        for sub in prepare_work.SHARED[module_id]:
            directory = module / "shared" / sub
            directory.mkdir(parents=True)
            (directory / "input.txt").write_text("original input\n", encoding="utf-8")
        (module / "scripts").mkdir()
        for script in prepare_work.SCRIPTS[module_id]:
            (module / "scripts" / script).write_text("# authored test control\n", encoding="utf-8")
        return module

    def test_preserves_attempt_and_rejects_repository_overlap(self):
        self.module("02")
        work = self.base / "existing"
        work.mkdir()
        (work / "decision.txt").write_text("keep", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            prepare_work.prepare("02", work, self.root)
        self.assertEqual((work / "decision.txt").read_text(), "keep")
        with self.assertRaises(ValueError):
            prepare_work.prepare("02", self.root.parent / "unrelated-new-work", self.root)
        self.assertFalse((self.root.parent / "unrelated-new-work").exists())

    def test_filters_staff_history_and_verifier_from_all_depths(self):
        module = self.module("08")
        for relative in ("shared/case/verify_safeguards.py", "shared/case/tests/test.py", "shared/case/history/old.txt", "shared/case/__pycache__/old.pyc", "shared/case/assessment/private.json"):
            target = module / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("must not enter W", encoding="utf-8")
        work = prepare_work.prepare("08", self.base / "attempt/deep/work", self.root)
        self.assertEqual((work / "shared/case/input.txt").read_text(), "original input\n")
        self.assertEqual({path.relative_to(work).as_posix() for path in work.rglob("*") if path.is_file()}, {"shared/case/input.txt", "shared/controls/input.txt"})

    def test_missing_control_holds_before_destination_creation(self):
        module = self.module("04")
        (module / "scripts/restore.py").unlink()
        work = self.base / "attempt/work"
        with self.assertRaisesRegex(ValueError, "required source"):
            prepare_work.prepare("04", work, self.root)
        self.assertFalse(work.exists())
        self.assertFalse(work.parent.exists())

    def test_frozen_renderer_remains_distinct_after_work_control_changes(self):
        self.module("04")
        work = prepare_work.prepare("04", self.base / "work with spaces", self.root)
        original = (work / "baseline/render_review.py").read_bytes()
        frozen = (work / "baseline/render_review.py.sha256").read_text().strip()
        (work / "scripts/render_review.py").write_text("faulty replacement", encoding="utf-8")
        self.assertEqual(hashlib.sha256((work / "baseline/render_review.py").read_bytes()).hexdigest(), frozen)
        self.assertEqual((work / "baseline/render_review.py").read_bytes(), original)
        self.assertNotEqual(hashlib.sha256((work / "scripts/render_review.py").read_bytes()).hexdigest(), frozen)

    def test_linked_source_and_broken_destination_link_refuse(self):
        module = self.module("03")
        secret = self.base / "outside.txt"
        secret.write_text("outside", encoding="utf-8")
        (module / "shared/case/link.txt").symlink_to(secret)
        with self.assertRaisesRegex(ValueError, "linked"):
            prepare_work.prepare("03", self.base / "work", self.root)
        self.assertFalse((self.base / "work").exists())
        (self.base / "broken").symlink_to(self.base / "absent")
        with self.assertRaises(FileExistsError):
            prepare_work.prepare("03", self.base / "broken", self.root)
        self.assertTrue((self.base / "broken").is_symlink())

    def test_noncanonical_module_ids_refuse(self):
        for module_id in ("2", "00", "01", "10", " 02", "02 ", "../02"):
            with self.subTest(module_id=module_id), self.assertRaises(ValueError):
                prepare_work.prepare(module_id, self.base / "work", self.root)
        self.assertFalse((self.base / "work").exists())


if __name__ == "__main__":
    unittest.main()
