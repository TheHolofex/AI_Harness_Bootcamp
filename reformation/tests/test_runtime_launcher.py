#!/usr/bin/env python3
"""Deterministic launcher regressions. Synthetic receipts never count as live proof."""
from __future__ import annotations
import copy
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "shared/run_omp.py"
SPEC = importlib.util.spec_from_file_location("run_omp", LAUNCHER)
runtime = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runtime)


class LauncherBehavior(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="course-launch-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.work = self.base / "work"
        self.work.mkdir()
        (self.work / "source.txt").write_text("input", encoding="utf-8")
        self.prompt = self.base / "prompt.md"
        self.prompt.write_text("Read source.txt without changing it.", encoding="utf-8")
        self.evidence = self.base / "evidence"

    def cli(self, extra=(), key=""):
        environment = dict(os.environ, OPENROUTER_API_KEY=key)
        return subprocess.run([sys.executable, str(LAUNCHER), "--workdir", str(self.work), "--prompt", str(self.prompt), "--evidence", str(self.evidence), *extra], capture_output=True, text=True, env=environment, cwd=self.base, timeout=20)

    def test_missing_key_stops_without_runtime_outputs_or_work_mutation(self):
        before = runtime.work_snapshot(self.work)
        result = self.cli()
        self.assertEqual(result.returncode, 2)
        self.assertIn("OPENROUTER_API_KEY unavailable", result.stderr)
        self.assertFalse(self.evidence.exists())
        self.assertEqual(runtime.work_snapshot(self.work), before)

    def test_missing_empty_instruction_and_permission_conflicts_are_prerequisites(self):
        empty = self.base / "empty.md"
        empty.write_text(" \n", encoding="utf-8")
        for args in (("--instruction", str(self.base / "missing")), ("--instruction", str(empty)), ("--allow-write", "../escape"), ("--allow-write", "source.txt"), ("--hash-tool", "missing.py", "--allow-write", "new.txt")):
            with self.subTest(args=args):
                result = self.cli(args)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertFalse(self.evidence.exists())

    def test_declared_policy_exact_schema_and_unknown_keys(self):
        declaration = self.work / "AGENT_POLICY.md"
        declaration.write_text("# Policy\n\n```json\n" + json.dumps(runtime.DECLARATION) + "\n```\n", encoding="utf-8")
        self.assertEqual(runtime.parse_declaration(declaration), runtime.DECLARATION)
        for update in ({"extra": True}, {"write_root": "."}, {"tools": ["course_read"]}, {"yolo": True}):
            changed = {**runtime.DECLARATION, **update}
            declaration.write_text("```json\n" + json.dumps(changed) + "\n```\n", encoding="utf-8")
            with self.subTest(update=update), self.assertRaises(ValueError):
                runtime.parse_declaration(declaration)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            runtime.strict_json('{"enabled":true,"enabled":false}')

    def test_isolation_removes_author_state_and_keeps_only_course_credential(self):
        isolated = self.base / "runtime"
        isolated.mkdir()
        poison = {"PI_CODING_AGENT_DIR": "/author", "OMP_PROFILE": "author", "ANTHROPIC_API_KEY": "direct", "OPENAI_API_KEY": "direct", "OPENROUTER_BASE_URL": "bad", "COURSE_GUARD_POLICY": "bad", "HOME": "/author", "APPDATA": "/author", "LANG": "C", "HTTPS_PROXY": "http://proxy.invalid"}
        with patch.dict(os.environ, poison):
            environment = runtime.isolated_env(isolated, self.evidence / "policy.json", "synthetic-key")
        self.assertFalse(set(poison).intersection(environment) - {"HOME", "APPDATA", "LANG", "HTTPS_PROXY", "COURSE_GUARD_POLICY"})
        self.assertEqual(environment["OPENROUTER_API_KEY"], "synthetic-key")
        self.assertEqual(environment["COURSE_GUARD_POLICY"], str(self.evidence / "policy.json"))
        for name in ("HOME", "USERPROFILE", "APPDATA", "LOCALAPPDATA", "XDG_CONFIG_HOME", "XDG_STATE_HOME"):
            self.assertTrue(Path(environment[name]).is_relative_to(isolated))

    def receipt(self):
        policy = dict.fromkeys(runtime.POLICY_KEYS)
        policy.update(schema_version=1, run_id="synthetic", work_root=str(self.work), profile="read", tools=["course_read"], write_files=[], write_root=None, provider=runtime.PROVIDER, model=runtime.MODEL, omp_version=runtime.OMP_VERSION)
        assistant = {"role": "assistant", "provider": runtime.PROVIDER, "model": runtime.MODEL, "stopReason": "stop", "content": [{"type": "text", "text": "Source describes custody only."}]}
        events = [{"type": "agent_start"}, {"type": "message_end", "message": assistant}, {"type": "agent_end", "isTerminal": True, "messages": [assistant]}]
        guard = [{"type": "guard_ready", "run_id": "synthetic", "provider": runtime.PROVIDER, "model": runtime.MODEL, "active_tools": ["course_read"]}, {"type": "provider_request", "run_id": "synthetic", "provider": runtime.PROVIDER, "model": runtime.MODEL}, {"type": "guard_end", "run_id": "synthetic", "ready": True, "failed": False, "provider_requests": 1}]
        before = runtime.snapshot(self.work, [self.base / "outside.txt"])
        return policy, events, guard, {"before": before, "after": copy.deepcopy(before)}

    def test_incomplete_error_duplicate_or_drift_receipts_hold(self):
        policy, events, guard, snapshots = self.receipt()
        self.assertEqual(runtime.validate_run(policy, events, guard, snapshots, 0), [])
        for reason in ("no-terminal", "duplicate-terminal", "truncated", "model-drift", "missing-guard", "retry", "guard-failed", "request-count", "offline-cutoff"):
            p, e, g, s = copy.deepcopy((policy, events, guard, snapshots))
            if reason == "no-terminal": e[-1]["isTerminal"] = False
            elif reason == "duplicate-terminal": e.append(e[-1])
            elif reason == "truncated": e[1]["message"]["stopReason"] = "length"
            elif reason == "model-drift": e[1]["message"]["model"] = "other"
            elif reason == "missing-guard": g.pop()
            elif reason == "retry": e.insert(1, {"type": "auto_retry_start"})
            elif reason == "guard-failed": g[-1]["failed"] = True
            elif reason == "request-count": g[-1]["provider_requests"] = 2
            elif reason == "offline-cutoff": e = [{"type": "session"}]; g.pop(1); g[-1]["provider_requests"] = 0
            with self.subTest(reason=reason):
                self.assertTrue(runtime.validate_run(p, e, g, s, 0))

    def test_unpaired_calls_and_forbidden_effects_hold(self):
        policy, events, guard, snapshots = self.receipt()
        events[1]["message"]["content"].append({"type": "toolCall", "id": "unpaired", "name": "course_read", "arguments": {"path": "source.txt"}})
        self.assertIn("unmatched assistant calls, executions, or results", runtime.validate_run(policy, events, guard, snapshots, 0))
        policy, events, guard, snapshots = self.receipt()
        snapshots["after"]["work"]["source.txt"]["sha256"] = "changed"
        snapshots["after"]["work"]["release.txt"] = {"type": "file", "sha256": "unreceipted"}
        snapshots["after"]["watch"][str(self.base / "outside.txt")] = {"type": "file", "sha256": "forbidden"}
        errors = runtime.validate_run(policy, events, guard, snapshots, 0)
        self.assertIn("watched target changed", errors)
        self.assertTrue(any("existing input/control" in error for error in errors))
        self.assertTrue(any("unreceipted output" in error for error in errors))

    def test_successful_tool_receipts_bind_execution_identity_path_and_order(self):
        policy, events, guard, snapshots = self.receipt()
        call = {"type": "toolCall", "id": "read-1", "name": "course_read", "arguments": {"path": "source.txt"}}
        assistant = {"role": "assistant", "provider": runtime.PROVIDER, "model": runtime.MODEL, "stopReason": "toolUse", "content": [call]}
        content = [{"type": "text", "text": "input"}]
        events[1:1] = [
            {"type": "message_end", "message": assistant},
            {"type": "tool_execution_start", "toolCallId": "read-1", "toolName": "course_read", "args": call["arguments"]},
            {"type": "tool_execution_end", "toolCallId": "read-1", "toolName": "course_read", "result": {"content": content}, "isError": False},
            {"type": "message_end", "message": {"role": "toolResult", "toolCallId": "read-1", "toolName": "course_read", "content": content, "isError": False}},
        ]
        decision = {"run_id": "synthetic", "type": "decision", "call_id": "read-1", "tool": "course_read", "arguments": call["arguments"], "allow": True, "resolved_path": str(self.work / "source.txt")}
        guard[-1:-1] = [decision, {**decision, "type": "execution_check"}, {"run_id": "synthetic", "type": "executed", "call_id": "read-1", "tool": "course_read", "resolved_path": str(self.work / "source.txt"), "output_sha256": None}]
        self.assertEqual(runtime.validate_run(policy, events, guard, snapshots, 0), [])
        for defect in ("wrong-tool", "wrong-path", "execution-before-authorization", "authorized-outside-read"):
            changed = copy.deepcopy(guard)
            if defect == "wrong-tool": changed[-2]["tool"] = "course_write"
            elif defect == "wrong-path": changed[-2]["resolved_path"] = str(self.base / "outside.txt")
            elif defect == "execution-before-authorization": changed[2:5] = [changed[4], changed[2], changed[3]]
            else:
                for row in changed[2:5]:
                    row["resolved_path"] = str(self.base / "outside.txt")
            with self.subTest(defect=defect):
                self.assertTrue(runtime.validate_run(policy, events, changed, snapshots, 0))

    def test_saved_evidence_rejects_altered_result_hashes_and_later_forbidden_effects(self):
        policy, events, guard, snapshots = self.receipt()
        self.evidence.mkdir()
        overlay = {"retry": {"enabled": False, "modelFallback": False}, "providers": {"cacheWarming": "off"}, "tools": {"approval": {"course_read": "allow"}, "intentTracing": False}}
        (self.evidence / "runtime-config.yml").write_bytes(runtime.json_bytes(overlay))
        policy["runtime_config_sha256"] = runtime.file_hash(self.evidence / "runtime-config.yml")
        (self.evidence / "policy.json").write_bytes(runtime.json_bytes(policy))
        policy_hash = runtime.file_hash(self.evidence / "policy.json")
        for row in guard:
            if row["type"] in {"guard_ready", "guard_end"}:
                row["policy_sha256"] = policy_hash
        for name, rows in (("events", events), ("guard", guard)):
            (self.evidence / f"{name}.jsonl").write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
        (self.evidence / "snapshots.json").write_bytes(runtime.json_bytes(snapshots))
        result = {"run_id": "synthetic", "provider": runtime.PROVIDER, "model": runtime.MODEL, "omp_version": runtime.OMP_VERSION, "status": "PASS", "exit_code": 0, "policy_sha256": policy_hash, "guard_sha256": runtime.file_hash(self.evidence / "guard.jsonl"), "instruction_sha256": None, "declared_policy_sha256": None, "input_sha256": {"source.txt": runtime.file_hash(self.work / "source.txt")}, "output_sha256": {}}
        (self.evidence / "result.json").write_bytes(runtime.json_bytes(result))
        (self.evidence / "response.md").write_text("Source describes custody only.", encoding="utf-8")
        self.assertEqual(runtime.audit_evidence(self.evidence), [])
        (self.evidence / "response.md").write_text("A substituted answer.", encoding="utf-8")
        self.assertIn("saved response differs from final assistant event", runtime.audit_evidence(self.evidence))
        (self.evidence / "response.md").write_text("Source describes custody only.", encoding="utf-8")
        altered = {**result, "input_sha256": {}}
        (self.evidence / "result.json").write_bytes(runtime.json_bytes(altered))
        self.assertIn("input_sha256 differs", runtime.audit_evidence(self.evidence))
        (self.evidence / "result.json").write_bytes(runtime.json_bytes(result))
        (self.base / "outside.txt").write_text("forbidden later effect")
        self.assertTrue(any("watched target changed after" in error for error in runtime.audit_evidence(self.evidence)))

    def test_jsonl_rejects_partial_or_non_event_records(self):
        target = self.base / "stream.jsonl"
        for raw in (b'{"type":"agent_end"}', b'{"type":', b'{}\n', b'\n'):
            target.write_bytes(raw)
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                runtime.read_jsonl(target)


if __name__ == "__main__":
    unittest.main()
