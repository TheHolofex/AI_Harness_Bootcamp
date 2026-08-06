#!/usr/bin/env python3
"""Populate thin vault_seed and a complete reference vault that passes verify_brain."""

from __future__ import annotations

import json
import shutil
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "vault_seed"
REF = ROOT / "reference_fixtures" / "complete_vault"
CORPUS = ROOT / "raw_corpus"
TOOLS_SRC = SEED / "tools"

FACTS = json.loads((CORPUS / "CANONICAL_FACTS.json").read_text(encoding="utf-8"))
MANIFEST = {m["source_id"]: m for m in json.loads((CORPUS / "MANIFEST.json").read_text(encoding="utf-8"))}
SLICE = json.loads((CORPUS / "ASSESSED_SLICE.json").read_text(encoding="utf-8"))


def w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def pick_source(preferred_families: list[str]) -> dict:
    for fam in preferred_families:
        for sid in SLICE["source_ids"]:
            m = MANIFEST[sid]
            if m["family"] == fam:
                return m
    sid = SLICE["source_ids"][0]
    return MANIFEST[sid]


def source_yaml(m: dict, claim: str, excerpt: str) -> str:
    return textwrap.dedent(
        f"""\
        - source_id: "{m['source_id']}"
          raw_path: "mission_flesh/p4/raw_corpus/{m['path']}"
          sha256: "{m['sha256']}"
          original_url: "{m.get('original_url','')}"
          publisher: "{m.get('publisher','unknown')}"
          document_date: "{m.get('document_date','unknown')}"
          retrieval_date: "{m.get('retrieval_date','')}"
          locator: "body"
          excerpt: "{excerpt}"
          claim: "{claim}"
          confidence: "high"
          uncertainty: "Course pack values; confirm against live railroad/port instructions before operations."
          contradictions: "See thin notices that claim 45 mph loaded rail speed; canonical is {FACTS['rail_max_speed_loaded_mph']} mph."
        """
    )


def content_note(
    rel: str,
    note_id: str,
    title: str,
    route_legs: list[str],
    modes: list[str],
    factors: list[str],
    threat_class: str,
    body: str,
    source_meta: dict,
    claim: str,
    excerpt: str,
) -> str:
    fm = textwrap.dedent(
        f"""\
        ---
        note_id: "{note_id}"
        title: "{title}"
        route_legs: {json.dumps(route_legs)}
        modes: {json.dumps(modes)}
        factors: {json.dumps(factors)}
        threat_class: "{threat_class}"
        confidence: "high"
        sources:
        """
    )
    return fm + source_yaml(source_meta, claim, excerpt) + "---\n\n" + body.strip() + "\n"


