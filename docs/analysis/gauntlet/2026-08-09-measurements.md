# Gauntlet Measurements — Reformation Core

Date: 2026-08-09

## Static oracle

| Run | Result | Evidence |
|---|---|---|
| Pre-implementation RED | 22 static passes, 40 failures, 8 manual procedures | `2026-08-09-core-oracle-red.txt` |
| First GREEN attempt | 238 passes, 3 wording-sensitive failures, 8 manual procedures | `2026-08-09-core-oracle-green-attempt-1.txt` |
| Final GREEN | 241 static passes, 0 failures, 8 manual procedures | `2026-08-09-core-oracle-green.txt` |
| Post-parsimony regression | 241 static passes, 0 failures, 8 manual procedures | `2026-08-09-core-oracle-post-parsimony.txt` |

The Reference SHA-256 remained `956b3831ef242e4b33c63f79683a6a6e7c2a05e4a357e61196d21e28a5abd360` across GREEN and post-parsimony runs.

## Skeleton size and budgets

| Measure | Result | Method |
|---|---:|---|
| Authoritative core Markdown files | 14 | Count README, map, objectives, guide, and ten module skeletons |
| Authoritative core Markdown lines | 689 | `wc -l` equivalent over those 14 files |
| Module count | 10 | Count `modules/core/*.md` |
| Total module lines | 344 | Line count over module skeletons |
| Largest module | 38 lines | Maximum module line count |
| Facilitated time | 30 hours | Sum module manifest fields |
| Practice time | 20 hours | Sum module manifest fields |
| Practice ratio | 66.7% | 20 ÷ 30 |
| First-use target | ≤60 minutes | Declared Module 00 gate; not pilot-measured |
| Variable spend target | ≤US$40/learner | Declared implementation budget; not pilot-measured |
| Human scoring target | ≤15 min/learner/module | Declared implementation budget; not pilot-measured |

## Parsimony deletion pass

Removed 30 superseded files totaling 7,502 lines from `reformation`:

- 13 legacy core lesson bodies;
- 3 advanced-extension bodies;
- 9 templates;
- 5 standalone reference/record documents.

Candidate list and exact line counts: `2026-08-09-parsimony-removal-candidates.txt`.

Reason: these artifacts did not serve the frozen authoritative core skeleton oracle and would leave competing prerequisite, evidence, and complexity systems beside the new core. Detailed lesson and adapter material must be rebuilt from the bounded skeleton instead of silently inherited.

## Human judges

| Judge | Result | Evidence |
|---|---|---|
| Curriculum and responsible-use judge | O03 2/2; O06 2/2; O09 2/2 | Delegate task `20260809_14` |
| Scope judge | 10/10 across audience and builder boundary | Delegate task `20260809_15` |
| Scale/degradation judge | Policy preservation 2/2; declared spend and scoring feasibility 1/2 | Delegate task `20260809_16` |

O14 recipient performance cannot be executed against a skeleton without an adapter, package, protected task set, and real recipient. Its check procedure is specified; implementation evidence is unavailable and is scored PARTIAL in the verdict.
