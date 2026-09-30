# Module 5 facilitator runbook

## Session result

The learner freezes a sample of sixteen runs, writes first-failure notes, reconciles counts to 16, infers two literals, configures them in the supplied predicate using the --config flag, and runs known-bad, known-good, and missing input. The harness processes the full eighty-run pile so that the learner can open at least one decisive item.

**What the harness changes:** The harness makes the eighty-run pile finishable inside the practice time by supplying the deterministic predicate adapter; the learner still opens the decisive runs and writes the first notes by hand.

## Before class

1. Confirm eighty files `R-001.md`–`R-080.md` under shared/corpus and no old `run-*.md`.
2. Confirm `shared/checks/known-bad.txt` and `known-good.txt` exist.
3. Confirm the predicate accepts `--config`.
4. Put graded corpora outside the learner repository.
5. Prepare a public practice labels file for the stretch (opened only after prediction).

## Three-hour route

| Time | Facilitator action | Learner result |
|---|---|---|
| 0:00–0:15 | Freeze the sample rule | Rule exists before outcomes |
| 0:15–1:15 | Learner writes first-failure notes | Sixteen notes |
| 1:15–1:40 | Learner tallies categories | Total 16 |
| 1:40–2:10 | Learner infers literals and writes config | Frozen predicate.json with exactly two strings |
| 2:10–2:40 | Learner runs the three controls | 1 / 0 / 1 with correct messages |
| 2:40–3:00 | Collect the handoff | Reconstruction or `HOLD` |

## Coaching boundary

You may point to a file or help run a supplied command. You may not supply a first-failure note, a count, a literal, or a second checker. If you cross that line, mark the work as guided practice.

## `HOLD` conditions

Use `HOLD` when fewer than eight interpretable runs exist in the sample, the supplied control is missing, the sample was chosen by outcome, the learner implements a new checker, the config does not contain exactly two distinct nonempty strings, or the learner opens outcomes before the sample rule is on disk.

## Stretch

If the learner does the stretch, confirm that the two stretch configs were frozen and the prediction was written before the public practice labels were opened. The stretch is optional.
