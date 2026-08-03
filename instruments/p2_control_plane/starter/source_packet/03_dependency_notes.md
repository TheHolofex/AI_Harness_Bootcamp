# Dependency notes

These are finish-to-start relationships between the four deliverables. A
successor is not ready while any predecessor remains incomplete.

| dependency_id | project_id | predecessor_deliverable_id | successor_deliverable_id | dependency_type | condition | status | owner | source_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DEP-001 | PRJ-001 | DLV-001 | DLV-002 | finish_to_start | Field names and rejected-record behavior are signed before the tabletop dataset is frozen. | satisfied | Maya Chen | SRC-003 |
| DEP-002 | PRJ-001 | DLV-002 | DLV-003 | finish_to_start | The response card must match the workflow that passes Priya's tabletop review. | open | Jonah Reed | SRC-003 |
| DEP-003 | PRJ-001 | DLV-002 | DLV-004 | evidence_gate | The go-live packet must include the 12-alert tabletop result and all misses. | open | Priya Shah | SRC-003 |
| DEP-004 | PRJ-001 | DLV-003 | DLV-004 | finish_to_start | Both site leads complete supervised practice before the go-live decision. | open | Elise Morgan | SRC-003 |

The longest launch path is DLV-001 to DLV-002 to DLV-003 to DLV-004. DLV-004
also depends directly on the DLV-002 tabletop evidence.
