# Tuesday corpora - manifest

Two corpora. `inbound/` is the morning material, `need/` is the afternoon
material. Everything in both is invented: exercise NORTHWIND SHELF, Task Group
MERIDIAN at Station Halberd, and the organisations, people, places and events
around them. Every file carries a synthetic marker.

Paths below are relative to `mission_flesh/tuesday/`.

---

## Morning - `inbound/`

An inbound roster arriving in four formats, the records that give it meaning, the
distribution lists as they stand, material that resembles a roster and is not,
and ten days of desk traffic.

### `inbound/arrivals/` - the roster, four formats

| File | Shape | Notes |
|---|---|---|
| `arrivals_a_station_manifest.csv` | CSV, 13 people | two title lines before the header row; columns `Last Name, First Name, Pers ID, Billet Code, Report DTG, Losing Element, Gaining Desk, Remarks`; dates as `14 AUG 26` |
| `arrivals_b_desk_paste.txt` | plain text, 9 people | pasted out of a chat channel; no delimiters, no columns; one prose line per person; dates as `18 Aug` or `the 18th` |
| `arrivals_c_persys_export.json` | JSON, 11 people | records under `personnel`; fields `surname, given, person_ref, posn_id, eff_date, gaining_desk, losing_element`; dates ISO-8601 with `Z`; `posn_id` is null throughout |
| `arrivals_c_persys_export_v2.json` | JSON, 12 people | the same system after a version upgrade; the record structure, the field naming and the date encoding all changed |
| `arrivals_d_partner_roster.csv` | CSV export, structurally damaged | a partner organisation's sheet that did not survive export; the header, the row structure and the date column are all affected |

### `inbound/records/` - what capability is written down in

| File | Shape | Holds |
|---|---|---|
| `billet_catalog.csv` | CSV, 16 rows | billet code to title, desk, capability; carries a revision date |
| `qualification_register.csv` | CSV, 43 rows | person to qualification, with grant date, expiry, status (`current`/`expired`/`pending`) and awarding authority |
| `current_roster.csv` | CSV, 21 rows | who is on station, against which billet, since when, with a status column |
| `rotation_out.csv` | CSV, 3 rows | last duty day and destination for people leaving |
| `desk_directory.md` | Markdown | the six desks, the capabilities the group recognises, which desk owns which list, and where capability is recorded |

### `inbound/distros/` - the lists as they stand today

Five Markdown files, each a header block plus a `Pers ID | Name | Desk` table.
All are hand-maintained and carry a last-touched date.

`distro_signals_outage.md` · `distro_movement_serials.md` ·
`distro_medical_recall.md` · `distro_imagery_tasking.md` · `distro_all_hands.md`

### `inbound/lookalike/` - material that is not a roster

| File | Shape | What it is |
|---|---|---|
| `course_roster_relay_refresher.csv` | CSV, 18 rows | course attendance and results |
| `partner_contact_list.csv` | CSV, 10 rows | partner organisation contacts |
| `equipment_signout_log.csv` | CSV, 12 rows | stores sign-out and return |
| `thread_shift_handover.md` | Markdown | a watch handover chat log |

### `inbound/traffic/` - ten days of desk messages

Sixteen Markdown files, `msg_01_*.md` through `msg_16_*.md`, each with a
`DTG / From / To / Classification` header block and a short body. They run
12 to 18 August 2026 and carry a mixture of standing direction, amendments,
cancellations, forwarded threads, requests and routine notices.

---

## Afternoon - `need/`

One question with a decision behind it, and the corpus the group holds on file.

| File | Shape | What it is |
|---|---|---|
| `INFORMATION_NEED.md` | Markdown | the decision, the two routes, the question, and what an answer has to settle |

### `need/corpus/` - 104 files across 12 source types

About 82,000 words of prose and 39,000 rows of table. The seven machine-readable
exports hold most of the volume; the two series exports cover several stations and
several sensors across several years, so a query has to say which one it means.
`HYD-2026-001` and `MET-2026-002` describe the networks and state plainly that a
reading from one station or sensor does not transfer to another.

| Export | Rows | Columns | Coverage |
|---|---|---|---|
| `met/ESTATE_SURFACE_SENSORS_2024-2026.csv` | 23,428 | `sensor_id, asset, date, hour_utc, surface_temp_c` | 8 sensors, three-hourly, 1 Jun to 30 Sep of 2024, 2025 and 2026 |
| `hydrology/BASIN_GAUGE_SERIES_2022-2026.csv` | 9,134 | `station_id, station_name, date, gauge_m, basis, quality` | 5 stations, daily, 2022 to 2026; `basis` is observed to 31 Aug 2026 and forecast after |
| `movement/CHECKPOINT2_RETURNS_2026.csv` | 5,836 | `date, hour_utc, northbound, southbound, barrier_state` | hourly, 1 Jan to 31 Aug 2026 |
| `maintenance/ESTATE_WORK_ORDERS_2025-2026.csv` | 403 | `wo_ref, raised, asset, description, contractor, status, closed` | one row per work order, 2025 to 2026 |
| `movement/SERIAL_HISTORY_2025-2026.csv` | 102 | `serial, date, route, vehicles, departed_utc, closed_utc, heaviest_t, delay_min, remarks` | one row per serial run, both corridors |
| `movement/MOV-2026-069_ferry_crossing_log.csv` | 9 | `date, first_lift_utc, last_lift_utc, vehicles_crossed, vessel, hours_worked, vehicles_per_hour` | one row per lift day |
| `finance/FIN-2026_sep_route_cost_comparison.csv` | 11 | `line, route_amber, route_cinder, unit, note` | per-line comparison of the two routes |

