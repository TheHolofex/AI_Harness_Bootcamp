# Module 7 public scoring rubric

The standard below does not change when case identifiers change.

Every hard gate must pass on a cell-by-cell basis. A strong summary cannot average away a single violation. The evaluator must account for all 120 rows.

| Hard gate | Passing evidence | `HOLD` examples |
|-----------|------------------|-----------------|
| Policy first | `hard gate, any single violation` and `any_violation_rejects` declared before any candidate result is opened | Policy rewritten after a result appears |
| Baselines pass | All 40 baseline briefs exit 0 under hard_gates.py | Any baseline contains an unsourced mass or a bare clock token |
| Candidate evidence | Every mass and time claim is checked against its authoritative source locator, with the actual violated gate recorded | A plausible-looking value is accepted without source support, or an unsupported value is averaged away |
| Evaluation | `evaluate_pairs.py` accounts for all 120 rows with matching source, brief, and configuration hashes; each result agrees with the inspected evidence | Missing or duplicate rows, mismatched hashes, or a gate result that contradicts its source |
| Cost proxy | Count of gate failures (0 or 1 per pair) recorded separately from any quality claim | Averaged score or model-quality language used as the decision |
| Restore | restore_baseline.py prints RESTORE OK; restored baselines pass their gates again; no candidate file is created or overwritten | Restore fails or a restored baseline now fails its gate |
| Handoff | Another reader can reconstruct the exact policy, every failing row and its reason, the cost-proxy count, and the restore evidence | Reconstruction requires the author to explain missing facts |

## Visible practice check
The visible commands can prepare a work copy, declare the policy, run hard_gates on any brief with its adjacent sources.json, run evaluate_pairs on the full case directory, and run restore_baseline. They cannot decide whether the policy was declared honestly before results.

## Graded attempt
The evaluator selects unseen pairs or holds the deciding gates outside the visible corpus. A missing or compromised graded artifact produces `HOLD`.
