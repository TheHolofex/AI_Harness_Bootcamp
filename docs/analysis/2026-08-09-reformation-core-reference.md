# Reference: Reformation Core Professional AI-Harness Course

Date frozen: 2026-08-09  
Mode: Reference  
Tier: Scout  
Status: **READ-ONLY AFTER ORACLE TRANSLATION**

## Assumptions

1. The subject is the core professional AI-harness course skeleton: audience, competency boundary, sequence, prerequisites, learning objectives, performance evidence, progression, and capstone.
2. Product adapters, lesson scripts, executable fixtures, instructor packs, learner-facing copy polish, web delivery, visual design, and specialist qualifications are outside this Reference.
3. Learners are capable professionals in a domain, may be nondevelopers, and have basic workplace digital competence.
4. The target is a 24–35 facilitated-hour bootcamp. This range is a design assumption because no calendar was supplied.
5. The expected cohort is 20 learners; the 10x condition is 200 learners. These are labeled planning assumptions.
6. The implementation may use managed, declarative, or no-code mechanisms. It may not require programming for core completion.
7. Research sources establish current curriculum and competency boundaries. They do not establish comparative course effectiveness.

# Part 1 — The Reference

## 1. The need

Domain professionals at the moment they begin using AI on recurring, decision-serving work need a bounded path from first useful result to independently verified, safely repeatable, recoverable, and transferable practice, preventing polished but unsupported output, unsafe delegation, hidden authority, brittle chat-only methods, and agent-system complexity that the work did not earn.

The underlying problem is not “teach every AI-harness mechanism.” It is **qualify professional judgment and operation at the smallest complexity rung needed for reliable work**.

**Done:** a nondeveloper can independently select appropriate AI work, direct and verify a useful artifact, operate one saved bounded workflow, recover from a material failure, evaluate a change, and transfer the package to another person, while correctly declining or escalating persistent-state, adaptive, or multi-agent machinery that exceeds the core role.

## 2. Field survey

