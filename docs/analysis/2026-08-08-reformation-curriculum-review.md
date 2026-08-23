# Reformation Curriculum Review

**Review target:** `reformation/` (23 files, 2,807 lines, modules 00–09)
**Reviewed:** 2026-08-08
**Method:** full read of `reformation/`; 10 parallel external research sweeps (187 unique sources); three independent competency models derived from the research by drafters who were never shown the module list; comparison performed only after the independent models were written.
**Repository changes:** this document only.

---

## 1. Executive verdict

**Scope.** Correctly scoped in subject, over-scoped in volume, and under-scoped on the three or four things that matter most. The competency set is the right *kind* of thing — durable mechanisms, not vendor syntax. But nine modules at 60–180 minutes each cannot carry ten independent objectives apiece. Three independent competency models, derived separately from current research, each landed on 36–40 hours plus an 8–10 hour capstone for a **narrower** set of skills than `reformation/` attempts in 18–26 hours. The course is trying to cover roughly twice the ground in roughly half the time.

**Strongest design choice.** The separation of competency / method / evidence from scenario / implementation ([`AUTHORING_GUIDE.md:13-20`](../../reformation/AUTHORING_GUIDE.md)), enforced by an evidence ladder that tops out at *"learner states the boundary of the evidence"* ([`COURSE_MAP.md:62-70`](../../reformation/COURSE_MAP.md)). Paired with `HOLD` as a passing state and the bounded-containment rule at [`06-durable-state.md:116`](../../reformation/modules/06-durable-state.md), this is a stronger evidence standard than any comparable curriculum found in the research. It should survive any rewrite untouched.

**Largest structural weakness.** The course teaches the learner to check *one artifact at a time* and never to look at *many runs at once*. There is no error analysis — no sampling of the learner's own runs, no first-failure annotation, no counted failure taxonomy, no ranking. Current practice calls this the single highest-yield evaluation activity and the most transferable one for a non-developer; all three independent models made it core at 2.5–3.5 hours. `reformation/` contains none of it. Because the failure taxonomy is what tells an operator *which* check to build, its absence makes every downstream checking exercise a guess about which failures matter.

**Three highest-priority changes.**

1. **Add error analysis as its own module** (P0). Sample your own runs, annotate the first failure in each, group, count, rank, convert the top-ranked failure into a mechanical check. This is the missing spine.
2. **Add a calibration measurement in Module 00** (P0). Predict, then measure, your own performance change on your own real task, scored on the size of the prediction gap rather than the direction. The perception–performance gap in AI-assisted work runs 30–40 points in the confident direction, and the course currently has no instrument for it. The legacy course had one and it was dropped.
3. **Make diagnosis a test, not a rehearsal** (P1). Every module has the learner plant their own failure, so they always know the answer. Grade first-divergence localization on faults the learner did **not** plant, in a harness they did **not** build, interleaved by fault class.

**What should not change.** The adapter separation rule. `HOLD` as a supported result. "Model self-assessment is not proof." The loaded / triggered / executed / bypassed diagnosis. The discriminating-probe test. The baseline-before-measures ordering in Module 05. The bounded-claim discipline. Module 01's worked-example-then-inspect design. Module 09's explicit refusal to accept a fresh session as person-transfer.

---

## 2. Audience and bootcamp level

### Inferred learner profile

The stated profile holds and the curriculum is internally consistent with it: *"You do not need to be a software developer"* ([`README.md:70`](../../reformation/README.md)). Capability requirements are stated as capabilities rather than products ([`README.md:72-81`](../../reformation/README.md)). One correction is warranted.

**The profile is not honoured in two modules.** Module 03 requires the learner to *"Build one deterministic guard … through a pre-action check, post-action check, outer workflow step, schema validator, or equivalent mechanism"* ([`03-control-layers.md:60-62`](../../reformation/modules/03-control-layers.md)). Module 04 requires them to *"expose or configure one small read-only capability of your own"* and to *"call or exercise it through the smallest available client"* ([`04-tool-boundaries.md:6,70`](../../reformation/modules/04-tool-boundaries.md)). For a non-developer both are code. The core says adapters must supply it ([`README.md:70`](../../reformation/README.md)), but never says *what* supplying it means — a fill-in-the-blank template, a pre-built component the learner only configures, or a facilitator writing it live. Those three produce very different competencies, and the skeleton does not choose.

This is the review's central adapter finding, and it matters more than usual because you are building a fresh implementation from this skeleton: **an under-specified adapter obligation is where a mechanism silently disappears.**

### Prerequisites

Correctly minimal and correctly stated as capability rather than brand. One prerequisite is assumed but never stated: the learner needs **a real recurring task of their own**. Modules 02, 03, 05, 06, and 07 all say "choose the work," and the research is unambiguous that far transfer does not happen — practice must run in the learner's own domain. Make this an admission requirement, not a module-time scramble.

### End-state capability

The eight-item end state ([`README.md:109-118`](../../reformation/README.md)) is well-formed and each item is observable. Two items in the independent models have no counterpart: the learner cannot state *what their own estimation error is*, and cannot state *which failures their harness actually produces, ranked by count*.

### Assumptions retained

- Delivery is facilitated or adapter-supported, not self-serve. Modules 01, 03, 04, 05, 07 do not stand alone ([`README.md:19`](../../reformation/README.md)).
- "Consequential" means real work with a real audience, but low-risk and reversible ([`09-capstone.md:20`](../../reformation/modules/09-capstone.md)).
- The learner will operate an existing harness, not build one.

### Uncertainties

- Cohort delivery vs. self-paced changes the answer on module sizing considerably. The research favours fixed-standard / variable-time; `reformation/`'s `HOLD`-and-continue rule ([`README.md:47-53`](../../reformation/README.md)) is a partial and rather good approximation of that, but it fights the per-module time boxes.
- Whether learners arrive with one harness in common or several. The port exercise (A5 below) is only affordable if they share one.

---

## 3. Research method and sources

### Searches performed

Ten parallel research sweeps, each running 6–10 distinct web searches plus direct fetches of primary sources, across: operator competency frameworks and comparable curricula; context and specification practice; evaluation and evidence practice; security, prompt injection and data boundaries; agent architecture and multi-agent evidence; model selection, cost and fine-tuning; tool and protocol interfaces; retrieval and durable state; observability and debugging; learning science and bootcamp failure modes. 435 tool calls total.

### Source-selection method

Sources were prioritised when they explained a **mechanism**, reported an **observed failure mode**, or defined a **measurable practice**. Feature descriptions and marketing claims were excluded. Vendor documentation was accepted as evidence of *how a mechanism works* and explicitly rejected as evidence that a vendor feature belongs in a durable core; vendor interest is recorded in the limitation column. Older sources were retained where they define an established standard or a durable mechanism (Kalyuga & Renkl 2009; Macnamara 2014; Michaeli & Romeike 2019; Deslauriers 2019).

### Evidence hierarchy applied

1. Controlled studies with stated N and design (METR; Deslauriers; Loibl & Leuders; Barbieri; Michaeli & Romeike; Chroma; ConstraintRot; Gloaguen et al.).
2. Large-scale field telemetry with disclosed methodology (20,574-session misalignment study; Anthropic Claude Code expertise study; MAST 1,642 traces).
3. Standards and specifications (MCP spec; OWASP GenAI project).
4. Vendor engineering write-ups explaining mechanism (Anthropic engineering posts; OpenAI agent guide).
5. Credible practitioner material with named authors (Husain; Shankar; Willison; Cognition).
6. Secondary commentary — used only for direction, never for numbers.

Where a widely circulated statistic could not be traced to a primary study, it was retained as *direction* and flagged as untraceable. Where two credible sources conflicted (multi-agent value; RAG-vs-long-context), both were carried into the model and the disagreement is stated rather than resolved.

### Source table

187 unique sources were collected. The table below lists those that support a specific claim made in this review.

