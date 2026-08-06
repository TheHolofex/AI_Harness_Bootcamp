# P5 — Poisoned corpus pack

This pack is the complete starting state for the P5 quarantine exercise. It
does not consume files or services from another module.

- `intake/` — seven logistics staff files (nothing announces its class)
- `reference_corpus/` — checksum-covered citation world + `trusted_facts.json`
- `scripts/` — restricted launcher, validator, promoter, inventory, and audit tools
- `harness/exposed/` — deny-by-default OpenCode runtime config for staging
- `control_templates/` — clean Direction/Closeout templates
- `staff/INTAKE_ANSWER_KEY.md` — facilitator only

Treat the whole batch as untrusted until each item has a validated triage row
promoted after one operator approval. The exposed agent writes only
`out/triage_candidate.json`. The reference pack and every staged input remain
unchanged throughout the run.

Run the deterministic checks from the repository root:

```text
python3 -m unittest discover -s mission_flesh/p5/tests -v
```
