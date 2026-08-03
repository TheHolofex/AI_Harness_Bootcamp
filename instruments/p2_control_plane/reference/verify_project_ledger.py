#!/usr/bin/env python3
"""Verify the P2 project ledger against its current source packet."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import sqlite3
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Dict, List


DATABASE_NAME = "project_ledger.sqlite3"
TABLE_COUNTS = {
    "projects": 1,
    "deliverables": 4,
    "dependencies": 4,
    "decisions": 3,
    "updates": 5,
    "sources": 6,
}
EXPECTED_COLUMNS = {
    "sources": ("source_id", "path", "title", "source_type", "updated_at", "authority", "sha256"),
    "projects": ("project_id", "name", "outcome", "success_measure", "target_date", "sponsor", "project_lead", "current_phase", "source_id"),
    "deliverables": ("deliverable_id", "project_id", "title", "owner", "reviewer", "status", "priority", "source_inputs", "output_path", "acceptance_condition", "due_date", "dependency_summary", "blocked_reason", "next_commitment", "source_id"),
    "dependencies": ("dependency_id", "project_id", "predecessor_deliverable_id", "successor_deliverable_id", "dependency_type", "condition", "status", "owner", "source_id"),
    "decisions": ("decision_id", "project_id", "title", "question", "decision_owner", "needed_by", "status", "options", "recommendation", "consequence_of_delay", "source_id"),
    "updates": ("update_id", "project_id", "update_date", "author", "deliverable_id", "summary", "status_signal", "next_action", "source_id"),
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
    """Raised when the ledger does not match the build contract."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(64 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def open_read_only(path: Path) -> sqlite3.Connection:
    if path.is_symlink() or not path.is_file():
        raise VerificationError(f"Missing regular ledger: {path}")
    connection = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only = ON")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def is_safe_relative(path_text: str) -> bool:
    posix = PurePosixPath(path_text)
    windows = PureWindowsPath(path_text)
    return not (
        posix.is_absolute()
        or windows.is_absolute()
        or bool(windows.drive)
        or ".." in posix.parts
        or ".." in windows.parts
    )


def verify_schema(connection: sqlite3.Connection) -> None:
    table_rows = connection.execute(
        "SELECT name, sql FROM sqlite_schema WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
    ).fetchall()
    table_sql = {row["name"]: row["sql"] for row in table_rows}
    if set(table_sql) != set(EXPECTED_COLUMNS):
        raise VerificationError(f"Unexpected application tables: {sorted(table_sql)!r}")
    for table, expected_names in EXPECTED_COLUMNS.items():
        columns = connection.execute(f"PRAGMA table_info({table})").fetchall()
        names = tuple(row["name"] for row in columns)
        if names != expected_names:
            raise VerificationError(f"{table} column contract changed: {names!r}")
        for index, row in enumerate(columns):
            if row["type"] != "TEXT" or row["notnull"] != 1 or row["dflt_value"] is not None:
                raise VerificationError(f"{table}.{row['name']} type/null/default contract changed")
            expected_pk = 1 if index == 0 else 0
            if row["pk"] != expected_pk:
                raise VerificationError(f"{table}.{row['name']} primary-key contract changed")
        sql = table_sql[table] or ""
        if not sql.rstrip().endswith("STRICT"):
            raise VerificationError(f"{table} must remain a STRICT table")
        foreign_keys = {
            (row["from"], row["table"], row["to"])
            for row in connection.execute(f"PRAGMA foreign_key_list({table})")
        }
        if foreign_keys != EXPECTED_FOREIGN_KEYS[table]:
            raise VerificationError(f"{table} foreign-key contract changed: {sorted(foreign_keys)!r}")
    for index_name, expected_columns in EXPECTED_INDEXES.items():
        index_row = connection.execute(
            "SELECT name FROM sqlite_schema WHERE type = 'index' AND name = ?", (index_name,)
        ).fetchone()
        if index_row is None:
            raise VerificationError(f"Required index is missing: {index_name}")
        columns = tuple(
            row["name"] for row in connection.execute(f"PRAGMA index_info({index_name})")
        )
        if columns != expected_columns:
            raise VerificationError(f"{index_name} column order changed: {columns!r}")
    if connection.execute("PRAGMA user_version").fetchone()[0] != 1:
        raise VerificationError("SQLite user_version must be 1")


