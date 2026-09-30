# Reference amendments

Every change from the frozen Reference v1 (2026-08-12) to v2 (2026-08-14), with the reason and the evidence that forced it. Required by §6 D4: a deviation that is not recorded reads as conformance.

## Contradictions inside v1, now resolved

| # | v1 | Problem | v2 |
|---|---|---|---|
| 1 | §5.D required Ubuntu to provide "a command-line-only alternative when a desktop session is not present"; the next sentence required a desktop-capable machine for Obsidian. | Two clauses of the same section demanded opposite things. The build silently resolved it toward refusal and recorded nothing. | §4.2 resolves it explicitly: no desktop session means a named stop with the limitation recorded. The CLI-only-alternative clause is withdrawn. |
| 2 | §8 set 3 facilitated hours including 2 hours of learner work. The shipped lab timebox summed to 180 minutes and the facilitator schedule to 150. | Three numbers, no arbiter, and no check. Both shipped schedules exceeded the frozen budget. | §4.6 names 180/120 as the single source of truth, sourced to `COURSE_MAP.md`. §6 D3 asserts the arithmetic. |
| 3 | §6 closed with "Qualification evidence must remain in evaluator custody," which the build read as licence to invent a second, unseen graded case scored in the session's last 20 minutes. | No such case exists anywhere in the course skeleton. `COURSE_MAP.md:58` and `modules/core/00-direct-bounded-work.md:6,12` specify one supplied case with a supplied **protected acceptance control** (`VERIFY:PROTECTED_ACCEPTANCE`). | §6 E6 requires the skeleton model: one supplied case, one protected control confirmed before work and run by the evaluator. The unseen-second-case architecture is withdrawn. |
| 4 | §3 said installing n8n and Obsidian "does not become Module 0's learning objective," while the shipped rubric made Setup a hard gate of the module result. | A learner with broken n8n failed PO-00 regardless of their work. | §6 E4 forbids a setup gate in the rubric. §7 restates setup as an entry condition. |

## Criteria v1 required but never checked

| # | Source | v1 | v2 |
|---|---|---|---|
| 5 | `LEARNING_OBJECTIVES.md` PO-00 evidence; `00-direct-bounded-work.md:13,24` | The **capability-limit statement** — model output vs product surface vs harness control vs human decision, plus one observed capability and one limitation — appeared in no lab step, no work file, and no rubric row. | §6 E1 makes it a required record with a rubric gate. |
| 6 | `00-direct-bounded-work.md:30` Gate: "the falsifier fails visibly" | The lab asked the learner only to *state* a falsifier. Nothing ran it. | §6 E2 requires the learner to run it and record the observed failure. |

## The oracle, rebuilt

v1 §9 enumerated 21 criteria checked almost entirely by substring presence. The suite reported 171 PASS / 0 FAIL — a true count — while the module simultaneously contained three of v1 §10's own absolute failures and two learner files that no scan read.

| # | v1 mechanism | Why it failed | v2 |
|---|---|---|---|
| 7 | Hand-maintained file dictionaries. | `shared/case/REQUEST.md` and `CHANGED_INPUT.md` — both opened and copied by the learner — were in no scan set. Arbitrary unsafe content in them passed. | §6 C1: glob-derived scan set with an asserted count. |
| 8 | Safety scan restricted to ```bash|powershell|sh|zsh fences. | Seventeen ```text and ```markdown blocks were unscanned, and shipped content already puts executable commands in ```text. | §6 C2: every fence, regardless of info string. |
| 9 | Pins matched against a concatenation of all files. | One correct pin masked any number of wrong ones. | §6 C3: parsed from `VERSIONS.md`, asserted per file. |
| 10 | One `**Terminal:` and one stop-condition pair per *file* satisfied "every command block" and "every install step". | Structural conformance was measured per file, not per unit. | §6 C5: per-unit counts. |
| 11 | No check had a negative fixture. | Nothing proved any check could fail. | §6 C6 and the governing principle: every criterion names an input it must reject; `tests/mutations/` asserts it. |
| 12 | Nothing checked that the module was reachable, that blocks were paste-safe, or that a guide could not strand the learner. | The two most severe defects found in review — an unpublished module and a clone the guide itself dirtied — were invisible to every check. | §6 Class A, entirely new. |

## New material with no v1 counterpart

