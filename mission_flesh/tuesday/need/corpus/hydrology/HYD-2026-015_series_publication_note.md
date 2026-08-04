# Basin Gauge Series: Publication and Revision Note

**Issued by:** Cordell Basin Hydrometric Service, Cordell Basin Relief Consortium
**Reference:** HYD-2026-015
**Issue:** 3
**Date of issue:** 22 June 2026
**Supersedes:** HYD-2026-015 Issue 2 (05 February 2026)
**Prepared by:** Vance, R., Hydrometric Officer
**Distribution:** All subscribers to the basin gauge series

**Classification:** TRAINING SYNTHETIC - EXERCISE NORTHWIND SHELF. All units, organisations, people, places and events in this document are invented.

## 1. What is published

The Service publishes one product: the basin gauge series. It contains rows for
each of the five stations in the network, each row carrying a station identifier,
a timestamp, a level, a quality flag and a row type. Everything the Service has to
say in numbers is in the series. Reports, notes and correspondence describe the
network and the methods; they do not restate values, and where a value appears in
correspondence it is a copy, not a source.

Subscribers receive the series by scheduled export. Ad hoc extracts for a named
period can be requested from the duty desk and are produced from the same store,
so an extract taken today and an extract taken next month for the same period may
differ, for the reasons set out below.

## 2. Row types: observed and forecast

Every row is one of two types, and the distinction is the single most important
thing in this note.

**Observed rows** describe the past. They are the record of what the network
measured, subject to the quality flag: **good** where the value is an instrument
measurement, **estimated** where the Service produced it to fill or correct a
gap. Observed rows are stable in the ordinary case. They change only when new
evidence arrives: a local logger is recovered after a communications outage and
real measurements replace a gap, a period is voided on review, a datum correction
is applied, or a rating revision causes derived values to be recomputed. Changes
of that kind are infrequent, are always improvements, and are logged.

**Forecast rows** describe the future. They are model output. They are not
measurements, they were never measurements, and they will never become
measurements: when the time they refer to arrives, the forecast row is replaced by
an observed row, and the forecast that stood in that slot is retained only in the
archive. A forecast row is the Service's best current estimate of what a station
will read, produced by a model with known limitations against inputs that are
themselves forecasts.

The two row types sit in the same table, in the same columns, in the same units.
This is convenient and it is also the commonest source of error among users. A
value copied out of the series without its row type carries no indication of
whether it is a measurement or a projection. Carry the row type. Where a value has
reached you without it, go back to the series.

## 3. How often forecast rows are revised

Forecast rows are regenerated on every model run. Runs are made four times daily,
nominally at 0300Z, 0900Z, 1500Z and 2100Z, with the updated rows appearing in
the series within about an hour of each run.

Every run replaces the entire forecast horizon. Forecast rows are not amended in
place and they do not accumulate: the run overwrites what the previous run
published for the same timestamps. This means a forecast row read at 0400Z and
the row for the same timestamp read at 1000Z are different products of different
runs, and they may differ substantially, particularly at the far end of the
horizon and particularly where rainfall input is uncertain.

Additional unscheduled runs are made when significant new rainfall input arrives
between scheduled runs. These are flagged in the run metadata. Users should not
assume that the forecast in front of them is the current one.

**The scheduled subscriber export does not carry the run stamp.** It is not one
of the columns in the series file. A forecast row read out of that file cannot be
dated from the row, and nothing in the file separates a row from the current run
from one that is four runs old. Where the run matters, request the extract from
the duty desk, which issues the run stamp with it, and record the two together.
Where the run stamp cannot be obtained, the forecast is undated, and it should be
quoted as undated by anyone who passes it on.

The practical rule the Service asks users to adopt: **a forecast has a shelf
life measured in hours.** A forecast figure quoted in a document written yesterday
is not wrong so much as superseded, and a decision taken today against it is being
taken against a projection that no longer exists. Read the current rows.

## 4. Skill and horizon

Forecast skill declines with lead time, and it declines faster in this basin than
in a slower catchment, for the reasons in HYD-2026-009. It also varies by station:
forecasts for the stable artificial control at COR-02 verify better than
forecasts for the mobile section at SEL-04, and forecasts for the flashy Halberd
tributary at COR-05 are the weakest in the network. No forecast row should be
treated as equally reliable across the horizon simply because it is present in
the series with the same precision as every other row.

The series does not carry an uncertainty band on forecast rows. Verification
statistics by station and lead time are held by the Service and are available on
request. Users making decisions with material consequences against forecast rows
are asked to obtain them rather than to assume.

## 5. Availability, provenance and support

The store is the authoritative copy. Local caches, spreadsheets, screenshots and
figures transcribed into other documents are snapshots, and every snapshot begins
going stale at the moment it is taken. Where a local copy is unavoidable, record
the extract time and the run stamp with it.

Planned interruptions to publication are notified to subscribers in advance.
Unplanned interruptions are notified as soon as the Service is aware of them. In
either case, absence of new rows means the series has stopped updating; it does
not mean conditions have stopped changing.

Queries, extract requests, verification statistics and corrections: Hydrometric
Service duty desk, Cordell Basin Relief Consortium.
