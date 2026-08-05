# P4 — Second brain

OpenCode-only module. Students process a pre-built raw corpus into an Obsidian vault through MCP.

## Layout
- `vault_seed/` — thin Obsidian seed copied to `Documents\p4-vault`
- `raw_corpus/` — warehouse (`MANIFEST.json`, `ASSESSED_SLICE.json`, synthesized + fetched docs)
- `controller/` — research brief, partitions, schema pointer, and P4 OpenCode MCP config
- `docs/VAULT_CONTRACT.md` — required artifacts and note schema
- `reference_fixtures/complete_vault/` — known-good completed vault
- `tools` live inside `vault_seed/tools/`: `verify_brain.py`, `verify_baseline.py`, `verify_vault.py` (shim)
- `archive_meridian_seed/` — previous MERIDIAN director-loop materials
- `tests/test_verify_brain.py` — mutation tests

Set `OPENCODE_CONFIG` to `controller/opencode.p4.json`. Set `OPENCODE_CONFIG_DIR` to `vault_seed/.opencode`. This loads the P4 agents without copying them into the shared course project.

Run the verifier from the course seed. The course-seed path lets `verify_brain.py` check each cited source against `raw_corpus/MANIFEST.json` and the source bytes.

## Verify
```bash
python3 mission_flesh/p4/vault_seed/tools/verify_brain.py mission_flesh/p4/reference_fixtures/complete_vault
python3 -m unittest mission_flesh.p4.tests.test_verify_brain -v
```
