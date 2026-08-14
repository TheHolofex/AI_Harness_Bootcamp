# Fixture manifest

Each failing fixture is the canonical draft with exactly one substitution.
The checker must reject it, and must name the listed check.

| Fixture | Must fail on |
|---|---|
| `fail/inverted-cost.md` | cost |
| `fail/inverted-eligibility.md` | identification |
| `fail/inverted-entrance.md` | entrance |
| `fail/capacity-changed-to-45.md` | capacity |
| `fail/capacity-spelled-wrong.md` | capacity |
| `fail/service-meals.md` | unconfirmed services |
| `fail/service-shuttle.md` | unconfirmed services |
| `fail/service-childcare.md` | unconfirmed services |
| `fail/service-medical.md` | unconfirmed services |
| `fail/service-overnight.md` | unconfirmed services |
| `fail/service-chargers.md` | unconfirmed services |
| `fail/missing-contact.md` | contact line |
| `fail/no-subject.md` | subject line |
| `fail/wrong-hours.md` | public hours |
| `fail/wrong-address.md` | address |
| `fail/missing-tuesday.md` | both days |
| `fail/missing-wednesday.md` | both days (wednesday) |
| `fail/public-distribution.md` | prohibited distribution |

| Fixture | Must pass |
|---|---|
| `pass/canonical.md` | every check |
| `pass/paraphrase.md` | every check, using different wording |
