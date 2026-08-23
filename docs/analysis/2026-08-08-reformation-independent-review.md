# Independent Review of Reformation

**Target:** `reformation/` — 32 files, 6,966 lines (8 architecture documents, 13 core modules `00–12`, 3 advanced extensions, 8 templates)
**Reviewed:** 2026-08-08
**Repository changes by this review:** this document only.

---

## 1. Executive verdict

**Rating: `READY WITH TARGETED REFINEMENTS`.**

The curriculum can serve as an implementation build specification. A competent team could build most of it from these files without inventing the durable mechanism, and — unusually — the specification anticipates most of the ways a team would accidentally destroy that mechanism while satisfying the prose. The per-module adapter obligation matrix ([`AUTHORING_GUIDE.md:88-102`](../../reformation/AUTHORING_GUIDE.md)), its five interpretation rules ([`104-111`](../../reformation/AUTHORING_GUIDE.md)), and the release gates ([`COURSE_MAP.md:102-113`](../../reformation/COURSE_MAP.md)) are load-bearing and genuinely good.

**Strongest design choice.** Separating *what the adapter supplies* from *what the learner authors, configures, and decides*, per module, defended by rule 5 — *"The adapter supplies mechanics, not judgment"* ([`110`](../../reformation/AUTHORING_GUIDE.md)) — and rule 4's definition of hidden as hidden from **both** learner and system under test ([`109`](../../reformation/AUTHORING_GUIDE.md)). This is what stops "adapter support" collapsing into click-through, and it is enforced in every module rather than asserted once.

**Largest remaining risk.** Several decisive gates are **single-instance measurements treated as verdicts**: the calibration gap (one matched pair at Module 00, one at Module 12), person transfer (one recipient), and localization (four hidden cases). Calibration is the worst. Grading the *size* of a prediction gap, then comparing Module 00 gap size with capstone gap size, is a difference-score comparison against a noisy measured quantity — it will show improvement by regression to the mean whether or not any calibration occurred, and hedging every prediction toward zero is close to score-maximizing. That is the one place the specification will produce confident, invalid evidence.

**Five highest-priority findings**

1. **`P0` — The calibration instrument cannot measure calibration as specified** ([`README.md:56-65`](../../reformation/README.md), [`00:33-46`](../../reformation/modules/00-setup-calibration.md), [`CALIBRATION_RECORD.md:166-175`](../../reformation/templates/CALIBRATION_RECORD.md)). Score the accumulated per-module closeout predictions and their recorded confidence values; retire the two-anchor gap comparison as the headline claim.
2. **`P1` — Four hidden cases cannot carry a localization verdict, and layer naming is the grade's least reliable dimension** ([`04:175-193`](../../reformation/modules/04-hidden-diagnosis.md)). Published expert agreement on bug-cause categories runs κ 0.31–0.46; four-item diagnostic samples sit near 0.2–0.4 reliability. Report localization cumulatively across the course, or raise the count and calibrate graders.
3. **`P1` — The two-proof conditional design has no positive-case counterweight and no ground truth for "correctly declined"** ([`README.md:42`](../../reformation/README.md), [`COURSE_MAP.md:76`](../../reformation/COURSE_MAP.md)). Declining is the cheap default; an all-declines record cannot distinguish discernment from avoidance.
4. **`P1` — Transfer-seed schema compliance is broken in 11 of 16 modules**, breaking the capstone artifact that consumes them ([`12:317-335`](../../reformation/modules/12-capstone.md)).
5. **`P2` — Six internal-consistency defects**: `(thing, property)` vs `(entity, property)`; ambiguous `cold` used 19 times against the guide's own ban; Module 09's prerequisite differs between course map and module; Module 12 restates the evidence ladder the course map reserves; the `Required closeout` line lacks a trailing `<br>` in all 16 modules; `**Path:**` is undeclared and appears in three.

**What should not change.** The obligation matrix and its interpretation rules. The hidden-fault security section. The independent-check definition. The two transfer claims and their non-substitutability. Module 05 in full. Module 04's refusal to credit a guessed repair. Module 11's replacement held-back set. The `HOLD` boundary. Every evidence-boundary section.

---

## 2. Review method and independence statement

**Files read.** All 32 files under `reformation/`, in full: 8 architecture documents (`README.md`, `COURSE_MAP.md`, `AUTHORING_GUIDE.md`, `TOOLS_AND_METHODS.md`, `THINKING_PATTERNS.md`, `GETTING_UNSTUCK.md`, `PATTERN_CATALOG.md`, `EVIDENCE_RECORD.md`); 13 core modules `00–12`; 3 advanced extensions; 8 templates.

**Research performed.** Seven parallel adversarial sweeps, each assigned one specific assessment-design claim the revised curriculum makes, each instructed to hunt disconfirming evidence and to enumerate the concrete ways an implementation team could satisfy the stated design while losing its effect. 274 tool calls, 118 unique sources. Areas: calibration measurement; selection-versus-operation two-proof design; person transfer and restatement gates; graded first-divergence localization; non-developer declarative configuration competence; bounding negative security claims; simulation-versus-executed evidence including reset-versus-compaction mechanics.

**Subagents.** Seven research agents in one workflow. Their returns were structured claims plus source URLs; I read every finding and every enumerated failure mode myself and made every judgment in this review. Where a research claim seemed too strong I narrowed it — the calibration finding, for example, is stated more narrowly here than the research returned, because the per-module closeout row in `CALIBRATION_RECORD.md` supplies a dose the research agent did not see.

**Mechanical checks** were run directly by me in the shell, not delegated: relative-link resolution, anchor-target resolution, H1 extraction, header-field extraction across all 16 modules, terminology greps, and transfer-seed schema compliance. Commands and results are in §13.

**When the previous review was opened.** After completing the file reading, the research, the mechanical checks, and my provisional findings and verdict — at Phase 8, as required. It informed only §14.

**How anchoring was controlled — and its honest limit.** I wrote the previous review earlier in this same session, so I could not be blind to it and I do not claim to have been. What I did control: I reconstructed the course from the current files rather than from the prior document; I commissioned new research aimed at the *current* design's specific claims rather than re-using the earlier corpus to re-litigate earlier findings; and the highest-priority finding in this review (§8, `P0-1`) **contradicts a recommendation the previous review made and this team implemented faithfully**. A review that only confirmed its predecessor would be the warning sign; this one does not.

**Limitations.**

- No adapter exists, so every claim about learner experience is a claim about the specification, not about observed learners. The specification says so itself ([`README.md:9`](../../reformation/README.md)).
- Reliability figures borrowed from medical and computing-education assessment are analogies, not measurements of this course. They bound what a given number of observations *can* support; they do not predict this cohort.
- I did not attempt to price or schedule the curriculum, per the brief.
- Two research areas returned findings I could not independently verify against primary sources within this session and are flagged `medium` confidence where used.

---

## 3. Intended learner and end state

The hypothesised profile survives contact with the files, with two refinements.

**Confirmed.** The learner brings *"one real, recurring, low-risk task from their own domain"* and *"willingness to make and defend consequential decisions rather than delegate them"* ([`README.md:13-18`](../../reformation/README.md)). Software development is explicitly not a prerequisite ([`20`](../../reformation/README.md)). The non-developer standard is operationalised, not asserted: six named accessible routes, and a floor of five things the learner must do regardless of route ([`AUTHORING_GUIDE.md:123-134`](../../reformation/AUTHORING_GUIDE.md)).

**Refinement 1 — the learner is an *evidence* worker before they are an AI operator.** Across 13 modules the dominant learner action is not configuring a harness; it is authoring a falsifiable expectation, preserving a raw artifact, and refusing to accept a summary. Someone comfortable with tools but uncomfortable holding an unresolved `HOLD` against schedule pressure will fail this course at Module 02, not Module 09. This is a defensible target, but it should be stated in admissions.

**Refinement 2 — the core is not fully non-developer-neutral at Module 07.** The learner must author *"the production outcome, branch table, structured model contract, exception policy, finish condition, rule and its one owning location"* ([`07-fixed-workflow.md:58`](../../reformation/modules/07-fixed-workflow.md)) and maintain a versioned workflow specification with input schemas and allowed classifications ([`64-76`](../../reformation/modules/07-fixed-workflow.md)). This is schema and policy authorship. It is genuinely within reach of a capable analyst working in a declarative surface, and the adapter is required to supply the runner — but it is the highest authorship demand in the core and the specification does not flag it as such.

**End state.** The nine end-state claims ([`README.md:131-141`](../../reformation/README.md)) are each traceable to a module and to a material proof. That traceability is rare and worth preserving. The one claim that outruns its evidence is *"calibrate confidence against matched evidence"* — see `P0-1`.

---

## 4. Independent competency model

Derived from the current files plus the seven adversarial research sweeps, before comparison. Each competency states what the learner must do, the observable mastery evidence, whether guided exposure suffices, whether repetition is required, and what may remain adapter-specific.

### Foundational — precede all consequential work

| # | Competency | Must be able to | Mastery evidence | Guided enough? | Repeat? | Adapter-specific |
|---|---|---|---|---|---|---|
| F1 | **Bound reach before acting** | Enumerate readable private data, untrusted ingress, effects, egress channels, and acting identity as *actual channels*, not labels; remove one leg; show the task still works | Before/after inventory, worst-case statement, passing run under the narrower bound | No | Every capability change | Where configuration lives; egress observation |
| F2 | **Restore from a bad run** | Take a labelled snapshot, break something, restore by the recorded action rather than hand repair, and state what the snapshot cannot undo | Demonstrated restore + list of uncovered effects | No | Yes | Snapshot/rollback mechanics |
| F3 | **State acceptance and falsifier before execution** | Name the artifact, the observable acceptance condition, a plausible polished-but-wrong result that must fail, and the stop condition | Timestamped pre-run record another person could apply | No | Every module | Where it is recorded |
| F4 | **Predict, observe, and confront the gap** | Record a committed numeric prediction before an outcome; compare it with an independently scored result; state what belief changed | An accumulating series of predictions with confidence values, scored against outcomes | No | **Many small instances, not two large ones** | Timing/counting instrument |
| F5 | **Refuse the producer's self-report** | Inspect the source of record before reading the summary | Record naming claim, independent artifact consulted, verdict; at least one caught disagreement | No | Every module | Which command reveals the record |

### Core

| # | Competency | Must be able to | Mastery evidence | Guided? | Repeat? |
|---|---|---|---|---|---|
| C1 | **Author a checkable brief with counted constraints and declared precedence** | Number every requirement, classify it, declare collision precedence, freeze before execution | Frozen brief; constraint count; precedence list; a collision actually resolved | No | Yes |
| C2 | **Give the decisive check an owner the producer cannot reach** | Freeze it, protect it, and demonstrate that a tampering attempt is refused or visible | Tamper attempt result + protection mechanism | No | Yes |
| C3 | **Place a requirement in advice, enforcement, or authority — and prove what survives a context boundary** | Sort each requirement; run the same rule conversation-only and durably reloaded across a real boundary; inspect resolved state | Matched pair of transcripts with resolved-state evidence on both sides | No | Yes |
| C4 | **Localize first divergence in an unfamiliar harness before repairing** | Write boundary expectations, bracket, run a discriminating probe, seal the localization | Sealed pre-repair localization graded against a key, separately from repair | No | **Many cases, interleaved** |
| C5 | **Derive a counted failure taxonomy from real runs** | Outcome-blind sample, first-failure-only free-form notes, categories after observation, counts, ranked, saturation stated | Raw notes, visible rubric revision, counts, ranking, saturation status | No | Yes |
| C6 | **Convert the leading failure into a validated deterministic check** | Freeze known-bad and known-good artifacts, author the narrowest mechanical condition, prove three directions | Known-bad fails, known-good passes, missing input fails visibly | No | Yes |
| C7 | **Repair the durable surface and prove non-recurrence in a clean session** | Change one owning surface, revert failures, reproduce original conditions without the repair conversation | Clean-session rerun + frozen known-bad still failing | No | Yes |
| C8 | **Read raw configuration and capability descriptions as executable content** | Inspect manifests inert, catch instruction-bearing content, pin versions, set a re-review trigger | Sealed finding before the answer key; pinned identity | No | Yes |
| C9 | **Budget approvals prospectively** | Set a ceiling and exhaustion behavior *before* the run; make dangerous actions unavailable; keep few gates showing the raw action | Prospective ceiling, before/after counts, observed rate, exhaustion case reaching a gate or `HOLD` | No | Yes |
| C10 | **Operate a saved fixed workflow through a rule change** | One rule, one owning location, predicted exact blast radius, zero per-record repair, second wave through the same artifact | Record-and-field diff matching the frozen prediction; manual-repair count zero | No | Yes |
| C11 | **Bound a negative claim to what was observed** | State containment, canary, recurrence, and comparison results with their observed channels, cases, and versions | Every claim carrying its scope in the same sentence | No | Every module |
| C12 | **Hand off with attached evidence and a stated unverified boundary** | Acceptance, raw check output, what was not verified, owner, run/rollback action, next trigger | Recipient can say what was verified without asking | No | Yes |
| C13 | **Choose the smallest sufficient rung and preserve the simpler one** | Name the observed failure of the lower rung before adding machinery; compare under matched opportunity | Recorded failing simpler run + budget-matched comparison | No | Yes |

