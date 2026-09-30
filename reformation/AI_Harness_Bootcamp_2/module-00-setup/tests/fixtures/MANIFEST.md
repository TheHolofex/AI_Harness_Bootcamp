# Fixture manifest

Each failing fixture is the canonical draft with exactly one substitution.
The checker must reject it, and must name the listed check.

| Fixture | Must fail on |
|---|---|
| `fail/too-short.md` | word count |
| `fail/no-subject.md` | subject line |
| `fail/wrong-commodity.md` | commodity |
| `fail/wrong-origin.md` | origin |
| `fail/wrong-clinic.md` | destination |
| `fail/missing-thursday.md` | thursday |
| `fail/missing-friday.md` | friday |
| `fail/wrong-hours.md` | documentation hours |
| `fail/missing-contact.md` | contact line |
| `fail/requested-wrong.md` | requested 40 |
| `fail/on-hand-changed-to-19.md` | on-hand 27 |
| `fail/wrong-pen.md` | pen 4 |
| `fail/claims-release.md` | custody not release |
| `fail/missing-owner.md` | release owner |
| `fail/assigns-vehicle.md` | no vehicle |
| `fail/approves-permit.md` | no permit |
| `fail/confirms-receipt.md` | no receipt |
| `fail/claims-supportable.md` | supportability |
| `fail/missing-class.md` | class participants |
| `fail/expect-window.md` | prohibited sentence |
| `fail/hs3-assigned.md` | HS-3 |
| `fail/stages-for-truck.md` | delivery promise |
| `fail/writes-go.md` | no GO |
| `fail/invented-clock-time.md` | invented clock |
| `fail/public-distribution.md` | prohibited distribution |

| Fixture | Must pass |
|---|---|
| `pass/canonical.md` | every check |
| `pass/paraphrase.md` | every check, using different wording |
