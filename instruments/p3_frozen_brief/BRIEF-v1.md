# BRIEF-v1 — Frozen extraction brief (do not modify)

**Brief ID:** BRIEF-v1  
**Version:** 1.0  
**Instruction to engines:** Use only the provided corpus files. If unknown, say UNKNOWN. Do not invent entities.

## Extract

Produce a markdown table with one row per **WatchID** found in the corpus:

| WatchID | DisplayName | Status | LocationOrService | RiskOrSeverity | Evidence (file + short quote) | Notes |

## Rules

1. **WatchID** must match an ID present in `watchlist.csv` (deterministic join).  
2. If a source mentions an entity not on the watchlist, list it under a final section **Unlisted mentions** (not in the main table).  
3. Status must be one of: `ACTIVE` | `CLEAR` | `UNKNOWN` | `BLOCKED` (map synonyms; if unclear → UNKNOWN).  
4. Every table cell that states a fact needs evidence quote ≤20 words.  
5. Contradictions: keep both claims in Notes; do not silently drop.  
6. No recommendations unless supported by corpus.

## Output order

1. Table  
2. Contradictions (bullets)  
3. Unlisted mentions  
4. Gaps (what the corpus does not support)
