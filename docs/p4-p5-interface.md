# P4 → P5 interface (consume-only read-out)

Recorded from shipped P4 artifacts on disk. P5 may not expand this interface.

## Vault path
- Student trusted vault: `%USERPROFILE%\Documents\p4-vault`
- Course seed: `mission_flesh/p4/vault_seed/`
- Instructor/reference complete vault: `mission_flesh/p4/reference_fixtures/complete_vault/`
- External baseline: `operator/evidence/P4_BASELINE_[YYYY-MM-DD].json`
- In-vault freeze path (also written by baseline tool): `Harness/BASELINE_MANIFEST.json`

## Required root / hub artifacts (complete vault)
From `mission_flesh/p4/docs/VAULT_CONTRACT.md` and `reference_fixtures/complete_vault/`:

| Path | Role |
|---|---|
| `AGENTS.md` | Project instructions |
| `MOC.md` | Map of contents |
| `Mission_Brief.md` | Operator-facing brief (P5 names this; **not** `Morning_Brief.md`) |
| `Audit.md` | Human audit sample |
| `Retrieval/Answers.md` | Cold-session answers Q1–Q4 with wikilinks |
| `Evidence/PERMISSIONS.json` | Director, worker, and retriever permission snapshot |
| `Evidence/MCP_RECEIPTS.jsonl` | MCP write receipts |
| `Harness/HARNESS_CARD.md` | Harness card |
| `Harness/RUN_STATE.md` | Run state |
| `Harness/HANDOFF_RECEIPT.md` | Handoff |
| `Notes/Modes.md` | Hub |
| `Notes/Nodes.md` | Hub |
| `Notes/Constraints.md` | Hub |
| `Notes/Threats.md` | Hub |
| `Notes/Sources.md` | Hub |
| `Notes/Route/Spine.md` | Route spine |
| `Notes/Content/*.md` | Content notes (≥8 with full source front matter) |
| `tools/verify_baseline.py` | Path/hash freeze and check |
| `tools/verify_brain.py` | Semantic brain verify |
| `tools/verify_vault.py` | Thin shim → brain default; baseline via flags |

**P5 Stage 01 minimum presence check (consume):** `MOC.md` and `Mission_Brief.md` (contract explicitly: “P5 names this file”). Prefer also confirming hubs under `Notes/`.

## Hubs and mission roots hostile intake may name
Safe demand targets (exist in complete vault / contract):
- `Mission_Brief.md`
- `Retrieval/Answers.md`
- `Notes/Modes.md`, `Notes/Nodes.md`, `Notes/Constraints.md`, `Notes/Threats.md`, `Notes/Sources.md`
- `Notes/Route/Spine.md`
- `Audit.md`
- Content examples: `Notes/Content/Rail_Clearance.md`, `MBT_Envelope.md`, `Sealift_Options.md`, `Protection_LOC.md`, `Export_Port.md`, `Taiwan_Arrival.md`, `Road_OSOW.md`, `Export_Controls.md`

Do **not** name `Morning_Brief.md`, `Systems.md`, or MERIDIAN hubs — those are archived only under `archive_meridian_seed/`.

## Baseline JSON schema (v1)
Produced/checked by `verify_baseline.py`:

```json
{
  "schema_version": 1,
  "vault_root": ".",
  "root_fingerprint": "<sha256 over sorted path:sha256 lines>",
  "terminal_reason": "SUCCESS",
  "verification": { "tool": "verify_baseline", "file_count": 0 },
  "files": [ { "path": "MOC.md", "bytes": 0, "sha256": "..." } ]
}
```

Skips `.obsidian`, `__pycache__`, `.git`. Excludes `Harness/BASELINE_MANIFEST.json` from the file list when freezing.

## Verifier CLI (P5 integrity)
Prefer direct baseline tool (do not teach `verify_vault.py` on the P5 required path):

