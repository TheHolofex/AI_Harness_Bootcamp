# P5 verification status

## Verified on the author host (macOS)

- The generated OpenCode configuration is deny-by-default and retains the exact
  candidate write path.
- Inherited MCP server entries resolve with `enabled: false`.
- P5 automated tests cover strict candidate validation, promotion evidence,
  exact staging deltas, modern session-export parsing, project-root binding,
  grep-path handling, protected-content disclosure, empty-export HOLD, and
  intent-only inventory HOLD.
- The closed reference pack passes its manifest and checksum checks. Tampering
  is rejected.
- The active learner page and P5 pack contain no dependency on another exercise
  or a separate knowledge application.

## Live checks still required

1. Run `Start-P5Exposed.ps1` on the course Windows image with
   `HB_XAI_MODEL` set and pinned OpenCode `1.18.11` available through `npx`.
2. Confirm a live write outside `out\triage_candidate.json` is denied and a
   write to that exact path succeeds. Confirm the resolved agent exposes only
   read, edit, and write—not search or listing tools.
3. Export a real exposed session and pass it through
   `audit_exposed_session.py`.
4. Run a timed learner pilot to confirm the 2–2.5 hour estimate and record
   where learners need facilitator help.

An inconclusive live check is HOLD for that run. It does not erase the local
deterministic test results.
