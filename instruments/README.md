# Course instruments — shared, finishable kits

In-class measurement gear for **P2**, **P3**, and **P8**.  
Not personal portable evals. Everyone on a track runs the **same** cases.

## Choose a track (once, keep it all week)

| Track | Folder name | Best if you… |
|---|---|---|
| **Engineering / software ops** | `engineering/` | Live in tickets, CI, PRs, services |
| **Mission / intel / ops** | `mission_ops/` | Live in reports, watches, field updates, briefs |

Pick at P2 start. **Do not switch mid-week** — P8 reuses the same suite IDs as P2 on your track.

## Layout

```text
instruments/
  p2_test_suite/           # Tue AM — harness before/after
  p3_frozen_brief/   # Tue PM — dual-engine frozen demand
  p8_hold_degrade/   # Fri AM — same suite IDs as P2, new endpoint
```

Each instrument has:
- student README + score sheet
- `engineering/` and `mission_ops/` full data kits
- facilitator key (answers / rubrics)

## Continuity

| Suite ID | P2 | P8 |
|---|---|---|
| D01–D05 | Baseline + after | Hold/degrade on open (or re-pointed) model |

P3 uses its own frozen corpus + brief (`F-` sources, brief `BRIEF-v1`) on the **same track**.

## Facilitation

- Issue track choice Monday PM or P2 open (2 minutes).
- Score sheets are student-owned; keys stay with staff unless pedagogy says otherwise.
- MVP uses these kits; personal portable eval stays transfer-only (post-course).

## P3 multi-agent stretch

`p3_multi_agent/` — Many Minds read-only pack. See `mission_flesh/p3/MANY_MINDS.md`.
