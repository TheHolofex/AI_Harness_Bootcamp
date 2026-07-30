# Many Minds — answer key (staff only)

**Do not paste into a student channel, and do not open this on a shared screen
before the synthesis files are written.** The corpus is deliberately unlabelled
so the specialists have something to actually find.

One honest caveat: students clone this repository in pre-work, so this file is
on their laptops too. Nothing here is secure — it is out of the learner guide's
way, not hidden. If a cohort needs real separation, delete this file from the
student-facing clone and keep the key in the staff channel instead.

Pack: `instruments/p3_multi_agent/` · Learner guide: `mission_flesh/p3/MANY_MINDS.md`

---

## The three seeded defects

All three are in `corpus/service_snippet.py`. All three survive the tests in
`corpus/tests_snippet.py`, which pass green.

| # | Symbol | What is wrong | Reproduces as | Lens that should catch it |
|---|---|---|---|---|
| D1 | `normalize_amount` | Empty input returns a silent `0.0` instead of failing closed | `normalize_amount("")` → `0.0` | 1 · correctness |
| D2 | `apply_discount` | `percent` is never clamped, so over-100% discounts invert the sign | `apply_discount(100.0, 150)` → `-50.0` | 1 · correctness, or 3 · spec drift |
| D3 | `authorize_transfer` | Role comparison is case-sensitive, so `"Admin"` is denied | `authorize_transfer("Admin", 100.0)` → `False` | 3 · spec drift |

Verify any time with:

```bash
cd instruments/p3_multi_agent/corpus
python3 -c "from service_snippet import *; print(normalize_amount(''), apply_discount(100.0,150), authorize_transfer('Admin',100.0))"
```

Expected: `0.0 -50.0 False`

## Where the contradictions live

`corpus/NOTES_ops.md` is the spec side of the drift, and it is legitimate
discoverable signal — leave it exactly as it is. It states:

- roles are **case-insensitive** and desk staff type `Admin` → contradicts D3
- empty amounts should **fail closed**, never become zero → contradicts D1
- discounts above 100% must be **rejected** → contradicts D2, and the "last
  incident" line describes D2's exact symptom (a `percent=150` paste producing
  a credit)

So D2 and D3 are reachable from two directions. D1 is reachable from the ops
note and from reading the function. A room that finds only one of the three has
usually collapsed all three lenses into one agent.

## What the test file misses

`tests_snippet.py` covers only the happy path — a plain amount, a 10% discount,
a lowercase admin under the limit. Lens 2 should name at least: empty and
malformed amount input, discount above 100 (and negative), the `"Admin"` casing
case, and the clerk boundary at exactly 500.

## Grading the synthesis

The stretch bar is in `operator/PASS_BARS.md` · P3 Stretch. What actually
separates a pass from theatre:

- **The merge is real.** Three agents on a 40-line corpus will overlap. If the
  synthesis lists nine findings with no dedupe, orchestration did not happen.
- **The kill is earned.** With up to five findings per agent on a corpus this
  small, agents pad. The padding is where legitimate kills come from — style
  nits, invented severities, "consider adding type hints." A student who cannot
  find anything to kill probably did not read the returns.
- **Missing D2 or D3 entirely** usually means the spec-drift lens never ran, or
  the agent read only the code and skipped `NOTES_ops.md`.
- **A finding that claims a defect not in this table** is worth reading closely.
  Sometimes it is a hallucination worth killing; occasionally a student's agent
  finds something real about the float arithmetic or the missing thousands
  separator. Both outcomes are good material for the log.

## If you need a harder run

Add a fourth file with a plausible-but-wrong fix already applied, and see
whether any lens catches that the fix does not hold. Do not add more defects to
the existing three — the pack is sized so three specialists finish inside the
block.

---

## Mastery-path grading (deeper bar)

Learner guide now requires three artifacts:

| File | Fail if |
|---|---|
| `out/baseline_single.md` | Missing, or subagents were used, or findings lack corpus evidence |
| `out/many_minds_synthesis.md` | Missing; undedupe paste job; kill is vibes-only |
| `out/many_minds_delta.md` | Missing; empty unique-to-* sections without search note; no defended verdict |

### What “earned kill” means
The discarded specialist claim must be wrong, out of scope, or unsupported **when checked against the corpus** (or clearly padded style advice). “I didn’t like it” is theater.

### Spot-audit order
1. Open delta verdict first.  
2. Confirm baseline exists and is non-empty.  
3. Check one kill’s corpus citation.  
4. Only then glance at whether D1–D3 appeared somewhere in baseline or parallel.

A student can miss one seeded defect and still pass the stretch if baseline+delta+earned kill are real. A student who “finds all three” with no baseline does **not** meet the mastery stretch.
