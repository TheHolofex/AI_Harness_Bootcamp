# System 3 Analysis: Standalone P5
Date: 2026-08-05

## Context

- The durable learning contract is already clear: define trust before intake, catch a false citation, catch a contradiction, contain a hostile instruction, prove the bounded effects are absent, and distinguish permission controls from truth judgments.
- The seven-file intake pack, closed reference corpus, strict candidate schema, validator, promoter, staging inventory, runtime-config builder, and session auditor are P5-owned.
- P4 and Obsidian enter the current exercise through the trusted target, baseline and recovery steps, launcher wording, hostile fixture, and the poisoned-acceptance cycle. They are not required by the three-poison triage mechanism.
- The current run creates or uses a P4 vault, recovery copy, cold-query project, staging project, control project, two baselines, two agents, an MCP writer, and an MCP reader. Several of those surfaces can fail before the learner reaches triage.
- The current deterministic P5 suite passes. Live Windows launcher behavior and the full Obsidian write/read/repair cycle remain unverified on the author host.
- The exact learner failures are not yet categorized. The redesign must stay honest about that unknown and make the exercise easier to reset and diagnose.

## Problem Frame

### Three useful statements of the problem

1. **Operational frame:** Convert an untrusted batch into a reviewed triage record without allowing text inside the batch to become machine authority.
2. **Teaching frame:** Give the learner one visible loop in which evidence checks, capability limits, deterministic validation, and human judgment each do a different job.
3. **Lab-design frame:** Ship all starting state inside P5 so every learner can delete two working folders and return to the same known state.

### Assumptions

1. The core lesson is the intake boundary, not persistence or retrieval. The learning objectives and three planted poison classes support this reading.
2. A P5-owned closed reference corpus is sufficient ground truth for the graded checks. The validator already verifies its manifest and resolves evidence against it.
3. The protected state can be the frozen staged inputs and reference pack. A separate durable store adds topology without adding a new decision the learner needs to make.
4. The absence claim must stay scoped to artifacts and capabilities the run actually checks: staged files, exact output paths, configured tools, and exported assistant/tool-call channels.
5. The exposed agent may write one candidate file. Content inside that allowed file still needs deterministic and human review; a path permission cannot certify truth.
6. OpenCode remains the exercise engine. P5 may rely on pre-work installation, but not on output or state from another exercise.
7. The deliberate poisoned-acceptance cycle is a separate persistent-knowledge lesson. Removing it does not weaken the stated P5 capability contract when the control-limit lesson remains in the candidate-validation gate.
8. The fifth intake file should be unambiguously clean. A hidden uncited falsehood creates a fourth poison and makes the stated class count unreliable.
9. Existing checklist identifiers should remain stable so browser progress and course navigation do not reset.

## Perspectives

### Learner advocate

The run should present one map: prepare, expose, validate, approve, prove. Every folder and receipt should appear because it answers a question the learner can state. This challenges Assumptions 3 and 6: even a self-contained launcher can become the lesson if setup dominates the first hour.

### Reliability engineer

A separate protected directory provides strong physical separation, but it also requires a new seed, baseline writer, recovery procedure, and tests. The existing full-tree staging inventory already hashes every fixed input and rejects any change, removal, symlink, or unexpected output. This challenges Assumption 3 by demanding narrow claim language in exchange for the simpler topology.

### Adversarial reviewer

Exact-path write permission does not defeat poisoned content because the hostile text can still influence the allowed candidate. The validator and operator gate are the mechanism that catches that class of failure. This reinforces Assumption 5 and keeps the exercise from collapsing into a permissions demo.

### Instructor

The exercise needs a stable answer key, a short recovery path, and receipts that can be inspected without replaying a learner's chat. P4 state and live Obsidian sessions make cohort support non-deterministic. This challenges Assumption 6 only if the OpenCode launcher itself cannot be made a single fail-closed step.

### Skeptic

"Prove nothing happened" can overstate what a local inventory and session export establish. The run cannot prove facts about unobserved processes or the wider machine. This challenges Assumption 4 and requires every outcome to name the checked surface instead of claiming universal containment.

