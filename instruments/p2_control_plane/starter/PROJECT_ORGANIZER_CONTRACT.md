# Project Organizer build contract

Turn the supplied HarborLight project files into one dependable local project
organizer. Codex should write and test the implementation; the learner directs
the build through the prompts on the course website.

## Required flow

```text
source_packet -> SQLite ledger -> read-only local MCP -> skill and agents
              -> visual project board -> deterministic release hook
```

## Ledger

Create `project_ledger.sqlite3` from the six UTF-8 source files. The schema must
contain exactly these application tables:

- `projects`
- `deliverables`
- `dependencies`
- `decisions`
- `updates`
- `sources`

Use stable source IDs, declared relationships, foreign keys, parameterized
writes, deterministic ordering, and source SHA-256 values. Do not infer a fact
that is absent from the packet. The builder must refuse to overwrite an
existing ledger unless `--rebuild` is present. A rebuild must use a temporary
database and `os.replace` only after integrity and foreign-key checks pass.

## Read-only MCP surface

Expose exactly four STDIO tools:

- `get_project_snapshot`
- `get_ready_work`
- `get_dependency_path`
- `get_decision_queue`

Open the SQLite file in read-only URI mode, enable `PRAGMA query_only`, accept
only bounded typed arguments, and expose no resource, prompt, write, shell, or
network capability. Every tool result must include the same current
`source_fingerprint`. `get_project_snapshot` owns outcome, delivery state,
unknowns, and source coverage; it must not duplicate the dependency path,
blocked-work array, or decision queue returned by the dedicated tools.

Put the shared, data-only ledger verifier in
`plugins/project-organizer/lib/ledger_verifier.py`. Every MCP request uses it
to check the exact schema, all source hashes, and every ledger value against
the source packet before returning data. The trusted hook may execute only
reviewed code bundled inside the plugin. It must treat project Python files,
schema, sources, SQLite, evidence reports, and release files as data and must
never import or run the project-root `verify_project_ledger.py`.

### Locked runtime

Lock the tested runtime exactly in both `package.json` and `package-lock.json`:

- `engines.node`: `>=22.22 <25`
- dependency `@modelcontextprotocol/server`: `2.0.0`
- development dependency `@modelcontextprotocol/client`: `2.0.0`
- dependency `zod`: `4.4.3`

Use exact dependency versions with no caret, tilde, tag, or other range. Define
no install-time lifecycle scripts such as `preinstall`, `install`, `postinstall`,
or `prepare`; package scripts may contain only the explicit `start` and `test`
commands. The class install command is:

```text
npm ci --prefix plugins/project-organizer --ignore-scripts --no-audit --no-fund
```

## Harness

Create one local plugin named `project-organizer` with one skill, the MCP
source, visual renderer, and a `Stop` release hook. Add two read-only workers
named `scope_mapper` and `dependency_planner`. Add one read-only reviewer named
`board_reviewer`, run only after the workers finish. Every model is
`gpt-5.6-terra`.

Update `.agents/plugins/marketplace.json` so its `plugins` array exposes the
local `project-organizer` package. That file is marketplace metadata; creating
it does not register the marketplace with a learner's Codex installation. The
build must not add the marketplace, install the plugin, or change user-level
plugin state. After package review, the learner registers the project root from
a PowerShell terminal with:

```powershell
codex plugin marketplace add "$env:USERPROFILE\Documents\HarnessBootcamp\P2_Project_Organizer"
```

They verify the root with `codex plugin marketplace list`, restart the ChatGPT
desktop app, and install Project Organizer from **AI Harness Bootcamp** under
**Plugins**. Disabling or uninstalling the plugin is separate from removing its
marketplace source with
`codex plugin marketplace remove ai-harness-bootcamp`.

The project-scoped Codex config must launch the MCP server with resolved
absolute paths. Do not depend on plugin-path environment expansion for MCP and
do not add a second `.mcp.json` registration. The project config is the only
MCP registration. Do not silently change the learner's personal plugin
configuration.

The equivalent supported CLI install is:

```text
codex plugin add project-organizer@ai-harness-bootcamp
```

## Agent evidence contract

The parent runs two workers concurrently. Their tool ownership is disjoint and
the four calls together cover the exact MCP surface. Save their exact JSON-only
returns without rewriting them:

- `.project-organizer/evidence/scope_mapper.json`

  ```json
  {
    "role": "scope_mapper",
    "verdict": "PASS",
    "source_fingerprint": "<64 lowercase hex>",
    "tools_used": ["get_project_snapshot", "get_decision_queue"],
    "project_id": "PRJ-001",
    "deliverable_ids": ["<all IDs in snapshot order>"],
    "decision_ids": ["<open IDs in queue order>"],
    "unknown_ids": ["<unknown field IDs in snapshot order>"],
    "findings": [{"summary": "<material finding>", "source_ids": ["SRC-###"]}]
  }
  ```

