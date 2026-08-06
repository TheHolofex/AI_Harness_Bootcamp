# P6 mission · Clear the Overnight Watch

This exercise shows what agentic work feels like when the agent owns a complete
piece of work, not one answer.

At 06:30, four overnight feeds disagree. Some reports are stale. One is a
duplicate. Deadlines overlap. Two sites could use the only mobile power unit.
You will watch Goose inspect the files, decide what matters, build an operating
picture, test it, and repair it without waiting for step-by-step instructions.

Then new evidence arrives. You will state what matters in your own words and
watch the agent revise the same work without losing what remains true.

## 1. Launch the morning command center

Open PowerShell anywhere and paste:

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\Documents\HarnessBootcamp\AI_Harness_Bootcamp\mission_flesh\p6\scripts\Start-P6.ps1"
```

Goose works in `runs\current`. It reads 14 evidence items across Markdown,
CSV, JSON, and a message dump. It makes a provisional choice for MPU-1, creates
the command center and its machine-readable state, runs the verifier, and
repairs any HOLD findings.

Wait for `P6 VERIFY PASS`. The assignment can differ when another choice is
supported by the evidence. After PASS, `command_center.html` opens
automatically. Spend a minute with it. Look for the priority order, the next
90 minutes, the MPU-1 rationale, and the
evidence ledger. Open `mission_state.json` if you want to see the same truth as
structured data.

## 2. Choose one direction and update the watch

Both directions are defensible. Choose one complete command and paste it
without editing.

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\Documents\HarnessBootcamp\AI_Harness_Bootcamp\mission_flesh\p6\scripts\Update-P6.ps1" -Intent "Clear the ambulance route first, even if relay restoration slips."
```

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\Documents\HarnessBootcamp\AI_Harness_Bootcamp\mission_flesh\p6\scripts\Update-P6.ps1" -Intent "Protect the regional coordination window; keep bridge clearance moving manually."
```

Your choice sets the operating priority. The launcher preserves that sentence
exactly. A late update now reopens Route Bravo for light vehicles, stabilizes
Cold Store 7, and turns Bridge Foxtrot into an ambulance priority. Goose must
reconcile the new evidence with the original feeds and your intent, then revise
the same two outputs.

After `P6 VERIFY PASS`, the revised command center opens automatically. Its
before/after view shows what is **NEW**, **CHANGED**, **CANCELLED**, and
**UNCHANGED**. That visible
continuity is the point of P6: the agent did not merely produce a second
summary. It maintained a checked body of work as the situation changed.

## If the run stops

A `P6 VERIFY HOLD` line names a factual gap. Rerun the same command. Wave 2 can
be rerun with the same or a revised `-Intent`. To begin again from the original
overnight watch, rerun `Start-P6.ps1`; it replaces `runs\current` with a fresh
Wave 1 workspace.
