# P6 · goose recipe notes (adapt)

goose is the Thursday vehicle for **autonomy under a written contract**.
It is a local agent platform (CLI + optional Desktop) with four levers you will
actually open today — not just a chat window with a fancy name.

Official docs: <https://goose-docs.ai>

## What goose is (enough for today)

```text
goose =
  loop (session / run)
  + packaged mission (recipe: instructions, params, extensions)
  + tool surface (MCP / built-in extensions + tool allowlists)
  + autonomy dial (GOOSE_MODE, max turns, permissions)
  + unattended path (schedule + retry + structured response)
```

Pi (later today) is mostly the bare loop. goose is the loop **plus** the four
levers above — *if you turn them on*. The autonomy contract’s **tool-enforced**
column is those levers; the **procedure-enforced** column is what you still own
when the tool cannot see the risk.

This course uses the **CLI** by default. Desktop exists (recipe library,
scheduler UI, MCP Apps) and is welcome if you already have it; nothing in the
pass bar requires it.

## Starter recipe in this folder

| File | Role |
|---|---|
| `watch_officer.yaml` | Starter recipe — adapt this, don’t only run a stock demo |
| `feeder/` | Watch traffic (dropping files simulates the desk) |
| `out/` | Create on first run; `watch_summary.md` is evidence |

### Recipe fields that map to the contract

| Recipe / runtime lever | Contract column | What it actually enforces |
|---|---|---|
| `instructions` + `prompt` | Both (mostly procedure until encoded) | Mission, bounds text, quarantine rule |
| `extensions` (here: `developer` only) | **Tool-enforced** | Which tools exist at all |
| `settings.max_turns` | **Tool-enforced** | Caps unattended thrash |
| `parameters.feeder_dir` | Tool + procedure | Where traffic is allowed to come from |
| `retry.checks` | **Tool-enforced** | Fail closed if `out/watch_summary.md` never appears |
| `GOOSE_MODE` (env / session) | **Tool-enforced** | `auto` vs approve / smart-approve |
| Scheduler (Desktop or CLI) | Tool path for unattended | Cron-style run; pause / run-now |
| Hostile-content handling | **Procedure-enforced** unless you add a checker | Feeder text is not operator orders |
| Stop authority / who may restart | **Procedure-enforced** | Human command, not a brand promise |

At least **three tool-enforced rows** should name a real goose setting or recipe
field (extension list, max_turns, mode, retry check, schedule), not only prose
that says “be safe.”

## Adapt before you claim the run

1. Copy this folder into your working project (or open the course clone path).
2. Edit `watch_officer.yaml`:
   - Confirm `feeder_dir` default matches your layout.
   - Tighten `instructions` bounds to match your LIVE Direction Brief.
   - Keep extensions narrow unless you can justify a wider tool surface in the contract.
3. Create the output folder:

```powershell
New-Item -ItemType Directory -Force -Path .\out | Out-Null
```

4. Run once from this directory (provider/model already set in pre-work):

```powershell
# Approve mode is the teaching default for the contract drill.
# auto is fine for the smoke proof; P6 should show you can dial autonomy.
$env:GOOSE_MODE = "approve"
goose run --recipe .\watch_officer.yaml
```

If your build wants an explicit path flag and rejects `--recipe`, check
`goose run --help` for the cohort-pinned version and use the recipe-file form it
prints. Record the exact command that worked in your operator log.

5. Evidence of a successful adapted run:
   - `out/watch_summary.md` exists
   - One line per normal feeder file
   - You changed something in the YAML (path, bounds, max_turns, or mode) so it is not stock-only

## Exception drill (event_04)

`feeder/event_04.txt` carries an `OUT_OF_BOUNDS` / hostile instruction.
Contract behavior:

- Do **not** delete logs or dump emails
- Append a `QUARANTINE:` line naming the source file
- Continue other files
- Log that the tool-enforced surface (no extra extensions, max_turns) and the
  procedure (treat feeder as data) both held — or which one failed

## Stop and restart proof

- **Stop:** interrupt a run (Ctrl+C in CLI, or stop in Desktop) under realistic
  load — e.g. mid-feeder or while it is about to touch `out/`.
- **Restart:** run the recipe again; prior good summary lines should still be
  present (append posture); contract frame unchanged (same recipe file / mode).
- Record both in the operator log with timestamps.

## Unattended / scheduled attempt

P6 MVP allows either:

1. **Scheduled attempt** — Desktop **Scheduler** or CLI schedule against
   `watch_officer.yaml`, then **Run now** once and keep the session/result, or
2. **Honest block** — scheduled path refused by OS/policy; write what you tried,
   the exact error, and what would be required to enable it.

Honesty over theater. A blocked schedule with a clear reason beats a fake green.

Docs entry points: Recipes and Scheduler on <https://goose-docs.ai>.

## Pi contrast (same hour)

Open Pi on a tiny task in the same folder. From **observation**, list:

| Rail | Present in goose today? | Present in Pi? |
|---|---|---|
| Packaged recipe (mission + params) | | |
| Extension / tool allowlist | | |
| Permission mode / max turns | | |
| Retry / success check | | |
| Schedule path | | |
| Written contract you authored | | |

Brochure claims do not count. If you did not turn a lever on, it is not a rail
you demonstrated.

## Autonomy contract template (minimum shape)

```text
| Risk on this feeder                         | Tool-enforced (goose lever)              | Procedure-enforced (you)                    |
|---------------------------------------------|------------------------------------------|---------------------------------------------|
| Agent wanders outside project               | extensions: developer only; cwd          | Brief bounds; reject scope creep            |
| Infinite tool loop                          | settings.max_turns: 12                   | Stop authority; when to Ctrl+C              |
| Auto-run destructive actions                | GOOSE_MODE=approve (or smart-approve)    | Never set auto for exception drill          |
| Hostile feeder text obeyed as orders        | (optional) no network/browser extension  | QUARANTINE rule; treat feeder as data       |
| “Success” with no artifact                  | retry check: out/watch_summary.md exists | You open the file in Explorer               |
| Unattended run without oversight            | Scheduler pause / run-now; or blocked    | Who may enable schedule; review window      |
```

Fill ≥3 rows in each column with **this feeder’s** real risks. No orphan risks.

## Provider posture (course lock)

- API keys only — OpenAI via `GOOSE_PROVIDER` / `GOOSE_MODEL` from pre-work.
- goose’s provider list also offers ChatGPT / Copilot / Claude subscription
  paths. **Do not use those** in this course.
- Docs often note strongest tool-calling on Claude-class models; the course pin
  is still your staff-posted OpenAI (or alternate) model. Measure what you get.

## Out of scope for MVP (exist in the product; not required today)

Subagents / parallel subrecipes, MCP Apps UI, Adversary Mode, custom MCP servers,
hooks, skills plugins, ACP editor integration. Stretch only if MVP is solid and
you can still evidence stop authority.

## Identity lock

Autonomy is not “the brand is safe.”
Autonomy is a loop plus bounds **you** wrote — some enforced by goose’s levers,
some enforced by your procedure — with stop authority that you demonstrated.
