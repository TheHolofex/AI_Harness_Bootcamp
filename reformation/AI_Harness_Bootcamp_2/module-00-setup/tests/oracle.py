#!/usr/bin/env python3
"""Acceptance oracle for Module 0, implementing Reference v2 section 6.

Governing principle: a check that has never failed proves nothing. Every check here
has at least one killing mutation in mutations.py, and test_module_00.py asserts that
the mutation actually kills it. A check with no killing mutation fails C6.

Import surface:
    run(module_root) -> list[Result]
"""

from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

# --------------------------------------------------------------------------------------
# Result model

PASS, WARN, FAIL = "PASS", "WARN", "FAIL"


@dataclass(frozen=True)
class Result:
    cid: str
    state: str
    detail: str

    def __str__(self) -> str:
        return f"[{self.state}] {self.cid}: {self.detail}"


class Recorder:
    def __init__(self) -> None:
        self.results: list[Result] = []

    def record(self, cid: str, ok: bool, detail: str, warn_only: bool = False) -> None:
        state = PASS if ok else (WARN if warn_only else FAIL)
        self.results.append(Result(cid, state, detail))

    def check(self, cid: str, ok: bool, ok_detail: str, fail_detail: str) -> None:
        self.record(cid, ok, ok_detail if ok else fail_detail)


# --------------------------------------------------------------------------------------
# File discovery (C1: glob-derived, never a hand-maintained list)

PLATFORM_GLOB = "platforms/*.md"
# Files a learner is told to open, copy, or execute. Maintainer material is excluded by
# directory, so a new learner file is picked up automatically and a new maintainer file
# is not silently scanned as learner prose.
MAINTAINER_DIRS = {"reference", "evidence", "facilitator", "assessment", "tests", "reviews",
                   # Checker test data. Deliberately corrupted drafts, not learner prose --
                   # scanning them as prose reads every planted error as a writing defect.
                   "fixtures", "pass", "fail", "v1-superseded", "v2"}


def module_files(root: Path) -> list[Path]:
    out = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if any(part in MAINTAINER_DIRS for part in p.relative_to(root).parts[:-1]):
            continue
        if p.suffix in {".md", ".py", ".sh", ".ps1"}:
            out.append(p)
    return out


def learner_docs(root: Path) -> list[Path]:
    return [p for p in module_files(root) if p.suffix == ".md"]


def learner_scripts(root: Path) -> list[Path]:
    return [p for p in module_files(root) if p.suffix in {".py", ".sh", ".ps1"}]


# --------------------------------------------------------------------------------------
# Fence parsing (C2: every fence, regardless of info string)

FENCE_RE = re.compile(r"^```([^\n`]*)\n(.*?)^```[ \t]*$", re.M | re.S)


@dataclass(frozen=True)
class Fence:
    path: Path
    line: int
    info: str
    body: str

    @property
    def lang(self) -> str:
        return self.info.strip().lower().split()[0] if self.info.strip() else ""

    @property
    def statements(self) -> list[str]:
        return [ln for ln in self.body.splitlines() if ln.strip() and not ln.strip().startswith("#")]


def fences(paths: list[Path]) -> list[Fence]:
    out = []
    for p in paths:
        text = p.read_text(encoding="utf-8")
        for m in FENCE_RE.finditer(text):
            out.append(Fence(p, text[: m.start()].count("\n") + 1, m.group(1), m.group(2)))
    return out


SHELL_LANGS = {"bash", "sh", "zsh"}
PS_LANGS = {"powershell", "pwsh"}
# A fence is "executable" if a learner is meant to run it. `text` blocks count: the
# v1 oracle exempted them and shipped runnable `codex login` inside one.
EXEC_LANGS = SHELL_LANGS | PS_LANGS | {"text", "console"}


# --------------------------------------------------------------------------------------
# Helpers

def repo_root(root: Path) -> Path | None:
    for parent in [root, *root.parents]:
        if (parent / ".git").exists():
            return parent
    return None


def git(root: Path, *args: str) -> str:
    try:
        return subprocess.run(
            ["git", "-C", str(root), *args], capture_output=True, text=True, timeout=30
        ).stdout
    except Exception:
        return ""


def section_of(path: Path, line: int) -> str:
    """The nearest '## ' heading above a line."""
    heading = ""
    for i, ln in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if i > line:
            break
        if ln.startswith("## "):
            heading = ln[3:].strip()
    return heading


# --------------------------------------------------------------------------------------
# Class A — reachable, runnable, cannot strand the learner

