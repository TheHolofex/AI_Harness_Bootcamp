# P6 · Clear the Overnight Watch

P6 is the moment the course stops feeling like prompt practice. One Goose run
reads four different overnight feeds, resolves stale and duplicate reports,
makes a real resource tradeoff, builds a polished browser-ready command center,
checks its own work, and repairs it until the facts hold together.

Then the situation changes. The learner gives one plain-language intent, and
Goose resumes the same mission and revises the operating picture in place.

The learner experience is deliberately small:

1. Launch Wave 1.
2. Inspect the command center that opens.
3. Choose and paste one complete Wave 2 command.
4. Inspect what the agent changed, cancelled, added, and preserved.

Use [MISSION.md](MISSION.md) for the two learner commands.

## What is in the pack

| Path | Purpose |
|---|---|
| `MISSION.md` | Learner mission and exact commands |
| `clear_overnight_watch.yaml` | One prepared Goose mission for both waves |
| `scenario/wave-1/incoming/` | Four mixed-format overnight feeds |
| `scenario/wave-2/late_update.md` | The late update revealed after Wave 1 passes |
| `scripts/Start-P6.ps1` | Prepare and run Wave 1 |
| `scripts/Update-P6.ps1` | Add intent and run the in-place revision |
| `scripts/verify.mjs` | Factual outcome verifier |
| `runs/current/` | Fixed working directory, generated and ignored by Git |

Goose keeps the learner's normal profile and adds the native Developer
extension. The recipe does not restrict tools, turns, or profile extensions.
The two mission outputs are:

- `runs/current/command_center.html`
- `runs/current/mission_state.json`

## Staff checks

From `mission_flesh\p6`:

```powershell
npm test
powershell -ExecutionPolicy Bypass -File .\scripts\Start-P6.ps1 -PrepareOnly
```

`-PrepareOnly` checks Node, Goose, the native Developer extension, and the
recipe before resetting and preparing `runs\current`. It makes no model call
and intentionally leaves the mission at HOLD because the two outputs do not
exist yet.
