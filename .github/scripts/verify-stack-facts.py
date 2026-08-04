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
  - Goose's Windows runtime, model, and native-exit guards remain present
  - The P2 Inbound surface and its morning corpus remain wired
  - The Agent Loops briefing and P4 personal harness remain wired in sequence
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
HCP_PAGE = REPO_ROOT / "site" / "blocks" / "hcp.html"
P2_PAGE = REPO_ROOT / "site" / "blocks" / "p2.html"
LOOPS_PAGE = REPO_ROOT / "site" / "blocks" / "loops.html"
P4_PAGE = REPO_ROOT / "site" / "blocks" / "p4.html"
P5_PAGE = REPO_ROOT / "site" / "blocks" / "p5.html"
P2_MATERIAL = REPO_ROOT / "mission_flesh" / "tuesday"
P4_SEED = REPO_ROOT / "mission_flesh" / "p4" / "vault_seed"
WINDOWS_SMOKE = REPO_ROOT / ".github" / "scripts" / "prework-verify.ps1"
WINDOWS_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "prework-smoke.yml"

UA = "AI-Harness-Bootcamp-stack-facts/2.0 (+staff)"
NODE_INDEX_URL = "https://nodejs.org/dist/index.json"
OPENCODE_PIN = "1.18.11"
OPENCODE_NPM_URL = f"https://registry.npmjs.org/opencode-ai/{OPENCODE_PIN}"
GOOSE_INSTALLER_URL = (
    "https://raw.githubusercontent.com/aaif-goose/goose/main/download_cli.ps1"
)
VC_REDIST_X64_URL = "https://aka.ms/vc14/vc_redist.x64.exe"


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
        "site/blocks/hcp.html",
        "site/blocks/p2.html",
        "site/js/registry.js",
        "operator/DIRECTION_BRIEF.md",
        "operator/CAPABILITIES.md",
        "instruments/endpoint_case_suite",
        "mission_flesh/tuesday/MANIFEST.md",
        "mission_flesh/tuesday/inbound/arrivals/arrivals_a_station_manifest.csv",
        "mission_flesh/tuesday/inbound/arrivals/arrivals_b_desk_paste.txt",
        "mission_flesh/tuesday/inbound/arrivals/arrivals_c_persys_export.json",
        "mission_flesh/tuesday/inbound/arrivals/arrivals_c_persys_export_v2.json",
        "mission_flesh/tuesday/inbound/arrivals/arrivals_d_partner_roster.csv",
        "mission_flesh/tuesday/inbound/records/billet_catalog.csv",
        "mission_flesh/tuesday/inbound/records/qualification_register.csv",
        "mission_flesh/tuesday/inbound/records/current_roster.csv",
        "mission_flesh/tuesday/inbound/records/rotation_out.csv",
        "mission_flesh/tuesday/inbound/records/desk_directory.md",
        "mission_flesh/tuesday/inbound/distros",
        "mission_flesh/tuesday/inbound/lookalike",
        "mission_flesh/tuesday/inbound/traffic",
        "instruments/p3_evidence_surface/server.mjs",
        "instruments/p3_evidence_surface/smoke.mjs",
        "instruments/p8_hold_degrade",
        "mission_flesh/b1",
        "mission_flesh/p1",
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
        "OpenCode pinned npm channel": f"npm install -g opencode-ai@{OPENCODE_PIN}",
        "Pi PowerShell installer": "https://pi.dev/install.ps1",
        "Microsoft Visual C++ x64 runtime": VC_REDIST_X64_URL,
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