**`engineering/`** - 17 Markdown

Structural and survey reporting across the whole estate, not only the two crossings. Several carry condition schedules or defect tables.

`ENG-2025-008_node_b_mast_inspection.md` · `ENG-2025-014_selwyn_bridge_inspection.md` · `ENG-2025-022_ferry_point_ramp_survey.md` · `ENG-2025-031_checkpoint2_barrier_survey.md` · `ENG-2026-001_estate_condition_summary.md` · `ENG-2026-003_selwyn_bridge_rerating.md` · `ENG-2026-005_marrow_cut_drainage_scheme.md` · `ENG-2026-007_bastion_reach_vehicle_park.md` · `ENG-2026-009_selwyn_bridge_deck_survey.md` · `ENG-2026-011_marrow_cut_defile_survey.md` · `ENG-2026-012_ferry_point_north_slip_repair.md` · `ENG-2026-014_station_halberd_gate_works.md` · `ENG-2026-016_node_d_hardstanding.md` · `ENG-2026-018_culvert_survey_amber_corridor.md` · `ENG-2026-020_node_d_fuel_point_assessment.md` · `ENG-2026-022_retaining_wall_cinder_corridor.md` · `ENG-2026-024_signage_and_marking_audit.md`

**`hydrology/`** - 7 Markdown and 1 CSV

The basin gauge series, plus the documents describing the gauging network, the datums, the quality flags and how the series is published. The narrative documents refer all figures to the series rather than repeating them.

`BASIN_GAUGE_SERIES_2022-2026.csv` · `HYD-2026-001_gauging_network_description.md` · `HYD-2026-002_datum_and_quality_notes.md` · `HYD-2026-004_telemetry_outage_log.md` · `HYD-2026-007_seasonal_outlook.md` · `HYD-2026-009_catchment_response_note.md` · `HYD-2026-012_annual_report_2025.md` · `HYD-2026-015_series_publication_note.md`

**`met/`** - 5 Markdown and 1 CSV

The estate surface temperature export, plus the network description, calibration record and format notes. The narrative documents carry no readings.

`ESTATE_SURFACE_SENSORS_2024-2026.csv` · `MET-2026-002_sensor_network_description.md` · `MET-2026-004_sensor_calibration_record.md` · `MET-2026-006_surface_vs_air_temperature_note.md` · `MET-2026-010_seasonal_summary_2025.md` · `MET-2026-013_export_format_note.md`

**`movement/`** - 12 Markdown and 3 CSV

Run reports through the year, planning running times for both corridors, standing orders, fleet and driver returns, and the serial, crossing and checkpoint logs.

`CHECKPOINT2_RETURNS_2026.csv` · `MOV-2026-012_february_run_report.md` · `MOV-2026-028_april_run_report.md` · `MOV-2026-041_may_run_report.md` · `MOV-2026-052_june_run_report.md` · `MOV-2026-058_cinder_running_times.md` · `MOV-2026-063_escort_tasking_policy.md` · `MOV-2026-069_ferry_crossing_log.csv` · `MOV-2026-071_vehicle_serviceability_return.md` · `MOV-2026-074_august_run_report.md` · `MOV-2026-077_amber_running_times.md` · `MOV-2026-079_driver_qualification_matrix.md` · `MOV-2026-081_september_serial_composition.md` · `MOV-2026-083_convoy_spacing_and_speed_orders.md` · `SERIAL_HISTORY_2025-2026.csv`

**`directives/`** - 2 Markdown

Standing direction, and the notices that amend it.

`MEM-2026-041_checkpoint2_overnight_closure.md` · `NOT-2026-118_rescission_notice.md`

**`contracts/`** - 3 Markdown

The ferry charter, the structural works framework, and the operator's promotional material.

`CON-2025-019_ardwick_structural_frame.md` · `CON-2026-002_sfs_ferry_charter.md` · `SFS_brochure_tolland_carrier.md`

**`correspondence/`** - 16 Markdown

Letters and memoranda in and out: the ferry operator, the structural contractor, the civil partner, and the detachments.

