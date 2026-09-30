# Module 7 · Evaluate a change with variation controls

Plan for one three-hour session. You will declare a hard-gate rule before you open results, compare two candidate desk briefs to their baselines across 40 paired cases, run the supplied evaluator, and restore the baseline copies from their frozen hashes.

The briefs describe heater-fuel cans from Ridge Depot to Clinic T-8 on vehicle SB-4. They are class review notes, not a movement order.

## Start here
1. Open [the Module 7 lab](shared/MODULE_07_LAB.md).
2. Read the [public scoring rubric](assessment/PUBLIC_RUBRIC.md) before you open a candidate.
3. If you use assistive technology or need another way to inspect a brief, read [Accessibility and equivalent inspection](shared/ACCESSIBILITY.md).

## The hard gates
Any single violation defeats a candidate. Do not average.

- Payload mass must be the exact number that appears in the authoritative #payload locator record, and the Source cell must name that locator.
- Gate times must name both the UTC value and the MDT value exactly as they appear in the authoritative #gate locator record, and the Source cells must name that locator.

A UTC word appearing in the wrong cell does not rescue a missing label. A bare clock token is a miss.

A malformed source packet or one belonging to a different case stops the whole comparison before results are written. It is not a candidate failure or a repair-cost observation. A malformed candidate brief under valid sources is a format-gate failure and remains in the comparison.

![Four kinds of evidence, not a blend](shared/figures/m07-variation.svg)

*Keep deterministic, repeated, hard-gate, and stochastic evidence in separate columns.*

## Class-only boundary
All names, hours, and masses used as defects are fictional course fixtures. Do not use this packet to plan, authorize, dispatch, or describe a real movement. A module result permits only class review.

