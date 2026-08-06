# P4 Second Brain — vault contract

## Paths
- Trusted vault (student): `%USERPROFILE%\Vaults\p4-vault`
- Course seed: `mission_flesh/p4/vault_seed/`
- Raw warehouse: `mission_flesh/p4/raw_corpus/`
- Assessed slice list: `mission_flesh/p4/raw_corpus/ASSESSED_SLICE.json`
- External baseline: `operator/evidence/P4_BASELINE_[YYYY-MM-DD].json`

## Tools
- `tools/verify_brain.py` — semantic completion of the second brain and source lineage against `raw_corpus/MANIFEST.json`
- `tools/verify_baseline.py` — path/hash freeze and check (P5 integrity)
- `tools/verify_vault.py` — thin shim: default = brain verify; `--check-manifest` / `--write-manifest` = baseline (P5-compatible)

## Required root artifacts (complete vault)
- `AGENTS.md`
- `MOC.md`
- `Mission_Brief.md` — operator-facing brief drawn from the brain (P5 names this file)
- `Audit.md` — human audit sample with at least one disposition
- `Retrieval/Answers.md` — cold-session answers with wikilinks into notes
- `Evidence/PERMISSIONS.json` — director, worker, and retriever permission snapshot
- `Evidence/MCP_RECEIPTS.jsonl` — one JSON object per substantive MCP mutation. Do not log the receipt-log append itself.
- `Harness/HARNESS_CARD.md`
- `Harness/RUN_STATE.md`
- `Harness/HANDOFF_RECEIPT.md`
- `Notes/Modes.md`, `Notes/Nodes.md`, `Notes/Constraints.md`, `Notes/Threats.md`, `Notes/Sources.md`
- `Notes/Route/Spine.md`
- `tools/verify_brain.py`, `tools/verify_baseline.py`, `tools/verify_vault.py`
- At least eight content notes under `Notes/` (excluding the five hubs and Spine) that carry full source front matter

## Note front matter (YAML)
Required keys on every content note:
- `note_id` (string, unique)
- `title`
- `route_legs` (list from: `la_origin`, `rail`, `road`, `port`, `sealift`, `taiwan`, `cross_cutting`)
- `modes` (list from: `rail`, `road`, `port`, `sealift`, `air`, `multimodal`)
- `factors` (list from: `physical`, `legal`, `operational`, `economic`, `political`, `protection`)
- `threat_class` (`none` | `protection` | `interdiction_history` | `chokepoint_context`)
- `confidence` (`high` | `medium` | `low`)
- `sources` (non-empty list of source objects)

Each source object requires:
- `source_id`, `raw_path`, `sha256`, `original_url`, `publisher`, `document_date`, `retrieval_date`, `locator`, `excerpt`, `claim`, `confidence`, `uncertainty`, `contradictions`

All source fields except `contradictions` must contain a non-empty string. `confidence` uses `high`, `medium`, or `low`. The verifier checks `source_id`, `raw_path`, `sha256`, `original_url`, `publisher`, `document_date`, and `retrieval_date` against the course corpus manifest. It also checks the source file bytes.

Body must include at least one `[[wikilink]]` to a hub, spine, or another note.

## Coverage minima (verify_brain)
- Modes represented across notes: `rail`, `road`, `port`, `sealift` (air optional)
- Factors: `physical`, `legal`, `operational`, `protection`
- Route legs: `la_origin` or `rail`, plus `port` or `sealift`, plus `taiwan` or `cross_cutting`
- At least one note with `threat_class` other than `none`, body ending in defensive implications (protect / detect / recover language)
- `Mission_Brief.md` cites at least three vault notes via wikilinks
- `Retrieval/Answers.md` contains answers for Q1–Q4 with wikilinks
- Every wikilink in `Mission_Brief.md` and `Retrieval/Answers.md` resolves to a vault file.
- `MOC.md` links the five hubs and `Notes/Route/Spine.md`. Those links must resolve.
- `Evidence/MCP_RECEIPTS.jsonl` has at least one successful director `write`, `append`, or `patch` event from an Obsidian tool. Each line has `ts`, `agent`, `tool`, `action`, `path`, and Boolean `ok` fields.
- `Evidence/PERMISSIONS.json` records director MCP read=allow and write=ask. It records delete, move, copy, active-file, command, web, and vault filesystem access as deny.
- `Evidence/PERMISSIONS.json` records researcher MCP, web, and filesystem write as deny.
- `Evidence/PERMISSIONS.json` records the cold retriever project as `Documents\p4-cold-query`. It records MCP read=allow and write=ask. It records filesystem and web as deny.
- `Harness/RUN_STATE.md` records Phase `COMPLETE` and Status `SUCCESS`.
- `Harness/HANDOFF_RECEIPT.md` records terminal reason `SUCCESS`, accepted artifacts, and residual risk.

The receipt check validates the recorded event structure. The Windows spike must still confirm that exported OpenCode events use these fields and tool names.

## Assessed-slice partitions
- The four partition names are `worker_conus_rail_road`, `worker_port_sealift_taiwan`, `worker_constraints`, and `worker_protection`.
- Each assessed source ID appears in exactly one partition.
- The union of the four partitions equals `source_ids` in `ASSESSED_SLICE.json`.
- The corpus retrieval date is the fixed course snapshot date. Rebuilding the warehouse must not use the current date.

## Baseline manifest schema (v1, P5-compatible)
```json
{
  "schema_version": 1,
  "vault_root": ".",
  "root_fingerprint": "<sha256 over sorted path:sha256 lines>",
  "terminal_reason": "SUCCESS",
  "verification": { "tool": "verify_baseline", "file_count": 0 },
  "files": [ { "path": "MOC.md", "bytes": 0, "sha256": "..." } ]
}
```

## Safety
Threat notes: protection requirements only. No target ranking, access methods, stepwise sabotage, or attack optimization.
