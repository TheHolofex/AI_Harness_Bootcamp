#!/usr/bin/env python3
"""Read-only query layer behind the P2 Project Organizer MCP tools."""

from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Set


LIB_DIRECTORY = Path(__file__).resolve().parents[1] / "lib"
if str(LIB_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(LIB_DIRECTORY))

import ledger_verifier  # noqa: E402


DATABASE_NAME = "project_ledger.sqlite3"
TOOL_NAMES = (
    "get_project_snapshot",
    "get_ready_work",
    "get_dependency_path",
    "get_decision_queue",
)


class QueryError(RuntimeError):
    """Raised when the bounded read-only query surface cannot answer safely."""


def open_read_only(project_root: Path) -> sqlite3.Connection:
    requested_root = project_root.expanduser().absolute()
    if requested_root.is_symlink() or not requested_root.is_dir():
        raise QueryError(f"Project root is not a regular directory, not a link: {requested_root}")
    root = requested_root.resolve()
    database = root / DATABASE_NAME
    if database.is_symlink() or not database.is_file():
        raise QueryError(f"Missing regular {DATABASE_NAME} in project root")
    connection = sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only = ON")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def row_dict(row: sqlite3.Row) -> Dict[str, Any]:
    return {key: row[key] for key in row.keys()}


def load_latest_updates(connection: sqlite3.Connection) -> Dict[str, Dict[str, Any]]:
    rows = connection.execute(
        """
        SELECT u.*
        FROM updates AS u
        WHERE NOT EXISTS (
            SELECT 1 FROM updates AS newer
            WHERE newer.deliverable_id = u.deliverable_id
              AND (newer.update_date > u.update_date
                   OR (newer.update_date = u.update_date AND newer.update_id > u.update_id))
        )
        ORDER BY u.deliverable_id
        """
    )
    return {row["deliverable_id"]: row_dict(row) for row in rows}


def load_deliverables(connection: sqlite3.Connection) -> List[Dict[str, Any]]:
    latest = load_latest_updates(connection)
    deliverables = []
    for row in connection.execute("SELECT * FROM deliverables ORDER BY due_date, deliverable_id"):
        item = row_dict(row)
        item["source_inputs"] = [part.strip() for part in item["source_inputs"].split(";") if part.strip()]
        item["latest_update"] = latest.get(item["deliverable_id"])
        deliverables.append(item)
    return deliverables


def load_decisions(connection: sqlite3.Connection, *, limit: int = 20) -> List[Dict[str, Any]]:
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 20:
        raise QueryError("limit must be an integer from 1 through 20")
    rows = connection.execute(
        """
        SELECT * FROM decisions
        WHERE status = ?
        ORDER BY needed_by, decision_id
        LIMIT ?
        """,
        ("open", limit),
    )
    decisions = []
    for row in rows:
        item = row_dict(row)
        item["options"] = [part.strip() for part in item["options"].split(";") if part.strip()]
        decisions.append(item)
    return decisions


def load_ready_work(
    connection: sqlite3.Connection,
    *,
    include_evidence: bool = True,
) -> List[Dict[str, Any]]:
    ready_ids = {
        row["deliverable_id"]
        for row in connection.execute(
            """
            SELECT d.deliverable_id
            FROM deliverables AS d
            WHERE d.status NOT IN (?, ?)
              AND NOT EXISTS (
                  SELECT 1
                  FROM dependencies AS dep
                  JOIN deliverables AS predecessor
                    ON predecessor.deliverable_id = dep.predecessor_deliverable_id
                  WHERE dep.successor_deliverable_id = d.deliverable_id
                    AND predecessor.status <> ?
              )
            ORDER BY d.due_date, d.deliverable_id
            """,
            ("complete", "blocked", "complete"),
        )
    }
    evidence_by_successor: Dict[str, List[Dict[str, Any]]] = {item: [] for item in ready_ids}
    if include_evidence:
        for row in connection.execute(
            """
            SELECT dep.successor_deliverable_id, dep.dependency_id,
                   dep.predecessor_deliverable_id, predecessor.status AS predecessor_status,
                   dep.source_id AS dependency_source_id,
                   predecessor.source_id AS predecessor_source_id
            FROM dependencies AS dep
            JOIN deliverables AS predecessor
              ON predecessor.deliverable_id = dep.predecessor_deliverable_id
            WHERE dep.successor_deliverable_id IN (
                SELECT d.deliverable_id FROM deliverables AS d
                WHERE d.status NOT IN (?, ?)
            )
            ORDER BY dep.successor_deliverable_id, dep.dependency_id
            """,
            ("complete", "blocked"),
        ):
            successor = row["successor_deliverable_id"]
            if successor in evidence_by_successor:
                evidence_by_successor[successor].append({
                    "dependency_id": row["dependency_id"],
                    "predecessor_deliverable_id": row["predecessor_deliverable_id"],
                    "predecessor_status": row["predecessor_status"],
                    "dependency_source_id": row["dependency_source_id"],
                    "predecessor_source_id": row["predecessor_source_id"],
                })
    ready = []
    for item in load_deliverables(connection):
        if item["deliverable_id"] not in ready_ids:
            continue
        if include_evidence:
            item["readiness_evidence"] = evidence_by_successor[item["deliverable_id"]]
        ready.append(item)
    return ready


