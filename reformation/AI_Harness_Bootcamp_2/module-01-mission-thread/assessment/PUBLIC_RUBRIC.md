# Module 1 public scoring rubric

The standard below does not change when identifiers, values, source order, or distractors change.

Every hard gate must pass. A strong summary cannot compensate for a material source or handoff failure.

| Hard gate | Passing evidence | `HOLD` examples |
|---|---|---|
| Exact identity | Mission, vehicle, route, destination, permit, lots, decision time, zones, and source versions match | Similar identifier, unstable source, missing version |
| Source use | Each source is used only for claims it has authority to establish | Receipt used as release; general page used as route authority |
| Thread depth | All eight steps appear; material rows address entry condition, claim, source, calculation, output, next handoff, and uncertainty | Summary jumps from receipt to mission success |
| Statement type | Every material statement is one `SOURCE FACT`, `CALCULATION`, `INFERENCE`, `DECISION`, or `UNSUPPORTED` | Compound claim hides several kinds |
| Source trace | Material claim includes source ID, version, locator, excerpt, and learner-written warrant | Citation exists but does not support interpretation |
| Arithmetic | Required values are recomputed from supported premises with units and time zones; counterfactual arrival is not presented as an achievable baseline ETA | Right number copied from AI; rack omitted; UTC treated as MDT; failed gate followed by unconditional arrival |
| Challenge | Stale, irrelevant, similar-ID, receipt/effect, hostile-text, and producer-self-review claims are rejected with reasons | Wrong source merely noticed or silently ignored |
| Review surface | Another person can see supported, contradicted, unresolved, blockers, sources, and next evidence in the supplied surface | Files exist but surface omits decision-critical state |
| Baseline verdict | `ACCEPT`, `REVISE`, `REJECT`, or `HOLD` matches every material gate and stays inside class use | Material miss with `ACCEPT`; later event reported as complete |
| Changed source | Prediction predates reveal; only dependent fields change; stale values disappear; unaffected claims remain | Baseline overwritten, unrelated claim changes, stale v5 remains |
| Handoff | Another person can reconstruct the result without coaching | Depends on memory, chat history, or author explanation |
| Thread walk | On an evaluator-selected adjacent pair, learner explains output, next entry condition, pass/fail, evidence, and break condition | Reads fields without explaining why the handoff succeeds or fails |
| Claim defense | On an evaluator-selected row, learner opens the exact source, defends the warrant or calculation, rejects a competing source, and names a falsifier | Chooses own easy row, relies on AI reassurance, or cannot locate support |

## Visible practice check

The visible checker can inspect:

- required files and columns;
- exact practice IDs and step names;
- source-manifest hashes;
- allowed statement and result labels;
- deterministic practice arithmetic;
- required challenge headings;
- baseline preservation;
- predicted and actual changed fields; and
- stale-value or unrelated-change errors.

It cannot decide whether a source is applicable, a passage supports the interpretation, the warrant is sound, an inference is responsible, or the final verdict is professionally defensible.

## Graded attempt

The evaluator selects an unseen case and holds the answer key. The producing AI cannot inspect or alter the decisive checks. A missing, inaccessible, exposed, or compromised graded source produces `HOLD` and a new case—not a simulated pass.

## Later attempt

A later attempt uses a new case against this same rubric. Repeating this packet does not replace that result.
