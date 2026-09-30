# Module 05 — Improve from observed failures

**Serves oracle:** S04, S12, S14, S16, S19  
**Primary objective:** PO-05 — Improve from observed failures  
**Prerequisites:** Preflighted accessible environment, this module's supplied run corpus, and a supplied deterministic control  
**Consumes:** VERIFY:PREFLIGHT; VERIFY:CASE; VERIFY:RUN_SAMPLE; VERIFY:DETERMINISTIC_CONTROL  
**Produces:** SAMPLE_MANIFEST; PREDICATE_SPEC; DETERMINISTIC_CONTROL_RESULT; PO05_RESULT  
**Facilitated time:** 3 hours  
**Practice time:** 2 hours  
**Performance stage:** Adversarial  
**Work surface:** Observed-run corpus  
**Practical work:** Confirm the supplied run sample and deterministic control, freeze an outcome-blind sample of 8–20 runs, record first material failures before categories, reconcile counts, infer two literal strings, and configure and validate them through the documented config interface.  
**Performance evidence:** SAMPLE_MANIFEST, raw first-failure notes, category revision and reconciled counts, PREDICATE_SPEC naming exact input/pass/fail/missing and malformed-config behavior, independent DETERMINISTIC_CONTROL_RESULT on known-bad, known-good, and missing input using the --config flag, and a bounded improvement decision.  
**Failure / HOLD:** Hold when fewer than eight interpretable runs exist, the supplied control is missing, acceptance cannot be applied, the sample was chosen by outcome, the selected failure is an arbitrary semantic condition outside supplied controls, or validation fails.  
**Scope boundary:** Describes the sampled workload only; it does not estimate universal failure rates. The learner specifies and configures. Public controls and labels are inspectable practice; any unseen qualification selection requires external evaluator custody.  
**Handoff:** Give the next owner the sample rule and its limits, the predicate and its input contract, the validated control, and the improvement decision.
**Case family:** [CASE_FAMILY.md](../../CASE_FAMILY.md). The adapter supplies a self-contained case in that family. This module’s gate does not consume another module’s product.


## Why

Memorable failures are a poor automation agenda. Reading actual runs, with first-failure discipline held before interpretation, is what turns experience into a check — and not every semantic defect can or should become a deterministic rule.

## Enabling objectives

1. Freeze 8–20 eligible runs and preserve passes, failures, retries, and dependence.
2. Write first-failure notes before deriving and revising binary categories.
3. Specify a mechanically decidable predicate and configure it in a supplied deterministic control.

## Gate

Pass PO-05 when the sample rule predates outcome inspection, notes predate categories, original and revised labels stay visible, counts reconcile to the sample, PREDICATE_SPEC names exact behavior (including two-literal config and error states), and the supplied control independently matches known bad, passes known good, and holds on missing input. If new implementation is needed, record the adapter dependency and `HOLD`; learner implementation credit is not awarded.

## Supplied-case domain (adapter)

Synthetic corpus of thread-verification runs (80 runs). Sample of 16 (within 8–20 band). First failures include receipt-as-release promotion cases. One mechanically decidable predicate configured as two case-sensitive substring literals under `all_present`. The control exits 1 on match and 0 otherwise. `UNRELEASED` containing `RELEASED` is a documented limit of the text check.
