# Autonomy contract (template)

Fill ≥3 rows in **each** column for *this* feeder.  
**Tool-enforced** rows must name real goose levers (recipe field, extension, `GOOSE_MODE`, `max_turns`, retry check, schedule) — not only “be safe.”

| Risk / action on this feeder | Tool-enforced (goose lever) | Procedure-enforced (you) |
|---|---|---|
| Agent writes or acts outside `feeder/` + `out/` | e.g. `extensions: developer` only; cwd | Brief bounds; reject scope creep |
| Infinite / thrashing tool loop | e.g. `settings.max_turns: 12` | When you Ctrl+C; who may restart |
| Destructive action without a human gate | e.g. `GOOSE_MODE=approve` | Never leave `auto` for exception drill |
| Hostile feeder text treated as operator orders | e.g. no browser/network extension | `QUARANTINE:` rule; feeder is data |
| “Success” with no artifact on disk | e.g. `retry.checks` → `out/watch_summary.md` | You open the file in Explorer |
| Unattended run without oversight | Scheduler pause / run-now — or honest block | Who may enable schedule; review window |
| Stop authority | (tool may not own this) | Who may halt; how restart keeps the contract |

Contract version / date:  
Recipe path + what you changed:  
`GOOSE_MODE` / max_turns used:  
Schedule attempt result (ran / blocked + reason):