| # | Section | Why |
|---|---|---|
| 13 | §1.1 — a setup path is a program; an unexecuted program is broken. | Docable: 0 of 40 hand-annotated tutorials reached a working setup. v1 treated non-execution as a caveat; v2 treats it as a prediction of failure. |
| 14 | §1.2 — no time budget in this document is authored. | Nathan & Petrosino: experts underestimate novice completion time and cannot correct for it when told. v1's budgets were authored. |
| 15 | §2 — field survey, fourteen exemplars with citations. | v1 had none. Its standards were asserted rather than derived. |
| 16 | §4.3 — the adversary is named: an AI on the learner's machine optimising for green, and an honest learner under time pressure. | METR measured 30.4% vs 0.7% reward hacking on oracle visibility. v1 had no threat model. |
| 17 | §4.4 — three-state verdict. | v1 was binary, so any pin drift produced a hard HOLD. `brew doctor` is the standing evidence that a noisy binary gate gets ignored. |
| 18 | §5 — off-axis frontier. | v1 had none, so the conventional design was defaulted into rather than chosen. |
| 19 | §6 B7–B9, X8 — the deciding control must not exist on the learner's machine, and the tool-proof and n8n checks must verify provenance. | okpy keyed its HMAC on a public string; v1's tool proof was satisfiable by three `printf` calls; v1's n8n check passed against any listener on port 5678. |
| 20 | §6 A8, A9, B10 — credential entry alone; duration annotations; bounded retries. | Bracketed-paste capture of the following line; Salerno's progress-feedback category (9/24 sessions); ImpossibleBench's finding that extra submissions raise gaming 33%→38%. |
| 21 | §8 — obsolescence with named signals. | v1 §12 listed empirical limits but no expiry conditions. |

## Carried forward unchanged

v1's shared environment rules (§4, now §3 invariants 1–8), its absolute-failure list, its parsimony rule, its 32/32 panel standard, and its refusal to accept an AI-detector score as evidence. The last is now cited: RAID (ACL 2024) and Liang et al. (2023).

## Re-freezing

`REFERENCE.sha256` records the SHA-256 of the amended `REFERENCE.md`, followed by `reference/REFERENCE.md`. Change the digest only for an explicit contract amendment; retain the reason and behavioral evidence here. Historical v1/v2 findings above remain historical.

## v3 amendment — one harness, one provider, honest evidence

| # | Previous requirement or defect | Current contract and reason |
|---|---|---|
| 22 | Multiple participant agent/tool chains, unaudited proof files, mixed provider pins and clean-tree gating | Git/Python/OMP 18.3.5 plus OpenRouter only; exact `openrouter/anthropic/claude-sonnet-4.6`; verified-first official binary; three-argument token-and-receipt proof. Preserve unrelated checkout changes and use external work. |
| 23 | Protected-control claims described a public practice checker as inaccessible; technical or agent results could be read as qualification | Public practice is inspectable. Qualification requires actual independent evaluator custody and original evidence; otherwise HOLD. No fabricated control, human result, or hidden second case. |
| 24 | Old timeboxes and perfect review scores implied measured performance | Session allocations and the 60-minute first-result goal are design targets. Keep platform, live, accessibility, peer and human outcomes separate; no unobserved pass. |
| 25 | Frozen reference still contained retired services, multi-agent setup checks, source-wording gates and thin-case examples after the setup cutover | Replace active §§3–8 with the implemented single-runtime and North Shelf contract; retain the research survey and historical evidence. Preserve all supplied case facts and the count-only changed input. |
| 26 | The public checker rejected “No vehicle is assigned,” “No permit is approved” and “No receipt is confirmed” by matching a shorter positive substring | An affirmative span shields only the nested substring; a separate contradictory occurrence still wins. Actual before/after counterexamples are retained in the staff QA record; nine polarity boundaries are permanent regression coverage. |
| 27 | macOS's reopened-terminal block repaired PATH while claiming persistent availability | Persist the non-secret user-bin setting idempotently in the selected login profile, then verify in a new shell without a PATH repair. The isolated cold-shell before-run selected the other installation and failed the intended-path check. |
| 28 | OMP `--no-rules` did not stop ancestor context discovery outside the isolated runtime cwd | Place cwd beneath isolated HOME. The real pinned-OMP before/after smoke observed the external synthetic context marker before the fix and its absence after it, with zero provider requests. |

The digest is re-frozen for this explicit v3 replacement, not to hide a failed gate. Per-run evidence and unresolved external dependencies are recorded in `reformation/evidence/exercise-runs.json`.
