# Module 2 facilitator runbook

## Session result

The learner places one saved rule, maps what actually loaded, predicts that the hostile note is data, runs the supplied screen on a clean note and hostile notes, loads the rule through the harness launcher and observes the instruction_loaded receipt with matching hashes before the first provider request, runs a fresh second session with identical load identity, tests the negative case for a missing rule file, and states the remaining bypass.

Desk knowledge is not graded. If learners need facts that are not in the packet, the case is defective.

**What the harness changes:** the launcher appends the saved rule through --append-system-prompt and the course_guard extension inspects ctx.getSystemPrompt() for the exact trimmed text, emits the instruction_loaded receipt with file_sha256 and loaded_text_sha256 before any provider_request, and the measurement prompt forces course_read on every DN-001 through DN-040 so the harness actually processes the pile.

## Before class

1. Run `python3 shared/case/guard.py shared/case/DN-003.md` from the Module 2 directory and confirm exit 0.
2. Run the same command on `shared/case/DN-014.md` and confirm exit 1.
3. Confirm `shared/controls/SAVED_INSTRUCTION.md` contains the current rule text.
4. Put graded notes and the deciding screen outside the learner repository and model context.
5. Confirm the learner's environment can copy a folder and run `python3`.
6. Print or provide the public rubric.
7. Confirm the learner can reach the shared run_omp.py launcher from the checkout.

## Three-hour route

| Time | Facilitator action | Learner result |
|---|---|---|
| 0:00–0:20 | Introduce the desk, class-only boundary, and the pile | Learner can name clean ticket versus hostile note |
| 0:20–0:45 | Learner maps resolved state | Direction, sources, saved instruction, screen, evidence named |
| 0:45–1:00 | Learner writes the prediction | Hostile note predicted as data before any screen run |
| 1:00–1:40 | Learner runs the screen | Clean note accepted; hostile note rejected |
| 1:40–2:20 | Learner loads the rule and inspects the receipt | instruction_loaded appears before provider_request with matching hashes |
| 2:20–2:40 | Learner runs a second fresh session | Load hashes match; answer is identical |
| 2:40–2:55 | Learner tests negative load | Missing rule stops before contact; run is restored |
| 2:55–3:00 | Collect the handoff | Reconstruction without coaching, or `HOLD` |

## Coaching boundary

You may:

- define a term already stated in the packet;
- point to the current step or file;
- help open a file or run a supplied command;
- ask the learner to state which file loaded.

You may not supply:

- the prediction that the hostile note is data;
- the expected exit status for any note;
- the wording of the remaining bypass;
- an edited screen; or
- the handoff verdict.

If you cross that line, mark the work as guided practice. Use a new protected case for scoring. Select the examples yourself when you ask a learner to defend a map row.

## Domain-overload check

Stop and inspect the case—not the learner—when:

- more than two learners ask for the same unstated yard fact;
- domain explanation exceeds 15 minutes;
- learners cannot explain “data versus instruction” in ordinary language; or
- graders cannot attribute a miss to context control rather than depot knowledge.

Record the issue and revise the adapter before the next cohort.

## `HOLD` conditions

Use `HOLD` when a decisive note, accessible view, screen, or reload path is missing or compromised; the producer can edit the deciding screen; the hostile note is treated as an instruction; the load receipt is missing or does not match; a negative load does not stop before contact; or the learner attempts consequential use.

A well-documented `HOLD` can complete practice. It does not pass the graded outcome.

## Collect

- resolved-state map;
- prediction;
- screen outputs;
- guard.jsonl (or the load receipt excerpt);
- second-session comparison;
- negative-load evidence;
- bypass statement;
- handoff; and
- protected result or reason for `HOLD`.

Do not collect credentials, private local files, outside operational details, or model chat history unrelated to the case.
