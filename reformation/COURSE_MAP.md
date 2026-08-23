# Core course map

**Serves oracle:** S02, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14, S17, S18, S19, S20, S21, S22, S23, S24, S25, S26

This file is authoritative for sequence, supplied inputs, work surfaces, budgets, degraded behavior, and qualification. [LEARNING_OBJECTIVES.md](LEARNING_OBJECTIVES.md) owns outcomes. [AUTHORING_GUIDE.md](AUTHORING_GUIDE.md) owns the module contract.

## Program design budgets

| Budget | Standard | Evidence status |
|---|---:|---|
| Facilitated seat-time **including practice** | 27 hours across nine sessions; bound 24–35 | Design arithmetic; unmeasured until pilot |
| Practice included in seat-time | 18 of 27 hours (66.7%); minimum 60% | Design arithmetic; unmeasured until pilot |
| First checked useful artifact | Within 60 minutes | Provisional until timestamped pilot |
| Core modules | 9, one per session | Measured structurally |
| Variable model/tool spend | Provisional ≤US$40 per learner | Requires usage ledger including retries/make-ups |
| Human scoring | Provisional median ≤15 min/gate; p90 ≤25 min | Requires timed judge logs including moderation and `HOLD` review |
| Binary hard-gate agreement | Provisional ≥90% exact | Requires ≥20 double-scored performances |
| Ordinal judgment agreement | Provisional weighted κ ≥0.70 | Requires ≥20 double-scored performances |
| Reassessment and make-up attempts | Outside the facilitated hours, at the original gate's own duration | Provisional; requires make-up scheduling and fixture-rotation evidence |
| Independent-recipient session | One per learner, outside the facilitated hours | Provisional; requires recruitment and scheduling evidence |
| Expected cohort / 10x case | 20 / 200 learners | Planning cases, not demonstrated capacity |

No unmeasured budget is reported as achieved. Delivery may vary support and extra optional practice; it may not hide required work outside seat-time or lower a gate.

## Schedule and independence

Nine sessions of three facilitated hours, including two hours of practice each.

| Session | Day | Module |
|---:|---|---|
| 1 | Monday AM | 00 Select, screen, and direct bounded work |
| 2 | Monday PM | 01 Verify sources and outputs |
| 3 | Tuesday AM | 02 Control context and reusable instructions |
| 4 | Tuesday PM | 03 Decide responsible release and operate bounded tools |
| 5 | Wednesday AM | 04 Diagnose and recover |
| 6 | Wednesday PM | 05 Improve from observed failures |
| 7 | Thursday AM | 06 Operate a fixed workflow through change |
| 8 | Thursday PM | 07 Evaluate a change with variation controls |
| 9 | Friday AM | 08 Transfer and close qualification |

Sessions run in this order, and **no module's gate depends on another module's evidence**. Every module receives its own supplied case and its own supplied machinery, verified at entry. A learner who misses or holds one session can still perform the next. A held outcome blocks final qualification, never participation.

Adapters share [CASE_FAMILY.md](CASE_FAMILY.md); every module still receives its own supplied case and its gate does not consume another module’s product.

## Performance progression

| Stage | Meaning | Sessions |
|---|---|---|
| **Guided** | Use and challenge a supplied bounded method. | Opening of session 1 |
| **Independent** | Author task-specific direction, evidence, and decisions. | 1–4 |
| **Adversarial** | Preserve standards under changed, misleading, malformed, over-authorized, hidden, or variable conditions. | 5–8 |
| **Transferred** | Operate from saved artifacts, support another person, and close every outcome. | 9 |

File presence cannot satisfy a performance stage. Simulation, discussion, replay, or producer self-assessment cannot satisfy executed operation.

## Sequence, supplied inputs, and gates

