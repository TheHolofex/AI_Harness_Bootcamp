#!/usr/bin/env python3
"""Trusted, data-only verifier for the Project Organizer ledger and source packet."""

from __future__ import annotations

import csv
import hashlib
import re
import sqlite3
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Dict, List, Mapping, Sequence


DATABASE_NAME = "project_ledger.sqlite3"
SOURCE_FILES = (
    "01_project_charter.md",
    "02_deliverables.csv",
    "03_dependency_notes.md",
    "04_decision_log.md",
    "05_status_updates.md",
    "06_source_register.csv",
)
EXPECTED_COLUMNS = {
    "sources": ("source_id", "path", "title", "source_type", "updated_at", "authority", "sha256"),
    "projects": ("project_id", "name", "outcome", "success_measure", "target_date", "sponsor", "project_lead", "current_phase", "source_id"),
    "deliverables": ("deliverable_id", "project_id", "title", "owner", "reviewer", "status", "priority", "source_inputs", "output_path", "acceptance_condition", "due_date", "dependency_summary", "blocked_reason", "next_commitment", "source_id"),
    "dependencies": ("dependency_id", "project_id", "predecessor_deliverable_id", "successor_deliverable_id", "dependency_type", "condition", "status", "owner", "source_id"),
    "decisions": ("decision_id", "project_id", "title", "question", "decision_owner", "needed_by", "status", "options", "recommendation", "consequence_of_delay", "source_id"),
    "updates": ("update_id", "project_id", "update_date", "author", "deliverable_id", "summary", "status_signal", "next_action", "source_id"),
}
EXPECTED_COUNTS = {
    "sources": 6,
    "projects": 1,
    "deliverables": 4,
    "dependencies": 4,
    "decisions": 3,
    "updates": 5,
}
EXPECTED_FOREIGN_KEYS = {
    "sources": set(),
    "projects": {("source_id", "sources", "source_id")},
    "deliverables": {("project_id", "projects", "project_id"), ("source_id", "sources", "source_id")},
    "dependencies": {
        ("project_id", "projects", "project_id"),
        ("predecessor_deliverable_id", "deliverables", "deliverable_id"),
        ("successor_deliverable_id", "deliverables", "deliverable_id"),
        ("source_id", "sources", "source_id"),
    },
    "decisions": {("project_id", "projects", "project_id"), ("source_id", "sources", "source_id")},
    "updates": {
        ("project_id", "projects", "project_id"),
        ("deliverable_id", "deliverables", "deliverable_id"),
        ("source_id", "sources", "source_id"),
    },
}
EXPECTED_INDEXES = {
    "idx_deliverables_project_status": ("project_id", "status", "due_date", "deliverable_id"),
    "idx_dependencies_successor": ("successor_deliverable_id", "predecessor_deliverable_id"),
    "idx_decisions_queue": ("status", "needed_by", "decision_id"),
    "idx_updates_deliverable_date": ("deliverable_id", "update_date", "update_id"),
}


