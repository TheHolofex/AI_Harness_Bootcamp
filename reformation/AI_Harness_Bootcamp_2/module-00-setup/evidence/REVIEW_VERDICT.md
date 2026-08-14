# Module 0 verdict

**Date:** 2026-08-14
**Standard:** `reference/REFERENCE.md` v2, SHA-256 recorded in `reference/REFERENCE.sha256`
**Changes from v1 and what forced them:** `reference/AMENDMENTS.md`

Every row below names the command that produces it and the file holding the output. Re-run any of
them from the module directory. A row without a reproducible command is not evidence, which is the
defect this table exists to avoid: the v1 verdict reported `171 PASS / 0 FAIL` for a suite whose
checks had never been shown to fail, on a tree containing three of v1's own absolute failures.

## Executable evidence

| Evidence | Command | Result |
|---|---|---|
| Acceptance oracle, all criteria | `python3 tests/oracle.py` | see `evidence/v2/suite.txt` |
| Oracle adequacy: every criterion proven able to fail | `python3 tests/test_module_00.py` | 37 mutations, 0 survivors — `evidence/v2/suite.txt` |
| Practice checker adequacy | `python3 tests/test_checker.py` | 18 checks, 18 killing fixtures — `evidence/v2/checker-adequacy.txt` |
| Checker rejects a fact-inverted draft | `python3 shared/case/check_artifact.py <inverted draft>` | 7 checks fail — `evidence/v2/checker-rejects-inverted.txt` |
| Checker fails a correct changed-input revision, as the lab states | `python3 shared/case/check_artifact.py <revised draft>` | fails on capacity only — `evidence/v2/checker-changed-input.txt` |
| n8n check rejects a non-n8n listener | `python3 -m http.server 5678` then `python3 shared/case/verify_n8n.py` | HOLD — `evidence/v2/n8n-rejects-any-listener.txt` |
| Tool proof rejects hand-created files | `python3 shared/case/verify_tool_proof.py <dir> <token>` | HOLD on all three — `evidence/v2/tool-proof-rejects-handmade.txt` |
| Starting state before any fix | `python3 tests/oracle.py` at the v1 tree | 12 PASS / 18 FAIL — `evidence/v2/oracle-red.txt` |

## Evidence inherited from the v1 build, not re-run here

These were produced during the v1 build and are kept because they remain true statements about the
external world. Neither was re-run for v2, so neither appears in the table above.

- `evidence/url-check.txt` — every public source link resolved on 2026-08-12.
- `evidence/ubuntu-container-subset.txt` — Ubuntu 24.04 ARM64 base packages and Python, in a
  container, at v1. A subset of one platform's step 3, not a platform run.

## What the oracle does and does not certify

It certifies that every criterion in Reference v2 §6 passes against this tree, and — separately, and
this is the part v1 had no equivalent of — that every one of those criteria fails when the module is
broken in the corresponding way. `tests/mutations.py` holds one mutation per criterion;
`tests/test_module_00.py` applies each to a temporary copy and requires the named criterion to fail.
Zero survivors.

It does not certify that any command runs on any target platform. Static acceptance is not execution.

## Target-platform execution status

| Platform | Status |
|---|---|
| Windows PowerShell on native Windows | **UNTESTED end to end** |
| Windows WSL 2 with Ubuntu | **UNTESTED end to end** |
| macOS Apple Silicon | shell fences parse; read-only checks run; **full install, provider and GUI path untested** |
| macOS Intel | **UNTESTED** |
| Ubuntu 24.04 ARM64 | base package and Python subset executed in a container; **GUI and provider path untested** |
| Ubuntu 26.04 | **UNTESTED** |
| Arch Linux x86_64 | **UNTESTED** |

Reference §1.1 is the reason this table is stated so plainly. Mirhosseini and Parnin executed 14,876
blocks from 616 setup tutorials in fresh virtual machines: **0 of 40 hand-annotated tutorials reached
a working setup.** A five-platform path that has not been run on five clean machines should be read
as broken on at least one of them right now. Nothing in this package changes that, and no row above
should be read as if it did.

## Class F — the prose panel

`reviews/round-1-*.md` hold three reviews scoring 23/32, 26/32 and 24/32 against a bar of 32/32.
Every deduction cites a sentence. Their findings were fixed and the fixes are in this tree.

**Class F is UNMEASURED.** The three reviewers are language models reading from an assigned seat.
Reference §6 Class F requires three people — one technical beginner, one experienced cross-platform
operator, one professional editor. The round-1 files say so in their own headers, and check D2
refuses a Class F pass claim until three reviews declare a human reviewer. The scores above are the
state of the prose *before* the fixes; no one has scored it since.

No AI-detector result appears anywhere in this package, and none would be accepted. At a 5%
false-positive operating point the best detector in RAID (ACL 2024) reaches 85.0% and most sit at
65–75%, a homoglyph substitution costs the strongest one 41.9 points, and Liang et al. (2023) found
over 61% of TOEFL essays by non-native writers flagged as machine-written.

## Still unmeasured

Every one of these needs a pilot, not an argument:

- setup duration on clean and partly configured machines, per platform;
- whether the first checked draft lands inside 60 minutes;
- provider spend per learner;
- keyboard and assistive-technology operation in Obsidian and n8n — the guidance in
  `shared/ACCESSIBILITY.md` names real tools and real operations, and none of it has been run by
  someone using them;
- managed-machine escalation time;
- scorer time and agreement on the rubric;
- protected-case custody at cohort scale.

Reference §1.2 forbids this package from authoring those numbers: Nathan and Petrosino (2003) found
experts underestimate novice completion time and do not improve when told about the bias. The
figures in Reference §4.6 are planning placeholders marked `UNMEASURED`, and the pilot replaces them.

## Decision

**Accepted as a reviewed implementation package, ready for a controlled pilot on one platform with a
facilitator present.**

**Not accepted as working on five platforms, not accepted as a measured learner experience, and not
accepted against Class F until three people score the prose.**
