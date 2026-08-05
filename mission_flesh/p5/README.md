# P5 — Poisoned corpus pack

Untrusted intake for the sealed P4 second brain.

- `intake/` — seven logistics staff files (nothing announces its class)
- `reference_corpus/` — closed citation world + `trusted_facts.json`
- `scripts/` — launcher, validator, promoter, auditors (trusted path)
- `harness/exposed/` — deny-by-default OpenCode runtime config for staging
- `harness/reader/` — fresh read-only MCP retriever for poisoned acceptance
- `control_templates/` — clean Direction/Closeout templates
- `fallback/` — instructor sealed vault + baseline (not P4 credit)
- `staff/INTAKE_ANSWER_KEY.md` — facilitator only

Treat the whole batch as untrusted until each item has a validated triage row
promoted after one operator approval. Nothing crosses into the vault without
that gate. The exposed agent writes only `out/triage_candidate.json`.

Run the deterministic checks from the repository root:

```text
python3 -m unittest discover -s mission_flesh/p5/tests -v
```
