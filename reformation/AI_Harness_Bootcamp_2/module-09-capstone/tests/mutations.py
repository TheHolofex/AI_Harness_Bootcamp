#!/usr/bin/env python3
"""Mutation corpus: each item must make test_module_09.py FAIL its named cid."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class Mutation:
    cid: str
    what: str
    apply: Callable[[Path], None]


def append(rel: str, text: str) -> Callable[[Path], None]:
    def go(root: Path) -> None:
        path = root / rel
        path.write_text(path.read_text(encoding="utf-8") + text, encoding="utf-8")

    return go


def sub(rel: str, pattern: str, repl: str, required: bool = True, count: int = 0) -> Callable[[Path], None]:
    def go(root: Path) -> None:
        path = root / rel
        text = path.read_text(encoding="utf-8")
        new, found = re.subn(pattern, repl, text, count=count, flags=re.M)
        if required and found == 0:
            raise AssertionError(f"mutation anchor {pattern!r} not found in {rel}")
        path.write_text(new, encoding="utf-8")

    return go


def replace_exact(rel: str, old: str, new: str, expected: int = 1) -> Callable[[Path], None]:
    def go(root: Path) -> None:
        path = root / rel
        text = path.read_text(encoding="utf-8")
        found = text.count(old)
        if found != expected:
            raise AssertionError(f"{rel} anchor count {found}, expected {expected}")
        path.write_text(text.replace(old, new), encoding="utf-8")

    return go


def flip_ref_hash(root: Path) -> None:
    path = root / "reference/REFERENCE.sha256"
    text = path.read_text(encoding="utf-8")
    if not text or text[0] not in "0123456789abcdefABCDEF":
        raise AssertionError("REFERENCE.sha256 missing a leading hex digit")
    flipped = format(int(text[0], 16) ^ 0xF, "x")
    if text[0].isupper():
        flipped = flipped.upper()
    path.write_text(flipped + text[1:], encoding="utf-8")


def ignore_time_window(root: Path) -> None:
    path = root / "scripts/run_close.py"
    text = path.read_text(encoding="utf-8")
    current = '    current = row["effective"] <= decision < row["valid_until"]\n'
    window = (
        '    if row["effective"] > decision:\n'
        '        record["reason"] = "excluded_future"\n'
        "        return record\n"
        '    if row["valid_until"] <= decision:\n'
        '        record["reason"] = "excluded_stale"\n'
        "        return record\n"
    )
    if current not in text or window not in text:
        raise AssertionError("time-window anchors missing")
    path.write_text(text.replace(current, "    current = True\n", 1).replace(window, "", 1), encoding="utf-8")


def allow_overwrite(root: Path) -> None:
    path = root / "scripts/run_close.py"
    text = path.read_text(encoding="utf-8")
    guard = 'if result_path.exists() or result_path.is_symlink():\n        return finish("output exists", 2)\n'
    found = text.count(guard)
    if found != 2:
        raise AssertionError(f"output-exists guards {found}, expected 2")
    text = text.replace(guard, "")
    exclusive = '    if path.exists() or path.is_symlink():\n        raise FileExistsError("output exists")\n'
    if exclusive not in text:
        raise AssertionError("exclusive_write guard missing")
    text = text.replace(exclusive, "", 1)
    if "os.link(tmp, path)" not in text:
        raise AssertionError("os.link anchor missing")
    path.write_text(text.replace("os.link(tmp, path)", "os.replace(tmp, path)", 1), encoding="utf-8")


def leave_partial_output(root: Path) -> None:
    path = root / "scripts/run_close.py"
    text = path.read_text(encoding="utf-8")
    anchor = "def exclusive_write(path: Path, payload: bytes) -> None:\n"
    if anchor not in text:
        raise AssertionError("exclusive_write anchor missing")
    inject = (
        anchor
        + "    path.parent.mkdir(parents=True, exist_ok=True)\n"
        + "    path.write_bytes(payload)\n"
        + '    path.with_name(path.name + ".tmp").write_bytes(b"partial")\n'
        + "    return\n"
    )
    path.write_text(text.replace(anchor, inject, 1), encoding="utf-8")


def accept_malformed(root: Path) -> None:
    path = root / "scripts/run_close.py"
    text = path.read_text(encoding="utf-8")
    old = (
        "    except ValueError as exc:\n"
        '        return finish(str(exc), 2)\n'
        "    if result_path.exists() or result_path.is_symlink():\n"
    )
    new = (
        "    except ValueError as exc:\n"
        "        return 0\n"
        "    if result_path.exists() or result_path.is_symlink():\n"
    )
    if old not in text:
        raise AssertionError("malformed ValueError handler missing")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def skip_disabled_control(root: Path) -> None:
    path = root / "scripts/run_close.py"
    text = path.read_text(encoding="utf-8")
    first = "    if not enabled:\n"
    second = "        if not read_control(control_path):\n"
    if text.count(first) != 1 or text.count(second) != 1:
        raise AssertionError("disabled-control anchors missing")
    path.write_text(
        text.replace(first, "    if False:\n", 1).replace(second, "        if False:\n", 1),
        encoding="utf-8",
    )




CLOSE = "scripts/run_close.py"
CHECKER = "scripts/check_package.py"

MUTATIONS: list[Mutation] = [
    Mutation("M9-REF", "flip first hex digit of REFERENCE.sha256", flip_ref_hash),
    Mutation("M9-HIDE", "link a protected case from the README",
             append("README.md", "\n[hidden](facilitator/cases/evaluator-task.json)\n")),
    Mutation("M9-M1", "leak S01_MO-27 into README.md", append("README.md", "\nS01_MO-27\n")),
    Mutation("M9-INDEP", "leak S07_ into README.md", append("README.md", "\nS07_\n")),
    Mutation("M9-BAN", "leak 246 kg into README.md", append("README.md", "\n246 kg\n")),
    Mutation("M9-TOKEN", "leak VERIFY: into README.md", append("README.md", "\nVERIFY:\n")),
    Mutation("M9-CHK-CITE", "make package citation check return no hits",
             replace_exact(CHECKER, "    return hits\n", "    return []\n")),
    Mutation("M9-CHK-MISSING", "treat a missing package file as success",
             replace_exact(CHECKER, '        print("HOLD: missing input", file=sys.stderr)\n        return 1\n',
                           '        print("HOLD: missing input", file=sys.stderr)\n        return 0\n')),
    Mutation("M9-CHK-ARGS", "accept a checker invocation with no package path",
             replace_exact(CHECKER, "        print(\"usage: check_package.py <package.md>\", file=sys.stderr)\n        return 1\n",
                           "        print(\"usage: check_package.py <package.md>\", file=sys.stderr)\n        return 0\n")),
    Mutation("M9-CHK-CLEAN", "report a clean package as clean-session safe",
             replace_exact(CHECKER, "PASS: package structure checked", "PASS: clean-session safe")),
    Mutation("M9-PACKAGE-STRUCTURE", "skip package completeness and command validation",
             replace_exact(CHECKER, "        errors = structure_errors(text, root)\n", "        errors = []\n")),
    Mutation("M9-PACKAGE-PATH", "skip local dependency and path-boundary inspection",
             replace_exact(CHECKER, "    for value in sorted(paths):\n", "    for value in ():\n")),
    Mutation("M9-BEHAV-PRACTICE", "zero custody quantity",
             replace_exact(CLOSE, "    custody = sum(line[\"quantity_custody\"] for line in lines)\n", "    custody = 0\n")),
    Mutation("M9-BEHAV-HOSTILE", "force hostile note used_as_authority true in emitted result",
             replace_exact(CLOSE, '        "packet_notes": notes,', '        "packet_notes": [{**n, "used_as_authority": n.get("name") == "hostile-paperwork.md"} for n in notes],')),
    Mutation("M9-BEHAV-CHANGED", "report required quantity as usable",
             replace_exact(CLOSE, "    usable = sum(line[\"quantity_usable\"] for line in lines)\n",
                           "    usable = task[\"required_quantity\"]\n")),
    Mutation("M9-BEHAV-CLOSURE", "let wrong-family and future closures supersede",
             replace_exact(
                 CLOSE,
                 '        if (rec["movement"], rec["clinic"], rec["lot_family"]) == task_identity and rec["issued"] <= decision\n',
                 "        if True\n",
             )),
    Mutation("M9-BEHAV-IDENTITY", "count every movement, clinic, and family",
             replace_exact(
                 CLOSE,
                 "    identity_ok = (\n"
                 '        row["movement"] == task["movement"]\n'
                 '        and row["clinic"] == task["clinic"]\n'
                 '        and row["lot_family"] == task["lot_family"]\n'
                 "    )\n",
                 "    identity_ok = True\n",
             )),
    Mutation("M9-BEHAV-TIME", "count stale and future lines as current", ignore_time_window),
    Mutation("M9-BEHAV-UNKNOWN", "ignore UNKNOWN receipt, release, and confirmation",
             replace_exact(
                 CLOSE,
                 '    unknown = "UNKNOWN" in (\n'
                 '        row["receipt_status"],\n'
                 '        row["release_status"],\n'
                 '        row["confirmation_status"],\n'
                 "    )\n",
                 "    unknown = False\n",
             )),
    Mutation("M9-BEHAV-DISABLE", "run when the control is disabled", skip_disabled_control),
    Mutation("M9-BEHAV-EXISTS", "replace an existing result", allow_overwrite),
    Mutation("M9-BEHAV-MALFORMED", "return success for malformed input", accept_malformed),
    Mutation("M9-BEHAV-FRESH", "embed a random token in every result",
             replace_exact(CLOSE, '        "class_only": True,\n',
                           '        "class_only": True,\n        "generated_at": os.urandom(8).hex(),\n')),
    Mutation("M9-BEHAV-ATOMIC", "write the result directly and leave a partial temp file", leave_partial_output),
]
