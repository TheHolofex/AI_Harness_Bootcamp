#!/usr/bin/env python3
"""Mutation tests for the P4 Director Loop vault verifier."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List


P4_ROOT = Path(__file__).resolve().parents[1]
SEED = P4_ROOT / "vault_seed"
VERIFIER_PATH = SEED / "tools" / "verify_vault.py"

SPEC = importlib.util.spec_from_file_location("p4_verify_vault", VERIFIER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Could not load the P4 vault verifier")
VERIFIER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFIER)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluator_receipt(
    hold_brief: bool,
    candidate_fingerprint: str,
    content_fingerprint: str,
) -> Dict[str, Any]:
    evidence: Dict[str, List[str]] = {
        "Required artifacts exist": ["Answers/Q1 Risks.md", "Answers/Q2 Blocked Decision.md", "Audit.md", "Morning_Brief.md"],
        "Personal rules visibly affect the output": ["AGENTS.md", "Morning_Brief.md"],
        "Answer claims cite direct manifested evidence": ["Harness/SOURCE_MANIFEST.json", "Answers/Q1 Risks.md", "Answers/Q2 Blocked Decision.md"],
        "Audit excerpts and dispositions are grounded": ["Audit.md", "Source_Packet/EXP-214_eu-export-qa.md", "Source_Packet/INC-481_billing-burn.md"],
        "Retrieval is earned and inside its budget": ["Harness/RUN_TRACE.md", "00_Inbox/processed/INBOX_slack_export.md", "Source_Packet/EXP-214_eu-export-qa.md"],
        "Normalized notes retain lineage and graph reachability": ["MOC.md", "Systems.md", "Decisions.md", "EU Export.md", "Blocked Decision.md"],
        "Morning Brief uses audited support only": ["Morning_Brief.md", "Audit.md"],
        "Resume, state, and trace agree": ["Harness/RESUME_RECEIPT.md", "Harness/RUN_STATE.md", "Harness/RUN_TRACE.md"],
    }
    hold_criterion = "Personal rules visibly affect the output"
    hold_finding = "The first brief's action heading did not reflect the personalized output priority."
    criteria = []
    for criterion in VERIFIER.EVALUATOR_CRITERIA:
        on_hold = hold_brief and criterion == hold_criterion
        criteria.append(
            {
                "criterion": criterion,
                "verdict": "HOLD" if on_hold else "PASS",
                "evidence_opened": evidence[criterion],
                "finding": hold_finding if on_hold else "NONE",
            }
        )
    findings = (
        [{"criterion": hold_criterion, "severity": "blocker", "summary": hold_finding}]
        if hold_brief
        else []
    )
    return {
        "role": "director_evaluator",
        "review": "REVIEW: HOLD" if hold_brief else "REVIEW: PASS",
        "candidate_fingerprint": candidate_fingerprint,
        "content_fingerprint": content_fingerprint,
        "criteria": criteria,
        "findings": findings,
    }


def write_candidate_state(root: Path) -> None:
    write(
        root / "Harness" / "RUN_STATE.md",
        """
# Run State

- Run ID: p4-course-001-resume
- Goal: produce two cited answers and a decision-ready Morning Brief from the manifested vault evidence
- Phase: AWAITING_CANDIDATE_CHECK
- Status: HAND_BACK
- Completed: fixed inbox inventory; approved organization; earned retrieval; human audit; fresh resume; brief
- Open: trusted candidate check and fresh evaluator
- Next permitted action: run the untouched course verifier in candidate mode
- Terminal reason: HUMAN_HAND_BACK
- Artifact pointers: Answers/Q1 Risks.md; Answers/Q2 Blocked Decision.md; Audit.md; Morning_Brief.md; Harness/RESUME_RECEIPT.md
""",
    )


def complete_vault(parent: Path) -> Path:
    root = parent / "p4-vault"
    shutil.copytree(SEED, root)
    processed = root / "00_Inbox" / "processed"
    processed.mkdir()
    for capture in sorted((root / "00_Inbox").glob("INBOX_*.md")):
        shutil.move(str(capture), str(processed / capture.name))

    write(
        root / "AGENTS.md",
        """
# Director Loop project instructions

- Audience: operations director preparing the Thursday steering meeting
- Decision horizon: this week, with the next required decision named explicitly
- Output priority: lead with blockers, then evidence-backed risks, then evidence gaps
- Evidence rule: every decision-driving claim cites an immutable manifested evidence root
- Escalate when: a decision lacks an owner or the evidence does not settle the choice
- Never do: invent an owner, silently upgrade a rumor, or write outside this vault
""",
    )
    write(
        root / "Harness" / "HARNESS_CARD.md",
        """
# Harness Card

## Goal and personal fit
- Recurring goal: prepare a director brief that separates supported risks from evidence gaps
- Decision owner: operations director
- Useful output: a short cited brief that supports the Thursday steering decision
- Non-goal: resolve decisions the vault cannot support

## Control flow
- Fixed outer flow: scope -> fixed inbox inventory -> organize with approval -> retrieve -> human audit and hand-back -> fresh resume -> evaluate -> finish
- Bounded adaptive retrieval loop: open at most six Source Packet records; each open must follow a raw link earned by the previous observation

## Budgets
- Maximum model turns: 12
- Wall-clock limit: 45 minutes
- Retry ceiling: 1 per correctable operation
- No-progress limit: 2 repeated observations

## Terminal reasons
- SUCCESS: required artifacts pass and the human audit is complete
- NEEDS_EVIDENCE: a decision-driving claim cannot be supported from the vault
- BUDGET_STOP: the turn or time limit is reached
- ERROR_CEILING: a correctable operation still fails after one retry
- NO_PROGRESS: two observations repeat without changing the state
- HUMAN_HAND_BACK: the next action requires operator judgment or approval

## Human approval
- Organization approval occurs before writes; citation audit occurs in a separate human pause.

## Complexity rejected
- Router — rejected: this run has one task class
- Parallel worker team — rejected: this evidence surface does not repay coordination cost
- Plugin — rejected: this personal workflow is still changing and needs no distribution
- New MCP server — rejected: the vault files already provide the bounded source surface
- Reflection without an oracle — rejected: revision is allowed only from verifier, audit, or evaluator evidence

## Component register
| Component | Job | Load timing | Cost | Disable path |
|---|---|---|---|---|
| AGENTS.md | Stable personal rules | Every project turn | Context tokens | Rename after saving a copy |
| director-loop skill | Integrated recurring procedure | Matching director-brief work | Procedure context | Do not invoke or remove the folder |
| SOURCE_MANIFEST.json | Immutable evidence registry | Before evidence use | Hash checks | Replace only with operator-approved evidence |
| RUN_STATE.md | Cross-session state | Start and end of stages | One small read and write | Archive after closeout |
| RUN_TRACE.md | Observable trajectory | After each material action | Short append | Stop after terminal state |
| RESUME_RECEIPT.md | Continuity check | Fresh resume | Hash reads | Skip only if the run hands back permanently |
| director_evaluator | Independent quality oracle | After candidate artifacts | One read-only context | Hand back if unavailable |
| verify_vault.py | Mechanical release check | Candidate, finish, baseline | Local Python run | Do not run |
""",
    )

    write(
        root / "EU Export.md",
        """
