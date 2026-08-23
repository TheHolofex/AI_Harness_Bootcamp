# Standard Gauntlet Measurements

Original Gauntlet date: 2026-08-09  
Current-state reconciliation: 2026-08-12

## Measurement status

This file separates historical Gauntlet runs from current skeleton measurements. Historical output files remain immutable evidence of the ten-module implementation that existed when those commands ran. They are not descriptions of the current nine-module skeleton.

## Historical test sequence — superseded implementation

| Run | Static passes | Failures | Manual procedures | Evidence |
|---|---:|---:|---:|---|
| Pre-implementation RED | 189 | 66 | 12 | `standard-oracle-red.txt` |
| GREEN attempt 1 | 319 | 5 | 12 | `standard-oracle-green-attempt-1.txt` |
| Initial GREEN | 324 | 0 | 12 | `standard-oracle-green.txt` |
| Post prerequisite-seam correction | 350 | 0 | 12 | `standard-oracle-post-seam.txt` |
| Product-regression extension | 376 | 0 | 12 | `standard-oracle-product-regression.txt` |
| Post-parsimony final | 376 | 0 | 12 | `standard-oracle-post-parsimony.txt` |

Those results explain the design history. They targeted the earlier chained ten-module structure.

## Frozen Reference

- SHA-256: `419a41a094673ac7cdc775b03c643ff8d8f6e50a680dc11ed8dea019713d0fc1`
- The current hash still matches `reference-sha256.txt`.
- Field survey: 17 official exemplars/frameworks.
- Source-access log: 16 direct HTTP 200 responses; one DeepLearning.AI URL returned a permanent redirect and was separately retrieved.
- The frozen bounds remain compatible with the current core: at most 10 modules and 24–35 facilitated hours.

## Current core structure — 2026-08-12

| Measure | Result | Method |
|---|---:|---|
| Authoritative Markdown files | 13 | README, map, objectives, guide, and nine modules |
| Authoritative Markdown lines | 614 | Line count over current `reformation/**/*.md` |
| Modules | 9 | Count `modules/core/*.md` |
| Module IDs | 00–08 | Filename/manifest scan |
| Module lines | 270 | Sum module line counts |
| Largest module | 30 lines | Maximum module line count |
| Facilitated design time | 27 hours | Nine manifests × 3 hours |
| Practice design time | 18 hours | Nine manifests × 2 hours; included in facilitated time |
| Practice ratio | 66.7% | 18 / 27 |
| Produced product tokens | 39 | Parse current `Produces` fields |
| Learner-visible supply edges | 30 | Parse current `VERIFY:` inputs |
| Evaluator-custody edges | 3 | Parse current `CUSTODY:` inputs |
| Cross-module consumed products | 0 | Independent-module invariant |
| Broken relative links | 0 | Active Standard oracle |
| Static oracle | 413 PASS / 0 FAIL / 12 MANUAL | `test_core_standard.py` current run |

## Current structural interpretation

- Every module receives its own preflighted supplied case.
- No module consumes another module's evidence.
- A missed or held module does not cascade into the next session.
- Final qualification still requires all nine program outcomes.
- Reassessment uses an unseen protected case at the original gate.
- Independent-recipient sessions and makeups are outside the 27 facilitated hours.

## Current manual procedures

The active oracle reports 12 manual procedures. They are not PASS until performed against the current nine-module structure:

1. primary-source research review;
2. outcome observability and ownership review;
3. responsibility-before-release review;
4. composed responsible-use review;
5. refusal-versus-mandatory-operation review;
6. learner-action scope classification;
7. independent-module first-action sufficiency review;
8. stochastic evaluation review;
9. composed untrusted-content/tool-authority execution;
10. independent-recipient transfer execution;
11. degraded and 20/200-learner policy trace;
12. empirical budget review.

Prior semantic reviews informed the redesign but do not automatically validate the later nine-module consolidation.

## Empirical status

The following remain **unmeasured**:

- first checked artifact within 60 minutes;
- completion in 27 facilitated hours;
- 18 hours of actual practice;
- ≤US$40 model/tool spend per learner;
- median ≤15 and p90 ≤25 minutes human scoring per gate;
- ≥90% exact hard-gate agreement;
- weighted κ ≥0.70 ordinal-rubric agreement;
- composed untrusted-content/tool-authority containment;
- protected-check tamper resistance;
- accessible same-state operation;
- clean-session and independent-person transfer;
- recipient recruitment and scheduling;
- reassessment/make-up duration and fixture rotation;
- 20-learner or 200-learner capacity, custody, moderation, and appeals.

No measured performance claim is inferred from the schedule arithmetic or static oracle.

## Parsimony history

- The active Scout oracle was removed because it targeted a superseded Reference.
- The current active oracle is `reformation/tests/test_core_standard.py`.
- Historical Standard output logs remain preserved and labeled historical.
- No current authoritative course file falls outside README, map, objectives, guide, or the nine module skeletons.