| Title | Publisher / author | URL | Date | Accessed | Claim supported | Limitation |
|---|---|---|---|---|---|---|
| Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity | METR | https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ | 2025-07-10 (Feb 2026 follow-up) | 2026-08-08 | Perception–performance gap: 19% slower while believing 20% faster | Small N (16), one domain; the same group's 2026 follow-up points the other way. Teach the method, not the number |
| How to Assess AI Literacy: Misalignment Between Self-Reported and Objective-Based Measures | Zhang et al., LAK 2026 | https://arxiv.org/pdf/2601.06101 | 2026-01-13 | 2026-08-08 | Self-reported AI competence is misaligned with objective competence | Education population, not workplace operators |
| Measuring actual learning versus feeling of learning… | Deslauriers et al., PNAS | https://www.pnas.org/doi/10.1073/pnas.1821936116 | 2019-09-24 | 2026-08-08 | Active learning outperforms while being rated lower by learners | Physics undergraduates; generalisation to adult professionals assumed |
| Can failure be made productive also in Bayesian reasoning? | Loibl & Leuders, Instructional Science | https://phfr.bsz-bw.de/frontdoor/deliver/index/docId/3543/file/11251_2024_Article_9670.pdf | 2024-07-12 | 2026-08-08 | Productive failure produced **no** main effect (N=75, 2×2); conditions matter more than the format | Conceptual replication in one domain |
| Exploring Barriers in Productive Failure | ICER 2023 | https://dl.acm.org/doi/10.1145/3568813.3600111 | 2023-08 | 2026-08-08 | Productive failure did not improve transfer in a post-secondary computing course | Quasi-experiment, single course |
| When Problem Solving Followed by Instruction Works | Sinha & Kapur, Review of Educational Research | https://journals.sagepub.com/doi/10.3102/00346543211019105 | 2021-10 | 2026-08-08 | Productive failure g = 0.36, reversing for domain-general skills | Meta-analysis heterogeneity; reversal condition is the load-bearing part here |
| A Meta-analysis of the Worked Examples Effect | Barbieri et al., Educational Psychology Review | https://link.springer.com/article/10.1007/s10648-023-09745-1 | 2023-01-30 | 2026-08-08 | Worked examples g = 0.48; faded steps strongest; **correct** examples beat incorrect | Mathematics domain |
| Expertise reversal effect and its instructional implications | Kalyuga & Renkl, Instructional Science | https://link.springer.com/article/10.1007/s11251-009-9102-0 | 2009 | 2026-08-08 | Guidance that helps novices harms learners with prior knowledge | Older; mechanism is durable |
| Deliberate Practice and Performance… A Meta-Analysis | Macnamara et al., Psychological Science | https://gwern.net/doc/psychology/2014-macnamara.pdf | 2014 | 2026-08-08 | Practice hours explain <1% of variance in professions | Contested effect sizes; direction is robust |
| Simulation-based mastery learning with translational outcomes | McGaghie et al. | https://journalofexpertise.org/articles/volume4_issue2/JoE_4_2_McGaghie_etal.pdf | 2019 | 2026-08-08 | Fixed standard / variable time outperforms time-based curricula | Medical education; transfer to operator training assumed |
| Beware of metacognitive laziness | Fan et al., BJET | https://bera-journals.onlinelibrary.wiley.com/doi/abs/10.1111/bjet.13544 | 2024-12 | 2026-08-08 | AI assistance improved the artifact but produced no knowledge gain or transfer; checklist group engaged most | Essay-writing task; N=117 |
| Navigating the Jagged Technological Frontier | Dell'Acqua et al., HBS/BCG → Organization Science | https://mitsloan.mit.edu/sites/default/files/2023-10/SSRN-id4573321.pdf | 2023-09 / 2025 | 2026-08-08 | Inside the frontier +12.2% tasks; outside it, 19% less likely to be correct | Consultants, 2023 model generation |
| Improving Debugging Skills in the Classroom | Michaeli & Romeike, WiPSCE '19 | https://computingeducation.de/pub/2019_Michaeli-Romeike_WIPSCE19.pdf | 2019-10-23 | 2026-08-08 | Teaching a **named** systematic debugging procedure: d = 0.69 vs. equal-time extra practice | Small N (13/15); school-age |
| Explicitly Teaching Debugging in Primary School: Effectiveness, Transferability and Durability | Koli Calling '25 | https://dl.acm.org/doi/10.1145/3769994.3769999 | 2025 | 2026-08-08 | Procedure transfers and lasts ~10 weeks, but only where the underlying system is understood | Primary school |
| Theory of Troubleshooting | Starr & Storey | https://arxiv.org/pdf/2602.10540 | 2026-02-16 | 2026-08-08 | Experts start from an expectation model, not a hypothesis; cognitive fatigue degrades diagnosis | Grounded theory, 27 professionals |
| How Coding Agents Fail Their Users: 20,574 Real-World Sessions | Notre Dame / Vanderbilt / Google | https://arxiv.org/pdf/2605.29442 | 2026-05-28 | 2026-08-08 | Constraint violation 38.3%, misread intent 27.0%, inaccurate self-reporting 22.6%, faulty implementation 17.8%; context loss only 4.3%; only 2.99% agent self-corrected | Coding agents specifically |
| Model or Harness? An Interaction-Centric Taxonomy | Scale AI | https://arxiv.org/html/2607.28802 | 2026-07-30 | 2026-08-08 | Blame attribution depends on the counterfactual chosen | Vendor research; explicit attribution principle stated |
| Why Do Multi-Agent LLM Systems Fail? (MAST) | Cemri et al., UC Berkeley | https://arxiv.org/abs/2503.13657 | 2025-03-17 (rev. 2025-10-26) | 2026-08-08 | 1,642 traces, 7 frameworks; 41–86.7% failure; design 41.8% / misalignment 36.9% / verification 21.3% | Frameworks of that period |
| The Illusion of Multi-Agent Advantage | Jwalapuram et al. | https://arxiv.org/html/2606.13003v1 | 2026-06 | 2026-08-08 | Under matched budgets, most multi-agent advantage disappears; automated designs degenerate into ensembles | Specific task families |
| Single-Agent LLMs Outperform Multi-Agent Systems Under Equal Thinking Token Budgets | Tran & Kiela, Stanford | https://arxiv.org/abs/2604.02460 | 2026-04-02 | 2026-08-08 | Budget-matched comparison as the standard of proof | Multi-hop reasoning only |
| How we built our multi-agent research system | Anthropic | https://www.anthropic.com/engineering/multi-agent-research-system | 2025-06-13 | 2026-08-08 | Multi-agent wins on breadth-first search; ~15x token cost; spend explains most of the gain | Vendor with an interest in the pattern; states the cost honestly |
| Don't Build Multi-Agents | Cognition | https://cognition.com/blog/dont-build-multi-agents | 2025-06-12 | 2026-08-08 | Parallel subagents making dependent decisions produce conflicting output | Vendor position piece; the read/write asymmetry is agreed by both sides |
| When to use multi-agent systems (and when not to) | Anthropic | https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them | 2026-01-23 | 2026-08-08 | Read work parallelises, write work does not; one writer per artifact | Vendor |
| A practical guide to building agents | OpenAI | https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf | 2025-04 | 2026-08-08 | Exhaust single-agent options first; control-flow ownership is the root decision | Vendor |
| Context Rot: How Increasing Input Tokens Impacts LLM Performance | Chroma | https://www.trychroma.com/research/context-rot | 2025-07-14 | 2026-08-08 | All 18 frontier models degrade as input length grows at constant task difficulty | Vendor sells retrieval; method is disclosed and the direction is corroborated |
| Diagnosing and Mitigating Context Rot in Long-horizon Search | Xia et al. | https://arxiv.org/abs/2606.29718 | 2026-06-29 (rev. 2026-08-04) | 2026-08-08 | Long-context failure presents as **premature termination** — the agent gives up | Search benchmarks |
| Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents? | Gloaguen et al., ETH Zurich SRI | https://arxiv.org/html/2602.11988v1 | 2026-02-12 | 2026-08-08 | Generated instruction files reduced success 0.5–2% at +20–23% cost; repository overviews measurably worthless | Coding agents; SWE-bench Lite + AGENTbench |
| Curse of Instructions (ManyIFEval) | Harada et al. | https://openreview.net/forum?id=R6q67CDBCH | 2025 | 2026-08-08 | Joint compliance falls roughly geometrically in the number of stacked constraints | Benchmark setting |
| Effective context engineering for AI agents | Anthropic | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | 2025-09-29 | 2026-08-08 | Context as a finite attention budget; compaction, note-taking, just-in-time retrieval, sub-agent isolation | Vendor |
| Best practices for Claude Code | Anthropic | https://code.claude.com/docs/en/best-practices | continuously updated | 2026-08-08 | The agent stops when work "looks done" absent a runnable check; a gap-hunting reviewer manufactures findings | Vendor, product-specific |
| How Claude remembers your project | Anthropic | https://code.claude.com/docs/en/memory | undated | 2026-08-08 | Instruction files are delivered as context with "no guarantee of strict compliance"; blocking requires a hook | Vendor, product-specific; the advice/enforcement split is the durable part |
| LLM Evals: Everything You Need to Know (Evals FAQ) | Hamel Husain | https://hamel.dev/blog/posts/evals-faq/ | 2025-05-28 (upd. 2026-07-18) | 2026-08-08 | Error analysis is the highest-yield activity; ~100 traces/cycle; saturation at ~20; binary over Likert; single expert owner; 60–80% of effort | Practitioner; sells a course on the method |
| Who Validates the Validators? | Shankar et al., UIST 2024 | https://arxiv.org/abs/2404.12272 | 2024-04-18 | 2026-08-08 | Criteria drift: grading outputs is what reveals the criteria | N=9 professionals |
| Quantifying and Mitigating Self-Preference Bias of LLM Judges | — | https://arxiv.org/html/2604.22891v2 | 2026-04 | 2026-08-08 | Models favour their own output; bias persists under anonymisation and grows with capability | Benchmark-based |
| How Claude Code is used in practice | Anthropic | https://www.anthropic.com/research/claude-code-expertise | 2026 (Oct 2025–Apr 2026) | 2026-08-08 | Domain expertise, not coding skill, predicts success; novice abandonment 19% vs 5–7% | Vendor telemetry, one product |
| Anthropic Economic Index: Cadences | Anthropic | https://www.anthropic.com/research/economic-index-june-2026-report | 2026-06-26 | 2026-08-08 | Median chat session 13 turns vs. a single prompt for the same output agentically | Vendor telemetry |
| How We Broke Top AI Agent Benchmarks | UC Berkeley RDI | https://rdi.berkeley.edu/blog/trustworthy-benchmarks-cont/ | 2026-04 | 2026-08-08 | An exploit agent scored ~100% on eight major agent benchmarks while solving zero tasks | Demonstrates the exploit, not typical practice |
| The lethal trifecta for AI agents | Simon Willison | https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ | 2025-06-16 | 2026-08-08 | Private data + untrusted content + external communication as the exfiltration condition | Practitioner framing, widely adopted |
| OWASP GenAI LLM Top 10 2026 | OWASP Gen AI Security Project | https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/ | 2026-08-03 | 2026-08-08 | Prompt injection #1 for a third consecutive edition; Excessive Agency to #3 on incident data | Consensus list; identifiers churn between editions |
| OWASP Top 10 for Agentic Applications 2026 | OWASP Gen AI Security Project | https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ | 2025-12-09 | 2026-08-08 | Prompt injection maps to six of ten agentic categories | As above |
| The Attacker Moves Second | Nasr, Carlini, Tramèr et al. | https://arxiv.org/abs/2510.09023 | 2025-10-10 | 2026-08-08 | Defenses reporting near-zero attack success are bypassed >90% by adaptive attackers | Research setting |
| MCP Security Notification: Tool Poisoning Attacks | Invariant Labs | https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks | 2025-04-01 | 2026-08-08 | Tool descriptions are model-visible and largely user-invisible; rug-pull class | Vendor sells guardrails |
| RCE and API Token Exfiltration Through Claude Code Project Files | Check Point Research | https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/ | 2026-02-25 | 2026-08-08 | Harness configuration files are executable content; opening an untrusted repo can exfiltrate a key before any prompt | Specific CVEs, one product; the class is general |
| Approval fatigue is agent governance's next attack surface | WorkOS | https://workos.com/blog/approval-fatigue-agent-governance | 2026 | 2026-08-08 | ~93% of permission prompts approved; ~1 in 3 dangerous commands slips through; diligence decays with volume | Vendor; figures partly product telemetry |
| Security Best Practices — MCP Specification 2026-07-28 | Model Context Protocol | https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices | 2026-07-28 | 2026-08-08 | Authority lives in the credential; token passthrough forbidden; progressive least privilege | Standard |
| Versioning — Model Context Protocol | MCP / Linux Foundation | https://modelcontextprotocol.io/specification/versioning | current | 2026-08-08 | Version string is the date of the last breaking change; roughly annual breaking revisions | Standard |
| Tools — MCP Specification 2026-07-28 | Model Context Protocol | https://modelcontextprotocol.io/specification/2026-07-28/server/tools | 2026-07-28 | 2026-08-08 | tools = model-controlled, resources = application-controlled, prompts = user-controlled | Standard |
| Writing effective tools for AI agents | Anthropic | https://www.anthropic.com/engineering/writing-tools-for-agents | 2025-09-11 | 2026-08-08 | Description refinement moved accuracy ~60%→75% (Slack) and ~55%→70% (Asana); bounded output as a contract term | Vendor internal evals |
| Introducing advanced tool use | Anthropic | https://www.anthropic.com/engineering/advanced-tool-use | 2025-11-24 | 2026-08-08 | Deferred tool loading gains **and** the conditions under which it hurts | Vendor feature promotion; the "when it hurts" conditions are the useful part |
| Temporal Validity in Retrieval Memory (MemStrata) | — | https://arxiv.org/html/2606.26511v1 | 2026-06-25 | 2026-08-08 | Embedding similarity cannot separate contradiction from duplicate (AUROC 0.59); deterministic (subject, relation) supersession cuts stale-fact error to ~0% | Specific corpora |
| From Untrusted Input to Trusted Memory | — | https://arxiv.org/html/2606.04329v1 | 2026-06-03 | 2026-08-08 | Four memory write channels including compaction and experience-synthesis; 34–67% attack success; detector ceiling too low to rely on | Research setting |
| Effective harnesses for long-running agents | Anthropic | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | 2025-11-26 | 2026-08-08 | Initializer session, progress log, explicit pass/fail checklist, nothing complete until verified end-to-end | Vendor |
| When Routing Collapses | — | https://arxiv.org/html/2602.03478v1 | 2026-02 | 2026-08-08 | Trained routers collapse to the strongest model; escalation ladder is durable, the router is not | Benchmark |
| Does Thinking More always Help? | NeurIPS 2025 | https://arxiv.org/abs/2506.04210 | 2025-06-04 (rev. 2025-10-23) | 2026-08-08 | Extended reasoning shows a rise-then-decline curve | Reasoning benchmarks |
| AI Coding Cost Analysis | Augment Code | https://www.augmentcode.com/guides/ai-coding-cost-analysis-agent-token-spend | 2026-07-24 | 2026-08-08 | Input tokens >99% of agentic spend; loop shape is the cost lever | Vendor; one workload class |
| AI-generated 'Workslop' Is Destroying Productivity | HBR / BetterUp Labs + Stanford SML | https://hbr.org/2025/09/ai-generated-workslop-is-destroying-productivity | 2025-09 | 2026-08-08 | 41% received unverified AI output; ~1h56m to resolve each; 42% trusted the sender less | Survey, self-report |
| Balancing AI tensions / DORA State of AI-assisted Software Development | DORA / Google Cloud | https://dora.dev/insights/balancing-ai-tensions/ | 2026-03-10 (2025 data) | 2026-08-08 | AI amplifies the surrounding system: throughput and instability rise together | Software delivery context |
| AI Fluency: Framework & Foundations | Anthropic Academy | https://anthropic.skilljar.com/ai-fluency-framework-foundations | undated | 2026-08-08 | The best-known competency framework stops at the conversation boundary | Vendor; free course, CC BY-NC-SA |
| Agentic Engineering Patterns | Simon Willison | https://simonw.substack.com/p/agentic-engineering-patterns | 2026-02-23 | 2026-08-08 | Test-driven agent loops; agents optimising to pass tests do not build good abstractions | Practitioner |
| Gartner Predicts Over 40% of Agentic AI Projects Will Be Canceled | Gartner | https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027 | 2025-06-25 | 2026-08-08 | Cancellation driven by cost, unclear value, inadequate risk controls | Analyst prediction, not measurement — scale context only |
| MIT NANDA "GenAI Divide" (via Forbes) | MIT NANDA / Forbes | https://www.forbes.com/sites/jasonsnyder/2025/08/26/mit-finds-95-of-genai-pilots-fail-because-companies-avoid-friction/ | 2025-08-26 | 2026-08-08 | Failure concentrates at the workflow-integration layer, not the model | Headline figure widely contested — mechanism only |
| Coding bootcamp placement-rate reporting | TechCrunch / Yahoo Tech | https://tech.yahoo.com/business/articles/biggest-coding-bootcamps-may-exaggerate-170000563.html | 2022-02-04, ongoing | 2026-08-08 | Denominator manipulation inflates bootcamp outcome claims | Journalism; older |
| Is Grep All You Need? How Agent Harnesses Reshape Agentic Search | — | https://arxiv.org/html/2605.15184v1 | 2026-05-14 | 2026-08-08 | Harness and result-delivery format swing retrieval results more than the retrieval method | Verbatim-span conversational QA only; authors state the caveat |

Additional sources (127 not tabulated) informed the over-taught / durable classifications in §4 and are recorded in the research corpus.

---

## 4. Independent competency model

Derived from the research by three drafters working from different lenses (failure-first; job-task frequency; durability under rising capability), none of whom saw `reformation/`. Where all three converged, confidence is high and it is noted.

### Foundational — precedes everything; practised repeatedly

| # | Competency | Learner can do | Observable mastery evidence | Mode |
|---|---|---|---|---|
| F1 | **Map the harness you are actually using** | Produce a one-page map of the working environment *by inspection* — what supplies context at startup, who fires each capability, where state is written, what the enforcement plane is — with each claim traced to something observed, not to documentation | The map, spot-checked: given a rule they wrote, they can say within a minute whether it is advice or enforcement, and show where they verified it | Once, then referenced |
| F2 | **State the acceptance artifact and the falsifier before the run** *(all 3 lenses)* | Before issuing any instruction, write what artifact will exist if this succeeded, what observation would show it failed, and what would make them stop entirely | Timestamped pre-run statement naming a specific artifact (file, row count, diff, sent record) and a specific disconfirming observation, applicable by another person without asking the author | Repeatedly |
| F3 | **Predict, then measure, your own performance change** *(all 3 lenses)* | Predict the effect, do a representative real task once unassisted and once with the harness on the same items, compare against a rubric they did not write | Timestamped prediction + two matched runs + externally scored rubric. **Graded on the size of the prediction gap, not the direction of the result** | Once early, once at capstone |
| F4 | **State and reduce blast radius** *(all 3 lenses)* | Enumerate what the agent can read, what it can write, whose credential it acts under, which effects are reversible; then narrow until the worst single outcome is absorbable, and show the task still completes | Before/after configuration, a written worst-case statement, a passing run under the narrower bound. A run that fails after narrowing and is then repaired counts for more than one that never bound | Repeatedly |
| F5 | **Establish a restore point and recover from a bad run** | Checkpoint before any run that can write; on a damaged run, restore rather than repair forward; state in advance which effects fall outside the checkpoint | Demonstrated restore, plus a written list of effects the checkpoint does not cover (messages sent, external systems touched) | Repeatedly |

### Core — the spine, practised at increasing difficulty

