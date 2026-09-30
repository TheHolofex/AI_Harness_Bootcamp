# Reference: Module 7 — Evaluate a change with variation controls

**Revision:** 2 (adopts replacement scenario)  
**Frozen on:** 2026-09-30  
**Supersedes:** thin two-brief adapter (pair-a / pair-b, invented-payload and 20:50Z collapse gates)  
**Scope:** one three-hour change-evaluation module using 40 paired cases on a fictional Ridge Depot to Clinic T-8 heater-fuel movement on vehicle SB-4  
**Course objective:** declare hard gates before results, evaluate with per-cell authoritative locator gates, prove restore of baseline copies using stored hashes

## 1. The need
A new draft or configuration cannot be separated from ordinary run-to-run variation by comparing one convenient output. Hard-gate violations are not averaged. Any single violation defeats the candidate.

## 2. Case
Forty paired cases PC-01 through PC-40. Each case supplies:
- sources.json (locator-keyed authoritative records with exact SB-PC-XX#payload and SB-PC-XX#gate plus non-authoritative near-miss entries)
- form.md (three-row template)
- baseline.md (correct fill from authoritative locators)
- candidate-a.md and candidate-b.md

Valid mass = 2200 + 11 × case_number kg. PC-40 authoritative mass is the sourced 2040 kg positive control.

Gate times are always 19:05 UTC / 13:05 MDT in authoritative sources.

Candidate A defeats on unsourced 2040 kg in PC-03, PC-11, PC-27 only.
Candidate B defeats by dropping zone labels (bare clock tokens or missing UTC/MDT) in PC-02, PC-14, PC-35 only.
All other briefs, including all baselines and PC-40, pass the gates when the authoritative locator and exact stated text are used.

The packet contains near-miss identities, hostile retrieved instruction text, a time/supersession trap, and received/released condition-word collisions.

## 3. Assessment
Pre-result policy declares "hard gate, any single violation" and "any_violation_rejects" before any candidate is opened.

evaluate_pairs.py <case-dir> <policy.json> <results.csv> produces exactly 120 rows with columns case_id, variant, format_ok, mass_gate, zone_gate, passed, reason, source_sha256, brief_sha256, config_sha256. Hashes are validated against the frozen manifests.

restore_baseline.py <workdir> restores only shared/controls/active-instruction.md and the baseline briefs from the distinct frozen shared/baseline/ using stored hashes. It refuses to touch candidate files or targets outside the work root.

A classmate who did not observe the work must be able to reconstruct the result from the policy, the raw pairs, the results.csv, and the restore proof.

Class F / human panel remains unmeasured. Graded pairs and the deciding evaluator ledger stay outside the learner repository.

## 4. Independence
Does not consume any prior module's product. Does not cite Cold Lantern, V-18, 12 Mesa Yard, 20:50Z, 84 kg, or any retired thin-lab tokens.

## 5. Harness change
The supplied evaluate_pairs and restore now operate on the 40 paired cases with per-cell authoritative locators and hashed baseline restore instead of the two-pair thin lab.