| ID | Module | Time / practice | Consumes | Produces | Work surface | Material gate |
|---:|---|---:|---|---|---|---|
| 00 | Select, screen, and direct bounded work | 3h / 2h | `VERIFY:PREFLIGHT`; `VERIFY:CASE`; `VERIFY:PROTECTED_ACCEPTANCE` | `FIRST_RESULT`; `MIN_SCREEN`; `DIRECTION`; `INTERNAL_ARTIFACT`; `PO00_RESULT` | **communication artifact** | Checked useful artifact within 60 minutes; delegate/human/refuse choices and minimum screen support bounded internal acceptance; frozen direction and protected changed-input check support internal accept/fix/hold |
| 01 | Verify sources and outputs | 3h / 2h | `VERIFY:PREFLIGHT`; `VERIFY:CASE`; `VERIFY:SOURCE_FIXTURES` | `SOURCE_EVIDENCE`; `DISCERNMENT_RESULT`; `STANDING_RULE`; `PO01_RESULT` | **research/source** work | Known-answer, source-trace, misleading-source, changed-source, and real-use checks support internal accept/revise/reject/hold |
| 02 | Control context and reusable instructions | 3h / 2h | `VERIFY:PREFLIGHT`; `VERIFY:CASE`; `VERIFY:PROTECTED_GUARD` | `CONTEXT_MAP`; `SOURCE_AS_DATA_CONTROL`; `RELOAD_RESULT`; `PO02_RESULT` | Reusable instruction and guard | Loading, precedence, reset survival, and bypass are independently evidenced |
| 03 | Decide responsible release and operate bounded tools | 3h / 2h | `VERIFY:PREFLIGHT`; `VERIFY:CASE`; `VERIFY:CAPABILITY` | `RELEASE_DECISION`; `AUTHORITY_BOUNDARY`; `COMPOSED_NEGATIVE`; `REVOCATION_RESULT`; `PO03_RESULT` | Tool-assisted artifact | Both claims pass: contextual release decision on every concern, and least-authority operation with containment, approval, disconnect, and revocation |
| 04 | Diagnose and recover | 3h / 2h | `VERIFY:PREFLIGHT`; `VERIFY:CASE`; `VERIFY:RESTORE_PATH`; `CUSTODY:HIDDEN_FAULT_ENV` | `LOCALIZATION_RESULT`; `RECOVERY_RESULT`; `PO04_RESULT` | Unfamiliar faulty harness | Localization is graded separately; PO-04 passes only after authorized correction or verified revert plus focused, end-to-end, and clean-condition evidence |
| 05 | Improve from observed failures | 3h / 2h | `VERIFY:PREFLIGHT`; `VERIFY:CASE`; `VERIFY:RUN_SAMPLE`; `VERIFY:PROTECTED_CONTROL` | `SAMPLE_MANIFEST`; `PREDICATE_SPEC`; `PROTECTED_CONTROL_RESULT`; `PO05_RESULT` | Observed-run corpus | Outcome-blind analysis supports a mechanically decidable predicate configured and validated in the supplied protected control; arbitrary semantic implementation is held |
| 06 | Operate a fixed workflow through change | 3h / 2h | `VERIFY:PREFLIGHT`; `VERIFY:CASE`; `VERIFY:BATCH_WORKLOAD`; `VERIFY:SAVED_WORKFLOW` | `FIXED_BASELINE`; `EXCEPTION_RULE`; `DETERMINISTIC_DELTA`; `CONFIG_ID`; `RESTORE_ACTION`; `PO06_RESULT` | **structured-data/batch** work | Same saved path handles baseline and second wave; one-rule exact delta is limited to deterministic outer state; stochastic material items follow a rule declared before the run or hold |
| 07 | Evaluate a change with variation controls | 3h / 2h | `VERIFY:PREFLIGHT`; `VERIFY:CASE`; `VERIFY:BASELINE_CONFIG`; `VERIFY:CANDIDATE` | `PRE_RESULT_POLICY`; `CHANGE_DECISION`; `COST_PROXY`; `RESTORED_BASELINE`; `PO07_RESULT` | Frozen paired cases | Pre-result repetition/exclusion rule, hard gates, paired evidence, bounded recommendation, and restored baseline support the decision |
| 08 | Transfer and close qualification | 3h / 2h | `VERIFY:PREFLIGHT`; `VERIFY:CASE`; `VERIFY:PO_LEDGER`; `CUSTODY:CAPSTONE_CASES`; `CUSTODY:RECIPIENT` | `RUNNABLE_PACKAGE`; `PO08_RESULT`; `QUALIFICATION_RESULT` | Unfamiliar professional task | Protected challenge, clean session, no-coaching independent person, and outcome ledger all pass; a missing outcome is reassessed at its original gate or qualification remains held |

