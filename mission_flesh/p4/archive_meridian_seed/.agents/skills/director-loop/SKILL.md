---
name: director-loop
description: Use for the P4 Director Loop when a learner needs to turn this vault into two direct-evidence director answers and an audited Morning Brief under the saved Harness Card. Do not use for intake outside the manifested vault or unrelated writing.
---

# Director Loop

Run one useful, bounded job. The saved vault—not chat history—is the system of record.

## Preflight or resume

1. Read `AGENTS.md`, `Harness/HARNESS_CARD.md`, and `Harness/RUN_STATE.md`.
2. Stop if a `[REPLACE: ...]` marker remains in `AGENTS.md` or `Harness/HARNESS_CARD.md`. Those are the only two files that must be personalized before the first run.
3. Confirm that the project root directly contains `MOC.md`. Work only inside that vault.
4. Read the active goal and the source boundary in `Harness/SOURCE_MANIFEST.json`.
5. If `RUN_STATE.md` is still the seed, initialize it from the active goal and append the inventory action and remaining budget to `RUN_TRACE.md`.
6. If `RUN_STATE.md` contains a prior hand-back and one next permitted action, resume that action. Do not initialize a second build, reopen processed sources, or recreate normalized notes.

The release checker is a trust boundary. Never edit it to make a result pass, and never use the copied `tools/verify_vault.py` for release. Run the untouched checker from the course repository against this copied vault.

## Required questions carried by this skill

Answer these exact questions:

1. What are the top operational risks this week and which notes support each?
2. What decision is blocked and what evidence is missing?

Optional only after the required artifacts pass: Where are we over-confident?

## Fixed outer flow

Follow one outer sequence:

1. scope and fixed inbox inventory;
2. propose organization;
3. receive human approval before organization writes;
4. perform bounded, question-driven packet retrieval;
5. write the two direct-evidence answers and prepare the audit;
6. save continuity hashes, update state, and end the build goal/chat for the human citation audit;
7. resume in a fresh goal/chat from saved state and complete `Harness/RESUME_RECEIPT.md`;
8. publish the Morning Brief from human-audited support;
9. pause at `AWAITING_CANDIDATE_CHECK`, run the deterministic candidate check, and preserve its exact receipt;
10. run exactly one fresh read-only evaluator on that same first snapshot regardless of candidate verdict; merge both finding sets into one total repair decision;
11. save evaluation, state, trace, and scoped handoff; then write and externally copy the baseline.

Do not add a router, parallel worker team, plugin, new MCP server, or reflection without an oracle. Those mechanisms do not remove a bottleneck in this run.

## Fixed inbox inventory and approved organization

Read each of the four files directly under `00_Inbox` once. This fixed batch is not the adaptive loop. Record each path and an observable result under `Fixed inbox inventory` in `Harness/RUN_TRACE.md`.

Propose titles, destination hubs, links, and preserved evidence-status words before writing. Wait for approval. Then:

- move each unchanged capture under `00_Inbox/processed/`;
- create decision-sized normalized notes;
- put `Raw sources: [[exact/evidence/path]]` near the top of every generated note;
- link every generated note from at least one of `People.md`, `Systems.md`, `Events.md`, or `Decisions.md`;
- keep all four hubs linked from `MOC.md`;
- never change raw evidence or `Harness/SOURCE_MANIFEST.json`.

A normalized note is navigation. It cannot certify its own claim.

## Six-open adaptive retrieval loop

Adaptive retrieval begins only after organization. It has a budget of six `Source_Packet` opens; the four fixed inbox reads do not consume that budget.

For the active question:

1. Start at the relevant hub and normalized note.
2. Choose a starting `Source_Packet` link that appears in one of the four fixed inbox captures. Record both paths.
3. Open a later packet only when a `Next ref` in an already opened raw record makes it relevant.
4. Record every open in the retrieval ledger using this exact table:

```text
| Open | Evidence root | Reference discovered in | Observable result |
|---|---|---|---|
```

