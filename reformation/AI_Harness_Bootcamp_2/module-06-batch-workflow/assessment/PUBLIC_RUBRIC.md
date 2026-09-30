# Module 6 public scoring rubric

The standard below does not change when lot identifiers change.

Every hard gate must pass. A hand-patched receipt cannot compensate for a one-rule miss.

| Hard gate | Passing evidence | `HOLD` examples |
|---|---|---|
| Same saved path | Wave 1 and wave 2 and stretch use the supplied `route.py` | Second script for wave 2 |
| Baseline receipts | Wave 1 and wave 2 baseline receipts are byte-identical | Non-key rows differ between waves |
| One-rule change | Only `RULE.md` changes; the config line is the single differing line | `route.py` edited |
| Deterministic delta | Exactly the lots that carry `PENDING` under the changed rule move to `reject,NOT_AUTHORIZED`; rack lots stay `hold,RESOURCE_CONFLICT`; all other rows byte-identical to their baseline | Another lot moves; rack lot becomes READY |
| Not READY | `PENDING` is never `READY` | A `PENDING` lot marked `READY` |
| Rack first | `RACK_CONFLICT` produces `hold,RESOURCE_CONFLICT` before any permit rule | Rack lot becomes pass or reject |
| Manual repair | No receipt is hand-edited; clean re-runs match | A CSV cell was typed or a row altered |
| Restore | `restore_rule.py <workdir>` prints `RESTORE OK`; restored receipt bytes match the original baseline receipt exactly | Rule left in the changed state; digest mismatch accepted |
| Handoff | Reconstruction without coaching | Depends on memory |

## Visible practice check

The visible commands can diff receipts against each other and against a fresh run on the same input. They cannot decide whether a probabilistic sentence would have needed a pre-declared rule.

## Graded attempt

The evaluator selects an unseen batch and holds the deciding rule line. A missing or compromised graded batch produces `HOLD`.