CLONE_PATH_RE = re.compile(r"(?<![\w/$.-])((?:[\w.-]+/){1,6}[\w.-]+\.(?:sh|ps1|py))")
RELATIVE_USE_RE = re.compile(r"(?<![\w/$\"'.-])((?:[\w.-]+/){0,4}[\w.-]+\.(?:sh|ps1|py))")
PATH_ASSIGN_RE = re.compile(r"""PATH=["']?([^"'\n]*)["']?""")


def class_a(r: Recorder, root: Path) -> None:
    docs, plats = learner_docs(root), sorted(root.glob(PLATFORM_GLOB))
    repo = repo_root(root)
    fs = fences(docs)

    # A1 — every clone-relative path a learner executes exists
    missing = []
    for f in fs:
        if f.lang not in EXEC_LANGS:
            continue
        for cand in CLONE_PATH_RE.findall(f.body):
            if cand.startswith(("http", "/", "~")) or "$" in cand:
                continue
            if repo and (repo / cand).exists():
                continue
            if (root / cand).exists() or (f.path.parent / cand).exists():
                continue
            missing.append(f"{f.path.name}:{f.line} -> {cand}")
    r.check("A1", not missing, f"{len(fs)} fences; every executed path resolves",
            f"unresolvable executed paths: {missing[:6]}")

    # A2 — the module is tracked
    if repo:
        tracked = [ln for ln in git(repo, "ls-files", str(root.relative_to(repo))).splitlines() if ln]
        on_disk = [p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]
        r.check("A2", len(tracked) == len(on_disk) and tracked,
                f"{len(tracked)} files tracked, matching {len(on_disk)} on disk",
                f"tracked={len(tracked)} on_disk={len(on_disk)}; module is not published")
    else:
        r.record("A2", False, "no git repository above the module")

    # A3 — no learner block can terminate the learner's shell
    escapes = []
    for f in fs:
        if f.lang not in EXEC_LANGS:
            continue
        for i, ln in enumerate(f.body.splitlines(), 1):
            s = ln.strip()
            if re.search(r"(^|[;&|}]\s*)(exit|return)\b", s) and "$?" not in s:
                escapes.append(f"{f.path.name}:{f.line + i}")
    r.check("A3", not escapes, "no fence can exit the learner's shell",
            f"{len(escapes)} shell-terminating statements: {escapes[:8]}")

    # A4 — a fence using a relative script path establishes its directory first
    strays = []
    for f in fs:
        if f.lang not in EXEC_LANGS:
            continue
        body = f.body
        uses = [c for c in RELATIVE_USE_RE.findall(body)
                if not c.startswith(("http", "/", "~", "$")) and "/" in c]
        if not uses:
            continue
        establishes = re.search(r"^\s*(cd|Set-Location)\s+[\"']?(\$HOME|\$env:USERPROFILE|/|~)", body, re.M)
        if not establishes:
            strays.append(f"{f.path.name}:{f.line} uses {uses[0]}")
    r.check("A4", not strays, "every relative-path fence sets its own directory",
            f"fences using a relative path without cd: {strays[:6]}")

    # A5 — following the guide cannot dirty the clone
    gi = (repo / ".gitignore").read_text(encoding="utf-8") if repo and (repo / ".gitignore").exists() else ""
    r.check("A5", re.search(r"^\.obsidian/?\s*$", gi, re.M) is not None,
            ".obsidian/ is ignored, so opening the vault cannot dirty the clone",
            "the guides open the clone as an Obsidian vault but .obsidian/ is not ignored")

    # A6 — every fence parses in the shell it declares
    # Reference section 4.4: a check that cannot run reports FAIL with the reason.
    # Silently skipping the PowerShell half hid 48 of 205 fences behind a green PASS.
    bad, skipped, parsed = [], [], 0
    for f in fs:
        if f.lang in SHELL_LANGS:
            sh = shutil.which("zsh") if f.lang == "zsh" else shutil.which("bash")
            if not sh:
                skipped.append(f.lang)
                continue
            p = subprocess.run([sh, "-n"], input=f.body, capture_output=True, text=True)
            parsed += 1
            if p.returncode != 0:
                bad.append(f"{f.path.name}:{f.line} {p.stderr.strip()[:70]}")
        elif f.lang in PS_LANGS:
            if not shutil.which("pwsh"):
                skipped.append("powershell")
                continue
            script = (
                "$e=$null;[void][System.Management.Automation.Language.Parser]::ParseInput("
                "[Console]::In.ReadToEnd(),[ref]$null,[ref]$e);if($e.Count){$e[0].Message;exit 1}"
            )
            p = subprocess.run(["pwsh", "-NoProfile", "-Command", script],
                               input=f.body, capture_output=True, text=True)
            parsed += 1
            if p.returncode != 0:
                bad.append(f"{f.path.name}:{f.line} {p.stdout.strip()[:70]}")
    for p_ in learner_scripts(root):
        if p_.suffix == ".py":
            c = subprocess.run([sys.executable, "-m", "py_compile", str(p_)], capture_output=True, text=True)
            parsed += 1
            if c.returncode != 0:
                bad.append(f"{p_.name}: {c.stderr.strip()[-70:]}")
    if bad:
        r.record("A6", False, f"parse failures: {bad[:5]}")
    elif skipped:
        counts = {k: skipped.count(k) for k in sorted(set(skipped))}
        r.record("A6", False,
                 f"{parsed} units parsed, but {len(skipped)} could not be checked here "
                 f"({counts}); install the missing parser and re-run — a check that cannot "
                 f"run is not a check that passed")
    else:
        r.record("A6", True, f"all {parsed} fences and scripts parse in their declared language")

    # A7 — no block can persist an empty PATH element
    empties = []
    for f in fs + [Fence(p, 1, p.suffix[1:], p.read_text(encoding="utf-8")) for p in learner_scripts(root)]:
        for val in PATH_ASSIGN_RE.findall(f.body):
            if "::" in val or val.startswith(":") or val.endswith(":"):
                empties.append(f"{f.path.name}:{f.line}")
    r.check("A7", not empties, "no PATH assignment can contain an empty element",
            f"PATH assignments that can yield '.' on PATH: {sorted(set(empties))[:5]}")

    # A8 — credential entry is alone in its fence, and the read is its last statement
    unsafe = []
    for f in fs:
        if not re.search(r"read\s+-r\s+-s|Read-Host[^\n]*-AsSecureString", f.body):
            continue
        st = f.statements
        if not st or not re.search(r"read\s+-r\s+-s|Read-Host[^\n]*-AsSecureString", st[-1]):
            unsafe.append(f"{f.path.name}:{f.line}")
    r.check("A8", not unsafe, "hidden-input reads end their fence; no pasted line can be captured",
            f"credential reads with following lines in the same paste: {unsafe}")

    # A9 — slow or silent steps state their expected duration
    DURATION = re.compile(r"Expect this to take", re.I)
    SLOW = re.compile(r"\b(brew install|brew update|apt install|apt update|pacman -Syu|"
                      r"npm install|winget install|wsl --install|nvm install)\b")
    unannotated = []
    for f in fs:
        if f.lang not in EXEC_LANGS or not SLOW.search(f.body):
            continue
        prior = f.path.read_text(encoding="utf-8").splitlines()[max(0, f.line - 12): f.line]
        if not any(DURATION.search(ln) for ln in prior):
            unannotated.append(f"{f.path.name}:{f.line}")
    r.check("A9", not unannotated, "every slow step states its expected duration",
            f"slow steps with no duration annotation: {unannotated[:8]}")

    # A10 — installer inspection completes before the installer runs.
    # Keyed on the file the download actually produced, not on a list of known installer
    # names: a guide could otherwise suppress this check by renaming the file.
    def token(raw: str) -> str:
        raw = raw.strip().strip("\"'")
        raw = re.sub(r"^\$\{?\w+\}?/", "", raw)          # "$tmp/x.sh" -> "x.sh"
        return raw.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]

    DOWNLOAD = re.compile(
        r"(?:curl|wget)\s[^\n]*?(?:-o|--output)\s+(\S+)"          # curl -o FILE
        r"|Invoke-WebRequest\s[^\n]*?-OutFile\s+(\S+)"             # PowerShell
        r"|(?:curl|wget)\s[^\n]*?(?:-O|--remote-name)\b[^\n]*?(\S+/([\w.-]+\.(?:sh|ps1)))"  # -O keeps the remote name
    )
    EXEC = re.compile(r"(?:^|\|\s*|;\s*|&&\s*|\b[A-Z_]+=\S+\s+)(?:bash|sh|zsh|&)\s+(\S+)", re.M)
    # The pager's target may be a variable ($installer) rather than a filename, so match
    # any token on the line rather than requiring a .sh/.ps1 suffix.
    PAGER = re.compile(r"(?:less|more|Get-Content|bat)\b([^\n]*)")

    late = []
    for p in plats:
        text = p.read_text(encoding="utf-8")
        downloaded = {token(next(g for g in m.groups() if g)): m.start()
                      for m in DOWNLOAD.finditer(text)}
        for m in EXEC.finditer(text):
            name = token(m.group(1))
            # Only files this guide downloaded need inspecting. A script the learner got
            # by cloning the repository was reviewed when the repository was reviewed.
            if name not in downloaded:
                continue
            before = text[: m.start()]
            line_no = before.count("\n") + 1
            paged = any(token(t) == name
                        for line in PAGER.findall(before) for t in line.split())
            if not paged:
                late.append(f"{p.name}:{line_no} runs {name} without paging it first")
                continue
            # The "what to look for" instruction must land before the executing fence.
            exec_fence_start = before.rfind("```")
            if not re.search(r"Confirm|check that it names|look for", before[:exec_fence_start], re.I):
                late.append(f"{p.name}:{line_no} inspection guidance for {name} arrives after execution")
    r.check("A10", not late, "downloaded installers are inspected before they run",
            f"execute-before-inspect: {sorted(set(late))[:6]}")


