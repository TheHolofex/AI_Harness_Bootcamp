# Module 6 · Operate a fixed workflow through change

Plan for one three-hour session. You will run one saved workflow on two 80-lot waves, change one configuration line in one place, and prove that only the predicted rows move under the rule. Restore the baseline rule from its distinct hashed copy.

`PENDING` is part of the routing decision. It is not a quality release. `RACK_CONFLICT` is evaluated first and produces `hold,RESOURCE_CONFLICT`.

## Start here

1. Open [the Module 6 lab](shared/MODULE_06_LAB.md).
2. Read the [public scoring rubric](assessment/PUBLIC_RUBRIC.md) before you change the rule.
3. If you use assistive technology or need another way to inspect a receipt, read [Accessibility and equivalent inspection](shared/ACCESSIBILITY.md).

## The one-rule change

Baseline: `pending_status: OPEN` (AUTHORIZED lots are `pass,READY`; PENDING lots are `hold,OPEN`; every other permit state and cancelled lots are `hold,OPEN`).

Changed: `pending_status: NOT_AUTHORIZED` (PENDING lots become `reject,NOT_AUTHORIZED`; everything else stays as baseline). Rack conflicts remain held first.

The saved path and the input file stay the same. Only the one line in `RULE.md` changes.

## Class-only boundary

All lots, permits, windows, and notes are fictional course fixtures. Do not use this packet to plan, authorize, dispatch, or describe a real movement. A module result permits only class review.

