# P2 project instructions

- Use `gpt-5.6-terra` for the main thread and every subagent.
- Read `HARNESS_PROFILE.md` before changing the daily-brief workflow.
- The main agent owns all writes. Before spawning a research or review agent,
  set the live parent turn to `Read only`. Return to `Ask for approval` only in
  a separate main-writer turn.
- Use only the files under `inputs/p1/` for claims in the daily brief. Preserve
  source qualifiers and cite factual claims with their C-number.
- Write the release candidate to `out/FINAL_DAILY_BRIEF.md` and leave source
  files unchanged.
- Never print, copy, or store API keys. Ask before any external write or
  destructive action.
- Keep no more than two spawned threads open. Wait for requested results, keep
  the concise returns, and close completed threads before another batch.
- A failing quality-gate receipt means HOLD. Attempt at most one focused repair;
  do not weaken the contract to obtain a pass.