def check_goose_windows_guards(report: Report) -> None:
    html = INSTALL_PAGE.read_text(encoding="utf-8")
    smoke = WINDOWS_SMOKE.read_text(encoding="utf-8-sig")
    workflow = WINDOWS_WORKFLOW.read_text(encoding="utf-8")
    expected = {
        "HTML rejects an empty xAI model": (
            html,
            "[string]::IsNullOrWhiteSpace($env:HB_XAI_MODEL)",
        ),
        "HTML pins the current xAI model before saving it": (
            html,
            "$env:HB_XAI_MODEL = 'grok-4.5'",
        ),
        "HTML checks the registered x64 runtime": (
            html,
            r"HKLM:\SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64",
        ),
        "HTML checks the alternate x64 runtime registry view": (
            html,
            r"HKLM:\SOFTWARE\WOW6432Node\Microsoft\VisualStudio\14.0\VC\Runtimes\x64",
        ),
        "HTML captures the Goose native exit code": (
            html,
            "$gooseExit = $LASTEXITCODE",
        ),
        "HTML diagnoses the missing-DLL status": (html, "-1073741515"),
        "Windows smoke checks the x64 runtime": (smoke, "runtime.vcredist_x64"),
        "Windows smoke captures the Goose native exit code": (
            smoke,
            "$gexit = $LASTEXITCODE",
        ),
        "Windows smoke makes an installed-but-broken Goose a hard failure": (
            smoke,
            'Write-Result -Name "bin.goose" -Ok $false -Detail "$($c.Source) - $detail" -Hard $true',
        ),
        "Windows smoke makes a missing Goose a hard failure": (
            smoke,
            'Write-Result -Name "bin.goose" -Ok $false -Detail "goose not on PATH (use the AAIF installer in the website checklist)" -Hard $true',
        ),
        "Windows workflow installs the x64 runtime": (
            workflow,
            VC_REDIST_X64_URL,
        ),
        "Windows workflow installs the official Goose CLI": (
            workflow,
            GOOSE_INSTALLER_URL,
        ),
    }
    missing = [label for label, (surface, token) in expected.items() if token not in surface]
    if missing:
        report.add(
            "setup.goose_windows_guards",
            False,
            "missing: " + ", ".join(missing),
            hard=True,
        )
    else:
        report.add(
            "setup.goose_windows_guards",
            True,
            f"{len(expected)} model, runtime, and native-exit guards present",
            hard=True,
        )


def check_registry_install_route(report: Report) -> None:
    registry = REGISTRY.read_text(encoding="utf-8")
    expected = [
        'code: "B0"',
        'url: "checklists/prework-install.html"',
        '"gs-runtime"',
    ]
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
            "B0 routes to the install page and requires the Goose runtime step",
            hard=True,
        )


def check_p2_inbound_surface(report: Report) -> None:
    registry = REGISTRY.read_text(encoding="utf-8")
    hcp = HCP_PAGE.read_text(encoding="utf-8")
    p2 = P2_PAGE.read_text(encoding="utf-8")
    manifest = (P2_MATERIAL / "MANIFEST.md").read_text(encoding="utf-8")
    expected = {
        "registry briefing": 'code: "HCP"',
        "registry route": 'codes: ["HCP", "P2", "MCP1", "MCP2", "P3"]',
        "registry title": 'title: "Inbound"',
        "registry storage": 'key: "ahb-checklist-p2-project-organizer"',
        "presentation URL": "Harness-Prompt-Folklore-Design-the-Control-Plane-Not-Just-the-Pro-74204eoe255uss1",
        "P2 material root": "mission_flesh\\tuesday\\inbound",
        "P2 damaged source": "arrivals_d_partner_roster.csv",
        "P2 upgraded export": "arrivals_c_persys_export_v2.json",
        "P2 normalizer": "scripts\\normalize_arrivals.py",
        "P2 hook event": "PreToolUse",
        "P2 hook registration": ".codex/hooks.json",
        "P2 hook trust": "/hooks",
        "P2 skill location": ".agents/skills/",
        "P2 plugin manifest": "plugins/inbound/.codex-plugin/plugin.json",
        "P2 marketplace file": ".agents/plugins/marketplace.json",
        "P2 marketplace registration": "codex plugin marketplace add",
        "P2 plugin root variable": "PLUGIN_ROOT",
        "P2 model": "gpt-5.6-terra",
        "P2 manifest morning corpus": "inbound/arrivals/",
    }
    surfaces = {
        "registry briefing": registry,
        "registry route": registry,
        "registry title": registry,
        "registry storage": registry,
        "presentation URL": hcp,
        "P2 material root": p2,
        "P2 damaged source": p2,
        "P2 upgraded export": p2,
        "P2 normalizer": p2,
        "P2 hook event": p2,
        "P2 hook registration": p2,
        "P2 hook trust": p2,
        "P2 skill location": p2,
        "P2 plugin manifest": p2,
        "P2 marketplace file": p2,
        "P2 marketplace registration": p2,
        "P2 plugin root variable": p2,
        "P2 model": p2,
        "P2 manifest morning corpus": manifest,
    }
    missing = [label for label, token in expected.items() if token not in surfaces[label]]
    if missing:
        report.add(
            "site.p2_inbound",
            False,
            "missing: " + ", ".join(missing),
            hard=True,
        )
    else:
        report.add(
            "site.p2_inbound",
            True,
            "presentation, route, morning corpus, normalizer, both hooks, both skills, package, marketplace, and Terra pin present",
            hard=True,
        )


