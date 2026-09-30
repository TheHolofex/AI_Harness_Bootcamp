# Module 04 — Diagnose and recover

**Serves oracle:** S04, S14, S15, S19, S22  
**Primary objective:** PO-04 — Diagnose and recover  
**Prerequisites:** Preflighted accessible environment, this module's supplied ledger and hashed baseline renderer, and a verified restore path  
**Consumes:** VERIFY:PREFLIGHT; VERIFY:CASE; VERIFY:RESTORE_PATH; CUSTODY:HIDDEN_FAULT_ENV  
**Produces:** LOCALIZATION_RESULT; RECOVERY_RESULT; PO04_RESULT  
**Facilitated time:** 3 hours  
**Practice time:** 2 hours  
**Performance stage:** Adversarial  
**Work surface:** Unfamiliar faulty harness (work-copy renderer after prepare)  
**Practical work:** Verify restore before fault exposure using explicit ledger input, diagnose one material hidden fault in a harness the learner did not build, seal first divergence with a read-only probe before repair, make one authorized reversible correction from the hashed baseline, and repeat the original conditions cleanly with focused, end-to-end, and fresh-process runs from an external work root.  
**Performance evidence:** Preserved symptom and hashes, boundary path, discriminating probe output, independent protected grade of the sealed LOCALIZATION_RESULT, correction record, focused/end-to-end/fresh-process reruns, clean-condition RECOVERY_RESULT, and restore verification on disposable roots.  
**Failure / HOLD:** Stop for a disputed oracle, failed restore verification, unknown external effect, exhausted three-attempt ceiling, failed revert, missing authority, or fatigue signal. Localization-only records `HOLD`, not recovery completion.  
**Scope boundary:** Proves one bounded diagnosis-and-recovery performance on the supplied fault; it does not establish mastery across fault classes, and repair outside learner authority is not required.  
**Handoff:** Give the next owner the sealed first divergence, the probe that discriminated it, the change made and its reversal path, and the clean-condition result.
**Case family:** [CASE_FAMILY.md](../../CASE_FAMILY.md). The adapter supplies a self-contained case in that family. This module’s gate does not consume another module’s product.

## Why

Random editing destroys attribution. A reliable operator preserves the evidence, proves the earliest unsupported boundary, and changes the owning surface only after an observation that could have come out the other way. Restore is verified before it is relied on, never inherited on trust. The harness must process 80 rows with near misses, broken handoffs, hostile text, time/supersession traps, and condition-word collisions.

## Enabling objectives

1. Write expected input, output, proof, and falsifier across the observable boundaries using an explicit ledger path.
2. Use a discriminating read-only probe before editing, and keep localization separate from repair.
3. Prove an authorized correction or verified revert with focused, end-to-end, and fresh-process evidence from the external work root.

## Gate

Localization earns bounded evidence on its own. PO-04 passes only when protected grading confirms the named first divergence, the probe materially discriminated, one-change and revert discipline held, and the original condition passes focused, end-to-end, and fresh-process reruns after verified restore. Correct localization with repair belonging to another owner is credited as localization and held for recovery.

## Supplied-case domain (adapter)

Hidden fault drops one thread-step field (permit status or gate time) from a rendered duty card. Fault lives in a work-copy renderer placed after restore is proved. The ledger contains 80 rows (BK-200–BK-279) for Basin Depot to Clinic F-9 on CS-2 with the required traps. The probe distinguishes source omission, wrong input version, and renderer omission.