def load_edges(connection: sqlite3.Connection) -> List[Dict[str, Any]]:
    return [
        row_dict(row)
        for row in connection.execute("SELECT * FROM dependencies ORDER BY dependency_id")
    ]


def longest_dependency_path(
    deliverable_ids: Sequence[str],
    edges: Sequence[Mapping[str, Any]],
    target: Optional[str] = None,
) -> List[str]:
    predecessors: Dict[str, List[str]] = {item: [] for item in deliverable_ids}
    successors: Dict[str, List[str]] = {item: [] for item in deliverable_ids}
    for edge in edges:
        predecessor = str(edge["predecessor_deliverable_id"])
        successor = str(edge["successor_deliverable_id"])
        predecessors[successor].append(predecessor)
        successors[predecessor].append(successor)
    for values in predecessors.values():
        values.sort()
    for values in successors.values():
        values.sort()

    memo: Dict[str, List[str]] = {}
    visiting: Set[str] = set()

    def path_to(node: str) -> List[str]:
        if node in memo:
            return memo[node]
        if node in visiting:
            raise QueryError("Dependency graph contains a cycle")
        visiting.add(node)
        candidates = [path_to(parent) + [node] for parent in predecessors[node]]
        visiting.remove(node)
        best = max(candidates, key=lambda path: (len(path), path)) if candidates else [node]
        memo[node] = best
        return best

    if target is not None:
        if target not in predecessors:
            raise QueryError(f"Unknown deliverable_id: {target}")
        return path_to(target)
    terminals = sorted(node for node in deliverable_ids if not successors[node])
    candidates = [path_to(node) for node in terminals or deliverable_ids]
    return max(candidates, key=lambda path: (len(path), path))


def connected_ids(start: str, adjacency: Mapping[str, Sequence[str]]) -> List[str]:
    seen: Set[str] = set()
    stack = list(reversed(sorted(adjacency.get(start, []))))
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stack.extend(reversed(sorted(adjacency.get(node, []))))
    return sorted(seen)


def get_dependency_path(connection: sqlite3.Connection, deliverable_id: str) -> Dict[str, Any]:
    if not isinstance(deliverable_id, str) or not deliverable_id.startswith("DLV-"):
        raise QueryError("deliverable_id must be a DLV-### string")
    deliverables = load_deliverables(connection)
    by_id = {item["deliverable_id"]: item for item in deliverables}
    if deliverable_id not in by_id:
        raise QueryError(f"Unknown deliverable_id: {deliverable_id}")
    edges = load_edges(connection)
    upstream_map: Dict[str, List[str]] = {key: [] for key in by_id}
    downstream_map: Dict[str, List[str]] = {key: [] for key in by_id}
    for edge in edges:
        predecessor = edge["predecessor_deliverable_id"]
        successor = edge["successor_deliverable_id"]
        upstream_map[successor].append(predecessor)
        downstream_map[predecessor].append(successor)
    path_ids = longest_dependency_path(list(by_id), edges, deliverable_id)
    path_pairs = set(zip(path_ids, path_ids[1:]))
    path_edges = [
        edge
        for edge in edges
        if (edge["predecessor_deliverable_id"], edge["successor_deliverable_id"]) in path_pairs
    ]
    return {
        "target_deliverable_id": deliverable_id,
        "launch_path": [by_id[item] for item in path_ids],
        "dependencies": path_edges,
        "upstream_ids": connected_ids(deliverable_id, upstream_map),
        "downstream_ids": connected_ids(deliverable_id, downstream_map),
    }


