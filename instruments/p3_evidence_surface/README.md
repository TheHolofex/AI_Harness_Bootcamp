# NORTHWIND evidence surface

A read-only local MCP server over the Tuesday afternoon corpus
(`mission_flesh/tuesday/need/corpus/`, 104 files across 12 source types).

## Why it is a surface and not a folder

The corpus holds about 82,000 words of prose and 36,000 rows of table. Two
exports alone run to 20,928 and 9,085 rows. Nothing can read it, so a tool that
returns whole files is a tool nobody can use — and a boundary written into an
agent's instructions is a boundary that agent can ignore. This server makes both
problems structural: it exposes a query surface with hard ceilings, and it can be
started against a subset of the corpus so that what an agent may not reach is a
property of the surface it was handed.

## Tools

| Tool | Job | Ceiling |
|---|---|---|
| `list_sources` | What is here — path, type, kind, size, digest; columns and row count for tables. Never contents. | — |
| `search_sources` | Where something is said. Path, line number, matching line only. | 50 matches |
| `read_span` | Numbered lines from one file, with the file digest. | 200 lines |
| `query_table` | Slice a CSV by column: `eq ne gt gte lt lte from to in contains`. Returns the matched count and the rows. | 500 rows |
| `resolve_citation` | Does this surface serve that path, and do those words appear in it, at which line, under which digest. | — |

`resolve_citation` reports what it checked and what it did not. It proves a
citation is structurally sound. It cannot prove the source supports the claim
built on it, and it says so in its own output so nothing downstream can present
it as having made that judgment.

## Running it

```
node server.mjs --root ../../mission_flesh/tuesday/need/corpus --describe
node server.mjs --root ../../mission_flesh/tuesday/need/corpus
```

`--source-types hydrology,met` restricts the surface. `--describe` prints what is
exposed and what is withheld. `--validate-only` checks the root and exits.
`NORTHWIND_EVIDENCE_ROOT` and `NORTHWIND_SOURCE_TYPES` are the environment
equivalents.

## Tests

```
npm ci --ignore-scripts --no-audit --no-fund
npm run smoke
```

41 checks through a real client-to-server stdio session: protocol and tool
surface, route boundaries and path escapes, bounded reads, the four slices the
route decision turns on, and provenance behaviour on a real quotation, an
invented one, and a missing file.

The slice checks are the ones worth keeping. They assert that the gauge at
`SEL-04` exceeds 3.20 m on 14 of the 16 window days while the wrong station says
1 of 16; that `SLW-DECK-02` exceeds 38 C on 32 of 32 prior-season window days
while the wrong sensor says 0 of 32; that September 2026 returns nothing at all,
because the export stops at the decision date; and that observed ferry
throughput is 9.02 vehicles per hour. If a corpus edit moves any of those, the
smoke test fails rather than the exercise quietly changing its answer.

## History

This replaces `p3_mcp_evidence`, which served the retired five-file frozen-brief
track and returned whole files. That package is gone; this is the only evidence
surface the course ships.
