# AI Harness Bootcamp

A five-day operator course: direct → harness → verify → adjudicate → bound → choose machine → transfer.
The course is a **website**, not a slide deck, and it runs from this repository.

## Students

Start with **[`prework/README.md`](prework/README.md)** and finish it before Monday. It stands up your own
Windows 11 workstation — there is no golden image. Plan two to four hours.

Then serve the site locally and work the interactive checklist:

```powershell
python -m http.server 8080
```

Open <http://localhost:8080/site/>.

## Staff

**[`START_HERE.md`](START_HERE.md)** is the operator entry point — run modes, the repo map, and the
before-the-window checklist. Fill **[`lead/COHORT_PIN.md`](lead/COHORT_PIN.md)** before pre-work opens;
it decides room quality more than any single curriculum page.

## Layout

| Path | What |
|---|---|
| `site/` | The course itself — block pages, checklists, references |
| `prework/` | Student-owned Windows install |
| `operator/` | Brief, log, pass bars, adversarial review, measurement, transfer |
| `instruments/` | Shared kits for P2, P3, P8 |
| `mission_flesh/` | Corpora and packs per block |
| `lead/` | Facilitator helpers and the cohort pin sheet |
| `server.py` | Password-gated host for deploying the site — see `HOSTING.md` |

Facilitator keys and answer material are excluded from the hosted site by `server.py`, but they are
present in this repository. See `lead/MANY_MINDS_ANSWER_KEY.md` for the caveat that follows from that.
