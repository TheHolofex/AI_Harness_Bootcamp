# Core authoring guide

**Serves oracle:** S02, S04, S05, S06, S07, S08, S09, S10, S11, S12, S14, S15, S16, S17, S18, S19, S20, S21, S24, S25, S26

## Scope and responsibility

This guide governs only the stable core skeleton. Product instructions, scenarios, commands, forms, fixtures, answers, and instructor procedures belong in adapters.

The learner specifies task-specific behavior, configures bounded values in supplied controls, tests, interprets, and decides. The **adapter implements** executable mechanics, dynamic checks, protected custody, equivalent accessible views, and evidence export, and supplies every module's case. A builder owns general-purpose code, API/MCP, retrieval pipelines, agent runtimes, and deployment.

Adapter-supplied raw state carries a plain-language legend naming each field and state value. The legend labels; it does not interpret the result.

## Module contract

Every module declares once:

- `Serves oracle`
- `Primary objective`
- `Prerequisites`
- `Consumes`
- `Produces`
- `Facilitated time`
- `Practice time`
- `Performance stage`
- `Work surface`
- `Practical work`
- `Performance evidence`
- `Failure / HOLD`
- `Scope boundary`
- `Handoff`

Modules are independent. Every entry in `Consumes` is supplied from outside the module and carries one of two prefixes:

- `VERIFY:` — the **learner** confirms it before the performance attempt. The check appears in that module's `Practical work` and its `Failure / HOLD` line. `VERIFY:PREFLIGHT` and `VERIFY:CASE` are the two universal session-entry preconditions: every module consumes them, and they are confirmed once at the start of the session rather than restated as module work.
- `CUSTODY:` — the **evaluator or adapter** confirms it, and the learner must not inspect it. Hidden faults, protected case banks, and recipient independence are custody items; a learner-facing check on one of these leaks the fixture.

No module consumes another module's product. Every token in `Produces` is named in that module's `Performance evidence` or `Gate`; the module's own claim-result token is established by its `Gate`. A mention in `Handoff` alone does not establish that a product exists.

A module has one primary outcome and at most three numbered enabling objectives. It leaves one evidence bundle and one claim result: `PASS` or `HOLD`. File presence cannot establish performance.

## Single ownership

| Sub-problem | Owner |
|---|---|
| Delegation, first-use limits, minimum screen, direction, bounded internal acceptance | 00 |
| Source verification and output discernment | 01 |
| Context, reusable instruction, source-as-data control | 02 |
| Full responsible release, tool authority, composed negative, revocation | 03 |
| Hidden-fault diagnosis and recovery | 04 |
| Observed-run analysis and predicate specification | 05 |
| Fixed workflow and deterministic outer-state change | 06 |
| Variation-aware candidate comparison and rollback | 07 |
| Restartability, person transfer, qualification closure | 08 |

## Responsibility before release

The minimum responsibility screen — source/data authority, sensitive-data boundary, affected audience or person, disclosure need, consequential authority, and human decision owner — is a standing rule applied in every module to its own supplied case. Modules 00–02 can make only bounded internal-acceptance decisions.

Module 03 owns the full contextual release and tool gate. A generic checklist or ethics statement fails. Every learner completes both the decision branch and the connection branch; a supported `no-use`, `no-release`, or `no-tool` position passes the decision claim and is studied for its reasoning, but does not satisfy or replace the operation claim.

## Evidence standard

Every bundle contains:

- work product or operated state;
- strongest independent or protected result;
- learner decision and owner;
- claim result;
- failure or `HOLD` when applicable;
- substitution record when a named dependency was replaced — what was replaced, the same-state basis, who certified it, and the affected outcome;
- scope boundary; and
- handoff.

The producer cannot edit, bypass, or select away its decisive check. A source of evidence is **independent or protected** only when custody sits outside the producer, the producer cannot enumerate or select the cases it will face, and the producer can neither author nor amend the result. Simulation, replay, discussion, narrated answers, and producer self-assessment cannot satisfy executed operation.