| # | Competency | Learner can do | Observable mastery evidence | Mode |
|---|---|---|---|---|
| C1 | **Write a brief whose every requirement is checkable** | Convert a request normally issued over a dozen corrective turns into one brief naming the specific files and interfaces, stating what is out of scope, ending in a verification step the agent runs itself; count the constraints and split or declare precedence rather than stacking | The brief, a fresh-session transcript, and turns-to-acceptable measured against the learner's own earlier baseline on a comparable task | Repeatedly |
| C2 | **Verify against an artifact the agent did not produce** *(all 3 lenses)* | Given a confident completion summary, inspect the system of record first — query the data, read the diff, list the directory, open the sent folder | A record per task showing claim, independent artifact consulted, verdict. **At least one graded instance must be a run where the summary is fluent and the artifact disagrees, caught unprompted** | Repeatedly |
| C3 | **Supply a runnable check the working agent cannot author or edit** | Choose the rung by stakes — in-prompt check, session goal condition, deterministic gate, fresh-context reviewer scoped to correctness — and write it before the work | Three tasks at different stakes, check written first, raw pass/fail attached, rung justified; **plus one demonstrated case where the agent satisfied the letter of a check without doing the work** | Repeatedly |
| C4 | **Sort each requirement into advice / enforced gate / made-impossible — and prove it survives a context reset** *(all 3 lenses)* | Place preferences in instruction text, fixed-moment requirements in a runtime check, never-events behind an absent capability; then verify what loaded, run long enough to compact, and test whether the rule still holds | The three-way sort, a working gate for at least one, and **a matched pair of transcripts on the same rule — violated after a reset when it lived only in conversation, held when re-established from a durable source** | Repeatedly |
| C5 | **Localize a failed run to first divergence and name the layer** *(all 3 lenses; largest hour allocation in all three)* | In a harness they did not build, write what each step should have produced, walk backward to the earliest departure, halve the interval to narrow it, and classify the layer | **Graded on correct localization and layer naming, not on eventual repair**, across ≥4 planted faults of different classes, interleaved rather than blocked | Repeatedly |
| C6 | **Classify the fault cheapest-cause-first before searching** | Name the class before searching, working a fixed short list in order of cheapness and controllability: permission/configuration → capability contract → context/state → instruction adherence → model judgment last | The named class plus the distinguishing probe that separated it, on a fault type not seen since the previous week | Repeatedly |
| C7 | **Read your own runs, name the first failure in each, group, count, rank** *(all 3 lenses)* | Sample real runs, write free-form notes on the *first* failure only, group into categories derived after the fact, count, rank, stop at saturation; binary labels | A counted taxonomy from 20–40 of the learner's own runs with raw notes attached, categories visibly derived from notes rather than imported, and a rubric that visibly changed between the first and second twenty labels | Repeatedly |
| C8 | **Convert the top-ranked failure into a mechanical check** | Build something returning pass/fail without a human reading the output; exhaust mechanical options before reaching for a model-graded one | A runnable check demonstrated passing on good output and **failing on the actual bad output that motivated it**. An unvalidated check scores zero | Repeatedly |
| C9 | **Fix the durable artifact and prove non-recurrence in a fresh session** *(all 3 lenses)* | Identify which durable artifact must change, change it one at a time, revert failed attempts, then reproduce the original conditions with no prior conversation | Named changed artifact + clean fresh-session run of the original failing case. **Recurrence in a fresh session is the objective fail condition regardless of how well the session ended** | Repeatedly |
| C10 | **Inventory reach and cut one leg** *(all 3 lenses)* | Produce a three-column inventory for their own configuration — private data reachable, every point where content they did not write enters, every way bytes can leave including non-obvious channels — then remove one leg and prove it with a canary | The inventory, the configuration change, a working run afterwards, and a canary result: a dummy secret in reachable data plus a hidden instruction in a document the agent reads, demonstrating the secret did not leave. Re-run after any new capability is attached | Repeatedly |
| C11 | **Read the raw configuration and the raw capability description before approving** | Open project configuration files and the capability description *as the model will receive it* rather than the approval summary; verify the publisher; pin the version; set a re-review trigger; treat configuration as executable content | An attach-or-decline decision for two candidates with raw descriptions quoted, plus one instance of finding a planted instruction inside a tool description or project configuration file | Repeatedly |
| C12 | **Budget approvals** *(all 3 lenses)* | Rate each capability on read/write, reversibility, whose permission, cost of a wrong call; make dangerous actions structurally unavailable rather than merely gated; place few gates at irreversible edges, each showing the raw action | The rating table, the resulting configuration, a before/after approval count from a real session, and the learner's own observed approval rate | Once, reinforced |
| C13 | **Start at the least machinery and climb only on demonstrated failure** | State whether the sequence is known in advance; start at the lowest rung — one well-contexted call, fixed sequence with gates, one agent with an owned loop, more than one context — and produce a recorded failure of the rung below before adding machinery | The rung choice with justification, a recorded failing run at the rung below, the resulting successful run. Jumping straight to an agent loop without a failing simpler run does not demonstrate this | Repeatedly |
| C14 | **Hand off with the check and its raw output attached** | Send no deliverable without the acceptance condition, the check run against it, its raw output, and a plain statement of what was not verified | Three real handoffs in the form sent, assessed by a recipient who did not watch the work: can they tell what was verified without asking? | Repeatedly |
| C15 | **Cold-resume from what the last session wrote** | Write state files before the work — outcome checklist the agent marks but cannot self-certify, progress log, frequent restore points — then kill the session and resume from the files alone | A cold-resume run completing with no re-explanation. **State a fresh session cannot find and use is scored as not existing** | Repeatedly |

### Advanced but appropriate

| # | Competency | Evidence |
|---|---|---|
| A1 | **Repair wrong-capability selection by rewriting descriptions, then re-measure** | Fixture set of ~10 realistic tasks with expected outputs **authored before tuning**; before/after selection accuracy on the identical set; description diff. Distinguishes "never saw the right one" from "saw it and could not tell them apart" |
| A2 | **Operate a fixed production workflow through a rule change** | A batch run; one rule changed in one place; a side-by-side comparison naming exactly which records and fields moved; **zero row-by-row manual repair**; a second wave through the same saved artifact |
| A3 | **Govern durable state** | Admission policy; provenance on every claim; one current value per (thing, property) with the superseded version marked; integrity check that detects a planted mutation; cold retrieval passing |
| A4 | **Re-run your own held-back case set after a capability change** | A privately assembled case set the learner never tuned against; paired before/after on identical items across a real change; a written statement of what moved, what did not, and what they will stop relying on |
| A5 | **Port one working control to a second harness** | The same violation attempt blocked in both harnesses, with a written statement of what stayed the same (the mechanism) and what had to be relearned (the syntax) |

### Optional extension

| # | Competency | Why optional |
|---|---|---|
| O1 | **Divide work across contexts** | Real but narrow: read work parallelises, write work does not; one writer per shared artifact; **budget-matched comparison required as the standard of proof**. All three lenses tiered this optional or advanced at ~1h |
| O2 | **Operate an adaptive loop with persistent state through a changed world** | Genuinely valuable, but the rarer case. Belongs after fixed-workflow competence |
| O3 | **Price a workflow in successful outcomes** | Durable as a unit (spend per outcome that cleared the bar); the arithmetic beneath it expires fast |
| O4 | **Formal endpoint or method comparison under a frozen suite** | The full apparatus is heavy for a bootcamp; A4 carries the durable residue at a fraction of the cost |

### Out of scope for this bootcamp

Authoring a protocol server or wire-format integration · multi-agent topology design and orchestration frameworks · building retrieval pipelines (chunking, embeddings, vector stores, rerankers) · fine-tuning mechanics (retain only the decision rule: *it changes form, not facts; it is a build-and-maintain commitment; escalate it*) · judge-validation statistics and power analysis · observability platform selection and instrumentation schemas · numbered risk taxonomies as syllabus · instruction-file formatting conventions · prompt-technique catalogs · model internals · benchmark and leaderboard literacy · standalone ethics module (fold into C10/C11/C12/C14 where it is assessable).

All three lenses excluded every item on this list independently.

### Mastery-level distinctions applied

The model separates **conceptual recognition** (fine-tuning decision rule), **guided execution** (first trace read), **independent selection** (rung choice, gate placement), **independent implementation** (brief, check, inventory), **diagnosis and recovery** (C5, C6, C9), and **transfer** (A4, A5, capstone). `reformation/` largely conflates the middle four; several of its modules describe guided execution while assessing as though it were independent implementation.

---

## 5. Coverage matrix

