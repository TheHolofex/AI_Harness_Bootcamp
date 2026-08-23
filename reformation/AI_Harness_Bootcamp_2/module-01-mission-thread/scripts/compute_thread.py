#!/usr/bin/env python3
"""Reference arithmetic for the fictional Cold Lantern practice case."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone

MDT = timezone(timedelta(hours=-6), name="MDT")
UTC = timezone.utc


def local_label(value: datetime) -> str:
    return value.astimezone(MDT).strftime("%H:%M MDT")


def compute() -> dict[str, object]:
    decision = datetime(2026, 10, 6, 14, 5, tzinfo=MDT)
    deadline = datetime(2026, 10, 6, 16, 0, tzinfo=MDT)
    v5_close = datetime(2026, 10, 6, 20, 50, tzinfo=UTC)
    v6_close = datetime(2026, 10, 6, 21, 20, tzinfo=UTC)
    departure = decision + timedelta(minutes=20)
    gate = departure + timedelta(minutes=28)
    clinic = gate + timedelta(minutes=40)

    scanned_totes = 12
    released_totes = 10
    kits_per_tote = 18
    gross_kg_per_tote = 132
    rack_kg = 84
    payload_limit_kg = 1650

    released_mass = released_totes * gross_kg_per_tote
    mission_payload = released_mass + rack_kg
    all_payload = scanned_totes * gross_kg_per_tote + rack_kg

    return {
        "scanned_kits": scanned_totes * kits_per_tote,
        "usable_kits": released_totes * kits_per_tote,
        "released_mass_kg": released_mass,
        "mission_payload_kg": mission_payload,
        "payload_margin_kg": payload_limit_kg - mission_payload,
        "all_scanned_payload_kg": all_payload,
        "all_scanned_overage_kg": all_payload - payload_limit_kg,
        "v5_closure_local": local_label(v5_close),
        "earliest_departure": local_label(departure),
        "earliest_gate_arrival": local_label(gate),
        "v5_gate_margin_minutes": int((v5_close - gate.astimezone(UTC)).total_seconds() // 60),
        "clinic_arrival_if_admitted": local_label(clinic),
        "clinic_margin_if_admitted_minutes": int((deadline - clinic).total_seconds() // 60),
        "v6_closure_local": local_label(v6_close),
        "v6_gate_margin_minutes": int((v6_close - gate.astimezone(UTC)).total_seconds() // 60),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = parser.parse_args()
    values = compute()
    if args.json:
        print(json.dumps(values, indent=2, sort_keys=True))
    else:
        for key, value in values.items():
            print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
