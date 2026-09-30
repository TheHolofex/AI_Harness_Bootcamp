# Reformation

**Serves oracle:** S02, S05, S06, S07, S09, S12, S13, S19, S20, S21, S24, S26

## Course identity

Reformation develops accountable AI-assisted work for a **professional domain user** at the smallest sufficient operating complexity. It is a professional AI-user and **harness operator** core, not a **builder** or software-engineering qualification. Final qualification requires observed human performance and the independent-recipient evidence; software checks and agent replays cannot award it.

A harness is the environment around a model: direction, context, sources, tools, permissions, working artifacts, saved controls, feedback, checks, and traces. The learner specifies bounded behavior, configures supplied controls, inspects evidence, and owns consequential decisions. An **adapter** implements and protects executable mechanics and supplies each module's case. A builder owns APIs, MCP, retrieval pipelines, agent runtimes, and deployment.

The core is designed for a **nondeveloper** who can use workplace files and applications and inspect plain-language configuration. A preflighted accessible environment supplies the mechanics.

The learner course is published under [`site/`](site/). Existing Markdown in [`AI_Harness_Bootcamp_2/`](AI_Harness_Bootcamp_2/) is maintainer source, not a second learner reading path. [`MISSION_THREAD_SCENARIOS.md`](MISSION_THREAD_SCENARIOS.md) owns the independent case specifications. [`evidence/exercise-runs.json`](evidence/exercise-runs.json) records observed exercise outcomes and explicit unverified lanes; design budgets are not pilot evidence.

## Core promise

The first-result design target is 60 minutes for producing and checking a useful bounded artifact; it is not a measured learner-completion promise. Before any consequential release, the learner applies a minimum responsibility screen. Across the core, the learner directs work, verifies sources, controls context, decides responsible release and operates a bounded tool, diagnoses failure, improves from observed runs, operates one fixed workflow, evaluates change with explicit treatment of model variation, and transfers the method.

The core runs as **ten sessions of three facilitated hours, including two hours of practice each** — Monday through Thursday morning and afternoon, Friday morning and afternoon. Every module owns one outcome, receives its own supplied case, and leaves **one evidence bundle per module**.

## Target sequence

| ID | Module | Primary capability |
|---:|---|---|
| 00 | Select, screen, and direct bounded work | Delegate appropriately, check one useful result, screen responsibility, and turn a request into accepted direction with a communication artifact. |
| 01 | Verify sources and outputs | Produce and challenge research/source work with independent evidence. |
| 02 | Control context and reusable instructions | Place information and rules where loading, precedence, survival, and bypass are observable. |
| 03 | Decide responsible release and operate bounded tools | Apply the full contextual release gate and operate a supplied capability at least authority, proving containment and removal. |
| 04 | Diagnose and recover | Localize a hidden fault, make an authorized reversible correction, and prove clean-condition recovery. |
| 05 | Improve from observed failures | Specify a mechanically decidable predicate and configure and validate it in a supplied deterministic control. |
| 06 | Operate a fixed workflow through change | Prove deterministic outer-state change while containing material probabilistic output. |
| 07 | Evaluate a change with variation controls | Use repeated controls or a justified deterministic case to separate change from ordinary variation. |
| 08 | Constrain agent behavior | Enforce a live agent’s declared tool boundary and distinguish observed denial from a prohibited call never attempted. |
| 09 | Transfer a runnable package | Assemble the smallest sufficient method, pass clean-session restart and stop/restore, and enable an independent person to operate the package. |

Cases and evidence bundles are **independent**: no gate consumes an earlier module’s product. Capabilities are cumulative: earlier skills are assumed, not retaught as new objectives. Authoritative sequence and supplied inputs are in [COURSE_MAP.md](COURSE_MAP.md). Outcomes are in [LEARNING_OBJECTIVES.md](LEARNING_OBJECTIVES.md). [AUTHORING_GUIDE.md](AUTHORING_GUIDE.md) owns the module contract.

## Core and advanced boundary

A fixed workflow is the highest machinery every core learner operates. Persistent state operation, adaptive flow operation, and multi-agent operation are advanced qualifications. Core learners recognize the trigger, simpler alternative, added risk, and escalation owner.

The core requires zero programming objectives. Dynamic checker implementation, API/MCP construction, custom RAG, agent-runtime development, and deployment remain adapter or builder work.

## Evidence and qualification rules