def write_seed() -> None:
    # Clear old harness files that are MERIDIAN-specific
    for p in (SEED / "Harness").glob("*"):
        if p.is_file():
            p.unlink()
    for p in [SEED / "AGENTS.md", SEED / "MOC.md"]:
        if p.exists():
            p.unlink()
    agents_dir = SEED / ".opencode" / "agents"
    if agents_dir.exists():
        for p in agents_dir.glob("*.md"):
            p.unlink()

    w(
        SEED / "AGENTS.md",
        """
# Second brain — project instructions

- Audience: logistics planner building a cited LA→Taiwan heavy-armor movement brain
- Evidence rule: every decision-driving claim cites a raw_corpus source with excerpt and sha256
- Write path: director writes vault notes only through Obsidian MCP (ask-gated). Never edit the vault as ordinary files from OpenCode.
- Workers: read assigned assessed-slice paths only; no web; no MCP; no vault writes
- Threat notes end in protect / detect / recover implications. No targeting studies.
- Never invent license case IDs, coordinates for attack, or stepwise sabotage instructions
- Stop when coverage quotas are met, cold retrieval answers exist, and human audit is recorded
""",
    )

    hubs = {
        "MOC.md": """# Map of contents

Hub index for the LA→Taiwan heavy-armor second brain.

- [[Notes/Modes]]
- [[Notes/Nodes]]
- [[Notes/Constraints]]
- [[Notes/Threats]]
- [[Notes/Sources]]
- [[Notes/Route/Spine]]
- [[Mission_Brief]] (filled at closeout)
- [[Retrieval/Answers]] (cold session)
""",
        "Notes/Modes.md": """# Modes

Movement modes for the serial. Link content notes here as they land.

- Rail
- Road / heavy haul
- Port / terminal
- Sealift
- Air (contrast only)
""",
        "Notes/Nodes.md": """# Nodes

Geographic and facility nodes along the route spine.

- Los Angeles–Long Beach origin complex
- Inland rail interface
- Export berth
- Pacific sealift leg
- Taiwan port of entry and bed-down
""",
        "Notes/Constraints.md": """# Constraints

Cross-cutting limits: physical envelope, permits, export controls, commercial capacity, time-distance.
""",
        "Notes/Threats.md": """# Threats (defensive)

Protection requirements and published vulnerability classes. Notes here must end in protect / detect / recover language.
""",
        "Notes/Sources.md": """# Sources

Index of raw_corpus source IDs admitted into the brain. Prefer MANIFEST source_id as the stable key.
""",
        "Notes/Route/Spine.md": """# Route spine

LA origin → rail / road → export port → sealift → Taiwan arrival → bed-down.

Link each leg note as workers return bundles.
""",
        "templates/NOTE_TEMPLATE.md": """---
note_id: "NOTE-000"
title: ""
route_legs: []
modes: []
factors: []
threat_class: "none"
confidence: "medium"
sources:
  - source_id: ""
    raw_path: ""
    sha256: ""
    original_url: ""
    publisher: ""
    document_date: ""
    retrieval_date: ""
    locator: ""
    excerpt: ""
    claim: ""
    confidence: "medium"
    uncertainty: ""
    contradictions: ""
---

# Title

Body with [[wikilinks]] to hubs.
""",
        "Harness/HARNESS_CARD.md": """# Harness card — second brain

## Goal
Build a cited Obsidian second brain for moving a main battle tank from the Los Angeles area to Taiwan, then answer graded queries from the brain only.

## Control flow
MCP smoke → assessed-slice worker dispatch → director MCP merge → structure → cold retrieval → human audit → baseline freeze.

## Budgets
- Four workers on four assessed-slice partitions
- Director-only MCP writes (ask)
- No live web on the graded path

## Terminal reasons
SUCCESS · NEEDS_EVIDENCE · BUDGET_STOP · HUMAN_HAND_BACK
""",
        "Harness/RUN_STATE.md": """# Run state

- Phase: SEED
- Status: READY
- Next permitted action: vault identity smoke + OpenCode MCP registration
""",
        "Harness/HANDOFF_RECEIPT.md": """# Handoff receipt

- Status: SEED (not a completed run)
- Replace this file at closeout with accepted artifacts and residual risk.
""",
        "Evidence/PERMISSIONS.example.json": json.dumps(
            {
                "director": {
                    "mcp": {
                        "read": "allow",
                        "write": "ask",
                        "delete": "deny",
                        "move": "deny",
                        "copy": "deny",
                        "active_file": "deny",
                        "command": "deny",
                    },
                    "filesystem_vault": "deny",
                    "web": "deny",
                },
                "researchers": {
                    "mcp": "deny",
                    "web": "deny",
                    "raw_corpus": "read",
                    "filesystem_write": "deny",
                },
                "retriever": {
                    "project": "Documents\\p4-cold-query",
                    "mcp": {"read": "allow", "write": "ask"},
                    "filesystem": "deny",
                    "web": "deny",
                },
            },
            indent=2,
        ),
        "Evidence/MCP_RECEIPTS.jsonl": "",
        "Evidence/MCP_RECEIPTS.example.jsonl": json.dumps(
            {
                "ts": "2026-08-05T00:00:00Z",
                "agent": "director",
                "tool": "obsidian_vault_write",
                "action": "write",
                "path": "Notes/Example.md",
                "ok": True,
            }
        ),
        ".opencode/agents/director.md": """---
description: P4 director with ask-gated Obsidian writes
mode: primary
permission:
  "*": deny
  external_directory: deny
  read: allow
  glob: allow
  grep: allow
  edit:
    "*": deny
    "operator/evidence/**": allow
  task:
    "*": deny
    "worker_*": allow
  obsidian_vault_list: allow
  obsidian_vault_read: allow
  obsidian_vault_get_document_map: allow
  obsidian_search_query: allow
  obsidian_search_simple: allow
  obsidian_tag_list: allow
  obsidian_vault_write: ask
  obsidian_vault_append: ask
  obsidian_vault_patch: ask
---

# Director agent

Merge worker bundles into the Obsidian vault through MCP only.
Save project evidence under operator/evidence. Never edit the external vault with filesystem tools.
Require the full citation schema on every note.
""",
        ".opencode/agents/retriever.md": """---
description: P4 cold retriever with Obsidian MCP only
mode: primary
permission:
  "*": deny
  external_directory: deny
  obsidian_vault_list: allow
  obsidian_vault_read: allow
  obsidian_vault_get_document_map: allow
  obsidian_search_query: allow
  obsidian_search_simple: allow
  obsidian_tag_list: allow
  obsidian_vault_write: ask
  obsidian_vault_append: ask
  obsidian_vault_patch: ask
---

# Cold retriever

Read the second brain through Obsidian MCP. Do not read the course repository or raw corpus.
Ask before you write the approved retrieval answer into the vault.
""",
        "README.md": """# P4 vault seed (thin)

Run `mission_flesh\\p4\\scripts\\Start-P4.ps1 Setup` to create `%USERPROFILE%\\Vaults\\p4-vault`, then use Obsidian's **Open folder as vault** command on that exact folder.
Do not copy this tree by hand: the setup script deliberately excludes `.opencode` and `.obsidian` state. The OpenCode project is the course repo, never the vault.

Graded work fills Notes/, Mission_Brief.md, Retrieval/Answers.md, Audit.md, Evidence/, and Harness closeout files.
""",
    }
    for rel, text in hubs.items():
        w(SEED / rel, text)

    for partition, source_ids in SLICE["partitions"].items():
        permission_lines = [
            "---",
            f"description: P4 researcher for {partition}",
            "mode: subagent",
            "permission:",
            '  "*": deny',
            "  external_directory: deny",
            "  read:",
            '    "*": deny',
            '    "operator/evidence/p4_run_contract.md": allow',
        ]
        for source_id in source_ids:
            raw_path = f"mission_flesh/p4/raw_corpus/{MANIFEST[source_id]['path']}"
            permission_lines.append(f"    {json.dumps(raw_path)}: allow")
        permission_lines.extend(
            [
                "---",
                "",
                f"# {partition}",
                "",
                "Read only the allowed assessed-slice source paths.",
                "Return structured JSON to the director.",
                "Do not use the web, MCP, shell, or filesystem write tools.",
            ]
        )
        w(agents_dir / f"{partition}.md", "\n".join(permission_lines))

    # controller briefs live beside seed
    controller = ROOT / "controller"
    w(
        controller / "RESEARCH_BRIEF.md",
        f"""
# Research brief — LA→Taiwan MBT move

Mission question: what does open-source evidence say about moving a main battle tank from the Los Angeles area to Taiwan end-to-end, and what defensive protection requirements matter along that path?

Canonical facts (do not drift):
- Combat weight: {FACTS['combat_weight_stons']} short tons
- Width: {FACTS['width_m']} m · Height: {FACTS['height_m']} m
- Loaded rail planning speed: {FACTS['rail_max_speed_loaded_mph']} mph
- Preferred Taiwan port: {FACTS['preferred_taiwan_port']}

Workers process only IDs in `raw_corpus/ASSESSED_SLICE.json` partitions.
""",
    )
    w(
        controller / "WORKER_PARTITIONS.md",
        """
# Worker partitions

See `mission_flesh/p4/raw_corpus/ASSESSED_SLICE.json` → `partitions`:

1. worker_conus_rail_road
2. worker_port_sealift_taiwan
3. worker_constraints
4. worker_protection
""",
    )
    w(
        controller / "opencode.p4.json",
        json.dumps(
            {
                "$schema": "https://opencode.ai/config.json",
                "mcp": {
                    "obsidian": {
                        "type": "remote",
                        "url": "http://127.0.0.1:27123/mcp/",
                        "enabled": True,
                        "oauth": False,
                        "headers": {
                            "Authorization": "Bearer {env:OBSIDIAN_REST_API_KEY}"
                        },
                    }
                },
            },
            indent=2,
        ),
    )
    w(
        controller / "NOTE_SCHEMA.md",
        (ROOT / "docs" / "VAULT_CONTRACT.md").read_text(encoding="utf-8")
        if (ROOT / "docs" / "VAULT_CONTRACT.md").exists()
        else "See mission_flesh/p4/docs/VAULT_CONTRACT.md",
    )


