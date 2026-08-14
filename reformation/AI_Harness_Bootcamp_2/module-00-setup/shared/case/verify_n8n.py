#!/usr/bin/env python3
"""Check that the learner's local n8n is running, and that it is n8n.

Something answering on port 5678 is not evidence that n8n is running. A stray web
server, a leftover container, or `python3 -m http.server 5678` will all answer. This
asks n8n's own health endpoint and requires an n8n-shaped reply.

Usage:  python3 verify_n8n.py [marker-file]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

BASE = "http://127.0.0.1:5678"
marker = Path(sys.argv[1]) if len(sys.argv) > 1 else None


def fetch(path: str, timeout: int = 5) -> tuple[int, str]:
    try:
        with urlopen(BASE + path, timeout=timeout) as response:
            return response.status, response.read(8192).decode("utf-8", "replace")
    except HTTPError as exc:
        return exc.code, exc.read(8192).decode("utf-8", "replace")


def main() -> int:
    try:
        status, body = fetch("/healthz")
    except (URLError, TimeoutError, OSError) as exc:
        print(f"HOLD: nothing answered at {BASE} — {exc}")
        print("      Start n8n in another terminal with: n8n start")
        return 1

    if not 200 <= status < 400:
        print(f"HOLD: {BASE}/healthz returned HTTP {status}")
        return 1

    # n8n's health endpoint replies with JSON carrying a status field.
    try:
        healthy = str(json.loads(body).get("status", "")).lower() in {"ok", "up", "healthy"}
    except (json.JSONDecodeError, AttributeError):
        healthy = False

    if not healthy:
        print(f"HOLD: something is listening on port 5678, but it is not n8n.")
        print(f"      {BASE}/healthz replied: {body.strip()[:120]!r}")
        print("      Stop whatever is using port 5678, then run: n8n start")
        return 1

    print(f"PASS: n8n answered its health check at {BASE}")
    if marker:
        marker.write_text("PASS\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
