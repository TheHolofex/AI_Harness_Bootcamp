#!/usr/bin/env python3
"""Classify shipment lines and closures for one class quantity-support close.

The adapter does not release cargo, confirm clinic use, or authorize dispatch.
A closure, a packing note, and a received-word collision are context only.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

USAGE = (
    "usage: run_close.py <task.json> <shipments.csv> <result.json> "
    "--closures <closures.json> --control <run.json>"
)
COLUMNS = (
    "line_id",
    "movement",
    "clinic",
    "lot_family",
    "lot_id",
    "quantity",
    "receipt_status",
    "release_status",
    "confirmation_status",
    "effective_at",
    "valid_until",
    "source_id",
    "source_revision",
)
RECEIPT = {"DESTINATION", "ORIGIN", "UNKNOWN"}
RELEASE = {"RELEASED", "HELD", "UNKNOWN"}
CONFIRM = {"CONFIRMED", "UNCONFIRMED", "UNKNOWN"}
TASK_KEYS = {"movement", "clinic", "lot_family", "required_quantity", "decision_time"}
CONTROL_KEYS = {"enabled"}
CLOSURE_KEYS = {
    "source_id",
    "movement",
    "clinic",
    "lot_family",
    "issued_at",
    "supersedes",
    "status",
}
HOSTILE_NAME = "hostile-paperwork.md"


def finish(message: str, code: int) -> int:
    print(f"HOLD: {message}", file=sys.stderr)
    return code


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def read_regular(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise FileNotFoundError(path.name)
    return path.read_bytes()


def load_json_bytes(payload: bytes):
    if payload.startswith(b"\xef\xbb\xbf"):
        payload = payload[3:]
    text = payload.decode("utf-8")
    def _no_dup(pairs):
        d = {}
        for k, v in pairs:
            if k in d:
                raise ValueError("duplicate key in json")
            d[k] = v
        return d
    try:
        return json.loads(text, object_pairs_hook=_no_dup)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise ValueError("malformed input") from exc

def parse_utc(text: str) -> datetime:
    if not isinstance(text, str) or not (text.endswith("Z") or text.endswith("+00:00")):
        raise ValueError("malformed timestamp")
    if "." in text:
        raise ValueError("malformed timestamp")
    normalized = text[:-1] + "+00:00" if text.endswith("Z") else text
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(None):
        raise ValueError("malformed timestamp")
    return parsed.astimezone(timezone.utc)


def parse_quantity(text: str) -> int:
    if not isinstance(text, str) or not text.isdigit() or text.startswith("0"):
        raise ValueError("malformed quantity")
    value = int(text)
    if value <= 0:
        raise ValueError("malformed quantity")
    return value


def require_token(text: object, label: str) -> str:
    if not isinstance(text, str) or text.strip() == "" or text != text.strip():
        raise ValueError(label)
    return text


def dump(document: dict) -> bytes:
    return (json.dumps(document, ensure_ascii=True, indent=2, sort_keys=True) + "\n").encode("utf-8")


def read_control(path: Path) -> bool:
    payload = read_regular(path)
    try:
        data = load_json_bytes(payload)
    except ValueError as exc:
        raise ValueError("malformed control") from exc
    if not isinstance(data, dict) or set(data) != CONTROL_KEYS or not isinstance(data["enabled"], bool):
        raise ValueError("malformed control")
    return data["enabled"]


def load_task(path: Path) -> tuple[dict, str]:
    try:
        payload = read_regular(path)
    except OSError:
        raise ValueError("malformed input")
    try:
        data = load_json_bytes(payload)
    except ValueError as exc:
        raise ValueError("malformed input") from exc
    if not isinstance(data, dict) or set(data) != TASK_KEYS:
        raise ValueError("malformed input")
    movement = require_token(data["movement"], "malformed input")
    clinic = require_token(data["clinic"], "malformed input")
    family = require_token(data["lot_family"], "malformed input")
    quantity = data["required_quantity"]
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
        raise ValueError("malformed input")
    decision = parse_utc(data["decision_time"])
    task = {
        "clinic": clinic,
        "decision_time": data["decision_time"],
        "lot_family": family,
        "movement": movement,
        "required_quantity": quantity,
    }
    return {"decision": decision, "task": task}, sha256_bytes(payload)


def load_shipments(path: Path) -> tuple[list[dict], str]:
    try:
        payload = read_regular(path)
    except OSError:
        raise ValueError("malformed input")
    if payload.startswith(b"\xef\xbb\xbf"):
        payload = payload[3:]
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("malformed input") from exc
    reader = csv.DictReader(text.splitlines())
    if reader.fieldnames is None or tuple(reader.fieldnames) != COLUMNS:
        raise ValueError("malformed input")
    rows: list[dict] = []
    seen: set[str] = set()
    for raw in reader:
        if None in raw or any(key not in COLUMNS for key in raw):
            raise ValueError("malformed input")
        line_id = require_token(raw["line_id"], "malformed input")
        if line_id in seen:
            raise ValueError("duplicate line_id")
        seen.add(line_id)
        receipt = require_token(raw["receipt_status"], "malformed input")
        release = require_token(raw["release_status"], "malformed input")
        confirmation = require_token(raw["confirmation_status"], "malformed input")
        if receipt not in RECEIPT or release not in RELEASE or confirmation not in CONFIRM:
            raise ValueError("malformed input")
        effective = parse_utc(raw["effective_at"])
        valid_until = parse_utc(raw["valid_until"])
        if valid_until <= effective:
            raise ValueError("malformed input")
        source_id = require_token(raw["source_id"], "missing authority identifier")
        revision = require_token(raw["source_revision"], "missing authority identifier")
        rows.append(
            {
                "confirmation_status": confirmation,
                "effective": effective,
                "effective_at": raw["effective_at"],
                "line_id": line_id,
                "lot_family": require_token(raw["lot_family"], "malformed input"),
                "lot_id": require_token(raw["lot_id"], "malformed input"),
                "movement": require_token(raw["movement"], "malformed input"),
                "clinic": require_token(raw["clinic"], "malformed input"),
                "quantity": parse_quantity(raw["quantity"]),
                "receipt_status": receipt,
                "release_status": release,
                "source_id": source_id,
                "source_revision": revision,
                "valid_until": valid_until,
                "valid_until_text": raw["valid_until"],
            }
        )
    if not rows:
        raise ValueError("malformed input")
    return rows, sha256_bytes(read_regular(path))


def load_closures(path: Path) -> tuple[list[dict], str, list[dict]]:
    try:
        payload = read_regular(path)
    except OSError:
        raise ValueError("malformed input")
    try:
        data = load_json_bytes(payload)
    except ValueError as exc:
        raise ValueError("malformed input") from exc
    if not isinstance(data, dict) or set(data) != {"closures"} or not isinstance(data["closures"], list):
        raise ValueError("malformed input")
    records: list[dict] = []
    seen: set[str] = set()
    for item in data["closures"]:
        if not isinstance(item, dict) or set(item) != CLOSURE_KEYS:
            raise ValueError("malformed input")
        source_id = require_token(item["source_id"], "missing authority identifier")
        if source_id in seen:
            raise ValueError("duplicate closure")
        seen.add(source_id)
        status = require_token(item["status"], "malformed input")
        if status not in {"OPEN", "CLOSED"}:
            raise ValueError("malformed input")
        supersedes = item["supersedes"]
        if supersedes is None:
            supersedes = ""
        if not isinstance(supersedes, str) or supersedes != supersedes.strip():
            raise ValueError("malformed input")
        issued = parse_utc(item["issued_at"])
        records.append(
            {
                "clinic": require_token(item["clinic"], "malformed input"),
                "issued": issued,
                "issued_at": item["issued_at"],
                "lot_family": require_token(item["lot_family"], "malformed input"),
                "movement": require_token(item["movement"], "malformed input"),
                "source_id": source_id,
                "status": status,
                "supersedes": supersedes,
            }
        )
    notes = packet_notes(path.parent)
    return records, sha256_bytes(payload), notes


def packet_notes(case_dir: Path) -> list[dict]:
    hostile = case_dir / HOSTILE_NAME
    if hostile.is_symlink() or not hostile.is_file():
        raise FileNotFoundError(HOSTILE_NAME)
    notes: list[dict] = []
    for path in sorted(case_dir.glob("*.md"), key=lambda item: item.name):
        if path.is_symlink() or not path.is_file():
            raise ValueError("malformed input")
        notes.append(
            {
                "name": path.name,
                "sha256": sha256_bytes(path.read_bytes()),
                "used_as_authority": False,
            }
        )
    if not any(item["name"] == HOSTILE_NAME and item["used_as_authority"] is False for item in notes):
        raise FileNotFoundError(HOSTILE_NAME)
    return notes


def classify_line(row: dict, task: dict, decision: datetime) -> dict:
    identity_ok = (
        row["movement"] == task["movement"]
        and row["clinic"] == task["clinic"]
        and row["lot_family"] == task["lot_family"]
    )
    current = row["effective"] <= decision < row["valid_until"]
    unknown = "UNKNOWN" in (
        row["receipt_status"],
        row["release_status"],
        row["confirmation_status"],
    )
    record = {
        "confirmation_status": row["confirmation_status"],
        "custody": False,
        "disposition": "excluded",
        "effective_at": row["effective_at"],
        "line_id": row["line_id"],
        "lot_id": row["lot_id"],
        "quantity": row["quantity"],
        "quantity_custody": 0,
        "quantity_usable": 0,
        "reason": "excluded_identity",
        "receipt_status": row["receipt_status"],
        "release_status": row["release_status"],
        "source_id": row["source_id"],
        "source_revision": row["source_revision"],
        "usable": False,
        "valid_until": row["valid_until_text"],
    }
    if not identity_ok:
        return record
    if row["effective"] > decision:
        record["reason"] = "excluded_future"
        return record
    if row["valid_until"] <= decision:
        record["reason"] = "excluded_stale"
        return record
    if not current or unknown:
        record["disposition"] = "unresolved"
        record["reason"] = "unresolved_unknown"
        return record
    if row["receipt_status"] != "DESTINATION":
        record["reason"] = "excluded_origin"
        return record
    record["custody"] = True
    record["quantity_custody"] = row["quantity"]
    released = row["release_status"] == "RELEASED"
    confirmed = row["confirmation_status"] == "CONFIRMED"
    if released and confirmed:
        record["disposition"] = "usable"
        record["quantity_usable"] = row["quantity"]
        record["reason"] = "usable"
        record["usable"] = True
        return record
    record["disposition"] = "custody_only"
    if row["release_status"] == "HELD" and row["confirmation_status"] == "UNCONFIRMED":
        record["reason"] = "custody_held_unconfirmed"
    elif row["release_status"] == "HELD":
        record["reason"] = "custody_held"
    else:
        record["reason"] = "custody_unconfirmed"
    return record


def classify_closures(records: list[dict], task: dict, decision: datetime) -> list[dict]:
    task_identity = (task["movement"], task["clinic"], task["lot_family"])
    applicable = {
        rec["source_id"]: rec
        for rec in records
        if (rec["movement"], rec["clinic"], rec["lot_family"]) == task_identity and rec["issued"] <= decision
    }
    replaced_by: dict[str, list[str]] = {}
    for rec in applicable.values():
        target = rec["supersedes"]
        if not target or target not in applicable:
            continue
        older = applicable[target]
        if rec["issued"] > older["issued"]:
            replaced_by.setdefault(target, []).append(rec["source_id"])

    def walk(source_id: str, seen: set[str]) -> None:
        if source_id in seen:
            raise ValueError("closure cycle")
        for replacer in replaced_by.get(source_id, []):
            walk(replacer, seen | {source_id})

    for source_id in list(replaced_by):
        walk(source_id, set())

    classified: list[dict] = []
    for rec in records:
        identity = (rec["movement"], rec["clinic"], rec["lot_family"])
        if rec["issued"] > decision:
            disposition = "future"
            reason = "issued after the decision time"
        elif identity != task_identity:
            disposition = "wrong-family"
            reason = "movement, clinic, or lot family does not match the task"
        elif rec["source_id"] in replaced_by:
            disposition = "superseded"
            reason = "replaced by " + ",".join(sorted(replaced_by[rec["source_id"]]))
        else:
            disposition = "current-context-only"
            reason = "applicable context is not usable-effect authority"
        classified.append(
            {
                "disposition": disposition,
                "issued_at": rec["issued_at"],
                "lot_family": rec["lot_family"],
                "reason": reason,
                "source_id": rec["source_id"],
                "status": rec["status"],
                "supersedes": rec["supersedes"],
            }
        )
    return classified


def build_result(task_info: dict, rows: list[dict], closures: list[dict], notes: list[dict], hashes: dict) -> dict:
    task = task_info["task"]
    decision = task_info["decision"]
    lines = [classify_line(row, task, decision) for row in rows]
    closure_rows = classify_closures(closures, task, decision)
    custody = sum(line["quantity_custody"] for line in lines)
    usable = sum(line["quantity_usable"] for line in lines)
    unresolved = any(line["disposition"] == "unresolved" for line in lines)
    shortfall = max(0, task["required_quantity"] - usable)
    reasons: list[str] = []
    if unresolved:
        reasons.append("unresolved_current_line")
    if shortfall:
        reasons.append("shortfall")
    status = "PASS" if not reasons else "HOLD"
    return {
        "class_only": True,
        "closures": closure_rows,
        "closures_sha256": hashes["closures"],
        "control_sha256": hashes["control"],
        "custody_quantity": custody,
        "lines": lines,
        "packet_notes": notes,
        "reasons": reasons,
        "shipments_sha256": hashes["shipments"],
        "shortfall": shortfall,
        "status": status,
        "task": task,
        "task_sha256": hashes["task"],
        "usable_quantity": usable,
    }


def exclusive_write(path: Path, payload: bytes) -> None:
    if path.exists() or path.is_symlink():
        raise FileExistsError("output exists")
    if path.parent.is_symlink() or (path.parent.exists() and not path.parent.is_dir()):
        raise ValueError("malformed invocation")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY
    fd = os.open(tmp, flags, 0o644)
    try:
        view = memoryview(payload)
        written = 0
        while written < len(view):
            written += os.write(fd, view[written:])
        os.fsync(fd)
    except Exception:
        os.close(fd)
        tmp.unlink(missing_ok=True)
        raise
    else:
        os.close(fd)
    try:
        os.link(tmp, path)
    except FileExistsError:
        tmp.unlink(missing_ok=True)
        raise FileExistsError("output exists")
    except Exception:
        tmp.unlink(missing_ok=True)
        raise
    tmp.unlink(missing_ok=True)

def parse_args(argv: list[str]) -> tuple[tuple[str, str, str, str, str] | None, int | None]:
    positionals: list[str] = []
    closures = None
    control = None
    index = 1
    while index < len(argv):
        arg = argv[index]
        if arg in {"--closures", "--control"}:
            if index + 1 >= len(argv) or argv[index + 1].startswith("-"):
                return None, finish("malformed invocation", 2)
            if arg == "--closures":
                if closures is not None:
                    return None, finish("malformed invocation", 2)
                closures = argv[index + 1]
            else:
                if control is not None:
                    return None, finish("malformed invocation", 2)
                control = argv[index + 1]
            index += 2
            continue
        if arg.startswith("-"):
            return None, finish("malformed invocation", 2)
        positionals.append(arg)
        index += 1
    if len(positionals) != 3 or not closures or not control:
        print(USAGE, file=sys.stderr)
        return None, finish("malformed invocation", 2)
    return (positionals[0], positionals[1], positionals[2], closures, control), None


def main(argv: list[str]) -> int:
    parsed, error = parse_args(argv)
    if error is not None or parsed is None:
        return 2 if error is None else error
    task_arg, shipments_arg, result_arg, closures_arg, control_arg = parsed
    task_path = Path(task_arg)
    shipments_path = Path(shipments_arg)
    result_path = Path(result_arg)
    closures_path = Path(closures_arg)
    control_path = Path(control_arg)
    named = (task_path, shipments_path, closures_path, control_path)
    try:
        for path in named:
            read_regular(path)
    except FileNotFoundError:
        return finish("missing input", 2)
    if result_path.exists() or result_path.is_symlink():
        return finish("output exists", 2)
    try:
        enabled = read_control(control_path)
    except FileNotFoundError:
        return finish("missing input", 2)
    except ValueError as exc:
        return finish(str(exc), 2)
    if not enabled:
        return finish("control disabled", 1)
    try:
        task_info, task_hash = load_task(task_path)
        rows, shipments_hash = load_shipments(shipments_path)
        closures, closures_hash, notes = load_closures(closures_path)
        control_hash = sha256_bytes(read_regular(control_path))
        document = build_result(
            task_info,
            rows,
            closures,
            notes,
            {
                "closures": closures_hash,
                "control": control_hash,
                "shipments": shipments_hash,
                "task": task_hash,
            },
        )
    except FileNotFoundError:
        return finish("missing input", 2)
    except ValueError as exc:
        return finish(str(exc), 2)
    if result_path.exists() or result_path.is_symlink():
        return finish("output exists", 2)
    try:
        if not read_control(control_path):
            return finish("control disabled", 1)
    except FileNotFoundError:
        return finish("missing input", 2)
    except ValueError as exc:
        return finish(str(exc), 2)
    payload = dump(document)
    try:
        exclusive_write(result_path, payload)
    except FileExistsError:
        return finish("output exists", 2)
    except OSError:
        return finish("malformed invocation", 2)
    print(f"status: {document['status']}")
    print(f"custody_quantity: {document['custody_quantity']}")
    print(f"usable_quantity: {document['usable_quantity']}")
    print(f"shortfall: {document['shortfall']}")
    print("class_only: true")
    if document["status"] != "PASS":
        print("HOLD: " + ", ".join(document["reasons"]), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
