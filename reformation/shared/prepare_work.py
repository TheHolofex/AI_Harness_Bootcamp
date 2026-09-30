#!/usr/bin/env python3
"""Create an external, non-overwriting Module 02–09 exercise work folder."""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
import tempfile
from pathlib import Path

REFORMATION = Path(__file__).resolve().parents[1]
SHARED = {
    "02": ("case", "controls"), "03": ("case", "tools"), "04": ("case",),
    "05": ("controls", "corpus", "checks"), "06": ("batch", "workflow", "baseline"),
    "07": ("cases", "controls", "baseline"), "08": ("case", "controls"),
    "09": ("case", "controls", "baseline"),
}
SCRIPTS = {
    "02": (), "03": (), "04": ("render_review.py", "restore.py"), "05": (),
    "06": ("restore_rule.py",), "07": ("evaluate_pairs.py", "restore_baseline.py"),
    "08": (), "09": ("run_close.py", "check_package.py"),
}
EXCLUDED = {"figures", "__pycache__", "staff", "reference", "reviews", "evidence", "tests", "facilitator", "history", "assessment", "ACCESSIBILITY.md", "PUBLIC_RUBRIC.md", "CUSTODY_CONTRACT.md"}


def excluded(name: str, module_id: str) -> bool:
    return name in EXCLUDED or name.startswith((".", "MODULE_", "graded-", "answer-key")) or name.endswith((".pyc", ".pyo")) or (module_id == "08" and name == "verify_safeguards.py")


def require_regular(path: Path, boundary: Path) -> None:
    if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(boundary.resolve()):
        raise ValueError(f"missing, linked, or escaped required source: {path}")


def prepare(module_id: str, destination: Path, root: Path = REFORMATION) -> Path:
    if module_id not in SHARED:
        raise ValueError("module-id must be exactly two digits, 02–09")
    requested = destination.expanduser().absolute()
    if requested.exists() or requested.is_symlink():
        raise FileExistsError(f"destination already exists: {requested}")
    dest = requested.resolve()
    repository = root.resolve().parent
    if dest.is_relative_to(repository) or repository.is_relative_to(dest):
        raise ValueError(f"destination must not overlap the repository: {dest}")
    modules = list((root / "AI_Harness_Bootcamp_2").glob(f"module-{module_id}-*"))
    if len(modules) != 1 or modules[0].is_symlink() or not modules[0].is_dir():
        raise ValueError(f"expected one real Module {module_id} directory")
    module = modules[0]
    copies: list[tuple[Path, Path]] = []
    for name in SHARED[module_id]:
        subtree = module / "shared" / name
        if not subtree.is_dir() or subtree.is_symlink():
            raise ValueError(f"missing or linked required input directory: {subtree}")
        for directory, dirs, files in os.walk(subtree, followlinks=False):
            parent = Path(directory)
            dirs[:] = [entry for entry in dirs if not excluded(entry, module_id)]
            for entry in dirs:
                if (parent / entry).is_symlink():
                    raise ValueError(f"linked input directory: {parent / entry}")
            for entry in files:
                if excluded(entry, module_id):
                    continue
                source = parent / entry
                require_regular(source, module)
                copies.append((source, source.relative_to(module)))
    for name in SCRIPTS[module_id]:
        source = module / "scripts" / name
        require_regular(source, module)
        copies.append((source, Path("scripts") / name))
    if module_id == "09":
        source = module / "shared/PACKAGE.md"
        require_regular(source, module)
        copies.append((source, Path("shared/PACKAGE.md")))
    # Validation precedes every destination mutation. A staging failure never
    # leaves an apparently prepared work folder.
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".course-prepare-", dir=dest.parent) as temporary:
        stage = Path(temporary) / "work"
        (stage / "shared").mkdir(parents=True)
        (stage / "scripts").mkdir()
        (stage / "out").mkdir()
        for source, relative in copies:
            target = stage / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        if module_id == "04":
            baseline = stage / "baseline"
            baseline.mkdir()
            content = (stage / "scripts/render_review.py").read_bytes()
            (baseline / "render_review.py").write_bytes(content)
            (baseline / "render_review.py.sha256").write_text(hashlib.sha256(content).hexdigest() + "\n", encoding="utf-8")
        if dest.exists() or dest.is_symlink():
            raise FileExistsError(f"destination already exists: {dest}")
        # Reserve the destination exclusively; never let POSIX rename replace an
        # empty folder that appeared after preflight.
        dest.mkdir()
        try:
            for child in stage.iterdir():
                child.rename(dest / child.name)
        except OSError:
            # Keep the incomplete attempt rather than erase an unexpected edit.
            raise ValueError(f"copy interrupted; preserve {dest} and choose a new destination")
    return dest


def next_arguments(module_id: str) -> list[str]:
    python = str(Path(sys.executable).resolve())
    if module_id == "03":
        return [python, "shared/tools/hash_source.py", "shared/case/REL-001.md"]
    if module_id == "04":
        return [python, "scripts/render_review.py", "shared/case/ledger.json", "out/baseline.md"]
    if module_id == "06":
        return [python, "shared/workflow/route.py", "shared/batch/wave1.csv", "out/wave1-baseline.csv"]
    if module_id == "07":
        code = 'from pathlib import Path; print(Path("shared/controls/policy.json").read_text(encoding="utf-8"))'
    elif module_id == "09":
        code = 'from pathlib import Path; print(Path("shared/case/task-practice.json").read_text(encoding="utf-8"))'
    else:
        folder = "shared/corpus" if module_id == "05" else "shared/case"
        code = f'from pathlib import Path; print("\\n".join(p.as_posix() for p in sorted(Path("{folder}").rglob("*")) if p.is_file()))'
    return [python, "-c", code]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("module_id")
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    try:
        work = prepare(args.module_id, args.destination)
    except FileExistsError as error:
        print(f"HOLD: {error}")
        return 1
    except (OSError, ValueError) as error:
        print(f"HOLD: {error}; correct the prerequisite and use a new destination")
        return 2
    command = next_arguments(args.module_id)
    ps_quote = lambda value: "'" + str(value).replace("'", "''") + "'"
    shell_quote = lambda value: "'" + str(value).replace("'", "'\"'\"'") + "'"
    print(f"PASS: created {work}")
    print("Next (Bash/zsh, ordinary user):")
    print(f"cd {shell_quote(work)} && " + " ".join(shell_quote(part) for part in command))
    print("Next (PowerShell, ordinary user):")
    print(f"Set-Location -LiteralPath {ps_quote(work)} -ErrorAction Stop")
    if command[1] == "-c":
        print("@'\n" + command[2] + "\n'@ | & " + ps_quote(command[0]) + " -")
    else:
        print("& " + " ".join(ps_quote(part) for part in command))
    print("if ($LASTEXITCODE -ne 0) { throw 'HOLD: the next command failed; preserve this attempt.' }")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
