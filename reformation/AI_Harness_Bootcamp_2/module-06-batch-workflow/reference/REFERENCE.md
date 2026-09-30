# Reference: Module 6 — Operate a fixed workflow through change

**Frozen on:** 2026-08-23 (v1)  
**Revision 2:** 2026-09-30 — adopted 80-lot replacement packet (LW-01–LW-80, two waves, rack-first, pending_status line, digest restore, stretch predicate change). Supersedes thin three-lot L-11/L-12/L-13 case.

**Scope:** one three-hour fixed-workflow module built around two fictional 80-lot waves  
**Course objective:** prove a one-rule deterministic outer-state change with exact byte delta and proven restore

## 1. The need

A fixed path makes repeated work inspectable. Exactness is defensible for routes, statuses, policy versions, receipts, and controlled fields — not for a single stochastic sentence.

**Done (v2):** baseline and changed receipts for both waves are produced by the supplied route.py; the two baseline receipts are byte-identical; exactly the lots carrying PENDING under the changed rule move while rack and others stay identical; restore_rule.py <workdir> from distinct baseline+digest prints RESTORE OK and yields byte match; stretch revision isolates input membership change from policy.

## 2. Case (replacement, revision 2)

80 lots `LW-01`–`LW-80` for Icehouse Depot to Clinic I-6.

Input columns: `lot,permit,gate_window,input_disposition,resource_exception`

- `input_disposition` (NEW/CHANGED/CANCELLED/UNCHANGED) is provenance only. CANCELLED rows carry permit `WITHDRAWN`.
- `resource_exception` empty or `RACK_CONFLICT`.
- RACK_CONFLICT evaluated first → `hold,RESOURCE_CONFLICT`.
- AUTHORIZED → `pass,READY`.
- PENDING → baseline `hold,OPEN` or changed `reject,NOT_AUTHORIZED`.
- All other supplied permit states → `hold,OPEN`.

Both waves contain the three PENDING lots LW-12/LW-28/LW-41 and the LW-19/LW-55 rack conflict. Wave 2 changes gates and dispositions for non-key lots but keeps permit and exception identical for routing identity. Thus baseline receipts are byte-identical across waves. Only the three (or stretch-set) PENDING rows move under the policy delta.

Baseline rule (in `shared/baseline/RULE.md` and initially in workflow):

```
pending_status: OPEN
```

Changed rule (edit only the active RULE.md):

```
pending_status: NOT_AUTHORIZED
```

Stretch (`wave2-revised.csv`): changes predicate membership (e.g. LW-12 becomes AUTHORIZED, LW-44 and LW-60 become PENDING). Predict the complete impact before running the same saved path.

## 3. Protected answer model

Graded batches and their deciding receipts are outside the student repository. Learners see the public rubric, the visible batch files (labeled practice), the router, and the restore. The deciding expected values for a graded attempt are never the checked-in thin `tests/expected/` files (those are historical).

The contract that must hold for any batch: exactly the PENDING rows move; rack always first; baseline receipts byte-identical; restore from distinct baseline+digest produces RESTORE OK + match; no hand patch accepted.

## 4. Assessment

Class F / human panel remains unmeasured.

## Amendments (v1 to v2)

| # | v1 (thin) | Problem | v2 (replacement) |
|---|-----------|---------|------------------|
| 1 | Three lots L-11/L-12/L-13; RULE.changed.md copy; restore without arg | Did not exercise volume floor, near-miss identities, hostile text, time trap, word collision, or rack precedence. Manual copy hid the rule. | 80 lots LW-01–80; two waves + stretch revision; one-line pending_status in RULE.md; restore_rule.py <workdir> with digest; rack first; full byte serialized comparison on disposable copies. |
| 2 | Manual-repair count file and "count is 0" | Incidental file; not consumer-visible behavior. | Removed from active contract. Repair is proven by byte match of clean re-run vs any altered receipt. |
| 3 | Expected files pinned L-11 etc and size-ish checks | Prose and incidental. | Behavioral: 80 rows, exact delta only on PENDING membership, byte identity for baseline waves, rack unchanged, hold on bad config, refuse existing output. |

Re-freeze after edit:

```bash
shasum -a 256 reference/REFERENCE.md | awk '{print $1"  reference/REFERENCE.md"}' > reference/REFERENCE.sha256
```
