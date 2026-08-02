# P3 MCP evidence packet

| Run field | Entry |
|---|---|
| Date | YYYY-MM-DD |
| Track | engineering / mission_ops |
| Comparator | `COMPARATOR.md` |
| Purpose | Source every material row plus every agreed claim that drives the release decision |

## Reviewed connection

Record an exception instead of copying a long protocol inventory.

| Expected course connection | Confirmed / exception |
|---|---|
| Project config launches the reviewed local server with the selected `p3_desk` root | |
| Codex alias `p3_evidence`; self-reported server `p3-evidence@1.0.0`; local `stdio` | |
| Exactly `list_evidence_files` and `read_evidence_file`; no resource, prompt, credential, network, or write surface | |
| Approval mode `prompt`; one approval does not authorize another call | |
| Local process still runs with the current user's privileges; this is not an OS sandbox | |

The locked course server and CI own the fixture tests: unknown files, traversal, symlinks, oversized or malformed files, empty resources and prompts, configuration refusal, and dependency-free disable. The learner run uses the intended surface to build the evidence below.

## Source plan and actual use

| Field | Entry |
|---|---|
| Decision-driving claims (WatchID / field) | |
| Planned source basenames, grouped | |
| Actual source basenames approved | |
| Unexpected request | none / denied tool or basename: |
| Calls match the plan | yes / no · explain: |

## Source inventory

List each source once. Add rows as needed.

| Source basename | SHA-256 | Decision-driving claims served |
|---|---|---|
| | | |

## Evidence appendix

Use one E-ID per source item; when a claim depends on two sources, give it two rows and two E-IDs. Reuse a file read across every claim it supports. Add rows as needed. Codex fills the returned excerpt and draft source relation in Stage 04. You fill the two raw-source columns in Stage 05; preserve the returned excerpt even when you correct it.

| E-ID | WatchID / field | Competing or agreed claim | Source basename + SHA-256 | Codex-returned excerpt (20 words or fewer) | Draft source relation (supports / contradicts / insufficient) | Raw-source context match? | Corrected excerpt or context, if needed | Missing evidence / why |
|---|---|---|---|---|---|---|---|---|
| E-01 | | | | | | | | |
| E-02 | | | | | | | | |
| E-03 | | | | | | | | |

## Cleanup and interpretation

- Managed project config says `enabled = false`: yes / no
- `P3 — MCP Evidence — [TODAY'S DATE]` task closed after the packet was saved: yes / no
- Unexpected surface or behavior: none / describe
- Required interpretation: **MCP result = shared retrieval path, not independent corroboration.**
