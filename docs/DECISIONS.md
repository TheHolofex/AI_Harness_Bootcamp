# P5 standalone implementation decisions

1. **P5 owns its complete starting state.** The exercise consumes only
   `mission_flesh/p5/` inputs and the learner's two fresh working folders.
2. **The quarantine gate is the product.** P5 ends with a validated,
   operator-approved triage record. It does not write accepted material into a
   downstream knowledge system.
3. **Closed reference world.** `reference_corpus/`, its manifest, checksums, and
   `trusted_facts.json` supply every graded citation and contradiction prior.
4. **Exactly three planted poison classes.** `intake_02` is the false citation,
   `intake_04` is the contradiction, and `intake_06` is hostile. `intake_05` is
   unambiguously clean.
5. **One exposed write path and direct reads only.** The exposed agent may
   write only `out/triage_candidate.json`. Search and listing tools are disabled;
   the supplied intake inventory and reference manifest name every file to read.
6. **One human authority gate.** The trusted promoter creates
   `triage_record.md` only after deterministic validation and explicit
   `--approve`.
7. **Bounded containment claim.** Before/after staging inventory, runtime-config
   hash, and role-aware session audit prove only the checked files, outputs,
   paths, and tool calls. The audit binds exported session-directory metadata to
   the resolved staging root and detects compact bulk dumps of protected facts.
8. **Generic connector isolation.** The launcher disables every inherited MCP
   server without depending on or naming a specific product.
9. **Exact staging delta.** Only `out/triage_candidate.json`,
   `out/session.json`, `review_table.md`, and `triage_record.md` may appear after
   the freeze. Any other addition, change, removal, or symlink is HOLD.
10. **Stable checklist state.** The twelve registry check identifiers remain
    unchanged.
11. **Historical integration assets removed.** The P4 fallback, read-only
    retrieval harness, generated work trees, and P4/P5 interface plans are not
    part of standalone P5.
12. **Failure is fail-closed.** An unparseable session export, intent-only tool
    inventory, changed input, unexpected output, or invalid candidate closes
    HOLD with its receipt preserved.