| Competency | Priority | Where it appears in `reformation/` | Depth taught | Evidence required | Verdict | Gap or excess |
|---|---|---|---|---|---|---|
| F1 Map the harness | Foundational | [`01-first-result.md:95-110`](../../reformation/modules/01-first-result.md) Stage 6; [`TOOLS_AND_METHODS.md:9-14`](../../reformation/TOOLS_AND_METHODS.md) | Guided execution, once | Six-part map with scenario/implementation/durable marking | **STRONG** | Map is of the *supplied* harness, not the learner's own. Repeat it on their own setup in Module 02 |
| F2 Acceptance artifact + falsifier | Foundational | [`DIRECTION_BRIEF.md:16-22`](../../reformation/templates/DIRECTION_BRIEF.md); [`README.md:39`](../../reformation/README.md); [`THINKING_PATTERNS.md:5-17`](../../reformation/THINKING_PATTERNS.md) | Independent implementation, repeated | "Done looks like" checklist, frozen before execution | **STRONG** | The falsifier ("what would a wrong result look like") is in Thinking Pattern 1 but is not a required brief field. Add it to the template |
| F3 Predict-then-measure own performance | Foundational | **Nowhere** | — | — | **MISSING** | Zero hits across all 23 files for calibration, overclaim, prediction of own speed, or unassisted baseline. The legacy course tracked this (`operator/MEASUREMENT_SPINE.md`) and it was dropped |
| F4 Blast radius | Foundational | [`00-setup.md:52`](../../reformation/modules/00-setup.md) (one sentence); [`04-tool-boundaries.md:86`](../../reformation/modules/04-tool-boundaries.md) "least authority needed" | Conceptual, scattered | None specific | **PRESENT BUT THIN** | Never a written inventory, never a worst-case statement, never a demonstrated narrowing. Arrives at Module 04 — after Modules 02–03 already ran consequential work |
| F5 Restore point and recovery | Foundational | [`00-setup.md:117`](../../reformation/modules/00-setup.md); [`02-direct-repeatable-work.md:85`](../../reformation/modules/02-direct-repeatable-work.md); [`THINKING_PATTERNS.md:125-138`](../../reformation/THINKING_PATTERNS.md) | Independent implementation | "A reversible workspace snapshot" | **STRONG** | Snapshot discipline is well handled. Never a *demonstrated restore after a bad run* — only snapshot-before-planting |
| C1 Checkable brief | Core | [`02-direct-repeatable-work.md:21-35`](../../reformation/modules/02-direct-repeatable-work.md); `DIRECTION_BRIEF.md` | Independent implementation, repeated | Frozen LIVE brief | **STRONG** | No turns-to-acceptable measurement; no constraint counting or precedence declaration. Compliance falls roughly geometrically in stacked constraints and the course never mentions it |
| C2 Verify against independent artifact | Core | [`README.md:41`](../../reformation/README.md); [`00-setup.md:64`](../../reformation/modules/00-setup.md); [`01-first-result.md:64-80`](../../reformation/modules/01-first-result.md) | Independent implementation, repeated | Known-answer, source-trace, functional, scope checks | **STRONG** | Best-covered competency in the course. Keep exactly as is |
| C3 Check the agent cannot author | Core | [`05-divide-and-govern.md:106-113`](../../reformation/modules/05-divide-and-govern.md); [`GETTING_UNSTUCK.md:161-166`](../../reformation/GETTING_UNSTUCK.md) "Protect the gate" | Independent implementation | Gate-tampering result | **PRESENT BUT THIN** | The principle is stated superbly but appears only inside the *multi-agent* module. It is a universal rule and arrives at module 5 of 9. Also missing: the stakes-indexed rung ladder |
| C4 Advice/enforcement sort **+ reset survival** | Core | [`03-control-layers.md:24-39`](../../reformation/modules/03-control-layers.md); [`TOOLS_AND_METHODS.md:40-48`](../../reformation/TOOLS_AND_METHODS.md) | Independent implementation | Control-layer map, working guard, negative test | **STRONG on the sort / MISSING on survival** | *"A sentence containing 'always' or 'never' is still advice unless something runs when the event occurs"* is exactly right. But nothing tests whether a placed rule survives a context reset — the mechanism by which correctly-sorted rules silently stop holding |
| C5 First-divergence localization | Core | [`THINKING_PATTERNS.md:96-109`](../../reformation/THINKING_PATTERNS.md); [`GETTING_UNSTUCK.md:49-68`](../../reformation/GETTING_UNSTUCK.md); [`03-control-layers.md:76-89`](../../reformation/modules/03-control-layers.md) | Guided, repeated | Loaded/triggered/executed diagnosis | **PRESENT BUT THIN** | The *method* is excellent and matches the research precisely. But the learner plants every fault themselves, so they always know the answer, and localization is never graded separately from repair |
| C6 Cheapest-cause-first classification | Core | [`GETTING_UNSTUCK.md:35-47`](../../reformation/GETTING_UNSTUCK.md) eight stuck states; [`08-evaluate-change.md:88-97`](../../reformation/modules/08-evaluate-change.md) seven failure layers | Conceptual + one application | Failure-layer diagnoses | **PRESENT BUT THIN** | Two different taxonomies (8 states, 7 layers) for the same job, neither ordered by cheapness. *"Do not blame the model first"* ([`08:97`](../../reformation/modules/08-evaluate-change.md)) is right but is stated once, in the last instructional module |
| C7 Error analysis over many runs | Core | **Nowhere** | — | — | **MISSING** | The single largest gap. No sampling, no first-failure annotation, no counted taxonomy, no ranking, no saturation. All three independent lenses made this core at 2.5–3.5h |
| C8 Failure → mechanical check | Core | [`02-direct-repeatable-work.md:58-68`](../../reformation/modules/02-direct-repeatable-work.md); [`00-setup.md:66-75`](../../reformation/modules/00-setup.md) | Independent implementation | Deterministic checks, watched failing once | **STRONG** | Module 00's *"you have watched the check fail once on a temporary wrong value"* is exactly the validated-check standard. But checks are derived from the brief, never from an observed failure ranking — because C7 is absent |
| C9 Durable fix + recurrence proof | Core | [`GETTING_UNSTUCK.md:98-111`](../../reformation/GETTING_UNSTUCK.md) step 7; [`THINKING_PATTERNS.md:111-123`](../../reformation/THINKING_PATTERNS.md) #9; `RECOVERY_NOTE.md` "Durable improvement" | Conceptual, advisory | Recovery note (required only in Module 00) | **PRESENT BUT THIN** | The principle is stated three times and required as evidence once. **No module asks the learner to prove the failure does not return in a fresh session** — the only objective test of whether a fix landed |
| C10 Reach inventory + canary | Core | Fragments: [`04-tool-boundaries.md:26,98-107`](../../reformation/modules/04-tool-boundaries.md); [`06-durable-state.md:78-94`](../../reformation/modules/06-durable-state.md); [`THINKING_PATTERNS.md:149-159`](../../reformation/THINKING_PATTERNS.md) #12 | Scattered, no single act | Hostile-input hold; external-content handling | **MISSING as an organising act** | The pieces are good — "treat returned content as data", "keep source instructions as untrusted data", trust/truth/permission separation. What is missing is the one repeatable inventory of the learner's own setup, and any egress/exfiltration channel awareness at all (zero hits for egress, exfiltration, canary, blast radius) |
| C11 Read raw config and raw descriptions | Core | [`04-tool-boundaries.md:14-30`](../../reformation/modules/04-tool-boundaries.md) Stage 1 | Independent selection | Third-party capability review and decision | **STRONG on capability review / MISSING on config** | *"'It appears in a registry' is not a review"* is excellent. But harness configuration files as executable content — a documented CVE class with a non-developer-performable control — is entirely absent |
| C12 Approval budgeting | Core | [`THINKING_PATTERNS.md:192-204`](../../reformation/THINKING_PATTERNS.md) #15 (advice only) | Conceptual | None | **MISSING** | *"The aim is not maximum human activity"* is directionally correct and never practised. "Approval" appears ~20 times as a card field or stop condition, never as a limited resource with a budget. No module asks the learner to count their own approvals |
| C13 Least machinery, climb on failure | Core | [`THINKING_PATTERNS.md:31-45`](../../reformation/THINKING_PATTERNS.md) #3, [`46-58`](../../reformation/THINKING_PATTERNS.md) #4; [`PATTERN_CATALOG.md:3`](../../reformation/PATTERN_CATALOG.md); [`05-divide-and-govern.md:19-32`](../../reformation/modules/05-divide-and-govern.md) | Independent selection | Baseline comparison and adoption decision | **STRONG** | Module 05's save-the-baseline-before-writing-the-measures ordering is the best instance of this found anywhere. Only weakness: the baseline is one worker at default budget, not **budget-matched** |
| C14 Evidence-attached handoff | Core | `HANDOFF.md`; [`README.md:43`](../../reformation/README.md); every module's evidence list | Independent implementation, repeated | Completed handoff with "what it does not prove" column | **STRONG** | Among the strongest in any curriculum reviewed. Preserve intact |
| C15 Cold resume | Core | [`00-setup.md:77-85`](../../reformation/modules/00-setup.md); [`02-direct-repeatable-work.md:127`](../../reformation/modules/02-direct-repeatable-work.md); [`06-durable-state.md:63-76`](../../reformation/modules/06-durable-state.md); [`09-capstone.md:116`](../../reformation/modules/09-capstone.md) | Independent implementation, repeated | Fresh-session regeneration; cold retrieval suite | **STRONG** | Well distributed and well assessed. Module 06's *"A confident answer without a walkable source trail fails the cold test"* is exactly right |
| A1 Repair capability selection | Advanced | [`04-tool-boundaries.md:84-96`](../../reformation/modules/04-tool-boundaries.md) Stage 6 | Independent implementation | Three selection cases, trace | **STRONG** | *"Do not hide a selection problem by instructing the harness to call a specific tool in every test"* is precisely the right rule. Missing: a fixture set authored before tuning, and before/after measurement |
| A2 Fixed production workflow + rule change | Advanced | [`07-control-flow.md:106-112`](../../reformation/modules/07-control-flow.md) Stage 7 — **sketched only** | Conceptual recognition | "Sketch a fixed workflow… choose fixed, adaptive, or hybrid" | **MISPLACED** | The course builds and operates the *adaptive* case (Stages 4–6) and only sketches the *fixed* case. Given that the correct default is no agentic machinery, this is inverted. The "change one rule once, measure what moved, zero manual repair" mechanic exists in the legacy course and has no successor here |
| A3 Govern durable state | Advanced | [`06-durable-state.md`](../../reformation/modules/06-durable-state.md) entire | Independent implementation | 11 evidence items | **STRONG but OVER-SCOPED** | Content is excellent and matches the research closely — including supersession, provenance, integrity, bounded claims. But 8 stages and 11 evidence items in 120–180 minutes is not deliverable |
| A4 Re-run held-back set after a change | Advanced | [`08-evaluate-change.md:38-53`](../../reformation/modules/08-evaluate-change.md) frozen suite | Independent implementation | Paired score matrix | **STRONG** | Correctly frozen, correctly paired, correctly bounded (*"Agreement across cases does not justify a broader claim than the suite tested"*) |
| A5 Port a control to a second harness | Advanced | [`03-control-layers.md:91-102`](../../reformation/modules/03-control-layers.md) Stage 5 portability test | Guided | "Test from a fresh folder, fresh session, or second machine" | **PRESENT BUT THIN** | Portability is tested against *relocation*, not against a *different enforcement plane*. The research calls the second-harness port the one reliable way to convert far transfer into near transfer |
| O1 Divide work | Optional | [`05-divide-and-govern.md`](../../reformation/modules/05-divide-and-govern.md) entire, 120–180 min | Independent implementation | 11 evidence items | **OVER-SCOPED** | Equal-largest module for a competency all three lenses tiered optional at ~1h. Missing the two decisive rules: budget-matched comparison, and read/write asymmetry stated plainly |
| O2 Adaptive loop | Optional | [`07-control-flow.md:61-104`](../../reformation/modules/07-control-flow.md) | Independent implementation | Two-wave artifact, state, traces | **STRONG content, MISPLACED weight** | Excellent design — the changed-world wave with NEW/CHANGED/CANCELLED/UNCHANGED is a genuinely good mechanic. It should follow the fixed case, not replace it |
| O3 Price in successful outcomes | Optional | [`TOOLS_AND_METHODS.md:112-122`](../../reformation/TOOLS_AND_METHODS.md) (reference only); [`08:105`](../../reformation/modules/08-evaluate-change.md) | Conceptual | Cost delta inside the comparison | **PRESENT BUT THIN** | Model-and-cost choice is listed as a valid decision artifact ([`AUTHORING_GUIDE.md:139`](../../reformation/AUTHORING_GUIDE.md)) but **no module requires one**. The legacy course had a dedicated block; only the heavyweight formal comparison survives |
| O4 Formal endpoint comparison | Optional | [`08-evaluate-change.md`](../../reformation/modules/08-evaluate-change.md) entire | Independent implementation | 11 evidence items | **OVER-SCOPED for core** | Sound module carrying fine-tuning residue it does not need |
| Fine-tuning mechanics | Out of scope | [`08:21,53,129-131`](../../reformation/modules/08-evaluate-change.md) | Fragments | Data admission and split record | **OUT OF SCOPE — correctly demoted, incompletely removed** | The decision rule at line 21 is the right content. The training-evaluation apparatus at 53 and 129–131 is legacy residue costing stages in an already-overfull module |
| Protocol internals | Out of scope | [`04-tool-boundaries.md:63-67`](../../reformation/modules/04-tool-boundaries.md) Stage 4 | Conceptual | Protocol lifecycle and failure map | **OPTIONAL, NOT CORE** | Handled at the right altitude — *"The protocol carries requests and results. It does not make the connected capability trustworthy"* is exactly right. But a whole stage on discovery/transport/negotiation/shutdown is more than an operator needs |
| Multi-agent topologies | Out of scope | [`PATTERN_CATALOG.md:30-45`](../../reformation/PATTERN_CATALOG.md) 14 named patterns | Conceptual | Three traced patterns | **OVER-SCOPED** | 14 patterns catalogued, 3 traced. Several catalogued patterns (debate-adjacent, supervisor-with-workers) are the ones the evidence most directly contradicts |
| Context as a finite budget | **Core in 2 of 3 lenses** | **Nowhere** | — | — | **MISSING** | "Context" is one of the six named harness parts ([`TOOLS_AND_METHODS.md:11`](../../reformation/TOOLS_AND_METHODS.md)) yet the word appears 12 times in 2,807 lines, always meaning *source material available*, never *a budget that degrades*. No compaction, no reset trigger, no attention limit, no premature-termination symptom |

---

## 6. What the curriculum teaches well

These are mechanisms worth preserving verbatim into the new implementation.

**The adapter separation rule.** [`AUTHORING_GUIDE.md:13-22`](../../reformation/AUTHORING_GUIDE.md) — competency / method / evidence stable, scenario / implementation replaceable, *"Write the module from the first three layers."* This is the correct architecture for a skeleton, and the fixture-check-vs-competency-check distinction at [`86-94`](../../reformation/AUTHORING_GUIDE.md) is the sharpest statement of it: *"the supplied workbook contains the expected number of rows"* versus *"a malformed record is refused without altering the last good output."*

**`HOLD` as a supported result, with a boundary.** [`README.md:45-53`](../../reformation/README.md) — *"A well-supported `HOLD` is a valid result"*, immediately bounded by *"Do not claim the held competency as passed until its material check succeeds."* This is the course's partial answer to fixed-standard-variable-time, and it is better than the cohort-paced completion the research finds nearly universal in commercial AI courses.

**Model self-assessment is not proof.** [`README.md:41`](../../reformation/README.md) and [`00-setup.md:64`](../../reformation/modules/00-setup.md) — *"Do not count a conversational claim as success. Open the file yourself."* Inaccurate self-reporting accounts for 22.6% of coded agent misalignment episodes and only ~3% of failures are agent-self-corrected. Stating this in Module 00 Stage 3 is correct sequencing.

**The advice / enforcement / authority distinction.** [`TOOLS_AND_METHODS.md:40-48`](../../reformation/TOOLS_AND_METHODS.md) — *"A sentence containing 'always' or 'never' is still advice unless something runs when the event occurs. A permission can block a write. It cannot decide whether a claim is true."* This matches vendor documentation and the field evidence exactly, and it is stated more clearly here than in any source consulted.

**Loaded / triggered / executed / bypassed.** [`03-control-layers.md:78-89`](../../reformation/modules/03-control-layers.md) — four states with the instruction *"Do not infer the state from silence."* Classifying the error before searching for it is the validated core of the only debugging intervention with a measured effect size (d = 0.69), and the fourth state (*"ran correctly but was bypassed elsewhere"*) is one most practitioners omit.

**The discriminating-probe test.** [`GETTING_UNSTUCK.md:70-84`](../../reformation/GETTING_UNSTUCK.md) — *"If every possible result would make you reinstall, rewrite everything, or add more prompt text, the probe has not narrowed the problem."* This is the single best sentence in the curriculum. It converts an attitude into a decidable test.

**Baseline before measures.** [`05-divide-and-govern.md:19-32`](../../reformation/modules/05-divide-and-govern.md) — *"Save its result and run identity before reading it closely… Write the measures for the divided run before opening the baseline."* This defends against exactly the confound that the 2026 multi-agent literature identifies, and it is rare in practice.

**Refutation over confirmation.** [`05-divide-and-govern.md:79-89`](../../reformation/modules/05-divide-and-govern.md) — *"A checker does not add helpful facts to rescue a weak finding… Do not use worker votes as truth. One authoritative contradiction can defeat a finding repeated by several workers."* Directly anticipates the consensus-collapse finding.

**Bounded containment claims.** [`06-durable-state.md:116`](../../reformation/modules/06-durable-state.md) — *"'No forbidden write appeared in the observed paths during this recorded run' is supportable. 'Nothing happened anywhere' is not."* No comparable curriculum found in the research teaches learners to bound a negative claim.

**The evidence boundary as a graded level.** [`COURSE_MAP.md:70`](../../reformation/COURSE_MAP.md) level 7 and `EVIDENCE_RECORD.md`'s *"What this does not prove"* column. Making "state what your evidence did not establish" the top of the ladder is the strongest assessment idea in the document.

**Module 01's shape.** [`01-first-result.md`](../../reformation/modules/01-first-result.md) — predict, run a supplied method, use the product for its real job, four checks, changed input with prediction first, reverse-engineer the harness. This is the worked-example effect implemented correctly, with prediction forcing the expectation model before the answer arrives. It is explicitly labelled *"a guided experience"* that *"does not yet prove that you can design the harness independently"* ([`8`](../../reformation/modules/01-first-result.md)) — the exact distinction most courses blur.

**Fresh session ≠ person transfer.** [`09-capstone.md:116-117`](../../reformation/modules/09-capstone.md) — *"If no person is available, record the fresh-session result as restartability, not independent operator transfer."* Correct, and rarely stated.

**Selection problems must not be hidden.** [`04-tool-boundaries.md:96`](../../reformation/modules/04-tool-boundaries.md) — *"Do not hide a selection problem by instructing the harness to call a specific tool in every test."*

**Repair the method, not the output.** [`02-direct-repeatable-work.md:81`](../../reformation/modules/02-direct-repeatable-work.md) — *"Do not repair generated content by hand. Repair the direction, method, or implementation, then rerun."*

---

## 7. Structural findings

### Sequence

The stated ordering logic ([`COURSE_MAP.md:28-44`](../../reformation/COURSE_MAP.md)) is sound: experience before abstraction, direction before machinery, complexity earns its cost, transfer on unfamiliar work. Two ordering problems remain.

