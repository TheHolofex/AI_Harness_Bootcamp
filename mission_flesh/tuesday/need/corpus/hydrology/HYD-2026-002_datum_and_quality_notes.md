# Datum, Quality Flags and Rating Revisions: Standing Notes for Users of the Basin Gauge Series

**Issued by:** Cordell Basin Hydrometric Service, Cordell Basin Relief Consortium
**Reference:** HYD-2026-002
**Issue:** 6
**Date of issue:** 03 March 2026
**Supersedes:** HYD-2026-002 Issue 5 (09 January 2026)
**Prepared by:** Lindqvist, H., Senior Hydrologist
**Distribution:** All subscribers to the basin gauge series

**Classification:** TRAINING SYNTHETIC - EXERCISE NORTHWIND SHELF. All units, organisations, people, places and events in this document are invented.

## 1. How station datums are set

Every station in the network reports level against a datum, and the datum is a
property of the station, not of the river. It is established as follows.

A permanent benchmark is established near the station, on stable ground or on a
structure judged unlikely to move: a weir abutment, a pier head, a bridge parapet
stud. The benchmark is levelled into the Basin Vertical Datum by closed traverse
from the nearest order network mark, and the traverse is run in both directions
and closed to tolerance before it is accepted. The sensor zero is then set by
levelling from the station benchmark, and a staff gauge or datum plate is fixed
at the section so that the electronic record can be checked against an
independent visual reading at every visit.

Benchmarks are re-levelled on a five-year cycle, and immediately if there is any
reason to think the mount has moved: scour at the abutment, settlement, vehicle
strike, structural work on the host asset. SEL-07 was re-levelled in 2021 after
the cut-off channel head was reprofiled, and its record carries a datum break at
that point. Pre-2021 and post-2021 values at that station are not directly
comparable unless the published correction has been applied; the correction is
held in the station metadata and is applied automatically in the series export.

Two points that users get wrong often enough to be worth stating plainly. The
datums are levelled independently at each station and are not offsets of one
another, so arithmetic between stations is not meaningful. And the datum is not
the bed: a station can read at the bottom of its range with water still in the
channel, and a reading near zero is a statement about the sensor, not about the
river being dry.

## 2. Quality flags

Every row in the series carries a quality flag. There are two in routine use.

**good.** The value is a telemetered instrument reading that has passed the
automatic range and rate-of-change checks and has not been superseded by review.
This is the default state of the record. A "good" flag means the instrument was
working and the value is what it measured. It does not mean the value has been
individually inspected by a hydrologist, and it does not mean the value is free
of the ordinary uncertainty of the instrument and the section.

**estimated.** The value has been produced by the Service rather than measured by
the instrument. This covers infill across telemetry outages, correction of
periods where the sensor was fouled, silted, iced or racked with debris, and
periods where the instrument was operating but the reading was demonstrably
wrong. Estimated values are produced by the methods set out in HYD-2026-004 and
are the best figure the Service can offer for that period; they are not
measurements and should not be treated as measurements in any analysis where the
difference matters. Where a run of consecutive rows is flagged estimated, treat
the whole run as a single reconstruction rather than as a set of independent
values.

A row's flag can change. Values enter the series flagged from the automatic
checks and may be reflagged on review, on a later site visit, or when a rating
revision is applied. Anyone holding a local copy of the series holds a snapshot,
and a snapshot goes stale.

## 3. Rating curve revisions

Level is measured. Flow is not: it is derived from level through a rating curve
fitted to gauged measurements at that section. The curve is a model of the
section, and the section changes.

Gaugings are made by current meter at wadeable sites and by acoustic profiler
from the boat or from a bridge at the others. The Service works to a programme of
routine gaugings through the year, with additional gaugings sought at high flow
whenever conditions and access allow, because the top end of every curve is the
part with the fewest measurements behind it and the widest uncertainty.

A curve is revised when the evidence requires it: when new gaugings depart
systematically from the current curve, after any event that visibly reworks the
control, after works on a structure at the section, or on a scheduled review. Each
curve carries a version number and a valid-from date. The mobile section at SEL-04
has needed revision most often; the artificial control at COR-02 least often.

Revisions are applied retrospectively. When a curve is revised, the derived flow
series for the affected period is recomputed and republished, which means that a
flow figure taken from the series on one date may not match the figure for the
same timestamp taken later. This is not an error and it is not a correction of a
mistake; it is the record improving as the evidence improves. Level values are not
affected by rating revisions. Users who need a stable citable figure should record
the curve version alongside the value, or cite the level rather than the derived
flow.

## 4. Standing warning

**A reading must be quoted against its station.** Every figure this Service
publishes is a measurement of one section of one river at one time, on that
station's datum, through that station's rating. Detached from its station
identifier and its timestamp it is not a weak figure or an approximate figure; it
is not a figure at all, because there is no way to recover what it was a
measurement of.

Users are asked to carry the identifier, the timestamp and the quality flag
whenever a value moves out of the series and into a report, a signal, a minute or
a decision log. Where a value has been passed on without them, go back to the
series rather than reasoning from what arrived.