### Conditional core — selection and operation are distinct claims

| # | Competency | Selection evidence | Operation evidence |
|---|---|---|---|
| K1 | **Governed durable state** | Reasoned non-adoption for own workload, or adoption with named cross-session requirement | Sanctioned boundary, one current value per exact `(entity, property)`, deterministic supersession, five cold-retrieval cases, integrity mutation detected |
| K2 | **Bounded adaptive flow** | Named condition the fixed path cannot branch on in advance | Two waves against one control-state record, budgets enforced, six unattended cases terminating safely, clean resume |
| K3 | **Divided work** | Complexity claim with a preserved simpler-rung failure and an independence matrix | Budget-matched baseline, one writer per shared artifact, refutation dispositions, attributed synthesis re-checked against the pinned gate |

### Advanced

A1 authoring and operating a callable capability lifecycle; A2 mechanism transfer to a second enforcement plane (distinct from relocation); A3 governed post-training from rights through removal. Each requires maintained code or named accountable owners and is correctly outside the core.

### Out of scope

Building retrieval pipelines; orchestration framework design; protocol wire-format implementation; judge-validation statistics; observability platform construction; numbered risk taxonomies as syllabus.

### Assessment-grade distinctions the model requires

Conceptual recognition → guided execution → independent selection → independent configuration → **diagnosis** → **recurrence-proved repair** → restartability → **person transfer**. The last three are separable and the specification is right to separate them. The model adds one constraint the curriculum does not currently honour: **no single observation supports a competency verdict** — a principle that applies to F4, C4, and person transfer alike.

---

## 5. Module reconstruction matrix

Reconstructed from the module files themselves and cross-checked against the obligation matrix. `HF` = instructor-only hidden fixture required.

| Module | Skill | Learner authors | Learner configures | Learner decides | Adapter supplies | Hidden/protected | Independent evidence | Recovery / recurrence | Transfer gate |
|---|---|---|---|---|---|---|---|---|---|
| **00** Setup & calibration | Bound, calibrate, restore, localize | Prediction; harness map; reach inventory; rollback limits; setup record ([`29`](../../reformation/modules/00-setup-calibration.md)) | Workspace boundary; endpoint values; secret reference; snapshot label; narrower reach | Whether evidence permits work; which leg to remove; `HOLD` | Two matched tasks; external rubric+scorer; canary fixture; capture sink; hidden setup fault ([`20-27`](../../reformation/modules/00-setup-calibration.md)) | Fault key; calibration rubric; dummy canary | External rubric; watched check failure; canary sink | `RECOVERY_NOTE` + reset-fixture reproof ([`176-180`](../../reformation/modules/00-setup-calibration.md)) | Fresh |
| **01** Guided first result | Judge a run against sources, known answers, use, change | Predictions; check notes; harness map; decision; evidence boundary | Supplied input + one changed input only | `RELEASE`/`FIX`/`HOLD`; guided vs mastery | Scenario; direction; run action; 4 protected checks; **matched analogous fixture** ([`32`](../../reformation/modules/01-guided-first-result.md)) | Expected deltas; answer key; one fluent-but-wrong artifact | Known-answer, source-trace, functional, scope; harness may not alter checks ([`101`](../../reformation/modules/01-guided-first-result.md)) | Recovery note + fresh reproof ([`145`](../../reformation/modules/01-guided-first-result.md)) | Fresh |
| **02** Direct work | Bounded rerunnable product with a protected check | Brief; falsifier; numbered constraints + precedence; source contract; checks; runbook; failure-design card | Sources; model placement; bounds; check invocation; one input change | Precedence; decisive check; live correction vs restart; release | Run skeleton; source fixture; **checker frozen before build**; disposable copy; usage reporting | Gate-tampering case; bad input with undisclosed expected failure | Builder cannot alter checks + planted tamper attempt ([`149`](../../reformation/modules/02-direct-work.md)) | Recovery note + **fresh fixture and fresh session** ([`189`](../../reformation/modules/02-direct-work.md)) | Fresh |
| **03** Context & control | Context as degrading budget; advice/enforcement/authority; reset survival | Context inventory; precedence; control map; procedure; guard policy; survival rule | Activation; scope; triggers; permission bounds; reload; port mapping | Advice vs enforced vs impossible; what must survive reset | Resolved-state view; **real compaction control in ≥1 reference adapter**; guard skeleton; second harness or `NOT SUPPORTED` | One unknown load/trigger/execute/bypass defect; expected matched-pair behavior | Matched A/B transcripts; resolved-state evidence | Recovery note + reset-fixture reproof ([`197`](../../reformation/modules/03-context-control-surfaces.md)) | Fresh |
| **04** Hidden diagnosis | First-divergence localization, graded before repair | Boundary expectations; probes; **sealed localization**; recovery notes | Nothing before sealing; one reversible repair after ([`45-47`](../../reformation/modules/04-hidden-diagnosis.md)) | Which boundary to probe; fault class; revert/escalate/stop | Unfamiliar harness; **≥5 case copies, ≥4 fault classes, interleaved**; sealed answer key; responsive debrief ([`22-34`](../../reformation/modules/04-hidden-diagnosis.md)) | **HF** — identities, locations, seeds, class order, scoring key | Instructor key vs sealed diagnosis; 10-point localization rubric | Fresh-session recurrence + frozen known-bad still fails ([`157-169`](../../reformation/modules/04-hidden-diagnosis.md)) | Fresh |
| **05** Error analysis | Counted taxonomy from real runs → validated check | Sample rule; free-form first-failure notes; codebook; revision log; counts; check condition | Sample selection; redaction; label sheet; check scaffold | What is material; first failure; splits/merges; saturation; top three | 20–40 real-run export or authentic corpus; blank labeling workspace; check runner; **instructor never supplies the taxonomy** ([`AUTHORING_GUIDE.md:95`](../../reformation/AUTHORING_GUIDE.md)) | Audit sample; ambiguous run; checker key; original failure conditions | Independent evidence per run; three-way check validation | Fresh-session non-recurrence ([`193-205`](../../reformation/modules/05-error-analysis.md)) | Fresh |
| **06** Tool boundaries & approval | Bound, select, contain, revoke | Review; boundary card; reach revision; selection fixtures; approval budget | Descriptions; allowed data; output limits; scoped credential; gates | Attach/decline; primitive; authority; acceptable worst case | ≥2 candidates + raw manifests; denied-write path; scoped dummy identity; canary + sink; withheld cases | Planted instruction in manifest/config; hidden instruction in returned content; expected selection per case | Selection traces; approval event log; egress logs; post-removal probe | First-divergence + one change + fresh rerun ([`252`](../../reformation/modules/06-tool-boundaries-approval.md)) | Fresh |
| **07** Fixed workflow | Operate a saved path through a rule change | Outcome; branch table; model contract; exception policy; rule + owning location; expected delta | The shell; the one rule; branch values; batch source; stop/rollback | Fixed vs hybrid; which exceptions go to a person; delta exactness; release | Runner with visible graph; batch; declarative rule location; protected gates; diff tooling; **row-edit detector**; hidden case | Changed-rule request; second wave; gate tamper; expected affected/unaffected fields | Independent expected-outcome fixture; row-edit audit | Sealed localization then smallest owning artifact ([`141`](../../reformation/modules/07-fixed-workflow.md)) | Fresh |
| **08** Durable state | Admission, provenance, deterministic supersession, integrity | Trust/write/authority/identity/correction/deletion policies; retrieval questions; containment statement | Schema; current-value rule; retrieval suite; dispositions | Admissibility; identity resolved?; duplicate vs contradiction vs supersession; repair | Store with staging/governed/history/current surfaces; **deterministic `(entity, property)` supersession**; integrity root outside writer authority; hidden case | Hostile/contradictory/stale/unauthorized-write/post-snapshot mutation; expected integrity signal | Five frozen cold cases; source-snapshot audit walk; externally held integrity root | Disposable copy; classify first failing boundary; fresh reproof ([`191-195`](../../reformation/modules/08-durable-state.md)) | Fresh |
| **09** Adaptive flow | Bounded adaptive control under budgets | Fixed-rung failure; mission; state fields; budgets; stop/replan; hand-back | Allowed actions; state transitions; ceilings; verifier; restart point | Whether evidence warrants a changed next action; whether adaptation earned use | P3 runner; control-state schema; two waves; timeout/duplicate/partial/orphan/cancel/resume fixtures; hidden control-flow fault | Wave-2 event set; state-corruption case; trigger withheld until Wave 1 frozen | Frozen verifier; receipts; budget counters | Sealed localization then owning boundary; clean-session resume ([`139`](../../reformation/modules/09-adaptive-flow.md)) | Fresh |
| **10** Multi-agent | Divide only on earned complexity; govern ownership | Complexity claim; acceptance; briefs; independence matrix; merge rule | Read/write boundaries; budget allocation; merge invocation | Whether work separates; conflict handling; adopt/simplify/remove | Isolated contexts; **budget meter and matching controls**; one-writer enforcement; protected evaluator identity; pinned gate manifest | Duplicated-source trap; conflicting supported finding; unauthorized shared write; unattended faults | Pinned immutable gate re-run against the **merged** artifact ([`178`](../../reformation/modules/10-multi-agent.md)) | Replacement hidden case after repair ([`150`](../../reformation/modules/10-multi-agent.md)) | Fresh |
| **11** Evaluate change | Frozen paired comparison → narrow fitness → rollback → person | Policy; behavior claim; gates; scoring guide; failure analysis; fitness statement; rollback trigger | Baseline/candidate profiles; frozen case invocation; thresholds; restoration | Whether comparison belongs; adopt/route/monitor/reject; residual risk | **≥2 exchangeable sealed held-back sets** ([`37`](../../reformation/modules/11-evaluate-change.md)); blinding support; cost receipts; hidden serving-path fault; listener protocol | Blinded arm identity; planted regression; tempting irrelevant improvement; listener answers | Held-back suite; blinded scoring; **unprompted listener restatement** ([`220-228`](../../reformation/modules/11-evaluate-change.md)) | Opened set becomes diagnostic; replacement set required for confirmatory claim ([`177`](../../reformation/modules/11-evaluate-change.md)) | **Person** |
| **12** Capstone | Whole method on unfamiliar work | Everything, plus recalibration prediction and seed-assembled transfer plan | Smallest sufficient supplied components | Architecture rung; admission; authority; hidden-fault response; release; recipient reliance | Clean P4 workspace; unfamiliar source pack; ≥3 fault classes with undisclosed selection; matched calibration pair; **separate recipient room, task, and rubric** | Material fault unknown to learner and to system under test; recipient rubric; calibration key | Ten-row independent evidence plan ([`377-388`](../../reformation/modules/12-capstone.md)) | Clean-session recurrence for **every** material failure | **Fresh + Person** |
| **Adv 01** Callable capability | Contract + lifecycle across failure modes | Contract; schemas; errors; retry/idempotency/cancellation/version policy | Bounds; authority; logging; host registration | Whether authorship is maintainable; which operations ship; release | Skeleton with empty logic; direct client; fault fixtures; compatibility runners | Hidden contract and selection tests; protected expected effects | Direct tests independent of host selection | Fresh-session recurrence after first-boundary repair | Fresh |
| **Adv 02** Port control | Mechanism transfer vs relocation | Policy without source-harness nouns; invariant fixtures; transfer ledger | Native control on both planes; trigger; denial path | Whether the mechanism transferred; whether either port ships | **Two genuinely different enforcement planes**; monitored allowed and forbidden sinks | Hidden bypass route + changed-input case per harness | Sink records on both sides, not refusal messages ([`174`](../../reformation/modules/advanced/02-port-control-second-harness.md)) | Localization graded separately; fresh reproof | Fresh |
| **Adv 03** Post-training | Rights → locked test → parity → reversible release → removal | Behavior spec; admission policy; split rules; checkpoint rule; monitoring plan | Approved data revision; training bounds; parity; rollout/removal | Whether post-training is justified; data admissibility; rollout/rollback | Governed workspace; split tooling; duplicate audit; **second locked set**; serving-parity environment | Leakage; rights failure; serving mismatch; base regression; incomplete removal | One locked paired test + broad base regression | Never reuse opened test evidence ([`271`](../../reformation/modules/advanced/03-post-training-evaluation.md)) | **Person** |

