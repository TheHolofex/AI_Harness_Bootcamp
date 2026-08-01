# P3 Frozen brief — course instrument

**When:** Tuesday PM (Twin-engine)  
**Purpose:** One **versioned** extraction brief + frozen corpus. Run **unchanged** on the Codex app and OpenCode. Adjudicate.

## Student flow

1. Use the **same track** as P2.  
2. Read `BRIEF-v1.md` (do not edit).  
3. Read frozen sources in your track `corpus/`.  
4. Run BRIEF-v1 on **Engine A** (Codex app) → save `output_codex.md`.  
5. Run BRIEF-v1 on **Engine B** (OpenCode, `--pure`, model pinned with `-m`) → save `output_opencode.md`.  
6. Fill `COMPARATOR.md` (side-by-side).  
7. Write verdict: keep / discard / unknown per disputed field.  
8. Log brief id `BRIEF-v1` + both outputs + comparator.

## Rules

- Brief text frozen. If you must clarify, create `BRIEF-v2` only as stretch and label it.  
- Joins on watchlist IDs are deterministic — models don’t get to invent join keys.  
- **The engines must be independent, and independence is checked, not assumed.** OpenCode reads `~/.claude/CLAUDE.md` and `.claude/skills` unless `OPENCODE_DISABLE_CLAUDE_CODE=1` is set (pre-work step 8). `--pure` keeps installed plugins from editing the brief on its way to the model. An engine reading the other's notes agrees for the wrong reason.
- **The same check applies to the Codex app, and it is the one students forget.** The app loads `AGENTS.md` from the project root — including the one you improved in P2 — plus `~/.codex/AGENTS.md`, any skills it discovers, and memories if you enabled them. Run BRIEF-v1 inside your P2 project and the Codex side is carrying your craft while OpenCode runs bare. That is not two engines disagreeing; that is one engine plus your notes.
  - Run P3 from a **clean folder** holding only the frozen corpus, or state in the comparator exactly which instruction files were live. Either is honest. Silence is not.
  - Record it the same way you record the model id: engine, model, and what context was loaded. **An advantage you didn't declare looks exactly like a capability you don't have.**
- **Pin the model on each run** (`-m`) rather than inheriting whichever was last used, and record engine, model id, and version beside each output. Two runs you can't identify are not evidence.
- Agreement ≠ truth.

## Timing

Corpus is small on purpose. Finishable in-block with time for adjudication.
