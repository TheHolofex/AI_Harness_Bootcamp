# System 3 Analysis: Reformation Module 00 vs 01 sequence
Date: 2026-08-23

## Context

- Bootcamp 2 build rule: later modules are not drafted until the current module closes its review gates.
- Module 00 verdict (2026-08-14): accepted for a controlled single-platform pilot with a facilitator present. Not accepted as five-platform working, not accepted as a measured learner experience, not accepted against Class F until three people score the prose.
- Module 00 Reference §1.1: an unexecuted setup path is a broken program. Five platform rows remain UNTESTED end to end.
- Module 00 Class F requires three human reviewers at 32/32. Round-1 files are language-model seats; check D2 refuses a Class F pass claim until the reviews declare a human reviewer.
- Module 00 working tree is dirty: fixture set moved to `tests/fixtures/`, checker gained invented-specifics checks, ten new fail fixtures are untracked. Criterion A2 requires on-disk file count to equal `git ls-files`.
- Module 01: Reference frozen 2026-08-14. Five files committed (Reference, hash, gauntlet prompt, RED oracle, `test_module_01.py`). Learner package, scripts, rubric, runbook, custody, and evidence are untracked. Local oracle-round-5: 167 PASS / 0 FAIL. Workflow tests OK. No `reviews/`, no `REVIEW_VERDICT.md`. Empirical criteria M1-29–M1-33 remain pilot work.
- Standard verdict (2026-08-12): build and time Modules 00, 03, and 08 first. Module 01 already exists as a second-module factory test.
- Last reformation commit: 2026-08-14. Course conclusion is nine independent runnable modules, not a polished Module 00.

Known: 00 cannot be fully finalized in this session. 01 can be closed to the same bar 00 already reached.

Unknown: whether the dirty 00 checker expansion currently passes B6. Whether a cohort date exists. Whether three human reviewers can be scheduled this week.

## Problem Frame

1. Which increment moves a nine-module course closer to a first facilitated week?
2. Which remaining 00 work is closeable here, and which work only looks closeable?
3. Can two in-flight module trees share a factory that has been proven once?

Assumptions:

1. "Conclusion" means nine independent runnable modules at the Module 00 pilot-acceptance bar, not Class F / five-platform / timed-pilot closure of Module 00.
2. Class F, five-platform execution, and M1-29–M1-33 cannot be closed by authoring more prose.
3. The build rule's "review gates" means the written verdict bar Module 00 already recorded, not the human-blocked remainder.
4. A dirty Module 00 tree that fails A2 is an open station, not a closed one.
5. Parallel work on 00 and 01 will fork voice, evidence, and oracle conventions before the factory has been reused once.
6. Module 01's untracked tree is a closeable package, not a new design problem.
7. Highest remaining course risk after 00/01 sits in Modules 03 and 08, not in further 00 checker depth.
8. Leaving 00's invented-specifics expansion half-applied creates a worse state than either landing it or reverting it.

## Perspectives

### Skeptic

"Finalize Module 00" is the wrong job. The 2026-08-14 verdict already named the remaining work as human and machine execution. More authoring on 00 cannot convert UNTESTED into executed. The dirty checker expansion is a new campaign wearing the clothes of closeout.

Challenges assumption 4 only in part: a dirty tree must be locked, but locking is not finalizing.

Sees: 00 can absorb unbounded pin, platform, and checker work while 02–08 stay empty.

### Outsider

A line does not stop because station 1's paint inspection is unscheduled. Station 1's spec is locked; the next station runs. A kitchen mid-renovation also does not take tickets. The dirty fixture move is a kitchen renovation. Close the hatch, then fire the next ticket.

Challenges assumption 3: the build rule is about a closed station, not about infinite remaining quality work.

Sees: sequence is lock-then-advance, not polish-then-advance and not two open stations.

### Historian

Course 1 shipped week-by-week and repaid it in P4/P5 pivots. Reformation already deleted 7,502 lines of premature lesson bodies (decision D-10 / SD-15–SD-16). Sequential closeout is the learned pattern. The 2026-08-12 shortlist of 00, 03, 08 was written before Module 01 existed as a green uncommitted package.

Challenges assumption 7 only on timing: 01 is now the cheapest way to prove the factory a second time, which 03 and 08 will need.

Sees: 01 closeout is factory proof. 03/08 remain the later risk modules.

### Futurist

Module 00 pins (n8n 2.34.5, OpenCode 1.18.17, Node 24) will be stale before five clean machines are run. Perfecting install paths now writes against melting ice. Source-verification judgment ages. A second closed module is the reusable asset.