**Verified:** every obligation in this matrix is operationalised in the module file itself, not only in `AUTHORING_GUIDE.md`. I checked this specifically because the brief warns against inferring a requirement from the authoring guide alone. Two exceptions are noted in §8 (`P2-3`, `P2-6`).

---

## 6. Competency coverage matrix

| Competency | Priority | Where taught | Where assessed | Depth | Independent evidence | Verdict | Main issue |
|---|---|---|---|---|---|---|---|
| F1 Bound reach | Foundational | [`00:96-121`](../../reformation/modules/00-setup-calibration.md); [`06:130-149`](../../reformation/modules/06-tool-boundaries-approval.md) | 00, 06, 12 + every closeout | Independent configuration, repeated | Canary sink + enumerated channels | **STRONG** | Canary is a non-adaptive probe; see `P2-1` |
| F2 Restore | Foundational | [`00:144-152`](../../reformation/modules/00-setup-calibration.md) | 00; prerequisite for 04 | Independent, demonstrated | Restore action vs hand repair | **STRONG** | — |
| F3 Acceptance + falsifier | Foundational | [`DIRECTION_BRIEF.md:23-36`](../../reformation/templates/DIRECTION_BRIEF.md); strand 1 | Every module | Independent, repeated | Frozen before execution | **STRONG** | — |
| F4 Predict → confront gap | Foundational | [`README.md:56-65`](../../reformation/README.md); [`00:33-46`](../../reformation/modules/00-setup-calibration.md); [`CALIBRATION_RECORD.md`](../../reformation/templates/CALIBRATION_RECORD.md) | 00, every closeout row, 12 | Independent | External rubric + scorer | **INTERNALLY INCONSISTENT** | The per-module rows supply a usable series; the headline claim uses the two-anchor gap comparison the series makes unnecessary and that regression invalidates — `P0-1` |
| F5 Refuse self-report | Foundational | [`00:131`](../../reformation/modules/00-setup-calibration.md); strand 2 | Every module | Independent, repeated | Source of record | **STRONG** | — |
| C1 Counted constraints + precedence | Core | [`02:61-73`](../../reformation/modules/02-direct-work.md) | 02, 12 | Independent | Collision resolved, not deferred | **STRONG** | — |
| C2 Protected decisive check | Core | [`02:149`](../../reformation/modules/02-direct-work.md); [`AUTHORING_GUIDE.md:169-186`](../../reformation/AUTHORING_GUIDE.md) | 02, 05, 07, 10, 12 | Independent, repeated | Planted tamper attempt | **STRONG** | — |
| C3 Placement + reset survival | Core | [`03:49-63,122-144`](../../reformation/modules/03-context-control-surfaces.md) | 03, 12 | Independent | Matched A/B with resolved state | **PRESENT BUT THIN** | Simulation-only completion status undefined; single run on a probabilistic phenomenon — `P1-3` |
| C4 First-divergence localization | Core | [`04`](../../reformation/modules/04-hidden-diagnosis.md) entire; [`GETTING_UNSTUCK.md:37-118`](../../reformation/GETTING_UNSTUCK.md) | 04, 07, 08, 09, 10, 11, 12 | Diagnosis, repeated | Sealed vs answer key | **STRONG teaching / OVER-SPECIFIED claim** | Four cases cannot carry the verdict; layer naming least reliable dimension — `P1-1` |
| C5 Counted taxonomy | Core | [`05`](../../reformation/modules/05-error-analysis.md) entire | 05, 12 | Independent | Outcome-blind sample + independent evidence per run | **STRONG** | No minimum `FAIL` count, so ranking can be vacuous — `P2-2` |
| C6 Validated deterministic check | Core | [`05:170-191`](../../reformation/modules/05-error-analysis.md) | 05, 12 | Independent | Three-way validation on frozen artifacts | **STRONG** | — |
| C7 Durable repair + recurrence | Core | [`GETTING_UNSTUCK.md:131-143`](../../reformation/GETTING_UNSTUCK.md); every module | Every module | Diagnosis + recurrence | Clean session + known-bad still fails | **STRONG** | — |
| C8 Config as executable content | Core | [`06:93,166`](../../reformation/modules/06-tool-boundaries-approval.md) | 06, 12, Adv 02 | Independent | Sealed finding before key | **STRONG** | — |
| C9 Prospective approval budget | Core | [`06:174,192-200`](../../reformation/modules/06-tool-boundaries-approval.md) | 06, 12 | Independent | Event log + exhaustion case reaching a gate | **STRONG** | Exactly answers the "count without a ceiling" trap the brief names |
| C10 Fixed workflow through change | Core | [`07`](../../reformation/modules/07-fixed-workflow.md) entire | 07, 12 | Independent | Record-and-field diff + row-edit detector | **STRONG** | Highest authorship demand in core; not flagged — §3 |
| C11 Bounded negative claims | Core | Every module's evidence boundary | Every module | Independent, repeated | — | **STRONG** | The single best-supported design choice in the course |
| C12 Evidence-attached handoff | Core | [`HANDOFF.md`](../../reformation/templates/HANDOFF.md); strand 5 | Every module | Independent, repeated | Recipient can state what was verified | **STRONG** | — |
| C13 Smallest sufficient rung | Core | [`TOOLS_AND_METHODS.md:69-82`](../../reformation/TOOLS_AND_METHODS.md); [`09:73`](../../reformation/modules/09-adaptive-flow.md); [`10:74-82`](../../reformation/modules/10-multi-agent.md) | 09, 10, 12 | Independent selection | Preserved failing simpler run + matched budget | **STRONG** | — |
| K1 Governed durable state | Conditional core | [`08`](../../reformation/modules/08-durable-state.md) entire | 08, 12 | Independent implementation | Integrity root outside writer authority | **STRONG** | Key naming inconsistent — `P2-6` |
| K2 Bounded adaptive flow | Conditional core | [`09`](../../reformation/modules/09-adaptive-flow.md) entire | 09, 12 | Independent | Six unattended cases | **STRONG** | Two-proof gaming — `P1-2` |
| K3 Divided work | Conditional core | [`10`](../../reformation/modules/10-multi-agent.md) entire | 10, 12 | Independent | Pinned gate re-run on merged artifact | **STRONG** | Two-proof gaming — `P1-2` |
| Frozen comparison + person transfer | Core | [`11`](../../reformation/modules/11-evaluate-change.md) entire | 11, 12 | Independent + person | Held-back suite; listener restatement | **PRESENT BUT THIN** | N=1 recipient, author-adjacent scorer risk, no answer key required for the restatement — `P1-4` |
| Non-developer independent participation | Foundational | [`AUTHORING_GUIDE.md:123-136`](../../reformation/AUTHORING_GUIDE.md) | Release gate | Specification-level | Real-user testing required ([`COURSE_MAP.md:110`](../../reformation/COURSE_MAP.md)) | **PRESENT BUT THIN** | The five safeguards include two the evidence says are weak signals — `P2-4` |
| Simulation vs executed evidence | Core | [`README.md:94`](../../reformation/README.md); [`AUTHORING_GUIDE.md:225`](../../reformation/AUTHORING_GUIDE.md) | Every module | Independent | — | **STRONG, with one false clause** | "Only a special adapter can produce compaction evidence" is not true — `P1-3` |
| Transfer seed → plan | Core | Every closeout; [`12:317-335`](../../reformation/modules/12-capstone.md) | 12 | Independent | Dated, triggered | **INTERNALLY INCONSISTENT** | 11 of 16 modules replace the canonical schema — `P1-5` |
| Protocol internals / orchestration frameworks / retrieval build | Out of scope | Advanced only | — | — | — | **OUT OF SCOPE** | Correctly placed |

---

## 7. What is strong and should be preserved

1. **The matrix interpretation rules** ([`AUTHORING_GUIDE.md:104-111`](../../reformation/AUTHORING_GUIDE.md)). Five rules that convert an obligation table into an anti-degradation mechanism, especially rule 2 (*"Choosing a cosmetic option does not count"*), rule 3 (*"A decision needs a rejected alternative"*), rule 4 (hidden from **both** learner and system under test), and rule 5 (*"The adapter supplies mechanics, not judgment"*).
2. **The independent-check definition** ([`169-179`](../../reformation/AUTHORING_GUIDE.md)), ending with *"A second model repeating the same sources and assumptions is not automatically independent. Consensus is not a substitute for provenance or a counterexample."*
3. **Hidden-fault security and grading** ([`155-167`](../../reformation/AUTHORING_GUIDE.md)) — randomise from multiple classes, do not encode class in filenames or ordering, record untouched expected states before delivery, grade localization separately, debrief against the learner's actual path, rotate fixtures. This is an operations manual for not leaking the answer.
4. **The two transfer claims and their non-substitutability** ([`README.md:75-80`](../../reformation/README.md)), enforced in the handoff template with separate checkbox blocks and the line *"An independent person is not interchangeable with a fresh model session"* ([`HANDOFF.md:144`](../../reformation/templates/HANDOFF.md)).
5. **Module 04's grading table** ([`04:175-193`](../../reformation/modules/04-hidden-diagnosis.md)): *"A correct repair earns no localization points. An accidental passing run cannot compensate for a wrong boundary or layer. A correct localization remains creditable when repair is outside learner authority."*
6. **Module 05 in full.** Outcome-blind sample frozen before outcomes are read; free-form notes before any category field is exposed; *"Do not begin with a published taxonomy or adapter-supplied category list"* ([`05:18`](../../reformation/modules/05-error-analysis.md)); a visible rubric revision requirement; frequency and severity explicitly not multiplied together ([`166`](../../reformation/modules/05-error-analysis.md)); and the supplied-corpus claim bounded to `UNPROVED` ([`63`](../../reformation/modules/05-error-analysis.md)).
7. **Module 11's replacement held-back set** ([`11:177`](../../reformation/modules/11-evaluate-change.md)): *"Once a held-back case has influenced repair, it is no longer held-back confirmation."* This closes a contamination path most evaluation curricula leave open.
8. **Module 10's merged-artifact recheck** ([`10:178`](../../reformation/modules/10-multi-agent.md)): *"Passing worker returns do not imply a passing merge."*
9. **Module 08's deterministic supersession policy** ([`08:38-50`](../../reformation/modules/08-durable-state.md)) — exact identity, then declared authority, then applicable time, with unresolved ties held; and the explicit refusal of *"nearest-match, majority vote, model confidence, or whichever candidate arrived last."*
10. **Module 06's approval ordering** ([`06:184-190`](../../reformation/modules/06-tool-boundaries-approval.md)) — make unavailable, then bound structurally, then keep a few raw-action gates — plus *"Fewer prompts are not automatically safer"* ([`200`](../../reformation/modules/06-tool-boundaries-approval.md)).
11. **Module 07's blast-radius standard** ([`07:120`](../../reformation/modules/07-fixed-workflow.md)): *"'Outputs look reasonable' is not acceptance"*, with a zero manual-repair count and a row-edit detector supplied by the adapter.
12. **Advanced 02's relocation ledger** ([`Adv02:92-113`](../../reformation/modules/advanced/02-port-control-second-harness.md)), which names syntax translation as a distinct middle category and refuses to let it count.
13. **The `HOLD` boundary** ([`README.md:111-113`](../../reformation/README.md)) and its per-module restatement: *"A well-supported `HOLD` is a valid operational decision, but it does not demonstrate the held acceptance item."*
14. **Every module's evidence-boundary section.** These are the strongest instance of competency C11 in any curriculum I have examined, and they are the reason the negative-claims research area returned `WELL-SUPPORTED` while every other area returned `PARTIALLY-SUPPORTED`.

---

## 8. Critical findings

### `P0-1` — The calibration instrument, as specified, cannot measure calibration

**Where:** [`README.md:56-65`](../../reformation/README.md); [`00-setup-calibration.md:33-46`](../../reformation/modules/00-setup-calibration.md); [`12-capstone.md:108-122`](../../reformation/modules/12-capstone.md); [`CALIBRATION_RECORD.md:104-119,166-175`](../../reformation/templates/CALIBRATION_RECORD.md).

**Problem.** Four defects compound.

