# Run Trace

Append observable actions and results. Do not record hidden reasoning or chain-of-thought.

| Step | Observable action | Observation or evidence | Budget after step | Outcome |
|---|---|---|---|---|
| [REPLACE: step number] | [REPLACE: tool call, file action, approval, check, or evaluator action] | [REPLACE: returned fact, artifact path, error, or human verdict] | [REPLACE: turns and minutes remaining] | [REPLACE: CONTINUE, REPAIR, FINISH, or HAND_BACK] |

## Fixed inbox inventory

Record all four unchanged captures once. These reads do not consume the adaptive packet budget.

| Fixed inbox capture | Observable result |
|---|---|
| [REPLACE: one direct inbox wikilink] | [REPLACE: status, named question, and starting refs found] |

## Retrieval ledger

Record one to six `Source_Packet` opens. The first packet must be linked by a fixed inbox capture; each later packet must be linked by a fixed capture or an earlier packet. Include at least one packet-to-packet hop.

| Open | Evidence root | Reference discovered in | Observable result |
|---|---|---|---|
| [REPLACE: 1 through at most 6] | [REPLACE: one Source_Packet wikilink] | [REPLACE: one already opened raw record] | [REPLACE: fact, gap, stop, or next ref found] |

## First-pass HOLD findings (append-only)

- [REPLACE: every preserved candidate/evaluator HOLD criterion and exact finding, or NONE]

Never delete a first-pass HOLD after repair. The final receipt belongs in `EVAL.md` and a later trace row.

Terminal reason: [REPLACE: the same allowed terminal reason recorded in RUN_STATE.md]
