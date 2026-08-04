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
per reporting interval. Nothing the network measures exists anywhere else in an
authoritative form; figures appearing in reports, signals, minutes and slides are
copies, and copies age.

The reporting interval in the export is three hours at all eight sensors: eight
rows per sensor per day, at 0000, 0300, 0600, 0900, 1200, 1500, 1800 and 2100
Zulu. The sensors log more often than that; the export is a reduction of the
logged record and not the logged record itself. A row is present for every
sensor at every interval of every day the export covers, and every row carries a
value.

## 2. Columns

| Column | Type | Content | Nulls |
|---|---|---|---|
| `sensor_id` | text | Sensor identifier as in MET-2026-002, for example `SLW-DECK-02` | never |
| `asset` | text | Short position label, host asset and position together, for example `Selwyn Bridge, mid-span north lane`. Repeated from the siting record for convenience | never |
| `date` | ISO 8601 date | The day the interval falls in | never |
| `hour_utc` | text | The interval, as a four-figure Zulu clock time. Always Zulu; the export carries no local time and applies no seasonal clock change | never |
| `surface_temp_c` | decimal | The surface temperature, Celsius, to one decimal place | never |

`asset` is included as a convenience only. It is a copy of the siting record and
the siting record governs. It carries no estate asset reference: to go from a
sensor to the `W-` reference of the asset it sits on, use MET-2026-002. Where the
label and the siting record disagree, MET-2026-002 is correct and the discrepancy
should be reported.

**Those five columns are the whole export.** In particular it carries no quality
flag, no source flag, no logger identifier, no calibration reference and no
export run identifier. The Cell holds all five against every interval and none of
them is published in the file subscribers receive. What follows from that is the
most important thing in this note.

The export carries no aggregates: no daily maxima, no minima, no means, no
rolling values. Anything of that kind in circulation was computed by whoever is
circulating it, from an extract of unknown age, and its provenance should be
established before it is relied upon.

The export also carries no air temperature. It never has and it is not planned to.
The two quantities are not interchangeable and holding them in one table would
invite exactly the substitution that MET-2026-006 exists to prevent.

## 3. Every row looks the same, and they are not the same

The Cell classifies every interval it holds. Four classes are in use.

**Measured** - an instrument reading that passed the automatic range and rate
checks and has not been superseded on review. Most of the record.

**Estimated** - a value produced by the Instrumentation Cell rather than
measured, covering short interpolations across planned isolations and corrections
applied after a calibration was found outside tolerance. Estimated values are the
Cell's best figure for the interval. They are not measurements.

**Suspect** - the instrument produced a value and there is reason to doubt it.
Typical causes are a sensing face known to be fouled, a mounting known to be
disturbed, or a reading that failed a check but could not be confidently voided.

**Recovered** - a value read off the local logger on a site visit rather than
received over the telemetry link. The value is a measurement; it simply reached
the Cell by another route, and it was absent from the export until the visit.

**None of those four classes appears in the export.** There is no quality column
to carry them. A corrected value, a doubted value and a clean instrument reading
are written to the same five columns in the same format to the same one decimal
place, and nothing in the file separates them. A user who reads the export alone
is reading every row as though it were a good measurement, because that is the
only thing the file offers.

There is likewise no `missing` class in the export. Where the network obtained
nothing, the Cell does not publish an empty row: it publishes its best figure for
the interval, and the export runs unbroken. **An unbroken series is not evidence
that the instrument was working.** The periods where it was not are listed in
section 5, and section 5 is the only place a subscriber can learn about them.

Where the class of a particular value matters - and it matters most for the
values a decision turns on - request the interval from the Instrumentation Cell
and record the class with the figure.

## 4. Coverage

**The export covers the summer season only.** For each year held, the file runs
from 01 June to 30 September inclusive and no further. The network is not exported
outside that window.

Years held:

| Season | Status | Note |
|---|---|---|
| 2024 | Closed | Full network, all eight sensors |
| 2025 | Closed | Full network. Summarised qualitatively at MET-2026-010 |
| 2026 | Open | Full network. File is populated to the most recent export run and grows as the season proceeds |

Earlier seasons were held on the previous collector and are not carried in this
export. Requests for them go to the Instrumentation Cell.

Two consequences follow and both catch users out.

First, **a query spanning a season boundary returns nothing for the interval
between seasons.** There is no data for October through May in any year. This is
a coverage decision and not an outage, and the export contains no rows at all for
those periods.

Second, **the open season file stops at the last export run.** Rows exist up to
that run and not beyond. The absence of rows for a recent day means the export
has not caught up, not that the sensors failed, and the last day present in the
file is the extract date rather than the end of the season. The export does not
carry the run identifier, so establish the extract date before treating the last
row as the current state of anything.

## 5. Known losses

The periods below are the ones in which the network did not deliver a measured
reading and the Cell supplied or recovered the value instead. The export shows
none of this: the rows for these periods are present, populated and
indistinguishable from the rest of the file. This schedule is maintained
alongside the export and is the only record a subscriber holds of which values
were produced rather than measured.

| Sensor | Season | Period | Cause | How the exported value was produced |
|---|---|---|---|---|
| CP2-PAD-01 | 2024 | 11 to 12 Jun | Logger battery replacement | Cell estimate, interpolated across the period |
| SLW-DECK-01 | 2024 | 03 to 09 Sep | Surfacing patch repair, sensor isolated | Cell estimate; no measurement exists for the period |
| BRH-PAD-01 | 2024 | 26 Sep | Collector outage, single day | Measured; read off the local logger on the site visit |
| NDD-PAD-01 | 2025 | 02 to 11 Jul | Logger fault, no local record for the period | Cell estimate; no measurement exists for the period |
| BRH-PAD-01 | 2025 | 24 to 29 Aug | Duct flooding after heavy rain, cable gland ingress | Cell estimate; no measurement exists for the period |
| SLW-DECK-03 | 2025 | 14 Sep | Collector outage, recovered on visit 17 Sep | Measured; read off the local logger |
| FPT-SLIP-01 | 2026 | 07 Jun | Apron works, sensor isolated for part of the day | Cell estimate for the isolated intervals |
| SLW-DECK-01 | 2026 | 12 to 13 Jul | Logger communications fault, recovered on visit 16 Jul | Measured; read off the local logger |
| CP2-PAD-01 | 2026 | 28 Jul | Collector outage | Cell estimate, interpolated across the day |

A recovered value is a measurement and the Cell stands behind it. An estimate is
not, however carefully it was produced, and four of the nine periods above cover
a sensor for which no measurement of any kind exists. Read the sensor and the
dates in this schedule against the sensor and the dates of any figure a decision
is going to rest on.

Anyone who took an extract during one of the recovery windows holds a file whose
rows for that period have since been replaced. The current export is correct and
the older extract is not.

## 6. Changes to published data

Rows already published can change. The three causes are recovery of local logger
data after a communications outage, reflagging after review, and correction of a
period following a calibration found outside tolerance. Each change is recorded in
the export change log, which is issued with the export.

The Instrumentation Cell does not maintain a list of who holds which extract and
cannot notify individual holders that their copy has been superseded. Nor does
the export identify itself: the file carries no run identifier, so two extracts
of the same period taken months apart are indistinguishable on inspection and the
older one gives no sign of being stale. Where a figure matters, re-extract it
rather than reusing a saved one, obtain the run identifier from the Cell, and
record it with any figure that is written into another document.

## 7. Requests

Extracts for a named sensor and period, the classification of a named interval,
the run identifier for an extract, the export change log, and the calibration
certificates in force behind any period: Instrumentation Cell, Estate Works
Section, Station Halberd.
