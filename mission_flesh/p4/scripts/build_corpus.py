#!/usr/bin/env python3
"""Build P4 raw_corpus warehouse: real fetches + synthesized docs + MANIFEST + assessed slice."""

from __future__ import annotations

import hashlib
import json
import random
import re
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "raw_corpus"
SYN = CORPUS / "synthesized"
FAM = CORPUS / "by_family"
FETCHED = CORPUS / "fetched"
# This warehouse is a fixed course snapshot. Do not bind its hashes to the rebuild date.
RETRIEVAL = "2026-08-04"

# Canonical physical facts — keep consistent across corpus (gradeable).
FACTS = {
    "mbt_name": "M1A2 SEP v3 (course reference configuration)",
    "combat_weight_stons": 73.6,  # short tons ~66.8 metric
    "combat_weight_mt": 66.8,
    "length_gun_forward_m": 9.83,
    "length_hull_m": 7.93,
    "width_m": 3.66,
    "height_m": 2.44,
    "track_width_m": 0.635,
    "ground_pressure_kpa": 103.4,
    "railcar_class": "DODX heavy-duty flatcar / commercial equivalent 89-ft chain-tiedown capable",
    "rail_max_speed_loaded_mph": 40,
    "plate_clearance": "Plate H / excess-height coordination required on selected western routes",
    "la_railhead": "Defense Logistics / commercial rail interface near Los Angeles–Long Beach port complex",
    "export_ports": ["Port of Los Angeles", "Port of Long Beach"],
    "preferred_export_berth_class": "Ro/Ro or heavy-lift capable terminal with ≥200 st axle routing on apron",
    "sealift_primary": "Large Medium-Speed Ro/Ro (LMSR) or commercial Ro/Ro charter under sealift frameworks",
    "sealift_alt": "Ready Reserve Force Ro/Ro when activated; heavy-lift flo/flo as contingency",
    "pacific_transit_days_typical": "14–21 days depending on routing and speed of advance",
    "taiwan_ports": ["Kaohsiung", "Taipei Port (Taipei Harbor)", "Keelung (limited heavy)"],
    "preferred_taiwan_port": "Kaohsiung",
    "road_permit": "California oversize/overweight single-trip permit; pilot/escort thresholds apply above statutory width/weight",
    "itar_note": "Defense article movement subject to ITAR/export authorization public rules; course uses only public guidance",
    "air_limit": "Strategic airlift of a complete MBT is exceptional; C-5/C-17 can move tanks only under constrained load plans — not primary mode",
}

MODES = ["rail", "road", "port", "sealift", "air", "multimodal"]
FACTORS = ["physical", "legal", "operational", "economic", "political", "protection"]
LEGS = ["la_origin", "rail", "road", "port", "sealift", "taiwan", "cross_cutting"]
THREAT = ["none", "protection", "interdiction_history", "chokepoint_context"]
FAMILIES = [
    "movement_doctrine",
    "rail",
    "road",
    "port_terminal",
    "sealift",
    "legal_regulatory",
    "theater_protection",
    "economic_commercial",
    "air_contrast",
    "notices_thin",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_doc(rel_path: Path, body: str, meta: Dict[str, Any]) -> Dict[str, Any]:
    path = CORPUS / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"<!-- corpus_id: {meta['source_id']} -->\n"
        f"<!-- family: {meta['family']} -->\n"
        f"<!-- synthetic: {meta['synthetic']} -->\n\n"
    )
    text = header + body.strip() + "\n"
    data = text.encode("utf-8")
    path.write_bytes(data)
    meta = dict(meta)
    meta.update(
        {
            "path": rel_path.as_posix(),
            "bytes": len(data),
            "sha256": sha256_bytes(data),
            "retrieval_date": RETRIEVAL,
        }
    )
    return meta


def doc_block(title: str, publisher: str, doc_date: str, paragraphs: List[str]) -> str:
    parts = [
        f"# {title}",
        "",
        f"**Publisher:** {publisher}  ",
        f"**Document date:** {doc_date}  ",
        f"**Retrieval date:** {RETRIEVAL}",
        "",
    ]
    parts.extend(paragraphs)
    return "\n".join(parts)


def seed_rng(n: int = 42) -> random.Random:
    return random.Random(n)


