# Module 0 facilitator runbook

## What this session must prove

Each learner can give AI a clear, limited job, check a material claim at the source, prove their own check is capable of failing, keep the draft inside the class, handle one changed fact, and leave work another person can inspect.

Setup is an entry condition, not the lesson, and it is not part of the PO-00 result. A learner whose machine is not ready records `HOLD` on setup and moves to a loaner machine or a paired observation path. Observation keeps the learner in the room but does not pass the operating task.

The module is scored on the supplied Northstar case. There is no second case. The learner has the case, the request, the changed input, and the practice checker in full; what they do not have is the protected acceptance control, which lives off their machine and is run by the evaluator.

## Before learners arrive

1. Run the relevant setup path on the actual classroom images.
2. Record each platform, architecture, installed versions, and date.
3. Confirm the course repository is clean and reachable.
4. Confirm the cohort's Codex authentication method, xAI model, and spending limit.
5. Rotate all setup proof folders and prior learner work.
6. Confirm the protected acceptance control is reachable from evaluator infrastructure and from nowhere a learner can reach.
7. Run one passing and at least three failing specimens through the protected control.
8. Confirm an accessible same-state path for every control a learner must operate.
9. Prepare a support owner for managed-machine and account problems.
10. Put a visible clock where learners can see the 60-minute first-draft limit.

## Session shape

The session runs 180 minutes: 120 minutes of learner working time and 60 minutes you lead. The learner's timebox covers only the 120.

### Facilitator-led segments

| Segment | Clock | What you do |
|---|---|---|
| Opening | 0:00–0:20 | Take the setup state for each learner and route anyone blocked. Name the case and the sharing limit. State plainly that a protected acceptance control decides the result, that it is not on their machine, that the practice checker is theirs to read, and that editing the practice checker moves nothing. Start the visible clock. |
| Checkpoint | 1:15–1:35 | Take the first-draft state from each learner. Confirm each direction brief and screen file was saved before the run. Anyone past two failed corrections is `HOLD` — record it and move them on rather than letting them rebuild. Do not read anyone's draft aloud. |
| Close | 2:40–3:00 | Collect the work folders. Confirm the original draft and the first failed output survive. Hand the folders to the evaluator; the protected control runs off these machines. Name what is unresolved for each `HOLD`. |

### Learner working time

| Clock | Learner work | Evidence you should see |
|---|---|---|
| 0:20–0:30 | Work folder created; acceptance control confirmed and recorded | `acceptance-control.md` naming where the deciding control runs |
| 0:30–0:40 | Case and practice checker read | The learner can name two things the checker cannot judge |
| 0:40–0:50 | Delegation decision and responsibility screen | Both files saved, both before any AI run |
| 0:50–1:00 | Direction brief frozen | Acceptance, falsifier, stop condition, and correction limit are all written |
| 1:00–1:15 | First draft produced and practice check run | A file on disk and a check output, by minute 60 of learner time |
| 1:35–1:50 | Material claim checked against the source | Exact source text quoted by the learner, not by the model |
| 1:50–2:00 | Falsifier run against a deliberately wrong copy | `falsifier-probe.md` plus the observed failure copied verbatim |
| 2:00–2:10 | Capability-limit statement written | Model output, product surface, harness control, and human decision separated; one capability and one limitation from this run |
| 2:10–2:15 | Class-review decision | `PASS FOR CLASS REVIEW` or `HOLD`, with a reason |
| 2:15–2:35 | Changed input predicted, applied, and compared | Prediction timestamped before the second run; `artifact.md` untouched |
| 2:35–2:40 | Handoff written | Another person can find the work without asking |

## Coaching limits

You may:

- point to the current step;
- define a term in plain language;
- help recover the machine or open a supplied file;
- ask what source supports a claim;
- remind the learner of the correction limit.

You may not:

- supply the delegation decision;
- fill in the responsibility screen;
- rewrite the direction brief;
- identify the material source line;
- describe how the protected acceptance control decides;
- tell the learner which statements the changed input should move;
- tell the learner what to break in the falsifier probe;
- accept a narrated action in place of an operation.

If coaching crosses one of those lines, mark that part of the attempt as guided practice in the evidence record. The evaluator scores what the learner operated, not what you supplied.

## Setup triage

| State | Action |
|---|---|
| Command missing in every new terminal | Return to the PATH step; do not reinstall all tools |
| Key missing in a new terminal | Expected; repeat hidden entry |
| Repository dirty before learner work | Inspect and reset with the owner; never delete blindly |
| Provider unavailable | Use the approved same-capability substitute and record it, or `HOLD` |
| Obsidian or n8n unavailable | Record the setup `HOLD`; it does not hold the module result, and a browser screenshot is not an equivalent operation |
| Managed policy | Capture the exact message and route it to the IT owner |
| Learner exceeds two draft corrections | Preserve the attempts and record the practice result as `HOLD` |

## End-of-session collection

Collect or verify:

- setup report path;
- `acceptance-control.md`;
- first-checked-draft timestamp;
- delegation and responsibility records, created before the run;
- original brief, draft, first check output, source check, and decision;
- `falsifier-probe.md` and the recorded observed failure;
- capability-limit statement;
- changed-input prediction and the unchanged original;
- handoff;
- reason for any `HOLD`;
- support packet for any blocked dependency.

Do not collect API keys, environment dumps, account screenshots, or the learner's full home path.
