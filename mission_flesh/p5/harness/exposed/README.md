# Exposed-session harness

`scripts/build_runtime_config.py` writes a schema-valid `opencode.json` with:
- every inherited MCP server discovered by the launcher set to `enabled: false`
- granular read rules for intake, reference pack, inventory, and schema only
- granular edit rules: deny `*`, allow only `out/triage_candidate.json`
- bash, task, skill, web, external-directory, and doom-loop permissions denied

`Start-P5Exposed.ps1` runs pinned OpenCode 1.18.11, resolves merged config twice,
strips Obsidian API key variables, refuses auto-approval, proves the final edit
allowlist and MCP-disabled state, and writes the sanitized live inventory. Use
`-PrepareOnly` before the staging freeze; run it again without that switch to
start the exposed session.
