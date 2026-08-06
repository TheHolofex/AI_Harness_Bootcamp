# P4 — Second brain

OpenCode-only module. Students process a pre-built raw corpus into an Obsidian vault through MCP.

## Layout
- `vault_seed/` — thin source tree used to create `%USERPROFILE%\Vaults\p4-vault`
- `raw_corpus/` — warehouse (`MANIFEST.json`, `ASSESSED_SLICE.json`, synthesized + fetched docs)
- `controller/` — research brief, partitions, schema pointer, and P4 OpenCode MCP config
- `docs/VAULT_CONTRACT.md` — required artifacts and note schema
- `reference_fixtures/complete_vault/` — known-good completed vault
- `tools` live inside `vault_seed/tools/`: `verify_brain.py`, `verify_baseline.py`, `verify_vault.py` (shim)
- `archive_meridian_seed/` — previous MERIDIAN director-loop materials
- `tests/test_verify_brain.py` — mutation tests

Run `scripts/Start-P4.ps1 Setup` to copy vault content without `.opencode` or `.obsidian` state. Run `scripts/Start-P4.ps1 Director` or `Retriever` to clear inherited OpenCode overrides, load `controller/opencode.p4.json` plus the shipped agents, verify the resolved boundary, and launch the correct project root.

The vault remains a normal writable Windows folder. OpenCode permissions are application controls; do not apply NTFS ACLs, read-only attributes, or ownership changes to the vault.

Run the verifier from the course seed. The course-seed path lets `verify_brain.py` check each cited source against `raw_corpus/MANIFEST.json` and the source bytes.

## Verify
```bash
python3 mission_flesh/p4/vault_seed/tools/verify_brain.py mission_flesh/p4/reference_fixtures/complete_vault
python3 -m unittest mission_flesh.p4.tests.test_verify_brain -v
```