```text
py -3 tools/verify_baseline.py <vault_root> --write-manifest [--external PATH]
py -3 tools/verify_baseline.py <vault_root> --check-manifest PATH_TO_BASELINE.json
```

Exit 0 prints `PASS baseline ...`. Exit 1 prints `HOLD baseline: ...` on stderr.

Course-relative path students use:

```text
%USERPROFILE%\Documents\HarnessBootcamp\AI_Harness_Bootcamp\mission_flesh\p4\vault_seed\tools\verify_baseline.py
```

Shim (not for P5 learner path): `verify_vault.py --check-manifest` / `--write-manifest` delegates to baseline.

## MCP registration (as shipped by P4)
- Product: **Obsidian Local REST API** built-in authenticated MCP endpoint.
- Human opens Obsidian on `Documents\p4-vault`, enables Local REST API, API key in **environment variable only**.
- OpenCode V1: set `OPENCODE_CONFIG` to `mission_flesh/p4/controller/opencode.p4.json`. Set `OPENCODE_CONFIG_DIR` to `mission_flesh/p4/vault_seed/.opencode`.
- Endpoint in the shipped config: `http://127.0.0.1:27123/mcp/`. The Windows spike must confirm this loopback HTTP path or replace it with trusted-certificate HTTPS.
- Director: MCP read allow; write/append/patch **ask**; delete/move/copy/command **deny**; filesystem edit of vault **deny**.
- Researchers: MCP **deny**; no vault write.
- Cold retriever: runs from empty `Documents\p4-cold-query`; MCP read allowed and write ask; no course repo or raw corpus in the project.
- Evidence: `Evidence/PERMISSIONS.json`, `Evidence/MCP_RECEIPTS.jsonl`.
- P4 ships a machine-readable project config under `controller/` and agent files under `vault_seed/.opencode/agents/`. The learner points the two OpenCode environment variables at those course paths. The learner does not copy agent files into the shared course project.
- **Implication for P5:** if the learner’s OpenCode user config retains a global Obsidian MCP server after P4, the exposed P5 triage session may inherit it. P5 must disable that server for the staging process (separate config dir / explicit deny / stripped key) and prove non-callability. Untested deny is not a boundary.

## Permission snapshot shape
`Evidence/PERMISSIONS.json` (example in seed):

```json
{
  "director": {
    "mcp": {
      "read": "allow", "write": "ask", "delete": "deny", "move": "deny",
      "copy": "deny", "active_file": "deny", "command": "deny"
    },
    "filesystem_vault": "deny",
    "web": "deny"
  },
  "researchers": {
    "mcp": "deny",
    "web": "deny",
    "raw_corpus": "read",
    "filesystem_write": "deny"
  },
  "retriever": {
    "project": "Documents\\p4-cold-query",
    "mcp": { "read": "allow", "write": "ask" },
    "filesystem": "deny",
    "web": "deny"
  }
}
```

## Domain facts P5 intake should not contradict carelessly
From complete vault Mission_Brief / content notes (public logistics framing):
- Combat-loaded MBT planning envelope ~**73.6 st**; primarily **rail + Ro/Ro sealift**, not air.
- Loaded rail planning speed **40 mph** (thin notices claiming 45 mph are audit noise).
- Export through LA/LB complex; arrival preference **Kaohsiung**.
- Sealift transit often **14–21 days** depending on routing/SOA.
- Protection notes end in protect / detect / recover.

## Registry (P4)
- Code `P4`, key `ahb-checklist-p4`, meta rewritten toward second brain / OpenCode + Obsidian MCP (consume live `registry.js` at implement time).

## What P5 does **not** get from P4
- No P4-exported `trusted_facts.json` or brain fact snapshot API.
- No guarantee the learner finished P4 (P5 ships instructor fallback from `reference_fixtures/complete_vault`).
- No project-scoped proof that global OpenCode MCP is off for other projects — P5 must enforce on its launcher.