# EU Export
Raw sources: [[Source_Packet/EXP-214_eu-export-qa]]; [[Source_Packet/REL-033_export-hotfix]]

EU export QA failed and release requires a clean regression run.
""",
    )
    write(
        root / "Billing API.md",
        """
# Billing API
Raw sources: [[Source_Packet/INC-481_billing-burn]]; [[Source_Packet/MET-481_billing-window]]

The billing API crossed its error threshold before returning below one percent.
""",
    )
    write(
        root / "SSO Stability.md",
        """
# SSO Stability
Raw sources: [[00_Inbox/processed/INBOX_oncall_paste]]

The SSO report remains explicitly unreproduced.
""",
    )
    write(
        root / "Blocked Decision.md",
        """
# Blocked Decision
Raw sources: [[Source_Packet/DEC-019_ship-order]]; [[Source_Packet/OWN-005_decision-owner]]

The change order lacks both a final decision owner and deciding evidence.
""",
    )
    write(root / "Systems.md", "# Systems\n\n- [[EU Export]]\n- [[Billing API]]\n- [[SSO Stability]]")
    write(root / "Decisions.md", "# Decisions\n\n- [[Blocked Decision]]")

    write(
        root / "Answers" / "Q1 Risks.md",
        """
# Q1 Risks

- [Q1-01] EU export quality is a live release risk: 7 of 20 test exports had empty customer-name columns. [[Source_Packet/EXP-214_eu-export-qa]]
- [Q1-02] Billing reliability breached its error threshold for 18 consecutive minutes. [[Source_Packet/INC-481_billing-burn]]
""",
    )
    write(
        root / "Answers" / "Q2 Blocked Decision.md",
        """
# Q2 Blocked Decision

- [Q2-01] The ship-order decision is blocked until one owner accepts it and records the deciding evidence. [[Source_Packet/DEC-019_ship-order]]
- [Q2-02] Finance engineering owns the export fix, but no owner is recorded for the SSO change or final sequence. [[Source_Packet/OWN-005_decision-owner]]
""",
    )
    write(
        root / "Audit.md",
        """
# Audit

| Claim ID | Claim | Evidence root | Source excerpt | Disposition | Resolution |
|---|---|---|---|---|---|
| Q1-01 | EU export quality is a live release risk: 7 of 20 test exports had empty customer-name columns. | [[Source_Packet/EXP-214_eu-export-qa]] | The 2026-07-31 QA run produced empty customer-name columns in 7 of 20 EU CSV exports; the US control run passed 20 of 20. | SUPPORT | No change |
| Q1-02 | Billing reliability breached its error threshold for 18 consecutive minutes. | [[Source_Packet/INC-481_billing-burn]] | Billing API five-hundred errors remained above the alert threshold for 18 consecutive minutes during the current on-call window. | SUPPORT | No change |
| Q2-01 | The ship-order decision is blocked until one owner accepts it and records the deciding evidence. | [[Source_Packet/DEC-019_ship-order]] | The ship-order decision remains blocked until one owner accepts the sequencing decision and records the evidence used to prioritize either change. | SUPPORT | No change |
| Q2-02 | Finance engineering owns the export fix, but no owner is recorded for the SSO change or final sequence. | [[Source_Packet/OWN-005_decision-owner]] | Finance engineering owns the EU export hotfix; no owner is recorded for the SSO idle-session change or for the final ship-order decision. | SUPPORT | No change |
""",
    )
    write(
        root / "Morning_Brief.md",
        """
# Morning Brief

Provenance: vault only; audited sources only

## Act on
- [Q1-01] EU export quality is a live release risk: 7 of 20 test exports had empty customer-name columns. [[Source_Packet/EXP-214_eu-export-qa]]
- [Q1-02] Billing reliability breached its error threshold for 18 consecutive minutes. [[Source_Packet/INC-481_billing-burn]]

## Hand back
- [Q2-01] The ship-order decision is blocked until one owner accepts it and records the deciding evidence. [[Source_Packet/DEC-019_ship-order]]
- [Q2-02] Finance engineering owns the export fix, but no owner is recorded for the SSO change or final sequence. [[Source_Packet/OWN-005_decision-owner]]
""",
    )
    write(
        root / "Harness" / "RUN_TRACE.md",
        """
# Run Trace

Record observable actions and results, not hidden reasoning or chain-of-thought.

| Step | Observable action | Observation or evidence | Budget after step | Outcome |
|---|---|---|---|---|
| 1 | Inventoried the fixed inbox batch | Four captures present and hash-matched | 11 turns; 42 minutes | CONTINUE |
| 2 | Organized approved notes | MOC reaches each normalized note through a hub | 9 turns; 35 minutes | CONTINUE |
| 3 | Ended the build goal for human audit | RUN_STATE saved next action and pre-resume hashes | 8 turns; 30 minutes | HAND_BACK |
| 4 | Resumed as p4-course-001-resume | Resume result: PASS; no sources reprocessed and no normalized notes recreated | 7 turns; 24 minutes | CONTINUE |

## Fixed inbox inventory

| Fixed inbox capture | Observable result |
|---|---|
| [[00_Inbox/processed/INBOX_decision_needed]] | Recorded blocked ship-order question and starting decision record |
| [[00_Inbox/processed/INBOX_director_ask]] | Recorded the director's export, SSO, and cyber questions |
| [[00_Inbox/processed/INBOX_oncall_paste]] | Preserved billing burn, unreproduced SSO rumor, and training-only status |
| [[00_Inbox/processed/INBOX_slack_export]] | Recorded EU defect, US control, and starting export records |

## Retrieval ledger

| Open | Evidence root | Reference discovered in | Observable result |
|---|---|---|---|
| 1 | [[Source_Packet/EXP-214_eu-export-qa]] | [[00_Inbox/processed/INBOX_slack_export]] | Found measured EU failure and next release record |
| 2 | [[Source_Packet/REL-033_export-hotfix]] | [[Source_Packet/EXP-214_eu-export-qa]] | Found clean-regression release gate; stopped export branch |
| 3 | [[Source_Packet/INC-481_billing-burn]] | [[00_Inbox/processed/INBOX_oncall_paste]] | Found active threshold breach and next metric record |
| 4 | [[Source_Packet/MET-481_billing-window]] | [[Source_Packet/INC-481_billing-burn]] | Found peak and recovery time; stopped billing branch |
| 5 | [[Source_Packet/DEC-019_ship-order]] | [[00_Inbox/processed/INBOX_decision_needed]] | Found blocked decision and next ownership record |
| 6 | [[Source_Packet/OWN-005_decision-owner]] | [[Source_Packet/DEC-019_ship-order]] | Found missing SSO and sequence owners; budget reached |

## First-pass HOLD findings (append-only)

- NONE before the fresh evaluator runs.