**Safety arrives after consequential work begins.** Blast radius, credential scoping, and reversibility appear as a sentence in Module 00 ([`52`](../../reformation/modules/00-setup.md)) and properly only at Module 04 ([`86`](../../reformation/modules/04-tool-boundaries.md)). Modules 02 and 03 already run real work against real sources. Reversibility is also a *technical precondition for diagnosis* — an operator who cannot return to a known state has no stable pass/fail oracle, and every localization method degrades to guessing.

**Verification independence arrives at module 5 of 9.** "The system under test never writes its own test" is universal but is introduced inside the multi-agent module ([`05:106-113`](../../reformation/modules/05-divide-and-govern.md)). It belongs in Module 00 or 01 and should be reinforced in every module thereafter.

### Prerequisites

Well handled within the module chain. One unstated prerequisite — a real recurring task of the learner's own — carries most of the transfer weight and should be an admission requirement.

Module 07 has a prerequisite that cannot be met by the skeleton: Stage 1 requires *"three executable examples or trace simulations"* ([`07:8`](../../reformation/modules/07-control-flow.md)). The fallback is honest (*"record the result as a simulation rather than an executed implementation"*), but a learner who only paper-traces an adaptive loop is then asked to design one in Stage 4 with no executed instance behind them.

### Module size

| Module | Stages | Evidence items | Stated time | Assessment |
|---|---:|---:|---|---|
| 00 | 5 | 7 | 60–120 min | Reasonable |
| 01 | 7 | 6 | 60–90 min | Tight but coherent — one activity, many lenses |
| 02 | 7 | 9 | 90–150 min | Overfull |
| 03 | 5 | 7 | 90–120 min | Overfull (build a procedure **and** a guard **and** diagnose **and** package) |
| 04 | 8 | 10 | 90–150 min | **Not deliverable.** Inspect a third-party capability, choose primitives, complete a ~30-field boundary card, map a protocol lifecycle, test directly through a client, connect, run three selection cases, run an injection test, package, verify disconnect — in 90 minutes, for a non-developer |
| 05 | 8 | 11 | 120–180 min | Over-scoped for an optional competency |
| 06 | 8 | 11 | 120–180 min | Excellent content, undeliverable volume |
| 07 | 7 | 10 | 120–180 min | Overfull, and weighted to the rarer case |
| 08 | 8 | 11 | 120–180 min | Overfull, carrying legacy residue |
| 09 | 8 + package | package | 3–6 hr | Appropriate |

Sum of module times: 14.5–22.5 hours. [`COURSE_MAP.md:3`](../../reformation/COURSE_MAP.md) states 18–26 hours; the parts do not add to the stated whole at either end. Against this, three independent competency models estimated 36, 40, and 40.5 hours for narrower coverage. **The volume problem is the dominant structural finding after the C7 gap.**

### Repetition

The five moves recur, which is good. But no *competency* is deliberately re-practised at increasing difficulty. In the independent models, 15 of ~20 core competencies were marked `practice-repeatedly`; in `reformation/`, each competency appears in exactly one module and is assessed once. Every guided lab should be followed by an unguided repetition on a different case within the same session — the unguided repetition being the unit of instruction. Nothing in the module shape requires this.

### Cognitive load

Six overlapping frameworks compete for the same working memory:

| Framework | Location | Items |
|---|---|---|
| The operating spine | [`README.md:37-43`](../../reformation/README.md) | 5 moves |
| The learning cycle | [`README.md:57-64`](../../reformation/README.md) | 6 stages |
| The repeated module shape | [`COURSE_MAP.md:48-58`](../../reformation/COURSE_MAP.md) | 9 questions |
| The required module shape | [`AUTHORING_GUIDE.md:26-38`](../../reformation/AUTHORING_GUIDE.md) | 12 items |
| The assessment ladder | [`COURSE_MAP.md:62-70`](../../reformation/COURSE_MAP.md) | 7 levels |
| The evidence ladder | [`AUTHORING_GUIDE.md:96-104`](../../reformation/AUTHORING_GUIDE.md) | 7 items |

The last two are **the same seven levels stated twice in different words** (present/exists, structured/structure, functional/behaviour, challenged/negative, changed/delta, transferred/fresh, bounded/boundary). Add the six-part harness, four classification axes, 14 patterns, 15 thinking patterns, 8 stuck states, a 9-step boundary chain, and a 7-item escalation packet, and the learner is decoding roughly 80 named items to perform maybe 15 actions.

### Assessment

Strong in kind — behaviour over artifact existence, with an explicit prohibition on assessing attendance or file presence ([`AUTHORING_GUIDE.md:40`](../../reformation/AUTHORING_GUIDE.md)). Three weaknesses:

1. **Self-planted failures.** Every module has the learner plant the fault, so the diagnosis is a rehearsal of a known answer. The research condition for failure-first learning to work is that the learner must generate genuine attempts against a gap they notice — and the strongest published null results came from exactly this configuration.
2. **Localization is never graded separately from repair.** A learner who guesses their way to a working state passes.
3. **No calibration instrument.** Nothing measures whether the learner's confidence tracks their evidence.

### Recovery

The method in [`GETTING_UNSTUCK.md`](../../reformation/GETTING_UNSTUCK.md) is the strongest single artifact in the skeleton and matches the validated intervention structure: named, small, ordered, taught briefly, referenced constantly. Three fixes:

- `RECOVERY_NOTE.md` is required as evidence only in Module 00 ([`115`](../../reformation/modules/00-setup.md)) and the capstone package. Modules 01–08 all plant failures and none collect the note. The course practises diagnosis eight times and records it once.
- Step 7 ("Teach the harness what you learned") never requires proof. Add the fresh-session recurrence test.
- The eight stuck states are not ordered by cheapness, so "the model is wrong" is not structurally the last available conclusion.

### Transfer

Transfer is assessed only at Module 09. The research is emphatic that delay between training and application predicts transfer failure, and that the first real-world attempt should be small and winnable because first-attempt failure predicts abandonment. The legacy course wrote a dated transfer seed at every module closeout and assembled them into horizons; `reformation/` dropped this entirely. A one-line dated seed per module costs about three minutes and is the highest-yield-per-minute item in this review.

### Adapter boundary

This matters most for your stated purpose. [`README.md:19`](../../reformation/README.md) flags Modules 01, 03, 04, 05, 07 as needing adapter support. Three problems:

1. **Two modules are unflagged but adapter-dependent.** Module 06 requires a durable store with a sanctioned admission boundary — *"a single writer, transactional service, append-only log, compare-and-swap operation, or partitioned ownership scheme"* ([`06:48`](../../reformation/modules/06-durable-state.md)). Module 08 requires two endpoints and possibly provisioned compute ([`08:131`](../../reformation/modules/08-evaluate-change.md)).
2. **The adapter contract says what a README must *declare*, never what it must *supply* per module.** [`AUTHORING_GUIDE.md:56-67`](../../reformation/AUTHORING_GUIDE.md) lists ten declaration fields but no per-module obligation table.
3. **The non-developer accommodation is unspecified.** For Modules 03 and 04, "the adapter provides the code" could mean a fill-in-the-blank template, a pre-built component the learner only configures, or a facilitator writing it live. These produce different competencies. Unresolved, a new implementation will either exclude non-developers or water the competency down to clicking.

**Recommendation:** add a per-module "what an adapter must supply" table to `AUTHORING_GUIDE.md`, with a required field stating the minimum the learner must author themselves versus configure. This is the single highest-value addition for a fresh build.

### Total bootcamp scope

Over-scoped in volume, under-scoped on error analysis, calibration, approval design, context budget, and reach inventory. The correction is not additive — the additions in §9 are funded by the prunes in §10, and the net time is roughly flat with a shift from breadth to repetition.

---

## 8. Module-by-module dispositions

| Module | Disposition | Keep | Change | Add | Prune or move | Rationale |
|---|---|---|---|---|---|---|
| **00 Setup** | `KEEP, REVISE` | All five stages; the watched-check-fail standard ([`75`](../../reformation/modules/00-setup.md)); cold-start boundary; the honest scope note at [`83`](../../reformation/modules/00-setup.md) | Stage 5's planted failure becomes an instructor-planted fault, not learner-planted | **F3 predict-then-measure baseline** (the learner's estimation gap, recorded before anything else); **F4 reach inventory**; **F5 demonstrated restore after a bad run** | — | This is where the operator's instruments get calibrated, and where reversibility must exist before any consequential run. Adding F3 here is the only place it works — it must precede any investment in believing the harness helped |
| **01 First result** | `KEEP` | Everything | — | — | — | The best-designed module. Worked example, prediction before result, product used for its real job, explicit guided-experience label. Do not touch it |
| **02 Direct repeatable work** | `KEEP, REVISE` | Frozen brief; input contract; changed-input rerun with prediction; repair-the-method rule ([`81`](../../reformation/modules/02-direct-repeatable-work.md)); judgment separation | Stage 6's planted failure gets a required `RECOVERY_NOTE.md` | **Turns-to-acceptable count** against the learner's own prior baseline; **constraint counting and precedence declaration**; repeat F1 on the learner's *own* harness; **live in-flight correction** as a named practised move | — | The brief is already strong; what is missing is measuring whether it actually reduced correction turns. Live correction was a distinct legacy capability and survives here only as half a sentence at [`55`](../../reformation/modules/02-direct-repeatable-work.md) |
| **03 Control layers** | `KEEP, REVISE` | The control-surface map; the advice/enforcement/authority distinction; the loaded/triggered/executed/bypassed diagnosis; the "what would be worse without each component" paragraph | Portability test ([`91-102`](../../reformation/modules/03-control-layers.md)) becomes a **second-harness port** where practical, not just a fresh folder | **The context-reset survival test** — state a rule in conversation, run long enough to compact, request the prohibited thing, watch it happen; then re-establish from a durable source and show it holds | Trim Stage 2 or Stage 5 to make room | **The single highest-value small addition in the course.** The module already teaches where a rule belongs; it does not teach that a correctly-placed rule can silently stop holding. That is the failure mode the sort exists to prevent |
| **04 Tool boundaries** | `SPLIT` | Stage 1 capability review; Stage 2 primitive choice; Stage 6 selection cases; Stage 7 content-as-data; Stage 8 disconnect | **04a (core, non-developer):** inspect, classify, scope, attach, test selection, treat returns as data, disconnect. **04b (optional/advanced):** build and directly test your own capability | To 04a: **config-as-executable-content**; **approval budgeting with a counted before/after**; the raw-manifest-vs-approval-dialog distinction | Move Stage 4 protocol lifecycle to optional depth; trim the boundary card from ~30 fields to the ~12 that change a decision | 8 stages and 10 evidence items in 90–150 minutes is not deliverable, and the build-your-own half is the part a non-developer cannot do unaided. The measured weight sits in curation, description, scope, and bounds — all configuration-surface work |
| **05 Divide and govern** | `MERGE` + `MAKE OPTIONAL` | The baseline-before-measures ordering; refuting checkers; no-votes-as-truth; the gate-tampering test; "parallelism did not earn use" as a valid result | Halve it. State **read/write asymmetry** as a hard rule: parallel readers, exactly one writer per shared artifact, one synthesizer. Make the baseline **budget-matched** | — | Move the **gate-tampering test to C3 in Module 02** (it is universal, not multi-agent-specific). Move the **unattended operations drill to Module 07** (it belongs with control flow). Fold what remains into an optional branch | All three independent lenses tiered multi-agent optional at ~1h; the evidence shows single agents match or beat multi-agent under matched budgets. The module's own honesty is its strength — but it spends a full module's hours proving a mostly-negative result |
| **06 Durable state** | `KEEP, REVISE` | Trust and write policy; retrieval schema; controlled writer; cold retrieval; hostile intake; integrity check with planted mutation; bounded containment claim | Make supersession explicit as **one current value per (thing, property), superseded version marked** — currently implicit in the status field at [`43`](../../reformation/modules/06-durable-state.md). Reduce 8 stages to ~5 | State plainly that similarity search cannot distinguish a contradiction from a duplicate | Merge Stages 3 and 4; merge Stages 7 and 8. Flag the adapter obligation explicitly | Content is closely aligned with the research — this is one of the better modules. The problem is purely volume |
| **07 Control flow** | `SPLIT` | The pattern classification on four axes; the adaptive mission design; the two-wave changed-world revision with NEW/CHANGED/CANCELLED/UNCHANGED; the fixed-vs-adaptive comparison | **07a (core): build and operate a fixed workflow** — batch run, change one rule in one place, side-by-side comparison naming exactly what moved, **zero manual repair**, second wave through the same saved artifact. **07b (advanced): the adaptive mission**, unchanged | Receive the unattended operations drill from Module 05 | Trim `PATTERN_CATALOG.md` from 14 patterns to ~7 that carry a decision | The correct default is no agentic machinery, and most consequential operator work is fixed or hybrid production. The course currently builds the rare case and sketches the common one. The "change one rule, measure the blast radius, zero manual repair" mechanic is the operational proof that the method lives in the artifact rather than in the operator's hands, and nothing in `reformation/` carries it |
| **08 Evaluate change** | `KEEP, REVISE` + `PRUNE` | Policy before comparison; frozen suite with a scoring guide written before results; baseline-is-not-reconstructed rule ([`68`](../../reformation/modules/08-evaluate-change.md)); failure-layer localization; the narrow-decision requirement; rollback verification | Require **a live human listener** for the transfer check at [`133`](../../reformation/modules/08-evaluate-change.md), passing only when they restate the fitness verdict unprompted — a fresh session is restartability, not person-transfer, and Module 09 already says so | — | Prune the fine-tuning apparatus: [`53`](../../reformation/modules/08-evaluate-change.md) training splits and checkpoint selection, [`129-131`](../../reformation/modules/08-evaluate-change.md) adapter removal and compute shutdown. Retain the decision rule at [`21`](../../reformation/modules/08-evaluate-change.md) | The comparison discipline is sound and durable. The training residue is legacy P9 material for a learner who should be declining fine-tuning with a reason, not evaluating a training run |
| **09 Capstone** | `KEEP` | Everything, especially the two-part transfer check and the seven-level assessment | Add F3 re-measurement (did the estimation gap close?) | — | — | Well-designed. The `HOLD`-can-pass rule at [`167`](../../reformation/modules/09-capstone.md) is correct and rare |
| **NEW — Error analysis** | `ADD` | — | — | Sample 20–40 of the learner's own runs; annotate the *first* failure only; group after the fact; count; rank; stop at saturation; binary labels; convert the top-ranked failure into a validated mechanical check; prove non-recurrence in a fresh session | — | The missing spine. Without a counted failure taxonomy, every check the learner builds is a guess about which failures matter |

