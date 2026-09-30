#!/usr/bin/env python3
"""Compare baseline and two candidates across the frozen case directory.

Usage: evaluate_pairs.py <case-dir> <policy.json> <results.csv>
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

VARIANTS = ("baseline", "candidate-a", "candidate-b")
COLUMNS = [
    "case_id",
    "variant",
    "format_ok",
    "mass_gate",
    "zone_gate",
    "passed",
    "reason",
    "source_sha256",
    "brief_sha256",
    "config_sha256",
]
MATERIAL = ["Payload mass", "Gate time in source", "Gate time for desk"]
GATES = ["sourced_mass", "labeled_gate_time"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hold(message: str) -> int:
    print(f"HOLD: {message}", file=sys.stderr)
    return 1


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_gates(policy_path: Path):
    gates_path = policy_path.parent / "hard_gates.py"
    if not gates_path.is_file():
        raise ValueError("hard_gates.py is not beside policy.json")
    spec = importlib.util.spec_from_file_location("course_hard_gates", gates_path)
    if spec is None or spec.loader is None:
        raise ValueError("hard_gates.py could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expected_cases(case_dir: Path) -> list[str]:
    return [f"PC-{number:02d}" for number in range(1, 41)]


def validate_policy(policy: dict, case_dir: Path, manifests: dict[str, Path]) -> None:
    if not isinstance(policy, dict):
        raise ValueError("policy must be an object")
    if policy.get("schema_version") != 1:
        raise ValueError("policy schema_version must be 1")
    case_ids = policy.get("case_ids")
    if not isinstance(case_ids, list) or any(not isinstance(value, str) for value in case_ids) or len(case_ids) != len(set(case_ids)):
        raise ValueError("policy case_ids are missing or duplicated")
    if case_ids != expected_cases(case_dir):
        raise ValueError("policy case_ids are not PC-01 through PC-40")
    present = sorted(path.name for path in case_dir.iterdir() if path.is_dir())
    if present != case_ids:
        raise ValueError("case directory does not contain exactly PC-01 through PC-40")
    config = policy.get("config_sha256")
    if not isinstance(config, dict) or set(config) != set(VARIANTS):
        raise ValueError("config_sha256 must map baseline, candidate-a, and candidate-b")
    for variant, path in manifests.items():
        actual = sha256(path)
        if config.get(variant) != actual:
            raise ValueError(f"config hash mismatch for {variant}")
    if policy.get("material_fields") != MATERIAL:
        raise ValueError("material_fields do not match the three brief rows")
    if policy.get("hard_gates") != GATES:
        raise ValueError("hard_gates do not match sourced_mass and labeled_gate_time")
    if policy.get("aggregation") != "any_violation_rejects":
        raise ValueError("aggregation must be any_violation_rejects")
    if policy.get("exclusions") != []:
        raise ValueError("exclusions must be empty")
    if policy.get("cost_proxy") != "failed_case_count":
        raise ValueError("cost_proxy must be failed_case_count")


def manifest_paths(policy_path: Path) -> dict[str, Path]:
    folder = policy_path.parent
    return {variant: folder / f"{variant}.json" for variant in VARIANTS}


def load_manifest(path: Path, variant: str) -> str:
    payload = load_json(path)
    if not isinstance(payload, dict):
        raise ValueError(f"{path.name} must be an object")
    if payload.get("variant") != variant or not isinstance(payload.get("brief_filename"), str):
        raise ValueError(f"{path.name} is not the {variant} batch manifest")
    filename = payload["brief_filename"]
    if filename != f"{variant}.md" or "/" in filename or "\\" in filename:
        raise ValueError(f"{path.name} brief_filename is not the variant brief")
    return filename


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print("usage: evaluate_pairs.py <case-dir> <policy.json> <results.csv>", file=sys.stderr)
        return 2
    case_dir = Path(argv[1])
    policy_path = Path(argv[2])
    results_path = Path(argv[3])
    if results_path.exists() or results_path.is_symlink():
        return hold("output exists; move it aside and choose a new results file")
    if not case_dir.is_dir() or not policy_path.is_file():
        return hold("missing case directory or policy.json")
    try:
        policy = load_json(policy_path)
        manifests = manifest_paths(policy_path)
        if any(not path.is_file() for path in manifests.values()):
            return hold("a batch manifest is missing beside policy.json")
        validate_policy(policy, case_dir, manifests)
        filenames = {variant: load_manifest(path, variant) for variant, path in manifests.items()}
        gates = load_gates(policy_path)
        rows = []
        for case_id in policy["case_ids"]:
            folder = case_dir / case_id
            sources = folder / "sources.json"
            if not sources.is_file():
                return hold(f"missing sources.json for {case_id}")
            packet = gates.load_sources(sources)
            if packet["case_id"] != case_id:
                return hold(f"{case_id}: sources.json belongs to {packet['case_id']}")
            source_hash = sha256(sources)
            for variant in VARIANTS:
                brief = folder / filenames[variant]
                if not brief.is_file():
                    return hold(f"missing {variant} brief for {case_id}")
                raw_brief = brief.read_bytes()
                parsed, reason = gates.parse_brief(raw_brief.decode("utf-8"), case_id)
                judged = gates.hold(reason) if parsed is None else gates.judge_rows(parsed, packet)
                rows.append(
                    {
                        "case_id": case_id,
                        "variant": variant,
                        "format_ok": "true" if judged["format_ok"] else "false",
                        "mass_gate": judged["mass_gate"],
                        "zone_gate": judged["zone_gate"],
                        "passed": "true" if judged["passed"] else "false",
                        "reason": judged["reason"],
                        "source_sha256": source_hash,
                        "brief_sha256": hashlib.sha256(raw_brief).hexdigest(),
                        "config_sha256": policy["config_sha256"][variant],
                    }
                )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, AttributeError) as error:
        return hold(str(error))
    if len(rows) != 120 or len({(row["case_id"], row["variant"]) for row in rows}) != 120:
        return hold("evaluation did not account for 120 distinct rows")
    try:
        results_path.parent.mkdir(parents=True, exist_ok=True)
        with results_path.open("x", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=COLUMNS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
    except OSError as error:
        return hold(f"cannot create a new results file: {error}")
    print("EVALUATED 120")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