# --------------------------------------------------------------------------------------
# Class B — the acceptance machinery discriminates

def class_b(r: Recorder, root: Path) -> None:
    # B1-B6 — the practice checker's own adequacy test carries these
    adequacy = subprocess.run([sys.executable, str(root / "tests/test_checker.py")],
                              capture_output=True, text=True)
    tail = (adequacy.stdout.strip().splitlines() or ["no output"])[-1]
    r.check("B1-B6", adequacy.returncode == 0,
            f"practice checker adequacy: {tail}",
            f"practice checker adequacy failed: {adequacy.stdout.strip()[-300:]}")

    # B7 — nothing on the learner's machine decides acceptance
    banned = re.compile(r"answer key|expected answer|graded case|solution file|"
                        r"hmac|hashlib\.(?:md5|sha)\w*\([^)]*(?:name|title|assignment)", re.I)
    leaks = []
    for p in module_files(root):
        for m in banned.finditer(p.read_text(encoding="utf-8")):
            # naming the concept is fine; shipping one is not
            line = p.read_text(encoding="utf-8")[: m.start()].count("\n") + 1
            leaks.append(f"{p.name}:{line} {m.group(0)!r}")
    r.check("B7", not leaks, "no deciding control, answer key, or keyed digest on the learner's machine",
            f"deciding material inside the module: {leaks[:5]}")

    # B8 — the tool proof binds the artifact to this run
    proof = (root / "shared/case/verify_tool_proof.py").read_text(encoding="utf-8")
    r.check("B8", "token" in proof and "st_mtime" in proof,
            "the tool proof requires this run's token and a write after it was issued",
            "the tool proof accepts any file with the right bytes")

    # B9 — the n8n check verifies n8n, not any listener
    n8n = (root / "shared/case/verify_n8n.py").read_text(encoding="utf-8")
    r.check("B9", "healthz" in n8n and "json" in n8n.lower(),
            "the n8n check requires an n8n-shaped reply, not just an open port",
            "the n8n check passes against any listener on port 5678")

    # B10 — the retry budget is bounded and stated where the learner reads it
    lab = (root / "shared/MODULE_00_LAB.md").read_text(encoding="utf-8")
    rubric = (root / "assessment/PUBLIC_RUBRIC.md").read_text(encoding="utf-8")
    r.check("B10", bool(re.search(r"two correction attempts|after two|no more than two", lab, re.I))
            and bool(re.search(r"two correction|no more than two", rubric, re.I)),
            "the correction budget is bounded at two attempts in the lab and the rubric",
            "the correction budget is not stated in both the lab and the rubric")


