# Module 06 — Operate a fixed workflow through change

**Serves oracle:** S04, S08, S13, S14, S17, S19  
**Primary objective:** PO-06 — Operate one fixed workflow  
**Prerequisites:** Preflighted accessible environment, this module's supplied batch workload, and supplied saved-workflow controls  
**Consumes:** VERIFY:PREFLIGHT; VERIFY:CASE; VERIFY:BATCH_WORKLOAD; VERIFY:SAVED_WORKFLOW  
**Produces:** FIXED_BASELINE; EXCEPTION_RULE; DETERMINISTIC_DELTA; CONFIG_ID; RESTORE_ACTION; PO06_RESULT  
**Facilitated time:** 3 hours  
**Practice time:** 2 hours  
**Performance stage:** Adversarial  
**Work surface:** Structured-data/batch work  
**Practical work:** Confirm the supplied batch workload, its input identities, and the saved-workflow controls; configure and run one saved fixed workflow on a baseline and a second wave; change one rule in one place; and prove the exact deterministic outer-state effects without hand patching.  
**Performance evidence:** Independent protected results, FIXED_BASELINE, EXCEPTION_RULE branch map, terminal receipts, one-rule diff, DETERMINISTIC_DELTA against route/status/field predictions, unaffected-record proof, probabilistic-output dispositions, zero manual-repair count, CONFIG_ID, and RESTORE_ACTION result.  
**Failure / HOLD:** Stop for a missing supplied workload or workflow controls, invalid contract, gate tampering, unexpected deterministic route/status/field change, material stochastic output with no rule declared before the run, manual record patch, incomplete terminal state, or failed restore.  
**Scope boundary:** The exact delta covers deterministic outer state, not unqualified generated wording. Persistent state, adaptive flow, multi-agent work, and deployment remain advanced.  
**Handoff:** Give the next owner the saved path and its configuration identity, the rule that changed and its proven blast radius, the exception routes, and the restore action.
**Case family:** [CASE_FAMILY.md](../../CASE_FAMILY.md). The adapter supplies a self-contained case in that family. This module’s gate does not consume another module’s product.


## Why

A fixed path makes repeated work inspectable, and it is the last rung most professional work actually needs. Exactness is defensible for routes, statuses, policy versions, receipts, and controlled fields — not for a single stochastic generation.

## Enabling objectives

1. Define saved steps, structured handoffs, validation, exceptions, terminal states, stop, and restore in supplied controls.
2. Predict and prove one-rule changes to deterministic outer state, and prove unaffected records stayed unchanged.
3. Route material probabilistic output through a rule declared before the run, or `HOLD`.

## Gate

Pass PO-06 when baseline and second wave use the same saved path, every lot reaches a terminal receipt (READY / OPEN / NOT_AUTHORIZED / RESOURCE_CONFLICT), the two baseline receipts are byte-identical, exactly the lots carrying PENDING under the changed line move to reject/NOT_AUTHORIZED while rack lots and all other rows stay byte-identical to baseline, the stretch membership delta is isolated from the policy effect, material note text never overrides the rule, the manual repair count is zero, and `restore_rule.py <workdir>` produces RESTORE OK plus byte match to the pre-change baseline receipt.

## Supplied-case domain (adapter)

80 lots `LW-01`–`LW-80`. Input columns: lot,permit,gate_window,input_disposition,resource_exception. `input_disposition` and gate text are provenance only. CANCELLED rows carry permit WITHDRAWN. One saved workflow (`route.py <input.csv> <out.csv>`). One config line `pending_status: OPEN|NOT_AUTHORIZED` in the adjacent RULE.md. RACK_CONFLICT evaluated first to hold,RESOURCE_CONFLICT. Baseline and second wave share identical permit and exception values so receipts are byte-identical. Exactly the PENDING rows move when the line changes. Restore takes the workdir, checks distinct baseline + matching digest, overwrites only the active rule, prints RESTORE OK only on byte equality. Stretch revision changes which rows meet the PENDING predicate; predict the delta, run the same saved path, prove the membership change.
