#!/usr/bin/env python3
"""Mutation corpus: proof that the oracle's checks can fail. Reference v2 section 6 C6.

Each mutation breaks the module in exactly one way and names the criterion that must
catch it. A criterion with no mutation here is unproven, and test_module_00.py fails on
that. This is DeMillo/Lipton/Sayward mutation adequacy (1978) pointed at a document set:
a check that no mutant kills is not a check.

Mutations append or create wherever possible rather than editing existing prose, so the
corpus survives ordinary revision of the module.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class Mutation:
    cid: str                      # criterion that must FAIL
    what: str                     # what was broken
    apply: Callable[[Path], None]


def append(rel: str, text: str) -> Callable[[Path], None]:
    def go(root: Path) -> None:
        p = root / rel
        p.write_text(p.read_text(encoding="utf-8") + text, encoding="utf-8")
    return go


def sub(rel: str, pattern: str, repl: str, required: bool = True, count: int = 0) -> Callable[[Path], None]:
    """Replace ALL occurrences by default. Replacing only the first leaves a second copy
    behind, and a mutation that only half-breaks the module proves nothing."""
    def go(root: Path) -> None:
        p = root / rel
        text = p.read_text(encoding="utf-8")
        new, n = re.subn(pattern, repl, text, count=count, flags=re.M | re.I)
        if required and n == 0:
            raise AssertionError(f"mutation anchor {pattern!r} not found in {rel}")
        p.write_text(new, encoding="utf-8")
    return go


def drop(rel: str) -> Callable[[Path], None]:
    def go(root: Path) -> None:
        (root / rel).unlink()
    return go


GUIDE = "platforms/macos.md"
LAB = "shared/MODULE_00_LAB.md"
RUBRIC = "assessment/PUBLIC_RUBRIC.md"

MUTATIONS: list[Mutation] = [
    # ---- Class A: reachable, runnable, cannot strand the learner
    Mutation("A1", "a guide runs a script that is not in the repository",
             append(GUIDE, "\n```bash\nbash scripts/does-not-exist.sh\n```\n")),
    Mutation("A2", "the module is no longer tracked by git",
             lambda root: subprocess.run(["git", "-C", str(root), "rm", "--cached", "-r", "-q", "."],
                                         capture_output=True)),
    Mutation("A3", "a learner block can terminate the learner's shell",
             append(GUIDE, "\n```bash\ntest -d /nowhere || exit 1\n```\n")),
    Mutation("A4", "a block runs a relative script without establishing its directory",
             append(GUIDE, "\n```bash\nbash scripts/verify-setup.sh\n```\n")),
    Mutation("A5", "opening the vault would dirty the clone",
             lambda root: sub(".gitignore", r"^\.obsidian/?\s*$", "# removed")(root.parent)
             if (root.parent / ".gitignore").exists() else None),
    Mutation("A6", "a fence does not parse in the shell it declares",
             append(GUIDE, "\n```bash\nif [ -z \"$x\" ; then printf 'broken\\n'\n```\n")),
    Mutation("A7", "a block persists an empty PATH element",
             append(GUIDE, "\n```bash\nexport PATH=\"$HOME/.local/bin::$PATH\"\n```\n")),
    Mutation("A8", "a pasted line after the credential read would be captured as the key",
             append(GUIDE, "\n```bash\nIFS= read -r -s XAI_API_KEY\nexport XAI_API_KEY\n```\n")),
    Mutation("A9", "a slow step does not say how long it takes",
             append(GUIDE, "\nNow install the extras.\n\n```bash\nbrew install jq\n```\n")),
    Mutation("A10", "an installer runs without being inspected",
             append(GUIDE, "\n```bash\ncurl -fsSL https://example.invalid/download_cli.sh -o /tmp/x.sh\n"
                           "bash /tmp/x.sh\n```\n")),

    # ---- Class B: the acceptance machinery discriminates
    Mutation("B1-B6", "the practice checker stops binding numbers to their subject",
             sub("shared/case/check_artifact.py",
                 r"capacity = counted\(text, [^)]*\)",
                 'capacity = {60} if re.search(r"\\b60\\b", text) else set()')),
    Mutation("B7", "a graded answer key ships inside the module",
             lambda root: (root / "shared/case/ANSWERS.md").write_text(
                 "# Expected answer\n\nThe graded case answer key.\n", encoding="utf-8")),
    Mutation("B8", "the tool proof accepts any file with the right bytes",
             sub("shared/case/verify_tool_proof.py", r"st_mtime", "st_size")),
    Mutation("B9", "the n8n check passes against any listener on the port",
             sub("shared/case/verify_n8n.py", r"healthz", "")),
    Mutation("B10", "the correction budget is removed from the rubric",
             sub(RUBRIC, r"(?i)no more than two[^|\n]*", "as many attempts as needed")),

    # ---- Class C: the oracle cannot be defeated by editing a file it does not read
    Mutation("C1", "a file the learner is sent to read is parked where the scan does not look",
             lambda root: ((root / "reference/EXTRA_HANDOUT.md").write_text(
                 "# Extra handout\n\n```text\nsudo npm install -g something -g\n```\n", encoding="utf-8"),
                 append("README.md", "\nRead the [extra handout](reference/EXTRA_HANDOUT.md).\n")(root))),
    Mutation("C2", "a dangerous command hides in a new learner file",
             lambda root: (root / "shared/case/EXTRA_HANDOUT.md").write_text(
                 "# Extra handout\n\n```text\nsudo npm install --global something -g\n```\n", encoding="utf-8")),
    Mutation("C2", "a dangerous command hides in a ```text fence",
             append(LAB, "\n```text\nsudo npm install --global whatever -g\n```\n")),
    Mutation("C3", "one guide pins a version that disagrees with VERSIONS.md",
             append("platforms/ubuntu.md", "\n```bash\nnpm install --global opencode-ai@0.9.0\n```\n")),
    Mutation("C5", "a platform guide loses its expected-value and stop lines",
             sub("platforms/arch-linux.md", r"\*\*You should see:\*\*", "It works.", required=False)),
    Mutation("C7", "an internal token reaches a learner file",
             append(LAB, "\nRecord PO00_RESULT when the run finishes.\n")),

    # ---- Class D: claims match artifacts
    Mutation("D1", "an evidence row claims a result with no command behind it",
             append("evidence/REVIEW_VERDICT.md", "\n## Executable evidence\n\n"
                    "| Evidence | Command | Result |\n|---|---|---|\n"
                    "| Everything worked | trust me | 171 PASS / 0 FAIL |\n")),
    Mutation("D2", "a review stops declaring what kind of reviewer produced it",
             lambda root: sub(f"reviews/{sorted(p.name for p in (root / 'reviews').glob('*.md'))[0]}",
                              r"^Reviewer kind:.*$", "")(root)),
    Mutation("D2", "a Class F pass is claimed without the human panel",
             lambda root: (append("evidence/REVIEW_VERDICT.md",
                                  "\n| Class F prose panel | PASS |\n")(root),
                           [sub(str(p.relative_to(root)), r"^Reviewer kind:\s*human", "Reviewer kind: model",
                                required=False)(root) for p in (root / "reviews").glob("*.md")])),
    Mutation("D3", "the lab timebox stops summing to the Reference budget",
             sub(LAB, r"^\|([^|\n]+)\|\s*(\d+) minutes\s*\|",
                 lambda m: f"|{m.group(1)}| {int(m.group(2)) + 25} minutes |")),
    Mutation("D4", "the amendment record is deleted",
             drop("reference/AMENDMENTS.md")),
    Mutation("D5", "a platform loses its stated execution status",
             sub("evidence/REVIEW_VERDICT.md", r"^\|[^|\n]*Arch[^\n]*\n", "", required=False)),
    Mutation("REF", "the frozen Reference is edited without re-freezing",
             append("reference/REFERENCE.md", "\nAn unrecorded change.\n")),

    # ---- Class E: learner records satisfy the skeleton gate
    Mutation("E1", "the capability-limit statement is removed from the rubric",
             sub(RUBRIC, r"(?i)capabilit\w*", "xxxx")),
    Mutation("E2", "the falsifier is stated but never run",
             sub(LAB, r"(?i)run your falsifier", "note your falsifier")),
    Mutation("E3", "the protected acceptance control disappears from the lab",
             sub(LAB, r"(?i)protected acceptance", "local")),
    Mutation("E4", "setup becomes a hard gate of the module result",
             sub(RUBRIC, r"^\|\s*Delegation\s*\|", "| Setup | fresh terminal finds the tools |", required=False)),
    Mutation("E5", "filesystem actions go back to prose with no command",
             append(LAB, "\nCreate a folder for your notes.\nCopy the source packet into it.\n"
                         "Create a folder for the changed draft.\nCopy the checker into it.\n"
                         "Create a folder for the handoff.\nMake a folder for your evidence.\n")),
    Mutation("E6", "a separate unseen graded case reappears",
             append(RUBRIC, "\nThe graded attempt uses a different, unseen case.\n")),

    # ---- Class F: the prose serves the reader
    # PATH may be defined in more than one learner file; the mutation has to remove every
    # definition, or it proves only that one of them was redundant.
    Mutation("F1", "PATH is used everywhere and defined nowhere",
             lambda root: [sub(str(p.relative_to(root)),
                               r"PATH is the list|PATH,? the list|`?PATH`? is (?:a|the)",
                               "PATH is important", required=False)(root)
                           for p in root.rglob("*.md")]),
    Mutation("F2", "making-of content returns to a learner page",
             append(LAB, "\nIn this section we will cover what the next session expects.\n")),
    Mutation("F3", "accessibility guidance stops naming assistive technology",
             sub("shared/ACCESSIBILITY.md", r"VoiceOver|NVDA|JAWS|Orca|Narrator", "a screen reader")),
    Mutation("F-VOICE", "the same instruction-free aphorism spreads across learner files",
             lambda root: [append(str(p.relative_to(root)),
                                  "\nA green result is not a correct result.\n")(root)
                           for p in sorted(root.rglob("*.md"))
                           if p.parent.name in {"shared", "platforms"} or p.name == "README.md"]),
    Mutation("F4", "a stop condition becomes a judgment call",
             append("platforms/ubuntu.md", "\n**Stop here if:** anything unusual happens.\n")),
]
