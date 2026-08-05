# P5 blocked items

## Verified on the author host (macOS)

- OpenCode `1.18.11` accepts the generated deny-by-default config through
  `opencode --pure debug config`.
- The resolved config retains the exact edit rule: deny `*`, allow only
  `out/triage_candidate.json`.
- Disabled MCP stubs resolve with `enabled: false`; `opencode --pure mcp list`
  succeeds when no server is configured.
- `opencode --pure debug agent p5_reader` loads the P5 reader with filesystem
  tools off, Obsidian read methods allowed, and Obsidian write/append/patch
  denied.
- P5 automated tests cover strict candidate validation, promotion evidence,
  exact staging deltas, modern session-export parsing, empty-export HOLD, and
  intent-only inventory HOLD.
- The P4 baseline verifier passes freeze/check and detects tampering against the
  complete fixture and P5 fallback when rerun from the repository root.

These checks prove the deterministic repository behavior. They do not prove
Windows process inheritance or a live Obsidian session.

## Still environment-blocked

The author host has no Windows PowerShell/OpenCode/Obsidian image. Live proof is
still required for:

1. `Start-P5Exposed.ps1` on Windows with `HB_XAI_MODEL` set and pinned OpenCode
   `1.18.11` available through `npx`.
2. A global P4 Obsidian MCP registration present before launch, proving the P5
   launcher discovers it, resolves it to `enabled: false`, strips API-key
   variables, and leaves it non-callable in the child session.
3. A live denied edit outside `out\triage_candidate.json` and a successful edit
   to that exact file.
4. A real `opencode export SESSION_ID` from the exposed session parsed by
   `audit_exposed_session.py`.
5. The full live poisoned-acceptance cycle: approved MCP patch, temporary
   poisoned baseline PASS, fresh read-only wrong cited answer, official baseline
   HOLD, approved MCP repair, fresh corrected retrieval, official baseline PASS.
6. A timed learner pilot establishing the 3–3.5 hour estimate.

Any inconclusive item above is a HOLD for that live run. It is not evidence that
the deterministic pack or scripts failed.
