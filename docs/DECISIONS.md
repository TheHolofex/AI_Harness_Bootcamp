# P5 implementation decisions

1. **P4 wins on names:** Trusted brief root is `Mission_Brief.md` (not `Morning_Brief.md`). Hubs are `Notes/{Modes,Nodes,Constraints,Threats,Sources}.md` and `Notes/Route/Spine.md`.
2. **Baseline tool:** P5 required path uses `mission_flesh/p4/vault_seed/tools/verify_baseline.py` only. `verify_vault.py` is a shim and is not taught on the P5 page.
3. **Poisoned-acceptance is required:** `intake_05_sealift_crisis_playbook.md` is classed clean for mechanical triage (cited LA/LB matches) but plants an uncited air-primary claim. Stage 05 forces director MCP write → retrieval of wrong answer → baseline HOLD on change → repair. Teaches unchanged ≠ true.
4. **Contradiction prior:** P5-owned `reference_corpus/trusted_facts.json` (not a P4 export). Within-batch clash in intake_04 reinforces TF-RAIL-SPEED-40.
5. **Reference pack is closed and P5-owned** under `mission_flesh/p5/reference_corpus/`. No P4 warehouse subset.
6. **Control workspace:** Direction/Closeout use `Documents\p5-control`, never the course repo (hostile source pack lives there).
7. **Full P4 baseline never enters staging.** Receipts only land in control.
8. **Exposed write surface:** only `out/triage_candidate.json`; final `triage_record.md` via `promote_triage_record.py --approve`.
9. **Registry:** kept all twelve ids; meta string only updated.
10. **OpenCode MCP isolation:** launcher resolves the merged config, force-disables every discovered MCP server, strips Obsidian API key variables, verifies deny-by-default read/edit rules, and records a sanitized resolved inventory. OpenCode 1.18.11 config resolution is proved on macOS; live Windows/global-Obsidian inheritance remains blocked.
11. **Instructor fallback:** `mission_flesh/p5/fallback/complete_vault` + `P4_BASELINE_FALLBACK.json` copied from P4 reference fixture; not P4 credit.
12. **False-citation terminology:** required catch is real-source/false-claim (45 vs 40 mph). Fabricated id SRC-FABRICATED-STEERING-99 declared in closed namespace as absent.
13. **Plan vs latest user note on brain_fact_snapshot:** cut P4 brain snapshot; used trusted_facts + within-batch contradiction. Poisoned-acceptance retained as required new capability.
14. **Where plan said “no required clean merge” and user required poisoned-acceptance:** user instruction wins; acceptance is a deliberate post-triage director path, not exposed-agent merge.


## Review remediation decisions (post no-ship review)

15. **Runtime config:** schema-valid granular permissions deny all reads except staged inputs and deny all edits except `out/triage_candidate.json`; the launcher uses supported config environment variables and no `--config` flag.
16. **Inventory:** full-tree snapshot; only four exact post-freeze additions are allowed (`out/triage_candidate.json`, `out/session.json`, `review_table.md`, `triage_record.md`). Any other addition, change, removal, or symlink HOLDs.
17. **Session audit:** parse legacy and OpenCode `info`/`parts` shapes; fail closed on zero units or intent-only inventory; ignore tool-result echoes; inspect structured tool calls and protected-content fingerprints.
18. **Validator:** exact schemas and seven-file staff oracle; quote resolution against intake/sources; required `trusted_fact_id`; ordered detect/isolate/verify phases; required false citation is real-source `contradicts` only.
19. **Promoter:** render structured evidence blocks, not summary-only table cells.
20. **Poisoned acceptance:** approved MCP patch changes the existing `Mission_Brief.md`, temporary poisoned-state baseline PASSes, a P5-owned fresh read-only agent retrieves the wrong cited answer, and an approved MCP repair restores the official baseline without requiring delete authority.
21. **Staff key:** `.gitignore` exception only for `mission_flesh/p5/staff/**` (root `staff/` remains ignored).
22. **Capability contracts:** false-citation wording retargeted to real-source/false-claim; poisoned-acceptance added to CAPABILITIES P5 requirements.
