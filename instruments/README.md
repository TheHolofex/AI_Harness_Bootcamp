# Course instruments — shared, finishable kits

In-class measurement gear for **P3** and **P8**.
Not personal portable evals. Everyone on a track runs the **same** cases.

## Choose a track in P3 and keep it through P8

| Track | Folder name | Best if you… |
|---|---|---|
| **Engineering / software ops** | `engineering/` | Live in tickets, CI, PRs, services |
| **Mission / intel / ops** | `mission_ops/` | Live in reports, watches, field updates, briefs |

Pick at P3 start. **Do not switch before P8** — Friday runs the same D01–D05 suite on Home and Open for that track.

## Layout

```text
instruments/
  endpoint_case_suite/ # D01–D05 course endpoint cases used by P8
  p3_frozen_brief/   # Tue PM — dual-engine frozen demand
  p8_hold_degrade/   # Fri AM — paired Home/Open endpoint evidence
```

The endpoint suite holds the frozen cases and operator-only grader. P3 holds its frozen
brief, track corpora, and comparator. P8 holds the paired score sheet and raw-run layout.
The live website carries the student procedure.

## Continuity

| Suite ID | P8 Home | P8 Open |
|---|---|---|
| D01–D05 | Raw Terra output, saved before re-point | Raw open-endpoint output under the same run controls |

P3 uses its own frozen corpus + brief (`F-` sources, brief `BRIEF-v1`) on the **same track**. After the two clean engine runs are saved, `p3_mcp_evidence/` supplies the exact-pinned, read-only local MCP path used to build the decision's evidence packet; the live website carries the complete operating instructions.

## Facilitation

- Issue the track choice at P3 open and retain it for P8.
- Score sheets are student-owned; keys stay with staff unless pedagogy says otherwise.
- MVP uses these kits; personal portable eval stays transfer-only (post-course).

## P3 multi-agent stretch

`p3_multi_agent/` — Many Minds read-only pack. See `mission_flesh/p3/MANY_MINDS.md`.
