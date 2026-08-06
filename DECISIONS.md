# DECISIONS — P4 Second brain pivot

1. **Root brief name for P5:** `Mission_Brief.md` (not `Morning_Brief.md`). Keeps a human-facing brief artifact; retargeted P5 Stage 01 and hostile intake accordingly.
2. **Verifier split:** `verify_brain.py` (semantic) + `verify_baseline.py` (path/hash) + `verify_vault.py` shim preserving P5’s `py -3 verify_vault.py $vault --check-manifest …` invocation.
3. **Baseline excludes `Harness/BASELINE_MANIFEST.json`** from the hashed file set so write-then-check is stable.
4. **Corpus scale:** 464 documents (420 synthesized + 44 fetched binaries/text). Assessed slice fixed at 96 with four worker partitions. Prefer real fetches first; synthesized docs carry canonical gradeable facts.
5. **Canonical facts locked** in `raw_corpus/CANONICAL_FACTS.json` (73.6 st, 40 mph rail, Kaohsiung preferred, etc.). Planted contradiction: thin notices claim 45 mph.
6. **Threat framing:** protection / detect / recover only; verifier rejects offensive tradecraft phrases and requires defensive language on threat notes.
7. **P4 schedule role:** attended consolidation after PG (Tuesday PM), not OpenCode intro. Page and capabilities state parallel dispatch as assumed.
8. **MCP path:** Obsidian Local REST API built-in MCP; API key via env var; vault at `%USERPROFILE%\Vaults\p4-vault`, outside the OpenCode project and commonly managed Documents folder.
9. **Old MERIDIAN seed** archived under `mission_flesh/p4/archive_meridian_seed/` (including old `verify_vault.py` and tests).
10. **Registry check IDs** fully replaced to match new page (12 ids); journey Wednesday blurb → “second brain”.
11. **Operator docs** (CAPABILITIES, MEASUREMENT_SPINE, OPERATOR_LOG, TRANSFER) retargeted to second-brain outcomes.
12. **No commit** performed (per instructions).
13. **OpenCode P4 config:** ship the V1 project config at `mission_flesh/p4/controller/opencode.p4.json`. It uses the Local REST API loopback HTTP endpoint `http://127.0.0.1:27123/mcp/` and reads the bearer key from `OBSIDIAN_REST_API_KEY`.
14. **Cold retrieval isolation:** run the cold query from an empty `Documents\p4-cold-query` project with the `retriever` agent. The course repo and raw corpus are not inside that project.
15. **Assessed-slice ownership:** every assessed source ID belongs to exactly one worker partition. The four partition counts are 32, 28, 22, and 14.
16. **Verifier lineage:** `verify_brain.py` checks note enums, exact permission fields, structured Obsidian receipts, and source ID/path/hash/metadata against the course corpus manifest and file bytes. It also resolves retrieval links and checks closeout state.
17. **P4 agent loading:** set `OPENCODE_CONFIG_DIR` to the shipped `vault_seed/.opencode` directory. Do not copy P4 agent files into the shared course project.
18. **Corpus snapshot date:** the pre-built warehouse keeps the fixed retrieval date `2026-08-04`. A later rebuild must not change every source hash because the wall-clock date changed.