class VerificationError(RuntimeError):
    """Raised when source data and the ledger do not match the fixed course contract."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(64 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def regular_text(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        raise VerificationError(f"Source must be a regular file, not a link: {path.name}")
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise VerificationError(f"Source is not UTF-8: {path.name}") from error


def csv_rows(path: Path, headers: Sequence[str]) -> List[Dict[str, str]]:
    regular_text(path)
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != list(headers):
            raise VerificationError(f"Unexpected columns in {path.name}")
        rows = []
        for line_number, row in enumerate(reader, start=2):
            if None in row:
                raise VerificationError(f"Extra field in {path.name}:{line_number}")
            cleaned = {key: (value or "").strip() for key, value in row.items()}
            if not any(cleaned.values()):
                continue
            if any(value == "" for key, value in cleaned.items() if key != "blocked_reason"):
                raise VerificationError(f"Blank required value in {path.name}:{line_number}")
            rows.append(cleaned)
    if not rows:
        raise VerificationError(f"No records in {path.name}")
    return rows


def markdown_cells(line: str) -> List[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        raise VerificationError("Malformed Markdown table row")
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def markdown_rows(path: Path, headers: Sequence[str]) -> List[Dict[str, str]]:
    lines = regular_text(path).splitlines()
    expected = list(headers)
    for index, line in enumerate(lines[:-1]):
        if not line.strip().startswith("|"):
            continue
        found = markdown_cells(line)
        separator = markdown_cells(lines[index + 1]) if lines[index + 1].strip().startswith("|") else []
        if found != expected or len(separator) != len(found) or not all(
            re.fullmatch(r":?-{3,}:?", cell) for cell in separator
        ):
            continue
        rows = []
        for row_line in lines[index + 2:]:
            if not row_line.strip().startswith("|"):
                break
            cells = markdown_cells(row_line)
            if len(cells) != len(found) or any(cell == "" for cell in cells):
                raise VerificationError(f"Malformed record in {path.name}")
            rows.append(dict(zip(found, cells)))
        if rows:
            return rows
    raise VerificationError(f"Required table not found in {path.name}")


def expected_packet(project_root: Path) -> Dict[str, List[Dict[str, str]]]:
    source_root = project_root / "source_packet"
    if source_root.is_symlink() or not source_root.is_dir():
        raise VerificationError(f"Source packet must be a regular directory, not a link: {source_root}")
    for filename in SOURCE_FILES:
        regular_text(source_root / filename)
    sources = csv_rows(source_root / SOURCE_FILES[5], EXPECTED_COLUMNS["sources"][:-1])
    if tuple(row["path"] for row in sources) != SOURCE_FILES:
        raise VerificationError("Source register must declare the exact six files in course order")
    for source in sources:
        posix = PurePosixPath(source["path"])
        windows = PureWindowsPath(source["path"])
        if posix.is_absolute() or windows.is_absolute() or windows.drive or len(posix.parts) != 1:
            raise VerificationError(f"Unsafe source path: {source['path']}")
        source["sha256"] = sha256_file(source_root / source["path"])

    charter = {
        row["field"]: row["value"]
        for row in markdown_rows(source_root / SOURCE_FILES[0], ("field", "value"))
    }
    project = [{column: charter[column] for column in EXPECTED_COLUMNS["projects"]}]
    packet = {
        "sources": sources,
        "projects": project,
        "deliverables": csv_rows(source_root / SOURCE_FILES[1], EXPECTED_COLUMNS["deliverables"]),
        "dependencies": markdown_rows(source_root / SOURCE_FILES[2], EXPECTED_COLUMNS["dependencies"]),
        "decisions": markdown_rows(source_root / SOURCE_FILES[3], EXPECTED_COLUMNS["decisions"]),
        "updates": markdown_rows(source_root / SOURCE_FILES[4], EXPECTED_COLUMNS["updates"]),
    }
    for table, rows in packet.items():
        key = EXPECTED_COLUMNS[table][0]
        if len(rows) != EXPECTED_COUNTS[table] or len({row[key] for row in rows}) != len(rows):
            raise VerificationError(f"Unexpected or duplicate records in {table}")
    return packet


def open_read_only(path: Path) -> sqlite3.Connection:
    if path.is_symlink() or not path.is_file():
        raise VerificationError(f"Missing regular ledger: {path}")
    connection = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only = ON")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def verify_schema(connection: sqlite3.Connection) -> None:
    table_rows = connection.execute(
        "SELECT name, sql FROM sqlite_schema WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
    ).fetchall()
    table_sql = {row["name"]: row["sql"] for row in table_rows}
    if set(table_sql) != set(EXPECTED_COLUMNS):
        raise VerificationError(f"Unexpected application tables: {sorted(table_sql)!r}")
    for table, expected_names in EXPECTED_COLUMNS.items():
        columns = connection.execute(f"PRAGMA table_info({table})").fetchall()
        if tuple(row["name"] for row in columns) != expected_names:
            raise VerificationError(f"{table} column contract changed")
        for index, row in enumerate(columns):
            if (
                row["type"] != "TEXT" or row["notnull"] != 1 or row["dflt_value"] is not None
                or row["pk"] != (1 if index == 0 else 0)
            ):
                raise VerificationError(f"{table}.{row['name']} type/null/key contract changed")
        if not (table_sql[table] or "").rstrip().endswith("STRICT"):
            raise VerificationError(f"{table} must remain a STRICT table")
        foreign_keys = {
            (row["from"], row["table"], row["to"])
            for row in connection.execute(f"PRAGMA foreign_key_list({table})")
        }
        if foreign_keys != EXPECTED_FOREIGN_KEYS[table]:
            raise VerificationError(f"{table} foreign-key contract changed")
    for index_name, expected_columns in EXPECTED_INDEXES.items():
        if connection.execute(
            "SELECT 1 FROM sqlite_schema WHERE type = 'index' AND name = ?", (index_name,)
        ).fetchone() is None:
            raise VerificationError(f"Required index is missing: {index_name}")
        columns = tuple(row["name"] for row in connection.execute(f"PRAGMA index_info({index_name})"))
        if columns != expected_columns:
            raise VerificationError(f"{index_name} column order changed")
    if connection.execute("PRAGMA user_version").fetchone()[0] != 1:
        raise VerificationError("SQLite user_version must be 1")


def is_safe_relative(path_text: str) -> bool:
    posix = PurePosixPath(path_text)
    windows = PureWindowsPath(path_text)
    return not (
        posix.is_absolute() or windows.is_absolute() or bool(windows.drive)
        or ".." in posix.parts or ".." in windows.parts
    )


def verify_ledger(project_root: Path) -> Dict[str, Any]:
    requested = project_root.expanduser().absolute()
    if requested.is_symlink() or not requested.is_dir():
        raise VerificationError(f"Project root must be a regular directory, not a link: {requested}")
    root = requested.resolve()
    packet = expected_packet(root)
    with open_read_only(root / DATABASE_NAME) as connection:
        verify_schema(connection)
        counts = {
            table: connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for table in EXPECTED_COUNTS
        }
        if counts != EXPECTED_COUNTS:
            raise VerificationError(f"Unexpected row counts: {counts!r}")
        if connection.execute("PRAGMA foreign_key_check").fetchall():
            raise VerificationError("Foreign-key check failed")
        if connection.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise VerificationError("Integrity check failed")
        for table, expected_rows in packet.items():
            columns = EXPECTED_COLUMNS[table]
            actual = [
                dict(row) for row in connection.execute(f"SELECT * FROM {table} ORDER BY {columns[0]}")
            ]
            expected = [
                {column: row[column] for column in columns}
                for row in sorted(expected_rows, key=lambda row: row[columns[0]])
            ]
            if actual != expected:
                raise VerificationError(f"{table} values differ from the current source packet")

        deliverables = [dict(row) for row in connection.execute("SELECT * FROM deliverables ORDER BY deliverable_id")]
        source_paths = {row["path"] for row in packet["sources"]}
        for deliverable in deliverables:
            if not is_safe_relative(deliverable["output_path"]):
                raise VerificationError(f"Unsafe deliverable output: {deliverable['output_path']}")
            inputs = {part.strip() for part in deliverable["source_inputs"].split(";") if part.strip()}
            if not inputs or not inputs.issubset(source_paths):
                raise VerificationError(f"Undeclared source input on {deliverable['deliverable_id']}")
        for dependency in connection.execute(
            """SELECT dep.dependency_id, dep.status AS dependency_status,
                      predecessor.status AS predecessor_status
               FROM dependencies AS dep JOIN deliverables AS predecessor
                 ON predecessor.deliverable_id = dep.predecessor_deliverable_id
               ORDER BY dep.dependency_id"""
        ):
            expected_status = "satisfied" if dependency["predecessor_status"] == "complete" else "open"
            if dependency["dependency_status"] != expected_status:
                raise VerificationError(f"{dependency['dependency_id']} status contradicts predecessor status")
        unknown = connection.execute(
            "SELECT decision_owner FROM decisions WHERE decision_id = ?", ("DEC-002",)
        ).fetchone()
        if unknown is None or unknown[0] != "Not assigned in source":
            raise VerificationError("DEC-002 must preserve its explicit unassigned decision owner")

    sources = packet["sources"]
    material = "\n".join(f"{row['source_id']}:{row['sha256']}" for row in sources)
    return {"counts": counts, "source_fingerprint": hashlib.sha256(material.encode("utf-8")).hexdigest()}