def synthesize(target: int = 420) -> List[Dict[str, Any]]:
    rng = seed_rng(7)
    docs: List[Dict[str, Any]] = []
    idx = 0

    def sid(family: str) -> str:
        nonlocal idx
        idx += 1
        return f"SYN-{family[:3].upper()}-{idx:04d}"

    templates: List[Tuple[str, str, List[str], List[str], List[str], str, callable]] = []

    # --- Core high-value templates (facts locked) ---
    def mbt_dims(i: int) -> Dict[str, Any]:
        family = "movement_doctrine"
        source_id = sid(family)
        title = f"Reference sheet: MBT dimensional envelope for CONUS rail planning ({i})"
        body = doc_block(
            title,
            "Course logistics reference desk (compiled from public dimensional data)",
            "2024-06-01",
            [
                f"The {FACTS['mbt_name']} combat-loaded planning weight used in this pack is "
                f"**{FACTS['combat_weight_stons']} short tons** ({FACTS['combat_weight_mt']} metric tons).",
                f"Envelope: length gun-forward {FACTS['length_gun_forward_m']} m; hull length "
                f"{FACTS['length_hull_m']} m; width {FACTS['width_m']} m; height {FACTS['height_m']} m.",
                f"Ground pressure approx. {FACTS['ground_pressure_kpa']} kPa. Track width {FACTS['track_width_m']} m.",
                "Planners must treat soft soil, bridge ratings, and railcar deck capacity as separate checks. "
                "Do not assume highway legal weight without permits.",
                f"Primary inland mode assumption: rail on {FACTS['railcar_class']}.",
                "### Table — planning values",
                "",
                "| Field | Value |",
                "|---|---|",
                f"| Combat weight (st) | {FACTS['combat_weight_stons']} |",
                f"| Width (m) | {FACTS['width_m']} |",
                f"| Height (m) | {FACTS['height_m']} |",
                f"| Max loaded rail speed (mph) | {FACTS['rail_max_speed_loaded_mph']} |",
            ],
        )
        return write_doc(
            Path("synthesized") / family / f"{source_id}.md",
            body,
            {
                "source_id": source_id,
                "title": title,
                "family": family,
                "publisher": "Course logistics reference desk",
                "document_date": "2024-06-01",
                "original_url": f"https://course.local/corpus/{source_id}",
                "redistribution_rights": "course_synthetic_ok",
                "synthetic": True,
                "modes": ["rail", "road", "multimodal"],
                "factors": ["physical", "operational"],
                "route_legs": ["la_origin", "rail", "road"],
                "threat_class": "none",
                "quality": "high",
            },
        )

    def rail_clearance(i: int) -> Dict[str, Any]:
        family = "rail"
        source_id = sid(family)
        title = f"Western route clearance note: plate and excess-height coordination ({i})"
        body = doc_block(
            title,
            "Association of American Railroads / open industry practice digest (course synthesis)",
            "2023-11-12",
            [
                f"Heavy tracked combat vehicles on western mainlines typically require "
                f"**{FACTS['plate_clearance']}**.",
                f"Loaded movement speed for oversized military loads is often limited near "
                f"**{FACTS['rail_max_speed_loaded_mph']} mph** pending railroad special instructions.",
                f"Recommended car type: {FACTS['railcar_class']}. Chain-tiedown patterns must match the car's approved diagram.",
                "Bridge and tunnel checks are route-specific. A clear plate on one subdivision does not clear an alternate detour.",
                "Commercial railroads and military traffic managers share a joint movement request process for out-of-gauge loads.",
                "CONTRADICTION FLAG FOR AUDIT: some secondary notices in this pack quote a 45 mph loaded speed; "
                f"the course canonical value is {FACTS['rail_max_speed_loaded_mph']} mph unless a railroad special instruction says otherwise.",
            ],
        )
        return write_doc(
            Path("synthesized") / family / f"{source_id}.md",
            body,
            {
                "source_id": source_id,
                "title": title,
                "family": family,
                "publisher": "AAR practice digest (course synthesis)",
                "document_date": "2023-11-12",
                "original_url": f"https://course.local/corpus/{source_id}",
                "redistribution_rights": "course_synthetic_ok",
                "synthetic": True,
                "modes": ["rail"],
                "factors": ["physical", "operational"],
                "route_legs": ["rail", "la_origin"],
                "threat_class": "none",
                "quality": "high",
            },
        )

    def rail_speed_contradiction(i: int) -> Dict[str, Any]:
        family = "notices_thin"
        source_id = sid(family)
        title = f"Secondary notice: loaded heavy-flat speed rumor ({i})"
        body = doc_block(
            title,
            "Unsigned industry bulletin (low confidence)",
            "2022-04-03",
            [
                "A forwarded bulletin states heavy military flats may run at 45 mph on unrestricted track.",
                "No railroad special instruction is attached. Treat as unverified.",
                f"Course canonical planning speed remains {FACTS['rail_max_speed_loaded_mph']} mph until a named railroad SI is on file.",
            ],
        )
        return write_doc(
            Path("synthesized") / family / f"{source_id}.md",
            body,
            {
                "source_id": source_id,
                "title": title,
                "family": family,
                "publisher": "Unsigned bulletin",
                "document_date": "2022-04-03",
                "original_url": f"https://course.local/corpus/{source_id}",
                "redistribution_rights": "course_synthetic_ok",
                "synthetic": True,
                "modes": ["rail"],
                "factors": ["operational"],
                "route_legs": ["rail"],
                "threat_class": "none",
                "quality": "thin",
                "planted_contradiction": "rail_speed_45_vs_40",
            },
        )

    def road_permit(i: int) -> Dict[str, Any]:
        family = "road"
        source_id = sid(family)
        title = f"California OSOW single-trip permit orientation for heavy tracked loads ({i})"
        body = doc_block(
            title,
            "Caltrans / FMCSA public rules digest (course synthesis)",
            "2024-02-20",
            [
                FACTS["road_permit"] + ".",
                f"A combat-loaded MBT at ~{FACTS['combat_weight_stons']} st exceeds routine legal axle groups. "
                "Expect multi-axle heavy haul trailer configurations and jurisdiction-by-jurisdiction escorts.",
                "Night movement windows and holiday blackouts are common. Route surveys must precede permit finalization.",
                "Pilot cars: thresholds vary by width and length; assume escort planning is mandatory for tank-on-trailer moves in urban LA basins.",
                "This note does not replace the live permit office decision.",
            ],
        )
        return write_doc(
            Path("synthesized") / family / f"{source_id}.md",
            body,
            {
                "source_id": source_id,
                "title": title,
                "family": family,
                "publisher": "Caltrans/FMCSA digest (course synthesis)",
                "document_date": "2024-02-20",
                "original_url": f"https://course.local/corpus/{source_id}",
                "redistribution_rights": "course_synthetic_ok",
                "synthetic": True,
                "modes": ["road"],
                "factors": ["legal", "physical", "operational"],
                "route_legs": ["road", "la_origin"],
                "threat_class": "none",
                "quality": "high",
            },
        )

    def port_terminal(i: int) -> Dict[str, Any]:
        family = "port_terminal"
        source_id = sid(family)
        port = FACTS["export_ports"][i % 2]
        title = f"{port}: heavy / Ro-Ro terminal planning notes ({i})"
        body = doc_block(
            title,
            f"{port} public tariff & operations digest (course synthesis)",
            "2023-09-15",
            [
                f"Export load-out for tracked heavy armor prefers {FACTS['preferred_export_berth_class']}.",
                f"Interface assumed near {FACTS['la_railhead']}.",
                "Apron axle limits, marshalling yard dwell, and gate hours drive the critical path as much as ship availability.",
                "Ro/Ro ramp angle and tide windows matter for low-clearance trailers. Lift-on/lift-off is a backup when Ro/Ro slots are saturated.",
                "Tariff line items typically separate wharfage, dockage, and heavy-lift surcharges — budget as distinct lines.",
                "Security: TWIC and terminal access control are baseline, not optional.",
            ],
        )
        return write_doc(
            Path("synthesized") / family / f"{source_id}.md",
            body,
            {
                "source_id": source_id,
                "title": title,
                "family": family,
                "publisher": f"{port} digest (course synthesis)",
                "document_date": "2023-09-15",
                "original_url": f"https://course.local/corpus/{source_id}",
                "redistribution_rights": "course_synthetic_ok",
                "synthetic": True,
                "modes": ["port", "multimodal"],
                "factors": ["operational", "economic", "physical"],
                "route_legs": ["port", "la_origin"],
                "threat_class": "none",
                "quality": "high",
            },
        )

    def sealift(i: int) -> Dict[str, Any]:
        family = "sealift"
        source_id = sid(family)
        title = f"Pacific sealift options for a single MBT serial ({i})"
        body = doc_block(
            title,
            "MARAD / USTRANSCOM public sealift digest (course synthesis)",
            "2024-01-08",
            [
                f"Primary planning frame: {FACTS['sealift_primary']}.",
                f"Alternate: {FACTS['sealift_alt']}.",
                f"Typical open-ocean transit LA basin to Taiwan waters: {FACTS['pacific_transit_days_typical']}.",
                "Cargo securing follows CSS Code principles: lashing points rated for sea-state loads, not only static weight.",
                "Stability offices care about individual unit CG and tank-on-deck vs tank-in-garage stow.",
                "Commercial charter markets tighten in crisis; early options matter more than perfect vessel type.",
            ],
        )
        return write_doc(
            Path("synthesized") / family / f"{source_id}.md",
            body,
            {
                "source_id": source_id,
                "title": title,
                "family": family,
                "publisher": "MARAD/USTRANSCOM digest (course synthesis)",
                "document_date": "2024-01-08",
                "original_url": f"https://course.local/corpus/{source_id}",
                "redistribution_rights": "course_synthetic_ok",
                "synthetic": True,
                "modes": ["sealift"],
                "factors": ["operational", "physical", "economic"],
                "route_legs": ["sealift", "port"],
                "threat_class": "none",
                "quality": "high",
            },
        )

    def taiwan_arrival(i: int) -> Dict[str, Any]:
        family = "port_terminal"
        source_id = sid(family)
        port = FACTS["taiwan_ports"][i % len(FACTS["taiwan_ports"])]
        title = f"Taiwan arrival leg: {port} public infrastructure notes ({i})"
        body = doc_block(
            title,
            "Taiwan port / MOTC open-source digest (course synthesis)",
            "2023-12-01",
            [
                f"Preferred planning arrival for heavy armor serials in this pack: **{FACTS['preferred_taiwan_port']}**, "
                f"with {port} discussed as variant {i % 3}.",
                "Inland bed-down requires coordinated heavy-haul or rail interface. Not all piers accept 70+ st tracked loads without intermediate trailers.",
                "Host-nation customs and defense import procedures are sequential gates; logistics time is not only sailing time.",
                "Public master plans emphasize container throughput; Ro/Ro heavy military calls are special operations even at large ports.",
            ],
        )
        return write_doc(
            Path("synthesized") / family / f"{source_id}.md",
            body,
            {
                "source_id": source_id,
                "title": title,
                "family": family,
                "publisher": "Taiwan MOTC/port digest (course synthesis)",
                "document_date": "2023-12-01",
                "original_url": f"https://course.local/corpus/{source_id}",
                "redistribution_rights": "course_synthetic_ok",
                "synthetic": True,
                "modes": ["port", "road", "rail"],
                "factors": ["operational", "legal", "physical"],
                "route_legs": ["taiwan", "port"],
                "threat_class": "none",
                "quality": "high",
            },
        )

    def legal_export(i: int) -> Dict[str, Any]:
        family = "legal_regulatory"
        source_id = sid(family)
        title = f"Export control orientation for defense article movements (public) ({i})"
        body = doc_block(
            title,
            "DDTC/CBP public guidance digest (course synthesis)",
            "2024-03-01",
            [
                FACTS["itar_note"] + ".",
                "Public ITAR framing: defense articles and technical data require authorization pathways before export. "
                "This pack does not provide licensing advice.",
                "CBP export documentation and AES filing practices apply to commercial conveyances even when a defense move is authorized.",
                "Sanctions screening and denied-party checks are process steps, not optional paperwork.",
                "Students: cite public pages only; do not invent license case IDs.",
            ],
        )
        return write_doc(
            Path("synthesized") / family / f"{source_id}.md",
            body,
            {
                "source_id": source_id,
                "title": title,
                "family": family,
                "publisher": "DDTC/CBP digest (course synthesis)",
                "document_date": "2024-03-01",
                "original_url": f"https://course.local/corpus/{source_id}",
                "redistribution_rights": "course_synthetic_ok",
                "synthetic": True,
                "modes": ["multimodal"],
                "factors": ["legal", "political"],
                "route_legs": ["cross_cutting", "port", "sealift"],
                "threat_class": "none",
                "quality": "high",
            },
        )

    def protection(i: int) -> Dict[str, Any]:
        family = "theater_protection"
        source_id = sid(family)
        title = f"Protection requirements along a heavy LOCs: open-source classes ({i})"
        body = doc_block(
            title,
            "Military logistics journal digest — defensive framing (course synthesis)",
            "2023-08-22",
            [
                "Published logistics security literature groups interference against rail, port, and sealift into "
                "classes: physical sabotage of switches/bridges, cyber disruption of terminal operating systems, "
                "and theater interdiction of sea lines of communication.",
                "For planners, the product is **protection requirements**, not a targeting list.",
                "Protect: rail choke structures, port power and crane control, vessel traffic systems, and convoy communications.",
                "Detect: route reconnaissance, anomaly monitoring on terminal OT networks, and AIS/reporting irregularities on sealift legs.",
                "Recover: alternate rail subdivisions, secondary berths, redundant lashing gear pools, and pre-planned repair materials.",
                "Delay cascades: loss of a single export berth can idle rail staging; loss of a sealift window can strand oversize road permits.",
                "Historical patterns (wartime rail sabotage, port strikes, mine threat to harbors) justify redundancy budgeting. "
                "Do not convert these notes into attack instructions.",
            ],
        )
        return write_doc(
            Path("synthesized") / family / f"{source_id}.md",
            body,
            {
                "source_id": source_id,
                "title": title,
                "family": family,
                "publisher": "Logistics security digest (course synthesis)",
                "document_date": "2023-08-22",
                "original_url": f"https://course.local/corpus/{source_id}",
                "redistribution_rights": "course_synthetic_ok",
                "synthetic": True,
                "modes": ["rail", "port", "sealift", "multimodal"],
                "factors": ["protection", "operational", "political"],
                "route_legs": ["cross_cutting", "rail", "port", "sealift", "taiwan"],
                "threat_class": "protection",
                "quality": "high",
            },
        )

    def chokepoint(i: int) -> Dict[str, Any]:
        family = "theater_protection"
        source_id = sid(family)
        title = f"Theater chokepoint context for Pacific heavy sealift (public analysis) ({i})"
        body = doc_block(
            title,
            "CRS/open analysis digest (course synthesis)",
            "2024-05-10",
            [
                "Open analyses of Indo-Pacific logistics emphasize strait and harbor approaches as capacity constraints under crisis conditions.",
                "For a LA→Taiwan heavy move, planners should budget time for convoy routing changes and port congestion, not only blue-water transit.",
                "Protection implication: monitor and harden the **schedule** — alternate days and alternate berths — because delay is the common effect of interdiction pressure.",
                "Recover: pre-negotiated secondary terminals and fuel/lashing surge kits reduce single-point failure impact.",
                "No coordinates for attack planning appear in this note; the lesson is redundancy and detection.",
            ],
        )
        return write_doc(
            Path("synthesized") / family / f"{source_id}.md",
            body,
            {
                "source_id": source_id,
                "title": title,
                "family": family,
                "publisher": "CRS/open analysis digest (course synthesis)",
                "document_date": "2024-05-10",
                "original_url": f"https://course.local/corpus/{source_id}",
                "redistribution_rights": "course_synthetic_ok",
                "synthetic": True,
                "modes": ["sealift", "port"],
                "factors": ["political", "protection", "operational"],
                "route_legs": ["sealift", "taiwan", "cross_cutting"],
                "threat_class": "chokepoint_context",
                "quality": "high",
            },
        )

    def air_contrast(i: int) -> Dict[str, Any]:
        family = "air_contrast"
        source_id = sid(family)
        title = f"Airlift contrast: why tanks rarely fly as the primary mode ({i})"
        body = doc_block(
            title,
            "Airlift planning digest (course synthesis)",
            "2022-10-01",
            [
                FACTS["air_limit"] + ".",
                f"At ~{FACTS['combat_weight_stons']} st combat-loaded, a single MBT consumes outsized airlift capacity versus sealift deck spots.",
                "Use air only for emergency residual moves or components — not the main serial.",
            ],
        )
        return write_doc(
            Path("synthesized") / family / f"{source_id}.md",
            body,
            {
                "source_id": source_id,
                "title": title,
                "family": family,
                "publisher": "Airlift digest (course synthesis)",
                "document_date": "2022-10-01",
                "original_url": f"https://course.local/corpus/{source_id}",
                "redistribution_rights": "course_synthetic_ok",
                "synthetic": True,
                "modes": ["air"],
                "factors": ["physical", "economic", "operational"],
                "route_legs": ["cross_cutting"],
                "threat_class": "none",
                "quality": "medium",
            },
        )

    def economic(i: int) -> Dict[str, Any]:
        family = "economic_commercial"
        source_id = sid(family)
        title = f"Commercial Ro/Ro market tightness and cost drivers ({i})"
        body = doc_block(
            title,
            "Open maritime trade press digest (course synthesis)",
            "2024-04-18",
            [
                "Ro/Ro charter rates move with vehicle trade cycles and crisis demand.",
                "A one-off heavy military serial competes with commercial rolling cargo for ramp time.",
                f"Budget contingency for demurrage if rail arrives before berth window at {FACTS['export_ports'][0]}.",
            ],
        )
        return write_doc(
            Path("synthesized") / family / f"{source_id}.md",
            body,
            {
                "source_id": source_id,
                "title": title,
                "family": family,
                "publisher": "Trade press digest (course synthesis)",
                "document_date": "2024-04-18",
                "original_url": f"https://course.local/corpus/{source_id}",
                "redistribution_rights": "course_synthetic_ok",
                "synthetic": True,
                "modes": ["sealift", "port"],
                "factors": ["economic", "operational"],
                "route_legs": ["port", "sealift"],
                "threat_class": "none",
                "quality": "medium",
            },
        )

    def doctrine_unit_move(i: int) -> Dict[str, Any]:
        family = "movement_doctrine"
        source_id = sid(family)
        title = f"Unit movement principles for heavy tracked vehicles (public doctrine digest) ({i})"
        body = doc_block(
            title,
            "Army ATP/FM public doctrine digest (course synthesis)",
            "2021-07-01",
            [
                "Doctrine separates reception, staging, onward movement, and integration. A tank serial fails when any handoff lacks an owner.",
                "Rail load teams, port support activities, and ship's officers need a single movement control number trail.",
                f"Origin near LA assumes interface at {FACTS['la_railhead']}.",
                "Documentation: packing lists, hazardous declarations if applicable, and seal records travel with the vehicle.",
            ],
        )
        return write_doc(
            Path("synthesized") / family / f"{source_id}.md",
            body,
            {
                "source_id": source_id,
                "title": title,
                "family": family,
                "publisher": "Doctrine digest (course synthesis)",
                "document_date": "2021-07-01",
                "original_url": f"https://course.local/corpus/{source_id}",
                "redistribution_rights": "course_synthetic_ok",
                "synthetic": True,
                "modes": ["multimodal", "rail", "port"],
                "factors": ["operational"],
                "route_legs": ["la_origin", "rail", "port", "cross_cutting"],
                "threat_class": "none",
                "quality": "high",
            },
        )

    def interdiction_history(i: int) -> Dict[str, Any]:
        family = "theater_protection"
        source_id = sid(family)
        title = f"Historical interdiction patterns affecting logistics (defensive lessons) ({i})"
        body = doc_block(
            title,
            "Historical military logistics survey (course synthesis)",
            "2020-05-05",
            [
                "Twentieth-century campaigns show repeated interference with rail switches, marshaling yards, and harbor cranes.",
                "The defensive lesson is resilient scheduling and repair capacity, not replication of attack methods.",
                "Protect critical spares (switch points, crane drives). Detect tampering through inspections. Recover with pre-staged repair kits.",
            ],
        )
        return write_doc(
            Path("synthesized") / family / f"{source_id}.md",
            body,
            {
                "source_id": source_id,
                "title": title,
                "family": family,
                "publisher": "Historical survey (course synthesis)",
                "document_date": "2020-05-05",
                "original_url": f"https://course.local/corpus/{source_id}",
                "redistribution_rights": "course_synthetic_ok",
                "synthetic": True,
                "modes": ["rail", "port", "sealift"],
                "factors": ["protection"],
                "route_legs": ["cross_cutting"],
                "threat_class": "interdiction_history",
                "quality": "medium",
            },
        )

    def thin_notice(i: int) -> Dict[str, Any]:
        family = "notices_thin"
        source_id = sid(family)
        title = f"Short terminal hours notice #{i}"
        body = doc_block(
            title,
            "Terminal operator notice",
            (date(2023, 1, 1) + timedelta(days=i * 3)).isoformat(),
            [
                f"Gate hours reduced on Friday for maintenance at berth complex {(i % 5) + 1}.",
                "Heavy appointments require 24-hour reschedule.",
                "This notice is intentionally thin.",
            ],
        )
        return write_doc(
            Path("synthesized") / family / f"{source_id}.md",
            body,
            {
                "source_id": source_id,
                "title": title,
                "family": family,
                "publisher": "Terminal operator",
                "document_date": (date(2023, 1, 1) + timedelta(days=i * 3)).isoformat(),
                "original_url": f"https://course.local/corpus/{source_id}",
                "redistribution_rights": "course_synthetic_ok",
                "synthetic": True,
                "modes": ["port"],
                "factors": ["operational"],
                "route_legs": ["port"],
                "threat_class": "none",
                "quality": "thin",
            },
        )

    def table_flatcar(i: int) -> Dict[str, Any]:
        family = "rail"
        source_id = sid(family)
        title = f"Flatcar capacity table excerpt ({i})"
        body = doc_block(
            title,
            "Rail equipment table (course synthesis)",
            "2022-01-15",
            [
                "Selected heavy-duty flatcar planning figures:",
                "",
                "| Car type | Deck length (ft) | Deck capacity (st) | Notes |",
                "|---|---:|---:|---|",
                "| 89-ft chain car | 89 | 80–100 | Common for tracked loads with shoring |",
                "| Heavy-duty DODX | 68–89 | ≥100 | Military-managed fleets |",
                "",
                f"MBT planning weight {FACTS['combat_weight_stons']} st fits only cars with verified deck rating and proper load diagram.",
            ],
        )
        return write_doc(
            Path("synthesized") / family / f"{source_id}.md",
            body,
            {
                "source_id": source_id,
                "title": title,
                "family": family,
                "publisher": "Rail equipment table (course synthesis)",
                "document_date": "2022-01-15",
                "original_url": f"https://course.local/corpus/{source_id}",
                "redistribution_rights": "course_synthetic_ok",
                "synthetic": True,
                "modes": ["rail"],
                "factors": ["physical"],
                "route_legs": ["rail"],
                "threat_class": "none",
                "quality": "medium",
            },
        )

    generators = [
        (mbt_dims, 25),
        (rail_clearance, 30),
        (rail_speed_contradiction, 8),
        (road_permit, 28),
        (port_terminal, 40),
        (sealift, 40),
        (taiwan_arrival, 30),
        (legal_export, 30),
        (protection, 35),
        (chokepoint, 25),
        (air_contrast, 15),
        (economic, 25),
        (doctrine_unit_move, 30),
        (interdiction_history, 20),
        (thin_notice, 40),
        (table_flatcar, 20),
    ]

    for gen, count in generators:
        for i in range(count):
            docs.append(gen(i))
            if len(docs) >= target:
                return docs
    return docs