1. **Regression to the mean is indistinguishable from learning.** The headline assessment compares Module 00 absolute gap with capstone absolute gap and asks *"Gap narrowed, widened, or unchanged?"* ([`CALIBRATION_RECORD.md:168-175`](../../reformation/templates/CALIBRATION_RECORD.md)). A difference score computed against a noisy measured value will shrink from a large first draw to a second draw by regression alone. This is the autocorrelation artifact that generated the canonical Dunning-Kruger plot. The specification will produce apparent calibration gains it did not earn.
2. **The measured term is mostly noise.** METR needed 246 tasks across 16 developers for enough power to detect a group-level effect. Generalizability work on rubric-scored performance puts case specificity at ~13% and case-task interaction at ~31% of score variance, against under 5% for rater variance and its interactions. The specification's one methodological safeguard — an externally authored rubric ([`00:22-23`](../../reformation/modules/00-setup-calibration.md)) — controls the smallest variance component and leaves the largest uncontrolled.
3. **Hedging to zero is near score-maximizing.** Scored on absolute gap against a noisy measured effect frequently near zero, "little or no effect" is close to optimal and requires no calibration at all.
4. **The prediction contaminates its own measurement.** The learner performs both arms and is graded on the gap, so managing the outcome toward the prediction is available.

**Consequence.** A program running this design will report calibration improvement in good faith on invalid evidence — the one failure mode the rest of the curriculum is built to prevent.

**Recommended change.** The fix is already half-built in the file. `CALIBRATION_RECORD.md` line 162 defines a **closeout row** carrying a prediction, a confidence value (0–100), and an observed result *for every module*. That is ~13 forecast-outcome pairs with confidence — a series from which a real calibration statistic can be computed. Specifically:

- Make the accumulated closeout series the **primary** calibration instrument, and score it on the relationship between stated confidence and observed hit rate across the series.
- Demote the Module 00 / capstone matched pair to what it is: an **encoding and confrontation exercise**, valuable because a committed prediction improves how the learner registers the outcome, and because it forces one unavoidable confrontation. Report it as a narrative record, not a scored gap.
- Delete or explicitly caveat the "gap narrowed / widened" comparison ([`166-175`](../../reformation/templates/CALIBRATION_RECORD.md)) as unable to distinguish learning from regression.
- Score the **process** (was the prediction sealed, was the confidence stated, was the confrontation recorded, did a named belief change) rather than the magnitude.
- Add anti-hedging: require a prediction with a stated confidence and a directional commitment, and score across the series so a constant "no effect" prediction is visibly uninformative.

**Evidence:** METR within-subject RCT (16 devs, 246 issues: forecast +24%, measured −19%, post-hoc still +20%); the efficiency-gain-illusion preregistered set (N=2,691) which additionally found that *experiencing* AI assistance increased adoption 44.5% vs 27.7% and worsened the speedup illusion; Good Judgment Project (training effect ran through 30+ forecasts per season, not through experience alone); Stone et al. 2023 (the "one round of feedback" that works is an individualised calibration *curve* over many forecasts, undefined at n=1); Fix 2022 on autocorrelation; generalizability-theory variance decomposition.

**Confidence: high.** This finding contradicts the previous review's own recommendation; see §14.

---

### `P1-1` — Four hidden cases cannot support a localization verdict, and layer naming is the weakest dimension in the grade

**Where:** [`04-hidden-diagnosis.md:171-193`](../../reformation/modules/04-hidden-diagnosis.md), especially line 193 (*"at least four independently localized hidden cases"*) and the 10-point rubric at [`175-182`](../../reformation/modules/04-hidden-diagnosis.md).

**Problem.** Three sub-issues.

1. **Item count.** A four-item diagnostic sample sits around 0.2–0.4 reliability in comparable formats. Key-feature write-in testing — the closest validated analogue, and the format this module correctly resembles — reaches 0.32 at one hour of testing time and needs roughly 4 hours for 0.66. An osteopathic clinical-reasoning viva required 18 stations for a generalizability coefficient of 0.80. Four cases is practice; it is not a verdict.
2. **Layer naming is the least reliable dimension.** Two-expert Cohen's κ on bug *type* was 0.31 and on *root cause* 0.46, against 0.68 for observable *effects*. The module awards 2 of 10 points for the least agreeable judgment and 3 for the most agreeable one (earliest divergence), which is the right relative weighting — but publishing a five-layer taxonomy without a grader-calibration and reconciliation step will produce score variance that belongs to the grader.
3. **Hedging to the broadest layer.** The rubric says *"Cheapest supported layer is named"* but does not state whether a superordinate or adjacent layer earns partial credit. If it does, naming the broadest plausible layer every time is a dominant strategy; in the closest published analogue, that strategy cleared the pass mark.

**Consequence.** The course's most distinctive assessment produces a number that reads as a competency judgment and is not one.

**Recommended change.** (a) Report the localization score as **cumulative across the course** — Modules 04, 07, 08, 09, 10, 11, and 12 all seal a localization, which is 10+ instances, enough to carry a judgment — rather than as a Module 04 verdict. (b) State an explicit no-partial-credit rule for adjacent or superordinate layers, mirroring the strict binary rule already published for first-divergence scoring. (c) Add grader calibration and a reconciliation step to the hidden-fault section, since expert agreement on cause categories only exceeds 0.80 after sustained moderated calibration. (d) Require the answer key to include faults of **omission** (a missing permission, an absent instruction, an unset ceiling, a field never written) and to state the expected localization for them — these are the most realistic harness faults and the class where an answer key is hardest to write.

**Evidence:** van der Vleuten & Schuwirth reliability-by-testing-time table; Page & Bordage key-feature design; Zhang, Roy & Arnaoudova strict binary localization scoring; two-expert κ on bug type/cause/effects; osteopathic viva generalizability study.

**Confidence: high** on item count and layer reliability; **medium** on the hedging strategy's magnitude in this specific format.

---

### `P1-2` — The two-proof conditional design has no positive-case counterweight and no ground truth for "correctly declined"

**Where:** [`README.md:42`](../../reformation/README.md); [`COURSE_MAP.md:76`](../../reformation/COURSE_MAP.md); [`AUTHORING_GUIDE.md:111`](../../reformation/AUTHORING_GUIDE.md); [`08:65`](../../reformation/modules/08-durable-state.md); [`09:73`](../../reformation/modules/09-adaptive-flow.md); [`10:82`](../../reformation/modules/10-multi-agent.md).

**Problem.** The structural separation is correct and well grounded — "knows when" and "can do" are empirically distinct constructs, and refusing to award operating mastery for a non-adoption decision is the right direction, since the far commoner curricular error is the reverse. Three defects remain.

1. **No counterweight.** For most real workloads, declining is correct. A learner's record can consist entirely of declines, and the specification cannot distinguish genuine discernment from default avoidance.
2. **No ground truth.** Declining produces no counterfactual, so "correctly declined" has no verifiable referent — the selective-labels problem. The learner both characterises the workload and draws the conclusion, with no independent check on the characterisation. A workload described one way earns a decline; the same workload described another way earns adoption.
3. **One bounded qualifying case is weak operation evidence.** Person × scenario variance in simulation-based assessment runs roughly double person variance, and the qualifying case is supplied by the adapter — structurally the classroom case that entrustment doctrine warns produces false-positive competence judgments.

**Consequence.** The record shows "mechanism: complete" for a learner who declined everything and operated one engineered case once.

**Recommended change.** (a) Grade the **workload characterisation**, not the verdict: require the learner to state the observable properties that drove the decision and have an instructor or peer challenge the characterisation, not the conclusion. (b) Require at least one *adoption* decision across the three conditional modules (08/09/10), so the record contains a positive case; where the learner's own work genuinely warrants none, the qualifying case supplies it and the record says so. (c) Mark the operation proof explicitly as **standardised-conditions evidence** rather than an equal-weight sibling of the selection proof. (d) Add a second, structurally different qualifying case for any conditional mechanism the learner intends to carry into the capstone.

**Evidence:** Miller's pyramid and the OSCE/written-test dissociation (31 of 40 total-score correlations); entrustment-decision literature on workplace vs classroom settings; simulation reliability variance decomposition; selective-labels problem.

**Confidence: high** on the counterweight and single-case issues; **medium** on how much a challenged characterisation would fix.

---

### `P1-3` — The compaction-evidence clause is over-strict in one direction and under-specified in another

**Where:** [`03-context-control-surfaces.md:131`](../../reformation/modules/03-context-control-surfaces.md); [`AUTHORING_GUIDE.md:93`](../../reformation/AUTHORING_GUIDE.md); [`COURSE_MAP.md:21`](../../reformation/COURSE_MAP.md).

**Problem.** Two halves.

1. **The distinction is right.** A reset and a compaction are mechanically different: reset deletes and re-injects durable files verbatim; compaction is partial, lossy, model-authored re-encoding with no re-injection. A reset can only *remove*; compaction can additionally *insert confidently wrong content* — and fabrication is the failure operators most need to catch. Constraint survival across compaction is probabilistic (0–59% by model family), selective by constraint type (soft policies decay ~50 points, hard safety norms ~6), and dose-responsive to summarisation aggressiveness. A reset reproduces none of those three signatures. The curriculum is correct to refuse the substitution and correct to require the label.
2. **The clause "at least one course adapter must expose a real context-pressure boundary" is false as a necessity claim and ambiguous as a completion rule.** Compaction is not exotic: harnesses emit compaction as a first-class observable event, and there are routes to genuine compaction evidence that do not require a bespoke adapter. More importantly, the specification never says what a learner's *completion status* is when their adapter offers only simulation. `COURSE_MAP.md:21` states the material proof without qualification; the module says label it a reset simulation; neither says whether that is a pass with a bounded claim or a `HOLD` on that evidence item.

**Consequence.** Most learners on most adapters will run the simulation, and the specification does not say what they have proved.

**Recommended change.** (a) Replace "only a special adapter can produce this" with an observable requirement: the evidence must show a **summarisation or re-encoding event**, not merely a session boundary, and must record the resolved state before and after. (b) State the completion rule explicitly — recommended: reset-simulation completes Module 03 with the context-degradation evidence item recorded `UNPROVED`, and the capstone's context-survival item ([`12:198-209`](../../reformation/modules/12-capstone.md)) then carries the real requirement. (c) Require **more than one run**, since constraint survival is probabilistic and a single passing run is not evidence. (d) Require the tested constraint to be a *soft* operational rule rather than a hard safety norm, or the exercise will usually pass and teach the wrong lesson. (e) Warn adapter builders against two specific fakes: truncation-instead-of-summarisation (reproduces deletion only) and verbatim re-injection after compaction (the correct production mitigation, which drives the violation rate to zero and destroys the exercise).

**Evidence:** ConstraintRot-style compaction governance measurements; documented compaction-fabrication cases; vendor documentation of compaction mechanics; Norman on functional vs physical fidelity.

**Confidence: high** on the reset/compaction asymmetry; **medium** on how easily adapter-free compaction evidence can be obtained in an arbitrary stack.

---

### `P1-4` — The person-transfer gate rests on one recipient, with no required answer key and no enforced non-interaction protocol

**Where:** [`11-evaluate-change.md:220-228`](../../reformation/modules/11-evaluate-change.md); [`12-capstone.md:355-371`](../../reformation/modules/12-capstone.md); [`HANDOFF.md:128-144`](../../reformation/templates/HANDOFF.md).

**Problem.** The distinction between restartability and person transfer is correct and well founded — independent reproduction fails at rates self-rerun never reveals, and a fresh model session additionally shares the producing model's priors and over-rates artifacts it recognises. The gate itself is under-specified in four ways.

1. **N=1.** Single-recipient pass/fail is a high-variance draw; in comparable usability work, individual evaluators ranged 55–100% problem coverage. A team that fails, changes nothing material, and retries with a different recipient will eventually pass.
2. **Scoring.** Module 12 requires a *"protected recipient rubric"* ([`12:369`](../../reformation/modules/12-capstone.md)) — good. Module 11 does not: it asks for a verbatim restatement ([`11:228`](../../reformation/modules/11-evaluate-change.md)) but names no key and no non-author scorer. A fluent-but-wrong restatement passes. Aviation hearback data show 37–40% of erroneous readbacks go uncorrected by the very people whose job is to catch them.
3. **Non-interaction.** *"Without leading questions, verdict choices, or sentence completion"* ([`11:220`](../../reformation/modules/11-evaluate-change.md)) is an instruction, not a protocol. Facilitator presence measurably changes recipient performance.
4. **Task selection.** The author chooses the named task, so it is necessarily the task the package covers. Independent-reproduction failures concentrate in what the author did not think to document.

**Consequence.** The course's strongest claim — that an independent person can operate the package — is carried by its least controlled measurement.

