# P4 learner pack · Director Loop

P4 turns a note vault into a small personal operating harness. The practical result is still the point: two answers and a Morning Brief that help a director decide. The harness earns its place by making evidence, next actions, stopping conditions, resume behavior, and quality checks inspectable.

Allow 2 hours 45 minutes for this module after the 30-minute Agent Loops and Agentic Patterns presentation.

## What you finish

Your completed copied vault contains:

- two stable-ID answer notes under `Answers/`;
- `Audit.md`, with a human disposition and exact raw excerpt for every first-pass claim;
- `Morning_Brief.md`, using only `SUPPORT` claim IDs and direct raw evidence;
- personalized `AGENTS.md` and `Harness/HARNESS_CARD.md`;
- an approved graph of normalized notes, each with `Raw sources:` lineage;
- an observable fixed inbox inventory and a six-open adaptive packet ledger in `RUN_TRACE.md`;
- `RESUME_RECEIPT.md`, candidate-check and evaluator receipts, `EVAL.md`, and `HANDOFF_RECEIPT.md`;
- `BASELINE_MANIFEST.json`, written only by the untouched course verifier after the full release passes.

The external copy of that manifest is P5's trusted starting point.

## Why this is an agent loop

```text
fixed outer flow
  -> fixed read of four inbox captures
  -> human-approved organization
  -> question selects relevant raw packet
  -> observation selects next linked packet
  -> stop on support, named gap, repetition, or budget
  -> human audit and deliberate hand-back
  -> fresh resume from saved state
  -> trusted candidate check
  -> fresh read-only evaluation
  -> zero or one evidence-driven repair
  -> scoped handoff and external baseline
```

The four inbox reads are fixed and do not consume the adaptive budget. Adaptivity starts when a question and an observed raw record determine the next packet. A later packet open is earned only when a fixed capture or earlier packet links to it. Each required answer must use packet evidence reached by that loop; otherwise the loop is decoration.

The harness deliberately rejects a router, parallel worker team, plugin, new MCP server, and free-form reflection loop. There is one task class, a bounded local evidence surface, and two real oracles: the deterministic checker and a fresh read-only evaluator.

## 1. Copy the seed

Open PowerShell:

```powershell
$courseRoot = "$env:USERPROFILE\Documents\HarnessBootcamp\AI_Harness_Bootcamp"
Copy-Item -Recurse "$courseRoot\mission_flesh\p4\vault_seed" "$env:USERPROFILE\Documents\p4-vault"
Set-Location "$env:USERPROFILE\Documents\p4-vault"
Get-ChildItem -Force
```

Open `Documents\p4-vault` as both the Codex project and the Obsidian vault. The folder directly containing `MOC.md` is the root.

If that destination already exists, rename the old folder before copying. Do not copy over a prior attempt.

## 2. Personalize the operating contract

Before invoking the skill, replace every complete `[REPLACE: ...]` marker in only these two files:

- `AGENTS.md`
- `Harness/HARNESS_CARD.md`

Use real choices: audience, decision horizon, output order, acceptable evidence strength, escalation condition, non-goal, budgets, and reasons not to add machinery. A cosmetic preference does not personalize a harness; a rule that changes an output or stop condition does.

The copied `Harness/SOURCE_MANIFEST.json`, skill, evaluator configuration, and checker are course-owned contracts. Do not edit them.

## 3. Run the integrated skill

Invoke:

```text
$director-loop
```

The copied skill carries the exact questions:

1. What are the top operational risks this week and which notes support each?
2. What decision is blocked and what evidence is missing?

The optional stretch is: Where are we over-confident?

First, the run reads the four short inbox captures as a fixed batch. It proposes note titles, hubs, links, and preserved status words. Approve the structure only if you can navigate it later.

After approval, every generated normalized note must contain a line like:

```text
Raw sources: [[Source_Packet/EXP-214_eu-export-qa]]
```

`MOC.md` links all four hubs. A hub must reach every generated note. Generated notes help traversal; they never certify their own content.

## 4. Make adaptive retrieval earn its cost

The adaptive ledger permits at most six `Source_Packet` opens. A starting packet must be linked by one of the fixed inbox captures. A later packet must be linked from an already opened raw record. Record the parent link and observable result for every open.