def build_reference() -> None:
    if REF.exists():
        shutil.rmtree(REF)
    shutil.copytree(SEED, REF, ignore=shutil.ignore_patterns("*.example.json", "*.example.jsonl", "README.md"))
    # tools already in seed
    # pick sources
    s_mbt = pick_source(["movement_doctrine"])
    s_rail = pick_source(["rail"])
    s_road = pick_source(["road"])
    s_port = pick_source(["port_terminal"])
    s_sea = pick_source(["sealift"])
    s_legal = pick_source(["legal_regulatory"])
    s_prot = pick_source(["theater_protection"])
    s_tw = pick_source(["port_terminal"])

    notes = [
        (
            "Notes/Content/MBT_Envelope.md",
            content_note(
                "Notes/Content/MBT_Envelope.md",
                "NOTE-MBT-001",
                "MBT dimensional envelope",
                ["la_origin", "rail", "road"],
                ["rail", "road", "multimodal"],
                ["physical", "operational"],
                "none",
                f"""# MBT dimensional envelope

Planning weight **{FACTS['combat_weight_stons']} short tons** ({FACTS['combat_weight_mt']} t).
Width {FACTS['width_m']} m; height {FACTS['height_m']} m.

See [[Notes/Modes]] and [[Notes/Route/Spine]].
""",
                s_mbt,
                f"Combat-loaded planning weight is {FACTS['combat_weight_stons']} short tons.",
                f"combat-loaded planning weight used in this pack is {FACTS['combat_weight_stons']} short tons",
            ),
        ),
        (
            "Notes/Content/Rail_Clearance.md",
            content_note(
                "Notes/Content/Rail_Clearance.md",
                "NOTE-RAIL-001",
                "Western rail clearance and speed",
                ["rail", "la_origin"],
                ["rail"],
                ["physical", "operational"],
                "none",
                f"""# Western rail clearance and speed

{FACTS['plate_clearance']}. Loaded planning speed **{FACTS['rail_max_speed_loaded_mph']} mph**.
Car type: {FACTS['railcar_class']}.

Linked from [[Notes/Modes]] and [[Notes/Constraints]].
""",
                s_rail,
                f"Loaded rail planning speed is {FACTS['rail_max_speed_loaded_mph']} mph pending special instructions.",
                f"Loaded movement speed often limited near {FACTS['rail_max_speed_loaded_mph']} mph pending railroad special instructions",
            ),
        ),
        (
            "Notes/Content/Road_OSOW.md",
            content_note(
                "Notes/Content/Road_OSOW.md",
                "NOTE-ROAD-001",
                "California OSOW permits for heavy tracked loads",
                ["road", "la_origin"],
                ["road"],
                ["legal", "physical", "operational"],
                "none",
                f"""# California OSOW permits

{FACTS['road_permit']}.

Hub: [[Notes/Constraints]].
""",
                s_road,
                "OSOW single-trip permits and escorts are required for tank-on-trailer moves in the LA basin.",
                "California oversize/overweight single-trip permit; pilot/escort thresholds apply above statutory width/weight",
            ),
        ),
        (
            "Notes/Content/Export_Port.md",
            content_note(
                "Notes/Content/Export_Port.md",
                "NOTE-PORT-001",
                "LA/LB export terminal heavy/Ro-Ro notes",
                ["port", "la_origin"],
                ["port", "multimodal"],
                ["operational", "economic", "physical"],
                "none",
                f"""# Export terminal

Preferred berth class: {FACTS['preferred_export_berth_class']}.
Ports: {', '.join(FACTS['export_ports'])}.

[[Notes/Nodes]] · [[Notes/Route/Spine]]
""",
                s_port,
                "Heavy armor export prefers Ro/Ro or heavy-lift capable terminals at LA/LB.",
                "Export load-out prefers Ro/Ro or heavy-lift capable terminal with heavy axle routing on apron",
            ),
        ),
        (
            "Notes/Content/Sealift_Options.md",
            content_note(
                "Notes/Content/Sealift_Options.md",
                "NOTE-SEA-001",
                "Pacific sealift options",
                ["sealift", "port"],
                ["sealift"],
                ["operational", "physical", "economic"],
                "none",
                f"""# Pacific sealift

Primary: {FACTS['sealift_primary']}.
Transit: {FACTS['pacific_transit_days_typical']}.

[[Notes/Modes]] · [[Notes/Route/Spine]]
""",
                s_sea,
                "Primary sealift frame is LMSR or commercial Ro/Ro under sealift frameworks.",
                "Primary planning frame: Large Medium-Speed Ro/Ro (LMSR) or commercial Ro/Ro charter",
            ),
        ),
        (
            "Notes/Content/Taiwan_Arrival.md",
            content_note(
                "Notes/Content/Taiwan_Arrival.md",
                "NOTE-TW-001",
                "Taiwan arrival and bed-down",
                ["taiwan", "port"],
                ["port", "road"],
                ["operational", "legal", "physical"],
                "none",
                f"""# Taiwan arrival

Preferred port: **{FACTS['preferred_taiwan_port']}**.
Also discussed: {', '.join(FACTS['taiwan_ports'])}.

[[Notes/Nodes]] · [[Notes/Route/Spine]]
""",
                s_tw,
                f"Preferred planning arrival port is {FACTS['preferred_taiwan_port']}.",
                f"Preferred planning arrival for heavy armor serials: {FACTS['preferred_taiwan_port']} with public infrastructure notes",
            ),
        ),
        (
            "Notes/Content/Export_Controls.md",
            content_note(
                "Notes/Content/Export_Controls.md",
                "NOTE-LEG-001",
                "Export control orientation (public)",
                ["cross_cutting", "port", "sealift"],
                ["multimodal"],
                ["legal", "political"],
                "none",
                f"""# Export controls

{FACTS['itar_note']}.

[[Notes/Constraints]]
""",
                s_legal,
                "Defense article movements require public ITAR/export authorization pathways before export.",
                "Defense article movement subject to ITAR/export authorization public rules; course uses only public guidance",
            ),
        ),
        (
            "Notes/Content/Protection_LOC.md",
            content_note(
                "Notes/Content/Protection_LOC.md",
                "NOTE-THR-001",
                "Protection requirements on heavy LOCs",
                ["cross_cutting", "rail", "port", "sealift", "taiwan"],
                ["rail", "port", "sealift", "multimodal"],
                ["protection", "operational", "political"],
                "protection",
                """# Protection requirements on heavy LOCs

Open-source logistics security classes: physical interference with rail/port infrastructure,
cyber disruption of terminal systems, and theater pressure on sealift schedules.

**Protect** choke structures, power, and vessel traffic systems.
**Detect** route and OT anomalies.
**Recover** with alternate berths, rail subdivisions, and repair kits.

Delay cascades when a berth or sealift window fails idle the inland chain.

[[Notes/Threats]] · [[Notes/Route/Spine]]

End each route assessment with actions to **protect**, **detect**, and **recover**.
""",
                s_prot,
                "Planners should budget protection and redundancy rather than target lists.",
                "For planners, the product is protection requirements, not a targeting list",
            ),
        ),
        (
            "Notes/Content/Air_Contrast.md",
            content_note(
                "Notes/Content/Air_Contrast.md",
                "NOTE-AIR-001",
                "Airlift is not the primary mode",
                ["cross_cutting"],
                ["air"],
                ["physical", "economic", "operational"],
                "none",
                f"""# Airlift contrast

{FACTS['air_limit']}.

[[Notes/Modes]]
""",
                pick_source(["air_contrast", "movement_doctrine"]),
                "Complete MBT airlift is exceptional and not the primary mode.",
                "Strategic airlift of a complete MBT is exceptional and not primary mode for the serial",
            ),
        ),
    ]

    for rel, text in notes:
        w(REF / rel, text)

    # Update hubs with links
    w(
        REF / "MOC.md",
        """# Map of contents

- [[Notes/Modes]] · [[Notes/Nodes]] · [[Notes/Constraints]] · [[Notes/Threats]] · [[Notes/Sources]]
- [[Notes/Route/Spine]]
- Content: [[Notes/Content/MBT_Envelope]] · [[Notes/Content/Rail_Clearance]] · [[Notes/Content/Road_OSOW]] · [[Notes/Content/Export_Port]] · [[Notes/Content/Sealift_Options]] · [[Notes/Content/Taiwan_Arrival]] · [[Notes/Content/Export_Controls]] · [[Notes/Content/Protection_LOC]] · [[Notes/Content/Air_Contrast]]
- [[Mission_Brief]] · [[Retrieval/Answers]] · [[Audit]]
""",
    )
    w(
        REF / "Notes/Modes.md",
        """# Modes

- Rail — [[Notes/Content/Rail_Clearance]]
- Road — [[Notes/Content/Road_OSOW]]
- Port — [[Notes/Content/Export_Port]] · [[Notes/Content/Taiwan_Arrival]]
- Sealift — [[Notes/Content/Sealift_Options]]
- Air contrast — [[Notes/Content/Air_Contrast]]
- Envelope — [[Notes/Content/MBT_Envelope]]
""",
    )
    w(
        REF / "Notes/Nodes.md",
        """# Nodes

- LA/LB complex — [[Notes/Content/Export_Port]]
- Rail interface — [[Notes/Content/Rail_Clearance]]
- Taiwan ports — [[Notes/Content/Taiwan_Arrival]]
""",
    )
    w(
        REF / "Notes/Constraints.md",
        """# Constraints

- Physical envelope — [[Notes/Content/MBT_Envelope]]
- Permits — [[Notes/Content/Road_OSOW]]
- Export law — [[Notes/Content/Export_Controls]]
""",
    )
    w(
        REF / "Notes/Threats.md",
        """# Threats (defensive)

- [[Notes/Content/Protection_LOC]]
""",
    )
    w(
        REF / "Notes/Sources.md",
        """# Sources

Admitted source IDs include those cited in Notes/Content/* front matter. Stable keys match raw_corpus MANIFEST source_id values.
""",
    )
    w(
        REF / "Notes/Route/Spine.md",
        """# Route spine

1. LA origin / rail-road — [[Notes/Content/MBT_Envelope]] · [[Notes/Content/Rail_Clearance]] · [[Notes/Content/Road_OSOW]]
2. Export port — [[Notes/Content/Export_Port]]
3. Sealift — [[Notes/Content/Sealift_Options]]
4. Taiwan — [[Notes/Content/Taiwan_Arrival]]
5. Protection overlay — [[Notes/Content/Protection_LOC]]
""",
    )

    w(
        REF / "Mission_Brief.md",
        f"""# Mission brief — LA→Taiwan MBT logistics brain

## Bottom line
A combat-loaded MBT at **{FACTS['combat_weight_stons']} st** moves primarily by **rail + Ro/Ro sealift**, not air. Export through the LA/LB complex and arrival preference **{FACTS['preferred_taiwan_port']}**.

## Mode picture
- Envelope and rail: [[Notes/Content/MBT_Envelope]] · [[Notes/Content/Rail_Clearance]]
- Road permits: [[Notes/Content/Road_OSOW]]
- Port and sea: [[Notes/Content/Export_Port]] · [[Notes/Content/Sealift_Options]]
- Arrival: [[Notes/Content/Taiwan_Arrival]]

## Constraints and protection
- Export controls: [[Notes/Content/Export_Controls]]
- Defensive protection requirements: [[Notes/Content/Protection_LOC]]

## Residual risk
Thin notices that claim 45 mph loaded rail speed conflict with the canonical **{FACTS['rail_max_speed_loaded_mph']} mph** planning value — treat as audit catch.
""",
    )

    w(
        REF / "Retrieval/Answers.md",
        f"""# Cold retrieval answers

## Q1 — Rail constraints out of LA
Plate/excess-height coordination and **{FACTS['rail_max_speed_loaded_mph']} mph** loaded planning speed apply; use heavy-duty flatcars. Sources: [[Notes/Content/Rail_Clearance]] · [[Notes/Content/MBT_Envelope]].

## Q2 — Sealift options
Primary frame is LMSR or commercial Ro/Ro; RRF/heavy-lift as alternate. Transit often {FACTS['pacific_transit_days_typical']}. [[Notes/Content/Sealift_Options]]

## Q3 — Protection requirements at chokepoints
Protect berths, power, VTS; detect OT/route anomalies; recover via alternate berths and repair kits. [[Notes/Content/Protection_LOC]]

## Q4 — Delay cascades if a node fails
Lost export berth idles rail staging; lost sealift window strands OSOW road permits. [[Notes/Content/Protection_LOC]] · [[Notes/Content/Export_Port]] · [[Notes/Content/Road_OSOW]]
""",
    )

    w(
        REF / "Audit.md",
        f"""# Human audit sample

| Note | Disposition | Finding |
|---|---|---|
| Notes/Content/Rail_Clearance.md | support | Matches canonical {FACTS['rail_max_speed_loaded_mph']} mph and plate guidance |
| Thin corpus notices claiming 45 mph | reject | Contradicts canonical speed; do not promote into spine |
| Notes/Content/Protection_LOC.md | support | Ends in protect/detect/recover language |

One repair cycle: removed any implied targeting language from threat notes before freeze.
""",
    )

    perms = {
        "director": {
            "mcp": {
                "read": "allow",
                "write": "ask",
                "delete": "deny",
                "move": "deny",
                "copy": "deny",
                "active_file": "deny",
                "command": "deny",
            },
            "filesystem_vault": "deny",
            "web": "deny",
        },
        "researchers": {
            "mcp": "deny",
            "web": "deny",
            "raw_corpus": "read",
            "filesystem_write": "deny",
        },
        "retriever": {
            "project": "Documents\\p4-cold-query",
            "mcp": {"read": "allow", "write": "ask"},
            "filesystem": "deny",
            "web": "deny",
        },
    }
    w(REF / "Evidence/PERMISSIONS.json", json.dumps(perms, indent=2))
    receipts = [
        {
            "ts": "2026-08-05T12:00:00Z",
            "agent": "director",
            "tool": "obsidian_vault_write",
            "action": "write",
            "path": "Notes/Content/MBT_Envelope.md",
            "ok": True,
        },
        {
            "ts": "2026-08-05T12:05:00Z",
            "agent": "director",
            "tool": "obsidian_vault_append",
            "action": "append",
            "path": "MOC.md",
            "ok": True,
        },
    ]
    (REF / "Evidence/MCP_RECEIPTS.jsonl").write_text(
        "\n".join(json.dumps(r) for r in receipts) + "\n", encoding="utf-8"
    )

    w(
        REF / "Harness/RUN_STATE.md",
        """# Run state

- Phase: COMPLETE
- Status: SUCCESS
- Next permitted action: freeze baseline for independent integrity checks
""",
    )
    w(
        REF / "Harness/HANDOFF_RECEIPT.md",
        """# Handoff receipt

- Terminal reason: SUCCESS
- Accepted: Mission_Brief.md, Retrieval/Answers.md, Audit.md, Notes/Content/*, Evidence/*
- Residual risk: commercial Ro/Ro market tightness; thin rail-speed notices rejected in audit
- Baseline: run tools/verify_baseline.py --write-manifest and copy external P4_BASELINE_DATE.json
""",
    )


def main() -> int:
    write_seed()
    build_reference()
    print("SEED_AND_REFERENCE_OK", REF)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