---

## 9. Additions

Each addition names what it displaces. Net time change is approximately +1 hour against a course that is already over-volume; the prunes in §10 recover 4–6 hours.

### A. Error analysis module — `P0`

- **Competency:** C7 + C8 + C9 as one continuous act.
- **Reason:** Named the highest-yield evaluation activity in practitioner guidance and made core by all three independent lenses at 2.5–3.5 hours. It requires domain judgment and disciplined reading, not code — which makes it the strongest available argument that a non-developer belongs in this work.
- **Where:** New module after the diagnosis work (position 5 in the revised sequence), once the learner has accumulated real runs from Modules 02–04.
- **Practice:** Read a sample of your own runs one at a time. Write a free-form note on the *first* thing that went wrong — not the cascading consequences. Group notes into named categories *after* the fact. Count. Rank. Stop when new runs stop producing new categories. Label binary pass/fail, never 1–5. Convert the top-ranked category into a mechanical check validated against the actual bad output that motivated it. Prove non-recurrence in a fresh session.
- **Evidence:** Raw notes; the counted taxonomy; the ranked top three; a rubric that visibly changed between the first and second twenty labels, with the change recorded; one runnable check demonstrated failing on known-bad and passing on known-good; a fresh-session recurrence test.
- **Time:** 150–180 min.
- **Funded by:** halving Module 05 (−60 min) and pruning Module 08's training apparatus (−30 min).

### B. Calibration baseline in Module 00 — `P0`

- **Competency:** F3.
- **Reason:** The perception–performance gap in AI-assisted work has been measured at roughly 39 points in the confident direction; self-reported AI competence is misaligned with objective competence. A course that teaches learners to demand evidence from AI systems cannot leave their own estimation unmeasured. The legacy course tracked overclaim per block; `reformation/` dropped it.
- **Where:** Module 00, before any harness work.
- **Practice:** Predict how much faster or better the harness will make a representative task from your own work. Do one instance unassisted, timed. Do a comparable instance with the harness, on the same items. Score both against a rubric you did not write.
- **Evidence:** Timestamped prediction, two matched runs, externally scored rubric. **Graded on the size of the prediction gap, not the direction of the result.** Repeated once at the capstone.
- **Time:** 60–90 min.
- **Funded by:** trimming Module 04's protocol lifecycle stage to optional depth (−30 min) and the boundary-card field reduction (−30 min).

### C. Context-reset survival test in Module 03 — `P1`

- **Competency:** C4's second half.
- **Reason:** A measured mechanism: a policy visible in context produced 0% violations; after compaction, 30%; pinning the constraint outside the compaction pass restored 0% for roughly 47 tokens. Soft organisational policies decayed far more than hard safety norms. This is the exact failure signature Module 03's sort exists to prevent, and the module currently stops one step short.
- **Where:** Module 03, new stage after the loaded/triggered/executed diagnosis.
- **Practice:** State a rule in conversation only. Run the session long enough to compact or reset. Request the prohibited thing. Watch the violation happen with no error. Then re-establish the rule from a durable source the harness re-reads, and show it holds.
- **Evidence:** A matched pair of transcripts on the same rule — violated in one, held in the other — plus a statement of which of the learner's own standing rules are conditional.
- **Time:** 30 min.
- **Funded by:** trimming Module 03 Stage 5's packaging exercise.

### D. Reach inventory and canary in Module 00 / Module 04a — `P1`

- **Competency:** C10 + C11.
- **Reason:** Converts an undetectable problem into an inventory problem. Prompt injection is a structural property of the model class, not a bug awaiting a patch; published defenses reporting near-zero success are bypassed above 90% by adaptive attackers; excessive agency moved to #3 in the 2026 OWASP list on incident data. The operator's real control is the boundary, not detection.
- **Where:** First pass in Module 00 (own setup, before consequential work); repeated in 04a whenever a capability is attached.
- **Practice:** Three-column inventory — private data reachable, every point where content you did not write enters, every way bytes can leave (including rendered images, links, free-text fields on allowlisted destinations). Remove one leg. Prove it with a canary: a dummy secret in reachable data plus a hidden instruction in a document the agent will read. Show the secret did not leave.
- **Evidence:** The inventory; the configuration change; a working run afterwards; the canary result. Re-run required after any new capability.
- **Time:** 45 min in Module 00, 20 min repeat in 04a.
- **Funded by:** Module 05 reduction.

### E. Approval budgeting in Module 04a — `P1`

- **Competency:** C12.
- **Reason:** Approximately 93% of permission prompts are approved; roughly one in three dangerous commands passes human gating; 94% of developers failed to detect live sabotage over five hours. Escalating everything is measurably worse than escalating selectively. `reformation/` treats approval as a field to record, never as a resource to budget — and [`THINKING_PATTERNS.md:204`](../../reformation/THINKING_PATTERNS.md) already points the right way without any module acting on it.
- **Where:** Module 04a.
- **Practice:** Count your own approval events and approval rate in a real session. Rate each capability on read/write, reversibility, whose permission, cost of a wrong call. Make dangerous actions structurally unavailable rather than gated. Place few gates at irreversible edges, each showing the raw action rather than the agent's description of it.
- **Evidence:** The rating table; before/after approval count on the same task; the learner's observed approval rate; a justification for each surviving gate *and each removed one*.
- **Time:** 45 min.
- **Funded by:** Module 04 split.

### F. Fixed-workflow build in Module 07a — `P1`

- **Competency:** A2.
- **Reason:** The correct default is no agentic machinery, and most working systems are mostly deterministic with model calls at a few points. The course builds the adaptive case and sketches the fixed one.
- **Where:** Module 07, first half.
- **Practice:** Run a batch through a fixed path. Change one rule in one place. Rerun. Produce a side-by-side comparison naming exactly which records and fields moved and which correctly did not. **Zero row-by-row manual repair.** Run a second wave of new records through the same saved artifact.
- **Evidence:** Both batch outputs; the one-line rule diff; the side-by-side comparison; a manual-edit count of zero; the second-wave receipt.
- **Time:** 90 min (Module 07 splits into 07a core and 07b advanced).
- **Funded by:** moving 07b to advanced, which removes it from the required path.

### G. Per-module transfer seed — `P1`

- **Competency:** transfer scaffolding across the course.
- **Reason:** Delay between training and application predicts transfer failure; implementation intentions bound to real triggers outperform generic action plans. Currently transfer lives only in Module 09.
- **Where:** Every module closeout.
- **Practice:** One dated line — a named workload from your own desk where this module's capability applies, and the trigger that will fire it.
- **Evidence:** The dated seed; assembled into horizons before the capstone.
- **Time:** 3 min per module (~30 min total).
- **Funded by:** the framework consolidation in §10.

### H. Instructor-planted faults for graded localization — `P1`

- **Competency:** C5 + C6 assessed properly.
- **Reason:** Teaching a named systematic procedure beat equal-time extra practice at d = 0.69 — but productive-failure results null out when the fault does not expose a gap the learner notices, or when the debrief is scripted rather than responsive. A self-planted fault is a rehearsal of a known answer.
- **Where:** One consolidated diagnosis lab, plus one instructor-planted fault in the capstone environment.
- **Practice:** Four faults of different classes, interleaved rather than blocked, in a harness the learner did not configure. Write what each step should have produced. Walk backward to the earliest divergence. Halve the interval. Name the layer. One change per attempt; revert failed attempts.
- **Evidence:** **Graded on correct localization and layer naming, not on eventual repair.** Adherence to one-change-per-attempt is part of the grade.
- **Time:** 90 min (partly recovered from stages already present in Modules 03 and 08).
- **Funded by:** consolidating the diagnosis fragments currently spread across Modules 00, 02, 03, 04, 05, 06, 07, 08.

---

## 10. Pruning and consolidation

| Prune / merge | Removed from core | Why | Durable mechanism retained | Where it is still taught | Time recovered |
|---|---|---|---|---|---|
| **Module 05 halved and made optional** | Four of eight stages; the module leaves the required path | All three lenses tiered multi-agent optional at ~1h; single agents match or beat multi-agent under matched budgets; role-based decomposition is the least-supported common design | Baseline-before-measures; refutation over confirmation; no-votes-as-truth; read/write asymmetry; budget-matched comparison; "it did not earn its cost" as a valid result | Optional branch, plus the baseline discipline promoted into C13 (Module 02) and the gate-tampering test promoted into C3 (Module 02) | 60–90 min |
| **Module 04 split; boundary card trimmed** | Build-your-own-capability moves to optional; card reduced from ~30 fields to ~12 | The measured performance and safety weight sits in curation, description, scope, and bounds — all configuration work. Authoring requires code the learner does not have | Every card field that changes a decision: job/non-job, inputs, output bounds, provenance, unverified fields, side effects, approval, failure behaviour, version, disconnect | 04a core; the full card and the build exercise in 04b optional | 45–60 min |
| **Protocol lifecycle stage to optional depth** | [`04:63-67`](../../reformation/modules/04-tool-boundaries.md) discovery / transport / negotiation / shutdown | The wire format carries a date-stamped breaking revision roughly annually; the current revision removed the handshake and session header outright | *"The protocol carries requests and results. It does not make the connected capability trustworthy"* — plus: know which version your harness pins, and read a version-mismatch error | One paragraph in 04a; full treatment in 04b | 30 min |
| **Fine-tuning apparatus removed from Module 08** | [`08:53`](../../reformation/modules/08-evaluate-change.md) training/validation/held-out splits and checkpoint selection; [`08:129-131`](../../reformation/modules/08-evaluate-change.md) adapter removal and compute shutdown | Out of the learner's remit; a build-and-maintain commitment requiring an engineering owner. All three lenses tiered it at ≤0.5h as a decision rule | The decision rule at [`08:21`](../../reformation/modules/08-evaluate-change.md): *"Fine-tuning is a poor fit for changing facts, a missing tool, unstable policy, or an unclear task"* — plus *changes form, not facts*, and *escalate rather than attempt* | Module 08 Stage 1, as a two-sentence decision with a written decline | 30 min |
| **Pattern catalog reduced 14 → ~7** | Debate-adjacent, supervisor-with-workers-as-tools, orchestrator-and-workers, handoff as separate entries | Several catalogued patterns are the ones the evidence most directly contradicts; the catalog teaches vocabulary without decision power. 14 named, 3 traced | The four classification axes ([`PATTERN_CATALOG.md:19-26`](../../reformation/PATTERN_CATALOG.md)) — these carry all the decision content; plus single pass, chain, routing, fan-out/fan-in, evaluator-optimizer, tool loop, hybrid | `PATTERN_CATALOG.md`, shortened; remaining patterns listed as reference without exercises | 20 min of decode load |
| **Evidence ladder and assessment ladder merged** | One of the two seven-level ladders | They are the same seven levels stated twice in different words, in two documents the learner reads | The seven levels, stated once | `COURSE_MAP.md`, referenced from `AUTHORING_GUIDE.md` | ~15 min of decode load |
| **Module shape frameworks merged** | The 9-question shape ([`COURSE_MAP.md:48-58`](../../reformation/COURSE_MAP.md)) and the 12-item shape ([`AUTHORING_GUIDE.md:26-38`](../../reformation/AUTHORING_GUIDE.md)) reconciled into one | Two authoring templates for one artifact, with different item counts, in two documents | The 12-item required shape (superset), with the 9 learner-facing questions derived from it | `AUTHORING_GUIDE.md` authoritative; `COURSE_MAP.md` presents the learner-facing subset | ~15 min of decode load |
| **Diagnosis fragments consolidated** | Scattered planted-failure stages across 8 modules | Practising diagnosis eight times without recording it once, always on self-planted faults, is repetition without assessment | Every planted-failure mechanic, including snapshot-before-break ([`02:85`](../../reformation/modules/02-direct-repeatable-work.md)) | One graded diagnosis lab with instructor-planted, interleaved faults; one self-planted failure retained in Module 02 to teach failure *design* and the snapshot discipline | 30–45 min, redeployed |

**Net:** roughly 4–6 hours recovered against roughly 6 hours of additions, with the remainder funded by the framework consolidation. The course does not get longer; it gets narrower and deeper.

---

## 11. Recommended course architecture

Not a replacement curriculum — the phase structure, sequence, and boundaries only.

### Phase structure

| Phase | Modules | What the learner gains | Est. |
|---|---|---|---|
| **0 — Ground the instruments** | 00 Setup (+ F3 calibration, F4 reach inventory, F5 restore drill) | A workspace that proves what works, a measured estimate of their own estimation error, a bounded blast radius, and a demonstrated recovery | 3–4 h |
| **1 — See it work, then direct it** | 01 First result · 02 Direct repeatable work (+ turns-to-acceptable, constraint budgeting, live correction, gate-tampering promoted here) | One complete run inspected; then their own bounded, rerunnable, checked product with a measured reduction in correction turns | 4–5 h |
| **2 — Place behaviour where it holds** | 03 Control layers (+ context-reset survival) · 04a Tool boundaries (+ config-as-code, approval budget) | Requirements sorted into advice / enforcement / made-impossible, with the placement proved to survive a reset; capabilities attached under least authority with budgeted approvals | 4–5 h |
| **3 — Find and fix what actually breaks** | Diagnosis lab (instructor-planted, interleaved) · **Error analysis (new)** | Graded first-divergence localization in a harness they did not build; a counted failure taxonomy from their own runs; the top failure converted to a validated check; non-recurrence proved | 5–6 h |
| **4 — Operate at scale** | 07a Fixed workflow · 06 Durable state (trimmed) | A production path where one rule change moves exactly what it should with zero manual repair; durable state that a cold session can use and that detects tampering | 5–6 h |
| **5 — Govern change** | 08 Evaluate change (slimmed, human-listener transfer) | A capability change governed through frozen work, paired evidence, layer diagnosis, narrow adoption, and verified rollback — defended to a person who was not there | 2.5–3 h |
| **Capstone** | 09 (+ F3 re-measurement) | The whole method on unfamiliar work, handed to a cold reader | 4–6 h |
| **Optional branches** | 04b Build a capability · 05 Divide work · 07b Adaptive mission · A5 Second-harness port | Depth for learners who need it or finish early | 1.5–2 h each |