5. Include at least one packet-to-packet hop. Stop a branch when the raw record supports the claim, names the missing evidence, repeats an observation, or the six-open/no-progress/time/turn budget stops it.
6. Write each answer claim as `- [Q1-01] ... [[direct/evidence/root]]` or `- [Q2-01] ... [[direct/evidence/root]]`. Apart from headings, keep answer content in these claim bullets so uncited prose cannot carry a hidden assertion. Keep each ID stable through audit and briefing. Every decision-driving claim must cite an opened manifested evidence root directly, and each required answer must use at least two distinct earned `Source_Packet` roots. A link to a generated summary is not evidence.

Never fill a gap from memory or chat. Use `NEEDS_EVIDENCE`, `BUDGET_STOP`, `ERROR_CEILING`, `NO_PROGRESS`, or `HUMAN_HAND_BACK` when that condition occurs.

## Human citation audit and deliberate fresh resume

Prepare `Audit.md` with this exact contract and one row for every answer citation occurrence:

```text
| Claim ID | Claim | Evidence root | Source excerpt | Disposition | Resolution |
|---|---|---|---|---|---|
```

The `Claim ID` and `Evidence root` must match the answer. Copy an exact carrying excerpt from that raw file. Then pause; the operator, not the generator, opens every evidence root and assigns `SUPPORT`, `PARTIAL`, or `NOT SUPPORTED`. Keep every audit row after review. A retained `PARTIAL` row uses `QUALIFIED: <exact final wording>` in `Resolution`; a removed `PARTIAL` or `NOT SUPPORTED` row uses `REMOVED: <reason>`. Never erase an adverse row to make the final answer pass.

Before pausing:

- save SHA-256 values for every processed inbox capture, every completed normalized note, and both answer files in `Harness/RESUME_RECEIPT.md` as the `Before` values;
- update `RUN_STATE.md` to `HAND_BACK` / `HUMAN_HAND_BACK`, with the human audit as the only next permitted action;
- append the hand-back action and remaining budget to the trace;
- intentionally end or archive this build goal/chat.

After the operator completes the audit, start a fresh goal/chat and invoke `$director-loop` again. Read `RUN_STATE.md` first. Before resumed output work, verify preserved artifacts and populate each answer's `Fresh-open SHA-256`; it must match `Saved-at-pause`. Do not redo the inbox inventory, move sources again, or recreate normalized notes. After applying only audit-driven qualifications/removals, populate `Final SHA-256`. A changed final answer is allowed only when `Authorized audit finding` names the stable ID of its `PARTIAL` or `NOT SUPPORTED` row. Record `Resume result: PASS`, the new run ID, zero reprocessed sources, zero recreated notes, and the resume result in the trace.

## Publish from audited evidence

Qualify or remove claims with `PARTIAL` or `NOT SUPPORTED`; do not manufacture a repair. Write `Morning_Brief.md` using only direct evidence roots with `SUPPORT` rows. Include exactly:

```text
Provenance: vault only; audited sources only
```

Apart from headings and the provenance line, keep brief content in claim bullets. Every claim bullet keeps the supported `[Q#-##]` ID, exact final answer wording, and direct raw wikilink. Carry unresolved evidence gaps forward as supported claim bullets or in the handoff; do not reuse a supported ID for a different claim or evidence root.

## One evaluation boundary, one repair ceiling

Set `RUN_STATE.md` to `Phase: AWAITING_CANDIDATE_CHECK`, `Status: HAND_BACK`, and `Terminal reason: HUMAN_HAND_BACK`. Keep the resumed Run ID, point to both answers, `Audit.md`, `Morning_Brief.md`, and `Harness/RESUME_RECEIPT.md`, and make running the trusted candidate check the only next permitted action. Then set the trusted course checker path in PowerShell. Adjust only `$courseRoot` if your course repository is elsewhere:

```powershell
$courseRoot = "$env:USERPROFILE\Documents\HarnessBootcamp\AI_Harness_Bootcamp"
$vault = "$env:USERPROFILE\Documents\p4-vault"
$courseVerifier = "$courseRoot\mission_flesh\p4\vault_seed\tools\verify_vault.py"
py -3 $courseVerifier $vault --candidate | Tee-Object -FilePath "$vault\Harness\CANDIDATE_CHECK_FIRST.txt"
```