## Nondeveloper and dynamic-check boundary

The learner can specify a mechanically decidable predicate and configure it in a **supplied protected control**. The adapter implements any new checker and owns its protected identity. If the observed failure is an arbitrary semantic condition that cannot be represented in supplied controls, record the predicate, implementation dependency, owner, and `HOLD`; do not award implementation credit.

The fixed workflow is the highest common-core machinery. Persistent state, adaptive flow, multi-agent operation, custom RAG, API/MCP construction, runtime development, and deployment are advanced. A learner who meets a trigger for one of them records the trigger, the simpler alternative, the added risk, and the escalation owner.

## Deterministic and stochastic evidence

Exact blast-radius claims apply to deterministic outer state: input identity, route, status, field presence, policy version, receipts, and controlled deterministic fields. When probabilistic content materially affects acceptance, the run applies the pre-result variation rule below or routes the item to `HOLD`; one generated sample cannot establish exactness.

An output is **material** when a criterion named in the module's gate depends on its content. The classification is declared before the run and graded with the protected control; the producer does not reclassify after seeing output.

Candidate evaluation declares before results one of:

- a deterministic case whose material result is mechanically fixed;
- repeated paired controls with run count and aggregation rule;
- a hard gate that any single violation defeats; or
- exclusion of the stochastic claim from the decision.

## Qualification and transfer

`HOLD` may permit continued participation when safety allows; because modules are independent, a held outcome never blocks a later session. Final qualification requires every PO passed. An outcome is reassessed only against its original gate, on an unseen protected case, scheduled outside the facilitated hours, with both attempts preserved.

Clean-session and independent-person transfer are separate. The evaluator selects the task and holds the rubric; the recipient has not completed this core and did not observe the build. The recipient's preserved first attempt is scored without author coaching.

## Publication check

Publish only when objective/map/module fields agree, every consumed token is supplied and prefixed, the first action can run from verified products alone, failure cannot be mistaken for pass, detailed implementation has not entered core, and every authoritative file names served oracle criteria.

Learner-facing material carries no product token, prefix token, or `PO` identifier. Adapters map them to plain-language records a learner would recognize from ordinary work. `PASS` and `HOLD` are not covered by that ban; see the recorded decision below.

## Recorded decisions

### Markdown now, HTML at delivery

`CLAUDE.md` states: "The website is the course. Do not add learner-facing Markdown pages." That rule is anchored to Course 1's site and its path map. Reformation has no site yet, and Module 0's platform guides fall inside the rule's own carve-out — the learner works in a terminal on files in the clone, so handling the file is part of the exercise.

Decision: Reformation modules are authored in Markdown now and published to HTML at delivery. Modules 01–08 follow this rather than re-deciding it one module at a time.

The port is owed work, not a free conversion. Fenced command blocks, terminal and privilege labels, expected-output blocks, stop conditions, and per-fence language tags all carry meaning that the checks read; the HTML must preserve every one of them, and the checks must be re-pointed at the published pages rather than left reading the Markdown they no longer govern. Budget the port as its own task with its own verification pass.

### `PASS` and `HOLD` are ordinary English, and they stay

The publication check above once banned any "claim-state word" from learner-facing material, while the frozen Module 0 Reference requires the learner to record `PASS` or `HOLD`, and both words appear throughout the learner surface. Two documents asserting opposite rules is worse than either rule.

Resolved in favour of `PASS` and `HOLD`. A check passes; work goes on hold. Both are words a competent professional already uses at work, and neither reveals anything about how the course is built. The requirement to map internal vocabulary to plain language is satisfied by plain-language forms such as `PASS FOR CLASS REVIEW / HOLD`.

Two limits hold anyway. A recorded `PASS` is the outcome of a check, never the evidence for it — the verification response the learner sees must portray the observed value, so a learner typing `PASS` into a file cannot stand as proof that anything was verified. And the genuinely internal tokens stay banned in learner-facing material: `PO` identifiers, the `VERIFY:` and `CUSTODY:` prefixes, product tokens, and served-criterion names.
