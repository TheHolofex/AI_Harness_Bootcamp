# P2 personal control plane

This kit creates the isolated Windows project used by P2. The website is the
student guide; this file is the maintainer map for the files behind it.

`bootstrap.ps1` copies `starter/` and the learner's completed P1 folder into
`Documents\HarnessBootcamp\P2_Control_Plane`. It refuses to overwrite an
existing project. If P1 was completed elsewhere, pass that folder with
`-P1Source`.

The starter contains:

- a short `AGENTS.md` and a focused repo skill for the P1 daily brief;
- three custom agents used under read-only parent turns, including one bounded
  to the official OpenAI Developer Docs MCP server;
- a repo marketplace with the course's release-control plugin;
- a disabled-by-default `Stop` quality gate and a smoke test;
- a harness profile and active-component release record.

Run the deterministic smoke test from the repository root:

```text
python instruments/p2_control_plane/starter/plugins/p2-release-control/tests/smoke_test.py
```

The hook is inert unless the active project contains
`P2_CONTROL_PLANE.json` with `enabled` set to `true`.
