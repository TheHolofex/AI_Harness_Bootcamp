# Module 3 facilitator runbook

## What the harness changes

The harness reads and hashes the 40-document pile and cannot write a release.

## Session result

The learner records a position with evidence under six concerns from the packet, then inspects, runs, contains, disconnects, and revokes a supplied hash tool.

Desk knowledge is not graded. If learners need facts that are not in the packet, the case is defective.

## Before class

1. Run `python3 shared/tools/hash_source.py shared/case/REL-001.md` from the Module 3 directory and confirm the line starts with `sha256`.
2. Run `python3 shared/tools/hash_source.py ../outside/sentinel.txt` (or /etc/passwd) and confirm exit 1 and `HOLD: path not allowed`.
3. Confirm 40 REL-*.md files exist under shared/case and the packet names NB-NOTE-17, Mill Depot, Clinic B-2, MH-6.
4. Put graded notes and the deciding tool outside the learner repository and model context.
5. Print or provide the public rubric.

## Three-hour route

| Time | Facilitator action | Learner result |
|---|---|---|
| 0:00–0:20 | Introduce both branches and the class-only limit | Learner can name decision versus connection |
| 0:20–1:00 | Learner writes the six-concern decision | Position recorded with citations under all six concerns and combined effect |
| 1:00–1:30 | Learner inspects raw authority and hashes REL-001 | Exact command; `sha256` line |
| 1:30–2:00 | Learner runs the composed-negative prompt against the tool | No second file; path still refused; 40 files read |
| 2:00–2:30 | Learner disconnects and revokes the work copy | File-not-found or `HOLD: path not allowed` (direct and adapter) |
| 2:30–3:00 | Collect the handoff | Reconstruction without coaching, or `HOLD` |

## Coaching boundary

You may:

- define a term already stated in the packet;
- point to the current step or file;
- help open a file or run a supplied command;
- ask the learner to state the sharing limit.

You may not supply:

- the disposition rationale;
- wording under any of the six concerns;
- the expected hash;
- the refuse message; or
- the revoke result.

If you cross that line, mark the work as guided practice. Use a new protected case for scoring. Select the examples yourself when you ask a learner to defend a concern row.

## Domain-overload check

Stop and inspect the case—not the learner—when:

- more than two learners ask for the same unstated packet fact;
- domain explanation exceeds 15 minutes; or
- graders cannot attribute a miss to release judgment or tool operation.

## `HOLD` conditions

Use `HOLD` when a decisive packet, accessible view, protected tool, or revoke path is missing or compromised; rights are unclear; the producer can edit the deciding tool; or the learner attempts consequential use.

A well-documented `HOLD` can complete practice. It does not pass the graded outcome.

## Collect

- release decision;
- authority inventory;
- hash line and refuse output;
- composed-negative result;
- disconnect and revoke records;
- handoff; and
- protected result or reason for `HOLD`.

Do not collect credentials, private local files, outside operational details, or model chat history unrelated to the case.