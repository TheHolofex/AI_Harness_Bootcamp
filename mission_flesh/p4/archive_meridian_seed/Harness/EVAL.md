# Evaluator Record

Bind exact checker/evaluator receipts. Never overwrite a first receipt after repair.

- Evaluator context: FRESH
- Access: READ_ONLY
- Default: FAIL
- Generator first-pass verdict: [REPLACE: READY only if every row below was claimed READY; otherwise NOT READY]
- Candidate verifier first-pass verdict: [REPLACE: PASS or HOLD from CANDIDATE_CHECK_FIRST.txt]
- Candidate verifier first-pass finding: [REPLACE: exact HOLD text or NONE]
- Fresh evaluator first-pass verdict: [REPLACE: PASS or HOLD from DIRECTOR_EVALUATOR_FIRST.json]
- First-pass criteria claimed ready: [REPLACE: count of READY rows]
- First-pass evaluator HOLD criteria: [REPLACE: count of all evaluator HOLD rows, including generator NOT READY rows]
- First-pass overclaim criteria: [REPLACE: count of evaluator HOLD rows whose generator claim was READY]
- Overclaim: [REPLACE: overclaim count/READY count]
- Repair cycles used: [REPLACE: 0 or 1 shared by candidate and evaluator]
- Repair scope: [REPLACE: NONE, CONTENT, or CONTROL_ONLY]
- Repair justification: [REPLACE: NONE for zero repairs; otherwise preserve every exact first blocker finding]
- Final candidate verifier verdict: [REPLACE: PASS]
- Final evaluator verdict: [REPLACE: PASS]
- Verdict: [REPLACE: PASS or HOLD]
- First candidate receipt: Harness/CANDIDATE_CHECK_FIRST.txt
- First candidate SHA-256: [REPLACE: exact receipt SHA-256]
- Final candidate receipt: [REPLACE: first receipt when no repair, otherwise Harness/CANDIDATE_CHECK_FINAL.txt]
- Final candidate SHA-256: [REPLACE: exact final candidate receipt SHA-256]
- First evaluator receipt: Harness/DIRECTOR_EVALUATOR_FIRST.json
- First evaluator SHA-256: [REPLACE: exact receipt SHA-256]
- Final evaluator receipt: [REPLACE: first receipt when it is final, otherwise Harness/DIRECTOR_EVALUATOR_FINAL.json]
- Final evaluator SHA-256: [REPLACE: exact final evaluator receipt SHA-256]

| Criterion | Generator first-pass claim | Evidence opened | Fresh evaluator first-pass verdict | Final verdict |
|---|---|---|---|---|
| Required artifacts exist | [REPLACE: READY or NOT READY] | [REPLACE: exact semicolon-separated first-receipt evidence list] | [REPLACE: PASS or HOLD] | [REPLACE: PASS or HOLD] |
| Personal rules visibly affect the output | [REPLACE: READY or NOT READY] | [REPLACE: exact semicolon-separated first-receipt evidence list] | [REPLACE: PASS or HOLD] | [REPLACE: PASS or HOLD] |
| Answer claims cite direct manifested evidence | [REPLACE: READY or NOT READY] | [REPLACE: exact semicolon-separated first-receipt evidence list] | [REPLACE: PASS or HOLD] | [REPLACE: PASS or HOLD] |
| Audit excerpts and dispositions are grounded | [REPLACE: READY or NOT READY] | [REPLACE: exact semicolon-separated first-receipt evidence list] | [REPLACE: PASS or HOLD] | [REPLACE: PASS or HOLD] |
| Retrieval is earned and inside its budget | [REPLACE: READY or NOT READY] | [REPLACE: exact semicolon-separated first-receipt evidence list] | [REPLACE: PASS or HOLD] | [REPLACE: PASS or HOLD] |
| Normalized notes retain lineage and graph reachability | [REPLACE: READY or NOT READY] | [REPLACE: exact semicolon-separated first-receipt evidence list] | [REPLACE: PASS or HOLD] | [REPLACE: PASS or HOLD] |
| Morning Brief uses audited support only | [REPLACE: READY or NOT READY] | [REPLACE: exact semicolon-separated first-receipt evidence list] | [REPLACE: PASS or HOLD] | [REPLACE: PASS or HOLD] |
| Resume, state, and trace agree | [REPLACE: READY or NOT READY] | [REPLACE: exact semicolon-separated first-receipt evidence list] | [REPLACE: PASS or HOLD] | [REPLACE: PASS or HOLD] |