def check_p4_agent_loop_surface(report: Report) -> None:
    registry = REGISTRY.read_text(encoding="utf-8")
    loops = LOOPS_PAGE.read_text(encoding="utf-8")
    p4 = P4_PAGE.read_text(encoding="utf-8")
    p5 = P5_PAGE.read_text(encoding="utf-8")
    expected = {
        "registry briefing": (registry, 'code: "LOOPS"'),
        "Wednesday route": (registry, 'codes: ["LOOPS", "P4", "P5"]'),
        "Gamma deck": (loops, "Control-Flow-Is-the-Product-nnbb430p72cg1wa"),
        "briefing completion": (loops, 'data-check-id="loops-complete"'),
        "P4 goal": (p4, "/goal"),
        "P4 skill": (p4, "$director-loop"),
        "P4 verifier": (p4, "tools\\verify_vault.py"),
        "P4 raw-source manifest": (p4, "SOURCE_MANIFEST.json"),
        "P4 configured evaluator": (p4, "director_evaluator"),
        "P4 real resume": (p4, "P4 — Resume"),
        "P4 resume receipt": (p4, "RESUME_RECEIPT.md"),
        "P4 external candidate check": (p4, "mission_flesh\\p4\\vault_seed\\tools\\verify_vault.py"),
        "P4 preserved first candidate receipt": (p4, "CANDIDATE_CHECK_FIRST.txt"),
        "P4 stable-content release binding": (p4, "stable-content fingerprint"),
        "P4 immutable evaluated trace": (p4, "evaluator-bound trace prefix"),
        "P4 non-performative control repair": (p4, "CONTROL_ONLY"),
        "P4 scoped handoff": (p4, "HANDOFF_RECEIPT.md"),
        "P4 manifest": (p4, "--write-manifest"),
        "P4 trust-anchor overwrite guard": (p4, "never overwrite a trust anchor"),
        "P5 pre/post manifest check": (p5, "--check-manifest"),
        "P5 external manifest anchor": (p5, "operator\\evidence\\P4_BASELINE_[TODAY].json"),
        "P5 isolated project": (p5, "choose exactly <code>Documents\\p5-staging</code>"),
        "P5 recovery verified before replacement": (p5, "Recovery copy failed the trusted baseline"),
        "P5 payload-free handoff": (p5, "P5_HANDOFF_[TODAY].md"),
    }
    required_files = [
        P4_SEED / "AGENTS.md",
        P4_SEED / ".agents" / "skills" / "director-loop" / "SKILL.md",
        P4_SEED / ".codex" / "agents" / "director_evaluator.toml",
        P4_SEED / "Harness" / "HARNESS_CARD.md",
        P4_SEED / "Harness" / "RUN_STATE.md",
        P4_SEED / "Harness" / "RUN_TRACE.md",
        P4_SEED / "Harness" / "EVAL.md",
        P4_SEED / "Harness" / "HANDOFF_RECEIPT.md",
        P4_SEED / "Harness" / "SOURCE_MANIFEST.json",
        P4_SEED / "tools" / "verify_vault.py",
    ]
    missing = [label for label, (surface, token) in expected.items() if token not in surface]
    forbidden = {
        "P4 obsolete cold-start demo": (p4, "P4 — Cold Start"),
        "P5 obsolete model diff baseline": (p5, "p4-vault_baseline"),
        "P5 broad exposed project": (p5, "choose your <code>Documents</code> folder"),
    }
    missing.extend(
        f"forbidden: {label}" for label, (surface, token) in forbidden.items() if token in surface
    )
    missing.extend(str(path.relative_to(REPO_ROOT)) for path in required_files if not path.is_file())
    if missing:
        report.add(
            "site.p4_personal_harness",
            False,
            "missing: " + ", ".join(missing),
            hard=True,
        )
    else:
        report.add(
            "site.p4_personal_harness",
            True,
            "deck, route, goal, skill, raw-source controls, bound evaluation, real resume, verifier, guarded manifest, recovery, and scoped handoff present",
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
    if name == "opencode-ai" and valid_version and version == OPENCODE_PIN:
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
            f"unexpected pinned package metadata: name={name!r}, version={version!r}, expected={OPENCODE_PIN!r}",
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
        check_goose_windows_guards(report)
        check_registry_install_route(report)
        check_p2_inbound_surface(report)
        check_p4_agent_loop_surface(report)
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
