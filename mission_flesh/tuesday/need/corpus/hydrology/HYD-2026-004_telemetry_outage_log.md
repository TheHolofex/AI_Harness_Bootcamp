# Telemetry Outage Log: Basin Gauging Network

**Issued by:** Cordell Basin Hydrometric Service, Cordell Basin Relief Consortium
**Reference:** HYD-2026-004
**Issue:** running log, extract to 31 July 2026
**Date of extract:** 01 August 2026
**Maintained by:** Brackley, J., Telemetry Technician
**Checked by:** Vance, R., Hydrometric Officer
**Distribution:** Hydrometric Service file; basin gauge series subscribers on request

**Classification:** TRAINING SYNTHETIC - EXERCISE NORTHWIND SHELF. All units, organisations, people, places and events in this document are invented.

## 1. Purpose of the log

This log records every period in which a station failed to deliver telemetered
data to the basin gauge series, together with what was done about the resulting
gap. It is the audit trail behind the **estimated** flag. Where a period appears
in this log as infilled, the corresponding rows in the series carry that flag and
were produced by the Service, not measured by the instrument.

An outage is logged when data does not reach the series. That covers instrument
failure, logger failure, power failure, communications failure and site
inaccessibility. Note that a communications outage is not always a data outage:
most stations log locally and the local record can be recovered on the next
visit, in which case the gap is backfilled with real measurements and flagged
**good**. The Infill column below records which of the two applies in each case.

## 2. Outage schedule

| Station | Start | End | Cause | Infill method | Flag applied |
|---|---|---|---|---|---|
| COR-05 | 08 Feb 2025 0415Z | 08 Feb 2025 1150Z | Modem lockup after power dip | Local logger recovered on visit 11 Feb | good |
| SEL-04 | 19 Feb 2025 2200Z | 24 Feb 2025 1030Z | Intake silted after high flow; sensor reading against silt | Correction against staff gauge readings and neighbouring stations | estimated |
| SEL-01 | 06 Mar 2025 0000Z | 06 Mar 2025 0900Z | Scheduled logger firmware update | Local logger recovered same visit | good |
| SEL-07 | 22 Mar 2025 1745Z | 27 Mar 2025 0800Z | Satellite terminal failure, unit replaced | Local logger recovered on visit 27 Mar | good |
| COR-02 | 11 Apr 2025 0300Z | 11 Apr 2025 0645Z | Network operator outage, area wide | Local logger recovered automatically on reconnection | good |
| SEL-01 | 02 May 2025 1200Z | 09 May 2025 1400Z | Battery and regulator failure, logger dead, no local record | Regression on SEL-04 and COR-02, adjusted for recession shape | estimated |
| COR-05 | 17 May 2025 0000Z | 17 May 2025 2359Z | Flume blocked with cut vegetation from estate grounds work | Period voided and reconstructed from COR-02 recession | estimated |
| SEL-04 | 03 Jun 2025 0930Z | 03 Jun 2025 1615Z | Planned works, ferry slipway apron, sensor isolated | Interpolated across a steady period | estimated |
| SEL-07 | 21 Jun 2025 0000Z | 21 Jun 2025 0600Z | Satellite pass gap, terminal reconfiguration | Local logger recovered | good |
| COR-02 | 14 Jul 2025 2130Z | 16 Jul 2025 0915Z | Debris racked on upstream pier, recorded level not representative of reach | Period voided, reconstructed from upstream and downstream stations | estimated |
| SEL-01 | 30 Jul 2025 1100Z | 30 Jul 2025 1330Z | Routine servicing, sensor out of water | Interpolated across a steady period | estimated |
| COR-05 | 12 Aug 2025 0000Z | 19 Aug 2025 1100Z | Logger card corrupt, no local record | Reconstructed from COR-02 and rainfall record; low confidence, flat period | estimated |
| SEL-04 | 04 Sep 2025 0200Z | 04 Sep 2025 1450Z | Dual SIM both failed to register, mast fault at exchange | Local logger recovered on visit 08 Sep | good |
| SEL-01 | 27 Sep 2025 0500Z | 29 Sep 2025 1200Z | Site inaccessible, mill track washed out, gate lock seized | Local logger recovered on visit 29 Sep | good |
| SEL-07 | 15 Oct 2025 0730Z | 22 Oct 2025 1600Z | Sensor cable damaged by vermin in the cut-off channel duct | Regression on COR-02, backwater term applied | estimated |
| COR-02 | 03 Nov 2025 0000Z | 03 Nov 2025 0400Z | Scheduled network maintenance | Local logger recovered | good |
| SEL-04 | 09 Nov 2025 1815Z | 13 Nov 2025 1000Z | Pier head strike by drifting timber, mounting displaced | Period voided; instrument re-levelled 13 Nov; reconstruction from SEL-01 and SEL-07 | estimated |
| COR-05 | 28 Nov 2025 2200Z | 30 Nov 2025 0930Z | Ice in flume throat | Period voided, no substitute available, flat estimate carried | estimated |
| SEL-01 | 12 Dec 2025 0000Z | 12 Dec 2025 1000Z | Antenna iced | Local logger recovered | good |
| SEL-07 | 26 Dec 2025 1300Z | 02 Jan 2026 1100Z | Terminal power fault over the holiday period, no attendance | Local logger recovered on visit 02 Jan | good |
| COR-02 | 18 Jan 2026 0345Z | 18 Jan 2026 1120Z | Modem lockup | Local logger recovered | good |
| SEL-04 | 21 Jan 2026 0000Z | 26 Jan 2026 1500Z | Intake silted after high flow | Correction against staff gauge readings taken 22, 24 and 26 Jan | estimated |
| SEL-01 | 09 Feb 2026 1600Z | 11 Feb 2026 0800Z | Logger clock drift, timestamps unusable | Period re-timed against local record and republished | estimated |
| COR-05 | 02 Mar 2026 0000Z | 02 Mar 2026 1200Z | Flume cleared of gravel, sensor isolated | Interpolated across a steady period | estimated |
| SEL-07 | 19 Mar 2026 0900Z | 19 Mar 2026 1730Z | Satellite terminal reboot | Local logger recovered | good |
| SEL-04 | 07 Apr 2026 1000Z | 07 Apr 2026 1545Z | Planned works, slipway apron drainage | Interpolated across a steady period | estimated |
| COR-02 | 25 Apr 2026 2300Z | 28 Apr 2026 0700Z | Intake silted after high flow | Correction against staff gauge and section survey | estimated |
| SEL-01 | 16 May 2026 0000Z | 16 May 2026 0800Z | Scheduled logger firmware update | Local logger recovered | good |
| COR-05 | 30 May 2026 0400Z | 06 Jun 2026 1100Z | Sensor failure, unit replaced, no local record for the period | Reconstructed from COR-02 and rainfall record; low confidence | estimated |
| SEL-04 | 22 Jun 2026 0130Z | 22 Jun 2026 0930Z | Network operator outage | Local logger recovered | good |
| SEL-07 | 11 Jul 2026 1200Z | 15 Jul 2026 1400Z | Terminal failure, replacement unit awaited from store | Local logger recovered on visit 15 Jul | good |
| COR-02 | 24 Jul 2026 0000Z | 24 Jul 2026 0330Z | Network operator outage, area wide | Local logger recovered | good |