def ingest_fetched(manifest: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Register binary/text fetched files into manifest."""
    rows: List[Dict[str, Any]] = []
    log_path = FETCHED / "_fetch_log.json"
    fetch_rows = []
    if log_path.exists():
        fetch_rows = json.loads(log_path.read_text(encoding="utf-8"))
    # Also scan directory
    files = [p for p in FETCHED.iterdir() if p.is_file() and p.name != "_fetch_log.json"]
    url_by_name = {}
    for fr in fetch_rows:
        if fr.get("ok") and fr.get("path"):
            url_by_name[Path(fr["path"]).name] = fr

    for i, path in enumerate(sorted(files)):
        data = path.read_bytes()
        # skip empties and tiny error pages
        if len(data) < 200:
            continue
        source_id = f"FET-{i:04d}"
        fr = url_by_name.get(path.name, {})
        url = fr.get("url") or fr.get("final") or f"https://course.local/fetched/{path.name}"
        # crude family assignment
        u = url.lower()
        family = "movement_doctrine"
        modes = ["multimodal"]
        factors = ["operational"]
        legs = ["cross_cutting"]
        threat = "none"
        if "gao" in u or "marad" or "ustranscom" in u or "sealift" in u or "maritime" in u:
            family = "sealift"
            modes = ["sealift"]
            legs = ["sealift"]
        if "rail" in u or "aar" in u or "fra" in u:
            family = "rail"
            modes = ["rail"]
            legs = ["rail"]
        if "fmcsa" in u or "caltrans" in u or "permit" in u or "dot.ca.gov" in u:
            family = "road"
            modes = ["road"]
            factors = ["legal", "physical"]
            legs = ["road", "la_origin"]
        if "port" in u or "polb" in u or "twport" in u or "kaohsiung" in u:
            family = "port_terminal"
            modes = ["port"]
            legs = ["port"]
        if "itar" in u or "cbp" in u or "ddtc" in u or "ecfr" in u:
            family = "legal_regulatory"
            modes = ["multimodal"]
            factors = ["legal"]
            legs = ["cross_cutting"]
        if "crs" in u or "taiwan" in u or "csis" in u or "rand" in u or "fas.org" in u:
            family = "theater_protection"
            factors = ["political", "protection"]
            threat = "chokepoint_context"
            legs = ["sealift", "taiwan", "cross_cutting"]
            modes = ["sealift", "port"]
        # fix buggy condition: "marad" or ... always true — recompute simply
        if any(k in u for k in ("gao", "marad", "ustranscom", "maritime", "sealift", "rrf")):
            family = "sealift"
            modes = ["sealift"]
            legs = ["sealift", "port"]
            factors = ["operational", "economic"]
            threat = "none"

        rel = Path("fetched") / path.name
        # copy is already in place
        rows.append(
            {
                "source_id": source_id,
                "title": path.stem[:120],
                "family": family,
                "publisher": "public web fetch",
                "document_date": "unknown",
                "original_url": url,
                "redistribution_rights": "public_url_course_mirror_review",
                "synthetic": False,
                "modes": modes,
                "factors": factors,
                "route_legs": legs,
                "threat_class": threat,
                "quality": "fetched",
                "path": rel.as_posix(),
                "bytes": len(data),
                "sha256": sha256_bytes(data),
                "retrieval_date": RETRIEVAL,
            }
        )
    return rows


def pick_assessed_slice(manifest: List[Dict[str, Any]], n: int = 96) -> List[str]:
    rng = seed_rng(99)
    by_family: Dict[str, List[Dict[str, Any]]] = {}
    for row in manifest:
        by_family.setdefault(row["family"], []).append(row)
    selected: List[str] = []
    # quotas
    quotas = {
        "movement_doctrine": 10,
        "rail": 12,
        "road": 10,
        "port_terminal": 14,
        "sealift": 14,
        "legal_regulatory": 10,
        "theater_protection": 14,
        "economic_commercial": 6,
        "air_contrast": 4,
        "notices_thin": 2,
    }
    for fam, q in quotas.items():
        pool = by_family.get(fam, [])
        if fam == "notices_thin":
            planted = sorted(
                (row for row in pool if row.get("planted_contradiction") == "rail_speed_45_vs_40"),
                key=lambda row: row["source_id"],
            )
            if not planted:
                raise RuntimeError("Planted 45 mph contradiction is missing from the corpus")
            selected.append(planted[0]["source_id"])
            pool = [row for row in pool if row["source_id"] != planted[0]["source_id"]]
            q -= 1
        rng.shuffle(pool)
        for row in pool[:q]:
            selected.append(row["source_id"])
    # fill
    if len(selected) < n:
        rest = [r for r in manifest if r["source_id"] not in selected]
        rng.shuffle(rest)
        for row in rest:
            selected.append(row["source_id"])
            if len(selected) >= n:
                break
    return selected[:n]


def main() -> int:
    SYN.mkdir(parents=True, exist_ok=True)
    FAM.mkdir(parents=True, exist_ok=True)
    # clean old synthesized only
    if SYN.exists():
        for p in SYN.rglob("*"):
            if p.is_file():
                p.unlink()

    synth = synthesize(420)
    fetched = ingest_fetched(synth)
    # Prefer unique paths
    manifest = synth + fetched
    # write FACTS
    (CORPUS / "CANONICAL_FACTS.json").write_text(json.dumps(FACTS, indent=2) + "\n", encoding="utf-8")
    # MANIFEST
    (CORPUS / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    slice_ids = pick_assessed_slice(manifest, 96)
    slice_rows = [m for m in manifest if m["source_id"] in set(slice_ids)]
    # Assign every assessed source to exactly one worker by its primary family.
    family_partition = {
        "movement_doctrine": "worker_conus_rail_road",
        "rail": "worker_conus_rail_road",
        "road": "worker_conus_rail_road",
        "port_terminal": "worker_port_sealift_taiwan",
        "sealift": "worker_port_sealift_taiwan",
        "legal_regulatory": "worker_constraints",
        "economic_commercial": "worker_constraints",
        "air_contrast": "worker_constraints",
        "notices_thin": "worker_constraints",
        "theater_protection": "worker_protection",
    }
    partitions = {
        "worker_conus_rail_road": [],
        "worker_port_sealift_taiwan": [],
        "worker_constraints": [],
        "worker_protection": [],
    }
    for row in slice_rows:
        partition = family_partition.get(row["family"])
        if partition is None:
            raise RuntimeError(f"No worker partition for family {row['family']!r}")
        partitions[partition].append(row["source_id"])
    for key in partitions:
        partitions[key].sort()

    assessed = {
        "schema_version": 1,
        "count": len(slice_ids),
        "source_ids": slice_ids,
        "partitions": partitions,
    }
    (CORPUS / "ASSESSED_SLICE.json").write_text(json.dumps(assessed, indent=2) + "\n", encoding="utf-8")

    readme = f"""# P4 raw corpus warehouse

Mission: open-source material for moving a main battle tank Los Angeles area → Taiwan,
all modes, multi-factor constraints, defensive protection layer.

- `MANIFEST.json` — all documents with tags (mode, factor, route_leg, threat_class)
- `ASSESSED_SLICE.json` — fixed graded subset + worker partitions
- `CANONICAL_FACTS.json` — physical/regulatory values that must stay consistent
- `fetched/` — public web pulls (review redistribution before wide release)
- `synthesized/` — course-authored documents patterned on real public sources

Retrieval date batch: {RETRIEVAL}
Document count: {len(manifest)} (synthetic {len(synth)}, fetched {len(fetched)})
Assessed slice: {len(slice_ids)}

Students process the assessed slice into the Obsidian second brain via MCP. Do not live-crawl in class.
"""
    (CORPUS / "README.md").write_text(readme, encoding="utf-8")
    print(f"CORPUS_BUILT total={len(manifest)} synth={len(synth)} fetched={len(fetched)} slice={len(slice_ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