Challenges assumption 1's implied urgency on 00 polish.

Sees: 00 setup rusts; 01's mechanism does not.

### Advocate

A learner cannot take Module 01 on a machine Module 00 never configured. They also cannot take a one-module course. The facilitator already has a 00 package accepted for a watched pilot. They do not have a second session.

Challenges the implied learner-blocking story for holding 01.

Sees: 00 is good enough to teach with a facilitator in the room. 01 is the missing Monday afternoon.

### Conflicts & Agreements

Agree: do not run 00 and 01 as parallel authoring campaigns. Do not treat Class F or five-platform execution as this session's closeout. Do not start Module 02.

Conflict: Skeptic would revert the 00 checker expansion as scope creep. Outsider would land it if the tests already exist, because an open hatch is worse than a small increment. Historian wants 01 closed now that it exists. Advocate wants Monday PM to exist.

Open question: land or revert the 00 invented-specifics expansion. That is a one-tree lock, not a sequencing fork.

## Creative Reframes

Inversion: close neither module. Extract the shared factory (Reference, oracle with negative fixtures, verdict table with reproducible commands, custody, voice panel) and apply it to 01–08. 00 already is that factory. 01 is the first reuse. Closing 01 *is* extracting the factory.

Pre-mortem: the course is still one module in October because "finalize 00" became five-platform archaeology, the 01 tree stayed untracked, and two parallel agents forked the oracle style. Failure mode is two dirty trees and no second verdict.

Restaurant analogy: lock the line, serve the next ticket. Do not rewrite the menu while tickets wait, and do not plate from a disassembled pass.

## Meta-Cognitive Audit

| Dimension | Score | Evidence |
|-----------|-------|---------|
| Problem definition | 4/5 | Three frames distinguish closeable work from human-blocked work. Cohort date still unknown. |
| Assumption validity | 4/5 | Assumptions 2 and 5 are strong. Assumption 6 is the weakest: 01 may hide review defects the oracle does not see. |
| Perspective diversity | 4/5 | Five seats. Missing: a live facilitator who has to teach 00 on Monday. |
| Creative exploration | 3/5 | Factory-reuse reframe and pre-mortem changed the job from "00 vs 01" to "lock then reuse." No third architecture appeared. |
| Bias awareness | 4/5 | First instinct was "finish remaining 00 then 01." Process changed the 00 job from finalize to lock. |

### Active Biases Identified

- Sunk cost on Module 00's depth and on the dirty checker expansion.
- Anchoring on the 2026-08-12 "build 00, 03, 08 first" line, written before 01 existed.
- Availability of the vivid five-platform UNTESTED table, which is real and not closeable here.
- Status-quo pull toward more 00 work because that tree already has a verdict format.

## Synthesis & Recommendation

**Close Module 01 to the Module 00 pilot-acceptance bar. Do not parallelize. Do not reopen Module 00 as a finalize campaign.**

Lock the Module 00 working tree first: land the in-flight invented-specifics checker if `tests/test_checker.py` and `tests/oracle.py` are green; revert it if they are not. That lock restores A2 and leaves 00 at the 2026-08-14 bar.

Then finish Module 01:

- parsimony-cut intermediate evidence rounds
- independent technical, curriculum, adversarial, and voice reviews
- `evidence/REVIEW_VERDICT.md` with reproducible commands
- list Module 01 under "Available now"
- keep M1-27 (human panel) and M1-29–M1-33 marked unmeasured

After 01 has a verdict, the next build is Module 03, then 08, matching the 2026-08-12 risk order. Modules 02, 04–07 follow the same factory.

Parallel 00+01 loses. Two dirty trees, one unproven factory, and a shared voice/oracle convention. The directories are separate; the standard is not.

"Finalize 00" loses. Class F, five-platform execution, and timed first-artifact measurement are the remaining 00 work, and none of them are authoring.

## Blind Spots & Uncertainties

- The 00 invented-specifics expansion may fail B6 or over-reject the paraphrase fixture. Land-vs-revert is unresolved until those commands run.
- Module 01 oracle-green does not imply review-green. M1-04, M1-17, M1-25, M1-27 are human or functional.
- A facilitator who must teach 00 next week would weight platform execution higher than a second module. No cohort date is in the repo.
- Assumption 6 may be wrong: 01 could need a Reference amendment the way 00 needed v2. That would delay 01 closeout without changing the sequence.
- Module independence means a held 00 does not block 01 participation. It does not mean a learner can skip setup. Preflight remains an entry condition.