# --------------------------------------------------------------------------------------
# Class C — the oracle cannot be defeated by editing a file it does not read

FORBIDDEN_TOKENS = ("VERIFY:", "CUSTODY:", "PO00_RESULT", "oracle criterion", "M0-17")
HOME_PATH_RE = re.compile(r"/Users/[\w.-]+|/home/[\w.-]+|C:\\Users\\[\w.-]+")
# Placeholder home directories are how a guide *should* refer to a learner's own path.
PLACEHOLDER_HOME = re.compile(r"^(?:/Users|/home|C:\\Users)[/\\](?:yourname|youruser|username|user|you)$", re.I)

DANGEROUS = {
    r"sudo\s+npm\s+(?:install|i)\b[^\n]*\s-g\b": "sudo global npm",
    r"npm\s+(?:install|i)\b[^\n]*\s-g\b[^\n]*sudo": "sudo global npm",
    r"curl\s[^\n]*(?:--insecure|\s-k\b)": "insecure curl",
    r"chmod\s+-R\s+0?777": "world-writable recursive chmod",
    r"rm\s+-rf\s+(?:~|/\s|\$HOME|[^\n]*AI_Harness_Bootcamp)": "destructive recursive delete",
    r"Set-ExecutionPolicy\s+(?:Unrestricted|Bypass)\s+-Scope\s+(?:LocalMachine|CurrentUser)": "policy bypass",
    r"(?:echo|printf|Write-Output|Write-Host)\s[^\n]*(?:\$\{?(?:XAI|OPENAI)_API_KEY|\$env:(?:XAI|OPENAI)_API_KEY)": "secret echo",
    r"pacman\s+-Sy(?!u)": "Arch partial upgrade",
    r"(?:cd|clone|--prefix)\s+[^\n]*/mnt/c": "WSL work on the Windows filesystem",
}


