#!/usr/bin/env python3
"""Public-site boundary regressions using isolated authored test courses."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("course_build", ROOT / "scripts/build_course.py")
builder = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = builder
SPEC.loader.exec_module(builder)

PROCEDURE = """# Example

## Read a file

Read the supplied source before deciding what it supports.

**Terminal: Bash or zsh, ordinary user.**

```bash
printf '%s\\n' 'a < b & c'
```

**Expected:** You see the literal comparison text.

```text
a < b & c
```

**Stop:** If the command fails, keep the error. **Recovery:** Correct the path and rerun.

[Input file](shared/case/SOURCE.md)

| Field | Meaning |
|:---|---:|
| state | An observed state. |
"""


class PublicationBehavior(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="course-publish-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        boot = self.root / "AI_Harness_Bootcamp_2"
        boot.mkdir()
        self.course = {"schema_version": 1, "course_id": "AI_Harness_Bootcamp_2", "source_root": "AI_Harness_Bootcamp_2", "site_dir": "site", "index": {"source": "README.md", "dest": "index.html"}, "modules": [], "shared_downloads": []}
        links = []
        for i in range(10):
            directory = f"module-{i:02d}-example"
            module = boot / directory
            (module / "shared/case").mkdir(parents=True)
            (module / "shared/case/SOURCE.md").write_text("# Authored test input\nA receipt is not a release.\n", encoding="utf-8")
            (module / "README.md").write_text(PROCEDURE, encoding="utf-8")
            links.append(f"[Assignment {i}]({directory}/README.md)")
            self.course["modules"].append({"id": f"{i:02d}", "directory": directory, "title": "Example", "pages": [{"source": "README.md", "dest": "README.html"}], "download_dirs": ["shared/case"]})
        (boot / "README.md").write_text("# Synthetic publication test\n\n" + "\n\n".join(links), encoding="utf-8")
        self.save_manifest()
        self.page = boot / "module-00-example/README.md"
        self.published = self.root / "site/AI_Harness_Bootcamp_2/module-00-example/README.html"

    def save_manifest(self):
        (self.root / "course.json").write_text(json.dumps(self.course), encoding="utf-8")

    def build(self, check=False):
        with contextlib.redirect_stdout(io.StringIO()):
            return builder.build(self.root, check)

    def test_rendered_links_raw_inputs_commands_and_accessible_tables(self):
        self.build()
        document = self.published.read_text(encoding="utf-8")
        tree = builder.parse_html(document)
        commands = [node for node in tree.walk() if "data-command" in node.attrs]
        self.assertEqual([node.text() for node in commands], ["printf '%s\\n' 'a < b & c'\n"])
        self.assertIn('href="shared/case/SOURCE.md"', document)
        self.assertIn('href="AI_Harness_Bootcamp_2/module-00-example/README.html"', (self.root / "site/index.html").read_text())
        self.assertEqual(len([node for node in tree.walk() if node.tag == "caption"]), 1)
        self.assertTrue(all(node.attrs.get("scope") == "col" for node in tree.walk() if node.tag == "th"))
        self.assertEqual(self.build(check=True), 0)

    def test_check_missing_site_and_raw_tampering_fail_without_writing(self):
        with self.assertRaisesRegex(ValueError, "missing or stale"):
            self.build(check=True)
        self.assertFalse((self.root / "site").exists())
        self.build()
        raw = self.published.parent / "shared/case/SOURCE.md"
        raw.write_text("tampered", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "missing or stale"):
            self.build(check=True)
        self.assertEqual(raw.read_text(), "tampered")

    def test_duplicate_destinations_and_escaping_paths_fail(self):
        self.course["modules"][0]["pages"].append({"source": "README.md", "dest": "README.html"})
        self.save_manifest()
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.build()
        self.assertFalse((self.root / "site").exists())
        for path in ("../outside", "/outside", "C:thing", "a\\b"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                builder.safe_relative(path)

    def test_unlisted_staff_links_and_active_html_fail_before_publication(self):
        for addition in ("\n[Staff](reference/REFERENCE.md)\n", "\n<script>alert('unsafe')</script>\n", '\n<img src="shared/case/SOURCE.md" onerror="alert(1)">\n'):
            with self.subTest(addition=addition):
                self.page.write_text(PROCEDURE + addition, encoding="utf-8")
                with self.assertRaises(ValueError):
                    self.build()
                self.assertFalse((self.root / "site").exists())

    def test_each_command_needs_its_own_terminal_and_later_observation(self):
        variants = [PROCEDURE.replace("```bash", "```", 1), PROCEDURE.replace("**Terminal: Bash or zsh, ordinary user.**", "**Bash**"), PROCEDURE + "\n## Another action\n\n**Terminal: Bash, ordinary user.**\n\n```bash\nprintf forgotten\n```\n"]
        for text in variants:
            with self.subTest(text=text):
                self.page.write_text(text, encoding="utf-8")
                with self.assertRaises(ValueError):
                    self.build()

    def test_broken_anchor_and_unlisted_output_are_rejected(self):
        self.page.write_text(PROCEDURE + "\n[Missing](#missing)\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "anchor"):
            self.build()
        self.page.write_text(PROCEDURE, encoding="utf-8")
        self.build()
        stray = self.root / "site/private.txt"
        stray.write_text("preserve me", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unlisted public output"):
            self.build()
        self.assertEqual(stray.read_text(), "preserve me")

    def test_symlinked_data_cannot_escape_the_public_allowlist(self):
        outside = self.root / "outside-secret.txt"
        outside.write_text("secret", encoding="utf-8")
        (self.page.parent / "shared/case/link.txt").symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "linked exercise"):
            self.build()
        self.assertFalse((self.root / "site").exists())


if __name__ == "__main__":
    unittest.main()
