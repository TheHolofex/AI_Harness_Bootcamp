---
name: daily-brief-release
description: Regenerate and release the P1 daily status brief from the declared C-number source set. Use when the user asks for the daily brief, a refreshed status brief, or a release-ready P1 update. Do not use for unrelated summaries, one-off notes, or work without the P1 source manifest.
---

# Daily brief release

1. Read `HARNESS_PROFILE.md`, `P2_CONTROL_PLANE.json`, and
   `inputs/p1/SOURCE_MANIFEST.md`. Stop if a required source is missing or the
   source declaration is inconsistent.
2. Use only the declared files under `inputs/p1/`. Preserve each source's
   uncertainty and map factual claims to C-number tags.
3. Ask the `evidence_scout` subagent for a read-only evidence map if
   `out/EVIDENCE_MAP.md` is missing or stale. The main agent writes the file.
4. Draft Shipped, Broken, Blocked, and Asks for the reader named in
   `HARNESS_PROFILE.md`. Keep the product decision-dense and within the line
   limit in `P2_CONTROL_PLANE.json`.
5. Save the candidate to `out/FINAL_DAILY_BRIEF.md`.
6. Stop at the candidate when the operator requests the candidate phase. In a
   separate parent turn set to `Read only`, ask the `decision_reviewer` to check
   the saved candidate, wait for its result, and close the completed thread.
7. In a later main-writer turn, save the exact review to
   `out/DECISION_REVIEW.md` and make only the smallest supported repair set.
8. Record observed time, turns, subagent runs, approvals, and repairs in
   `out/RUN_RECEIPT.md`. If usage or cost is not visible, write `not exposed`;
   never estimate it from memory.
9. Keep the contract disabled until the candidate, review, evidence, and run
   receipt exist. Enable it as the final configuration change before the
   release turn stops. The `Stop` quality gate then makes the deterministic
   check. PASS permits release. FAIL means HOLD and allows at most one focused
   repair; never weaken the contract to make the receipt green.
