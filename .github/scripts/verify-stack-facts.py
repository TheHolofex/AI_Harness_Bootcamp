#!/usr/bin/env python3
"""Rotting-facts harness for AI Harness Bootcamp staff pins.

Runs on any machine (macOS/Linux/Windows) with Python 3.9+ and network.
Does NOT install tools and does NOT need API keys.

Exit 0 = all hard checks passed (soft warnings allowed).
Exit 1 = one or more hard failures.
Exit 2 = could not run (missing deps / network total failure).

What it covers:
  - Documented winget package IDs still resolve in winget-pkgs (or local winget)
  - OpenJS.NodeJS.LTS still exists and looks like an LTS line
  - npm opencode-ai latest vs winget SST.opencode drift signal
  - Goose docs host reachable
  - Sanity: course repo still contains load-bearing paths

What it does NOT cover (need Windows + keys + person):
  - Codex GUI, Computer Use, browser→deck
  - Funded key write proofs
  - Ollama tool-calling quality
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

# parents: scripts -> .github -> repo
REPO_ROOT = Path(__file__).resolve().parents[2]

UA = "AI-Harness-Bootcamp-stack-facts/1.0 (+staff)"


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

    @property
    def hard_failed(self) -> bool:
        return any((not r.ok) and r.hard for r in self.results)


def _auth_headers(url: str) -> dict:
    """Authenticate GitHub API calls when a token is available.

    Unauthenticated api.github.com allows 60 requests/hour *per IP*, and CI
    runners share IPs — so an unauthenticated run can 403 for reasons that have
    nothing to do with the course. GITHUB_TOKEN is injected by Actions; locally
    it is simply absent and the call falls back to unauthenticated.
    """
    if "api.github.com" not in url:
        return {}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    return {"Authorization": f"Bearer {token}"} if token else {}


def http_json(url: str, timeout: float = 25.0) -> Tuple[Optional[object], str]:
    headers = {"User-Agent": UA, "Accept": "application/json"}
    headers.update(_auth_headers(url))
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return json.loads(raw), f"HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        if e.code in (403, 429) and "api.github.com" in url and not _auth_headers(url):
            return None, f"HTTP {e.code} (unauthenticated GitHub rate limit — set GITHUB_TOKEN)"
        return None, f"HTTP {e.code}"
    except Exception as e:  # noqa: BLE001 — staff tool; surface any network failure
        return None, f"{type(e).__name__}: {e}"


def http_text(url: str, timeout: float = 25.0) -> Tuple[Optional[str], str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace"), f"HTTP {resp.status}"
    except Exception as e:  # noqa: BLE001
        return None, f"{type(e).__name__}: {e}"


def run_cmd(argv: List[str], timeout: float = 60.0) -> Tuple[int, str]:
    try:
        p = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        out = (p.stdout or "") + (p.stderr or "")
        return p.returncode, out.strip()
    except FileNotFoundError:
        return 127, "not found"
    except subprocess.TimeoutExpired:
        return 124, "timeout"


def check_repo_paths(rep: Report) -> None:
    required = [
        "MEMORY.md",
        "DAY_PROJECT_TABLE.md",
        "prework/INSTALL_GUIDE.md",
        "prework/FACILITATOR_NOTES.md",
        "instruments/p2_test_suite",
        "instruments/p3_frozen_brief",
        "instruments/p3_multi_agent",
        "instruments/p8_hold_degrade",
        "mission_flesh/p3/MANY_MINDS.md",
        "mission_flesh/p6/local_endpoint_notes.md",
        "mission_flesh/p6/watch_officer.yaml",
        "lead/BROWSER_DECK_DEMO.md",
        # lead/COHORT_PIN.md is staff-only: it lives under the gitignored staff/
        # tree and is never present in a student clone or on a CI runner.
        "operator/PASS_BARS.md",
        "site/week.html",
    ]
    missing = [p for p in required if not (REPO_ROOT / p).exists()]
    if missing:
        rep.add("repo.load_bearing_paths", False, "missing: " + ", ".join(missing), hard=True)
    else:
        rep.add("repo.load_bearing_paths", True, f"{len(required)} paths present", hard=True)


def winget_show(package_id: str) -> Tuple[bool, str]:
    code, out = run_cmd(["winget", "show", "--id", package_id, "-e", "--accept-source-agreements"], timeout=90)
    if code == 127:
        return False, "winget not available on this machine"
    if code != 0:
        return False, out[:300] or f"exit {code}"
    # Prefer Version line
    m = re.search(r"(?im)^\s*Version:\s*(\S+)", out)
    ver = m.group(1) if m else "unknown"
    return True, f"winget show ok · Version {ver}"


def _version_sort_key(v: str):
    return [int(x) if x.isdigit() else x for x in re.split(r"[.-]", v)]


def github_winget_latest(package_id: str) -> Tuple[bool, str, Optional[str]]:
    """Best-effort: search winget-pkgs via GitHub API path convention.

    OpenJS.NodeJS.LTS -> manifests/o/OpenJS/NodeJS/LTS
    SST.opencode      -> manifests/s/SST/opencode

    Returns (ok, detail, latest_version_or_None).
    """
    parts = package_id.split(".")
    if len(parts) < 2:
        return False, "bad package id", None
    publisher = parts[0]
    # Remaining segments are path under publisher (NodeJS.LTS -> NodeJS/LTS)
    rest = "/".join(parts[1:])
    letter = publisher[0].lower()
    url = (
        "https://api.github.com/repos/microsoft/winget-pkgs/contents/manifests/"
        f"{letter}/{publisher}/{rest}"
    )
    data, status = http_json(url)
    if data is None:
        return False, status, None
    if isinstance(data, list) and data:
        names = [x.get("name", "") for x in data if isinstance(x, dict)]
        vers = [n for n in names if re.match(r"^\d", n)]
        sample = sorted(vers, key=_version_sort_key)[-1] if vers else names[0]
        latest = sample if vers else None
        return True, f"winget-pkgs has {publisher}/{rest} (e.g. {sample})", latest
    return False, "empty or unexpected API payload", None


def github_winget_manifest_exists(package_id: str) -> Tuple[bool, str]:
    ok, detail, _latest = github_winget_latest(package_id)
    return ok, detail


# Package ids this harness watches. Keep in step with prework/INSTALL_GUIDE.md —
# check_guide_ids_covered() fails if the guide installs something absent here,
# so the two lists cannot drift apart silently.
WATCHED_WINGET = [
    ("Git.Git", True),
    ("OpenJS.NodeJS.LTS", True),
    ("SST.opencode", True),
    ("Python.Python.3.14", False),  # minor floats between cohorts; soft
    ("Obsidian.Obsidian", False),
    ("Microsoft.PowerShell", False),  # optional PS7 install in guide section 1
    ("Ollama.Ollama", False),  # optional local-model stretch in guide section 14b
]

# Store-delivered ids have no winget-pkgs manifest, so they are not checkable here.
NOT_IN_WINGET_PKGS = {"9PLM9XGG6VKS"}


def check_guide_ids_covered(rep: Report) -> None:
    """Every winget id the guide tells a student to install must be watched above.

    This is the anti-drift check on the harness itself. Without it, the list can
    quietly diverge from the guide and keep reporting green about the wrong ids.
    """
    guide = REPO_ROOT / "prework" / "INSTALL_GUIDE.md"
    if not guide.exists():
        rep.add("guide.winget_ids_covered", False, "prework/INSTALL_GUIDE.md missing", hard=True)
        return
    text = guide.read_text(encoding="utf-8")
    found = set(re.findall(r"winget install[^\n]*?--id\s+([A-Za-z0-9._]+)", text))
    found |= set(re.findall(r"winget install\s+([A-Z][A-Za-z0-9._]*\.[A-Za-z0-9._]+)", text))
    found -= NOT_IN_WINGET_PKGS
    watched = {p for p, _ in WATCHED_WINGET}
    missing = sorted(found - watched)
    if missing:
        rep.add(
            "guide.winget_ids_covered",
            False,
            "guide installs ids this harness does not check: " + ", ".join(missing),
            hard=True,
        )
    else:
        rep.add(
            "guide.winget_ids_covered",
            True,
            f"all {len(found)} guide winget ids are watched",
            hard=True,
        )


def check_winget_ids(rep: Report) -> None:
    packages = WATCHED_WINGET
    have_winget = run_cmd(["winget", "--version"])[0] == 0
    for pkg, hard in packages:
        if have_winget:
            ok, detail = winget_show(pkg)
            if not ok and "not available" not in detail.lower():
                # fall through to github
                ok2, detail2 = github_winget_manifest_exists(pkg)
                if ok2:
                    rep.add(f"winget.{pkg}", True, f"{detail2} (local winget show failed: {detail[:80]})", hard=hard)
                else:
                    rep.add(f"winget.{pkg}", False, f"local: {detail[:120]}; api: {detail2}", hard=hard)
            else:
                rep.add(f"winget.{pkg}", ok, detail, hard=hard)
        else:
            ok, detail = github_winget_manifest_exists(pkg)
            rep.add(f"winget.{pkg}", ok, detail + " (no local winget)", hard=hard)


def check_node_lts_claim(rep: Report) -> None:
    """Course claims OpenJS.NodeJS.LTS lands in 22.22–24.x band for n8n."""
    data, status = http_json("https://nodejs.org/dist/index.json")
    if not isinstance(data, list):
        rep.add("node.lts_schedule", False, f"could not fetch node dist index ({status})", hard=False)
        return
    lts = [row for row in data if row.get("lts")]
    if not lts:
        rep.add("node.lts_schedule", False, "no LTS entries in index", hard=True)
        return
    # newest LTS first in index.json
    latest_lts = lts[0]
    ver = str(latest_lts.get("version", "")).lstrip("v")
    major = int(ver.split(".")[0]) if ver else -1
    # soft band warning if outside 22-24 inclusive majors currently documented
    in_band = major in (22, 24) or (22 <= major <= 24)
    if in_band:
        rep.add("node.lts_schedule", True, f"latest Node LTS is v{ver} (lts={latest_lts.get('lts')})", hard=True)
    else:
        rep.add(
            "node.lts_schedule",
            False,
            f"latest Node LTS is v{ver} — MEMORY/n8n band may need a rewrite (was 22.22–24.x)",
            hard=True,
        )


def check_opencode_channel_drift(rep: Report) -> None:
    npm_data, npm_status = http_json("https://registry.npmjs.org/opencode-ai/latest")
    npm_ver = None
    if isinstance(npm_data, dict) and npm_data.get("version"):
        npm_ver = str(npm_data["version"])
        rep.add("opencode.npm_latest", True, f"opencode-ai@{npm_ver}", hard=True)
    else:
        rep.add("opencode.npm_latest", False, f"npm registry failed ({npm_status})", hard=True)

    winget_ver = None
    if run_cmd(["winget", "--version"])[0] == 0:
        ok, detail = winget_show("SST.opencode")
        m = re.search(r"Version\s+(\S+)", detail)
        if ok and m:
            winget_ver = m.group(1)
            rep.add("opencode.winget_version", True, f"SST.opencode@{winget_ver}", hard=False)
        else:
            rep.add("opencode.winget_version", False, detail[:200], hard=False)
            ok2, detail2, latest = github_winget_latest("SST.opencode")
            if ok2 and latest:
                winget_ver = latest
                rep.add("opencode.winget_manifest", True, f"{detail2} (fallback)", hard=False)
    else:
        ok, detail, latest = github_winget_latest("SST.opencode")
        rep.add("opencode.winget_manifest", ok, detail, hard=False)
        if ok and latest:
            winget_ver = latest

    if npm_ver and winget_ver and npm_ver != winget_ver:
        rep.add(
            "opencode.channel_drift",
            False,
            f"npm {npm_ver} != winget {winget_ver} — pin must name CHANNEL+version",
            hard=False,  # warning: expected sometimes; staff must still pin channel
        )
    elif npm_ver and winget_ver:
        rep.add("opencode.channel_drift", True, f"npm and winget both {npm_ver}", hard=False)
    elif npm_ver and not winget_ver:
        rep.add(
            "opencode.channel_drift",
            False,
            f"npm {npm_ver}; winget version unknown — still pin CHANNEL+version",
            hard=False,
        )


def check_goose_docs(rep: Report) -> None:
    text, status = http_text("https://goose-docs.ai")
    if text and ("goose" in text.lower() or "provider" in text.lower()):
        rep.add("goose.docs_reachable", True, status, hard=False)
    else:
        rep.add("goose.docs_reachable", False, status, hard=False)


def check_memory_mentions_pins(rep: Report) -> None:
    mem = (REPO_ROOT / "MEMORY.md").read_text(encoding="utf-8")
    need = [
        "SST.opencode",
        "OpenJS.NodeJS.LTS",
        "OPENCODE_DISABLE_CLAUDE_CODE",
        "p3_multi_agent",
        "local_endpoint_notes",
        "COHORT_PIN",
        "BROWSER_DECK_DEMO",
    ]
    missing = [n for n in need if n not in mem]
    if missing:
        rep.add("memory.pin_surface", False, "MEMORY.md missing: " + ", ".join(missing), hard=True)
    else:
        rep.add("memory.pin_surface", True, "load-bearing pin strings present", hard=True)


def main() -> int:
    print(f"repo: {REPO_ROOT}")
    rep = Report()
    try:
        check_repo_paths(rep)
        check_memory_mentions_pins(rep)
        check_guide_ids_covered(rep)
        check_winget_ids(rep)
        check_node_lts_claim(rep)
        check_opencode_channel_drift(rep)
        check_goose_docs(rep)
    except Exception as e:  # noqa: BLE001
        print(f"[FAIL] harness.crash: {type(e).__name__}: {e}", file=sys.stderr)
        return 2

    hard_fails = [r for r in rep.results if not r.ok and r.hard]
    soft_fails = [r for r in rep.results if not r.ok and not r.hard]
    print()
    print(f"summary: {len(rep.results)} checks · hard_fail={len(hard_fails)} · warn={len(soft_fails)}")
    if hard_fails:
        print("hard failures:")
        for r in hard_fails:
            print(f"  - {r.name}: {r.detail}")
        return 1
    if soft_fails:
        print("warnings (pin sheet still required):")
        for r in soft_fails:
            print(f"  - {r.name}: {r.detail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