def source_fingerprint(sources: Iterable[Mapping[str, Any]]) -> str:
    material = "\n".join(f"{row['source_id']}:{row['sha256']}" for row in sources)
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def current_source_fingerprint(connection: sqlite3.Connection) -> str:
    sources = [
        row_dict(row)
        for row in connection.execute("SELECT source_id, sha256 FROM sources ORDER BY source_id")
    ]
    return source_fingerprint(sources)


def get_project_snapshot(connection: sqlite3.Connection) -> Dict[str, Any]:
    project_row = connection.execute("SELECT * FROM projects ORDER BY project_id LIMIT 1").fetchone()
    if project_row is None:
        raise QueryError("Ledger contains no project")
    project = row_dict(project_row)
    deliverables = load_deliverables(connection)
    ready = load_ready_work(connection, include_evidence=False)
    decisions = load_decisions(connection)
    sources = [row_dict(row) for row in connection.execute("SELECT * FROM sources ORDER BY source_id")]
    status_counts = {status: 0 for status in ("planned", "ready", "in_progress", "blocked", "complete")}
    for item in deliverables:
        status_counts[item["status"]] += 1
    now = next((item for item in deliverables if item["status"] == "in_progress"), None)
    if now is None and ready:
        now = ready[0]
    next_item = None
    if now is not None:
        next_item = {
            "deliverable_id": now["deliverable_id"],
            "commitment": now["next_commitment"],
            "owner": now["owner"],
            "due_date": now["due_date"],
            "source_id": now["source_id"],
        }
    as_of_row = connection.execute("SELECT MAX(update_date) AS as_of FROM updates").fetchone()
    unknowns = []
    for decision in decisions:
        if decision["decision_owner"] == "Not assigned in source":
            unknowns.append({
                "field": f"{decision['decision_id']}.decision_owner",
                "value": decision["decision_owner"],
                "impact": decision["consequence_of_delay"],
                "needed_by": decision["needed_by"],
                "source_id": decision["source_id"],
            })
    return {
        "project": project,
        "as_of": as_of_row["as_of"],
        "counts": {
            "deliverables": len(deliverables),
            **status_counts,
            "ready_now": len(ready),
            "open_decisions": len(decisions),
            "unknowns": len(unknowns),
        },
        "now": now,
        "next": next_item,
        "unknowns": unknowns,
        "deliverables": deliverables,
        "sources": sources,
        "source_fingerprint": source_fingerprint(sources),
    }


def dispatch(project_root: Path, tool_name: str, arguments: Mapping[str, Any]) -> Dict[str, Any]:
    if tool_name not in TOOL_NAMES:
        raise QueryError(f"Unknown tool: {tool_name}")
    try:
        ledger_verifier.verify_ledger(project_root)
    except Exception as error:
        raise QueryError(f"Ledger/source verification failed: {error}") from error
    with open_read_only(project_root) as connection:
        if tool_name == "get_project_snapshot":
            if arguments:
                raise QueryError("get_project_snapshot accepts no arguments")
            return get_project_snapshot(connection)
        if tool_name == "get_ready_work":
            if arguments:
                raise QueryError("get_ready_work accepts no arguments")
            ready = load_ready_work(connection)
            return {
                "ready_work": ready,
                "count": len(ready),
                "source_fingerprint": current_source_fingerprint(connection),
            }
        if tool_name == "get_dependency_path":
            if set(arguments) != {"deliverable_id"}:
                raise QueryError("get_dependency_path requires only deliverable_id")
            result = get_dependency_path(connection, arguments["deliverable_id"])
            result["source_fingerprint"] = current_source_fingerprint(connection)
            return result
        if not set(arguments).issubset({"limit"}):
            raise QueryError("get_decision_queue accepts only limit")
        decisions = load_decisions(connection, limit=arguments.get("limit", 10))
        return {
            "decisions": decisions,
            "count": len(decisions),
            "source_fingerprint": current_source_fingerprint(connection),
        }


def main(argv: Sequence[str]) -> int:
    if len(argv) not in (3, 4):
        print("usage: query_ledger.py PROJECT_ROOT TOOL_NAME [JSON_ARGUMENTS]", file=sys.stderr)
        return 2
    root = Path(argv[1])
    tool_name = argv[2]
    try:
        arguments = json.loads(argv[3]) if len(argv) == 4 else {}
        if not isinstance(arguments, dict):
            raise QueryError("JSON arguments must be an object")
        result = dispatch(root, tool_name, arguments)
    except (json.JSONDecodeError, OSError, QueryError, sqlite3.Error) as error:
        print(f"query failed: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
