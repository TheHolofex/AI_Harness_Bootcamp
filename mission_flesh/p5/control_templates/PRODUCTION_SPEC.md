# P5 production spec

Block / mission: P5 — quarantined intake against the sealed second brain  
Status: LIVE

## Outcome
`Documents\p5-staging\triage_record.md` contains one validated row per intake
file after a single operator approval; three poison classes are evidenced;
pre/post baseline PASS; non-vault absence receipts PASS; payload-free handoff
in this control workspace; poisoned acceptance shows temporary-baseline PASS
with a wrong cited answer, followed by an approved MCP repair and official
baseline PASS.

## Bounds
- Trusted vault: `Documents\p4-vault` (or instructor fallback) — outside staging
- Integrity baseline: external `P4_BASELINE_[TODAY].json` — never copied into staging
- Recovery: `Documents\p4-vault_recovery` after pre-exposure PASS only
- Exposed project: `Documents\p5-staging` via trusted launcher only
- Control workspace: `Documents\p5-control` (this folder)
- Citation world: staged `reference_corpus` including `trusted_facts.json`
- Exposed agent write surface: only `out\triage_candidate.json`
- No Obsidian MCP on the exposed session; API key stripped

## Evidence standard
Quoted claim/source pairs, contradiction extracts, hostile line quotes, validator
table, baseline receipts, staging inventory, runtime config hash, role-aware
session audit. Assistant self-report is not evidence.

## Stop / hand-back
Stop on unexpected vault change, launcher fail-closed, or validator HOLD.
Restore from recovery only after recovery itself passes baseline check.
