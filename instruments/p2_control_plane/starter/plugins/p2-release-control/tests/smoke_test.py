#!/usr/bin/env python3
"""Smoke-test the P2 release-control hook without Codex or credentials."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


HOOK = Path(__file__).resolve().parents[1] / "hooks" / "quality_gate.py"
FALLBACK_RECEIPT = Path("out/QUALITY_GATE_RECEIPT.json")
REQUIRED_EVIDENCE = {
    "inputs/p1/SOURCE_MANIFEST.md": "# Current sources\n\n| ID | File |\n|---|---|\n| C1 | one.md |\n| C2 | two.md |\n",
    "inputs/p1/AUDIT.md": "# P1 citation audit\n\nPASS\n",
    "inputs/p1/RELEASE_RECORD.md": "# P1 release record\n\nReleased with residual risk recorded.\n",
    "out/PLUGIN_REVIEW.md": "# Plugin review\n\nLocal-only Stop hook reviewed.\n",
    "out/EVIDENCE_MAP.md": "# Evidence map\n\nC1 and C2 mapped to their source files.\n",
    "out/CONFIG_EVIDENCE.md": "# Configuration evidence\n\nCurrent official configuration verified.\n",
    "out/DECISION_REVIEW.md": "# Decision review\n\nPASS\n",
    "out/RUN_RECEIPT.md": "# Run receipt\n\nObserved run recorded.\n",
}


def invoke(root: Path, *, stop_active: bool = False, manual: bool = False) -> dict[str, Any]:
    event = {
        "cwd": str(root),
        "hook_event_name": "Stop",
        "stop_hook_active": stop_active,
        "model": "gpt-5.6-terra",
    }
    command = [sys.executable, str(HOOK)]
    if manual:
        command.append("--check")
    result = subprocess.run(
        command,
        cwd=root,
        input="" if manual else json.dumps(event),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(f"hook exited {result.returncode}: {result.stderr}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise AssertionError(f"hook returned invalid JSON: {result.stdout!r}; stderr={result.stderr!r}") from error


def write_config(root: Path, *, enabled: bool = True, **overrides: Any) -> dict[str, Any]:
    config: dict[str, Any] = {
        "enabled": enabled,
        "deliverable": "out/final.md",
        "receipt": "out/receipt.json",
        "required_files": [],
        "required_headings": ["Shipped", "Broken", "Blocked", "Asks"],
        "citation_pattern": r"\[C[1-9][0-9]*\]",
        "minimum_citations": 2,
        "maximum_nonblank_lines": 14,
        "forbidden_patterns": [r"\bTODO\b"],
    }
    config.update(overrides)
    (root / "P2_CONTROL_PLANE.json").write_text(json.dumps(config), encoding="utf-8")
    return config


def write_required_evidence(root: Path) -> None:
    for relative, text in REQUIRED_EVIDENCE.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def passing_product(*, extra: str = "") -> str:
    return (
        "# Brief\n"
        "## Shipped\n- release complete [C1]\n"
        "## Broken\n- one qualified issue [C2]\n"
        "## Blocked\n- none\n"
        "## Asks\n- approve release\n"
        f"{extra}"
    )


def write_product(root: Path, text: str | None = None, relative: str = "out/final.md") -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if text is not None else passing_product(), encoding="utf-8")
    return path


def read_receipt(root: Path, relative: str = "out/receipt.json") -> dict[str, Any]:
    return json.loads((root / relative).read_text(encoding="utf-8"))


def assert_blocks(payload: dict[str, Any], message: str) -> None:
    assert payload.get("decision") == "block", message
    assert isinstance(payload.get("reason"), str) and payload["reason"].strip(), "block must explain why"


def assert_second_stop_is_bounded(root: Path) -> None:
    second = invoke(root, stop_active=True)
    assert "systemMessage" in second and "decision" not in second, "second failure must HOLD without looping"


def assert_fallback_hold(root: Path) -> dict[str, Any]:
    receipt = read_receipt(root, FALLBACK_RECEIPT.as_posix())
    assert receipt["status"] == "HOLD", "configuration/read failures need a durable HOLD receipt"
    assert receipt["results"][0]["status"] == "FAIL"
    return receipt


def test_inert_states() -> None:
    with tempfile.TemporaryDirectory(prefix="p2-hook-inert-") as temporary:
        root = Path(temporary)
        assert invoke(root) == {}, "missing project contract must be inert"
        write_config(root, enabled=False)
        assert invoke(root) == {}, "disabled project contract must be inert"


def test_malformed_contract_fails_closed() -> None:
    with tempfile.TemporaryDirectory(prefix="p2-hook-malformed-") as temporary:
        root = Path(temporary)
        stale = root / FALLBACK_RECEIPT
        stale.parent.mkdir(parents=True)
        stale.write_text(
            '{"gate":"p2-release-control","status":"PASS","stale":true}\n', encoding="utf-8"
        )
        (root / "P2_CONTROL_PLANE.json").write_text("{bad json", encoding="utf-8")
        assert_blocks(invoke(root), "malformed contract must hold once")
        fallback = assert_fallback_hold(root)
        assert "stale" not in fallback, "fallback HOLD must atomically replace a stale PASS receipt"
        assert_second_stop_is_bounded(root)

    with tempfile.TemporaryDirectory(prefix="p2-hook-nonobject-") as temporary:
        root = Path(temporary)
        (root / "P2_CONTROL_PLANE.json").write_text("[]", encoding="utf-8")
        assert_blocks(invoke(root), "non-object contract must hold")
        assert_fallback_hold(root)


def test_required_evidence_cannot_be_weakened() -> None:
    with tempfile.TemporaryDirectory(prefix="p2-hook-evidence-") as temporary:
        root = Path(temporary)
        write_config(root, required_files=[])
        write_product(root)
        assert_blocks(invoke(root), "stable P1 and P2 evidence must remain required")
        receipt = read_receipt(root)
        assert receipt["status"] == "FAIL"
        failed = {row["check"] for row in receipt["results"] if row["status"] == "FAIL"}
        for relative in REQUIRED_EVIDENCE:
            assert f"required file: {relative}" in failed, f"gate omitted required evidence {relative}"


def test_normal_fail_bounded_then_pass_atomic() -> None:
    with tempfile.TemporaryDirectory(prefix="p2-hook-product-") as temporary:
        root = Path(temporary)
        write_config(root)
        write_required_evidence(root)
        write_product(root, "# Brief\n## Shipped\n- done [C1]\n## Broken\n- TODO [C2]\n")
        assert_blocks(invoke(root), "bad product must request one repair")
        assert read_receipt(root)["status"] == "FAIL"
        assert_second_stop_is_bounded(root)

        write_product(root)
        assert invoke(root) == {}, "passing product must allow Stop"
        receipt = read_receipt(root)
        assert receipt["status"] == "PASS"
        assert receipt["sha256"], "PASS receipt must bind to product bytes"
        leftovers = list((root / "out").glob(".receipt.json.*.tmp"))
        assert not leftovers, f"atomic receipt write left temporary files: {leftovers}"
        assert invoke(root, manual=True) == {}, "manual check must use the same passing gate"


def test_distinct_manifest_backed_citations() -> None:
    with tempfile.TemporaryDirectory(prefix="p2-hook-citations-") as temporary:
        root = Path(temporary)
        write_config(root)
        write_required_evidence(root)

        repeated = passing_product().replace("[C2]", "[C1]") + "- repeated [C1] [C1] [C1]\n"
        write_product(root, repeated)
        assert_blocks(invoke(root), "repeating one citation must not satisfy the distinct minimum")
        receipt = read_receipt(root)
        row = next(row for row in receipt["results"] if row["check"] == "distinct citation count")
        assert row["status"] == "FAIL" and "1 found" in row["detail"]

        write_product(root, passing_product().replace("[C2]", "[C3]"))
        assert_blocks(invoke(root), "citation absent from the manifest must hold")
        receipt = read_receipt(root)
        row = next(row for row in receipt["results"] if row["check"] == "citations declared in source manifest")
        assert row["status"] == "FAIL" and "C3" in row["detail"]

        write_product(root)
        assert invoke(root) == {}, "two distinct declared citation IDs must pass citation checks"


def test_course_key_shapes_are_blocked_and_redacted() -> None:
    with tempfile.TemporaryDirectory(prefix="p2-hook-secrets-") as temporary:
        root = Path(temporary)
        write_config(root, forbidden_patterns=[])
        write_required_evidence(root)

        xai_key = "xai-abcdefghijklmnopqrstuvwx"
        write_product(root, passing_product(extra=f"- leaked {xai_key}\n"))
        payload = invoke(root)
        assert_blocks(payload, "xAI-shaped key must hold even if config removes optional patterns")
        assert xai_key not in json.dumps(payload), "hook output must not repeat a detected key"
        assert xai_key not in json.dumps(read_receipt(root)), "receipt must not store a detected key"

        openai_key = "sk-proj-abcdefghijklmnopqrstuvwx"
        write_product(root, passing_product(extra=f"- leaked {openai_key}\n"))
        payload = invoke(root)
        assert_blocks(payload, "OpenAI-shaped key must hold even if config removes optional patterns")
        assert openai_key not in json.dumps(payload)
        assert openai_key not in json.dumps(read_receipt(root))


def test_absolute_and_escaping_paths_are_rejected() -> None:
    cases = [
        ("deliverable", "/tmp/outside.md"),
        ("deliverable", r"C:\outside\final.md"),
        ("deliverable", "../outside.md"),
        ("required_files", ["/tmp/source.md"]),
        ("required_files", [r"C:\outside\source.md"]),
    ]
    for field, value in cases:
        with tempfile.TemporaryDirectory(prefix="p2-hook-path-") as temporary:
            root = Path(temporary)
            write_config(root, **{field: value})
            assert_blocks(invoke(root), f"unsafe {field} path must hold: {value!r}")
            assert_fallback_hold(root)
            assert_second_stop_is_bounded(root)


def test_receipt_path_is_safe_and_nonoverlapping() -> None:
    invalid_receipts = [
        "/tmp/receipt.json",
        r"C:\outside\receipt.json",
        "receipt.json",
        "out/nested/receipt.json",
        "out/../receipt.json",
        "out/receipt.txt",
    ]
    for receipt_value in invalid_receipts:
        with tempfile.TemporaryDirectory(prefix="p2-hook-receipt-") as temporary:
            root = Path(temporary)
            write_config(root, receipt=receipt_value)
            assert_blocks(invoke(root), f"unsafe receipt path must hold: {receipt_value!r}")
            assert_fallback_hold(root)

    with tempfile.TemporaryDirectory(prefix="p2-hook-overlap-") as temporary:
        root = Path(temporary)
        write_config(root, deliverable="out/receipt.json", receipt="out/receipt.json")
        write_required_evidence(root)
        original = passing_product()
        write_product(root, original, relative="out/receipt.json")
        assert_blocks(invoke(root), "receipt must not overlap the deliverable")
        assert (root / "out/receipt.json").read_text(encoding="utf-8") == original
        assert_fallback_hold(root)

    with tempfile.TemporaryDirectory(prefix="p2-hook-canonical-overlap-") as temporary:
        root = Path(temporary)
        write_config(
            root,
            deliverable="out/QUALITY_GATE_RECEIPT.json",
            receipt="out/QUALITY_GATE_RECEIPT.json",
        )
        write_required_evidence(root)
        original = passing_product()
        write_product(root, original, relative="out/QUALITY_GATE_RECEIPT.json")
        assert_blocks(invoke(root), "fallback receipt must not overwrite an overlapping deliverable")
        assert (root / "out/QUALITY_GATE_RECEIPT.json").read_text(encoding="utf-8") == original
        alternate = read_receipt(root, "out/QUALITY_GATE_HOLD_1.json")
        assert alternate["status"] == "HOLD"

    with tempfile.TemporaryDirectory(prefix="p2-hook-required-overlap-") as temporary:
        root = Path(temporary)
        write_config(root, required_files=["out/receipt.json"], receipt="out/receipt.json")
        write_required_evidence(root)
        original = "required evidence must survive\n"
        (root / "out/receipt.json").write_text(original, encoding="utf-8")
        assert_blocks(invoke(root), "receipt must not overlap configured evidence")
        assert (root / "out/receipt.json").read_text(encoding="utf-8") == original
        assert_fallback_hold(root)


def test_symlink_escape_fails_closed() -> None:
    with tempfile.TemporaryDirectory(prefix="p2-hook-symlink-root-") as root_temporary, tempfile.TemporaryDirectory(
        prefix="p2-hook-symlink-outside-"
    ) as outside_temporary:
        root = Path(root_temporary)
        outside = Path(outside_temporary)
        write_config(root, receipt="out/receipt.json")
        try:
            (root / "out").symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            return
        payload = invoke(root)
        assert_blocks(payload, "receipt symlink leaving the project must hold")
        assert "could not write" in payload["reason"].lower()
        assert not list(outside.iterdir()), "hook must not write through an escaping symlink"


def test_bad_regex_and_read_failure_leave_hold_receipt() -> None:
    with tempfile.TemporaryDirectory(prefix="p2-hook-regex-") as temporary:
        root = Path(temporary)
        write_config(root, forbidden_patterns=["["])
        assert_blocks(invoke(root), "bad regular expression must hold")
        assert_fallback_hold(root)
        assert_second_stop_is_bounded(root)

    with tempfile.TemporaryDirectory(prefix="p2-hook-citation-pattern-") as temporary:
        root = Path(temporary)
        write_config(root, citation_pattern=".*")
        assert_blocks(invoke(root), "citation pattern must not be broadened beyond one [C#] tag")
        assert_fallback_hold(root)

    with tempfile.TemporaryDirectory(prefix="p2-hook-decode-") as temporary:
        root = Path(temporary)
        write_config(root)
        write_required_evidence(root)
        path = root / "out/final.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"\xff\xfe\x80")
        assert_blocks(invoke(root), "unreadable deliverable must hold")
        assert_fallback_hold(root)


def test_fallback_write_failure_still_fails_closed() -> None:
    with tempfile.TemporaryDirectory(prefix="p2-hook-fallback-") as temporary:
        root = Path(temporary)
        (root / "P2_CONTROL_PLANE.json").write_text("{bad json", encoding="utf-8")
        (root / "out").write_text("not a directory", encoding="utf-8")
        payload = invoke(root)
        assert_blocks(payload, "receipt I/O failure must not make the gate fail open")
        assert "could not write" in payload["reason"].lower()
        assert_second_stop_is_bounded(root)


def main() -> int:
    test_inert_states()
    test_malformed_contract_fails_closed()
    test_required_evidence_cannot_be_weakened()
    test_normal_fail_bounded_then_pass_atomic()
    test_distinct_manifest_backed_citations()
    test_course_key_shapes_are_blocked_and_redacted()
    test_absolute_and_escaping_paths_are_rejected()
    test_receipt_path_is_safe_and_nonoverlapping()
    test_symlink_escape_fails_closed()
    test_bad_regex_and_read_failure_leave_hold_receipt()
    test_fallback_write_failure_still_fails_closed()
    print("PASS p2-release-control: inert, evidence, citation, secret, path, atomic receipt, bounded repair, and pass paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