Terminal reason: HUMAN_HAND_BACK
""",
    )

    preserved_paths = sorted(
        [path.relative_to(root).as_posix() for path in processed.glob("*.md")]
        + ["Billing API.md", "Blocked Decision.md", "EU Export.md", "SSO Stability.md"]
    )
    preserved_rows = "\n".join(
        f"| {relative} | {file_hash(root / relative)} | {file_hash(root / relative)} | UNCHANGED |"
        for relative in preserved_paths
    )
    q1_hash = file_hash(root / ANSWER_PATHS_LOCAL[0])
    q2_hash = file_hash(root / ANSWER_PATHS_LOCAL[1])
    write(
        root / "Harness" / "RESUME_RECEIPT.md",
        f"""
# Resume Receipt

- Resume result: PASS
- Prior run ID: p4-course-001-build
- Resumed run ID: p4-course-001-resume
- Saved next permitted action: read completed human audit and verify continuity hashes
- First resumed action: read completed human audit and verify continuity hashes
- Reprocessed source count: 0
- Recreated normalized note count: 0

| Preserved artifact | Before SHA-256 | After SHA-256 | Result |
|---|---|---|---|
{preserved_rows}

| Answer artifact | Saved-at-pause SHA-256 | Fresh-open SHA-256 | Final SHA-256 | Authorized audit finding |
|---|---|---|---|---|
| Answers/Q1 Risks.md | {q1_hash} | {q1_hash} | {q1_hash} | NONE |
| Answers/Q2 Blocked Decision.md | {q2_hash} | {q2_hash} | {q2_hash} | NONE |
""",
    )

    write(
        root / "Harness" / "RUN_STATE.md",
        """
# Run State

- Run ID: p4-course-001-resume
- Goal: produce two cited answers and a decision-ready Morning Brief from the manifested vault evidence
- Phase: AWAITING_CANDIDATE_CHECK
- Status: HAND_BACK
- Completed: fixed inbox inventory; approved organization; earned retrieval; human audit; fresh resume; brief
- Open: trusted candidate check and fresh evaluator
- Next permitted action: run the untouched course verifier in candidate mode
- Terminal reason: HUMAN_HAND_BACK
- Artifact pointers: Answers/Q1 Risks.md; Answers/Q2 Blocked Decision.md; Audit.md; Morning_Brief.md; Harness/RESUME_RECEIPT.md
""",
    )

    first_snapshot_fingerprint = VERIFIER.candidate_fingerprint(root)
    first_content_fingerprint = VERIFIER.evaluated_content_fingerprint(root)
    first_state_identity, first_trace_bytes, first_trace_hash = VERIFIER.candidate_control_metadata(root)
    first_candidate_output = (
        "PASS P4 candidate: 4 answer citations, 4 audit rows, "
        f"6 earned retrieval opens; fingerprint {first_snapshot_fingerprint}; "
        f"content {first_content_fingerprint}; stateid {first_state_identity}; "
        f"trace {first_trace_bytes}:{first_trace_hash}"
    )
    first_candidate_path = root / "Harness" / "CANDIDATE_CHECK_FIRST.txt"
    final_candidate_path = root / "Harness" / "CANDIDATE_CHECK_FINAL.txt"
    write(first_candidate_path, first_candidate_output)

    first_receipt_path = root / "Harness" / "DIRECTOR_EVALUATOR_FIRST.json"
    final_receipt_path = root / "Harness" / "DIRECTOR_EVALUATOR_FINAL.json"
    first_receipt = evaluator_receipt(
        hold_brief=True,
        candidate_fingerprint=first_snapshot_fingerprint,
        content_fingerprint=first_content_fingerprint,
    )
    write_json(first_receipt_path, first_receipt)

    brief = root / "Morning_Brief.md"
    brief.write_text(
        brief.read_text(encoding="utf-8").replace("## Act on", "## Act now"),
        encoding="utf-8",
    )
    trace = root / "Harness" / "RUN_TRACE.md"
    trace.write_text(
        trace.read_text(encoding="utf-8")
        + """

## First-pass evaluation and one repair

- Candidate check: PASS.
- Personal rules visibly affect the output — The first brief's action heading did not reflect the personalized output priority.
- One combined repair changed the action heading to match the saved output priority.

Terminal reason: HUMAN_HAND_BACK
""",
        encoding="utf-8",
    )
    final_snapshot_fingerprint = VERIFIER.candidate_fingerprint(root)
    final_content_fingerprint = VERIFIER.evaluated_content_fingerprint(root)
    final_state_identity, final_trace_bytes, final_trace_hash = VERIFIER.candidate_control_metadata(root)
    final_candidate_output = (
        "PASS P4 candidate: 4 answer citations, 4 audit rows, "
        f"6 earned retrieval opens; fingerprint {final_snapshot_fingerprint}; "
        f"content {final_content_fingerprint}; stateid {final_state_identity}; "
        f"trace {final_trace_bytes}:{final_trace_hash}"
    )
    write(final_candidate_path, final_candidate_output)
    final_receipt = evaluator_receipt(
        hold_brief=False,
        candidate_fingerprint=final_snapshot_fingerprint,
        content_fingerprint=final_content_fingerprint,
    )
    write_json(final_receipt_path, final_receipt)
    trace.write_text(
        trace.read_text(encoding="utf-8")
        + """

## Closeout after evaluation

- Final trusted candidate check: PASS.
- Final fresh read-only evaluator: PASS.
- Scoped handoff completed with accepted artifacts and residual risk.

Terminal reason: SUCCESS
""",
        encoding="utf-8",
    )
    eval_rows = "\n".join(
        "| {criterion} | READY | {evidence} | {first} | PASS |".format(
            criterion=row["criterion"],
            evidence="; ".join(row["evidence_opened"]),
            first=row["verdict"],
        )
        for row in first_receipt["criteria"]
    )
    write(
        root / "Harness" / "EVAL.md",
        f"""
# Evaluator Record

- Evaluator context: FRESH
- Access: READ_ONLY
- Default: FAIL
- Generator first-pass verdict: READY
- Candidate verifier first-pass verdict: PASS
- Candidate verifier first-pass finding: NONE
- Fresh evaluator first-pass verdict: HOLD
- First-pass criteria claimed ready: 8
- First-pass evaluator HOLD criteria: 1
- First-pass overclaim criteria: 1
- Overclaim: 1/8
- Repair cycles used: 1
- Repair scope: CONTENT
- Repair justification: The first brief's action heading did not reflect the personalized output priority.
- Final candidate verifier verdict: PASS
- Final evaluator verdict: PASS
- Verdict: PASS
- First candidate receipt: Harness/CANDIDATE_CHECK_FIRST.txt
- First candidate SHA-256: {file_hash(first_candidate_path)}
- Final candidate receipt: Harness/CANDIDATE_CHECK_FINAL.txt
- Final candidate SHA-256: {file_hash(final_candidate_path)}
- First evaluator receipt: Harness/DIRECTOR_EVALUATOR_FIRST.json
- First evaluator SHA-256: {file_hash(first_receipt_path)}
- Final evaluator receipt: Harness/DIRECTOR_EVALUATOR_FINAL.json
- Final evaluator SHA-256: {file_hash(final_receipt_path)}

