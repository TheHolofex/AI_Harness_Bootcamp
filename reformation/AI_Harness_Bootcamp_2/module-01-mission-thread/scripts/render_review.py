#!/usr/bin/env python3
"""Render the Module 1 work into one local, keyboard-readable HTML review page."""

from __future__ import annotations

import argparse
import csv
import html
from pathlib import Path

SECTION_FILES = [
    ("Challenge matrix", "challenge-matrix.md"),
    ("Baseline corrected brief", "corrected-brief.md"),
    ("Changed corrected brief", "changed-brief.md"),
    ("Baseline verdict", "baseline-verdict.md"),
    ("Change prediction", "change-prediction.md"),
    ("Changed verdict", "changed-verdict.md"),
    ("Handoff", "handoff.md"),
]


def table(path: Path) -> str:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        return "<p>Empty ledger.</p>"
    head, *body = rows
    source_index = head.index("source_id") if "source_id" in head else -1

    def cell(index: int, value: str) -> str:
        escaped = html.escape(value)
        if index == source_index and value.startswith("S"):
            candidates = sorted((path.parent / "case-packet/sources").glob(f"{value}_*.md"))
            if candidates:
                target = candidates[0].relative_to(path.parent).as_posix()
                return f"<td><a href='{html.escape(target)}'>{escaped}</a></td>"
        return f"<td>{escaped}</td>"

    return "<div class='scroll'><table><thead><tr>" + "".join(f"<th scope='col'>{html.escape(name)}</th>" for name in head) + "</tr></thead><tbody>" + "".join("<tr>" + "".join(cell(index, value) for index, value in enumerate(row)) + "</tr>" for row in body) + "</tbody></table></div>"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workdir", type=Path)
    args = parser.parse_args()
    work = args.workdir.resolve()
    output = work / "review.html"
    sections = []
    for title, name in SECTION_FILES:
        path = work / name
        text = path.read_text(encoding="utf-8") if path.exists() else f"Missing: {name}"
        sections.append(f"<section><h2>{html.escape(title)}</h2><pre>{html.escape(text)}</pre></section>")
    ledgers = []
    for title, name in (("Source register", "source-register.csv"), ("Baseline thread", "thread-ledger.csv"), ("Changed thread", "changed-thread-ledger.csv")):
        path = work / name
        ledgers.append(f"<section><h2>{title}</h2>{table(path) if path.exists() else '<p>Missing ledger.</p>'}</section>")
    document = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Module 1 review</title><style>
body{{font:18px/1.55 system-ui,sans-serif;max-width:1100px;margin:auto;padding:2rem;color:#171717;background:#fff}}
a{{color:#0645ad}} pre{{white-space:pre-wrap;background:#f5f5f5;padding:1rem;border:1px solid #bbb}}
.scroll{{overflow:auto}} table{{border-collapse:collapse;font-size:.85rem}} th,td{{border:1px solid #777;padding:.45rem;text-align:left;vertical-align:top}} th{{background:#eee;position:sticky;top:0}}
:focus{{outline:3px solid #005fcc;outline-offset:2px}}
</style></head><body><h1>Cold Lantern verification review</h1>
<p>Local class review only. Use the source manifest and supplied source files to inspect cited records.</p>
<nav aria-label="Review sections"><a href="#decision">Skip to decisions</a></nav>
{''.join(ledgers)}<div id="decision">{''.join(sections)}</div></body></html>"""
    output.write_text(document, encoding="utf-8")
    print(f"PASS: wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