- A person owns consequential acceptance, release, refusal, authority expansion, and residual risk.
- A material acceptance uses independent evidence. A protected assessment additionally requires actual external custody; public practice files are inspectable, not secret because prose calls them protected.
- The producer cannot edit, bypass, or select away its decisive graded check. Authored practice data, hashes, model authorship, and agent role-play do not certify human qualification.
- Every learner both decides and operates. A supported `no-use`, `no-release`, or `no-tool` decision is professional performance and is recorded and studied; it does not satisfy or replace the operation claim.
- A material failure is preserved before repair. Localization-only is held, not recovery completion.
- File presence and refusal prose do not prove execution. Keep actual tool calls, execution results, guard records, and disk snapshots. A technical replay establishes only the behavior it exercised.
- `HOLD` may permit continued participation. Final qualification requires every program outcome passed or reassessed against its original gate on an unseen case held by an evaluator; without an actual independent recipient and evaluator custody the qualification lane remains HOLD.
- Clean-session restartability and independent-person transfer are separate; neither can substitute for the other.
- Each module bundle contains the artifact/state, decisive evidence, decision, claim result, failure or `HOLD`, scope boundary, and handoff.

## Authoritative files

- [Course map](COURSE_MAP.md)
- [Learning objectives](LEARNING_OBJECTIVES.md)
- [Authoring guide](AUTHORING_GUIDE.md)
- [`modules/core/`](modules/core/)
- [Mission-thread scenario memory](MISSION_THREAD_SCENARIOS.md) — staff specs for session projects; not a lab

Detailed scenarios, commands, forms, answer keys, fixtures, and platform procedures remain outside the core skeleton. Only allowlisted public pages and exercise files enter `site/`; staff references, historical reviews, graded selections, and answer keys stay outside publication.

## Pinned execution and publication

Participants need Git, Python 3.12+, Oh My Pi **18.3.5**, a browser, and an ordinary text editor. The only provider credential is `OPENROUTER_API_KEY`, supplied to the current process. Every live exercise selects **`openrouter/anthropic/claude-sonnet-4.6`** through `shared/run_omp.py`. The launcher creates fresh runtime state, exposes only course tools, disables retries and model fallback, and preserves evidence separately from work. The guard is an OMP tool boundary, not an operating-system sandbox.

Modules 02–09 use `shared/prepare_work.py`; Module 01 retains its nine-source starter and Module 00 retains its four-file copy. Helpers refuse existing work/output attempts. A missing key or unavailable pinned provider/model holds the live lane without replacing it with a different model or unlabeled fixture.

The child working directory is inside its redirected, fresh HOME. In pinned OMP, `--no-rules` does not disable [ancestor context-file discovery](https://github.com/can1357/oh-my-pi/blob/v18.3.5/packages/coding-agent/src/discovery/helpers.ts); placing cwd beside HOME allowed an outside ancestor's instructions to load. An actual offline OMP replay observed the leak before this placement fix and its absence afterward, with zero provider requests.

`reformation/.gitattributes` keeps text checkouts at LF so frozen source/control digests survive Git's automatic line-ending conversion. Native Windows setup also disables `core.autocrlf` for the clone command only. Do not renormalize or reset an existing dirty checkout to repair a hash failure; retain the mismatch and use an intact fresh copy.

Native OMP can exit 0 after an extension preparation error. The launcher still holds an attempt without exactly one completed terminal turn, the expected model identity, complete guard lifecycle, and matching tool/disk receipts. An offline host-invoked guard smoke verifies extension APIs and allow/deny behavior; it is not a model tool call or provider evidence. Runtime evidence files are local audit records, not cryptographic proof against an operator who can rewrite the whole evidence directory.

The saved-evidence audit joins each successful call to its authorization, independent execution check, tool/path identity, and filesystem effect. It also binds `response.md` to the final assistant event; changing only the extracted answer cannot change the recorded model response.

Node is required only by maintainers to reuse the existing figure renderer. From the repository root, create the virtual environment once and run:

```bash
python3.12 -m venv reformation/.venv
reformation/.venv/bin/python -m pip install -r reformation/requirements-dev.txt
node reformation/scripts/render_figures.mjs
reformation/.venv/bin/python reformation/scripts/build_course.py
reformation/.venv/bin/python reformation/scripts/check_course.py
reformation/.venv/bin/python reformation/scripts/build_course.py --check
python3.12 -m http.server 8765 --bind 127.0.0.1 --directory reformation/site
```

On native Windows, use `reformation\.venv\Scripts\python.exe` for the virtual-environment interpreter. Reuse the environment during correction loops. `check_course.py` never starts paid model calls; live verification is explicit and separately recorded. Serve only `reformation/site`, not the repository or staff source tree.
