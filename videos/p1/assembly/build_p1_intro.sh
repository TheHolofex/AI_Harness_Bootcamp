#!/usr/bin/env bash
# Build P1 intro from stills/clips + optional VO.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"   # videos/
REPO="$(cd "$ROOT/.." && pwd)"
cd "$REPO"

VENV_PY="$ROOT/.venv/bin/python"
if [[ ! -x "$VENV_PY" ]]; then
  python3 -m venv "$ROOT/.venv"
  "$ROOT/.venv/bin/pip" install -q pillow
  VENV_PY="$ROOT/.venv/bin/python"
fi

exec "$VENV_PY" videos/p1/assembly/build_p1_intro.py --mvp-stills-only "$@"
