# Module 07 — Evaluate a change with variation controls

**Serves oracle:** S04, S14, S17, S19, S25  
**Primary objective:** PO-07 — Evaluate a change with variation controls  
**Prerequisites:** Preflighted accessible environment, this module's supplied baseline configuration, and a supplied candidate  
**Consumes:** VERIFY:PREFLIGHT; VERIFY:CASE; VERIFY:BASELINE_CONFIG; VERIFY:CANDIDATE  
**Produces:** PRE_RESULT_POLICY; CHANGE_DECISION; COST_PROXY; RESTORED_BASELINE; PO07_RESULT  
**Facilitated time:** 3 hours  
**Practice time:** 2 hours  
**Performance stage:** Adversarial  
**Work surface:** Frozen paired cases  
**Practical work:** Confirm the supplied baseline configuration and candidate, declare the variation rule and hard gates before any result, compare the candidate against the preserved baseline on frozen paired cases, make a narrow decision, and restore the baseline.  
**Performance evidence:** Independent protected PRE_RESULT_POLICY, repeated paired controls or a justified deterministic case, raw output pairs and receipts, variation summary, hard-gate dispositions, COST_PROXY, bounded CHANGE_DECISION, and RESTORED_BASELINE control result.  
**Failure / HOLD:** Hold for rule changes made after results, a single unqualified stochastic sample, incomparable authority or opportunity, an opened case reused as confirmation, missing raw evidence, or unproved rollback.  
**Scope boundary:** Supports a decision only for the named behavior, cases, repetition rule, environment, and served configuration; it does not establish general model superiority or authorize implementation.  
**Handoff:** Give the next owner the frozen criteria, the paired evidence, the decision and its exact boundary, the rollback trigger, and the restored home state.
**Case family:** [CASE_FAMILY.md](../../CASE_FAMILY.md). The adapter supplies a self-contained case in that family. This module’s gate does not consume another module’s product.


## Why

A new model or method cannot be separated from ordinary run-to-run variation by comparing one convenient output. How repetition, aggregation, hard gates, or exclusion will be handled has to be settled before anyone sees a result, or the goalposts move by themselves.

## Enabling objectives

1. Freeze the behavior claim, eligible cases, hard gates, cost proxy, and adoption or rollback rule.
2. Declare before results a deterministic case, a repeated control count and aggregation rule, an any-single-violation gate, or exclusion of the stochastic claim.
3. Make a bounded decision and prove the baseline can be restored.

## Gate

Pass PO-07 when the variation rule predates results, repeated controls or deterministic evidence support the claim, hard-gate violations are not averaged away, raw pairs and receipts remain available, CHANGE_DECISION is no broader than its evidence, and RESTORED_BASELINE passes a control case with candidate influence removed. An opened case that informed a repair becomes diagnostic and cannot serve as confirmation.

## Supplied-case domain (adapter)

Baseline vs candidate on paired Cold Lantern-family briefs. Hard gates: no invented payload; no UTC/local collapse. Restore baseline.