def verify_ledger(project_root: Path) -> Dict[str, Any]:
    requested_root = project_root.expanduser().absolute()
    if requested_root.is_symlink() or not requested_root.is_dir():
        raise VerificationError(f"Project root must be a regular directory, not a link: {requested_root}")
    root = requested_root.resolve()
    source_root = root / "source_packet"
    if source_root.is_symlink() or not source_root.is_dir():
        raise VerificationError(f"Source packet must be a regular directory, not a link: {source_root}")
    builder_path = root / "build_project_ledger.py"
    if builder_path.is_symlink() or not builder_path.is_file():
        raise VerificationError(f"Missing regular packet parser: {builder_path}")
    spec = importlib.util.spec_from_file_location("p2_build_project_ledger_for_verify", builder_path)
    if spec is None or spec.loader is None:
        raise VerificationError("Could not load the bounded packet parser")
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    expected_packet = builder.load_packet(root)
    with open_read_only(root / DATABASE_NAME) as connection:
        verify_schema(connection)

        actual_counts = {
            table: connection.execute(f"SELECT COUNT(*) AS count FROM {table}").fetchone()["count"]
            for table in TABLE_COUNTS
        }
        if actual_counts != TABLE_COUNTS:
            raise VerificationError(f"Unexpected row counts: {actual_counts!r}")
        if connection.execute("PRAGMA foreign_key_check").fetchall():
            raise VerificationError("Foreign-key check failed")
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            raise VerificationError(f"Integrity check failed: {integrity}")

        sources = [dict(row) for row in connection.execute("SELECT * FROM sources ORDER BY source_id")]
        for source in sources:
            source_path = source_root / source["path"]
            if source_path.is_symlink() or not source_path.is_file():
                raise VerificationError(f"Declared source is missing or linked: {source['path']}")
            if sha256_file(source_path) != source["sha256"]:
                raise VerificationError(f"Source hash changed after build: {source['path']}")

        for table, expected_rows in expected_packet.items():
            columns = EXPECTED_COLUMNS[table]
            actual_rows = [
                dict(row)
                for row in connection.execute(f"SELECT * FROM {table} ORDER BY {columns[0]}")
            ]
            normalized_expected = [
                {column: row[column] for column in columns}
                for row in sorted(expected_rows, key=lambda row: row[columns[0]])
            ]
            if actual_rows != normalized_expected:
                raise VerificationError(f"{table} values differ from the current source packet")

        deliverables = [dict(row) for row in connection.execute("SELECT * FROM deliverables ORDER BY deliverable_id")]
        source_paths = {source["path"] for source in sources}
        for deliverable in deliverables:
            required = (
                "owner", "reviewer", "source_inputs", "output_path", "acceptance_condition",
                "dependency_summary", "next_commitment",
            )
            if any(not str(deliverable[field]).strip() for field in required):
                raise VerificationError(f"Incomplete deliverable: {deliverable['deliverable_id']}")
            if not is_safe_relative(deliverable["output_path"]):
                raise VerificationError(f"Unsafe deliverable output: {deliverable['output_path']}")
            inputs = {part.strip() for part in deliverable["source_inputs"].split(";")}
            if not inputs or not inputs.issubset(source_paths):
                raise VerificationError(f"Undeclared source input on {deliverable['deliverable_id']}")

        open_decisions = connection.execute(
            "SELECT COUNT(*) FROM decisions WHERE status = ?", ("open",)
        ).fetchone()[0]
        blocked = connection.execute(
            "SELECT COUNT(*) FROM deliverables WHERE status = ? AND blocked_reason <> ''", ("blocked",)
        ).fetchone()[0]
        if open_decisions < 1 or blocked < 1:
            raise VerificationError("Ledger lacks a consequential open decision or blocked deliverable")
        unknown_owner = connection.execute(
            "SELECT decision_owner FROM decisions WHERE decision_id = ?", ("DEC-002",)
        ).fetchone()
        if unknown_owner is None or unknown_owner[0] != "Not assigned in source":
            raise VerificationError("DEC-002 must preserve its explicit unassigned decision owner")
        dependency_rows = connection.execute(
            """
            SELECT dep.dependency_id, dep.status AS dependency_status,
                   predecessor.status AS predecessor_status
            FROM dependencies AS dep
            JOIN deliverables AS predecessor
              ON predecessor.deliverable_id = dep.predecessor_deliverable_id
            ORDER BY dep.dependency_id
            """
        ).fetchall()
        for dependency in dependency_rows:
            expected = "satisfied" if dependency["predecessor_status"] == "complete" else "open"
            if dependency["dependency_status"] != expected:
                raise VerificationError(
                    f"{dependency['dependency_id']} status contradicts predecessor status"
                )

    fingerprint_input = "\n".join(f"{row['source_id']}:{row['sha256']}" for row in sources)
    fingerprint = hashlib.sha256(fingerprint_input.encode("utf-8")).hexdigest()
    return {"counts": actual_counts, "source_fingerprint": fingerprint}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()
    try:
        result = verify_ledger(Path(args.project_root))
    except (VerificationError, OSError, sqlite3.Error) as error:
        print(f"HOLD project ledger: {error}")
        return 1
    counts = result["counts"]
    print(
        "PASS project ledger: "
        f"{counts['projects']} project, {counts['deliverables']} deliverables, "
        f"{counts['dependencies']} dependencies, {counts['decisions']} decisions, "
        f"{counts['updates']} updates, {counts['sources']} sources; "
        f"fingerprint {result['source_fingerprint'][:12]}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
