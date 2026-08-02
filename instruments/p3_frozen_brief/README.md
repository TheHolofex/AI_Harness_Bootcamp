# P3 Frozen brief — course instrument

**When:** Tuesday PM (Twin-engine)  
**Purpose:** One **versioned** extraction brief + frozen corpus. Run **unchanged** on the Codex app and OpenCode. Adjudicate.

## Student flow

1. Use the **same track** as P2.  
2. Read `BRIEF-v1.md` (do not edit).  
3. Read frozen sources in your track `corpus/`.  
4. Run BRIEF-v1 on **Engine A** (Codex app, `gpt-5.6-terra`, OpenAI API key stored in Codex sign-in) → save `output_codex.md`.
5. Run BRIEF-v1 on **Engine B** (OpenCode, xAI key, `--pure`, `xai/$env:HB_XAI_MODEL` pinned with `-m`) → save `output_opencode.md`.
6. Fill `COMPARATOR.md` (side-by-side).  
7. After the frozen comparison, connect the project-local `p3_evidence` MCP server and build `MCP_EVIDENCE_PACKET.md` for every material row plus every agreed claim that drives the release decision. Confirm the connection fit and contract, group by source, read each needed file once, record the useful-call receipt, and disable the server when the packet is saved.
8. Write verdict: keep / discard / unknown for every material difference and agreed release-driving claim.
9. Log brief id `BRIEF-v1` + both outputs + comparator + MCP evidence packet.

## Rules

- Brief text frozen. If you must clarify, create `BRIEF-v2` only as stretch and label it.  
- Joins on watchlist IDs are deterministic — models don’t get to invent join keys.  
- **Run separation and shared paths must be recorded, not assumed.** OpenCode can import Claude-named compatibility files even when no Anthropic key exists. Set `OPENCODE_DISABLE_CLAUDE_CODE=1` to block those files. The setting does not call Anthropic. Use `--pure` to keep installed plugins from editing the brief on its way to the model. An engine reading the other's notes agrees for the wrong reason.
- **The same check applies to the Codex app, and it is the one students forget.** The app loads `AGENTS.md` from the project root — including the one you improved in P2 — plus `~/.codex/AGENTS.md`, any skills it discovers, and memories if you enabled them. Run BRIEF-v1 inside your P2 project and the Codex side is carrying your craft while OpenCode runs bare. That is not two engines disagreeing; that is one engine plus your notes.
  - Run P3 from a **clean folder** holding only the frozen corpus, or state in the comparator exactly which instruction files were live. Either is honest. Silence is not.
  - Record it the same way you record the model id: engine, model, and what context was loaded. **An advantage you didn't declare looks exactly like a capability you don't have.**
- **Pin both models.** Select `gpt-5.6-terra` in every Codex chat. Run OpenCode with `-m "xai/$env:HB_XAI_MODEL"` rather than inheriting whichever model was last used. Record engine, model id, and version beside each output. Two runs you can't identify are not evidence.
- **Clear MCP before the frozen engine run.** An enabled MCP server can add tools, server guidance, and a different retrieval path to Codex. Record the active surface, then disable it for the control. Add the course server only after both raw outputs and the comparator exist.
- **Treat MCP as an evidence route, not another mind.** The P3 server reads the same five files. Its result can make retrieval repeatable; it cannot corroborate the underlying claim. Record why the connection fits, the course origin and commit, local implementation fingerprints, server instructions and two-tool contract, planned and actual source basenames plus real exceptions, E-ID evidence rows, and raw-context checks in `MCP_EVIDENCE_PACKET.md`.
- **Use safeguards to ship the work, not to stage a lab.** The course smoke suite tests unknown files, traversal, symlinks, malformed text, size limits, empty resource and prompt surfaces, and safe disable behavior. In the live run, approve only source basenames in the real call plan, deny any unexpected request, verify decisive excerpts in raw context, and disable the project server when the packet is saved.
- P3 has no Anthropic setup or access. An optional Anthropic exercise may be introduced near the end of the course only if the instructor confirms it.
- Agreement ≠ truth.

## Timing

Corpus is small on purpose. Finishable in-block with time for adjudication.
