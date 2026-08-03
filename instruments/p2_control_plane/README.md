# P2 Project Organizer

This kit backs the P2 live-classroom build. The website is the learner guide;
this file is the maintainer map.

`bootstrap.ps1` copies only `starter/` to
`Documents\HarnessBootcamp\P2_Project_Organizer`. It refuses to overwrite an
existing project. The starter deliberately contains source material and build
contracts, not a finished organizer.

The starter's `.agents/plugins/marketplace.json` is local catalog metadata, not
automatic user-level discovery. The live lesson has each learner register the
P2 project root with `codex plugin marketplace add` before restarting the app
and installing Project Organizer.

`reference/` is the tested implementation produced by the lesson prompts. It
contains the SQLite builder, read-only local MCP server, project-organizer
skill, two read-only workers, sequential reviewer, visual renderer, and
deterministic release hook. It is not copied to the learner project.

Maintainer checks:

```text
python3 instruments/p2_control_plane/reference/tests/verify_reference.py
npm ci --prefix instruments/p2_control_plane/reference/plugins/project-organizer --ignore-scripts --no-audit --no-fund
npm test --prefix instruments/p2_control_plane/reference/plugins/project-organizer
powershell -NoProfile -ExecutionPolicy Bypass -File instruments/p2_control_plane/reference/tests/configure_smoke.ps1
```

The reference MCP test makes no network calls after `npm ci` completes.
The PowerShell check verifies that MCP configuration is an idempotent bounded
edit and preserves unrelated project settings.
