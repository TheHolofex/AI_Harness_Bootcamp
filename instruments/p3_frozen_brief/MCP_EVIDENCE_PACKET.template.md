# P3 MCP evidence packet

| Run field | Entry |
|---|---|
| Date | YYYY-MM-DD |
| Track | engineering / mission_ops |
| Comparator | `COMPARATOR.md` |
| Purpose | Source every material row plus every agreed claim that drives the release decision |

## Why this connection has this shape

This is the reviewed course design, not a worksheet to recreate. Record only an exception you actually observe.

| Decision | Reviewed P3 design |
|---|---|
| Work goal and fit | Build a reusable, auditable source packet for the decision-driving claims. A direct read is simpler for this tiny one-off corpus; MCP earns its place here through a reviewed retrieval boundary and a useful-call receipt that carries into the final handoff |
| Primitive | Two model-selected read tools under host policy; no resource or prompt because every content read requires a visible approval |
| Transport | Local `stdio`: one Codex host launches one reviewed process for one user; no remote service or OAuth is needed |
| Authority | Exact file allowlist, exact tool allowlist, approval per call, short timeouts, and no credential, network, or write surface |
| Exit | Packet saved, managed connection disabled, evidence task closed |

Exception from the reviewed design: none / describe

## Reviewed connection

Record an exception instead of copying a long protocol inventory.

| Expected course connection | Confirmed / exception |
|---|---|
| Course repository origin + commit recorded; `server.mjs` and `package-lock.json` are unmodified; SHA-256 fingerprints recorded for this run | |
| Project config launches the reviewed local server with the selected `p3_desk` root | |
| Codex alias `p3_evidence`; self-reported server `p3-evidence@1.0.0`; local `stdio` | |
| Exact server instructions reviewed; they do not change the planned workflow | |
| Exactly `list_evidence_files` and `read_evidence_file`; titles, descriptions, input/output schemas, and annotations match `--describe` | |
| No resource, prompt, credential, network, or write surface | |
| Approval mode `prompt`; one approval does not authorize another call | |
| Local process still runs with the current user's privileges; this is not an OS sandbox | |

The repository origin and commit establish where the reviewed implementation came from; the local hashes fingerprint the exact files used in this run. The locked course server and CI own the fixture tests: unknown files, traversal, symlinks, oversized or malformed files, empty resources and prompts, configuration refusal, and dependency-free disable. The learner run uses the intended surface to build the evidence below. Tool schemas validate the shape of a request or result; they do not prove that server metadata or returned claims are true. Source hashes and the Stage 05 raw-context check establish the evidence.

## Source plan and actual use

| Field | Entry |
|---|---|
| Decision-driving claims (WatchID / field) | |
| Planned source basenames, grouped | |
| Actual source basenames approved | |
| Deviation, error, retry, or denied request | none / describe: |
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
- Did standardized retrieval, provenance, and scope control earn the connection overhead for this job? yes / no · why
- Required interpretation: **MCP result = shared retrieval path, not independent corroboration.**