def class_c(r: Recorder, root: Path) -> None:
    docs, scripts = learner_docs(root), learner_scripts(root)
    all_files = docs + scripts

    # C1 — nothing a learner is sent to read sits outside the scan set. The scan set is a
    # glob, so the only way a learner file escapes it is by living in a maintainer
    # directory. That is the failure this catches.
    scanned = {p.resolve() for p in all_files}
    escaped = []
    for p in docs:
        for target in re.findall(r"(?<!!)\[[^\]]+\]\(([^)#]+)\)", p.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("mailto:"):
                continue
            linked = (p.parent / target).resolve()
            if not linked.exists() or linked.is_dir():
                continue
            if linked.suffix in {".md", ".py", ".sh", ".ps1"} and linked not in scanned:
                escaped.append(f"{p.name} -> {linked.name}")
    r.check("C1", not escaped,
            f"scan set derived by glob: {len(all_files)} files, and every linked file is inside it",
            f"files a learner is sent to read that no scan reads: {sorted(set(escaped))[:5]}")

    # C2 — safety scan reads every fence, whatever the info string
    hits = []
    scanned = 0
    for f in fences(docs):
        scanned += 1
        for pat, label in DANGEROUS.items():
            if re.search(pat, f.body, re.I):
                hits.append(f"{label} at {f.path.name}:{f.line}")
    for p in scripts:
        for pat, label in DANGEROUS.items():
            if re.search(pat, p.read_text(encoding="utf-8"), re.I):
                hits.append(f"{label} in {p.name}")
    r.check("C2", not hits, f"{scanned} fences and {len(scripts)} scripts scanned, no dangerous form",
            f"dangerous forms: {hits[:6]}")

    # C3 — pins parsed from VERSIONS.md and asserted per file
    versions = (root / "shared/VERSIONS.md").read_text(encoding="utf-8")
    pins = dict(re.findall(r"^\|\s*(OpenCode|n8n)\s*\|\s*`?([\d.]+)`?\s*\|", versions, re.M))
    pkg = {"OpenCode": "opencode-ai", "n8n": "n8n"}
    wrong = []
    for p in sorted(root.glob(PLATFORM_GLOB)):
        body = p.read_text(encoding="utf-8")
        for name, ver in pins.items():
            for found in re.findall(rf"{pkg[name]}@([\d.]+)", body):
                if found != ver:
                    wrong.append(f"{p.name}: {pkg[name]}@{found} != {ver}")
    r.check("C3", bool(pins) and not wrong,
            f"pins {pins} parsed from VERSIONS.md and asserted per file",
            f"pin drift: {wrong[:6]}" if pins else "no pins parsed from VERSIONS.md")

    # C5 — structural criteria per unit, not per file
    gaps = []
    for p in sorted(root.glob(PLATFORM_GLOB)):
        text = p.read_text(encoding="utf-8")
        labelled = len(re.findall(r"\*\*Terminal:", text))
        runnable = len([f for f in fences([p]) if f.lang in SHELL_LANGS | PS_LANGS])
        if labelled < 1 or runnable == 0:
            gaps.append(f"{p.name}: {labelled} labels / {runnable} runnable fences")
            continue
        sections = re.findall(r"^## \d+\.[^\n]*", text, re.M)
        stops = len(re.findall(r"\*\*Stop here if:\*\*", text))
        sees = len(re.findall(r"\*\*You should see:\*\*", text))
        if stops < len(sections) - 1 or sees < len(sections) - 2:
            gaps.append(f"{p.name}: {len(sections)} sections but {stops} stops / {sees} expectations")
    r.check("C5", not gaps, "every platform section carries a terminal label, expectation and stop",
            f"structural gaps: {gaps}")

    # C7 — no internal token, and no personal path, anywhere a learner can reach
    leaks = []
    for p in all_files + [root / "reference/GAUNTLET_PROMPT.md"]:
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        for tok in FORBIDDEN_TOKENS:
            if tok in text:
                leaks.append(f"{p.name}: {tok}")
        for m in HOME_PATH_RE.findall(text):
            if PLACEHOLDER_HOME.match(m):
                continue
            leaks.append(f"{p.name}: personal path {m}")
    r.check("C7", not leaks, "no internal token or personal path in reachable files",
            f"leaks: {sorted(set(leaks))[:6]}")


# --------------------------------------------------------------------------------------
# Class D — claims match artifacts

def class_d(r: Recorder, root: Path) -> None:
    # D1 — every evidence row names a command that reproduces it and the stored output.
    # v1's rows ("Module structural/safety oracle | 171 PASS / 0 FAIL") named neither, so a
    # reader could not tell what had been run or re-run it.
    vpath = root / "evidence/REVIEW_VERDICT.md"
    vraw = vpath.read_text(encoding="utf-8") if vpath.exists() else ""
    # Every such section, not just the first: a second table appended below would
    # otherwise never be read, which is exactly how v1's scan set let files escape.
    sections = [m.group(1) for m in
                re.finditer(r"##\s*Executable evidence\s*\n(.*?)(?=\n##\s|\Z)", vraw, re.S)]
    rows = [row for s in sections
            for row in re.findall(r"^\|(?!\s*[-:]+\s*\|)([^|\n]+)\|([^|\n]+)\|([^|\n]+)\|\s*$", s, re.M)]
    rows = [x for x in rows if "Evidence" not in x[0]]
    bad = []
    # A backticked filename is not a command. The first token must be something runnable.
    RUNNABLE = re.compile(r"`\s*(?:python3?|bash|sh|zsh|pwsh|git|npm|npx|shasum|docker|curl|make)\b")
    for name, command, result in rows:
        if not RUNNABLE.search(command):
            bad.append(f"{name.strip()}: no runnable command")
            continue
        for ref in re.findall(r"`?(evidence/[\w./-]+)`?", result):
            if not (root / ref).exists():
                bad.append(f"{name.strip()}: {ref} missing")
        if "evidence/" not in result:
            bad.append(f"{name.strip()}: no stored output")
    r.check("D1", bool(rows) and not bad,
            f"{len(rows)} evidence rows, each naming a command and a stored output",
            f"evidence rows: {bad[:5]}" if rows else "no '## Executable evidence' table with rows")

    # D2 — every score is backed by a review that names its reviewer, kind, revision and
    # rubric, and Class F is only satisfied by the human panel the Reference requires.
    reviews = sorted((root / "reviews").glob("*.md")) if (root / "reviews").exists() else []
    verdict = root / "evidence/REVIEW_VERDICT.md"
    vtext = verdict.read_text(encoding="utf-8") if verdict.exists() else ""
    REQUIRED = ("Reviewer kind:", "Role:", "Module revision:", "Rubric:", "Total:")
    malformed = [p.name for p in reviews
                 if not all(f in p.read_text(encoding="utf-8") for f in REQUIRED)]
    human = [p for p in reviews
             if re.search(r"^Reviewer kind:\s*human", p.read_text(encoding="utf-8"), re.M | re.I)]
    # A Class F PASS may only be claimed when three human reviews exist.
    claims_class_f_pass = bool(re.search(r"Class F[^\n|]*\|[^\n|]*\bPASS\b", vtext))
    problems = []
    if not reviews:
        problems.append("no review files")
    if malformed:
        problems.append(f"reviews missing required fields: {malformed}")
    if claims_class_f_pass and len(human) < 3:
        problems.append(f"Class F claimed PASS with {len(human)} human reviews")
    r.check("D2", not problems,
            f"{len(reviews)} reviews ({len(human)} human), each naming reviewer, kind, revision and rubric",
            f"review record: {'; '.join(problems)}")

    # D3 — one budget, three consumers
    lab = (root / "shared/MODULE_00_LAB.md").read_text(encoding="utf-8")
    lab_minutes = sum(int(m) for m in re.findall(r"^\|[^|]+\|\s*(\d+)\s*minutes?\s*\|", lab, re.M))
    ref = (root / "reference/REFERENCE.md").read_text(encoding="utf-8")
    want = int(re.search(r"Learner working time inside it\*{0,2}\s*\|\s*\*{0,2}(\d+)", ref).group(1))
    run = (root / "facilitator/RUNBOOK.md").read_text(encoding="utf-8")
    spans = re.findall(r"^\|\s*(\d):(\d\d)[–-](\d):(\d\d)\s*\|", run, re.M)
    run_minutes = sum((int(c) * 60 + int(d)) - (int(a) * 60 + int(b)) for a, b, c, d in spans)
    r.check("D3", lab_minutes == want and run_minutes == want,
            f"lab {lab_minutes} min == runbook {run_minutes} min == Reference {want} min",
            f"budgets disagree: lab={lab_minutes} runbook={run_minutes} reference={want}")

    # D4 — deviations are recorded
    r.check("D4", (root / "reference/AMENDMENTS.md").exists(),
            "amendments to the Reference are recorded",
            "reference/AMENDMENTS.md is missing; deviations read as conformance")

    # D5 — platform status is stated per platform, never inferred
    platforms = ["PowerShell", "WSL", "macOS", "Ubuntu", "Arch"]
    stated = [p for p in platforms if re.search(rf"\|[^|\n]*{p}[^|\n]*\|[^|\n]*"
                                                r"(UNTESTED|untested|learner-run|executed|pilot)", vtext)]
    r.check("D5", len(stated) == len(platforms),
            "every platform has an explicit execution status",
            f"platforms without a stated execution status: {sorted(set(platforms) - set(stated))}")

    # M0-REF — the Reference is frozen and the hash matches
    href = root / "reference/REFERENCE.sha256"
    want_hash = href.read_text(encoding="utf-8").split()[0] if href.exists() else ""
    got = hashlib.sha256((root / "reference/REFERENCE.md").read_bytes()).hexdigest()
    r.check("REF", bool(want_hash) and want_hash == got, f"Reference frozen at {got[:12]}",
            f"Reference hash {got[:12]} does not match recorded {want_hash[:12]}")


# --------------------------------------------------------------------------------------
# Class E — learner records satisfy the skeleton gate

def class_e(r: Recorder, root: Path) -> None:
    lab = (root / "shared/MODULE_00_LAB.md").read_text(encoding="utf-8")
    rubric = (root / "assessment/PUBLIC_RUBRIC.md").read_text(encoding="utf-8")
    custody = (root / "assessment/CUSTODY_CONTRACT.md").read_text(encoding="utf-8")
    runbook = (root / "facilitator/RUNBOOK.md").read_text(encoding="utf-8")

    # E1 — capability-limit statement
    has_record = re.search(r"capability", lab, re.I) and re.search(r"limitation", lab, re.I)
    has_four = all(re.search(t, lab, re.I) for t in
                   (r"model output", r"product", r"harness", r"human decision"))
    r.check("E1", bool(has_record and has_four) and bool(re.search(r"capabilit", rubric, re.I)),
            "capability-limit statement is a required record with a rubric gate",
            "capability-limit statement missing from the lab or the rubric")

    # E2 — the falsifier is run, not merely stated. Both halves are required: an
    # instruction to run it, and a place to record what running it produced.
    runs = re.search(r"\brun (?:your|the) falsifier\b", lab, re.I)
    records = re.search(r"observed failure|what you (?:actually )?saw when you ran it", lab, re.I)
    r.check("E2", bool(runs and records and re.search(r"falsifier", rubric, re.I)),
            "the learner runs the falsifier and records the observed failure",
            f"falsifier is run: {bool(runs)}; observed failure recorded: {bool(records)}; "
            f"rubric gate: {bool(re.search(r'falsifier', rubric, re.I))}")

    # E3 — protected acceptance control confirmed and recorded
    r.check("E3", bool(re.search(r"protected acceptance", lab, re.I)) and
            bool(re.search(r"protected acceptance", rubric, re.I)),
            "the protected acceptance control is confirmed and its result recorded",
            "no protected acceptance control in the lab or rubric")

    # E4 — setup is not a PO-00 gate
    setup_gated = re.search(r"^\|\s*Setup\s*\|", rubric, re.M)
    r.check("E4", setup_gated is None,
            "setup is an entry condition, not a module gate",
            "the rubric makes setup a hard gate; a broken tool would hold PO-00")

    # E5 — every filesystem action the lab asks for is followed by an exact command.
    # Counting fences is not enough: prose can be added faster than fences.
    lines = lab.splitlines()
    IMPERATIVE = re.compile(r"^\s*(?:\d+\.\s*)?(?:Create|Copy|Make|Move|Rename)\b[^\n]*"
                            r"(?:folder|directory|file|packet|checker|copy)", re.I)
    orphans = []
    for i, line in enumerate(lines):
        if not IMPERATIVE.match(line):
            continue
        window = "\n".join(lines[i: i + 9])
        if "```" not in window:
            orphans.append(line.strip()[:60])
    r.check("E5", not orphans,
            "every filesystem action the lab asks for is followed by an exact command",
            f"prose-only filesystem actions: {orphans[:4]}")

    # E6 — supplied case with a protected control, not a separate unseen case
    invented = re.search(r"unseen case|different, unseen|graded unseen case", lab + rubric + custody + runbook, re.I)
    r.check("E6", invented is None,
            "scored on the supplied case with a protected control, per the course skeleton",
            f"a separate unseen graded case appears: {invented.group(0) if invented else ''}")


# --------------------------------------------------------------------------------------
# Class F — machine-checkable parts of the prose criteria

MAKING_OF = [
    (r"\bin this (?:section|module|session)\b", "meta-commentary"),
    (r"\bwhat we(?:'|’)ll cover\b", "meta-commentary"),
    (r"\bthe next session\b", "curriculum structure"),
    (r"\bModule 1\b", "curriculum structure"),
    (r"\byour Module 0 files remain evidence\b", "design rationale"),
    (r"\bthis (?:guide|document|page) is organi[sz]ed\b", "meta-commentary"),
    (r"\bwhich the guide reads from\b", "design rationale"),
]


def class_f(r: Recorder, root: Path) -> None:
    docs = learner_docs(root)
    joined = {p: p.read_text(encoding="utf-8") for p in docs}

    # F1 — PATH is defined at first use
    defines_path = any(re.search(r"PATH is the list|PATH,? the list|`?PATH`? is (?:a|the)", t)
                       for t in joined.values())
    r.check("F1", defines_path,
            "PATH is defined in ordinary language before it is used",
            "PATH heads a section in all five guides and is never defined")

    # F2 — no making-of content in learner files
    found = []
    for p, t in joined.items():
        for pat, label in MAKING_OF:
            for m in re.finditer(pat, t, re.I):
                found.append(f"{p.name}: {label} — {m.group(0)!r}")
    r.check("F2", not found, "no learner file explains how the course is built",
            f"making-of content: {sorted(set(found))[:6]}")

    # F3 — accessibility guidance names real assistive technology
    acc = (root / "shared/ACCESSIBILITY.md").read_text(encoding="utf-8")
    named = [t for t in ("VoiceOver", "NVDA", "JAWS", "Orca", "Narrator") if t in acc]
    r.check("F3", len(named) >= 3,
            f"accessibility guidance names real assistive technology: {named}",
            "accessibility guidance names no assistive technology and gives no operation")

    # F-VOICE — the aphorism tic. Panel dimensions 6 and 8 are human-judged, but one
    # failure mode is mechanical: the same "X is not Y" figure, carrying no instruction,
    # repeated across files. The first panel found it in four. Implementation addition
    # recorded in reference/AMENDMENTS.md; it raises the bar, it does not lower it.
    APHORISM = re.compile(r"(?<![.\w])([A-Z][^.!?\n]{8,90}?\b(?:is|are) not\b[^.!?\n]{3,70})\.")
    tics: dict[str, list[str]] = {}
    for p, t in joined.items():
        # Body prose only: no fenced blocks, no stop conditions, no table rows or bullets.
        prose = FENCE_RE.sub("", t)
        prose = "\n".join(ln for ln in prose.splitlines()
                          if ln[:1] not in {"-", "|", "#", ">", "*"} and "Stop here if" not in ln)
        for m in APHORISM.finditer(prose):
            s = m.group(1).strip()
            # An aphorism carries no instruction: no reader, no condition, no action.
            if re.search(r"\byou(?:r|rs)?\b|\bif\b|\bwhen\b|\bunless\b|\buntil\b", s, re.I):
                continue
            tics.setdefault(p.name, []).append(s[:70])
    r.check("F-VOICE", len(tics) <= 2,
            f"the declarative-antithesis figure appears in {len(tics)} learner file(s)",
            f"the same aphorism figure carries no instruction in {len(tics)} files: "
            f"{ {k: v[:1] for k, v in list(tics.items())[:5]} }")

    # F4 — stop conditions name observable conditions
    vague = []
    for p in sorted(root.glob(PLATFORM_GLOB)):
        for m in re.finditer(r"\*\*Stop here if:\*\*\s*([^\n]*)", p.read_text(encoding="utf-8")):
            if re.search(r"\b(seems|looks wrong|feels|something is off|anything unusual)\b", m.group(1), re.I):
                vague.append(f"{p.name}: {m.group(1)[:60]}")
    r.check("F4", not vague, "every stop condition names an observable state",
            f"judgment-based stop conditions: {vague}")


# --------------------------------------------------------------------------------------

def run(root: Path) -> list[Result]:
    r = Recorder()
    class_a(r, root)
    class_b(r, root)
    class_c(r, root)
    class_d(r, root)
    class_e(r, root)
    class_f(r, root)
    return r.results


if __name__ == "__main__":
    module = Path(__file__).resolve().parents[1]
    results = run(module)
    for res in results:
        print(res)
    bad = [x for x in results if x.state == FAIL]
    print(f"\n{len(results) - len(bad)} PASS / {len(bad)} FAIL")
    sys.exit(1 if bad else 0)
