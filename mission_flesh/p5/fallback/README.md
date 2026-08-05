# Instructor fallback P4 input (P5-owned)

Known-good sealed second brain + matching external baseline for learners whose
P4 run did not complete. Using this package is **not** completing P4.

Record in P5 evidence: `P4 input source: instructor fallback`

Contents:
- `complete_vault/` — copy of `mission_flesh/p4/reference_fixtures/complete_vault`
- `P4_BASELINE_FALLBACK.json` — path/hash baseline for that tree

Copy vault to `Documents\p4-vault` only when the learner has no sealed vault.
Copy the baseline to the course `operator/evidence/` path as
`P4_BASELINE_[TODAY].json` for the run. Do not copy it into P5 staging.
