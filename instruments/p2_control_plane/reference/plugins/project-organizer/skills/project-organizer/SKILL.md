---
name: project-organizer
description: Build or refresh the local P2 Project Organizer from project_ledger.sqlite3. Use when asked to organize the HarborLight project, determine ready or blocked work, map its dependency path and decisions, produce PROJECT_STATE.json and PROJECT_BOARD.html, or release those artifacts through RUN_RECEIPT.json.
---

# Project Organizer

Use the ledger and the configured `project_organizer` MCP server as the factual
surface. Never reconstruct project facts from memory.

## Run the organizer

1. Run `py -3 verify_project_ledger.py`. Stop on HOLD.
2. Confirm `/mcp` shows exactly `get_project_snapshot`, `get_ready_work`,
   `get_dependency_path`, and `get_decision_queue` under one local read-only
   server.
3. Launch `scope_mapper` and `dependency_planner` as the only two concurrent
   workers. The scope worker owns snapshot plus decision queue; the dependency
   worker owns ready work plus the `DLV-004` path. Do not duplicate those calls
   in the parent. Wait for both. Keep their roles read-only.
4. Save their exact JSON-only returns as
   `.project-organizer/evidence/scope_mapper.json` and
   `.project-organizer/evidence/dependency_planner.json`. Do not rewrite a HOLD
   to PASS.
5. Run the renderer from the project root:

   ```text
   py -3 plugins\project-organizer\scripts\render_project_board.py --project-root .
   ```

   The renderer refuses stale, malformed, overlapping, or HOLD worker reports;
   binds both report hashes into the candidate state and pending receipt; and
   writes the receipt last.
6. Launch `board_reviewer` only after the candidate board exists. Save its
   exact JSON-only return as
   `.project-organizer/evidence/board_reviewer.json`. Do not rerender after the
   review; its hashes bind to the current candidate and avoid a circular build.
   If it returns HOLD, repair the implementation or ledger build—not the source
   evidence—then rerun the workers, renderer, and reviewer. If that focused
   repair changes plugin code, first validate the revised package; have the
   learner run `codex plugin remove project-organizer@ai-harness-bootcamp`
   followed by `codex plugin add project-organizer@ai-harness-bootcamp`, restart
   Codex, inspect `/hooks`, and approve the reviewed hook. Do not silently edit
   personal plugin configuration, and do not manufacture a failure.
7. Finish the Codex turn normally. The trusted `Stop` hook validates the two
   worker reports and requires a current `REVIEW: PASS` bound to the exact
   candidate hashes.
8. In the production response, report the candidate path, reviewer result, and
   three artifact paths. Say plainly that the Stop hook updates
   `RUN_RECEIPT.json` after the response. Do not claim you observed that
   post-response result. A human or later turn confirms release only when the
   receipt has `status: PASS`, `gate_status: PASS`, and
   `board_status: RELEASE`.

`py -3 plugins\project-organizer\hooks\release_gate.py --check` executes the
learner project's source-package copy. Use it only for instructor-requested
package diagnosis or testing. It is strictly non-mutating: it never creates or
changes the receipt, release artifacts, evidence reports, or repair count. A
PASS from that command does not prove the installed trusted Stop hook is
current and must never be used to claim release. If plugin code changes,
validate the package, have the learner remove and add the plugin again, restart
Codex, inspect and approve `/hooks`, then finish the turn normally so the
installed Stop gate runs and writes the authoritative receipt.

The final receipt derives three bound agent reports and four tool reports from
the saved evidence. It records local usage as `not exposed`; never substitute
an expected number for an observation.

## Hold conditions

Hold if source hashes changed, the ledger fails integrity or foreign-key
checks, the four MCP contracts disagree with the board, a required visual
answer is missing, the reviewer finds a material decision error, or artifact
hashes do not match. An explicit source value such as `Not assigned in source`
is an honest unknown, not a placeholder failure. Return the smallest concrete
repair and keep the recorded source facts intact.