**Recommended change.** (a) Require Module 11 to use the same protected-rubric-plus-independent-evaluator structure Module 12 already specifies. (b) Require a **non-author scorer**. (c) Specify the non-interaction protocol mechanically (author absent or non-responding; questions logged, not answered; a recorded session). (d) Have the **evaluator, not the author, select the named task** from a small set the adapter supplies. (e) State plainly that a single recipient supports a bounded claim about that recipient, and require a second recipient for any package the learner intends to put into real use.

**Evidence:** I-PASS (23% error reduction for the full bundle including receiver synthesis and direct observation, not for restatement alone; adherence to receiver synthesis fell to 8–12% once unobserved); teach-back systematic review (consistently positive, low quality, and no study linking restatement accuracy to later performance); AHRQ handoff review (process measures improved far more than outcomes); Faulkner evaluator-variance data; aviation hearback error rates.

**Confidence: high.**

---

### `P1-5` — Transfer-seed schema compliance is broken in 11 of 16 modules, which breaks the capstone artifact that consumes them

**Where:** every module's identity block declares the canonical schema and states that module-specific fields are *"appendices, not replacements"* (e.g. [`06:13`](../../reformation/modules/06-tool-boundaries-approval.md)). But the actual transfer-seed **sections** in 11 modules supply bespoke bold fields instead of the canonical line — for example [`06:279-285`](../../reformation/modules/06-tool-boundaries-approval.md) (Workload and trigger / Primitive to try / First safe boundary / Re-inventory trigger / Owner and first safe trial), and identically in [`Adv01:278-284`](../../reformation/modules/advanced/01-build-callable-capability.md) and [`Adv02:245-251`](../../reformation/modules/advanced/02-port-control-second-harness.md). Only Modules 04, 05, 10, 11 and Advanced 03 give the canonical `YYYY-MM-DD | …` line as a usable body template.

**Problem.** Module 06's seed as written has **no date field** and no *"evidence to collect"* field. Module 12 Stage 9 requires *"Collect every transfer seed from Modules 00–11. Preserve each original date and wording"* and builds a table keyed on Seed date, Named workload, Real trigger, Smallest next use, and Evidence to collect ([`12:317-333`](../../reformation/modules/12-capstone.md)).

**Consequence.** A team implementing each module exactly as written produces a seed corpus the capstone cannot assemble. This is precisely the "satisfy the prose, lose the mechanism" class the brief asks me to hunt.

**Recommended change.** Give every module the canonical line as the seed template and append module-specific fields beneath it, as the identity block already instructs. This is a mechanical edit to 11 files.

**Confidence: high.** Verified mechanically; see §13.

---

### `P2-1` — Canary evidence: right scope language, three unaddressed validity threats

**Where:** [`00:111-121`](../../reformation/modules/00-setup-calibration.md); [`06:223-231`](../../reformation/modules/06-tool-boundaries-approval.md); [`SETUP_RECORD.md:84-103`](../../reformation/templates/SETUP_RECORD.md).

**Problem.** The scoping language is the best-supported design choice in the course — channel enumeration has been known to be inherently incomplete for four decades, and *"A passing canary supports only the tested fixture, configuration, paths, and observed channels"* ([`00:121`](../../reformation/modules/00-setup-calibration.md)) is exactly the defensible form. Three threats sit inside the scope, not outside it.

1. **Right channel, wrong observable.** If the monitor records the policy verdict ("no requests to non-allowlisted domains") rather than the traffic, every documented allowlist bypass passes. The specification requires inspecting channels; it does not require inspecting *bytes* rather than *decisions*.
2. **Zero-power canary.** If the planted marker never enters the model's context at the decision point, the test cannot fail regardless of harness behavior. The specification says place it in "the adapter-designated reachable file" but never requires evidence that the agent actually read it.
3. **Non-adaptive probe.** One hand-written attempt with no evasion. Published defenses reporting near-zero attack success have been broken above 90% by attackers allowed to move second.

**Recommended change.** Require (a) the canary check to inspect transmitted content, with the policy verdict recorded separately; (b) positive-control evidence that the marker was reachable and read in the run — a canary that could not have fired proves nothing; (c) one deliberately evasive second attempt, or an explicit statement that only the non-adaptive case was tested.

**Confidence: high.**

---

### `P2-2` — Module 05 sets no minimum failure count, so the ranked top three can be vacuous

**Where:** [`05-error-analysis.md:143-168`](../../reformation/modules/05-error-analysis.md).

**Problem.** The sample is 20–40 *runs*, but the analysis unit that matters is *failed* runs. A well-run workload sampled outcome-blind may yield 3 failures in 3 different categories. The "frequency-ranked top three" is then a 1-1-1 tie, saturation is trivially satisfied (five consecutive runs with no new category is guaranteed when most runs pass), and the "top-ranked failure" that drives Stage 7's check is arbitrary.

**Consequence.** The module's central deliverable can be produced with no information in it, while every stated rule is followed.

**Recommended change.** Add a minimum observed-failure count (a defensible floor is 8–10 `FAIL` runs) as a condition for claiming a ranking; below it, the learner still builds a check for the most consequential observed failure but records the ranking as `INSUFFICIENT FAILURES TO RANK`. Also require the saturation criterion to be evaluated over failed runs, not over all runs.

**Confidence: high** on the defect; **medium** on the specific floor.

---

### `P2-3` — Two of the five safeguards for non-developer independence are weak signals

**Where:** [`README.md:100-107`](../../reformation/README.md); [`AUTHORING_GUIDE.md:134`](../../reformation/AUTHORING_GUIDE.md).

**Problem.** The negative half of the standard — *"A path that preselects the answer and asks the learner only to click Run, Approve, or Continue is a demonstration, not course completion"* ([`README.md:109`](../../reformation/README.md)) — is the best-supported part. Two of the five positive safeguards are weaker than the specification assumes.

- *"own the … verdict"* — self-assessed correctness is near-uninformative as a competence signal and degrades further with a model in the loop.
- *"change a readable policy … and predict its effect"* — outcome-prediction accuracy on declarative rulesets runs 47.6–86.2% even on *correct* rulesets, and non-programmers are measurably more confident and less correct than programmers on exactly this task. Rule interaction, precedence, timing, and omission are where the collapse occurs — not single isolated knobs.

**Recommended change.** (a) Require the causal control to involve **interaction or precedence** at least once per learner, not only an isolated knob — Module 02's precedence work and Module 03's precedence declaration already create the opening. (b) Score predictions against ground truth rather than accepting them as participation. (c) Add an omission-class defect to the seeded faults, since every measured collapse in end-user rule authoring concentrates there. (d) Do not count "owns the verdict" as evidence of correctness; count it as evidence of accountability, which is what it actually establishes.

**Evidence:** Panko spreadsheet-error corpus (51% of 1,170 real spreadsheets contained errors); Brackenbury et al. trigger-action rule interpretation; end-user policy-authoring defect studies.

**Confidence: high.**

---

### `P2-4` — Module 09's prerequisite differs between the course map and the module

**Where:** [`COURSE_MAP.md:27`](../../reformation/COURSE_MAP.md) requires *"recorded failure of the simpler fixed rung for the chosen case"*. [`09-adaptive-flow.md:7`](../../reformation/modules/09-adaptive-flow.md) allows *"a preserved fixed-rung failure **or** an adapter-supplied qualifying case whose next branch cannot be usefully named in advance"*.

**Problem.** The module is the more coherent of the two — it correctly implements the two-proof rule — but the course map is declared authoritative for prerequisites and a team building from it will impose a condition the module does not require.

**Recommended change.** Update the course map row to match the module.

**Confidence: high.**

---

### `P2-5` — `cold` is used 19 times against the guide's own ban, twice ambiguously

**Where:** [`AUTHORING_GUIDE.md:224`](../../reformation/AUTHORING_GUIDE.md) states the rule: *"Say `clean session` for restartability and `independent person` for person transfer; do not use `cold` ambiguously."*

Violations: `cold-reader handoff` ([`02:221`](../../reformation/modules/02-direct-work.md)) and `cold handoff` ([`COURSE_MAP.md:30`](../../reformation/COURSE_MAP.md)) are genuinely ambiguous between the two transfer claims — the exact confusion the rule exists to prevent, in a course whose central distinction is that these are different. `cold start` ([`00:162`](../../reformation/modules/00-setup-calibration.md), [`00:199`](../../reformation/modules/00-setup-calibration.md)) means clean session. Module 08 uses `cold retrieval` / `cold session` / `cold answer` 9 times as a defined term ([`08:27`](../../reformation/modules/08-durable-state.md)) while its own Stage 3 opens *"Start a fresh session"* — two names for one thing in one module.

**Recommended change.** Replace `cold-reader handoff` and `cold handoff` with the specific claim (`clean-session` or `independent-person`). Either retire `cold retrieval` in favour of `clean-session retrieval`, or keep it as a defined term and add it to the language rule as an explicit exception.

**Confidence: high.**

---

### `P2-6` — The canonical supersession key has two names

**Where:** `(thing, property)` in [`COURSE_MAP.md:26`](../../reformation/COURSE_MAP.md) and [`AUTHORING_GUIDE.md:98`](../../reformation/AUTHORING_GUIDE.md); `(entity, property)` and `(entity_id, property_key)` in [`08:17,32,160`](../../reformation/modules/08-durable-state.md).

**Problem.** This is the one invariant a durable-state adapter must implement mechanically. Two names for it in the three documents an implementer reads is exactly where a mechanism gets built twice or built differently.

**Recommended change.** Adopt `(entity, property)` — the module's term, and the more precise one — everywhere, with `(entity_id, property_key)` as the schema-level spelling.

**Confidence: high.**

---

### `P2-7` — Module 12 restates the evidence ladder the course map reserves

**Where:** [`COURSE_MAP.md:90`](../../reformation/COURSE_MAP.md): *"Module authors reference these names; they do not restate or rename the ladder."* [`12-capstone.md:420-426`](../../reformation/modules/12-capstone.md) restates all seven levels with capstone-specific definitions.

**Problem.** Module 12's version is *specialisation*, not duplication, and it is useful. But as written it violates a rule stated one document away, and a reviewer applying the publication checklist ([`AUTHORING_GUIDE.md:230-247`](../../reformation/AUTHORING_GUIDE.md)) has to make a judgment call the specification should have made.

**Recommended change.** Amend the course-map rule to permit per-module specialisation that preserves the seven names and their order, and prohibit renaming, reordering, adding, or dropping levels.

**Confidence: high.**

---

### `P3-1` — The `Required closeout` identity line lacks a trailing `<br>` in all 16 modules

Every other field in the identity manifest ends `<br>`; the `Required closeout` line does not, so it renders joined to the `Transfer-seed schema` line that follows. Contract item 1 requires the identity fields to appear together and be easy to locate. Mechanical, 16 files.

**Confidence: high.**

---

### `P3-2` — `**Path:**` is an undeclared identity field present only in Modules 07, 08, 09

Contract item 1 ([`AUTHORING_GUIDE.md:27`](../../reformation/AUTHORING_GUIDE.md)) enumerates the identity fields; `Path` is not among them (`Target path` is a different field, and these three modules carry that separately). The content is useful — it states core/conditional placement. Either add `Path` to the contract and apply it to all 16 modules, or fold the sentence into the module's opening paragraph.

**Confidence: high.**

---

## 9. Module-by-module dispositions