Stop a branch when you have enough direct evidence for the active claim, can name the missing evidence, repeat an observation, or reach a declared budget. Do not open a record merely to fill six rows.

Write answer claims in this form:

```text
- [Q1-01] The exact decision-driving claim. [[Source_Packet/EXACT_RECORD]]
```

Keep the ID stable. Apart from headings, keep answer content in these claim bullets; uncited prose cannot carry a hidden assertion. Each answer needs at least two distinct direct evidence roots, including at least two earned packet records. A normalized-note link does not count as evidence.

## 5. Hand the evidence judgment to the human

The run prepares this exact table in `Audit.md`:

```text
| Claim ID | Claim | Evidence root | Source excerpt | Disposition | Resolution |
|---|---|---|---|---|---|
```

For every first-pass claim:

1. Open the direct evidence root.
2. Confirm its hash-bound path appears in `SOURCE_MANIFEST.json`.
3. Copy the exact carrying excerpt into the audit row.
4. Assign `SUPPORT`, `PARTIAL`, or `NOT SUPPORTED`.
5. Use `QUALIFIED: <exact final wording>` for a retained partial claim.
6. Use `REMOVED: <reason>` for a removed partial or unsupported claim.

Do not delete an adverse row after removing its claim. The preserved row is part of the useful audit trail.

Before the human audit, the run saves before-hashes in `RESUME_RECEIPT.md`, records `HUMAN_HAND_BACK` and the one next action, and ends the build goal/chat. Perform the audit, then start a fresh goal/chat and invoke `$director-loop` again.

The resumed run reads state first. It verifies that processed captures and normalized notes are byte-identical, and that each answer's `Fresh-open` hash matches its `Saved-at-pause` hash. It records zero reprocessing and recreation, then continues only at the saved next action. A later `Final` answer hash may differ only when the receipt names the stable ID of the adverse audit row that caused it.

## 6. Build the brief from claim-level support

Every brief bullet keeps the supported claim ID, exact final answer wording, and same evidence root:

```text
- [Q1-01] The exact supported final answer wording. [[Source_Packet/EXACT_RECORD]]
```

The brief must include:

```text
Provenance: vault only; audited sources only
```

Apart from headings and the provenance line, keep brief content in those claim bullets. Support is claim-level, not merely file-level. One supported sentence in a raw record cannot whitelist a different unsupported assertion from that record.

## 7. Use the untouched checker and preserve receipts

The copied vault cannot validate itself. Set the untouched course checker path:

```powershell
$courseRoot = "$env:USERPROFILE\Documents\HarnessBootcamp\AI_Harness_Bootcamp"
$vault = "$env:USERPROFILE\Documents\p4-vault"
$courseVerifier = "$courseRoot\mission_flesh\p4\vault_seed\tools\verify_vault.py"
```

At `AWAITING_CANDIDATE_CHECK`, run and preserve the first result:

Before the command, `RUN_STATE.md` must keep the resumed Run ID, use `Phase: AWAITING_CANDIDATE_CHECK`, `Status: HAND_BACK`, and `Terminal reason: HUMAN_HAND_BACK`, point to both answers, `Audit.md`, `Morning_Brief.md`, and `Harness/RESUME_RECEIPT.md`, and name the trusted candidate check as its only next action.

```powershell
py -3 $courseVerifier $vault --candidate | Tee-Object -FilePath "$vault\Harness\CANDIDATE_CHECK_FIRST.txt"
```

Never overwrite the first receipt. The checker verifies the trusted source hashes and copied contracts, stable claim IDs, exact audit excerpts, graph reachability, fixed and adaptive reads, direct packet use, resume continuity, and brief support.

Do not repair a candidate HOLD yet. Freeze candidate inputs between the check and evaluation—do not update state, trace, answers, audit, brief, notes, or evidence; save only the excluded receipt files. Spawn exactly the read-only evaluator defined in `.codex/agents/director_evaluator.toml` against the same fingerprinted snapshot regardless of the first candidate verdict. Save its exact JSON as `Harness/DIRECTOR_EVALUATOR_FIRST.json`; its full-candidate and stable-content fingerprints must equal the pair in `CANDIDATE_CHECK_FIRST.txt`.

