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
  - The official Node channel still publishes a current LTS release
  - The npm OpenCode package and AAIF goose installer remain available
  - Goose's Windows runtime, model, and native-exit guards remain present
  - The P2 Inbound surface and its morning corpus remain wired
  - The Agent Loops briefing and P4 second-brain exercise remain wired in sequence
  - The Thursday Pi lab still contains ten runnable patterns and precedes P6
  - The repository still contains load-bearing exercise and facilitator paths

What it does not cover (needs Windows, funded keys, and a person):
  - Installer behavior, PATH changes, or managed-device policy
  - Harness authentication and model access
  - Write proofs, sandbox behavior, or browser-to-deck operation
"""

from __future__ import annotations

import gzip
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
PI_PAGE = REPO_ROOT / "site" / "blocks" / "pi.html"
PI_FIGURE_ROOT = REPO_ROOT / "site" / "assets" / "blocks" / "pi"
PI_ROOT = REPO_ROOT / "mission_flesh" / "pi"
PI_PACKAGE = PI_ROOT / "package.json"
PI_RUNTIME = PI_ROOT / "src" / "pi-runtime.ts"
PI_TEST = PI_ROOT / "tests" / "patterns.test.ts"
STACK_FACTS_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "stack-facts.yml"
P2_MATERIAL = REPO_ROOT / "mission_flesh" / "tuesday"
P4_SEED = REPO_ROOT / "mission_flesh" / "p4" / "vault_seed"
P6_ROOT = REPO_ROOT / "mission_flesh" / "p6"
P6_START = P6_ROOT / "scripts" / "Start-P6.ps1"
P6_WAVE2 = P6_ROOT / "scripts" / "Update-P6.ps1"
P6_TEST = P6_ROOT / "tests" / "p6.test.mjs"
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
        "site/blocks/pi.html",
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
        "instruments/osint_desk/probe.mjs",
        "instruments/osint_desk/specimen/server.mjs",
        "instruments/osint_desk/starter/server.mjs",
        "instruments/osint_desk/fixtures/ais_vessels_planted.json",
        "instruments/p3_evidence_surface/server.mjs",
        "instruments/p3_evidence_surface/smoke.mjs",
        "instruments/p8_hold_degrade",
        "mission_flesh/b1",
        "mission_flesh/p1",
        "mission_flesh/p4",
        "mission_flesh/p5",
        "mission_flesh/p6/MISSION.md",
        "mission_flesh/p6/clear_overnight_watch.yaml",
        "mission_flesh/p6/scripts/Start-P6.ps1",
        "mission_flesh/p6/scripts/Update-P6.ps1",
        "mission_flesh/p6/scripts/p6-lib.mjs",
        "mission_flesh/p6/scripts/prepare.mjs",
        "mission_flesh/p6/scripts/update.mjs",
        "mission_flesh/p6/scripts/verify.mjs",
        "mission_flesh/p6/tests/p6.test.mjs",
        "mission_flesh/pi/package.json",
        "mission_flesh/pi/package-lock.json",
        "mission_flesh/pi/src/pi-runtime.ts",
        "mission_flesh/pi/src/run.ts",
        "mission_flesh/pi/tests/patterns.test.ts",
        "mission_flesh/pi/scripts/Setup-PiLab.ps1",
        "mission_flesh/pi/scripts/Run-Pattern.ps1",
        "mission_flesh/pi/scripts/Verify-PiLab.ps1",
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

    stale_pi = [
        marker
        for marker in (
            "https://pi.dev/install.ps1",
            'data-check-id="pi-install"',
            'data-check-id="pi-verify"',
            'data-check-id="pi-write"',
            "from-pi.txt",
        )
        if marker in html
    ]
    if stale_pi:
        report.add(
            "setup.no_unused_pi",
            False,
            "unused Pi pre-work remains: " + ", ".join(stale_pi),
            hard=True,
        )
    else:
        report.add(
            "setup.no_unused_pi",
            True,
            "Pi install and proof path removed from required pre-work",
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
        "Windows smoke runs the supported P6 prepare-only path": (
            smoke,
            'Write-Result -Name "p6.prepare_only"',
        ),
        "Windows workflow installs the x64 runtime": (
            workflow,
            VC_REDIST_X64_URL,
        ),
        "Windows workflow installs the official Goose CLI": (
            workflow,
            GOOSE_INSTALLER_URL,
        ),
        "Windows workflow runs P6 prepare-only": (
            workflow,
            ".\\scripts\\Start-P6.ps1",
        ),
        "Windows workflow runs P6 Node gates": (
            workflow,
            "node --test .\\tests\\p6.test.mjs",
        ),
    }
    missing = [label for label, (surface, token) in expected.items() if token not in surface]
    forbidden = {
        "HTML exact Goose version pin": (html, "GOOSE_VERSION"),
        "Windows smoke exact Goose version pin": (smoke, "GOOSE_VERSION"),
        "Windows workflow exact Goose version pin": (workflow, "GOOSE_VERSION"),
        "Windows smoke duplicates the P6 Goose flag list": (
            smoke,
            "goose.p6_run_surface",
        ),
    }
    missing.extend(
        f"forbidden: {label}"
        for label, (surface, token) in forbidden.items()
        if token in surface
    )
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


def check_p6_prepare_surface(report: Report) -> None:
    smoke = WINDOWS_SMOKE.read_text(encoding="utf-8-sig")
    workflow = WINDOWS_WORKFLOW.read_text(encoding="utf-8")
    required_files = [
        P6_START,
        P6_WAVE2,
        P6_ROOT / "MISSION.md",
        P6_ROOT / "clear_overnight_watch.yaml",
        P6_ROOT / "scripts" / "p6-lib.mjs",
        P6_ROOT / "scripts" / "prepare.mjs",
        P6_ROOT / "scripts" / "update.mjs",
        P6_ROOT / "scripts" / "verify.mjs",
        P6_TEST,
    ]
    missing = [
        str(path.relative_to(REPO_ROOT))
        for path in required_files
        if not path.is_file()
    ]
    if missing:
        report.add(
            "site.p6_prepare_surface",
            False,
            "missing: " + ", ".join(missing),
            hard=True,
        )
        return

    start = P6_START.read_text(encoding="utf-8-sig")
    wave2 = P6_WAVE2.read_text(encoding="utf-8-sig")
    recipe = (P6_ROOT / "clear_overnight_watch.yaml").read_text(encoding="utf-8")
    expected = {
        "P6 prepare-only switch": (start, "[switch]$PrepareOnly"),
        "P6 fixed current run default": (start, 'Join-Path $P6Root "runs\\current"'),
        "P6 reads Goose run help": (start, '@("run", "--help")'),
        "P6 checks native Developer capability": (start, '$helpText.Contains("--with-builtin")'),
        "P6 recipe validation": (start, '@("recipe", "validate", $SourceRecipe)'),
        "P6 live run adds Developer": (start, "--with-builtin developer"),
        "P6 two-output dashboard contract": (recipe, "Write exactly two mission outputs"),
        "P6 dashboard output": (recipe, "command_center.html"),
        "P6 mission state output": (recipe, "mission_state.json"),
        "P6 browser handoff": (start, 'Open-CommandCenter -Path (Join-Path $RunRoot "command_center.html")'),
        "P6 no-inference receipt": (start, "P6 PREPARE-ONLY PASS run=$RunRoot no model call started"),
        "P6 Wave 2 prepare-only switch": (wave2, "[switch]$PrepareOnly"),
        "P6 Wave 2 explicit run root": (wave2, "[string]$RunRoot"),
        "P6 Wave 2 selected intent": (wave2, "[string]$Intent"),
        "P6 Wave 2 live run adds Developer": (wave2, "--with-builtin developer"),
        "P6 Wave 2 passes intent": (wave2, "--intent $Intent"),
        "P6 Wave 2 browser handoff": (wave2, 'Open-CommandCenter -Path (Join-Path $RunRoot "command_center.html")'),
        "P6 Wave 2 no-inference receipt": (wave2, "P6 UPDATE PREPARE-ONLY PASS run=$RunRoot no model call started"),
        "pre-work authoritative P6 prepare result": (smoke, '"p6.prepare_only"'),
        "CI P6 current Node LTS lane": (workflow, 'node-version: "lts/*"'),
        "CI P6 checks the latest LTS": (workflow, "check-latest: true"),
        "CI P6 custom run root": (workflow, "-PrepareOnly -RunRoot $runRoot"),
        "CI P6 Node verifier tests": (workflow, "node --test .\\tests\\p6.test.mjs"),
    }
    absent = [
        label
        for label, (surface, token) in expected.items()
        if token not in surface
    ]
    forbidden = {
        "duplicated pre-work Goose flag probe": (smoke, "goose.p6_run_surface"),
        "P6 --no-profile": (start, "--no-profile"),
        "P6 --render-recipe probe": (start, "--render-recipe"),
        "P6 --no-session override": (start, "--no-session"),
        "P6 --params override": (start, "--params"),
        "P6 --max-turns override": (start, "--max-turns"),
        "P6 Wave 2 --no-profile": (wave2, "--no-profile"),
        "P6 Wave 2 --render-recipe probe": (wave2, "--render-recipe"),
        "P6 Wave 2 --no-session override": (wave2, "--no-session"),
        "P6 Wave 2 --params override": (wave2, "--params"),
        "P6 Wave 2 --max-turns override": (wave2, "--max-turns"),
        "P6 recipe extension allowlist": (recipe, "extensions:"),
        "P6 recipe settings restriction": (recipe, "settings:"),
    }
    violations = [
        label
        for label, (surface, token) in forbidden.items()
        if token in surface
    ]
    if absent or violations:
        detail = []
        if absent:
            detail.append("missing: " + ", ".join(absent))
        if violations:
            detail.append("forbidden: " + ", ".join(violations))
        report.add(
            "site.p6_prepare_surface",
            False,
            "; ".join(detail),
            hard=True,
        )
    else:
        report.add(
            "site.p6_prepare_surface",
            True,
            "native Developer launch, two-output mission, no-key prepare paths, and Node verifier gates present",
            hard=True,
        )


def check_registry_install_route(report: Report) -> None:
    registry = REGISTRY.read_text(encoding="utf-8")
    prework_registry = registry.split("var REGISTRY", 1)[0]
    expected = [
        'code: "B0"',
        'url: "checklists/prework-install.html"',
        '"gs-runtime"',
        '"g-three"',
    ]
    missing = [needle for needle in expected if needle not in registry]
    stale_prework = [
        marker
        for marker in ('"pi-install"', '"pi-verify"', '"pi-write"', '"pi-why"', '"g-four"')
        if marker in prework_registry
    ]
    missing.extend(f"stale pre-work id {marker}" for marker in stale_prework)
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
            "B0 routes to the install page, requires Goose, and contains no unused Pi proof ids",
            hard=True,
        )


def check_pi_pattern_lab(report: Report) -> None:
    page = PI_PAGE.read_text(encoding="utf-8")
    registry = REGISTRY.read_text(encoding="utf-8")
    package = json.loads(PI_PACKAGE.read_text(encoding="utf-8"))
    runtime = PI_RUNTIME.read_text(encoding="utf-8")
    test_source = PI_TEST.read_text(encoding="utf-8")
    workflow = STACK_FACTS_WORKFLOW.read_text(encoding="utf-8")

    expected_sources = [
        "01-prompt-chain.ts",
        "02-routing.ts",
        "03-parallel.ts",
        "04-orchestrator-workers.ts",
        "05-handoff.ts",
        "06-evaluator-optimizer.ts",
        "07-tool-loop.ts",
        "08-planner-executor.ts",
        "09-reflection.ts",
        "10-supervisor-tools.ts",
    ]
    expected_figures = [
        "pi-pattern-01-prompt-chain.webp",
        "pi-pattern-02-routing.webp",
        "pi-pattern-03-parallel.webp",
        "pi-pattern-04-orchestrator-workers.webp",
        "pi-pattern-05-handoff.webp",
        "pi-pattern-06-evaluator-optimizer.webp",
        "pi-pattern-07-tool-loop.webp",
        "pi-pattern-08-planner-executor.webp",
        "pi-pattern-09-reflection.webp",
        "pi-pattern-10-supervisor-tools.webp",
    ]
    missing_sources = [
        name for name in expected_sources
        if not (PI_ROOT / "src" / "patterns" / name).is_file()
    ]
    missing_figures = [
        name for name in expected_figures
        if not (PI_FIGURE_ROOT / name).is_file()
    ]

    dependencies = package.get("dependencies", {})
    expected_dependencies = {
        "@earendil-works/pi-agent-core": "0.83.0",
        "@earendil-works/pi-ai": "0.83.0",
    }
    wrong_dependencies = [
        f"{name}@{dependencies.get(name)!r}"
        for name, version in expected_dependencies.items()
        if dependencies.get(name) != version
    ]

    page_markers = [
        'data-context-for="PI"',
        'data-storage-key="ahb-checklist-pi"',
        "Setup-PiLab.ps1",
        "Verify-PiLab.ps1",
        "PI LAB VERIFY PASS patterns=10",
    ]
    for number, (source, figure) in enumerate(
        zip(expected_sources, expected_figures), start=1
    ):
        page_markers.extend(
            [
                f"Pattern {number:02d}",
                source,
                figure,
                f'data-check-id="pi-pattern-{number:02d}"',
                f"PI PATTERN {number:02d} PASS",
            ]
        )
    missing_page = [marker for marker in page_markers if marker not in page]

    runtime_markers = [
        "new Agent({",
        "createModels()",
        "xaiProvider()",
        'this.models.getModel("xai", modelId)',
        'runtime.models.checkAuth("xai")',
        "this.models.streamSimple.bind(this.models)",
    ]
    missing_runtime = [marker for marker in runtime_markers if marker not in runtime]

    registry_markers = [
        'code: "PI"',
        'kind: "exercise"',
        'url: "blocks/pi.html"',
        'codes: ["PI", "P6", "P7"]',
        'item.kind === "exercise"',
    ]
    missing_registry = [marker for marker in registry_markers if marker not in registry]
    sequence_ok = registry.find('code: "PI"') < registry.find('code: "P6"')

    forbidden = [
        marker for marker in (
            "@mariozechner/pi-",
            'id="ideas"',
            "YOUR ONE-SENTENCE",
            "tripwire",
            "kill switch",
        )
        if marker.lower() in page.lower() or marker in runtime
    ]
    test_markers = [
        'assert.deepEqual(ids, ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"])',
        "result.trace.length >= 2",
        "routing rejects output outside its two declared routes",
        "evaluator PASS still reaches the optimizer",
        "supervisor cannot satisfy both delegations by repeating one tool",
    ]
    missing_tests = [marker for marker in test_markers if marker not in test_source]
    workflow_markers = [
        '"site/blocks/pi.html"',
        '"site/js/shell.js"',
        "mission_flesh/pi/package-lock.json",
        "Test the Pi agentic-pattern implementations",
        "working-directory: mission_flesh/pi",
        "npm run check",
        "npm test",
    ]
    missing_workflow = [marker for marker in workflow_markers if marker not in workflow]

    problems = []
    if missing_sources:
        problems.append("missing sources: " + ", ".join(missing_sources))
    if missing_figures:
        problems.append("missing figures: " + ", ".join(missing_figures))
    if wrong_dependencies:
        problems.append("wrong dependencies: " + ", ".join(wrong_dependencies))
    if missing_page:
        problems.append("page missing: " + ", ".join(missing_page))
    if missing_runtime:
        problems.append("runtime missing: " + ", ".join(missing_runtime))
    if missing_registry or not sequence_ok:
        problems.append(
            "registry missing/order: "
            + ", ".join(missing_registry + ([] if sequence_ok else ["PI before P6"]))
        )
    if forbidden:
        problems.append("forbidden/stale: " + ", ".join(forbidden))
    if missing_tests:
        problems.append("tests missing: " + ", ".join(missing_tests))
    if missing_workflow:
        problems.append("workflow missing: " + ", ".join(missing_workflow))

    if problems:
        report.add("site.pi_pattern_lab", False, "; ".join(problems), hard=True)
    else:
        report.add(
            "site.pi_pattern_lab",
            True,
            "ten pinned Pi Agent Core implementations, colocated pattern diagrams, copy-paste runs, CI-backed offline tests, and Thursday-before-P6 route present",
            hard=True,
        )


def http_headers_text(
    url: str, headers: dict, timeout: float = 25.0
) -> Tuple[Optional[str], str]:
    """Like http_text, but for services that require specific request headers."""
    merged = {"User-Agent": UA}
    merged.update(headers)
    request = urllib.request.Request(url, headers=merged)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
            if response.headers.get("Content-Encoding") == "gzip":
                raw = gzip.decompress(raw)
            return raw.decode("utf-8", errors="replace"), f"HTTP {response.status}"
    except urllib.error.HTTPError as error:
        return None, f"HTTP {error.code}"
    except Exception as error:  # noqa: BLE001 - report staff-facing network failures
        return None, f"{type(error).__name__}: {error}"


def check_osint_feeds(report: Report) -> None:
    """The two public feeds the open source desk builds on.

    Soft by design: these are third-party services, and an outage is news about
    them rather than a broken repository.
    """
    body, detail = http_text(
        "https://opensky-network.org/api/states/all"
        "?lamin=51&lomin=-1&lamax=52&lomax=1"
    )
    report.add(
        "osint.opensky_channel",
        body is not None and '"states"' in body,
        detail if body is None else f"anonymous access still returns state vectors ({detail})",
        hard=False,
    )

    # Digitraffic requires gzip and asks callers to identify themselves.
    body, detail = http_headers_text(
        "https://meri.digitraffic.fi/api/ais/v1/vessels",
        {"Accept": "application/json", "Accept-Encoding": "gzip", "Digitraffic-User": UA},
    )
    report.add(
        "osint.digitraffic_channel",
        body is not None and '"mmsi"' in body,
        detail if body is None else f"keyless AIS metadata still served ({detail})",
        hard=False,
    )


def check_p2_inbound_surface(report: Report) -> None:
    registry = REGISTRY.read_text(encoding="utf-8")
    hcp = HCP_PAGE.read_text(encoding="utf-8")
    p2 = P2_PAGE.read_text(encoding="utf-8")
    manifest = (P2_MATERIAL / "MANIFEST.md").read_text(encoding="utf-8")
    expected = {
        "registry briefing": 'code: "HCP"',
        "registry route": 'codes: ["HCP", "P2", "MCP1", "MCP2", "P3", "OSD"]',
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


def check_p4_second_brain_surface(report: Report) -> None:
    registry = REGISTRY.read_text(encoding="utf-8")
    loops = LOOPS_PAGE.read_text(encoding="utf-8")
    p4 = P4_PAGE.read_text(encoding="utf-8")
    p5 = P5_PAGE.read_text(encoding="utf-8")
    expected = {
        "registry briefing": (registry, 'code: "LOOPS"'),
        "Wednesday route": (registry, 'codes: ["LOOPS", "P4", "P5"]'),
        "Gamma deck": (loops, "Control-Flow-Is-the-Product-nnbb430p72cg1wa"),
        "briefing completion": (loops, 'data-check-id="loops-complete"'),
        "P4 Windows launcher": (p4, "Start-P4.ps1"),
        "P4 writable vault root": (p4, "%USERPROFILE%\\Vaults\\p4-vault"),
        "P4 Obsidian MCP plugin": (p4, "Local REST API with MCP"),
        "P4 MCP endpoint": (p4, "http://127.0.0.1:27123/mcp/"),
        "P4 API-key boundary": (p4, "OBSIDIAN_REST_API_KEY"),
        "P4 cold retriever": (p4, "Cold retrieval only"),
        "P4 applied repair": (p4, "one applied repair"),
        "P4 fresh repair proof": (p4, "Retrieval/Repair_Check.md"),
        "P4 external integrity snapshot": (p4, "P4_INTEGRITY_"),
        "P4 mutation detection": (p4, "PASS disposable mutation detected"),
        "P4 verifier": (p4, "mission_flesh\\p4\\vault_seed\\tools\\verify_vault.py"),
        "P4 external manifest": (p4, "--write-manifest --external"),
        "P5 frozen before inventory": (p5, "STAGING_INV_BEFORE_[TODAY].json"),
        "P5 exact candidate output": (p5, "out\\triage_candidate.json"),
        "P5 isolated project": (p5, "Documents\\p5-staging"),
        "P5 role-aware session audit": (p5, "SESSION_AUDIT_[TODAY].json"),
        "P5 payload-free handoff": (p5, "P5_HANDOFF_[TODAY].md"),
    }
    required_files = [
        P4_SEED / "AGENTS.md",
        P4_SEED / ".opencode" / "agents" / "director.md",
        P4_SEED / ".opencode" / "agents" / "retriever.md",
        P4_SEED / "Harness" / "HARNESS_CARD.md",
        P4_SEED / "Harness" / "RUN_STATE.md",
        P4_SEED / "Retrieval" / "Repair_Check.md",
        P4_SEED / "tools" / "verify_vault.py",
    ]
    missing = [label for label, (surface, token) in expected.items() if token not in surface]
    forbidden = {
        "P4 obsolete cold-start demo": (p4, "P4 — Cold Start"),
        "P4-to-P5 artifact dependency": (p4.lower(), "p5"),
        "P4 stale handoff receipt": (p4, "HANDOFF_RECEIPT.md"),
        "P4 stale downstream baseline name": (p4, "P4_BASELINE_"),
        "P5 obsolete model diff baseline": (p5, "p4-vault_baseline"),
        "P5 broad exposed project": (p5, "choose your <code>Documents</code> folder"),
        "P5 P4 dependency": (p5.lower(), "p4-vault"),
        "P5 Obsidian dependency": (p5.lower(), "obsidian"),
        "P5 second-brain dependency": (p5.lower(), "second brain"),
        "P5 poisoned-acceptance dependency": (p5.lower(), "poisoned acceptance"),
    }
    missing.extend(
        f"forbidden: {label}" for label, (surface, token) in forbidden.items() if token in surface
    )
    missing.extend(str(path.relative_to(REPO_ROOT)) for path in required_files if not path.is_file())
    if missing:
        report.add(
            "site.p4_second_brain",
            False,
            "missing: " + ", ".join(missing),
            hard=True,
        )
    else:
        report.add(
            "site.p4_second_brain",
            True,
            "P4 MCP brain, cold repair, external integrity, and standalone P5 quarantine surfaces present",
            hard=True,
        )


def check_node_lts_claim(report: Report) -> None:
    """Verify the official Node channel still publishes a parseable current LTS."""
    data, status = http_json(NODE_INDEX_URL)
    if data is None:
        report.add(
            "node.lts_channel",
            False,
            f"could not fetch Node release index ({status})",
            hard=False,
        )
        return
    if not isinstance(data, list):
        report.add("node.lts_channel", False, "unexpected Node index payload", hard=True)
        return

    lts_rows = [row for row in data if isinstance(row, dict) and row.get("lts")]
    if not lts_rows:
        report.add("node.lts_channel", False, "Node index contains no LTS release", hard=True)
        return

    latest_lts = lts_rows[0]
    version = str(latest_lts.get("version", ""))
    if not re.fullmatch(r"v?\d+\.\d+\.\d+(?:[-+].*)?", version):
        report.add(
            "node.lts_channel",
            False,
            f"could not parse latest LTS version {version!r}",
            hard=True,
        )
        return

    report.add(
        "node.lts_channel",
        True,
        f"latest Node LTS is {version} ({latest_lts.get('lts')})",
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
        '$RELEASE_TAG = if ($RELEASE -eq "true") { "canary" } else { "stable" }',
        '"goose-$ARCH-pc-windows-msvc.zip"',
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
        check_p6_prepare_surface(report)
        check_registry_install_route(report)
        check_pi_pattern_lab(report)
        check_p2_inbound_surface(report)
        check_osint_feeds(report)
        check_p4_second_brain_surface(report)
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
