#!/usr/bin/env python3
"""Promote validated triage_candidate.json to triage_record.md after --approve."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

from validate_triage_candidate import VErr, validate


def esc(s: str) -> str:
    return (s or "").replace("|", "\\|").replace("\n", " ").strip()


def evidence_cell(ev: dict) -> str:
    parts = [esc(ev.get("summary") or "")]
    if ev.get("claim_quote"):
        parts.append(f"claim: «{esc(ev['claim_quote'])}»")
    if ev.get("source_id"):
        parts.append(f"source_id: {esc(ev['source_id'])}")
    if ev.get("source_quote"):
        parts.append(f"source: «{esc(ev['source_quote'])}»")
    if ev.get("source_resolution"):
        parts.append(f"resolution: {esc(ev['source_resolution'])}")
    if ev.get("contradiction_left") or ev.get("contradiction_right"):
        parts.append(
            f"contra: «{esc(ev.get('contradiction_left') or '')}» vs «{esc(ev.get('contradiction_right') or '')}»"
        )
    if ev.get("trusted_fact_id"):
        parts.append(f"trusted_fact: {esc(ev['trusted_fact_id'])}")
    if ev.get("hostile_lines"):
        hl = "; ".join(esc(x) for x in ev["hostile_lines"][:4])
        parts.append(f"hostile: {hl}")
    return " · ".join(p for p in parts if p)


def render_md(data: dict) -> str:
    lines = [
        "# Triage record",
        "",
        "Promoted from `out/triage_candidate.json` after operator approval. "
        "The exposed agent cannot write this file.",
        "",
        "| File | Class | Evidence | Disposition | Times (detect / isolate / verify) |",
        "|---|---|---|---|---|",
    ]
    for row in sorted(data["rows"], key=lambda r: r["file"]):
        ev = row.get("evidence") or {}
        times = row.get("times") or {}
        t = f"{esc(times.get('detect','—'))} / {esc(times.get('isolate','—'))} / {esc(times.get('verify','—'))}"
        lines.append(
            f"| {row['file']} | {row['class']} | {evidence_cell(ev)} | {row['disposition']} | {t} |"
        )
    lines += [
        "",
        "## Structured evidence blocks",
        "",
    ]
    for row in sorted(data["rows"], key=lambda r: r["file"]):
        ev = row.get("evidence") or {}
        lines.append(f"### {row['file']} ({row['class']} → {row['disposition']})")
        lines.append("")
        lines.append(f"- Summary: {ev.get('summary','')}")
        if ev.get("claim_quote"):
            lines.append(f"- Claim quote: {ev['claim_quote']}")
        if ev.get("source_id"):
            lines.append(f"- Source id: {ev['source_id']}")
        if ev.get("source_quote"):
            lines.append(f"- Source quote: {ev['source_quote']}")
        if ev.get("source_resolution"):
            lines.append(f"- Source resolution: {ev['source_resolution']}")
        if ev.get("contradiction_left"):
            lines.append(f"- Contradiction left: {ev['contradiction_left']}")
        if ev.get("contradiction_right"):
            lines.append(f"- Contradiction right: {ev['contradiction_right']}")
        if ev.get("trusted_fact_id"):
            lines.append(f"- Trusted fact id: {ev['trusted_fact_id']}")
        if ev.get("hostile_lines"):
            lines.append("- Hostile lines:")
            for hl in ev["hostile_lines"]:
                lines.append(f"  - {hl}")
        times = row.get("times") or {}
        lines.append(
            f"- Times: detect={times.get('detect')} · isolate={times.get('isolate')} · verify={times.get('verify')}"
        )
        lines.append("")
    lines += [
        "## Controls used",
        "",
        "| Control | What it controls | Evidence from this run | Residual risk |",
        "|---|---|---|---|",
        "| Exact p5-staging project + launcher | reachable paths and tools | runtime config hash + resolved MCP list | operator could still run tools outside the launcher |",
        "| Granular edit allowlist | agent write surface | only out/triage_candidate.json allowed | misconfigured OpenCode merge could widen writes |",
        "| Citation + contradiction checks | content quality | structured evidence blocks above | operator still owns each disposition |",
        "| Deterministic baseline check | trusted-vault integrity | manifest before/after PASS | only paths in the P4 baseline are covered |",
        "",
        "## Reusable intake rule",
        "",
        "I never accept intake into trusted knowledge until it has a validated triage row "
        "promoted after my single approval gate.",
        "",
        "## After sanctioned writes",
        "",
        "A separate retrieval check is required after any approved write into the brain. "
        "Baseline PASS means unchanged, not true.",
        "",
    ]
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("candidate", type=Path)
    ap.add_argument("--pack-root", type=Path, required=True)
    ap.add_argument("--staging-root", type=Path, required=True)
    ap.add_argument("--approve", action="store_true")
    ap.add_argument("--hash-out", type=Path, default=None)
    args = ap.parse_args(argv)
    if not args.approve:
        print("HOLD promote: missing --approve", file=sys.stderr)
        return 2
    try:
        validate(args.candidate, args.pack_root, args.staging_root)
    except VErr as e:
        print(f"HOLD promote: candidate invalid: {e}", file=sys.stderr)
        return 1
    data = json.loads(args.candidate.read_text(encoding="utf-8"))
    out = args.staging_root / "triage_record.md"
    if out.exists():
        print(
            f"HOLD promote: {out} already exists — refuse overwrite without fresh staging",
            file=sys.stderr,
        )
        return 1
    text = render_md(data)
    out.write_text(text, encoding="utf-8")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    print(f"PASS promote: wrote {out}")
    print(f"SHA256 {digest}")
    if args.hash_out:
        args.hash_out.parent.mkdir(parents=True, exist_ok=True)
        args.hash_out.write_text(
            f"Path: {out}\nAlgorithm: SHA256\nHash: {digest}\nDate: {date.today().isoformat()}\n",
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
