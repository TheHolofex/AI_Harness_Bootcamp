# Reference: Module 4 — Diagnose and recover

**Frozen on:** 2026-09-30 (revision 2)  
**Scope:** one three-hour diagnose-and-recover module built around an 80-row ledger for the Copper Span movement  
**Course objective:** localize a hidden field drop in a work-copy renderer, prove restore first from a hashed baseline, and recover with three distinct runs on disposable external roots

## 1. The need

Random editing destroys attribution. Restore that is not run is not restore. A missing review field that is patched by typing the value back in hides the owning surface. The harness must actually process the pile of 80 rows including near misses, three true-but-broken handoffs, hostile text, time/supersession trap, and condition-word collision.

**Done:** the learner prepares a work root with prepare_work, verifies restore from the hashed baseline, seals the first missing field using a read-only probe after a public fault placement, replaces only the work-copy renderer, and produces focused, end-to-end, and fresh-process reruns that all emit the required fields.

## 2. Better framing

The module is not a hunt through staff folders. The hidden drop lives in a work-copy renderer placed after restore is proved. The learner-facing scripts/render_review.py and the place_practice_fault.py are public and inspectable. Graded cases stay outside.

## 3. Authority

Repository authority: `reformation/modules/core/04-diagnose-recover.md`, `reformation/LEARNING_OBJECTIVES.md`, `reformation/AUTHORING_GUIDE.md`, and the Copper Span section of `reformation/MISSION_THREAD_SCENARIOS.md`.

## 4. Case boundary

80 ledger rows `BK-200`–`BK-279` for vehicle resupply of IV fluid cases from Basin Depot to Clinic F-9 on vehicle `CS-2`. The renderer takes an explicit `ledger.json` and `review.md` path. Not Module 1 answers. Not a movement order.

The learner does not write a new renderer, open staff folders, or release work outside the class. The work root is disposable and must support paths with spaces and unrelated cwd.

## 5. Protected answer model (revision 2)

- Clean renderer (explicit ledger input) emits both `permit_status` and `gate_time_mdt` plus current/near-miss metadata.
- A public place_practice_fault.py --variant A drops `permit_status`; --variant B drops `gate_time_mdt`.
- Restore.py <workdir> makes the work copy identical to the baseline after digest match, prints RESTORE OK, and preserves prior failed renderer + out/ in attempts/ before the sole replacement.
- Probe distinguishes renderer_omission, source_omission, and wrong_input_version.
- Three recovery proofs: focused (work copy), end-to-end (explicit), fresh-process (unrelated cwd).

## 6. Workflow (revision 2)

1. Prepare W with prepare_work.py 04 <dest>.
2. Clean render from W using explicit ledger.json.
3. Verify restore.py . first.
4. Facilitator places fault with source place_practice_fault.py --variant A|B.
5. Run faulty render, run probe, seal first miss.
6. One authorized restore.py .
7. Three named recovery outputs (focused, end-to-end, fresh-process).
8. Handoff.

## 7. Assessment

Hard gates are in `assessment/PUBLIC_RUBRIC.md`. Class F / human panel remains unmeasured.

## 8. Absolute failures

Do not tell learners to open a staff path. Do not claim a human panel that did not sit. Do not report timing without measurement. Do not leave old repo-relative implicit card lookups or shell restore callers.

## Revision 2 contract change

## Revision 3 contract change (2026-09-30)

Probe now uses --review/--intended (optional), always prints selected_source_ids from render classify current + review_present + per-field cause (source_omission on current rows, wrong_input_version when --intended differs, renderer_omission vs output_absent). Source omission may HOLD render; probe diagnoses without output. Three proofs: probe check, complete render, fresh unrelated cwd process. Genuine stretch ledgers for three causes. Portable R/PY/M/W setup. 80-row and identity unchanged. Digest recomputed.


This reference supersedes the thin V-18/THREAD_CARD adapter (revision 1). The digest is recomputed on this file as the contract change record. The 80-row ledger, explicit CLI, Python restore with baseline+sha256+attempts preservation, public place and probe, and three-proof requirement are now the ground truth.