| Module | Disposition | Keep | Change | Add | Remove or move | Rationale |
|---|---|---|---|---|---|---|
| **00** Setup & calibration | `KEEP, REVISE` | Reach inventory with four enumerated surfaces; canary with scope statement; restore-after-bad-run; hidden setup fault; watched check failure | Recast Stage 0 as a sealed prediction + confrontation exercise; stop scoring gap magnitude as the calibration claim (`P0-1`) | Canary positive control and content-level observable (`P2-1`) | — | Everything except the calibration scoring is strong; the scoring is the course's one invalid measurement |
| **01** Guided first result | `KEEP` | Predict-before-run; real delivery surface ([`71`](../../reformation/modules/01-guided-first-result.md)); four checks; **Stage 8 unguided analogous case** | — | — | — | Correct implementation of guided→faded→independent, with an explicit refusal to claim design mastery ([`18`](../../reformation/modules/01-guided-first-result.md)) |
| **02** Direct work | `KEEP` | Numbered constraints + precedence; falsifier; `BOUNDARY CALL`; builder-cannot-alter-checks with planted tamper; failure-design card; fresh-fixture recurrence | Replace `cold-reader handoff` (`P2-5`) | Canonical transfer-seed line (`P1-5`) | — | The strongest core module; the self-planted fault is correctly scoped to failure *design* ([`167`](../../reformation/modules/02-direct-work.md)) |
| **03** Context & control | `KEEP, CLARIFY` | Context-as-budget; precedence ladder; compaction symptom cluster; matched A/B; `NOT SUPPORTED` for second harness | State the simulation-only completion rule; require >1 run; require a soft constraint (`P1-3`) | Adapter warnings against truncation-fakes and post-compaction re-injection | Replace "only a special adapter" necessity claim | The reset/compaction distinction is right and the exercise is well built; the completion rule is missing |
| **04** Hidden diagnosis | `KEEP, REVISE` | Ownership contract; boundary path; interval halving; sealed localization; repair-status enum; responsive debrief; fading support | Report localization cumulatively across the course, not as a Module 04 verdict; state no-partial-credit for adjacent/superordinate layers (`P1-1`) | Grader calibration + reconciliation; omission-class faults in the key | — | Best-designed diagnosis lab I have reviewed; the only defect is the strength of the claim it makes from four items |
| **05** Error analysis | `KEEP, CLARIFY` | Everything | — | Minimum failure count for a ranking claim; saturation evaluated over failed runs (`P2-2`) | — | Fully resolves the previous review's largest gap and adds protections it did not ask for |
| **06** Tool boundaries & approval | `KEEP, REVISE` | Raw-manifest review; primitive table; prospective approval ceiling + exhaustion case; canary; disconnect/revocation | Canonical transfer-seed line (`P1-5`) | Canary positive control (`P2-1`) | — | The approval-budget design directly answers the "count without a ceiling" trap |
| **07** Fixed workflow | `KEEP, CLARIFY` | Seven invariants; one owning rule location; exact record-and-field diff; zero manual repair; second wave; hidden case | Flag the schema/policy authorship load and name the accessible route (§3) | Canonical transfer-seed line | Fold `**Path:**` into prose (`P3-2`) | The most operationally demanding core module and the most likely place a non-developer stalls |
| **08** Durable state | `KEEP, REVISE` | Six invariants; deterministic supersession order; five cold-retrieval cases; externally held integrity root; propagation checks | Unify `(entity, property)` naming (`P2-6`); resolve `cold` (`P2-5`) | Canonical transfer-seed line | Fold `**Path:**` into prose | Content is excellent; the defects are naming, and naming is what an implementer builds from |
| **09** Adaptive flow | `KEEP, CLARIFY` | Seven control invariants; control state separate from living artifact; six unattended cases; budget ceilings producing terminal states | Align the course-map prerequisite (`P2-4`) | Positive-case requirement across 08/09/10 (`P1-2`) | Fold `**Path:**` into prose | Unattended drill is the strongest part; prerequisite text is the only real inconsistency |
| **10** Multi-agent | `KEEP` | Complexity claim; budget-matched baseline; independence matrix; read/write asymmetry; refute-don't-vote; merged-artifact recheck against the pinned gate | — | Positive-case requirement (`P1-2`) | — | Correctly conditional and correctly deflationary; the merged-artifact recheck is a genuine contribution |
| **11** Evaluate change | `KEEP, REVISE` | Post-training decline/escalate gate; hard gates vs aggregates; repeated trials and blinding; replacement held-back set; rollback demonstrated even on rejection | Add protected rubric, non-author scorer, non-interaction protocol, evaluator-selected task to the listener gate (`P1-4`) | — | — | Substantively excellent; the person gate is under-specified relative to Module 12's own treatment |
| **12** Capstone | `KEEP, REVISE` | Ten-row independent evidence plan; instructor-injected fault; recalibration; accumulated-run analysis with honest `HOLD`; both transfer gates; package structure | Recast recalibration per `P0-1`; permit ladder specialisation explicitly (`P2-7`) | Second recipient for packages intended for real use (`P1-4`) | — | Genuinely integrative rather than a replay; the `HOLD`-does-not-pass-an-unproved-gate rule ([`418`](../../reformation/modules/12-capstone.md)) is exactly right |
| **Adv 01** Callable capability | `KEEP` | Primitive comparison table; contract frozen before implementation; ten direct cases before host registration; idempotency and cancellation semantics; version identities separated | Canonical transfer-seed line | — | — | Correctly advanced; correctly gated on maintainability |
| **Adv 02** Port control | `KEEP` | Relocation / syntax-translation / mechanism-transfer trichotomy; invariant fixtures; sink-record evidence; `HOLD` when both planes are the same | Canonical transfer-seed line | — | — | The trichotomy is the contribution; do not simplify it |
| **Adv 03** Post-training | `KEEP` | Decision gate with written decline; rights ledger; dependency-group splitting; leakage audit including transformed descendants; development-only checkpoint selection; serving parity; removal proof | — | — | — | The most rigorous treatment of post-training governance in the corpus; correctly outside the core |

---

## 10. Adapter and implementation audit

Per module: does the specification tell a new team what to build without leaving a mechanism to chance? `✓` specified · `~` partially · `✗` missing.

| Module | Scenario/source | Starter | Editable vs protected surfaces | Executable vs simulation | Protected checks | Hidden cases | Answer key + debrief | Resolved-state visibility | Evidence export | Restore/cleanup/revoke | Accessibility | Non-developer route | Instructor isolation | Authors | Configures | Decides | Proves completion | Must remain unproved |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 00 | ✓ | ✓ | ✓ | ~ | ✓ | ✓ | ~ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 01 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 02 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 03 | ✓ | ✓ | ✓ | **~** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **~** | ✓ |
| 04 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **~** | ✓ |
| 05 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **~** | ✓ |
| 06 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 07 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | ✓ | ✓ | ✓ | ✓ | **~** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 08 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 09 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 10 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 11 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | ✓ | ✓ | ✓ | ✓ | ✓ | **~** | ✓ | ✓ | ✓ | **~** | ✓ |
| 12 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **~** | ✓ |
| Adv 01 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | ✓ | ✓ | ✓ | ~ | n/a | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Adv 02 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | ✓ | ✓ | ✓ | ~ | n/a | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Adv 03 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ~ | ✓ | ✓ | ✓ | ~ | n/a | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

### Mechanisms a competent team could omit while claiming compliance

1. **Compaction theatre** (03). Implement "context-pressure control" as truncation of the oldest turns, or re-inject the constraint verbatim after compaction. Both satisfy the prose; the first reproduces only deletion, the second drives the violation rate to zero. **Neither is named as prohibited.**
2. **Zero-power canary** (00, 06, 12). Place the marker where the agent had no reason to read it. Every stated requirement is met and the test cannot fail. **No positive control is required.**
3. **Policy-verdict monitoring** (00, 06). Record "no requests to non-allowlisted destinations" rather than transmitted bytes. Passes through every documented allowlist bypass.
4. **Single-instance verdicts** (00 calibration, 04 localization, 11 listener). Each is specified as a gate; none carries an instance-count or reliability qualification except Module 04's floor of four, which is itself too low.
5. **Trivially qualifying case** (08, 09, 10). Build the bounded qualifying case so the mechanism is obviously warranted, obviously configured, and obviously successful. Rule 5 forbids pre-authoring the *judgment* but nothing forbids engineering the case to make the judgment trivial.
6. **Vacuous ranking** (05). Sample 20 runs of a healthy workload, observe 3 failures in 3 categories, report a ranked top three.
7. **Commission-only seeded faults** (04, 12). Seed only faults where something wrong is present, never faults of omission — a missing permission, an absent instruction, an unset ceiling. The specification requires four *classes* but does not require omission to be among them, and omission is both the most realistic harness fault and the class an answer key is hardest to write for.
8. **Answer-key variance** (04, 07, 08, 09, 11, 12). Every module requires a sealed key; none requires the key to be validated, calibrated across graders, or pre-published as an acceptance set. The key becomes a larger source of score variance than the learner.
9. **Broken seed schema** (`P1-5`). Already present in the specification as written.

Items 1–3, 6, and 7 are cheap to close with one sentence each in the relevant obligation-matrix row. Items 4 and 8 are the substantive `P0`/`P1` work.

---

## 11. Progression and assessment audit

**Prerequisites available before required — yes, with one exception.** The chain 00→01→02→03→04→05→06→07→08→{09→10} is sound and each module's opening paragraph names the specific artifacts it inherits. The exception is Module 05, which requires *"an eligible learner-owned or authentic supplied operational run corpus"* ([`05:6`](../../reformation/modules/05-error-analysis.md)). By Module 05 the learner has completed roughly four modules of exercises, which is unlikely to yield 20 eligible runs of *their own recurring work* — the runs from Modules 01–04 are course fixtures, not attempts at the workload for its actual intended use ([`05:54-58`](../../reformation/modules/05-error-analysis.md)). The specification anticipates this and supplies the authentic-corpus fallback with an `UNPROVED` claim, and the capstone re-runs the analysis on accumulated real runs ([`12:124-140`](../../reformation/modules/12-capstone.md)). That is honest. It does mean **most learners will meet error analysis first on someone else's corpus**, and the specification should say so plainly rather than presenting learner-owned as the default.

**Guided before independent — yes.** Module 01 is explicitly guided ([`01:18`](../../reformation/modules/01-guided-first-result.md)) and its Stage 8 supplies the unguided repetition on a different case within the same module — the strongest single implementation of the guided-experience rule in the corpus.

**Fixed before adaptive — yes.** 07 precedes 09; 09's prerequisite names the fixed rung; the capstone's Stage 3 orders it again ([`12:155-171`](../../reformation/modules/12-capstone.md)).

**Single-worker evidence before divided work — yes**, and budget-matched ([`10:102-114`](../../reformation/modules/10-multi-agent.md)).

**Localization before error analysis — yes**, and the ordering rationale is stated: *"Error notes are useful only when the learner can identify the first failure rather than its downstream symptoms"* ([`COURSE_MAP.md:39`](../../reformation/COURSE_MAP.md)).

**Selection proof separate from operating proof — structurally yes**, defectively in practice (`P1-2`).

**Competencies repeated at increasing difficulty — yes.** The strand escalation table ([`COURSE_MAP.md:50-56`](../../reformation/COURSE_MAP.md)) is the mechanism, and it is real: each strand's cell content genuinely escalates rather than restating.

**Capstone integrates rather than repeats — yes.** Stage 2 re-runs error analysis on *accumulated* runs and compares codebooks; Stage 3 forces an architecture decision from that analysis; Stage 6 injects a fault the learner has not seen; Stage 9 assembles seeds collected across the course. None of these is available before Module 12.

**Getting unstuck on unknown failures — yes**, in Modules 04, 07, 08, 09, 10, 11, 12.

**Core completable without unmaintainable code — mostly.** Module 07 is the pressure point (§3). Everywhere else the adapter supplies the executable component and the learner configures it.

**Assessment integrity.** The specification independently closes eight of the fourteen traps the brief enumerates: fresh-session ≠ person transfer; opened held-back set ≠ post-repair confirmation ([`11:177`](../../reformation/modules/11-evaluate-change.md)); canary bounded to observed channels; learner-planted faults do not prove hidden-fault diagnosis ([`AUTHORING_GUIDE.md:36`](../../reformation/AUTHORING_GUIDE.md)); supplied corpus ≠ own failure distribution ([`05:63`](../../reformation/modules/05-error-analysis.md)); non-adoption ≠ operating mastery ([`10:16`](../../reformation/modules/10-multi-agent.md)); simulation ≠ executed ([`README.md:94`](../../reformation/README.md)); repair success ≠ localization ([`04:183`](../../reformation/modules/04-hidden-diagnosis.md)). Two are closed but weakly (approval count without a prospective ceiling — closed at [`06:174`](../../reformation/modules/06-tool-boundaries-approval.md); reset simulation reported as compaction resilience — closed at [`03:131`](../../reformation/modules/03-context-control-surfaces.md) but with the completion status undefined). One is closed for supersession specifically ([`08:50`](../../reformation/modules/08-durable-state.md)) and one for divided-worker opportunity ([`10:104`](../../reformation/modules/10-multi-agent.md)). Two remain substantially open: single-instance verdicts, and the selection-proof gameability.

---

## 12. Recovery, calibration, and transfer audit

**Recovery — strong.** A single canonical sequence in [`GETTING_UNSTUCK.md:9-158`](../../reformation/GETTING_UNSTUCK.md), a single cheapest-first five-layer taxonomy repeated identically in the guide, Module 04, `DIAGNOSIS_RECORD.md`, and `RECOVERY_NOTE.md`, with a clear separation between *stuck-state observation* and *causal layer* ([`04:67`](../../reformation/modules/04-hidden-diagnosis.md)). A material failure is defined ([`GETTING_UNSTUCK.md:7`](../../reformation/GETTING_UNSTUCK.md)) so the recovery-note requirement is decidable rather than a matter of taste. Every module requires clean-session recurrence rather than a warm pass. The one gap: `GETTING_UNSTUCK.md` never states an attempt ceiling or a fatigue stop rule, though it does list `HOLD` conditions ([`242-255`](../../reformation/GETTING_UNSTUCK.md)) — worth adding, since prolonged troubleshooting measurably degrades judgment and a bounded attempt count is what makes stopping acceptable to capable, stubborn learners.

