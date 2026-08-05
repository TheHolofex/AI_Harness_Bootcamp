# Harness Card

Complete every `[REPLACE: ...]` field before invoking `$director-loop`.

## Goal and personal fit

- Recurring goal: [REPLACE: the useful recurring outcome this harness produces]
- Decision owner: [REPLACE: the person or role who owns the resulting decision]
- Useful output: [REPLACE: the exact artifact and what it lets the reader do]
- Non-goal: [REPLACE: a plausible task this harness must not absorb]

## Control flow

- Fixed outer flow: scope -> fixed read-all of four inbox captures -> organize with approval -> retrieve -> human audit hand-back -> fresh resume -> candidate check -> evaluate -> finish or hand back
- Bounded adaptive retrieval loop: [REPLACE: after organization, how the active question and each observed note/link determine the next relevant note and what ends the search]

The four short captures are read as one fixed batch outside the retrieval budget. Only the later question-driven traversal is adaptive because each next `Source_Packet` record must be linked by already opened raw evidence. The adaptive loop may open at most six packet records and must feed both required answers.

## Budgets

- Maximum model turns: [REPLACE: positive integer]
- Wall-clock limit: [REPLACE: positive integer] minutes
- Retry ceiling: [REPLACE: positive integer] per correctable operation
- No-progress limit: [REPLACE: positive integer] repeated observations

These are declared operating limits in P4. Record who notices and stops the run. P6 will test which limits a harness mechanism actually enforces.

## Terminal reasons

- SUCCESS: required artifacts pass and the human audit is complete
- NEEDS_EVIDENCE: a decision-driving claim cannot be supported from the vault
- BUDGET_STOP: the turn or time limit is reached
- ERROR_CEILING: a correctable operation still fails after the retry ceiling
- NO_PROGRESS: the allowed repeated observations occur without a state change
- HUMAN_HAND_BACK: the next action requires operator judgment or approval

## Human approval

- Organization gate: approve proposed note titles, hubs, links, and preserved status words before writes.
- Citation-audit gate: pause once after the answers exist; the operator opens every citation and owns its disposition.
- Irreversible or external action: not permitted in this vault.

## Complexity rejected

- Router — rejected: [REPLACE: why this run does not contain separable task classes]
- Parallel worker team — rejected: [REPLACE: why the source volume or independence does not repay coordination]
- Plugin — rejected: [REPLACE: why this personal workflow is not stable enough to distribute]
- New MCP server — rejected: [REPLACE: why project-scoped files are already the correct tool surface]
- Reflection without an oracle — rejected: [REPLACE: which verifier, human audit, and evaluator evidence may trigger revision]

## Component register

| Component | Job | Load timing | Cost | Disable path |
|---|---|---|---|---|
| `AGENTS.md` | Stable personal operating rules | Every project turn | Always-on context | Rename after saving a copy |
| `director-loop` skill | One integrated recurring procedure | Only matching director-brief work | Procedure context and one run | Do not invoke or remove the skill folder |
| `RUN_STATE.md` | Cross-session completed/open/next state | Start and end of each material stage | One small read and write | Archive after closeout |
| `RUN_TRACE.md` | Observable actions, evidence, budgets, and findings | Append after material actions | Small append-only record | Stop appending after terminal state |
| `SOURCE_MANIFEST.json` | Course-owned exact-path evidence hashes | Before any raw evidence is trusted | One bounded hash pass | Replace only through a new trusted course seed |
| `RESUME_RECEIPT.md` | Cross-context continuity evidence | Once after the human audit | Hash reads and one receipt | Hand back if continuity cannot be established |
| `EVAL.md` | Fresh read-only default-fail criterion review | After the human audit and brief | One evaluator pass | Skip only when the run already handed back before evaluation |
| `director_evaluator` | Independent rubric check | After the first trusted candidate check, regardless of verdict | One fresh read-only context | Hand back if it is unavailable |
| course `verify_vault.py` | Mechanical artifact, trust-anchor, and baseline checks | Candidate, release, and P5 drift checks | One external local Python run | Hand back rather than use the copied checker |

Keep a component only while its job changes the quality, recoverability, or cost of the finished work.
