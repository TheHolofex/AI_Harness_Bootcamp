# P3 Comparator

**Student:** ________

## Run control

| Field | Recorded value |
|---|---|
| Brief | `BRIEF-v1.md` · unmodified: yes / no |
| Track | engineering / mission_ops |
| Working folder | `Documents\HarnessBootcamp\p3_desk` |
| Date | YYYY-MM-DD |
| Brief ambiguity to watch | none noted / describe |

## Run identity

| | Engine A | Engine B |
|---|---|---|
| Tool | Codex app | OpenCode |
| Model id | `gpt-5.6-terra` | `xai/` + the value of `HB_XAI_MODEL` |
| Credential role | OpenAI API key stored in Codex sign-in | `XAI_API_KEY` environment variable through OpenCode |
| Version | | |
| Run label | `P3 — Engine A — [TODAY'S DATE]` | exact OpenCode command |
| Retry / failure record | none / first chat + failure + retry chat | none / describe service failure |
| Run separation and shared paths recorded | clean folder ☐ · or instruction files declared below ☐ | `OPENCODE_DISABLE_CLAUDE_CODE=1` ☐ · `--pure` ☐ |
| Context loaded (Codex app) | `AGENTS.md` ☐ · skills ☐ · plugins/hooks ☐ · custom agents ☐ · memories ☐ — list which: ________ | — |
| MCP surface during frozen run | no user-configured/external server active confirmed with `/mcp verbose` ☐ · unavoidable built-ins listed but not invoked ☐ · or list every exception below | — |

The Codex app can load `AGENTS.md`, skills, plugins and hooks, custom agents, memories, and MCP surfaces. Run P3 in your P2 project and Engine A is carrying the control plane you built while Engine B runs bare — that is one engine plus your harness, not two engines. Declare it or run clean.

## Side-by-side (add rows as needed)

During Stage 03, add every material difference. Before Stage 04, also add each agreed claim that drives the release decision and mark `Agree?` as `yes`. Leave low-consequence agreement out.

| WatchID | Field | Codex app | OpenCode | Agree? | Operator verdict (keep/discard/unknown) | Evidence ID + why |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |
| | | | | | | |

## Comparison result

Deterministic join check: pass / exception: ____

Fields inspected: ____

Material differences: ____

Dispositions: keep ____ · discard ____ · unknown ____

A discard count of zero is valid when the sources support every consequential claim.

## MCP evidence packet — after both raw runs and comparison

The source plan, source inventory, returned excerpts, raw-context checks, and cleanup live in `MCP_EVIDENCE_PACKET.md`. This comparator owns the final keep / discard / unknown verdict and its E-ID in the side-by-side table above.

## Adjudication note (supervisor-readable)

### Supported operational picture

WatchID by WatchID:

### Unknowns and missing evidence

### Discarded or qualified claims

### Release decision

USE / USE WITH LIMITS / HOLD

### Residual risk

### Next action


## Files

- [ ] output_codex.md
- [ ] output_opencode.md
- [ ] MCP_EVIDENCE_PACKET.md
