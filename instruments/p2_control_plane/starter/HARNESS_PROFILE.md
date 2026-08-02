# P2 harness profile

## Work product

- Product: Regenerable daily status brief
- Reader: [replace from the P1 release contract]
- Decision this supports: [replace]
- Final path: `out/FINAL_DAILY_BRIEF.md`

## Acceptance contract

- Current source set is declared in `inputs/p1/SOURCE_MANIFEST.md`.
- The brief contains Shipped, Broken, Blocked, and Asks.
- Every factual claim carries a source tag such as `[C3]`.
- Source uncertainty and qualifiers remain visible.
- No TODO, TBD, placeholder, OpenAI-shaped key, or xAI-shaped key remains.
- The quality-gate receipt is PASS before release.

## Control routing

| Need | Surface | Why it belongs there |
|---|---|---|
| Short project constraints | `AGENTS.md` | Always present in this project |
| Daily-brief procedure | `.agents/skills/daily-brief-release/SKILL.md` | Loads for this repeatable product |
| Release check | P2 Release Control plugin + `Stop` hook | Runs even when the model forgets to self-check |
| Source inspection | `evidence_scout` subagent | Isolates a read-heavy evidence pass |
| Independent product review | `decision_reviewer` subagent | Challenges the draft before the main writer releases it |
| Current Codex behavior | `docs_researcher` + official Docs MCP | Uses current primary documentation instead of model memory |
| Permission and cost limits | Project config + live parent-turn mode | Caps open threads, makes research and review read-only, and leaves external authority with the operator |

## Runtime limits

- Main and subagent model: `gpt-5.6-terra`
- Maximum open subagent threads: 2; close completed threads before another batch
- Research and review parent turns: `Read only`
- Main writing turns: `Ask for approval`
- External writes: none
- MCP surface: official OpenAI Developer Docs, read-only research role only
- Quality-gate continuation: one focused repair maximum
- Operator approval: required for any action outside this project

## Evidence produced

| Evidence | Path | Result |
|---|---|---|
| Current configuration check | `out/CONFIG_EVIDENCE.md` | [pending] |
| Plugin inspection | `out/PLUGIN_REVIEW.md` | [pending] |
| P1 source map | `out/EVIDENCE_MAP.md` | [pending] |
| Final daily brief | `out/FINAL_DAILY_BRIEF.md` | [pending] |
| Independent decision review | `out/DECISION_REVIEW.md` | [pending] |
| Quality-gate receipt | `out/QUALITY_GATE_RECEIPT.json` | [pending] |
| Run receipt | `out/RUN_RECEIPT.md` | [pending] |
| Active-component manifest | `out/ACTIVE_CONTROL_PLANE.md` | [pending] |

## Release record

- Started: [local time]
- Finished: [local time]
- Elapsed minutes: [observed]
- Main turns: [observed]
- Subagent runs: [observed]
- Manual repair passes: [observed]
- Approval prompts: [observed]
- Usage or cost shown by the active surface: [amount or "not exposed"]
- Decision: KEEP / REVISE / REVERT
- Component to keep: [name and reason]
- Component to leave off until needed: [name and trigger]
- Residual risk: [one concrete sentence]
