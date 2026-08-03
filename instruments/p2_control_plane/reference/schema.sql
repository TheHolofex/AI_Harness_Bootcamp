PRAGMA foreign_keys = ON;

CREATE TABLE sources (
    source_id TEXT PRIMARY KEY CHECK (source_id GLOB 'SRC-[0-9][0-9][0-9]'),
    path TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    source_type TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    authority TEXT NOT NULL,
    sha256 TEXT NOT NULL CHECK (length(sha256) = 64)
) STRICT;

CREATE TABLE projects (
    project_id TEXT PRIMARY KEY CHECK (project_id GLOB 'PRJ-[0-9][0-9][0-9]'),
    name TEXT NOT NULL,
    outcome TEXT NOT NULL,
    success_measure TEXT NOT NULL,
    target_date TEXT NOT NULL,
    sponsor TEXT NOT NULL,
    project_lead TEXT NOT NULL,
    current_phase TEXT NOT NULL,
    source_id TEXT NOT NULL REFERENCES sources(source_id)
) STRICT;

CREATE TABLE deliverables (
    deliverable_id TEXT PRIMARY KEY CHECK (deliverable_id GLOB 'DLV-[0-9][0-9][0-9]'),
    project_id TEXT NOT NULL REFERENCES projects(project_id),
    title TEXT NOT NULL,
    owner TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('planned', 'ready', 'in_progress', 'blocked', 'complete')),
    priority TEXT NOT NULL CHECK (priority IN ('P0', 'P1', 'P2')),
    source_inputs TEXT NOT NULL,
    output_path TEXT NOT NULL UNIQUE,
    acceptance_condition TEXT NOT NULL,
    due_date TEXT NOT NULL,
    dependency_summary TEXT NOT NULL,
    blocked_reason TEXT NOT NULL,
    next_commitment TEXT NOT NULL,
    source_id TEXT NOT NULL REFERENCES sources(source_id)
) STRICT;

CREATE TABLE dependencies (
    dependency_id TEXT PRIMARY KEY CHECK (dependency_id GLOB 'DEP-[0-9][0-9][0-9]'),
    project_id TEXT NOT NULL REFERENCES projects(project_id),
    predecessor_deliverable_id TEXT NOT NULL REFERENCES deliverables(deliverable_id),
    successor_deliverable_id TEXT NOT NULL REFERENCES deliverables(deliverable_id),
    dependency_type TEXT NOT NULL CHECK (dependency_type IN ('finish_to_start', 'evidence_gate')),
    condition TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('open', 'satisfied')),
    owner TEXT NOT NULL,
    source_id TEXT NOT NULL REFERENCES sources(source_id),
    CHECK (predecessor_deliverable_id <> successor_deliverable_id),
    UNIQUE (predecessor_deliverable_id, successor_deliverable_id)
) STRICT;

CREATE TABLE decisions (
    decision_id TEXT PRIMARY KEY CHECK (decision_id GLOB 'DEC-[0-9][0-9][0-9]'),
    project_id TEXT NOT NULL REFERENCES projects(project_id),
    title TEXT NOT NULL,
    question TEXT NOT NULL,
    decision_owner TEXT NOT NULL,
    needed_by TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('open', 'resolved', 'deferred')),
    options TEXT NOT NULL,
    recommendation TEXT NOT NULL,
    consequence_of_delay TEXT NOT NULL,
    source_id TEXT NOT NULL REFERENCES sources(source_id)
) STRICT;

CREATE TABLE updates (
    update_id TEXT PRIMARY KEY CHECK (update_id GLOB 'UPD-[0-9][0-9][0-9]'),
    project_id TEXT NOT NULL REFERENCES projects(project_id),
    update_date TEXT NOT NULL,
    author TEXT NOT NULL,
    deliverable_id TEXT NOT NULL REFERENCES deliverables(deliverable_id),
    summary TEXT NOT NULL,
    status_signal TEXT NOT NULL CHECK (status_signal IN ('green', 'amber', 'red', 'complete')),
    next_action TEXT NOT NULL,
    source_id TEXT NOT NULL REFERENCES sources(source_id)
) STRICT;

CREATE INDEX idx_deliverables_project_status
    ON deliverables(project_id, status, due_date, deliverable_id);
CREATE INDEX idx_dependencies_successor
    ON dependencies(successor_deliverable_id, predecessor_deliverable_id);
CREATE INDEX idx_decisions_queue
    ON decisions(status, needed_by, decision_id);
CREATE INDEX idx_updates_deliverable_date
    ON updates(deliverable_id, update_date, update_id);

PRAGMA user_version = 1;