## Minimum and full responsibility gates

`MIN_SCREEN` covers source/data authority, sensitive-data boundary, affected audience/person, disclosure need, consequential authority, and human decision owner. It is a standing rule: every module applies it to its own supplied case, and an unresolved item is `HOLD`. Modules 00–02 can claim only bounded internal acceptance.

An acceptance is **bounded internal** when the artifact reaches only named participants in the learning engagement and no decision outside it depends on the artifact. Anything else is **consequential** and requires the Module 03 gate.

Module 03 owns the full gate: privacy/security, copyright/IP, fairness/bias, transparency/disclosure, affected-person impact and recourse, and human accountability, including their combined effect. A generic checklist or universal legal conclusion fails.

Decision and operation are separate claims, and **every learner completes both**:

- **decision branch:** a supported `no-use`, `no-release`, `no-tool`, or bounded release position with its contextual evidence;
- **connection branch:** performed by every learner on the supplied safe capability — raw authority, useful bounded action, composed negative, approval, disconnect, and revocation.

A supported refusal is professional performance and is recorded and examined for its reasoning. It is studied, not credited as operation, and it does not replace the supplied connection case. `PO03_RESULT` names which position the learner took.

## Complexity and implementation boundary

Fixed workflow is the highest mandatory operation. Persistent state operation is advanced. Adaptive flow operation is advanced. Multi-agent operation is advanced.

The learner specifies and configures bounded behavior in supplied controls. The adapter implements dynamic protected checks and accessible mechanics. API/MCP, custom RAG, runtime, and deployment remain builder work.

## Degraded and 10x policy

If a **model**, **tool**, **source**, **protected fixture**, **recipient**, **accessible** same-state view, or **restore** path is missing, the affected outcome uses equivalent same-state execution, retains only bounded unaffected evidence, or records `HOLD`. No replay or narration becomes operation. A substituted dependency is named in the gate record with its same-state basis and who certified it. Because no module depends on another's evidence, a missing dependency holds one outcome and does not cascade.

At 200 learners, outcomes, supplied cases, rubrics, qualification, transfer, and hidden custody remain unchanged. The scale plan must account for mechanical runners, hidden-case rotation, scorer calibration, **double-scoring**, **moderation**, **appeals**, make-up attempts, and independent-**recipient capacity**. Missing staffing or budget evidence is exposed as provisional, not solved by sampling learners or weakening gates.

## Qualification and transfer

`HOLD` can permit continued participation when safe. **Final qualification** requires every program outcome passed. A missing outcome is **reassessed** against its original gate on an **unseen** protected case, scheduled outside the facilitated hours; capstone work does not overwrite the prior attempt. A protected case the learner has already worked is spent and cannot carry that learner's evidence at any cohort size.

Clean-session restartability and independent-person transfer are separate and cannot substitute. The **evaluator** — neither the learner nor a cohort member — selects the task and holds the protected rubric. The **recipient** has not completed this core and did not observe the package being built, receives operating access before the attempt, and completes an evaluator-selected task on a preserved **first attempt** with **no author coaching**. A held first attempt may be retried only with a new recipient and a new task, both attempts preserved.