**Calibration — the weakest instrument in the course.** See `P0-1`. The design's instincts are right: seal before running, use an external rubric and scorer, score the gap rather than the direction, record carryover and order limits ([`CALIBRATION_RECORD.md:46`](../../reformation/templates/CALIBRATION_RECORD.md)), and refuse to infer improved calibration from an improved result ([`HANDOFF.md:72`](../../reformation/templates/HANDOFF.md)). What is wrong is the statistical form of the headline claim, and the fix is to promote the instrument the template already contains.

**Transfer — strong in design, thin in measurement.** The two-claim distinction is correct and consistently enforced across 16 files. Dated seeds are required at every closeout and assembled into a trigger-based plan with five dispositions ([`12:317-335`](../../reformation/modules/12-capstone.md)) — a genuinely good artifact that answers "delay predicts abandonment" directly. Two defects: the schema-compliance break (`P1-5`) that prevents the plan being assembled, and the single-recipient gate (`P1-4`). Note also that the transfer plan requires *"one near trigger that can occur without expanding authority"* ([`12:335`](../../reformation/modules/12-capstone.md)) — which is exactly the "engineer the first attempt to be small and winnable" principle, arrived at independently.

---

## 13. Internal consistency and mechanical checks

| Check | Command | Result |
|---|---|---|
| Relative links resolve | Python walk over all `[text](target)` in `**/*.md`, normalising against each file's directory | **PASS** — 0 broken of all links checked |
| Anchor targets exist | Extract `#anchor` fragments; slugify all `^#{1,6}` headings; `comm -23` | **PASS** — 6 anchors used, all resolve (`per-module-adapter-obligation-matrix`, `advanced-extension-adapter-obligation-matrix`, `evidence-ladder`, `decision-policy-and-the-hold-boundary`, `two-different-transfer-claims`, `calibration-and-transfer-seed`) |
| H1 titles vs course-map labels | `head -1` on all 16 module files | **PASS** — course map declares short names as navigation labels and the H1 as canonical ([`COURSE_MAP.md:9`](../../reformation/COURSE_MAP.md)); consistent |
| Module numbering vs filenames | Filename prefix vs H1 module number | **PASS** — 00–12 and Advanced 01–03 all match |
| Infrastructure profiles | Header field extraction across 16 files | **PASS** — 00–05 P0, 06 P1, 07–08 P2, 09–10 P3, 11–12 P4; Adv 01/02 P1, Adv 03 P4. Matches `README.md:86-92` cumulative logic |
| Transfer gates | Header field extraction | **PASS** — Fresh everywhere except 11 (Person), 12 (Fresh + Person), Adv 03 (Person). Matches course map |
| Adapter flags | Header field extraction | **PASS** — all 16 `REQUIRED`, matching [`COURSE_MAP.md:10`](../../reformation/COURSE_MAP.md) |
| Prerequisites vs course map | Field extraction + diff | **1 MISMATCH** — Module 09 (`P2-4`) |
| Build-status language | `grep` + `uniq -c` | **PASS** — 13 distinct strings, all following `<scope> curriculum complete; <specific> adapter pending` |
| Evidence-ladder single source | `grep` for the seven level names | **1 RESTATEMENT** — Module 12 lines 420–426 (`P2-7`) |
| Transfer-seed schema declared | `grep -l` for the canonical line | **PASS** — declared in all 16 modules + 5 architecture/template files |
| Transfer-seed schema **usable in body** | Count `YYYY-MM-DD` per file | **11 OF 16 FAIL** — only 04, 05, 10, 11, Adv 03 provide it as a body template (`P1-5`) |
| `cold` terminology rule | `grep -rn 'cold'` vs [`AUTHORING_GUIDE.md:224`](../../reformation/AUTHORING_GUIDE.md) | **19 OCCURRENCES, 2 AMBIGUOUS** (`P2-5`) |
| Supersession key naming | `grep` for `thing, property` / `entity, property` | **2 NAMES** (`P2-6`) |
| Identity-manifest line breaks | Locate `Required closeout` line, test trailing `<br>` | **16 OF 16 FAIL** (`P3-1`) |
| Undeclared identity field | `grep -l '^\*\*Path:\*\*'` | **3 FILES** — 07, 08, 09 (`P3-2`) |
| Duplicate competing frameworks | Read all architecture docs | **PASS** — the previous six overlapping frameworks are gone; `AUTHORING_GUIDE.md:23` states the single contract explicitly replaces them |
| Obsolete migration wording | Read for stale module numbers / "former course" references | **PASS** — no stale numbering; build-status language is forward-looking and dated |

---

## 14. Reconciliation with the prior review

Read after completing the independent findings above. Authorship caveat in §2.

| Prior finding | Current status | Independent agreement? | Evidence |
|---|---|---|---|
| `P0-1` No error analysis anywhere | `RESOLVED` | **Yes** — and exceeded | Module 05 exists in full with outcome-blind sampling, first-failure-only annotation, emergent codebook, visible revision log, saturation criterion, three-way check validation, and a bounded supplied-corpus claim. It adds protections the prior review did not request ([`05:63,139,166`](../../reformation/modules/05-error-analysis.md)) |
| `P0-2` No calibration instrument | `PARTIALLY RESOLVED` | **Partly — and I now disagree with the prior recommendation's specific form** | The instrument was implemented faithfully, including the prior review's exact instruction to score "the size of the prediction gap, not the direction." New research shows that scoring form is a difference-score comparison against a noisy measured value and will show improvement by regression alone. The correction is `P0-1`. The prior review's *diagnosis* (no calibration instrument, and the perception gap is real and large) stands; its *prescription* was statistically wrong and I am withdrawing it |
| `P0-3` Adapter obligations not stated per module | `RESOLVED` | **Yes** | [`AUTHORING_GUIDE.md:88-102`](../../reformation/AUTHORING_GUIDE.md) — 13 core rows with five columns each, plus 3 advanced rows, plus five interpretation rules. Modules 06 and 08, previously unflagged, are now flagged and specified |
| `P1-1` Self-planted faults; diagnosis never tested | `RESOLVED` | **Yes** | Module 04 is a graded localization lab with instructor-planted, interleaved faults in a harness the learner did not build; localization is graded before and separately from repair. Module 02 retains exactly one self-planted fault, correctly scoped to failure *design* ([`02:167`](../../reformation/modules/02-direct-work.md)). My residual concern is the item count (`P1-1` in §8), which is a different objection than the prior review's |
| `P1-2` Context named but its defining property untaught | `RESOLVED` | **Yes** | [`03:49-63`](../../reformation/modules/03-context-control-surfaces.md) teaches degradation, precedence, and symptom clusters; Stage 3 runs the matched survival test. The reset-simulation labelling ([`131`](../../reformation/modules/03-context-control-surfaces.md)) is a protection the prior review did not think to ask for. Residual: completion rule undefined (`P1-3`) |
| `P1-3` Approval recorded, never budgeted | `RESOLVED` | **Yes** | [`06:174`](../../reformation/modules/06-tool-boundaries-approval.md) requires a **prospective** ceiling and exhaustion behavior before the run, plus an adapter-supplied case that would exceed it. This closes the trap more thoroughly than the prior review specified |
| `P1-4` No reach inventory; egress and config-as-code absent | `RESOLVED` | **Yes** | [`00:96-121`](../../reformation/modules/00-setup-calibration.md) four-surface inventory with an explicit instruction not to substitute a label for a channel; [`06:93`](../../reformation/modules/06-tool-boundaries-approval.md) config-as-executable with a sealed challenge. Residual: canary validity threats (`P2-1`), which the prior review did not raise |
| `P1-5` Fixed case sketched, adaptive built | `RESOLVED` | **Yes** | Module 07 is a full core module with seven invariants, exact record-and-field blast radius, zero manual repair, and a second wave |
| `P1-6` Module 05 over-scoped; baseline not budget-matched | `RESOLVED` | **Yes** | Multi-agent moved to Module 10, explicitly conditional; [`10:102-114`](../../reformation/modules/10-multi-agent.md) matches aggregate opportunity across five named dimensions and preserves the baseline-before-measures ordering. The read/write asymmetry is now stated as a hard rule ([`120`](../../reformation/modules/10-multi-agent.md)) |
| `P1-7` No competency practised twice | `RESOLVED` | **Yes** | Five strands mandatory in every module ([`README.md:46-54`](../../reformation/README.md)) with a genuine escalation table ([`COURSE_MAP.md:50-56`](../../reformation/COURSE_MAP.md)) |
| `P1-8` Transfer confined to the capstone | `PARTIALLY RESOLVED` | **Yes on design, no on execution** | Dated seeds are required at every closeout and assembled into a trigger-based plan with five dispositions. But 11 of 16 modules do not supply the canonical schema in their seed section, so the capstone cannot assemble what it specifies (`P1-5`) |
| `P1-9` Module sizing not achievable | `NO LONGER APPLICABLE` | **Agree it should have been dropped** | [`COURSE_MAP.md:5`](../../reformation/COURSE_MAP.md) removes duration estimates by design and forbids reducing proof to fit a calendar. The current brief also excludes duration as a reason to prune. The prior finding's substance — too many objectives per unit — is now handled by variable practice against fixed standards |
| `P2-1` Recovery notes collected once | `RESOLVED` | **Yes** | Required for every material failure, with "material" defined ([`GETTING_UNSTUCK.md:7`](../../reformation/GETTING_UNSTUCK.md)) |
| `P2-2` No fresh-session recurrence proof | `RESOLVED` | **Yes** | Universal, with the warm-pass exclusion stated in the guide, both diagnosis templates, and every module |
| `P2-3` Module 08 accepted a fresh session as person transfer | `RESOLVED` | **Yes** | Module 11's gate is `Person`, with a verbatim unprompted restatement and an explicit refusal of the model-session substitute ([`11:228`](../../reformation/modules/11-evaluate-change.md)). Residual: gate under-specified (`P1-4`) |
| `P2-4` Fine-tuning residue | `RESOLVED` | **Yes** | Moved to Advanced 03; Module 11 Stage 1 now requires a written decline or escalation ([`11:72-77`](../../reformation/modules/11-evaluate-change.md)) |
| `P2-5` Model-and-cost choice required nowhere | `RESOLVED` | **Yes** | [`02:98-116`](../../reformation/modules/02-direct-work.md) requires model placement with a rejected simpler alternative and cost per accepted outcome, with `cost not exposed` rather than an invented figure |
| `P2-6` Two overlapping fault taxonomies | `RESOLVED` | **Yes** | One cheapest-first five-layer taxonomy, repeated identically in four places, with stuck-state words explicitly demoted to observations ([`04:67`](../../reformation/modules/04-hidden-diagnosis.md)) |
| `P2-7` Live correction was half a sentence | `RESOLVED` | **Yes** | Named `BOUNDARY CALL` with four parts, a receipt requirement, and an explicit prohibition on smuggling scope ([`02:124-133`](../../reformation/modules/02-direct-work.md)) |
| `P2-8` Constraint budgeting absent | `RESOLVED` | **Yes** | [`02:61-73`](../../reformation/modules/02-direct-work.md) numbered constraints, five classes, declared precedence, collision rule, and a stop-for-decision requirement |
| `P2-9` Supersession implicit | `RESOLVED` | **Yes, substantively** | [`08:38-50`](../../reformation/modules/08-durable-state.md) is a full deterministic policy. Residual: two names for the key (`P2-6` in §8) |
| `P3-1` `EVIDENCE_RECORD` unreferenced by modules | `RESOLVED` | **Yes** | Every module indexes into it |
| `P3-2` Duplicate seven-level ladders | `RESOLVED` | **Yes** | Single ladder in the course map with a no-restatement rule. Residual: Module 12 restates it (`P2-7`) |
| `P3-3` Competing module-shape frameworks | `RESOLVED` | **Yes** | One authoritative 14-item contract that explicitly names and replaces the four prior frameworks ([`AUTHORING_GUIDE.md:23`](../../reformation/AUTHORING_GUIDE.md)) |
| `P3-4` Falsifier not a brief field | `RESOLVED` | **Yes** | [`DIRECTION_BRIEF.md:33`](../../reformation/templates/DIRECTION_BRIEF.md), and strand 1 makes it universal |
| `P3-5` Time estimates did not sum | `NO LONGER APPLICABLE` | **Agree** | Durations removed |
| `P3-6` Trim the pattern catalog | `PARTIALLY RESOLVED — better than requested` | **I withdraw the original recommendation** | The catalog was not trimmed; it was **split** into seven core production defaults and seven advanced/reference entries, with a warning that a label never justifies an architecture ([`PATTERN_CATALOG.md:5`](../../reformation/PATTERN_CATALOG.md)) and a note that several advanced labels are mechanically the same as core patterns ([`90`](../../reformation/PATTERN_CATALOG.md)). This preserves the vocabulary while removing its aspirational pull — a better solution than deletion |
| `P3-7` State the real-recurring-task prerequisite | `RESOLVED` | **Yes** | [`README.md:15`](../../reformation/README.md) |