**Core total: 28–35 hours + capstone.** Higher than the current stated 18–26, lower than the independent models' 36–40, and honest about a load that is currently understated.

### Sequence rationale

Reversibility and blast radius precede consequential work because an operator who cannot return to a known state has no stable pass/fail oracle — every later diagnostic degrades to guessing. Calibration precedes everything because the learner must experience their own estimation error before they have any investment in believing the tooling helped; run it later and it becomes ceremony. Localization precedes error analysis because a learner who cannot say where a run diverged cannot write a useful note about it. Error analysis precedes check-building, always — an automated check can only measure a failure someone has already named, so building checks first produces coverage of imagined problems while real ones go unmeasured. Fixed workflow precedes adaptive because the fixed case is both more common and the baseline the adaptive case must beat.

### Core versus optional boundary

**Core** is everything a capable non-developer can perform through configuration, writing, and inspection, with an adapter supplying commands and fixtures. **Optional** is everything requiring authorship of code, or covering a competency whose evidence base is thin or narrow (multi-agent), or whose value is real but secondary for this learner (adaptive loops, formal endpoint comparison).

The test: *if the learner cannot do this without writing code they cannot maintain, it is optional or it is adapter-supplied — and the adapter contract must say which.*

### Cross-course skill strands

Five strands recur in every phase rather than appearing once:

1. **Acceptance and falsifier before the run** — every module opens with F2.
2. **Verify against an artifact the agent did not produce** — every module's evidence includes at least one.
3. **Localize, then repair the durable artifact, then prove non-recurrence** — every planted or encountered failure closes this way, with a `RECOVERY_NOTE.md`.
4. **Blast radius re-stated whenever capability expands** — Modules 00, 02, 04a, 06, 07a, capstone.
5. **Evidence-attached handoff** — every module ends with one; a recipient who did not watch the work must be able to tell what was verified.

Plus a **dated transfer seed** at every closeout, assembled into horizons before the capstone.

### Prerequisite relationships

```
F3 calibration ─┐
F4 blast radius ├─→ all consequential work
F5 restore     ─┘

F1 harness map ──→ C5 localization ──→ C7 error analysis ──→ C8 checks ──→ C9 durable fix
                        │                                                        │
C2 verify ──────────────┴────────────────────────────────────────────────────────┘

C1 brief ──→ C13 least machinery ──→ 07a fixed ──→ 07b adaptive (optional)
                                          │
C4 sort + reset survival ──→ C12 approvals┘

C10 reach inventory ──→ C11 raw config ──→ 04a attach ──→ 04b build (optional)

C15 cold resume ──→ A3 durable state ──→ A4 held-back set ──→ 08 govern change
```

Everything converges on the capstone, which exercises all five strands on work the course did not stage.

---

## 12. Prioritized change list

### `P0 — blocks the course`

**P0-1 · No error analysis anywhere**
*Location:* absent from all 23 files (verified by search for taxonomy / open coding / sampling runs / counted failures / saturation).
*Problem:* The learner never looks at many runs at once and never produces a counted, ranked list of the failures their harness actually produces.
*Learner consequence:* Every check they build is a guess about which failures matter. They leave able to check an artifact but unable to improve a harness, and unable to answer "what goes wrong most often here?" — which is the question that drives every subsequent decision.
*Change:* Add the error-analysis module (§9A).
*Evidence:* Named the highest-yield evaluation activity in practitioner guidance (Husain, hamel.dev), consuming 60–80% of development effort; both the 20,574-session field study and the MAST taxonomy built their codebooks this way; made core by all three independent competency models at 2.5–3.5 h; requires no code.
*Confidence:* **High.**

**P0-2 · No calibration instrument**
*Location:* absent (zero matches for calibration, overclaim, prediction of own performance, or unassisted baseline).
*Problem:* The course measures the artifact's evidence rigorously and never measures whether the operator's confidence tracks it.
*Learner consequence:* They can pass every check while systematically over-estimating their own effectiveness — the specific error measured at ~39 points in the confident direction among people using these tools daily.
*Change:* Add F3 predict-then-measure to Module 00, repeat at the capstone, graded on the gap not the direction (§9B).
*Evidence:* METR randomized trial; LAK 2026 self-report misalignment; >80% of transfer studies measure perception rather than transfer; the legacy course tracked overclaim per block (`operator/MEASUREMENT_SPINE.md`) and it was dropped in the rewrite.
*Confidence:* **High.**

**P0-3 · Adapter obligations are not stated per module**
*Location:* [`AUTHORING_GUIDE.md:42-69`](../../reformation/AUTHORING_GUIDE.md); [`README.md:19`](../../reformation/README.md) (flags 01, 03–05, 07; omits 06 and 08).
*Problem:* The contract says what an adapter README must *declare*, never what it must *supply* for each module, and never what the learner must author themselves versus configure.
*Learner consequence:* Modules 03 and 04 require code a non-developer cannot write; whether that becomes a template, a pre-built component, or a facilitator writing it live determines whether the competency survives or degrades to clicking.
*Change:* Add a per-module obligation table with a required field: *minimum the learner authors* vs *supplied by the adapter*. Flag Modules 06 and 08 as adapter-dependent.
*Evidence:* Internal consistency — [`README.md:70`](../../reformation/README.md) promises adapters will provide code but no contract field carries the promise. This is the highest-value fix for a fresh implementation.
*Confidence:* **High.**

### `P1 — high-value structural change`

**P1-1 · Deliberate failures are self-planted, so diagnosis is never tested**
*Location:* [`00:87-105`](../../reformation/modules/00-setup.md), [`02:83-98`](../../reformation/modules/02-direct-repeatable-work.md), [`03:76-89`](../../reformation/modules/03-control-layers.md), [`05:104-115`](../../reformation/modules/05-divide-and-govern.md), [`06:118`](../../reformation/modules/06-durable-state.md), [`07:101`](../../reformation/modules/07-control-flow.md), [`09:74-90`](../../reformation/modules/09-capstone.md).
*Problem:* The learner plants the fault and therefore knows the answer; localization is never graded separately from repair.
*Learner consequence:* Eight rehearsals, zero tests. A learner who guesses their way to a working state passes.
*Change:* Consolidate into one graded lab with instructor-planted, interleaved faults in a harness the learner did not build; grade localization and layer naming, not repair. Retain one self-planted failure in Module 02 to teach failure design and snapshot discipline (§9H).
*Evidence:* Michaeli & Romeike d = 0.69 for a taught procedure over equal-time practice; Loibl & Leuders null result under exactly the self-planted/scripted-debrief configuration; ICER 2023 null for productive failure in a computing course; Barbieri — correct examples beat incorrect ones for acquisition; all three lenses specified "a harness the learner did not build."
*Confidence:* **High.**

**P1-2 · Context is a named harness part whose defining property is never taught**
*Location:* [`TOOLS_AND_METHODS.md:11`](../../reformation/TOOLS_AND_METHODS.md) defines Context as *"the source material and standing information available to the model"*; the word appears 12 times in 2,807 lines and never as a budget.
*Problem:* No compaction, no reset trigger, no attention limit, no premature-termination symptom. A rule correctly sorted into "advice" in Module 03 can silently stop holding and the course never says so.
*Learner consequence:* The most common way a well-designed harness quietly stops working is invisible to them, and the "agent gave up" symptom gets misread as a capability ceiling rather than a context reset.
*Change:* Add the context-reset survival test to Module 03 (§9C); add reset triggers to Module 02.
*Evidence:* ConstraintRot — 0% violation with policy visible, 30% after compaction, restored to 0% by pinning outside the compaction pass; Chroma — all 18 frontier models degrade with input length at constant difficulty; premature-termination study; vendor documentation stating instruction files carry "no guarantee of strict compliance."
*Caveat:* the durability lens argued for cutting context *craft* as capability-graded scaffolding, and that argument is sound. The *diagnosis* — did it load, did it survive — is what both other lenses kept and what is recommended here. Do not add compaction-writing technique.
*Confidence:* **High** for the survival test; **medium** for anything further.

**P1-3 · Approval is a recorded field, never a budgeted resource**
*Location:* ~20 occurrences as a card field or stop condition; [`THINKING_PATTERNS.md:192-204`](../../reformation/THINKING_PATTERNS.md) is advice only.
*Problem:* No module asks the learner to count their own approvals, observe their own approval rate, or justify removing a gate.
*Learner consequence:* They will design more gates believing that is safer, and rubber-stamp them.
*Change:* Add approval budgeting to Module 04a (§9E).
*Evidence:* ~93% approval rate with diligence declining as volume rises; ~1 in 3 dangerous commands passing human gating; 94% of developers failing to detect live sabotage over five hours, with an LLM monitor reducing that only to 63%.
*Confidence:* **High** on direction; **medium** on the specific figures, several of which are vendor telemetry.

