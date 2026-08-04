# AI Harness Bootcamp

The website is the course. Open [`site/index.html`](site/index.html) through the hosted course URL and follow the large day-by-day cards: B0, B1, Model Economics, P1, the Harness Control Plane presentation, P2 Project Organizer, two MCP presentations, P3, the Agent Loops & Agentic Patterns presentation, then P4 through P8.

Markdown in this repository is not a second reading path. It remains only where a lesson asks a student or an AI harness to work with real files:

| Path | Purpose |
|---|---|
| `operator/` | Direction briefs, logs, pass bars, adversarial review, measurement, and transfer files |
| `mission_flesh/` | Module corpora, starter files, and exercise inputs |
| `instruments/` | Exercise kits, test suites, comparison packs, graders, and score sheets |

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

## Course progression rule

Every project assumes that learners can already do everything required in the earlier projects. Earlier capabilities may return as prerequisites, operating constraints, or evidence standards, but they are not new learning objectives and should not be retaught as though the class is seeing them for the first time. Give a short reminder or link back at the point of use when needed; reserve project time for the next capability.

Write each project's mastery claim and learning objectives by answering:

> **What can the learner now do that they could not do before this project?**

Apply these tests whenever a project is created or revised:

1. **Capability-delta test:** complete the sentence “Before this project, the learner could ___. After this project, the learner can ___.” The second clause must name a meaningful new capability, not a new file, tool, scenario, or repetition count.
2. **Prerequisite test:** if an earlier project already taught the skill, state it as assumed knowledge or a required quality bar. Do not count it again as a learning objective.
3. **Dependency test:** each new objective must use at least one earlier capability and extend it into work the learner could not previously perform.
4. **Evidence test:** files, installations, checkboxes, logs, reflections, and transfer entries may prove or reinforce learning. They are not learning objectives by themselves.
5. **Progression test:** the project's mastery claim must add one clear capability to the course arc without restating an earlier mastery claim in different words.

Remediation is the exception. If learners cannot perform a prerequisite, repair it explicitly as prerequisite recovery without redefining it as the current project's new content.