### Conflicts and agreements

All perspectives support a P5-owned resettable start, the three poison classes, and the validator-plus-human promotion gate. The main disagreement is physical separation versus fewer setup surfaces. The scoped claim resolves it: P5 proves that its frozen reference pack and staged inputs were unchanged, no forbidden output appeared, and the exported session used only the allowed tools and paths. It does not claim that the whole machine was inert.

## Creative Reframes

### Intake compiler

Treat the agent as a parser. Untrusted Markdown compiles into a typed JSON candidate. A deterministic validator checks syntax and evidence invariants. A human supplies the authority needed to promote the candidate into the durable triage record. Hostile prose remains input data throughout the pipeline.

### Security checkpoint

The checkpoint is the product. The exercise does not need to send approved material into a downstream knowledge system to prove the checkpoint works. The reference corpus supplies the screening standard; the promoted triage record supplies the disposition receipt.

### Pre-mortem inversion

Six months after a failed cohort, learners remember how to repair an Obsidian connection and cannot explain why a clean permission report does not make a claim true. Removing the live store mutation leaves the four mechanisms visible: capability boundary, evidence checks, deterministic validation, and human authority.

## Meta-Cognitive Audit

| Dimension | Score | Evidence |
|---|---:|---|
| Problem definition | 5/5 | The learning contract and existing P5-owned mechanics align on one intake-gate loop. |
| Assumption validity | 4/5 | Repository evidence supports the design; categorized learner failure data is still absent. |
| Perspective diversity | 4/5 | Learner, reliability, adversarial, instructor, and skeptical views produce a real topology-versus-simplicity conflict. |
| Creative exploration | 4/5 | Compiler, checkpoint, and failure-inversion frames expose a smaller exercise shape. |
| Bias awareness | 4/5 | Sunk-cost and current-architecture anchoring were active; the recommendation removes the newest and most elaborate stage. |

### Active biases identified

- **Anchoring:** The first replacement idea was another protected store and another baseline script. Reframing the triage gate as the product removed both.
- **Sunk cost:** The poisoned-acceptance stage has detailed scripts, fixtures, and prose. Its implementation effort does not make it part of the core P5 lesson.
- **Status quo:** Keeping generic all-connector disablement is justified only as a verified capability boundary. The learner-facing prose should make it one setup result, not a concept prerequisite.

## Synthesis and Recommendation

Rebuild P5 as a five-stage, P5-owned quarantine lab:

1. Write the trust rule and evidence scope in `p5-control` before opening intake.
2. Create a fresh `p5-staging`, copy the P5 intake and closed reference pack, prepare the restricted OpenCode runtime, and freeze a full-tree inventory.
3. Run one exposed agent that writes only `out/triage_candidate.json`, then validate the candidate outside the session, review one table, and use one operator approval to promote `triage_record.md`.
4. Export and audit the session, compare the staging inventory, and verify the runtime-config hash.
5. Map each control to the claim it supports and close with a payload-free handoff.

The hostile fixture should target P5-owned reference files and forbidden output paths. The fifth intake file should become clearly clean. The page should state exactly three planted poison classes. The active launcher and auditor should retain generic connector disablement while dropping all Obsidian-specific credentials, fields, and messages. The P4 baseline wrapper, fallback vault, reader harness, and poisoned-acceptance workflow should leave the active exercise.

The evidence claim stays bounded: the P5 reference pack and staged inputs remained byte-identical, only approved output paths appeared, and the exported session contained no forbidden tool or path use. The validator and operator disposition establish content quality; the permission boundary does not.

## Blind Spots and Uncertainties

- A timed learner pilot is still needed to set the new duration and identify instruction-level friction.
- The pinned OpenCode launcher has no automated Windows test in this repository.
- Future OpenCode export-shape changes may require updates to the session auditor.
- A staged reference pack is logically protected, not physically outside the exposed project. The runtime permission proof and before/after inventory carry that boundary; the page must not imply stronger isolation.
- The logistics domain may add cognitive load for learners unfamiliar with the scenario. The closed references reduce outside knowledge requirements but do not remove domain vocabulary.