Candidate and evaluator HOLDs share one repair budget:

- Merge every first candidate and first evaluator blocker before changing files.
- If either first receipt is on `HOLD`, make one smallest combined correction, save the candidate recheck to `CANDIDATE_CHECK_FINAL.txt`, and save a fresh evaluator receipt for that same new fingerprint pair to `DIRECTOR_EVALUATOR_FINAL.json`. The full candidate fingerprint must change.
- In `EVAL.md`, record `Repair scope: CONTENT` when the stable-content fingerprint changes. Use `CONTROL_ONLY` only when stable mission content correctly stays unchanged and every blocker concerns retrieval control, resume, state, or trace. Copy every exact first blocker into `Repair justification`; do not make a cosmetic content edit merely to change a hash.
- If either final receipt remains on `HOLD`, hand back; the repair budget is exhausted.
- If both pass without repair, do not create final receipt files; each first receipt also serves as final.

Never erase first-pass findings. `EVAL.md` binds every receipt path and SHA-256, separates generator claims from evaluator verdicts, and computes overclaim only from evaluator HOLD rows the generator had called `READY`.

Each candidate receipt also binds the `RUN_STATE.md` Run ID and Goal plus the exact byte length and SHA-256 of `RUN_TRACE.md`. Preserve the first evaluated trace as an exact prefix. During the one repair, append the finding and repair; never rewrite prior rows. The final candidate receipt binds that longer prefix.

## 8. Finish, hand off, and freeze the baseline

After the final evaluator passes, complete `EVAL.md`, finalize `RUN_STATE.md`, and complete `HANDOFF_RECEIPT.md`. The handoff stays scoped to this run: terminal reason, accepted artifacts, chosen pattern, intervention and repair counts, candidate/evaluator results, residual risk, reflection, one bounded workplace trial, and resume result. Then append exactly this last block to `RUN_TRACE.md`; do not edit earlier trace bytes or add anything after it:

```text
## Closeout after evaluation

- Final trusted candidate check: PASS.
- Final fresh read-only evaluator: PASS.
- Scoped handoff completed with accepted artifacts and residual risk.

Terminal reason: SUCCESS
```

The handoff records `Candidate verifier result: PASS`. It does not self-assert the later full release. Keep `Manifest status: PENDING` permanently so writing the manifest does not make its own input stale.

Run the full release and write the in-vault manifest:

```powershell
py -3 $courseVerifier $vault --write-manifest
```

Copy the exact result outside the candidate vault, then verify that external copy:

```powershell
$stamp = Get-Date -Format "yyyy-MM-dd"
$evidenceDir = "$courseRoot\operator\evidence"
New-Item -ItemType Directory -Force $evidenceDir | Out-Null
$externalManifest = "$evidenceDir\P4_BASELINE_$stamp.json"
$externalHandoff = "$evidenceDir\P4_HANDOFF_$stamp.md"
if ((Test-Path $externalManifest) -or (Test-Path $externalHandoff)) { throw "Today's P4 evidence already exists. Preserve it; use the recorded path or a new operator-approved run ID." }
Copy-Item "$vault\Harness\BASELINE_MANIFEST.json" $externalManifest
Copy-Item "$vault\Harness\HANDOFF_RECEIPT.md" $externalHandoff
py -3 $courseVerifier $vault --check-manifest $externalManifest
```

`--check-manifest` is read-only. It rejects changed, added, or deleted vault files and never rewrites the external baseline. P5 must point to that external manifest, not a manifest that later intake can change inside the vault.

## Terminal reasons

- `SUCCESS` — release artifacts, audit, resume, receipts, and handoff pass.
- `NEEDS_EVIDENCE` — a decision-driving claim cannot be supported.
- `BUDGET_STOP` — the turn, time, or six-open limit is reached.
- `ERROR_CEILING` — a correctable operation still fails after its retry ceiling.
- `NO_PROGRESS` — the allowed repeated observation occurs without state change.
- `HUMAN_HAND_BACK` — the next action requires operator judgment or authority.

A fluent brief is not success. Success is a practical goal completed with direct evidence, bounded work, recoverable state, preserved interventions, and an explicit stopping reason.