| Criterion | Generator first-pass claim | Evidence opened | Fresh evaluator first-pass verdict | Final verdict |
|---|---|---|---|---|
{eval_rows}
""",
    )

    accepted = "; ".join(
        list(VERIFIER.OUTPUT_PATHS)
        + ["Harness/CANDIDATE_CHECK_FINAL.txt", "Harness/DIRECTOR_EVALUATOR_FINAL.json"]
    )
    write(
        root / "Harness" / "RUN_STATE.md",
        f"""
# Run State

- Run ID: p4-course-001-resume
- Goal: produce two cited answers and a decision-ready Morning Brief from the manifested vault evidence
- Phase: TERMINAL
- Status: COMPLETE
- Completed: fixed inbox inventory; approved organization; earned retrieval; human audit; fresh resume; evaluator; verifier; handoff
- Open: owner and deciding evidence still need to be supplied for the ship-order decision
- Next permitted action: NONE — hand the residual evidence gap to the operations director
- Terminal reason: SUCCESS
- Artifact pointers: {accepted}
""",
    )
    write(
        root / "Harness" / "HANDOFF_RECEIPT.md",
        f"""
# Handoff Receipt

- Handoff status: COMPLETE
- Terminal reason: SUCCESS
- Accepted artifacts: {accepted}
- Chosen pattern: fixed outer flow with bounded adaptive retrieval because one recurring decision brief needs evidence-driven next opens, not routing overhead
- Human intervention count: 2
- Repair cycles used: 1
- Evaluator result: PASS
- Candidate verifier result: PASS
- Residual risk: the ship-order decision still lacks one accountable owner and recorded deciding evidence
- Reflection: keep the source manifest and six-open ledger because they made provenance and stopping observable
- Workplace trial: use the harness for next week's operations steering brief
- Trial owner: operations director
- Trial date: next Thursday steering window
- Trial success signal: a decision-ready brief in under 45 minutes with zero unsupported decision claims
- Resume result: PASS
- Manifest status: PENDING
""",
    )
    return root


ANSWER_PATHS_LOCAL = (Path("Answers/Q1 Risks.md"), Path("Answers/Q2 Blocked Decision.md"))


class VerifyVaultTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = complete_vault(Path(self.tempdir.name))

    def test_complete_vault_passes_and_writes_deterministic_manifest(self) -> None:
        result = VERIFIER.verify_vault(self.root)
        self.assertEqual(result["terminal_reason"], "SUCCESS")
        self.assertEqual(result["answer_citations"], 4)
        self.assertEqual(result["retrieval_opens"], 6)

        manifest_path = VERIFIER.write_manifest(self.root, result)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        paths = [item["path"] for item in manifest["files"]]
        self.assertEqual(paths, sorted(paths))
        self.assertIn("Harness/HANDOFF_RECEIPT.md", paths)
        self.assertNotIn("Harness/BASELINE_MANIFEST.json", paths)
        first = manifest_path.read_bytes()
        VERIFIER.write_manifest(self.root, VERIFIER.verify_vault(self.root))
        self.assertEqual(manifest_path.read_bytes(), first)
        self.assertEqual(VERIFIER.check_manifest(self.root)["files"], len(paths))

    def test_unresolved_personalization_placeholder_holds(self) -> None:
        agents = self.root / "AGENTS.md"
        agents.write_text(
            agents.read_text(encoding="utf-8").replace(
                "operations director preparing the Thursday steering meeting",
                "[REPLACE: your real audience]",
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(VERIFIER.VerificationError, "Unresolved.*AGENTS.md"):
            VERIFIER.verify_vault(self.root)

    def test_skill_keeps_required_questions_inside_copied_vault(self) -> None:
        skill = self.root / ".agents" / "skills" / "director-loop" / "SKILL.md"
        skill.write_text(
            skill.read_text(encoding="utf-8").replace(
                VERIFIER.REQUIRED_QUESTIONS[0], "A question that is no longer the course question"
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(VERIFIER.VerificationError, "Copied contract differs"):
            VERIFIER.verify_vault(self.root)

    def test_answer_must_cite_direct_evidence_not_generated_note(self) -> None:
        answer = self.root / "Answers" / "Q1 Risks.md"
        answer.write_text(
            answer.read_text(encoding="utf-8").replace(
                "[[Source_Packet/EXP-214_eu-export-qa]]", "[[EU Export]]"
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(VERIFIER.VerificationError, "evidence roots directly"):
            VERIFIER.verify_vault(self.root)

    def test_raw_evidence_hash_change_holds(self) -> None:
        raw = self.root / "Source_Packet" / "EXP-214_eu-export-qa.md"
        raw.write_text(raw.read_text(encoding="utf-8") + "tampered\n", encoding="utf-8")
        with self.assertRaisesRegex(VERIFIER.VerificationError, "Evidence-root hash mismatch"):
            VERIFIER.verify_vault(self.root)

    def test_audit_excerpt_must_be_exact_raw_substring(self) -> None:
        audit = self.root / "Audit.md"
        audit.write_text(
            audit.read_text(encoding="utf-8").replace("7 of 20 EU", "8 of 20 EU", 1),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(VERIFIER.VerificationError, "exact substring"):
            VERIFIER.verify_vault(self.root)

    def test_removed_not_supported_claim_remains_in_audit(self) -> None:
        write_candidate_state(self.root)
        audit = self.root / "Audit.md"
        audit.write_text(
            audit.read_text(encoding="utf-8")
            + "| Q1-03 | Export fix is already released. | [[Source_Packet/REL-033_export-hotfix]] | The export hotfix can enter the Thursday 02:00 UTC change window only after a clean 20-file EU regression run. | NOT SUPPORTED | REMOVED: the source says candidate, not released |\n",
            encoding="utf-8",
        )
        result = VERIFIER.verify_candidate(self.root)
        self.assertEqual(result["answer_citations"], 4)
        self.assertEqual(result["audit_rows"], 5)

    def test_brief_cannot_reuse_supported_id_for_new_wording(self) -> None:
        brief = self.root / "Morning_Brief.md"
        brief.write_text(
            brief.read_text(encoding="utf-8").replace(
                "EU export quality is a live release risk",
                "EU export quality is a catastrophic release risk",
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(VERIFIER.VerificationError, "SUPPORT wording\+root"):
            VERIFIER.verify_vault(self.root)

    def test_each_answer_must_materially_use_packet_retrieval(self) -> None:
        answer = self.root / "Answers" / "Q1 Risks.md"
        answer.write_text(
            answer.read_text(encoding="utf-8")
            .replace(
                "[[Source_Packet/EXP-214_eu-export-qa]]",
                "[[00_Inbox/processed/INBOX_slack_export]]",
            )
            .replace(
                "[[Source_Packet/INC-481_billing-burn]]",
                "[[00_Inbox/processed/INBOX_oncall_paste]]",
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(VERIFIER.VerificationError, "at least two earned Source_Packet"):
            VERIFIER.verify_candidate(self.root)

    def test_manifest_binds_exact_evidence_path_not_just_filename(self) -> None:
        original = self.root / "Source_Packet" / "AUTH-007_sso-observation.md"
        moved = self.root / "00_Inbox" / "processed" / original.name
        shutil.move(str(original), str(moved))
        with self.assertRaisesRegex(VERIFIER.VerificationError, "missing exact path"):
            VERIFIER.verify_candidate(self.root)

    def test_generated_note_requires_raw_sources_lineage(self) -> None:
        note = self.root / "EU Export.md"
        note.write_text(
            note.read_text(encoding="utf-8").replace("Raw sources:", "Navigation links:"),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(VERIFIER.VerificationError, "raw-capture lineage"):
            VERIFIER.verify_vault(self.root)

    def test_generated_note_must_be_reachable_from_a_hub(self) -> None:
        hub = self.root / "Systems.md"
        hub.write_text(hub.read_text(encoding="utf-8").replace("- [[EU Export]]\n", ""), encoding="utf-8")
        with self.assertRaisesRegex(VERIFIER.VerificationError, "not reachable"):
            VERIFIER.verify_vault(self.root)

    def test_unearned_retrieval_open_holds(self) -> None:
        write_candidate_state(self.root)
        trace = self.root / "Harness" / "RUN_TRACE.md"
        trace.write_text(
            trace.read_text(encoding="utf-8").replace(
                "[[Source_Packet/EXP-214_eu-export-qa]] | Found clean-regression",
                "[[Source_Packet/INC-481_billing-burn]] | Found clean-regression",
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(VERIFIER.VerificationError, "Unearned retrieval"):
            VERIFIER.verify_vault(self.root)

    def test_seventh_adaptive_open_holds(self) -> None:
        write_candidate_state(self.root)
        trace = self.root / "Harness" / "RUN_TRACE.md"
        text = trace.read_text(encoding="utf-8")
        marker = "\n\n## First-pass HOLD findings"
        extra = (
            "\n| 7 | [[Source_Packet/INC-482_sso-rumor]] | "
            "[[00_Inbox/processed/INBOX_oncall_paste]] | Extra open |\n"
        )
        trace.write_text(text.replace(marker, extra + "\n## First-pass HOLD findings"), encoding="utf-8")
        with self.assertRaisesRegex(VERIFIER.VerificationError, "1 to 6 opens"):
            VERIFIER.verify_vault(self.root)

    def test_evaluator_receipt_hash_is_bound(self) -> None:
        receipt = self.root / "Harness" / "DIRECTOR_EVALUATOR_FIRST.json"
        receipt.write_text(receipt.read_text(encoding="utf-8") + " ", encoding="utf-8")
        with self.assertRaisesRegex(VERIFIER.VerificationError, "receipt SHA-256"):
            VERIFIER.verify_vault(self.root)

    def test_evaluator_receipt_must_share_candidate_fingerprint(self) -> None:
        receipt = self.root / "Harness" / "DIRECTOR_EVALUATOR_FIRST.json"
        old_hash = file_hash(receipt)
        payload = json.loads(receipt.read_text(encoding="utf-8"))
        payload["candidate_fingerprint"] = "0" * 64
        write_json(receipt, payload)
        evaluation = self.root / "Harness" / "EVAL.md"
        evaluation.write_text(
            evaluation.read_text(encoding="utf-8").replace(old_hash, file_hash(receipt)),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(VERIFIER.VerificationError, "not bound to the candidate"):
            VERIFIER.verify_vault(self.root)

    def test_evaluator_evidence_opened_must_be_safe_existing_paths(self) -> None:
        receipt = self.root / "Harness" / "DIRECTOR_EVALUATOR_FIRST.json"
        old_hash = file_hash(receipt)
        payload = json.loads(receipt.read_text(encoding="utf-8"))
        payload["criteria"][0]["evidence_opened"] = ["../outside-vault.md"]
        write_json(receipt, payload)
        evaluation = self.root / "Harness" / "EVAL.md"
        evaluation.write_text(
            evaluation.read_text(encoding="utf-8").replace(old_hash, file_hash(receipt)),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(VERIFIER.VerificationError, "unsafe evidence path"):
            VERIFIER.verify_vault(self.root)

    def test_evaluator_rejects_duplicate_blocker_for_one_criterion(self) -> None:
        receipt = self.root / "Harness" / "DIRECTOR_EVALUATOR_FIRST.json"
        old_hash = file_hash(receipt)
        payload = json.loads(receipt.read_text(encoding="utf-8"))
        payload["findings"].append(dict(payload["findings"][0]))
        write_json(receipt, payload)
        evaluation = self.root / "Harness" / "EVAL.md"
        evaluation.write_text(
            evaluation.read_text(encoding="utf-8").replace(old_hash, file_hash(receipt)),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(VERIFIER.VerificationError, "duplicate blocker"):
            VERIFIER.verify_vault(self.root)

    def test_release_rejects_content_changed_after_final_evaluation(self) -> None:
        brief = self.root / "Morning_Brief.md"
        brief.write_text(
            brief.read_text(encoding="utf-8").replace("## Act now", "## Ignore these items"),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(VERIFIER.VerificationError, "evaluator-approved content changed"):
            VERIFIER.verify_vault(self.root)

    def test_release_rejects_first_trace_rewritten_during_repair(self) -> None:
        final_candidate = self.root / "Harness" / "CANDIDATE_CHECK_FINAL.txt"
        final_evaluator = self.root / "Harness" / "DIRECTOR_EVALUATOR_FINAL.json"
        trace = self.root / "Harness" / "RUN_TRACE.md"
        evaluation = self.root / "Harness" / "EVAL.md"

        first_metadata = VERIFIER.load_candidate_receipt(
            self.root, "Harness/CANDIDATE_CHECK_FIRST.txt"
        )
        final_metadata = VERIFIER.load_candidate_receipt(
            self.root, "Harness/CANDIDATE_CHECK_FINAL.txt"
        )
        first_trace_bytes = first_metadata[5]
        final_trace_bytes = final_metadata[5]
        original_trace = trace.read_bytes()
        self.assertEqual(
            hashlib.sha256(original_trace[:first_trace_bytes]).hexdigest(), first_metadata[6]
        )

        rewritten_prefix = original_trace[:final_trace_bytes].replace(
            b"Four captures present", b"Four captures altered", 1
        )
        self.assertNotEqual(rewritten_prefix, original_trace[:final_trace_bytes])
        trace.write_bytes(rewritten_prefix)
        new_candidate_fingerprint = VERIFIER.candidate_fingerprint(self.root)
        new_state_identity, new_trace_bytes, new_trace_hash = VERIFIER.candidate_control_metadata(
            self.root
        )

        old_candidate_hash = file_hash(final_candidate)
        status = final_candidate.read_text(encoding="utf-8").split("; fingerprint ", 1)[0]
        final_candidate.write_text(
            f"{status}; fingerprint {new_candidate_fingerprint}; "
            f"content {final_metadata[3]}; stateid {new_state_identity}; "
            f"trace {new_trace_bytes}:{new_trace_hash}\n",
            encoding="utf-8",
        )

        old_evaluator_hash = file_hash(final_evaluator)
        payload = json.loads(final_evaluator.read_text(encoding="utf-8"))
        payload["candidate_fingerprint"] = new_candidate_fingerprint
        write_json(final_evaluator, payload)
        eval_text = evaluation.read_text(encoding="utf-8")
        eval_text = eval_text.replace(old_candidate_hash, file_hash(final_candidate))
        eval_text = eval_text.replace(old_evaluator_hash, file_hash(final_evaluator))
        evaluation.write_text(eval_text, encoding="utf-8")

        trace.write_bytes(rewritten_prefix + VERIFIER.TRACE_CLOSEOUT.encode("utf-8"))
        with self.assertRaisesRegex(
            VERIFIER.VerificationError, "first evaluator-approved RUN_TRACE prefix"
        ):
            VERIFIER.verify_vault(self.root)

    def test_release_rejects_state_identity_changed_during_repair(self) -> None:
        final_candidate = self.root / "Harness" / "CANDIDATE_CHECK_FINAL.txt"
        final_evaluator = self.root / "Harness" / "DIRECTOR_EVALUATOR_FINAL.json"
        state = self.root / "Harness" / "RUN_STATE.md"
        trace = self.root / "Harness" / "RUN_TRACE.md"
        evaluation = self.root / "Harness" / "EVAL.md"

        final_metadata = VERIFIER.load_candidate_receipt(
            self.root, "Harness/CANDIDATE_CHECK_FINAL.txt"
        )
        full_trace = trace.read_bytes()
        trace.write_bytes(full_trace[: final_metadata[5]])
        state.write_text(
            state.read_text(encoding="utf-8").replace(
                "produce two cited answers", "produce two polished answers", 1
            ),
            encoding="utf-8",
        )
        new_candidate_fingerprint = VERIFIER.candidate_fingerprint(self.root)
        new_state_identity, new_trace_bytes, new_trace_hash = VERIFIER.candidate_control_metadata(
            self.root
        )

        old_candidate_hash = file_hash(final_candidate)
        status = final_candidate.read_text(encoding="utf-8").split("; fingerprint ", 1)[0]
        final_candidate.write_text(
            f"{status}; fingerprint {new_candidate_fingerprint}; "
            f"content {final_metadata[3]}; stateid {new_state_identity}; "
            f"trace {new_trace_bytes}:{new_trace_hash}\n",
            encoding="utf-8",
        )
        old_evaluator_hash = file_hash(final_evaluator)
        payload = json.loads(final_evaluator.read_text(encoding="utf-8"))
        payload["candidate_fingerprint"] = new_candidate_fingerprint
        write_json(final_evaluator, payload)
        eval_text = evaluation.read_text(encoding="utf-8")
        eval_text = eval_text.replace(old_candidate_hash, file_hash(final_candidate))
        eval_text = eval_text.replace(old_evaluator_hash, file_hash(final_evaluator))
        evaluation.write_text(eval_text, encoding="utf-8")
        trace.write_bytes(full_trace)

        with self.assertRaisesRegex(
            VERIFIER.VerificationError, "RUN_STATE Run ID or Goal changed during evaluation"
        ):
            VERIFIER.verify_vault(self.root)

    def test_release_rejects_unbounded_trace_closeout(self) -> None:
        trace = self.root / "Harness" / "RUN_TRACE.md"
        trace.write_text(
            trace.read_text(encoding="utf-8").replace(
                "- Scoped handoff completed with accepted artifacts and residual risk.\n",
                "- Scoped handoff completed with accepted artifacts and residual risk.\n"
                "- Unreviewed autonomous action: approved.\n",
                1,
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(VERIFIER.VerificationError, "exact post-evaluation block"):
            VERIFIER.verify_vault(self.root)

    def test_release_accepts_semantically_exact_crlf_closeout(self) -> None:
        final_metadata = VERIFIER.load_candidate_receipt(
            self.root, "Harness/CANDIDATE_CHECK_FINAL.txt"
        )
        trace = self.root / "Harness" / "RUN_TRACE.md"
        prefix = trace.read_bytes()[: final_metadata[5]]
        crlf_closeout = VERIFIER.TRACE_CLOSEOUT.replace("\n", "\r\n").encode("utf-8")
        trace.write_bytes(prefix + crlf_closeout)
        result = VERIFIER.verify_vault(self.root)
        self.assertEqual(result["terminal_reason"], "SUCCESS")

    def test_content_blocker_cannot_release_with_unchanged_stable_content(self) -> None:
        final_candidate = self.root / "Harness" / "CANDIDATE_CHECK_FINAL.txt"
        final_evaluator = self.root / "Harness" / "DIRECTOR_EVALUATOR_FINAL.json"
        brief = self.root / "Morning_Brief.md"
        state = self.root / "Harness" / "RUN_STATE.md"
        trace = self.root / "Harness" / "RUN_TRACE.md"
        evaluation = self.root / "Harness" / "EVAL.md"

        first_metadata = VERIFIER.load_candidate_receipt(
            self.root, "Harness/CANDIDATE_CHECK_FIRST.txt"
        )
        final_metadata = VERIFIER.load_candidate_receipt(
            self.root, "Harness/CANDIDATE_CHECK_FINAL.txt"
        )
        brief.write_text(
            brief.read_text(encoding="utf-8").replace("## Act now", "## Act on", 1),
            encoding="utf-8",
        )
        final_state = state.read_text(encoding="utf-8")
        full_trace = trace.read_bytes()
        write_candidate_state(self.root)
        trace.write_bytes(full_trace[: final_metadata[5]])
        new_candidate_fingerprint = VERIFIER.candidate_fingerprint(self.root)
        new_content_fingerprint = VERIFIER.evaluated_content_fingerprint(self.root)
        self.assertEqual(new_content_fingerprint, first_metadata[3])
        new_state_identity, new_trace_bytes, new_trace_hash = VERIFIER.candidate_control_metadata(
            self.root
        )

        old_candidate_hash = file_hash(final_candidate)
        status = final_candidate.read_text(encoding="utf-8").split("; fingerprint ", 1)[0]
        final_candidate.write_text(
            f"{status}; fingerprint {new_candidate_fingerprint}; "
            f"content {new_content_fingerprint}; stateid {new_state_identity}; "
            f"trace {new_trace_bytes}:{new_trace_hash}\n",
            encoding="utf-8",
        )
        old_evaluator_hash = file_hash(final_evaluator)
        payload = json.loads(final_evaluator.read_text(encoding="utf-8"))
        payload["candidate_fingerprint"] = new_candidate_fingerprint
        payload["content_fingerprint"] = new_content_fingerprint
        write_json(final_evaluator, payload)
        eval_text = evaluation.read_text(encoding="utf-8")
        eval_text = eval_text.replace(old_candidate_hash, file_hash(final_candidate))
        eval_text = eval_text.replace(old_evaluator_hash, file_hash(final_evaluator))
        evaluation.write_text(eval_text, encoding="utf-8")
        state.write_text(final_state, encoding="utf-8")
        trace.write_bytes(full_trace)

        with self.assertRaisesRegex(
            VERIFIER.VerificationError, "unchanged stable mission content requires"
        ):
            VERIFIER.verify_vault(self.root)

    def test_explicit_control_only_repair_does_not_require_performative_content_edit(self) -> None:
        control_criterion = "Resume, state, and trace agree"
        control_finding = "The first trace omitted the trusted candidate-check action."
        final_candidate = self.root / "Harness" / "CANDIDATE_CHECK_FINAL.txt"
        first_evaluator = self.root / "Harness" / "DIRECTOR_EVALUATOR_FIRST.json"
        final_evaluator = self.root / "Harness" / "DIRECTOR_EVALUATOR_FINAL.json"
        brief = self.root / "Morning_Brief.md"
        state = self.root / "Harness" / "RUN_STATE.md"
        trace = self.root / "Harness" / "RUN_TRACE.md"
        evaluation = self.root / "Harness" / "EVAL.md"

        first_metadata = VERIFIER.load_candidate_receipt(
            self.root, "Harness/CANDIDATE_CHECK_FIRST.txt"
        )
        brief.write_text(
            brief.read_text(encoding="utf-8").replace("## Act now", "## Act on", 1),
            encoding="utf-8",
        )

        old_first_evaluator_hash = file_hash(first_evaluator)
        first_payload = json.loads(first_evaluator.read_text(encoding="utf-8"))
        for row in first_payload["criteria"]:
            if row["criterion"] == "Personal rules visibly affect the output":
                row["verdict"] = "PASS"
                row["finding"] = "NONE"
            elif row["criterion"] == control_criterion:
                row["verdict"] = "HOLD"
                row["finding"] = control_finding
        first_payload["findings"] = [
            {"criterion": control_criterion, "severity": "blocker", "summary": control_finding}
        ]
        write_json(first_evaluator, first_payload)

        trace_text = trace.read_text(encoding="utf-8")
        trace_text = trace_text.replace(
            "- Personal rules visibly affect the output — The first brief's action heading did not reflect the personalized output priority.\n"
            "- One combined repair changed the action heading to match the saved output priority.\n",
            f"- {control_criterion} — {control_finding}\n"
            "- One combined repair appended the missing candidate-check action without changing mission content.\n",
            1,
        )
        marker = "\n\n## Closeout after evaluation"
        new_prefix_text, separator, _ = trace_text.partition(marker)
        self.assertEqual(separator, marker)
        new_prefix = new_prefix_text.encode("utf-8")
        final_state = state.read_text(encoding="utf-8")
        write_candidate_state(self.root)
        trace.write_bytes(new_prefix)
        new_candidate_fingerprint = VERIFIER.candidate_fingerprint(self.root)
        new_content_fingerprint = VERIFIER.evaluated_content_fingerprint(self.root)
        self.assertEqual(new_content_fingerprint, first_metadata[3])
        new_state_identity, new_trace_bytes, new_trace_hash = VERIFIER.candidate_control_metadata(
            self.root
        )

        old_final_candidate_hash = file_hash(final_candidate)
        status = final_candidate.read_text(encoding="utf-8").split("; fingerprint ", 1)[0]
        final_candidate.write_text(
            f"{status}; fingerprint {new_candidate_fingerprint}; "
            f"content {new_content_fingerprint}; stateid {new_state_identity}; "
            f"trace {new_trace_bytes}:{new_trace_hash}\n",
            encoding="utf-8",
        )
        old_final_evaluator_hash = file_hash(final_evaluator)
        final_payload = json.loads(final_evaluator.read_text(encoding="utf-8"))
        final_payload["candidate_fingerprint"] = new_candidate_fingerprint
        final_payload["content_fingerprint"] = new_content_fingerprint
        write_json(final_evaluator, final_payload)

        eval_text = evaluation.read_text(encoding="utf-8")
        eval_text = eval_text.replace(old_first_evaluator_hash, file_hash(first_evaluator))
        eval_text = eval_text.replace(old_final_candidate_hash, file_hash(final_candidate))
        eval_text = eval_text.replace(old_final_evaluator_hash, file_hash(final_evaluator))
        eval_text = eval_text.replace("Repair scope: CONTENT", "Repair scope: CONTROL_ONLY", 1)
        eval_text = eval_text.replace(
            "Repair justification: The first brief's action heading did not reflect the personalized output priority.",
            f"Repair justification: {control_finding}",
            1,
        )
        eval_text = eval_text.replace(
            "| Personal rules visibly affect the output | READY | AGENTS.md; Morning_Brief.md | HOLD | PASS |",
            "| Personal rules visibly affect the output | READY | AGENTS.md; Morning_Brief.md | PASS | PASS |",
            1,
        )
        eval_text = eval_text.replace(
            "| Resume, state, and trace agree | READY | Harness/RESUME_RECEIPT.md; Harness/RUN_STATE.md; Harness/RUN_TRACE.md | PASS | PASS |",
            "| Resume, state, and trace agree | READY | Harness/RESUME_RECEIPT.md; Harness/RUN_STATE.md; Harness/RUN_TRACE.md | HOLD | PASS |",
            1,
        )
        evaluation.write_text(eval_text, encoding="utf-8")
        state.write_text(final_state, encoding="utf-8")
        trace.write_bytes(new_prefix + VERIFIER.TRACE_CLOSEOUT.encode("utf-8"))

        result = VERIFIER.verify_vault(self.root)
        self.assertEqual(result["evaluation"]["repair_scope"], "CONTROL_ONLY")

    def test_repair_cycle_requires_a_changed_candidate_fingerprint(self) -> None:
        first = self.root / "Harness" / "CANDIDATE_CHECK_FIRST.txt"
        final = self.root / "Harness" / "CANDIDATE_CHECK_FINAL.txt"
        first_match = re.search(
            r"fingerprint ([0-9a-f]{64})", first.read_text(encoding="utf-8")
        )
        final_match = re.search(
            r"fingerprint ([0-9a-f]{64})", final.read_text(encoding="utf-8")
        )
        self.assertIsNotNone(first_match)
        self.assertIsNotNone(final_match)
        old_hash = file_hash(final)
        final.write_text(
            final.read_text(encoding="utf-8").replace(
                final_match.group(1), first_match.group(1), 1
            ),
            encoding="utf-8",
        )
        evaluation = self.root / "Harness" / "EVAL.md"
        evaluation.write_text(
            evaluation.read_text(encoding="utf-8").replace(old_hash, file_hash(final)),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(VERIFIER.VerificationError, "repair cycle did not change"):
            VERIFIER.verify_vault(self.root)

    def test_not_ready_hold_still_uses_the_single_repair(self) -> None:
        evaluation = self.root / "Harness" / "EVAL.md"
        text = evaluation.read_text(encoding="utf-8")
        text = text.replace("Generator first-pass verdict: READY", "Generator first-pass verdict: NOT READY")
        text = text.replace("First-pass criteria claimed ready: 8", "First-pass criteria claimed ready: 7")
        text = text.replace("First-pass overclaim criteria: 1", "First-pass overclaim criteria: 0")
        text = text.replace("Overclaim: 1/8", "Overclaim: 0/7")
        text = text.replace(
            "| Personal rules visibly affect the output | READY |",
            "| Personal rules visibly affect the output | NOT READY |",
        )
        evaluation.write_text(text, encoding="utf-8")
        result = VERIFIER.verify_vault(self.root)
        self.assertEqual(result["evaluation"]["repair_cycles"], 1)
        self.assertEqual(result["evaluation"]["first_pass_overclaim"], 0)

    def test_resume_rejects_unauthorized_answer_change(self) -> None:
        answer = self.root / "Answers" / "Q1 Risks.md"
        before = file_hash(answer)
        answer.write_text(
            answer.read_text(encoding="utf-8").replace(
                "a live release risk", "an urgent release risk"
            ),
            encoding="utf-8",
        )
        after = file_hash(answer)
        audit = self.root / "Audit.md"
        audit.write_text(
            audit.read_text(encoding="utf-8").replace(
                "| SUPPORT | No change |",
                "| PARTIAL | QUALIFIED: EU export quality is an urgent release risk: 7 of 20 test exports had empty customer-name columns. |",
                1,
            ),
            encoding="utf-8",
        )
        brief = self.root / "Morning_Brief.md"
        brief.write_text(
            "\n".join(
                line
                for line in brief.read_text(encoding="utf-8").splitlines()
                if "[Q1-01]" not in line
            )
            + "\n",
            encoding="utf-8",
        )
        receipt = self.root / "Harness" / "RESUME_RECEIPT.md"
        receipt.write_text(
            receipt.read_text(encoding="utf-8").replace(
                f"| Answers/Q1 Risks.md | {before} | {before} | {before} | NONE |",
                f"| Answers/Q1 Risks.md | {before} | {before} | {after} | NONE |",
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(VERIFIER.VerificationError, "lacks a named PARTIAL"):
            VERIFIER.verify_vault(self.root)

    def test_resume_must_take_saved_next_action_first(self) -> None:
        write_candidate_state(self.root)
        receipt = self.root / "Harness" / "RESUME_RECEIPT.md"
        receipt.write_text(
            receipt.read_text(encoding="utf-8").replace(
                "First resumed action: read completed human audit and verify continuity hashes",
                "First resumed action: regenerate the normalized notes",
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(VERIFIER.VerificationError, "first resumed action must equal"):
            VERIFIER.verify_candidate(self.root)

    def test_candidate_rejects_run_id_that_disagrees_with_resume(self) -> None:
        write_candidate_state(self.root)
        state = self.root / "Harness" / "RUN_STATE.md"
        state.write_text(
            state.read_text(encoding="utf-8").replace(
                "Run ID: p4-course-001-resume", "Run ID: unrelated-run", 1
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(VERIFIER.VerificationError, "Run ID must match"):
            VERIFIER.verify_candidate(self.root)

    def test_candidate_requires_awaiting_candidate_check_phase(self) -> None:
        write_candidate_state(self.root)
        state = self.root / "Harness" / "RUN_STATE.md"
        state.write_text(
            state.read_text(encoding="utf-8").replace(
                "Phase: AWAITING_CANDIDATE_CHECK", "Phase: BUILDING", 1
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(VERIFIER.VerificationError, "AWAITING_CANDIDATE_CHECK"):
            VERIFIER.verify_candidate(self.root)

    def test_candidate_accepts_documented_trusted_candidate_check_wording(self) -> None:
        write_candidate_state(self.root)
        state = self.root / "Harness" / "RUN_STATE.md"
        state.write_text(
            state.read_text(encoding="utf-8").replace(
                "run the untouched course verifier in candidate mode",
                "run the trusted candidate check",
                1,
            ),
            encoding="utf-8",
        )
        result = VERIFIER.verify_candidate(self.root)
        self.assertEqual(result["resume"]["result"], "PASS")

    def test_incomplete_handoff_holds(self) -> None:
        handoff = self.root / "Harness" / "HANDOFF_RECEIPT.md"
        handoff.write_text(
            handoff.read_text(encoding="utf-8").replace("Handoff status: COMPLETE", "Handoff status: DRAFT"),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(VERIFIER.VerificationError, "Handoff status must be COMPLETE"):
            VERIFIER.verify_vault(self.root)

    def test_manifest_check_rejects_changed_file(self) -> None:
        VERIFIER.write_manifest(self.root, VERIFIER.verify_vault(self.root))
        note = self.root / "EU Export.md"
        note.write_text(note.read_text(encoding="utf-8") + "changed\n", encoding="utf-8")
        with self.assertRaisesRegex(VERIFIER.VerificationError, "changed: EU Export.md"):
            VERIFIER.check_manifest(self.root)

    def test_manifest_check_rejects_added_file(self) -> None:
        VERIFIER.write_manifest(self.root, VERIFIER.verify_vault(self.root))
        write(self.root / "extra.txt", "new file")
        with self.assertRaisesRegex(VERIFIER.VerificationError, "added: extra.txt"):
            VERIFIER.check_manifest(self.root)

    def test_manifest_check_rejects_deleted_file(self) -> None:
        VERIFIER.write_manifest(self.root, VERIFIER.verify_vault(self.root))
        (self.root / "EU Export.md").unlink()
        with self.assertRaisesRegex(VERIFIER.VerificationError, "deleted: EU Export.md"):
            VERIFIER.check_manifest(self.root)

    def test_cli_checks_external_manifest_without_rewriting_it(self) -> None:
        internal = VERIFIER.write_manifest(self.root, VERIFIER.verify_vault(self.root))
        external = self.root.parent / "P4_BASELINE_TEST.json"
        shutil.copy2(internal, external)
        before = external.read_bytes()
        checked = subprocess.run(
            [
                sys.executable,
                str(VERIFIER_PATH),
                str(self.root),
                "--check-manifest",
                str(external),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        self.assertIn("PASS P4 baseline:", checked.stdout)
        self.assertEqual(external.read_bytes(), before)

    def test_copied_checker_refuses_to_validate_its_own_vault(self) -> None:
        copied_verifier = self.root / "tools" / "verify_vault.py"
        checked = subprocess.run(
            [sys.executable, str(copied_verifier), str(self.root), "--candidate"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(checked.returncode, 1)
        self.assertIn("Refusing self-verification", checked.stdout)

    def test_cli_never_overwrites_manifest_after_failure(self) -> None:
        first = subprocess.run(
            [sys.executable, str(VERIFIER_PATH), str(self.root), "--write-manifest"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        manifest_path = self.root / "Harness" / "BASELINE_MANIFEST.json"
        manifest_path.write_text("sentinel\n", encoding="utf-8")
        answer = self.root / "Answers" / "Q1 Risks.md"
        answer.write_text(answer.read_text(encoding="utf-8").replace("[[Source_Packet/EXP-214_eu-export-qa]]", "[[Missing Source]]"), encoding="utf-8")
        failed = subprocess.run(
            [sys.executable, str(VERIFIER_PATH), str(self.root), "--write-manifest"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(failed.returncode, 1)
        self.assertIn("HOLD P4 vault:", failed.stdout)
        self.assertEqual(manifest_path.read_text(encoding="utf-8"), "sentinel\n")


if __name__ == "__main__":
    unittest.main()
