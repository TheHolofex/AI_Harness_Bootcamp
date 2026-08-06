# BLOCKED — P4 Second brain pivot

Items that need hardware or live apps not available in this authoring environment. Everything else in the pivot was completed and tested on disk.

## Needs from you (Windows classroom box)

1. **Obsidian + Local REST API plugin pin**
   - Install Obsidian and enable Local REST API.
   - Enable the HTTP server and confirm `http://127.0.0.1:27123/mcp/` on the course Windows image.
   - If the course requires HTTPS, trust the plugin certificate and change the P4 config to `https://127.0.0.1:27124/mcp/`.
   - Record the exact plugin version next to the course OpenCode build in prework.
   - Smoke: OpenCode MCP inspect → read `MOC.md` → ask-gated write of `Evidence/_smoke.md`.

2. **OpenCode MCP registration + permission files on Windows**
   - Confirm that the pinned build uses OpenCode V1 syntax: `opencode`, `permission`, and the V1 `mcp` object.
   - If the pin uses OpenCode V2, convert the config to `opencode2`, `permissions`, and ordered V2 rules before class.
   - Run `opencode mcp list` and confirm server `obsidian` is connected.
   - Run `opencode agent list` and confirm `director`, `retriever`, and all four `worker_*` agents load from the project.
   - Confirm director read tools work, write/append/patch ask, and delete/move/copy/active-file/command tools deny. Confirm `external_directory` is denied.
   - Confirm each `worker_*` agent can read only its run contract and assigned manifest paths. Confirm that it has no MCP, web, shell, filesystem write, or external-directory access.
   - Confirm the retriever starts in `Documents\p4-cold-query` and cannot read the course repo or raw corpus. Confirm `external_directory` is denied.
   - Confirm env var injection of `OBSIDIAN_REST_API_KEY` and `HB_XAI_MODEL`.
   - Confirm `OPENCODE_CONFIG_DIR` loads the six P4 agents without copying them into the course project.
   - Export one OpenCode session. Confirm the real tool-event names and fields match `Evidence/MCP_RECEIPTS.jsonl`.

3. **Student-facing PowerShell blocks in `site/blocks/p4.html`**
   - Run Stage 01 seed copy, Stage 02 config and MCP smoke, Stage 06 cold project, and Stage 08 baseline freeze on a clean Windows profile.
   - Flag any path or `py -3` launcher differences for the image.

4. **Timed pilot (~165 min)**
   - Full learner run with four workers on the assessed slice; cut to three workers if retrieval/audit slip.

5. **Fetched public PDFs redistribution review**
   - `raw_corpus/fetched/` holds live pulls (`redistribution_rights: public_url_course_mirror_review`). Legal/redistribution pass before shipping a release archive to students. Synthesized docs are course-owned.

6. **Prework download packaging (optional release asset)**
   - If git size is painful, wrap `raw_corpus` as a versioned zip + SHA-256 and add the prework download step on the install clinic page (not done here).

## Already verified without that hardware

- `verify_brain` PASS on `reference_fixtures/complete_vault`
- `verify_brain` HOLD on unsourced note
- `verify_baseline` / `verify_vault --check-manifest` PASS then HOLD after mutation
- `python3 -m unittest mission_flesh.p4.tests.test_verify_brain`
- Registry check IDs match `p4.html`
- P5 is standalone: its active page and pack consume no P4 artifact or service, and its standalone contract test passes
