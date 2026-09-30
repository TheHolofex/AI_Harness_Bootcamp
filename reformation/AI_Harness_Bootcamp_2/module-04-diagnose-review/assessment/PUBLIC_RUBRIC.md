# Module 4 public scoring rubric

The standard below does not change when identifiers or times change.

Every hard gate must pass. A strong summary cannot compensate for an unproved restore or a repair made before the miss was sealed.

| Hard gate | Passing evidence | HOLD examples |
|---|---|---|
| Restore first | RESTORE OK before any swap | Diagnose on an unproved path |
| Clean render | Clean renderer (explicit ledger) emits permit_status and gate_time_mdt | Clean run already missing a field |
| Sealed first miss | Probe shows exactly one earliest omission; sealed before replace | Field guessed after the replace |
| One authorized replace | Restore from the baseline; no hand edit of the dropped field | Second change; typed-in field |
| Three reruns | Focused, end-to-end, and fresh-process all show both fields | One rerun only |
| Handoff | Another person can reconstruct the result without coaching | Depends on memory or chat history |

## Visible practice check

The visible commands can inspect:

- required files and 80-row ledger;
- both fields in a clean render with explicit ledger;
- a dropped field after public place_practice_fault --variant A or B;
- RESTORE OK when the two renderer files match after digest;
- probe output naming the omission cause.

They cannot decide whether the sealed miss was written before the replace.

## Graded attempt

The evaluator selects an unseen ledger snapshot and holds the prepared work copy. The producing AI cannot inspect or alter that copy. A missing, inaccessible, exposed, or compromised graded ledger produces HOLD and a new case—not a simulated pass.
