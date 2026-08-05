#!/usr/bin/env python3
"""Compatibility entry point for the canonical P5 runtime-config builder."""
from __future__ import annotations

import runpy
from pathlib import Path

CANONICAL = Path(__file__).resolve().parents[2] / "scripts" / "build_runtime_config.py"
runpy.run_path(str(CANONICAL), run_name="__main__")
