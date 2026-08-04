# Estate Surface Sensor Export: Format, Coverage and Known Gaps

**Issued by:** Estate Works Section, Instrumentation Cell, Task Group MERIDIAN, Station Halberd
**Reference:** MET-2026-013
**Issue:** 4
**Date of issue:** 02 August 2026
**Supersedes:** MET-2026-013 Issue 3 (14 January 2026)
**Prepared by:** Okafor, B., Instrumentation Cell
**Distribution:** All recipients of the estate surface sensor export

**Classification:** TRAINING SYNTHETIC - EXERCISE NORTHWIND SHELF. All units, organisations, people, places and events in this document are invented.

## 1. The export

The estate surface sensor export is the single authoritative product of the
network described in MET-2026-002. It is a delimited text export produced from
the estate collector store, one file per season per year, with one row per sensor
per logging interval. Nothing the network measures exists anywhere else in an
authoritative form; figures appearing in reports, signals, minutes and slides are
copies, and copies age.

The logging interval is ten minutes at all eight sensors. Rows are emitted for
every interval whether or not a reading was obtained.

## 2. Columns

| Column | Type | Content | Nulls |
|---|---|---|---|
| `timestamp` | ISO 8601, Zulu | Start of the logging interval. Always Zulu; the export carries no local time and applies no seasonal clock change | never |
| `sensor_id` | text | Sensor identifier as in MET-2026-002, for example `SLW-DECK-02` | never |
| `asset_ref` | text | Estate asset reference for the host asset, for example `W-41` | never |
| `position` | text | Short position label, repeated from the siting record for convenience | never |
| `surface_temperature` | decimal | The measured surface temperature, Celsius, to one decimal place | where quality is `missing` |
| `quality` | enum | One of `good`, `estimated`, `suspect`, `missing`. See section 3 | never |
| `source` | enum | `telemetered` where the value arrived over the link, `recovered` where it was read from the local logger on a site visit | where quality is `missing` |
| `logger_id` | text | Identifier of the logger that produced the row; the three Selwyn Bridge sensors share one logger | never |
| `cal_ref` | text | Reference of the calibration in force for that sensor at that timestamp, keyed to MET-2026-004 | never |
| `export_run` | text | Identifier and time of the export run that produced the file | never |

`position` is included as a convenience only. It is a copy of the siting record
and the siting record governs. Where the two disagree, MET-2026-002 is correct
and the discrepancy should be reported.

The export carries no aggregates: no daily maxima, no minima, no means, no
rolling values. Anything of that kind in circulation was computed by whoever is
circulating it, from an extract of unknown age, and its provenance should be
established before it is relied upon.

The export also carries no air temperature. It never has and it is not planned to.
The two quantities are not interchangeable and holding them in one table would
invite exactly the substitution that MET-2026-006 exists to prevent.

## 3. Quality values

`good` - an instrument reading that passed the automatic range and rate checks and
has not been superseded on review.

`estimated` - a value produced by the Instrumentation Cell rather than measured,
covering short interpolations across planned isolations and corrections applied
after a calibration was found outside tolerance. Estimated values are the Cell's
best figure for the interval; they are not measurements.

`suspect` - the instrument produced a value, the value is present in the row, and
there is reason to doubt it. Typical causes are a sensing face known to be fouled,
a mounting known to be disturbed, or a reading that failed a check but could not
be confidently voided. A `suspect` row is the most dangerous row in the export,
because it looks exactly like a `good` row to anyone who has dropped the quality
column.

`missing` - no value. The row exists to make the gap visible. Users who filter out
`missing` rows before analysis will silently convert a gap into continuity.

## 4. Coverage

**The export covers the summer season only.** For each year held, the file runs
from 01 May to 30 September inclusive and no further. The network is not exported
outside that window.

Years held:

| Season | Status | Note |
|---|---|---|
| 2022 | Closed | Partial network only; SLW-DECK-02 and SLW-DECK-03 not yet installed. Rows for those sensors do not exist for this season |
| 2023 | Closed | Full network from 01 May |
| 2024 | Closed | Full network |
| 2025 | Closed | Full network. Summarised qualitatively at MET-2026-010 |
| 2026 | Open | Full network. File is populated to the most recent export run and grows as the season proceeds |

Two consequences follow and both catch users out.

First, **a query spanning a season boundary returns nothing for the interval
between seasons.** There is no data for October through April in any year. This is
a coverage decision, not a gap and not an outage, and the export contains no rows
at all for those periods rather than rows flagged `missing`.

Second, **the open season file is incomplete by design.** Rows exist up to the last
export run and not beyond. The absence of a row for a recent interval usually
means the export has not caught up, not that the sensor failed. Check the
`export_run` value on the last row present before concluding anything about
instrument health.

## 5. Known gaps

The following periods within the exported seasons contain `missing` or
`estimated` rows for the reasons given. This schedule is maintained alongside the
export and is the reference for the gaps in it.

| Sensor | Season | Period | Cause | Quality applied |
|---|---|---|---|---|
| SLW-DECK-02 | 2022 | Whole season | Not installed | rows absent |
| SLW-DECK-03 | 2022 | Whole season | Not installed | rows absent |
| MRW-ROAD-01 | 2023 | 08 to 15 Jul | Duct flooded, cable fault | missing |
| FPT-SLIP-01 | 2023 | 21 Aug to 02 Sep | Unit failure, replacement awaited from store | missing |
| CP2-PAD-01 | 2024 | 11 to 12 Jun | Logger battery replacement | estimated |
| SLW-DECK-01 | 2024 | 03 to 09 Sep | Surfacing patch repair, sensor isolated | missing |
| BRH-PAD-01 | 2024 | 26 Sep | Collector outage, single day, recovered on visit | good, source `recovered` |
| NDD-PAD-01 | 2025 | 02 to 11 Jul | Logger fault, no local record for the period | missing |
| BRH-PAD-01 | 2025 | 24 to 29 Aug | Duct flooding after heavy rain, cable gland ingress | missing |
| SLW-DECK-03 | 2025 | 14 Sep | Collector outage, recovered on visit 17 Sep | good, source `recovered` |
| MRW-ROAD-01 | 2026 | 19 to 21 May | Traffic control works at the narrows, sensor isolated | estimated |
| FPT-SLIP-01 | 2026 | 07 Jun | Apron works, sensor isolated for part of the day | estimated |
| SLW-DECK-01 | 2026 | 12 to 13 Jul | Logger communications fault, recovered on visit 16 Jul | good, source `recovered` |
| CP2-PAD-01 | 2026 | 28 Jul | Collector outage | missing |

Note that a `recovered` source is not a gap in the data even though it was a gap
in the export at the time. Anyone who took an extract during one of those windows
holds a file with rows absent that are now present. The current export is correct
and the older extract is not.

## 6. Changes to published data

Rows already published can change. The three causes are recovery of local logger
data after a communications outage, reflagging after review, and correction of a
period following a calibration found outside tolerance. Each change is recorded in
the export change log, which is issued with the export.

The Instrumentation Cell does not maintain a list of who holds which extract and
cannot notify individual holders that their copy has been superseded. Where a
figure matters, re-extract it rather than reusing a saved one, and record the
`export_run` value with any figure that is written into another document.

## 7. Requests

Extracts for a named sensor and period, the export change log, and the
calibration certificates behind the `cal_ref` values: Instrumentation Cell, Estate
Works Section, Station Halberd.