`COR-2026-006_consortium_hardstanding_terms.md` · `COR-2026-011_ferry_operator_schedule_change.md` · `COR-2026-017_ardwick_routine_progress.md` · `COR-2026-023_node_b_detachment_manning.md` · `COR-2026-029_checkpoint2_controller_strength.md` · `COR-2026-034_consortium_waste_and_water.md` · `COR-2026-039_bastion_reach_welfare.md` · `COR-2026-044_ardwick_availability_advisory.md` · `COR-2026-047_insurance_and_liability_note.md` · `COR-2026-049_ferry_operator_invoice_query.md` · `COR-2026-051_sfs_operating_limits.md` · `COR-2026-053_marrow_cut_road_closure_notice.md` · `COR-2026-055_visit_programme.md` · `COR-2026-057_consortium_liaison_memo.md` · `COR-2026-058_radio_coverage_complaint.md` · `COR-2026-060_node_d_detachment_note.md`

**`minutes/`** - 12 Markdown

Route working group across the year, estate works board, safety committee, logistics coordination, and the rotation planning conference.

`MIN-2026-01-15_route_working_group.md` · `MIN-2026-02-11_estate_works_board.md` · `MIN-2026-02-19_route_working_group.md` · `MIN-2026-03-19_route_working_group.md` · `MIN-2026-04-16_route_working_group.md` · `MIN-2026-05-13_estate_works_board.md` · `MIN-2026-05-21_route_working_group.md` · `MIN-2026-06-18_route_working_group.md` · `MIN-2026-06-24_safety_committee.md` · `MIN-2026-07-16_route_working_group.md` · `MIN-2026-07-29_logistics_coordination.md` · `MIN-2026-08-06_rotation_planning_conference.md`

**`finance/`** - 4 Markdown and 1 CSV

The route cost comparison, the works budget, and notes on the charter, the hire terms and the planning rates.

`FIN-2026-004_annual_works_budget.md` · `FIN-2026-008_hardstanding_hire_review.md` · `FIN-2026-012_ferry_charter_variation.md` · `FIN-2026-015_escort_and_fuel_rates.md` · `FIN-2026_sep_route_cost_comparison.csv`

**`maintenance/`** - 3 Markdown and 1 CSV

The estate work order export, the planned maintenance schedule, and reactive repair summaries.

`ESTATE_WORK_ORDERS_2025-2026.csv` · `MNT-2026-002_planned_maintenance_schedule.md` · `MNT-2026-009_reactive_repairs_summary.md` · `MNT-2026-013_winter_readiness_plan.md`

**`safety/`** - 5 Markdown

Near miss register, incident investigations, and routine safety bulletins.

`SAF-2026-003_near_miss_register.md` · `SAF-2026-007_fuel_spill_investigation.md` · `SAF-2026-011_driving_hours_review.md` · `SAF-2026-014_manual_handling_bulletin.md` · `SAF-2026-016_slip_and_ramp_safety_note.md`

**`open_source/`** - 11 Markdown

Local bulletins, trade press, a council notice, forum threads and a community noticeboard scrape. Quality varies sharply; several items carry no date and no byline.

`NOTE_ferry_capacity_hearsay.md` · `OS-01_selwyn_valley_bulletin_0714.md` · `OS-02_basin_bulletin_undated.md` · `OS-03_ferry_users_forum_thread.md` · `OS-04_selwyn_valley_bulletin_0512.md` · `OS-05_selwyn_valley_bulletin_0609.md` · `OS-06_selwyn_valley_bulletin_0811.md` · `OS-07_basin_haulage_trade_note.md` · `OS-08_council_planning_notice.md` · `OS-09_ferry_users_forum_thread_2.md` · `OS-10_community_noticeboard_scrape.md`

---

## Shared vocabulary

Both corpora sit in the same invented world and use the same names.

**Capabilities:** `SIGNALS` `MOVEMENT` `MEDICAL` `SUPPLY` `IMAGERY` `LIAISON`

**Places:** Station Halberd · Node B (W-04) · Node D (W-07) · Checkpoint 2
(W-19) · Ferry Point (W-22) · Bastion Reach (W-31) · Selwyn Bridge (W-41) ·
Marrow Cut · the river Selwyn

**Routes:** Route AMBER, north through Checkpoint 2, the Marrow Cut and the
Selwyn Bridge. Route CINDER, south-west through Node D and the Ferry Point
ferry.

**Organisations:** Task Group MERIDIAN · Cordell Basin Relief Consortium ·
Selwyn Ferry Services Ltd (MV Tolland Carrier) · Ardwick Structural

**Identifier forms:** people `P-nnnn` · billets `SG-n` `MV-n` `MD-n` `SP-n`
`IM-n` `LN-n` · qualifications `Q-RLY` `Q-CPX` `Q-AID` `Q-STK` `Q-FEED` `Q-LIA` ·
watch IDs `W-nn` · documents `ENG-` `MOV-` `MIN-` `COR-` `CON-` `FIN-` `HYD-`
`MET-` `MEM-` `NOT-` `OS-`
