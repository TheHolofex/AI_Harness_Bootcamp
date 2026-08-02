# AI Harness Bootcamp

The website is the course. Open [`site/index.html`](site/index.html) through the hosted course URL and follow the large day-by-day cards: B0, B1, Model Economics, P1, the Harness Control Plane presentation, P2, two MCP presentations, then P3 through P8.

Markdown in this repository is not a second reading path. It remains only where a lesson asks a student or an AI harness to work with real files:

| Path | Purpose |
|---|---|
| `operator/` | Direction briefs, logs, pass bars, adversarial review, measurement, and transfer files |
| `mission_flesh/` | Module corpora, starter files, and exercise inputs |
| `instruments/` | Test suites, comparison packs, graders, and score sheets |

The optional handouts under `site/resources/` are linked directly from the module that owns them. They add depth but do not form a separate course path.

## Maintainer map

| Path | Purpose |
|---|---|
| `site/` | Canonical learner-facing course |
| `resources/handouts/` and `resources/figures/` | Source material for generated optional handouts |
| `scripts/` | Resource build and verification tools |
| `lead/` | Internal facilitator runbooks; not learner navigation |
| `server.py` | Password-gated host; see [`HOSTING.md`](HOSTING.md) |

Do not add learner-facing Markdown pages. Put core instruction in the owning pre-work or module HTML page. Put optional depth in the resource build system. Add a raw file only when working with that file is part of the exercise.
