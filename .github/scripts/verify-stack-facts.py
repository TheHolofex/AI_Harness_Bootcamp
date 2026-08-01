#!/usr/bin/env python3
"""Rotting-facts harness for the bootcamp's canonical install clinic.

Runs on any machine with Python 3.9+ and network access. It does not install
tools and does not need API keys.

Exit 0 = all hard checks passed (soft network warnings allowed).
Exit 1 = one or more hard failures.
Exit 2 = the harness itself could not run.

What it covers:
  - The live install-clinic HTML still names the intended install channels
  - The course registry still routes B0 to that canonical page
  - The current Node LTS remains inside the range taught for n8n
  - The npm OpenCode package and AAIF goose installer remain available
  - The repository still contains load-bearing exercise and facilitator paths

What it does not cover (needs Windows, funded keys, and a person):
  - Installer behavior, PATH changes, or managed-device policy
  - Harness authentication and model access
  - Write proofs, sandbox behavior, or browser-to-deck operation
"""

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple


# parents: scripts -> .github -> repo
REPO_ROOT = Path(__file__).resolve().parents[2]
INSTALL_PAGE = REPO_ROOT / "site" / "checklists" / "prework-install.html"
REGISTRY = REPO_ROOT / "site" / "js" / "registry.js"

UA = "AI-Harness-Bootcamp-stack-facts/2.0 (+staff)"
NODE_INDEX_URL = "https://nodejs.org/dist/index.json"
OPENCODE_NPM_URL = "https://registry.npmjs.org/opencode-ai/latest"
GOOSE_INSTALLER_URL = (
    "https://raw.githubusercontent.com/aaif-goose/goose/main/download_cli.ps1"
)


@dataclass
class Result:
    name: str
    ok: bool
    hard: bool
    detail: str


@dataclass
class Report:
    results: List[Result] = field(default_factory=list)

    def add(self, name: str, ok: bool, detail: str, hard: bool = True) -> None:
        self.results.append(Result(name, ok, hard, detail))
        mark = "PASS" if ok else ("FAIL" if hard else "WARN")
        print(f"[{mark}] {name}: {detail}")


def http_json(url: str, timeout: float = 25.0) -> Tuple[Optional[object], str]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": UA, "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
            return json.loads(raw), f"HTTP {response.status}"
    except urllib.error.HTTPError as error:
        return None, f"HTTP {error.code}"
    except Exception as error:  # noqa: BLE001 - report staff-facing network failures
        return None, f"{type(error).__name__}: {error}"


def http_text(url: str, timeout: float = 25.0) -> Tuple[Optional[str], str]:
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read().decode("utf-8", errors="replace"), f"HTTP {response.status}"
    except urllib.error.HTTPError as error:
        return None, f"HTTP {error.code}"
    except Exception as error:  # noqa: BLE001 - report staff-facing network failures
        return None, f"{type(error).__name__}: {error}"


def check_repo_paths(report: Report) -> None:
    required = [
        "site/index.html",
        "site/prework.html",
        "site/checklists/prework-install.html",
        "site/js/registry.js",
        "operator/DIRECTION_BRIEF.md",
        "operator/PASS_BARS.md",
        "instruments/p2_test_suite",
        "instruments/p3_frozen_brief",
        "instruments/p3_multi_agent",
        "instruments/p8_hold_degrade",
        "mission_flesh/b1",
        "mission_flesh/p1",
        "mission_flesh/p3/MANY_MINDS.md",
        "mission_flesh/p4",
        "mission_flesh/p5",
        "mission_flesh/p6/local_endpoint_notes.md",
        "mission_flesh/p6/watch_officer.yaml",
        "mission_flesh/p7",
        "mission_flesh/p8",
        "lead/BROWSER_DECK_DEMO.md",
        "lead/HARNESS_CASE_TALKS.md",
    ]
    missing = [path for path in required if not (REPO_ROOT / path).exists()]
    if missing:
        report.add(
            "repo.load_bearing_paths",
            False,
            "missing: " + ", ".join(missing),
            hard=True,
        )
    else:
        report.add(
            "repo.load_bearing_paths",
            True,
            f"{len(required)} paths present",
            hard=True,
        )


def check_canonical_install_surface(report: Report) -> None:
    html = INSTALL_PAGE.read_text(encoding="utf-8")
    expected = {
        "Git official download": "https://git-scm.com/install/windows",
        "Node LTS official download": "https://nodejs.org/en/download",
        "Python official download": "https://www.python.org/downloads/windows/",
        "course repository clone": (
            "git clone https://github.com/TheHolofex/AI_Harness_Bootcamp.git"
        ),
        "ChatGPT/Codex installer": (
            "https://get.microsoft.com/installer/download/9PLM9XGG6VKS"
        ),
        "OpenCode npm channel": "npm install -g opencode-ai",
        "Pi PowerShell installer": "https://pi.dev/install.ps1",
        "AAIF goose PowerShell installer": GOOSE_INSTALLER_URL,
        "Obsidian official download": "https://obsidian.md/download",
        "n8n npm channel": "npm install n8n -g",
    }
    missing = [label for label, needle in expected.items() if needle not in html]
    if missing:
        report.add(
            "setup.install_channels",
            False,
            "canonical page missing: " + ", ".join(missing),
            hard=True,
        )
    else:
        report.add(
            "setup.install_channels",
            True,
            f"{len(expected)} current channel facts present in canonical HTML",
            hard=True,
        )

    if re.search(r"\bwinget\b", html, flags=re.IGNORECASE):
        report.add(
            "setup.no_winget",
            False,
            "canonical install page mentions winget",
            hard=True,
        )
    else:
        report.add(
            "setup.no_winget",
            True,
            "canonical install page contains no winget path",
            hard=True,
        )


