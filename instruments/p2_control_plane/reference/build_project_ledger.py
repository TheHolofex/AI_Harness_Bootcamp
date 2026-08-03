#!/usr/bin/env python3
"""Build the P2 SQLite project ledger from the bounded source packet."""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import sqlite3
import tempfile
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Dict, Iterable, List, Mapping, Sequence


DATABASE_NAME = "project_ledger.sqlite3"
SOURCE_DIRECTORY = "source_packet"
SOURCE_FILES = (
    "01_project_charter.md",
    "02_deliverables.csv",
    "03_dependency_notes.md",
    "04_decision_log.md",
    "05_status_updates.md",
    "06_source_register.csv",
)
ID_PATTERNS = {
    "source_id": re.compile(r"^SRC-[0-9]{3}$"),
    "project_id": re.compile(r"^PRJ-[0-9]{3}$"),
    "deliverable_id": re.compile(r"^DLV-[0-9]{3}$"),
    "dependency_id": re.compile(r"^DEP-[0-9]{3}$"),
    "decision_id": re.compile(r"^DEC-[0-9]{3}$"),
    "update_id": re.compile(r"^UPD-[0-9]{3}$"),
}


class BuildError(RuntimeError):
    """Raised when source evidence cannot produce a valid ledger."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(64 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(path: Path) -> str:
    if path.is_symlink() or not path.is_file():
        raise BuildError(f"Source must be a regular file, not a link: {path.name}")
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise BuildError(f"Source is not valid UTF-8: {path.name}") from error


def read_csv_rows(path: Path, expected_headers: Sequence[str]) -> List[Dict[str, str]]:
    read_text(path)
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != list(expected_headers):
            raise BuildError(
                f"Unexpected columns in {path.name}: {reader.fieldnames!r}; "
                f"expected {list(expected_headers)!r}"
            )
        rows = []
        for line_number, row in enumerate(reader, start=2):
            if None in row:
                raise BuildError(f"Extra field in {path.name}:{line_number}")
            cleaned = {key: (value or "").strip() for key, value in row.items()}
            if not any(cleaned.values()):
                continue
            if any(value == "" for key, value in cleaned.items() if key != "blocked_reason"):
                raise BuildError(f"Blank required value in {path.name}:{line_number}")
            rows.append(cleaned)
    if not rows:
        raise BuildError(f"No data rows in {path.name}")
    return rows


def split_markdown_row(line: str) -> List[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        raise BuildError(f"Malformed Markdown table row: {line!r}")
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def is_separator_row(cells: Sequence[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def read_markdown_table(path: Path, expected_headers: Sequence[str]) -> List[Dict[str, str]]:
    lines = read_text(path).splitlines()
    expected = list(expected_headers)
    for index, line in enumerate(lines[:-1]):
        if not line.strip().startswith("|"):
            continue
        headers = split_markdown_row(line)
        separator = split_markdown_row(lines[index + 1]) if lines[index + 1].strip().startswith("|") else []
        if headers != expected or not is_separator_row(separator) or len(separator) != len(headers):
            continue
        rows = []
        for row_line in lines[index + 2 :]:
            if not row_line.strip().startswith("|"):
                break
            cells = split_markdown_row(row_line)
            if len(cells) != len(headers):
                raise BuildError(f"Wrong table width in {path.name}: {row_line!r}")
            if any(cell == "" for cell in cells):
                raise BuildError(f"Blank table cell in {path.name}: {row_line!r}")
            rows.append(dict(zip(headers, cells)))
        if not rows:
            raise BuildError(f"Markdown table has no rows in {path.name}")
        return rows
    raise BuildError(f"Required Markdown table not found in {path.name}")


def require_id(row: Mapping[str, str], field: str, source_name: str) -> None:
    pattern = ID_PATTERNS.get(field)
    if pattern is not None and not pattern.fullmatch(row[field]):
        raise BuildError(f"Invalid {field} in {source_name}: {row[field]!r}")


def require_unique(rows: Sequence[Mapping[str, str]], field: str, source_name: str) -> None:
    values = [row[field] for row in rows]
    if len(values) != len(set(values)):
        raise BuildError(f"Duplicate {field} in {source_name}")
    for row in rows:
        require_id(row, field, source_name)


def require_enum(
    rows: Sequence[Mapping[str, str]],
    field: str,
    allowed: Sequence[str],
    source_name: str,
    record_field: str,
) -> None:
    allowed_set = set(allowed)
    for row in rows:
        if row[field] not in allowed_set:
            choices = ", ".join(allowed)
            raise BuildError(
                f"Invalid {field} {row[field]!r} in {source_name} record "
                f"{row[record_field]}; expected one of: {choices}"
            )


def require_safe_relative(path_text: str, label: str, *, basename_only: bool = False) -> None:
    posix = PurePosixPath(path_text)
    windows = PureWindowsPath(path_text)
    if (
        posix.is_absolute()
        or windows.is_absolute()
        or bool(windows.drive)
        or ".." in posix.parts
        or ".." in windows.parts
        or (basename_only and len(posix.parts) != 1)
    ):
        raise BuildError(f"Unsafe {label}: {path_text!r}")


def load_packet(project_root: Path) -> Dict[str, List[Dict[str, str]]]:
    source_root = project_root / SOURCE_DIRECTORY
    if source_root.is_symlink() or not source_root.is_dir():
        raise BuildError(f"Missing regular source directory: {source_root}")
    for filename in SOURCE_FILES:
        read_text(source_root / filename)

    source_headers = ("source_id", "path", "title", "source_type", "updated_at", "authority")
    sources = read_csv_rows(source_root / "06_source_register.csv", source_headers)
    require_unique(sources, "source_id", "06_source_register.csv")
    declared_paths = [row["path"] for row in sources]
    if tuple(declared_paths) != SOURCE_FILES:
        raise BuildError("Source register must declare the exact six packet files in course order")
    for row in sources:
        require_safe_relative(row["path"], "source path", basename_only=True)
        row["sha256"] = sha256_file(source_root / row["path"])

    charter_rows = read_markdown_table(source_root / "01_project_charter.md", ("field", "value"))
    charter = {row["field"]: row["value"] for row in charter_rows}
    project_fields = (
        "project_id",
        "name",
        "outcome",
        "success_measure",
        "target_date",
        "sponsor",
        "project_lead",
        "current_phase",
        "source_id",
    )
    if tuple(charter) != project_fields:
        raise BuildError("Charter facts must contain the exact project fields in contract order")
    projects = [{field: charter[field] for field in project_fields}]
    require_unique(projects, "project_id", "01_project_charter.md")

    deliverable_headers = (
        "deliverable_id", "project_id", "title", "owner", "reviewer", "status", "priority",
        "source_inputs", "output_path", "acceptance_condition", "due_date", "dependency_summary",
        "blocked_reason", "next_commitment", "source_id",
    )
    deliverables = read_csv_rows(source_root / "02_deliverables.csv", deliverable_headers)
    require_unique(deliverables, "deliverable_id", "02_deliverables.csv")
    require_enum(
        deliverables, "status", ("planned", "ready", "in_progress", "blocked", "complete"),
        "02_deliverables.csv", "deliverable_id",
    )
    require_enum(deliverables, "priority", ("P0", "P1", "P2"), "02_deliverables.csv", "deliverable_id")

    dependency_headers = (
        "dependency_id", "project_id", "predecessor_deliverable_id", "successor_deliverable_id",
        "dependency_type", "condition", "status", "owner", "source_id",
    )
    dependencies = read_markdown_table(source_root / "03_dependency_notes.md", dependency_headers)
    require_unique(dependencies, "dependency_id", "03_dependency_notes.md")
    require_enum(
        dependencies, "dependency_type", ("finish_to_start", "evidence_gate"),
        "03_dependency_notes.md", "dependency_id",
    )
    require_enum(dependencies, "status", ("open", "satisfied"), "03_dependency_notes.md", "dependency_id")

    decision_headers = (
        "decision_id", "project_id", "title", "question", "decision_owner", "needed_by", "status",
        "options", "recommendation", "consequence_of_delay", "source_id",
    )
    decisions = read_markdown_table(source_root / "04_decision_log.md", decision_headers)
    require_unique(decisions, "decision_id", "04_decision_log.md")
    require_enum(decisions, "status", ("open", "resolved", "deferred"), "04_decision_log.md", "decision_id")

    update_headers = (
        "update_id", "project_id", "update_date", "author", "deliverable_id", "summary",
        "status_signal", "next_action", "source_id",
    )
    updates = read_markdown_table(source_root / "05_status_updates.md", update_headers)
    require_unique(updates, "update_id", "05_status_updates.md")
    require_enum(
        updates, "status_signal", ("green", "amber", "red", "complete"),
        "05_status_updates.md", "update_id",
    )

    source_ids = {row["source_id"] for row in sources}
    source_paths = set(declared_paths)
    project_ids = {row["project_id"] for row in projects}
    deliverable_ids = {row["deliverable_id"] for row in deliverables}
    for table_name, rows in (
        ("projects", projects), ("deliverables", deliverables), ("dependencies", dependencies),
        ("decisions", decisions), ("updates", updates),
    ):
        for row in rows:
            if row["source_id"] not in source_ids:
                raise BuildError(f"{table_name} row cites unknown source: {row['source_id']}")
            if row["project_id"] not in project_ids:
                raise BuildError(f"{table_name} row cites unknown project: {row['project_id']}")
    for row in deliverables:
        require_safe_relative(row["output_path"], "deliverable output path")
        for source_input in (part.strip() for part in row["source_inputs"].split(";")):
            if source_input not in source_paths:
                raise BuildError(f"Deliverable cites undeclared input: {source_input!r}")
    for row in dependencies:
        for field in ("predecessor_deliverable_id", "successor_deliverable_id"):
            require_id(row, field, "03_dependency_notes.md")
            if row[field] not in deliverable_ids:
                raise BuildError(f"Dependency cites unknown deliverable: {row[field]}")
    for row in updates:
        require_id(row, "deliverable_id", "05_status_updates.md")
        if row["deliverable_id"] not in deliverable_ids:
            raise BuildError(f"Update cites unknown deliverable: {row['deliverable_id']}")

    return {
        "sources": sorted(sources, key=lambda row: row["source_id"]),
        "projects": sorted(projects, key=lambda row: row["project_id"]),
        "deliverables": sorted(deliverables, key=lambda row: row["deliverable_id"]),
        "dependencies": sorted(dependencies, key=lambda row: row["dependency_id"]),
        "decisions": sorted(decisions, key=lambda row: row["decision_id"]),
        "updates": sorted(updates, key=lambda row: row["update_id"]),
    }


def insert_rows(connection: sqlite3.Connection, table: str, columns: Sequence[str], rows: Iterable[Mapping[str, str]]) -> None:
    column_sql = ", ".join(columns)
    placeholders = ", ".join("?" for _ in columns)
    statement = f"INSERT INTO {table} ({column_sql}) VALUES ({placeholders})"
    connection.executemany(statement, ([row[column] for column in columns] for row in rows))


def build_ledger(project_root: Path, *, rebuild: bool = False) -> Path:
    requested_root = project_root.expanduser().absolute()
    if requested_root.is_symlink() or not requested_root.is_dir():
        raise BuildError(f"Project root must be a regular directory, not a link: {requested_root}")
    root = requested_root.resolve()
    schema_path = root / "schema.sql"
    if schema_path.is_symlink() or not schema_path.is_file():
        raise BuildError(f"Missing regular schema file: {schema_path}")
    schema = schema_path.read_text(encoding="utf-8")
    packet = load_packet(root)
    target = root / DATABASE_NAME
    if target.exists() and not rebuild:
        raise BuildError(f"Refusing to overwrite {target.name}; rerun with --rebuild")

    descriptor, temporary_name = tempfile.mkstemp(prefix=".project_ledger.", suffix=".tmp", dir=str(root))
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        connection = sqlite3.connect(str(temporary))
        try:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute("PRAGMA journal_mode = DELETE")
            connection.execute("PRAGMA synchronous = FULL")
            connection.executescript(schema)
            insert_rows(connection, "sources", (
                "source_id", "path", "title", "source_type", "updated_at", "authority", "sha256"
            ), packet["sources"])
            insert_rows(connection, "projects", (
                "project_id", "name", "outcome", "success_measure", "target_date", "sponsor",
                "project_lead", "current_phase", "source_id"
            ), packet["projects"])
            insert_rows(connection, "deliverables", (
                "deliverable_id", "project_id", "title", "owner", "reviewer", "status", "priority",
                "source_inputs", "output_path", "acceptance_condition", "due_date", "dependency_summary",
                "blocked_reason", "next_commitment", "source_id"
            ), packet["deliverables"])
            insert_rows(connection, "dependencies", (
                "dependency_id", "project_id", "predecessor_deliverable_id", "successor_deliverable_id",
                "dependency_type", "condition", "status", "owner", "source_id"
            ), packet["dependencies"])
            insert_rows(connection, "decisions", (
                "decision_id", "project_id", "title", "question", "decision_owner", "needed_by", "status",
                "options", "recommendation", "consequence_of_delay", "source_id"
            ), packet["decisions"])
            insert_rows(connection, "updates", (
                "update_id", "project_id", "update_date", "author", "deliverable_id", "summary",
                "status_signal", "next_action", "source_id"
            ), packet["updates"])
            foreign_key_errors = connection.execute("PRAGMA foreign_key_check").fetchall()
            if foreign_key_errors:
                raise BuildError(f"Foreign-key check failed: {foreign_key_errors!r}")
            integrity = connection.execute("PRAGMA integrity_check").fetchone()
            if integrity != ("ok",):
                raise BuildError(f"Integrity check failed: {integrity!r}")
            connection.commit()
        finally:
            connection.close()
        os.replace(str(temporary), str(target))
    except Exception:
        if temporary.exists():
            temporary.unlink()
        raise
    return target


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".", help="Project root containing schema.sql and source_packet")
    parser.add_argument("--rebuild", action="store_true", help="Atomically replace an existing validated ledger")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        target = build_ledger(Path(args.project_root), rebuild=args.rebuild)
    except (BuildError, OSError, sqlite3.Error) as error:
        print(f"HOLD project ledger: {error}")
        return 1
    print(f"Built {target.name} from 6 declared UTF-8 sources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