| Exemplar | What it gets right | Where it breaks against this need | Confidence |
|---|---|---|---|
| [Google AI Professional Certificate](https://grow.google/ai-professional/) | Zero-experience entry; structured prompting; planning, research, writing, data analysis, source verification, reusable assets, chained workflows, and light app building through 20+ activities. | Product-centered and broad rather than an operator qualification; the public curriculum does not require protected checks, fault localization, recurrence proof, authority revocation, or person transfer. | High on published curriculum; medium on assessment depth. |
| [Anthropic AI Fluency: Framework & Foundations](https://anthropic.skilljar.com/ai-fluency-framework-foundations) | A compact professional model: Delegation, Description, Discernment, Diligence; explicitly includes effective, efficient, ethical, and safe use. | Stops at general fluency. It does not qualify operation of tools, saved workflows, state, recovery, or transfer. | High. |
| [OpenAI Academy](https://academy.openai.com/) | Presents a useful progression from foundations to applied work and agents/workflows; emphasizes context, boundaries, review, improvement, and reuse. | Public catalog content is dynamic and product-specific; it is not a stable vendor-neutral performance standard, and independent acceptance/transfer is not consistently visible from the public catalog. | Medium. |
| [Microsoft AI-3025 and Microsoft 365 Copilot learning paths](https://learn.microsoft.com/en-us/training/courses/ai-3025/) | Embeds AI in familiar office work; covers grounding, prompts, organizational data, documents, email, meetings, spreadsheets, presentations, and prebuilt agents. | Tied to one productivity ecosystem; operation beyond its managed boundaries does not establish general harness diagnosis, protected evidence, or portability. | High. |
| [DeepLearning.AI — Generative AI for Everyone](https://www.coursera.org/learn/generative-ai-for-everyone) | Efficient beginner foundation in capabilities, limitations, prompts, project lifecycle, opportunities, risks, and business implications. | Six-hour conceptual breadth cannot qualify recurring workflow operation, abnormal-condition response, or transfer. | High. |
| [DeepLearning.AI — AI Agents in LangGraph](https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/) | Teaches controllable agents, persistence, state, search, and human-in-the-loop behavior. | Requires intermediate Python and targets developers. It demonstrates that persistence and agent runtime design are builder competencies, not universal nondeveloper foundations. | High. |
| [NIST AI RMF and Generative AI Profile](https://www.nist.gov/itl/ai-risk-management-framework) | Supplies a defensible governance frame—Govern, Map, Measure, Manage—and concrete generative-AI risk categories. | It is an organizational risk framework, not a learner sequence or bootcamp assessment. Applied wholesale, it would overload a professional-user course. | High. |
| [European Commission DigComp 3.0](https://joint-research-centre.ec.europa.eu/projects-and-activities/education-and-training/digital-transformation-education/digital-competence-framework-citizens-digcomp/digcomp-30_en) | Integrates AI across information evaluation, communication, content creation, privacy/safety, and problem solving; treats competence as knowledge, skill, and attitude. | Broad digital competence does not specify harness context, tool authority, protected checks, recovery, or transfer. | High. |
| [EU AI Act Article 4 literacy Q&A](https://digital-strategy.ec.europa.eu/en/faqs/ai-literacy-questions-answers) | Requires literacy measures to reflect role, prior knowledge, context of use, system risks, output interpretation, and human oversight. | It sets contextual obligations, not a universal curriculum or proficiency threshold. Legal applicability and wording can change. | High on current published guidance; medium at 18 months. |

Survey conclusion: mainstream workplace courses are strongest at **use AI well**; developer courses are strongest at **build agentic systems**. The unoccupied center is **operate AI-assisted work as a bounded, checked, recoverable, transferable method without requiring software engineering**.

## 3. Governing constraints and invariants

### Invariants

1. **Human accountability:** AI may inform a consequential decision; it may not silently own acceptance, release, refusal, authority expansion, or residual-risk acceptance.
2. **Independent evidence:** every released material artifact has at least one decisive observation outside the producing path or protected from it.
3. **Source and claim integrity:** unsupported claims, missing evidence, or disputed acceptance produce a visible hold, not a polished release.
4. **Least-powerful sufficient method:** prompting precedes reusable procedure; fixed workflow precedes persistent state, adaptation, or multiple workers.
5. **Nondeveloper completion:** no core objective requires programming, API implementation, retrieval-pipeline construction, agent-runtime construction, or deployment engineering.
6. **Role- and risk-contextual literacy:** foundations, controls, and evidence match the learner's role and intended use; generic familiarity is not enough. This reflects current EU Article 4 guidance.
7. **Privacy, security, IP, fairness, transparency, and affected-person impact:** release judgment addresses each when applicable; “responsible use” cannot be satisfied by a warning slide.
8. **Recovery preserves evidence:** a material failure is preserved, bounded, diagnosed before repair, changed once at an owning surface, and checked under the original condition.
9. **Transfer is observed:** restartability and another person's use are different claims.
10. **Vendor neutrality:** competencies and evidence survive replacement of the product, model, scenario, or interface.
11. **Accessibility:** a core proof is possible through keyboard-operable, text-exportable, inspectable controls; inaccessible hidden state cannot carry evidence.
12. **Scope:** the core skeleton contains only objectives, sequence, contracts, practice classes, evidence classes, boundaries, and budgets. Detailed lesson implementation lives elsewhere.

### Legal and policy constraints

- EU deployments may require contextual AI-literacy measures under Article 4 and human-oversight training for applicable high-risk systems. The skeleton must make role, context, risk, and oversight visible; it does not claim legal compliance.
- Personal data, confidential data, intellectual property, accessibility, records retention, sector policy, and employment rules vary by learner context. The core must require an applicable-policy decision and an escalation owner; it cannot provide one universal answer.
- NIST AI RMF and the OECD AI Principles are guidance/reference frameworks, not pass-through legal requirements.

### Economic and ergonomic constraints

- **Facilitated core time:** 24–35 hours; ideal target **30 hours** (assumption).
- **Active practice:** at least **60%** of facilitated time.
- **Time to first useful AI-assisted artifact:** at most **60 minutes** after the course starts in a preflighted environment.
- **Core modules:** at most **10**, each with one primary program objective and no more than three enabling objectives.
- **Mandatory learner record burden:** one evidence bundle per module; recovery appendix only when a material failure occurs.
- **External variable tool/model spend:** at most **US$40 per learner** for the core, excluding tuition, staff, and hardware (planning guess).
- **Human scoring burden:** target at most **15 minutes per learner per module gate**, using protected mechanical checks for mechanically decidable facts and a short rubric for judgment (planning guess).

### Tradeoff frontier

| Axis | Ideal position | Reason |
|---|---|---|
| Breadth ↔ operational depth | Three common work surfaces plus one fully operated workflow | Enough breadth for workplace transfer; depth concentrated where repeatability begins. |
| Safety ↔ time to value | First useful bounded result before deep controls | Early value earns attention; the environment is preflighted so safety does not depend on lecture-first delay. |
| User fluency ↔ builder skill | Advanced user/harness operator | The learner configures and decides; supplied components own runtime implementation. |
| Standardization ↔ domain relevance | Stable evidence contract with replaceable domain scenarios | Competence remains comparable while the work remains authentic. |
| Completeness ↔ parsimony | Ten or fewer modules, one primary objective each | Every required element must change a learner performance claim. |
| Rigor ↔ grading scalability | Protected checks plus narrow human judgment | Machine checks decide mechanics; people judge fitness, context, and responsibility. |
| Complexity exposure ↔ mandatory operation | Recognize all rungs; operate only through fixed workflow in core | Learners can decline complexity without being forced to build it. |

## 4. The ideal, characterized

### Normal conditions

The learner encounters a preflighted workspace, chooses a bounded low-risk task, states what AI should and should not do, and produces a useful artifact within 60 minutes. The course then moves from guided inspection to independent direction, source verification, reusable controls, fault recovery, safe tool connection, a fixed workflow, controlled change evaluation, and transfer. Every module ends with one performance claim and one evidence bundle.

### Edge conditions

- If the learner's own work is unsuitable, private, too consequential, or too sparse, a domain-neutral authentic case supports the competency while the transfer claim remains bounded.
- If a protected check is disputed, the module stops at `HOLD`; the learner does not rewrite the oracle.
- If the learner cannot use a native interface accessibly, an equivalent text/raw-state path tied to the same mechanism carries the proof.
- If a learner already demonstrates an objective on a protected novel case, the module can be tested out without waiving the evidence standard.
- If a failure is outside learner authority, correct localization plus a named handoff is credited separately from repair.

### Adversarial conditions

The core includes safe tests for instruction-like untrusted content, misleading or irrelevant sources, a polished unsupported answer, attempted check tampering, excessive tool authority, malformed input, a changed rule with unintended blast radius, and an instructor-planted hidden fault. The learner must refuse, hold, contain, or recover without widening authority or weakening acceptance.

### Degraded conditions

If the network, model, tool, source, check, or instructor fixture is unavailable, the learner preserves the last trustworthy state, identifies the missing dependency, and records a bounded `HOLD`. Simulated behavior is labeled simulated and cannot satisfy an executed-operation objective. The course can continue on unaffected objectives; it does not silently convert discussion into performance evidence.

### 10x load or scale

At 200 learners instead of 20, the objectives, artifacts, protected checks, and rubrics remain unchanged. Mechanically decidable checks run without per-learner reinterpretation; human judges score only named judgment fields. Cohort scale may increase staff or elapsed grading time, but may not weaken hidden-case custody, transfer scoring, or evidence ownership. A skeleton that requires bespoke instructor interpretation for every field fails this condition.

### Numerical budgets

| Budget | Reference value | Status |
|---|---:|---|
| Facilitated core | 30 hours; permissible 24–35 | Assumption and oracle bound |
| Active practice | ≥18 of 30 hours (≥60%) | Oracle bound |
| First useful artifact | ≤60 minutes | Oracle bound |
| Core module count | ≤10 | Oracle bound |
| Primary objectives | Exactly 1 per module | Oracle bound |
| Enabling objectives | ≤3 per module | Oracle bound |
| Common work surfaces | ≥3: research/source work, communication artifact, structured-data/batch work | Oracle bound |
| Independent evidence on material release | 100% | Invariant |
| Unsupported falsifier released | 0 | Invariant |
| Core programming requirement | 0 objectives | Invariant |
| Required full operation of persistent state, adaptive loops, or multi-agent systems | 0 core objectives | Invariant |
| External variable spend | ≤US$40/learner | Planning guess |
| Human judge time | ≤15 min/learner/module gate | Planning guess |
| Broken prerequisite or relative links | 0 | Oracle bound |
| Program objectives without practice and evidence | 0 | Oracle bound |

### Encountering the ideal

In the first ten seconds, a learner sees the real work product they will make, the decision it serves, and the first safe action. They do not see an architecture taxonomy, compliance disclaimer, installation sequence, or evidence bureaucracy as the opening experience.

After the course, they stop having to remember what happened in a chat, guess whether an output is good, grant broad tool access “just in case,” patch individual records, or explain an operating method live to every recipient. The saved artifact, check, boundary, recovery path, and handoff carry that load.

## 5. The off-axis frontier

| Rank | Approach | Mechanism | What it buys | What it costs | Becomes right when |
|---:|---|---|---|---|---|
| **1** | **Common core plus operator qualifications** | Aviation type-rating analogy: all learners qualify on shared professional operations; persistent state, adaptive control, and multi-agent work become separate role-triggered ratings. | Preserves the harness-operator identity, keeps the common core nondeveloper-accessible, and prevents machinery from becoming an attendance tax. | Requires honest credential boundaries and may reduce the apparent size of the core. | The audience contains both ordinary AI power users and people who will operate agentic systems. |
| **2** | **Scenario spiral** | One recurring work product passes through framing, source checks, tools, workflow, change, recovery, and transfer instead of using one scenario per concept. | Low orientation cost, visible cumulative value, fewer artifacts. | Scenario-specific blind spots and less evidence of transfer until the end. | The cohort shares a domain or one scenario can represent its work credibly. |
| **3** | **Competency stations** | Healthcare OSCE analogy: short standardized stations test delegation, verification, tool approval, diagnosis, workflow change, and handoff independently. | Strong comparability, test-out support, and 10x grading scalability. | Can feel fragmented and may reward station tactics over sustained operation. | Certification reliability and heterogeneous prior experience dominate. |
| **4** | **Apprenticeship studio** | Learners bring one real workflow and improve it under expert critique over several cycles. | Maximum authenticity and workplace transfer. | High instructor load, privacy complications, weak cross-learner comparability. | Cohorts are small, trusted, and have mature real work available. |
| **5** | **Managed-product playbooks — dissolve the problem** | The organization provides locked, role-specific assistants and fixed workflows; users learn only task selection, review, escalation, and approved use. | Eliminates most harness configuration, tool-boundary, and recovery burden. | Low portability and little ability to diagnose or adapt when the managed product changes. | Roles are narrow, systems are centrally governed, and local method construction is not expected. |
| **6** | **Governance-first certification** | Teach policy, risk classification, documentation, and approval before practical operation. | Fast organizational coverage and audit readiness. | Delays value and can create policy fluency without operating competence. | The role is assurance, procurement, audit, or oversight rather than AI-assisted production. |

Ranking defense: the common-core/type-rating model best fits the mixed nondeveloper audience and preserves the distinctive operator mechanisms. The scenario spiral is the best delivery form when domain alignment is strong. Competency stations are strongest for certification scale. Apprenticeship is strongest for transfer but violates the Scout budget at ordinary cohort sizes. Managed playbooks are the correct dissolution when the organization intentionally removes local harness design. Governance-first is valid for a different role.

## 6. The acceptance oracle

The following criteria are immutable for the Gauntlet implementation.

| ID | Criterion | Check method | Passing observation |
|---|---|---|---|
| **O01** | Bounded identity and audience | Static test of README and course map; human scope judge | Core identifies professional domain users/nondevelopers and distinguishes AI user, harness operator, and builder responsibilities. |
| **O02** | Research-grounded foundation | Named human judge checks Reference survey against linked official sources | At least six current primary exemplars cover workplace fluency, agent-builder training, and governance/competency frameworks; uncertainties are labeled. |
| **O03** | Complete program outcomes | Static test of `LEARNING_OBJECTIVES.md`; curriculum judge rubric | Outcomes cover foundations/limits, delegation, direction, source verification, discernment, workplace artifacts, responsible release, harness controls, workflow/recovery, evaluation/transfer. Every outcome names observable performance evidence. |
| **O04** | Parsimonious sequence | Static test of course map and module manifests | Ten or fewer core modules; exactly one primary outcome and at most three enabling objectives per module; no duplicate primary owner. |
| **O05** | Practical time budget | Static arithmetic from module manifests | Total facilitated time is 24–35 hours; practice is at least 60%; first useful artifact is explicitly due within 60 minutes. |
| **O06** | Early value | Static and human check of Module 00 | Module 00 starts from a preflighted environment, includes use/delegate/refuse judgment, produces a useful artifact, and checks at least one material claim before setup/governance depth. |
| **O07** | Common workplace breadth | Static coverage ledger and human check | Every learner encounters research/source work, a communication artifact, and structured-data or batch work, each with a named artifact and check. |
| **O08** | Performance progression | Static sequence tags and human rubric | Course explicitly progresses Guided → Independent → Adversarial/changed conditions → Transferred; discussion or file presence cannot satisfy operation. |
| **O09** | Responsible release | Static objective scan plus human rubric | Core requires applicable decisions for privacy/security, IP/copyright, fairness/bias, transparency/disclosure, affected-person impact, and human accountability. |
| **O10** | Signature harness controls | Static objective/map scan | Core assesses direction, context/source boundaries, independent checks, tool authority, one saved fixed workflow, evidence-preserving diagnosis/recovery, change evaluation, and handoff. |
| **O11** | Nondeveloper core boundary | Static test and curriculum judge | No core objective requires code authorship, API/MCP implementation, RAG pipeline construction, persistent-state runtime design, adaptive-loop operation, multi-agent orchestration, or deployment engineering. Selection and escalation may be core. |
| **O12** | Complexity is earned | Static test of scope statements | Fixed workflow is the highest machinery every learner must operate. Persistent state, adaptive flow, and multi-agent operation are explicitly outside core completion. |
| **O13** | Evidence and recovery | Static module-contract test | Every module names practical work, performance evidence, failure/hold behavior, scope boundary, and handoff. Every material release uses independent/protected evidence. |
| **O14** | Transfer | Static capstone test and named recipient rubric | Capstone separately tests a clean-session rerun and an independent person's use of the saved package; one cannot substitute for the other. |
| **O15** | Record burden | Static scan of requirements | One evidence bundle per module; no required per-module Brier score, accumulated calibration series, duplicate ladder, or multiple competing operating cycles. |
| **O16** | Skeleton parsimony | Line-count and artifact-manifest test | Authoritative core module skeleton totals ≤900 lines; each module ≤110 lines; every authoritative file declares the oracle criteria it serves. |
| **O17** | Internal integrity | Link/prerequisite/ID static tests | Zero broken relative links; core IDs, prerequisites, titles, outcome owners, durations, and transfer gates agree across authoritative files. |
| **O18** | Degraded and 10x behavior | Human judge using stated rubric | Skeleton preserves claim labels under unavailable fixtures/simulation and supports 200 learners without changing objectives, checks, rubrics, or hidden-case rules. |
| **O19** | Cost and grading budgets | Static declaration plus implementation-plan judge | Core declares ≤US$40 variable spend/learner and ≤15 minutes human scoring/learner/module gate as implementation budgets; missing budget is a failure, not permission to ignore cost. |

### Named human-judge rubrics

**Curriculum judge:** an experienced workforce educator or AI enablement lead who did not author the skeleton. Score each semantic criterion `0 absent / 1 present but vague / 2 observable and bounded`. Every applicable row must score 2.

**Scope judge:** a reviewer receives only the authoritative core files and lists every required learner action. Pass when no action is implementation-detail work and none crosses O11–O12.

**Recipient judge:** a person who did not observe the capstone build uses a protected rubric to score purpose/bounds, operation, evidence interpretation, stop/restore, and next-owner handoff. All five fields must pass on the preserved first attempt.

**Scale/degradation judge:** a delivery lead traces one normal cohort and a 200-learner cohort, then injects missing model, missing fixture, and inaccessible native UI cases. Pass when objectives and claim labels remain unchanged and each missing dependency produces a bounded alternate path or `HOLD`.

### Absolute failure conditions

An implementation is not the ideal if any one occurs, even if every other criterion passes:

1. The first useful AI-assisted artifact is scheduled after 60 minutes.
2. Core completion requires programming or custom agent-runtime implementation.
3. Every learner must operate persistent state, adaptive loops, or multi-agent orchestration.
4. A material artifact can be released using only producer self-assessment.
5. Privacy/security is present but IP, fairness, transparency, affected-person impact, or accountability is absent from release judgment.
6. The core exceeds 10 modules or 35 facilitated hours.
7. Any program objective lacks both practical work and performance evidence.
8. A simulation is recorded as executed operation.
9. Clean-session restartability substitutes for independent-person transfer.
10. The implementation changes this Reference to match what was built.

## 7. Anti-goals

Excellence here does not include:

- model training, fine-tuning, ML theory, or benchmark engineering;
- API, MCP server, connector, retrieval-pipeline, database, or agent-runtime implementation;
- full persistent-state, adaptive-loop, or multi-agent operation in common core;
- product tours or exhaustive feature catalogs;
- separate modules for every work application;
- detailed adapter commands, lesson scripts, instructor fault packs, or protected fixtures;
- a universal legal-compliance claim;
- a statistically stable personal calibration score from a bootcamp-sized series;
- ten-case diagnostic mastery claims;
- multiple evidence ladders, named operating cycles, or duplicate record systems;
- duration inflation to preserve already-written material;
- advanced content retained merely because it is technically good;
- generality for hypothetical industries, products, or future agent architectures without a current core objective.

## 8. Obsolescence

This Reference becomes wrong if, within 18 months, one of the following changes the work boundary:

1. Managed workplace AI products make protected checks, provenance, permissions, rollback, and transfer packages automatic and reliably inspectable, dissolving much of the harness-operator role.
2. Persistent state or bounded agent operation becomes a universal baseline professional interaction rather than an advanced role, supported by audited managed controls rather than local system design.
3. Regulation requires a different mandatory literacy or oversight curriculum for the target population.
4. Credible workplace evidence shows that fixed-workflow operation no longer predicts safe or effective use of contemporary AI systems.
5. Learner pilots show that the assumed 30-hour/nondeveloper profile cannot reach independent operation even with accessible managed adapters.

Earliest signals:

- major workplace suites expose standardized evidence, authority, and rollback receipts by default;
- foundational nontechnical certificates begin requiring persistent-state and multi-agent performance rather than awareness;
- EU or U.S. guidance publishes role-specific mandatory learning outcomes that conflict with this oracle;
- two consecutive pilots miss the 60-minute first-value or 60% practice budgets;
- scope judges repeatedly classify core work as solution-architect or developer work.

Review those signals quarterly. Do not revise this frozen Reference during the Gauntlet; create a successor Reference when a trigger fires.