def check_registry_install_route(report: Report) -> None:
    registry = REGISTRY.read_text(encoding="utf-8")
    expected = ['code: "B0"', 'url: "checklists/prework-install.html"']
    missing = [needle for needle in expected if needle not in registry]
    if missing:
        report.add(
            "site.b0_route",
            False,
            "registry missing: " + ", ".join(missing),
            hard=True,
        )
    else:
        report.add(
            "site.b0_route",
            True,
            "B0 routes to checklists/prework-install.html",
            hard=True,
        )


def check_node_lts_claim(report: Report) -> None:
    """Verify the newest Node LTS fits the 22.22-or-newer, below-25 clinic range."""
    data, status = http_json(NODE_INDEX_URL)
    if data is None:
        report.add(
            "node.lts_range",
            False,
            f"could not fetch Node release index ({status})",
            hard=False,
        )
        return
    if not isinstance(data, list):
        report.add("node.lts_range", False, "unexpected Node index payload", hard=True)
        return

    lts_rows = [row for row in data if isinstance(row, dict) and row.get("lts")]
    if not lts_rows:
        report.add("node.lts_range", False, "Node index contains no LTS release", hard=True)
        return

    latest_lts = lts_rows[0]
    version = str(latest_lts.get("version", ""))
    match = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)(?:[-+].*)?", version)
    if not match:
        report.add(
            "node.lts_range",
            False,
            f"could not parse latest LTS version {version!r}",
            hard=True,
        )
        return

    major, minor, _patch = (int(part) for part in match.groups())
    supported = (major > 22 or (major == 22 and minor >= 22)) and major < 25
    if supported:
        report.add(
            "node.lts_range",
            True,
            f"latest Node LTS is {version} ({latest_lts.get('lts')})",
            hard=True,
        )
    else:
        report.add(
            "node.lts_range",
            False,
            f"latest Node LTS is {version}; canonical clinic requires >=22.22 and <25",
            hard=True,
        )


def check_opencode_npm_channel(report: Report) -> None:
    data, status = http_json(OPENCODE_NPM_URL)
    if data is None:
        report.add(
            "opencode.npm_channel",
            False,
            f"could not fetch npm package metadata ({status})",
            hard=False,
        )
        return

    if not isinstance(data, dict):
        report.add(
            "opencode.npm_channel",
            False,
            "unexpected npm registry payload",
            hard=True,
        )
        return

    name = data.get("name")
    version = str(data.get("version", ""))
    valid_version = re.fullmatch(r"\d+\.\d+\.\d+(?:[-+].*)?", version)
    if name == "opencode-ai" and valid_version:
        report.add(
            "opencode.npm_channel",
            True,
            f"opencode-ai@{version} is published on npm",
            hard=True,
        )
    else:
        report.add(
            "opencode.npm_channel",
            False,
            f"unexpected package metadata: name={name!r}, version={version!r}",
            hard=True,
        )


def check_goose_installer_channel(report: Report) -> None:
    script, status = http_text(GOOSE_INSTALLER_URL)
    if script is None:
        report.add(
            "goose.installer_channel",
            False,
            f"could not fetch AAIF PowerShell installer ({status})",
            hard=False,
        )
        return

    markers = [
        "aaif-goose/goose",
        "releases/download",
        'Join-Path $env:USERPROFILE ".local\\bin"',
    ]
    missing = [marker for marker in markers if marker not in script]
    if missing:
        report.add(
            "goose.installer_channel",
            False,
            "AAIF installer changed shape; missing: " + ", ".join(missing),
            hard=True,
        )
    else:
        report.add(
            "goose.installer_channel",
            True,
            f"AAIF PowerShell installer reachable ({status})",
            hard=True,
        )


def main() -> int:
    print(f"repo: {REPO_ROOT}")
    report = Report()
    try:
        check_repo_paths(report)
        check_canonical_install_surface(report)
        check_registry_install_route(report)
        check_node_lts_claim(report)
        check_opencode_npm_channel(report)
        check_goose_installer_channel(report)
    except Exception as error:  # noqa: BLE001 - make harness failures explicit
        print(f"[FAIL] harness.crash: {type(error).__name__}: {error}", file=sys.stderr)
        return 2

    hard_failures = [result for result in report.results if not result.ok and result.hard]
    warnings = [result for result in report.results if not result.ok and not result.hard]
    print()
    print(
        f"summary: {len(report.results)} checks · "
        f"hard_fail={len(hard_failures)} · warn={len(warnings)}"
    )
    if hard_failures:
        print("hard failures:")
        for result in hard_failures:
            print(f"  - {result.name}: {result.detail}")
        return 1
    if warnings:
        print("warnings (review before the next clinic):")
        for result in warnings:
            print(f"  - {result.name}: {result.detail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