**Summary:** 23 `RESOLVED`, 3 `PARTIALLY RESOLVED`, 2 `NO LONGER APPLICABLE`, 0 `STILL PRESENT`, 0 `REGRESSED`. Two prior recommendations I now disagree with: the calibration scoring form (withdrawn and replaced) and the pattern-catalog trim (superseded by a better solution the team found).

**The new findings in §8 are mostly not carry-overs.** `P0-1`, `P1-1`, `P1-2`, `P1-3`, `P1-4`, `P2-1`, `P2-2`, and `P2-3` all concern the *measurement validity of mechanisms the revision introduced* — a class of problem that did not exist in the earlier version because the mechanisms did not exist. That is the expected shape of a second review, and it is a better problem to have.

---

## 15. Prioritized revision plan

### Before adapter implementation

1. **`P0-1`** Recast calibration: promote the accumulated closeout series to primary instrument, demote the two-anchor gap comparison, add anti-hedging, score process not magnitude. Touches `README.md`, `00`, `12`, `CALIBRATION_RECORD.md`, `EVIDENCE_RECORD.md`, `HANDOFF.md`. *Do this first — every adapter will otherwise build the invalid instrument.*
2. **`P1-5`** Restore the canonical transfer-seed line as the body template in 11 modules. Mechanical.
3. **`P1-3`** Define the Module 03 completion rule for simulation-only adapters; replace the "only a special adapter" necessity claim with an observable requirement; require more than one run and a soft constraint; add the two adapter anti-fakes to the obligation-matrix row.
4. **`P1-1`** State the no-partial-credit rule for adjacent/superordinate layers; require omission-class faults in the key; add grader calibration and reconciliation to the hidden-fault section; report localization cumulatively.
5. **`P1-4`** Bring Module 11's listener gate up to Module 12's standard: protected rubric, non-author scorer, mechanical non-interaction protocol, evaluator-selected task.
6. **`P1-2`** Require at least one positive (adoption) case across 08/09/10; grade the workload characterisation rather than the verdict; mark operation proofs as standardised-conditions evidence.
7. **`P2-4`, `P2-5`, `P2-6`, `P2-7`, `P3-1`, `P3-2`** Consistency edits. All mechanical.

### During adapter implementation

8. **`P2-1`** Canary positive control and content-level observable — an adapter obligation, testable at build time.
9. **`P2-2`** Minimum failure count for a ranking claim in Module 05.
10. **`P2-3`** Require at least one interaction/precedence causal control per learner; score predictions against ground truth; seed one omission-class defect.
11. Flag Module 07's authorship load and name the accessible route concretely in the first adapter built for it.
12. Add an attempt ceiling and stop rule to `GETTING_UNSTUCK.md`.

### Pilot-study questions

- Does the accumulated closeout series actually produce enough forecast-outcome pairs with usable confidence values to compute a calibration statistic, or do learners leave the confidence column blank?
- What is the observed inter-grader agreement on fault-layer naming with a real answer key and two graders? If it lands near the published κ 0.31–0.46, layer naming needs reconciliation before it can be scored at all.
- How many eligible learner-owned runs actually exist at Module 05 across a real cohort? This determines whether the supplied corpus is the exception or the norm.
- Can a capable non-developer complete Module 07's workflow specification in a declarative surface without assistance? This is the single highest feasibility risk in the core.
- Does the two-proof structure produce any adoption decisions in practice, or does every learner decline every conditional mechanism?
- How much does the person-transfer verdict vary across recipients for the same package?

### Advanced-extension improvements

- Advanced 01–03 all mark the accessibility column `~`; each requires code or specialist tooling and none states an accessibility path. Since these are explicitly non-core and gated on maintainability, a stated position ("accessibility parity is not offered for advanced extensions; here is the accommodation") is sufficient and better than silence.
- Advanced 02's egress-allowlist worked case is excellent; a second worked shape (a procedure or a tool boundary, both named as permissible at [`Adv02:20`](../../reformation/modules/advanced/02-port-control-second-harness.md)) would prevent implementers reading the worked case as the only case.
- Advanced 03's transfer gate is `Person` but, unlike Modules 11 and 12, it does not specify a rubric or a non-author evaluator for the qualified-recipient check ([`Adv03:273`](../../reformation/modules/advanced/03-post-training-evaluation.md)). Same fix as `P1-4`.

---

## 16. What not to change

1. **The per-module adapter obligation matrix and its five interpretation rules.** This is the specification's core contribution.
2. **Rule 4** — hidden means hidden from both the learner and the system under test. Weakening this to "hidden from the learner" would silently break Modules 04, 07, 08, 09, 10, 11, and 12 at once.
3. **The independent-check definition**, including the refusal to treat a second model as automatically independent.
4. **The hidden-fault security and grading section.** Every clause in it prevents a specific leak.
5. **The two transfer claims and their non-substitutability**, and the separate checkbox blocks in `HANDOFF.md` that make substitution visible.
6. **Module 05 in full.** Do not add a starter taxonomy "to help learners get going" — the prohibition at [`05:18`](../../reformation/modules/05-error-analysis.md) is what makes the module work.
7. **Module 04's refusal to credit a guessed repair**, and the repair-status enum that lets `NOT ATTEMPTED — localization only` be a legitimate outcome.
8. **Module 11's replacement held-back set rule.**
9. **Module 10's merged-artifact recheck against the pinned gate**, and the prohibition on automatic adoption.
10. **Module 08's deterministic supersession order** and its explicit rejection of similarity, vote, confidence, and arrival order.
11. **Module 06's ordering** — unavailable, then structurally bounded, then a few raw-action gates — and *"Fewer prompts are not automatically safer."*
12. **Every evidence-boundary section.** These are the best-supported design choice in the course and the reason its negative claims are defensible.
13. **The `HOLD` boundary** and its per-module restatement.
14. **The `AUTHORING_GUIDE.md` language rules**, especially *"Never say the learner need not understand it"* and the executed / facilitated / simulated distinction.
15. **`PATTERN_CATALOG.md`'s core/advanced split** with the label warning. Do not trim it further.

---

## 17. Blind spots and unresolved decisions

**My independence is partial and I have said so.** I authored the prior review earlier in this session. The strongest evidence that this review is not merely confirmatory is that its top finding withdraws a prior recommendation this team implemented faithfully. But a reviewer who had never seen the earlier document might weight things differently, and a third-party review before implementation would be worth its cost.

**Reliability figures are borrowed.** The κ values, generalizability coefficients, and item-count thresholds come from medical and computing-education assessment. They establish that *four items cannot carry a verdict* and *cause-category naming is low-agreement* as general properties of these measurement types. They do not tell you what this course will observe. The pilot questions in §15 are the way to find out, and I would not spend heavily on raising item counts before running them.

**I did not test the specification against a real implementation team.** Every "a team could omit this while claiming compliance" claim in §10 is a reading of the text, not an observation. Some may be closed by adapter conventions that do not exist yet.

**The Module 05 corpus problem may be larger than it looks.** If most learners meet error analysis on a supplied corpus, the course's central transferable skill is first practised on someone else's failure distribution and only revisited at the capstone, where fewer than 20 accumulated runs sends it to `HOLD` ([`12:138`](../../reformation/modules/12-capstone.md)). It is possible for a learner to complete the course having never analysed their own failure distribution — honestly recorded, but a weaker end state than the README implies. Whether this matters depends on cohort composition, which I cannot assess from files.

**I have not resolved whether the two-proof design can be fixed or only bounded.** My recommendation (grade the characterisation, require one adoption, mark operation proofs as standardised) improves it. Whether "correctly declined" can ever carry a competency claim without a counterfactual is a genuinely open question, and the honest fallback is to record selection decisions as *documented reasoning* rather than as proof.

**Unresolved decision for the team:** whether the calibration strand should survive at all in scored form. My recommendation keeps it, because the perception gap it targets is real and large and because a committed prediction improves how the learner encodes the outcome. But a defensible alternative is to keep the prediction ritual as a learning device, drop every scored calibration claim, and delete the end-state bullet that promises calibration. That is a smaller, safer course. I recommend the first path because the accumulated series is already in the template and costs little to score properly — but the second is not wrong.

**Two research areas returned findings I could not verify against primary sources this session** — the specific numeric claims about adapter-free routes to compaction evidence, and the trigger-action rule-interpretation accuracy range. Both are used at `medium` confidence and neither carries a `P0` or `P1` finding on its own.

---

## Final report

**Review file written:** [`docs/analysis/2026-08-08-reformation-independent-review.md`](2026-08-08-reformation-independent-review.md). No file under `reformation/` was read-modified, and no other repository file was touched.

**External sources:** 118 unique, from 7 adversarial research sweeps (274 tool calls). By type: 46 peer-reviewed studies and systematic reviews (assessment reliability and generalizability, entrustment and competency literature, calibration training, teach-back and handoff outcomes, debugging instruction, end-user programming); 21 preprints and recent arXiv papers (compaction governance, compaction fabrication, agent evaluation); 14 standards and security-guidance documents (covert-channel analysis, CWE, security testing practice); 12 vendor engineering and product documentation sources; 15 named-practitioner and independent-analysis sources; 10 industry field studies and telemetry reports. Roughly 40 are cited directly in §8.

**Files inspected:** 32 of 32 under `reformation/`, all read in full — 8 architecture documents, 13 core modules, 3 advanced extensions, 8 templates (6,966 lines). Plus 1 prior review, read at Phase 8.

**Five highest-confidence findings**

1. **The calibration instrument cannot measure calibration as specified** (`P0-1`). Gap-size scoring plus a two-anchor start/end comparison is a difference-score design against a noisy measured value; it will report improvement produced by regression. The fix is already half-present in `CALIBRATION_RECORD.md`'s per-module closeout row. **This withdraws a recommendation the previous review made.**
2. **Transfer-seed schema compliance is broken in 11 of 16 modules**, and the capstone artifact that consumes those seeds requires the fields the 11 modules omit (`P1-5`). Verified mechanically.
3. **Four hidden cases cannot support a localization verdict, and layer naming is the least reliable dimension in the grade** (`P1-1`). Comparable formats need substantially more items; published expert agreement on cause categories runs κ 0.31–0.46.
4. **The two-proof conditional design has no positive-case counterweight and no ground truth for a correct decline** (`P1-2`). A record of all-declines plus one engineered qualifying case reads as completion.
5. **Six named internal-consistency defects**, all mechanically verified: `(thing/entity, property)`; 19 uses of `cold` against the guide's own ban, two genuinely ambiguous; Module 09's prerequisite mismatch; Module 12's ladder restatement; the missing `<br>` in all 16 identity manifests; the undeclared `**Path:**` field in three modules.

**Sources and tests unavailable**

- No adapter, fixture, or instructor pack exists, so nothing about learner experience could be tested — only the specification.
- Rendered-Markdown verification was not performed; the `<br>` finding is from source inspection.
- Two research claims could not be traced to primary sources within the session and are flagged `medium` confidence in §17; neither carries a `P0` or `P1` finding alone.
- No paywalled sources were purchased; where only an abstract was available the claim is limited to what the abstract states.

**Final `git status --short`**

```text
 M .env.example
 M HOSTING.md
 M server.py
 M site/blocks/p8.html
?? docs/analysis/2026-08-08-reformation-curriculum-review.md
?? docs/analysis/2026-08-08-reformation-independent-review.md
?? reformation/
?? site/css/friday-chat.css
?? site/friday-chat.html
?? site/js/friday-chat.js
```

**Confirmation.** Identical to the baseline recorded at the start of this review except for one added file: `docs/analysis/2026-08-08-reformation-independent-review.md`. `reformation/` remains untracked and unmodified. No course file was edited. The four pre-existing modified files and the other untracked files were dirty before this review began and were not touched.
