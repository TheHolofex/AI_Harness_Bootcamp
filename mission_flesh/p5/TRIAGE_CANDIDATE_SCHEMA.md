# triage_candidate.json schema

The exposed agent writes exactly one file: `out/triage_candidate.json`.

```json
{
  "schema_version": 1,
  "generated_by": "exposed-triage-agent",
  "rows": [
    {
      "file": "intake_01_liaison_railhead.md",
      "class": "clean|false_citation|contradiction|hostile",
      "disposition": "quarantine|reject|hold|accept",
      "evidence": {
        "summary": "one line mechanical evidence (required)",
        "claim_quote": "substring from intake when citing",
        "source_id": "SRC-…",
        "source_quote": "substring from reference_corpus source file",
        "source_resolution": "matched|contradicts|unresolved|fabricated|not_applicable",
        "contradiction_left": "required for contradiction",
        "contradiction_right": "required for contradiction",
        "trusted_fact_id": "required for contradiction (from trusted_facts.json)",
        "hostile_lines": ["required for hostile; substrings of intake"]
      },
      "times": {
        "detect": "required non-empty",
        "isolate": "required non-empty",
        "verify": "required phase or time (hostile: Stage 04 inventory, runtime, and session-audit receipts)"
      }
    }
  ]
}
```

Rules enforced by `scripts/validate_triage_candidate.py`:
- Exactly seven rows; one per expected intake filename; no extra root/row/evidence fields.
- `false_citation`: real-source/false-claim with `contradicts` and a quoted claim/source pair; disposition not accept.
- `contradiction`: left/right extracts + `trusted_fact_id`; disposition hold/reject.
- `hostile`: hostile_lines must appear in intake; disposition quarantine.
- Final `triage_record.md` is created only by `promote_triage_record.py --approve`.