## 3. Infill methods in use

**Local logger recovery.** The preferred outcome. The instrument was working and
recording; only the communications path failed. The recovered values are real
measurements, are inserted into the series in place of the gap, and are flagged
**good**. Users who took a copy of the series during the outage window will find
that window empty in their copy and populated in the current series; the current
series is correct.

**Interpolation across a steady period.** Used only for short planned outages
taken deliberately in settled conditions, where the level either side of the gap
is close and the record shows no event in progress. Flagged **estimated**.

**Regression on neighbouring stations.** Used for longer gaps where no local
record exists. A relationship is fitted between the failed station and one or
more working stations over a long period of concurrent record, and applied across
the gap. This works acceptably at COR-02 and SEL-01, less well at SEL-04 because
the section is mobile, and poorly at SEL-07 because of backwater influence, which
is why a backwater term is applied there and the uncertainty remains wide.

**Reconstruction from recession and rainfall.** The weakest method, used at COR-05
where there is no comparable neighbour. The catchment is small and flashy and the
reconstruction is only credible in flat, dry periods. Where it has been used in a
period containing rain, the log entry says so.

**Voiding.** Where an instrument was working but measuring the wrong thing, the
recorded values are removed before infill. Silted intakes, displaced mountings,
racked debris and ice all produce plausible looking numbers that are not river
level. A period that has been voided is more dangerous to a user than an empty
period, because the original values may have been read and passed on before the
void was applied.

## 4. Standing note

The **estimated** flag is not a comment on the quality of the Service's work. It
is a statement about the provenance of a value: measured, or produced. Any
analysis that treats an estimated run as though it were a set of independent
measurements will understate its own uncertainty. Where an estimated period
matters to a decision, ask the Service for the confidence assessment rather than
inferring one from the fact that a number is present.
