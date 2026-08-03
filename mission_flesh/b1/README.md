# B1 · First Light example corpus

Synthetic training data. The B1 dashboard build reads all seven Markdown files in `reports/` in one pass. `DELTA_new.md` is part of the supplied corpus, not a staged update.

- 7 records
- 6 dated records
- `report_06_export_eu.md` has no DTG and must remain explicit
- Dated window: 0340Z–0600Z
- Shared ticket fields on every record: Classification, Entities, Location, Status, Severity, Summary, Related, Reporter (plus type-specific lines)
- One primary incident thread (Relay-7 / vb-07) plus a standalone high-severity EU export ticket
- Relationship edges are declared in each file’s **Related** line; the dashboard should surface them as chips and light timeline connectors — not as a force-directed graph

Build the finished dashboard at `first_light/index.html`. Do not modify the source reports.
