#!/usr/bin/env bash
# Portable baseline check wrapper (author/CI). Learners use PowerShell on Windows.
set -u
VAULT=${1:?vault}
MANIFEST=${2:?manifest}
OUT=${3:?receipt_out}
COURSE_ROOT=${COURSE_ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}
TOOL="$COURSE_ROOT/mission_flesh/p4/vault_seed/tools/verify_baseline.py"
python3 "$TOOL" "$VAULT" --check-manifest "$MANIFEST" | tee "$OUT"
exit ${PIPESTATUS[0]}