**P1-4 · No reach inventory; egress and config-as-code entirely absent**
*Location:* fragments at [`04:26,98-107`](../../reformation/modules/04-tool-boundaries.md), [`06:78-94`](../../reformation/modules/06-durable-state.md); zero matches for egress, exfiltration, canary, or blast radius.
*Problem:* Good pieces exist ("treat returned content as data", trust/truth/permission separation) with no organising act and no exit-channel awareness. Harness configuration files as executable content is absent despite being a documented CVE class with a control a non-developer can perform.
*Learner consequence:* They can reason about untrusted content in the abstract but cannot answer "what can leave this machine and how" for their own setup.
*Change:* Add the reach inventory and canary to Module 00, repeated in 04a (§9D); add config-as-executable to 04a.
*Evidence:* Lethal-trifecta framing; OWASP 2026 (injection #1 for a third edition, excessive agency to #3 on incident data); The Attacker Moves Second (>90% bypass of published defenses); Check Point CVE-2025-59536 / CVE-2026-21852; all three lenses made this foundational-to-core.
*Confidence:* **High.**

**P1-5 · The fixed production case is sketched while the adaptive case is built**
*Location:* [`07:106-112`](../../reformation/modules/07-control-flow.md) — *"Sketch a fixed workflow for the same task."*
*Problem:* The course builds the rarer case hands-on and the more common one on paper. The "change one rule once, measure exactly what moved, zero manual repair" mechanic has no successor from the legacy course.
*Learner consequence:* They leave able to design an adaptive mission but without the operational proof that a method lives in the artifact rather than in their hands.
*Change:* Split Module 07 into 07a fixed (core) and 07b adaptive (advanced) (§9F).
*Evidence:* Both major vendors direct builders to exhaust single-call and fixed options first; the control-flow ownership question is the root decision; production practice is mostly deterministic code with model calls at a few points; compounding per-step reliability (95%^20 ≈ 36%) makes step count the dominant design variable.
*Confidence:* **High.**

**P1-6 · Module 05 is the equal-largest module for an optional competency, and its baseline is not budget-matched**
*Location:* [`05-divide-and-govern.md`](../../reformation/modules/05-divide-and-govern.md), 120–180 min, 8 stages, 11 evidence items; baseline at [`19-32`](../../reformation/modules/05-divide-and-govern.md); comparison at [`117-128`](../../reformation/modules/05-divide-and-govern.md).
*Problem:* The comparison is against one worker at default budget, which is the exact confound the 2026 literature identifies. The read/write asymmetry — the highest-yield rule in the area — is implicit at [`58`](../../reformation/modules/05-divide-and-govern.md) and [`62`](../../reformation/modules/05-divide-and-govern.md) but never stated as a rule.
*Learner consequence:* They may conclude division helped when the extra tokens did the work.
*Change:* Halve it, make it optional, add budget-matching, state the read/write rule plainly; promote the gate-tampering test to Module 02 and the unattended-ops drill to Module 07 (§10).
*Evidence:* Two independent 2026 studies finding single agents match or beat multi-agent under matched budgets; ~15x token cost with spend explaining most of the variance; MAST 41–86.7% failure rates; role-based decomposition the least-supported common design; all three lenses tiered it optional at ~1h.
*Confidence:* **High** on budget-matching and the read/write rule; **medium** on the exact size of the cut.

**P1-7 · No competency is practised twice**
*Location:* structural — each competency appears in exactly one module.
*Problem:* No spiral, no interleaving, no unguided repetition following a guided one.
*Learner consequence:* Recognition of a procedure gets mistaken for the ability to produce it.
*Change:* Adopt the five cross-course strands (§11); require an unguided repetition on a different case within the same session as every guided lab.
*Evidence:* 15 of ~20 core competencies marked `practice-repeatedly` in all three models; desirable-difficulty literature on spacing and interleaving; "tutorial hell" as the dominant self-taught failure mode; the guided-lab rule at [`AUTHORING_GUIDE.md:147-158`](../../reformation/AUTHORING_GUIDE.md) already states this principle but no module enforces it.
*Confidence:* **High.**

**P1-8 · Transfer is confined to the capstone**
*Location:* transfer appears at [`09-capstone.md:112-131`](../../reformation/modules/09-capstone.md) only.
*Problem:* No per-module transfer seed; the legacy course had dated seeds at every closeout assembled into horizons.
*Learner consequence:* Delay between learning and application predicts abandonment.
*Change:* One dated seed per module (§9G).
*Evidence:* Transfer factors with real support include early opportunity to apply and success on first attempts; implementation intentions bound to real triggers outperform generic plans; `operator/TRANSFER_GATES.md` documents the mechanism that was dropped.
*Confidence:* **High.**

**P1-9 · Module sizing is not achievable**
*Location:* Modules 04, 05, 06, 08 — 8 stages and 10–11 evidence items each in 90–180 min.
*Change:* Split 04 and 07; halve 05; trim 06 and 08 (§8, §10).
*Evidence:* Cognitive load and expertise reversal; three independent estimates of 36–40 h for narrower coverage; the internal arithmetic (module times sum to 14.5–22.5 h against a stated 18–26 h).
*Confidence:* **High.**

### `P2 — meaningful improvement`

**P2-1 · Recovery notes collected once, practised eight times.** [`00:115`](../../reformation/modules/00-setup.md) is the only module requiring `RECOVERY_NOTE.md`. Add it to every module that plants or encounters a failure. Confidence: **high**.

**P2-2 · No fresh-session recurrence proof.** [`GETTING_UNSTUCK.md:98-111`](../../reformation/GETTING_UNSTUCK.md) step 7 and [`THINKING_PATTERNS.md:111-123`](../../reformation/THINKING_PATTERNS.md) #9 state the principle; nothing tests it. Recurrence in a fresh session is the only objective test of whether a fix landed, and misalignment self-persists across adjacent sessions well above chance. Confidence: **high**.

**P2-3 · Module 08 accepts a fresh session as person-transfer.** [`08:133`](../../reformation/modules/08-evaluate-change.md) accepts *"a fresh reviewer session or another person"* interchangeably, while [`09:116-117`](../../reformation/modules/09-capstone.md) correctly refuses to. Require a live listener, passing only on unprompted restatement of the fitness verdict. The legacy course's 90-second defense had exactly this pass condition. Confidence: **high**.

**P2-4 · Fine-tuning residue in Module 08.** Prune [`08:53`](../../reformation/modules/08-evaluate-change.md) and [`08:129-131`](../../reformation/modules/08-evaluate-change.md); retain the decision rule at [`08:21`](../../reformation/modules/08-evaluate-change.md) and add the *form, not facts* framing plus a written decline. Confidence: **high**.

**P2-5 · Model-and-cost choice is a listed decision artifact that no module requires.** [`AUTHORING_GUIDE.md:139`](../../reformation/AUTHORING_GUIDE.md) lists it; [`TOOLS_AND_METHODS.md:112-122`](../../reformation/TOOLS_AND_METHODS.md) covers it as reference reading. The routine per-step choice is a weekly decision; only the heavyweight formal comparison (Module 08) is taught. Add a one-paragraph model-placement decision to Module 02's brief. Confidence: **medium** — the durability lens argued most cost material expires; the surviving unit (spend per outcome that cleared the bar) is small and worth one paragraph, not a module.

**P2-6 · Two overlapping fault taxonomies, neither ordered by cheapness.** [`GETTING_UNSTUCK.md:35-47`](../../reformation/GETTING_UNSTUCK.md) (8 stuck states) and [`08:88-97`](../../reformation/modules/08-evaluate-change.md) (7 failure layers). Reconcile into one ordered list of ~5 classes, cheapest and most controllable first, so "the model is wrong" is structurally the last available conclusion. Confidence: **high**.

**P2-7 · Live in-flight correction survives as half a sentence.** [`02:55`](../../reformation/modules/02-direct-repeatable-work.md) — *"interrupt with one precise correction"* — was a distinct legacy capability with its own mastery description. It is a high-frequency operator move. Name it and assess it in Module 02. Confidence: **medium**.

**P2-8 · Constraint budgeting absent.** Joint compliance falls roughly geometrically in the number of stacked constraints, and violations are silent. Add constraint counting and precedence declaration to Module 02's brief. Confidence: **high**.

**P2-9 · Supersession is implicit.** [`06:43`](../../reformation/modules/06-durable-state.md) has a status field including "superseded" but never states the mechanism: one current value per (thing, property), replaced by recency and structure, never by similarity. Deterministic supersession cut stale-fact error from 15–40% to ~0% while embedding similarity separated contradictions from duplicates at near chance. Confidence: **high**.

### `P3 — polish`

- **P3-1** · `EVIDENCE_RECORD.md` is named as the index in [`README.md:17`](../../reformation/README.md) and [`COURSE_MAP.md:5`](../../reformation/COURSE_MAP.md) but no module's evidence list references it. Confidence: high.
- **P3-2** · Merge the two identical seven-level ladders ([`COURSE_MAP.md:62-70`](../../reformation/COURSE_MAP.md), [`AUTHORING_GUIDE.md:96-104`](../../reformation/AUTHORING_GUIDE.md)). Confidence: high.
- **P3-3** · Reconcile the 9-question and 12-item module shapes. Confidence: high.
- **P3-4** · Add the falsifier ("what would a wrong result look like", currently only in [`THINKING_PATTERNS.md:12`](../../reformation/THINKING_PATTERNS.md)) as a required `DIRECTION_BRIEF.md` field. Confidence: high.
- **P3-5** · Module time estimates do not sum to the stated course total. Confidence: high.
- **P3-6** · Trim `PATTERN_CATALOG.md` from 14 patterns to ~7. Confidence: medium.
- **P3-7** · State the unstated prerequisite — the learner brings a real recurring task — in `README.md`. Confidence: high.

---

## 13. What not to change

An indiscriminate rewrite would most likely damage these. Each is better than its equivalent in the comparable material reviewed.

1. **The five-layer separation rule** ([`AUTHORING_GUIDE.md:13-22`](../../reformation/AUTHORING_GUIDE.md)) and the fixture-check-vs-competency-check distinction ([`86-94`](../../reformation/AUTHORING_GUIDE.md)). This is the skeleton's reason for existing.
2. **`HOLD` as a supported result, with its boundary** ([`README.md:45-53`](../../reformation/README.md)). Do not simplify this into a pass/fail. The boundary clause — cannot claim the competency until the material check passes — is what keeps it honest.
3. **"Model self-assessment is not proof"** ([`README.md:41`](../../reformation/README.md)) and Module 00's open-the-file-yourself instruction ([`00:64`](../../reformation/modules/00-setup.md)).
4. **The advice / enforcement / authority distinction** ([`TOOLS_AND_METHODS.md:40-48`](../../reformation/TOOLS_AND_METHODS.md)), particularly the "always/never is still advice" sentence.
5. **Loaded / triggered / executed / bypassed, with "do not infer the state from silence"** ([`03:78-89`](../../reformation/modules/03-control-layers.md)).
6. **The discriminating-probe test** ([`GETTING_UNSTUCK.md:70-84`](../../reformation/GETTING_UNSTUCK.md)). The best sentence in the curriculum.
7. **Baseline saved and measures written before the baseline is read** ([`05:19-32`](../../reformation/modules/05-divide-and-govern.md)). Keep this even while shrinking the module around it.
8. **Refutation over confirmation, and votes are not truth** ([`05:79-89`](../../reformation/modules/05-divide-and-govern.md)).
9. **The bounded containment claim** ([`06:116`](../../reformation/modules/06-durable-state.md)).
10. **The evidence boundary as the top assessment level** ([`COURSE_MAP.md:70`](../../reformation/COURSE_MAP.md)) and the "what this does not prove" column in `EVIDENCE_RECORD.md` and `HANDOFF.md`.
11. **Module 01 entirely.** Prediction before the run, product used for its real job, four checks, changed input with prediction first, explicit guided-experience labelling.
12. **Fresh session is restartability, not person-transfer** ([`09:116-117`](../../reformation/modules/09-capstone.md)). Propagate this to Module 08 rather than relaxing it.
13. **"Do not hide a selection problem by instructing the harness to call a specific tool"** ([`04:96`](../../reformation/modules/04-tool-boundaries.md)).
14. **"Repair the direction, method, or implementation, then rerun"** ([`02:81`](../../reformation/modules/02-direct-repeatable-work.md)).
15. **The guided-lab rule** ([`AUTHORING_GUIDE.md:147-158`](../../reformation/AUTHORING_GUIDE.md)) — a copy-and-run lab is *"guided experience, not independent mastery."* Enforce it harder rather than softening it.
16. **The vendor-neutral language rules** ([`AUTHORING_GUIDE.md:106-117`](../../reformation/AUTHORING_GUIDE.md)), especially *"Explain what a command or component does. Do not tell learners they do not need to understand it."*

---

## 14. Blind spots and unresolved questions

**Delivery mode was not settled and it changes several recommendations.** Facilitated cohort, self-paced with an adapter, or a hybrid. The graded-localization lab (P1-1) needs a debrief responsive to each learner's actual path — the configuration where scripted post-mortems produced null results. If that is unaffordable, substitute worked examples with fading and accept slower acquisition. The second-harness port (A5) is only affordable if the cohort shares one primary harness.

**Cohort prior-knowledge spread was not assessed.** "Capable but not necessarily developers" spans a systems administrator and a lawyer. The expertise reversal effect makes a single fixed-pace path wrong for that mix by construction. If the spread is wide, the module sizing recommendations understate the problem and a diagnostic-plus-skip-ahead structure matters more than anything in §11.

**Where the three lenses disagreed, I chose and the choice is contestable.** The durability lens cut context management from core entirely, arguing that every operator *action* it implies is capability-graded scaffolding whose benefit is inversely proportional to model strength — a well-supported argument. The other two kept the reset-survival diagnostic. I kept the diagnostic and excluded the craft (P1-2). If you believe models will manage their own context reliably within the course's revision cycle, cut P1-2 to a single demonstration.

**The multi-agent cut could be too deep.** The budget-matched studies cover specific task families (multi-hop reasoning, particular benchmarks). If your learners' real work is genuinely breadth-first search over independent sources — the one shape where the gains are large and measured — Module 05 deserves more than an optional branch. The safe version of the recommendation is the two mechanism fixes (budget-matching, read/write asymmetry), which are correct regardless of how much time the module gets.

**Several load-bearing figures are vendor telemetry from one product.** The 93% approval rate, the novice/expert abandonment gap, the multi-agent token multiplier, and the description-refinement accuracy gains all come from vendors with an interest. The directions are corroborated across sources; the magnitudes should not be taught as facts.

**Two widely cited numbers could not be traced to primary studies:** the 60%-single-run-to-25%-across-eight-runs agentic degradation figure, and the ~37% lab-to-deployment benchmark gap. The practices they motivate (run it more than once; consistency across runs is the acceptance standard) are supported by other evidence. Do not quote the numbers.

**The METR finding cuts both ways and is used carefully here.** The 2025 result (19% slower, believed 20% faster) and the 2026 follow-up (~18% speedup with later tooling) point in opposite directions. The recommendation (P0-2) rests on the *perception gap*, which both datasets support, not on the direction of the productivity effect.

**Legacy material was consulted for lost mechanisms only.** `operator/CAPABILITIES.md`, `operator/MEASUREMENT_SPINE.md`, and `operator/TRANSFER_GATES.md` surfaced four droppings worth restoring (calibration/overclaim tracking, per-module transfer seeds, the human-listener defense, the fixed-workflow rule-change mechanic). I did not audit the legacy course for quality and no recommendation rests on preserving legacy material for its own sake.

**Not assessed:** whether learners can actually complete Module 04a's capability work through configuration alone in a real harness — that depends entirely on the adapter you build, which is exactly why P0-3 matters. Also not assessed: accessibility of the delivered artifacts, which [`AUTHORING_GUIDE.md:167`](../../reformation/AUTHORING_GUIDE.md) names in the cross-cutting release check but no module operationalises.

---

## Report

**File written:** [`docs/analysis/2026-08-08-reformation-curriculum-review.md`](2026-08-08-reformation-curriculum-review.md). No other file in the repository was modified.

**External sources used:** 187 unique sources collected across 10 parallel research sweeps (435 tool calls). By type: 41 peer-reviewed or preprint studies (learning science, agent failure taxonomies, evaluation methodology, security, retrieval); 38 vendor engineering and documentation sources (Anthropic, OpenAI, MCP specification, LangChain, Chroma); 22 standards and security-guidance sources (OWASP GenAI project, NIST AI RMF, MCP security specification, CVE disclosures); 31 named-practitioner sources (Husain, Shankar, Willison, Cognition, Osmani); 29 field-telemetry and industry-study sources (METR, DORA, MIT NANDA, PwC, Gartner, HBR/BetterUp); 26 secondary commentary sources used for direction only. 62 are tabulated in §3 as directly supporting a claim made here.

**Five highest-confidence findings**

1. **Error analysis is absent and is the largest gap** (P0-1). Verified by search across all 23 files; made core by all three independent competency models; named the highest-yield evaluation activity in practitioner guidance; requires no code, which makes it the strongest argument that this learner belongs in this work.
2. **No calibration instrument exists** (P0-2). Zero matches for any form of predict-then-measure. The legacy course had one and it was dropped. The perception–performance gap in AI-assisted work is large, measured, and runs in the confident direction.
3. **Diagnosis is rehearsed eight times and tested zero times** (P1-1). Every planted failure is planted by the learner; localization is never graded separately from repair. This is the exact configuration that produced null results in the productive-failure replication literature.
4. **The course is over-volume by roughly a factor of two** (P1-9). Modules 04, 05, 06, and 08 carry 8 stages and 10–11 evidence items each in 90–180 minutes; three independent models estimated 36–40 hours for narrower coverage against a stated 18–26.
5. **Context is a named harness part whose defining operational property is never taught** (P1-2). Twelve occurrences in 2,807 lines, always meaning "source material available," never "a budget that degrades." The compaction failure — a correctly-sorted rule silently ceasing to hold — is precisely the failure mode Module 03's sort exists to prevent.

**Sources or searches not accessed**

- Several 2026 arXiv entries were read via HTML abstract and body rather than PDF; page-level citation was not possible for those.
- The MIT NANDA "GenAI Divide" report was reached through secondary coverage only; the primary PDF was not retrieved. Its headline figure is widely contested and is used here for mechanism, not magnitude.
- The Anthropic AI Fluency course content behind the Skilljar enrolment wall was not accessed; the framework description comes from the public landing page.
- Two circulated statistics (single-run vs eight-run agentic degradation; lab-to-deployment benchmark gap) could not be traced to primary studies and are excluded from the recommendations.
- No paywalled academic sources were purchased; where only an abstract was available (Kalyuga & Renkl 2009; ICER 2023), the claim is limited to what the abstract states.
