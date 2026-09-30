#!/usr/bin/env python3
"""Judge one three-row brief against the sources.json beside it.

Usage: hard_gates.py <brief.md>
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

FIELDS = ("Payload mass", "Gate time in source", "Gate time for desk")
SOURCE_KEYS = {
    "source_id",
    "locator",
    "text",
    "authoritative",
    "payload_kg",
    "gate_utc",
    "gate_local",
    "local_zone",
}
MASS_VALUE = re.compile(r"^(\d+) kg$")
UTC_VALUE = re.compile(r"^((?:[01]\d|2[0-3]):[0-5]\d) UTC$")
MDT_VALUE = re.compile(r"^((?:[01]\d|2[0-3]):[0-5]\d) MDT$")
TIME_TOKEN = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")


def hold(detail: str) -> dict:
    return {
        "format_ok": False,
        "mass_gate": "not_judged",
        "zone_gate": "not_judged",
        "passed": False,
        "reason": detail,
    }


def unique_object(pairs: list[tuple]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_sources(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    except (OSError, UnicodeError, ValueError) as error:
        raise ValueError(f"sources unreadable: {error}") from error
    if not isinstance(payload, dict):
        raise ValueError("sources must be an object")
    case_id = payload.get("case_id")
    sources = payload.get("sources")
    if not isinstance(case_id, str) or not re.fullmatch(r"PC-\d{2}", case_id):
        raise ValueError("sources case_id is missing")
    if not isinstance(sources, dict) or not sources:
        raise ValueError("sources must be a locator-keyed map")
    for locator, record in sources.items():
        if not isinstance(locator, str) or not isinstance(record, dict):
            raise ValueError("each source must be a locator-keyed record")
        if set(record) != SOURCE_KEYS or record.get("locator") != locator:
            raise ValueError(f"source record does not match the locator contract: {locator}")
        if not isinstance(record.get("authoritative"), bool):
            raise ValueError(f"authoritative must be boolean: {locator}")
        if not isinstance(record.get("text"), str) or not record["text"].strip():
            raise ValueError(f"source text is empty: {locator}")
        if not isinstance(record["source_id"], str) or not record["source_id"].strip():
            raise ValueError(f"source_id is empty: {locator}")
        if record["payload_kg"] is not None and (type(record["payload_kg"]) is not int or record["payload_kg"] < 0):
            raise ValueError(f"payload_kg must be a nonnegative integer or null: {locator}")
        for field in ("gate_utc", "gate_local"):
            value = record[field]
            if value is not None and (not isinstance(value, str) or not TIME_TOKEN.fullmatch(value)):
                raise ValueError(f"{field} must be HH:MM or null: {locator}")
        if record["local_zone"] is not None and not isinstance(record["local_zone"], str):
            raise ValueError(f"local_zone must be text or null: {locator}")
    authoritative = {locator for locator, record in sources.items() if record["authoritative"]}
    if authoritative != {f"SB-{case_id}#payload", f"SB-{case_id}#gate"}:
        raise ValueError("sources authoritative locators differ from this case's payload and gate")
    return payload


def split_row(line: str) -> list[str] | None:
    text = line.strip()
    if not text.startswith("|") or not text.endswith("|"):
        return None
    cells = [cell.strip() for cell in text[1:-1].split("|")]
    return cells


def parse_brief(text: str, case_id: str) -> tuple[list[dict] | None, str]:
    lines = [line.rstrip() for line in text.splitlines()]
    content = [line for line in lines if line.strip()]
    if not content or not content[0].startswith("# ") or re.findall(r"PC-\d+", content[0]) != [case_id]:
        return None, "format"
    table = [split_row(line) for line in content[1:]]
    if len(table) != 5 or any(row is None or len(row) != 3 for row in table):
        return None, "format"
    header, separator, *rows = table
    if header != ["Field", "Value", "Source"]:
        return None, "format"
    if any(not re.fullmatch(r":?-{3,}:?", cell) for cell in separator):
        return None, "format"
    if [row[0] for row in rows] != list(FIELDS):
        return None, "format"
    return [{"field": row[0], "value": row[1], "source": row[2]} for row in rows], ""


def one_authoritative(sources: dict, kind: str) -> dict | None:
    found = []
    for locator, record in sources.items():
        if not record["authoritative"] or record["locator"] != locator:
            continue
        if kind == "payload" and locator.endswith("#payload") and type(record["payload_kg"]) is int:
            found.append(record)
        if kind == "gate" and locator.endswith("#gate") and isinstance(record["gate_utc"], str):
            found.append(record)
    return found[0] if len(found) == 1 else None


def text_states(record: dict, needle: str) -> bool:
    return bool(re.search(r"(?<![\w.])" + re.escape(needle) + r"(?!\w)", record["text"]))


def judge_rows(rows: list[dict], packet: dict) -> dict:
    sources = packet["sources"]
    payload = one_authoritative(sources, "payload")
    gate = one_authoritative(sources, "gate")
    if payload is None or gate is None:
        return hold("format")
    by_field = {row["field"]: row for row in rows}
    mass = by_field["Payload mass"]
    source_time = by_field["Gate time in source"]
    desk_time = by_field["Gate time for desk"]
    mass_match = MASS_VALUE.fullmatch(mass["value"])
    mass_ok = bool(
        mass_match
        and int(mass_match.group(1)) == payload["payload_kg"]
        and mass["source"] == payload["locator"]
        and text_states(payload, f"{payload['payload_kg']} kg")
    )
    utc_match = UTC_VALUE.fullmatch(source_time["value"])
    mdt_match = MDT_VALUE.fullmatch(desk_time["value"])
    zone_ok = bool(
        utc_match
        and mdt_match
        and utc_match.group(1) == gate["gate_utc"]
        and mdt_match.group(1) == gate["gate_local"]
        and gate["local_zone"] == "MDT"
        and source_time["source"] == gate["locator"]
        and desk_time["source"] == gate["locator"]
        and text_states(gate, f"{gate['gate_utc']} UTC")
        and text_states(gate, f"{gate['gate_local']} MDT")
    )
    # A zone word in a different cell is not consulted. Bare clock tokens fail here.
    if TIME_TOKEN.fullmatch(source_time["value"]) or TIME_TOKEN.fullmatch(desk_time["value"]):
        zone_ok = False
    reasons = []
    if not mass_ok:
        reasons.append("sourced_mass")
    if not zone_ok:
        reasons.append("labeled_gate_time")
    return {
        "format_ok": True,
        "mass_gate": "pass" if mass_ok else "fail",
        "zone_gate": "pass" if zone_ok else "fail",
        "passed": not reasons,
        "reason": "pass" if not reasons else ";".join(reasons),
    }


def judge_brief(brief: Path) -> dict:
    sources_path = brief.parent / "sources.json"
    if not sources_path.is_file():
        return hold("missing sources")
    try:
        packet = load_sources(sources_path)
        text = brief.read_text(encoding="utf-8")
    except (OSError, UnicodeError, ValueError) as error:
        return hold(str(error))
    rows, reason = parse_brief(text, packet["case_id"])
    if rows is None:
        return hold(reason)
    return judge_rows(rows, packet)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: hard_gates.py <brief.md>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print("HOLD: missing input", file=sys.stderr)
        return 1
    result = judge_brief(path)
    if result["passed"]:
        print("PASS")
        return 0
    print(f"HOLD: {result['reason']}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