Never overwrite `Harness/CANDIDATE_CHECK_FIRST.txt`, and do not repair yet when it says `HOLD`. Freeze candidate inputs between the checker and evaluator: do not update state, trace, answers, audit, brief, notes, or evidence; only save the excluded receipt files. Spawn exactly one fresh evaluator from `.codex/agents/director_evaluator.toml` against that same fingerprinted snapshot regardless of the candidate verdict. It must copy both the full candidate fingerprint and stable content fingerprint. Save its exact JSON—without rewriting or summarizing it—to `Harness/DIRECTOR_EVALUATOR_FIRST.json`, then compute its SHA-256.

Merge the first candidate finding, if any, with every evaluator blocker. Append them under `First-pass HOLD findings (append-only)` in `RUN_TRACE.md`. If either first receipt is on HOLD, approve and make one smallest combined repair. Then:

- rerun the trusted candidate checker without overwriting the first receipt:

```powershell
py -3 $courseVerifier $vault --candidate | Tee-Object -FilePath "$vault\Harness\CANDIDATE_CHECK_FINAL.txt"
```

- without editing candidate inputs after the final check, spawn a new fresh read-only evaluator from the same TOML against that final candidate snapshot;
- save its exact JSON to `Harness/DIRECTOR_EVALUATOR_FINAL.json` and compute its SHA-256.

That is the only repair cycle. Do not take one repair for the checker and another for the evaluator. The first evaluator receipt must copy both first candidate fingerprints; after repair, both final receipts must share the new pair, and the full candidate fingerprint must differ from the first. If either final result remains on `HOLD`, hand back. If both first results pass, record zero repairs, do not create either final receipt, and use each first receipt as final. Full release recomputes the stable content fingerprint, so changing mission content after evaluation cannot pass.

In `Harness/EVAL.md`, use `Repair scope: CONTENT` when stable mission content changed. Use `CONTROL_ONLY` only when the stable-content fingerprint correctly stays unchanged and every first blocker concerns retrieval control, resume, state, or trace. `Repair justification` must preserve every exact first blocker. Never make a cosmetic content edit just to change a hash. A zero-repair run records `NONE` for both fields.

Each candidate receipt also records the `RUN_STATE.md` Run ID and Goal identity plus the exact byte length and SHA-256 of `RUN_TRACE.md`. Never rewrite the first evaluated trace prefix. During the one repair, append its finding and action before running the final candidate check; that final receipt binds the longer prefix.

The optional repaired candidate receipt path is exactly `Harness/CANDIDATE_CHECK_FINAL.txt`.

Complete `Harness/EVAL.md`. Its row verdicts and opened-evidence lists must exactly match the bound receipt JSON. Preserve generator first-pass claims, first-pass evaluator verdicts, and final verdicts separately. Overclaim is:

```text
first-pass evaluator HOLD rows whose generator claim was READY / all rows whose generator claim was READY
```

## Scoped handoff and baseline

After the final evaluator passes, complete `Harness/EVAL.md`, finalize `RUN_STATE.md`, and complete `Harness/HANDOFF_RECEIPT.md` with only the terminal reason, accepted artifacts, chosen pattern, intervention and repair counts, evaluator result, candidate-verifier result, residual risk, reflection, bounded workplace trial, and resume result. Keep `Manifest status: PENDING`; do not edit this receipt after the manifest is written.

Append exactly this final block to `Harness/RUN_TRACE.md`; do not edit the bound prefix or append anything else:

```text
## Closeout after evaluation

- Final trusted candidate check: PASS.
- Final fresh read-only evaluator: PASS.
- Scoped handoff completed with accepted artifacts and residual risk.

Terminal reason: SUCCESS
```

Run the untouched course verifier and write the in-vault baseline only after the handoff is complete:

```powershell
py -3 $courseVerifier $vault --write-manifest
```

Copy that exact manifest outside the candidate vault for P5, then check the external copy:

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

Do not edit either receipt or the vault after this passes. Report only saved paths, observable actions, evidence, budgets, interventions, verdicts, and the terminal reason—never hidden reasoning or chain-of-thought.
