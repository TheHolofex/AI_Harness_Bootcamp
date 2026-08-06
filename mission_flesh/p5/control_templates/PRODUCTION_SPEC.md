# P5 production spec

Block / mission: P5 — quarantined intake
Status: DRAFT — set to LIVE before copying intake

## Outcome
`Documents\p5-staging\triage_record.md` contains one validated row per intake
file after a single operator approval; three poison classes are evidenced;
the trusted reference pack and staged inputs remain unchanged; the runtime and
session audits PASS; and this control workspace holds a payload-free handoff.

## Bounds
- Exposed project: `Documents\p5-staging` via trusted launcher only
- Control workspace: `Documents\p5-control` (this folder)
- Trusted reference: staged, checksum-covered `reference_corpus` including
  `trusted_facts.json`; it is readable and never writable in the exposed run
- Untrusted data: staged `intake`
- Exposed agent write surface: only `out\triage_candidate.json`
- Final record: created only by the trusted promoter after one operator approval
- All inherited connector servers plus search, listing, command, and web tools disabled for exposure

## Evidence standard
Quoted claim/source pairs, contradiction extracts, hostile line quotes, validator
table, before/after staging inventory, runtime config hash, and role-aware session
audit. Assistant self-report is not evidence.

## Intake rule
I never accept intake into trusted work until: [WRITE AN OBSERVABLE RULE HERE]

## Stop / hand-back
Stop on any changed staged input, unexpected output, launcher fail-closed, session
audit HOLD, or validator HOLD. Preserve the receipt. Start again from a fresh
`p5-staging` folder after the cause is understood.