- `.project-organizer/evidence/dependency_planner.json`

  ```json
  {
    "role": "dependency_planner",
    "verdict": "PASS",
    "source_fingerprint": "<64 lowercase hex>",
    "tools_used": ["get_ready_work", "get_dependency_path"],
    "ready_ids": ["<ready IDs in tool order>"],
    "launch_path_ids": ["<longest declared path IDs in tool order>"],
    "blocked_ids": ["<blocked IDs on that path>"],
    "findings": [{"summary": "<material finding>", "source_ids": ["SRC-###"]}]
  }
  ```

Both workers return `HOLD` rather than filling a missing fact or reconciling
conflicting tool results. Each returns one to four source-cited findings.

After the candidate state and board exist, run the reviewer and save its exact
JSON-only return as `.project-organizer/evidence/board_reviewer.json`:

```json
{
  "role": "board_reviewer",
  "review": "REVIEW: PASS",
  "source_fingerprint": "<state fingerprint>",
  "state_sha256": "<exact state file hash>",
  "board_sha256": "<exact board file hash>",
  "checked_sections": ["outcome", "now_next", "ready_work", "launch_path", "blocked_work", "decision_queue", "unknowns", "source_coverage", "worker_reconciliation"],
  "findings": [{"severity": "note", "summary": "<finding>", "source_ids": ["SRC-###"]}]
}
```

`REVIEW: PASS` has no blocker. `REVIEW: HOLD` has at least one blocker and the
smallest concrete repair. Do not rerender after review: its hashes deliberately
bind the exact candidate. The state and pending receipt bind both worker report
hashes. The final receipt also binds the reviewer report hash, including when a
valid `REVIEW: HOLD` prevents release.

## Required release files

- `PROJECT_STATE.json` — structured facts behind the candidate board
- `PROJECT_BOARD.html` — large, visual, locally viewable candidate board
- `RUN_RECEIPT.json` — `PENDING`, `PASS`, or `HOLD`, with hashes that bind it
  to the other two files

The renderer writes each file through a temporary file and atomically replaces
that file's destination. It replaces the state and board first, then writes the
receipt last using the same per-file method. The three-file release set is not
one atomic transaction. The renderer marks the state and board `CANDIDATE` and
the receipt `PENDING`; neither is a release claim. `RUN_RECEIPT.json` is the
only release decision. The board embeds the exact state SHA-256, and the
reviewer binds both candidate hashes.

The automatic `Stop` hook stays inert until the trio exists. It checks schema,
full source-to-ledger parity, the current worker reports, an exact byte match
between the board and the trusted deterministic render of its state, the
offline/no-script boundary, and a current `REVIEW: PASS`. It then writes a
receipt with board `RELEASE` and gate `PASS`, or requests one bounded repair.
It must not loop, increment repairs above one, or issue a second block even if
a later event resets `stop_hook_active`.

Invoking
`py -3 plugins\project-organizer\hooks\release_gate.py --check` runs the
learner source-package copy for diagnosis or testing only. Even when it passes,
it cannot prove the installed Stop hook is current and cannot be used to claim
release. It is strictly non-mutating: it never creates or modifies the receipt,
state, board, evidence reports, or repair count. A plugin-code repair still
requires package validation, plugin reinstall, Codex restart, `/hooks` review
and trust approval, and then the normal installed Stop run, which alone writes
the authoritative receipt. The diagnostic command returns a normal process
failure when its source-package checks do not pass.

Exact render parity creates a deliberate trust boundary. If the focused repair
changes plugin code, validate the revised package, then have the learner use
the Plugins screen to uninstall/install it again, or run:

```text
codex plugin remove project-organizer@ai-harness-bootcamp
codex plugin add project-organizer@ai-harness-bootcamp
```

Restart Codex, inspect `/hooks`, and approve the reviewed hook before rerunning
the workers, renderer, and reviewer. The local marketplace does not need to be
added again. A source-data or generated-artifact repair does not require this
reinstall branch.

The production response reports the candidate, reviewer result, and artifact
paths only. It explains that the Stop hook updates the receipt after the
response. A human or later turn inspects `RUN_RECEIPT.json`; the same turn must
not claim it observed its own post-response Stop result.

## Useful board

The board must visibly answer:

1. What outcome are we driving?
2. What is happening now?
3. What should happen next?
4. What is the longest declared launch path?
5. What is blocked, and why?
6. Who owns each open decision, and when is it needed?
7. What is the next concrete commitment?
8. Which consequential fact or owner remains unknown in the supplied record?

Call the sequence a **longest declared launch path**, not a calculated critical
path. The packet supplies predecessor relationships but no duration estimates,
so CPM would overstate what the evidence supports.

The board must visibly label **Ready now** and **Source coverage**, show a
generated-at time, and keep source IDs beside material claims.
