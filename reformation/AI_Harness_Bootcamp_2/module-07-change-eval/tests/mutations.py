"""Mutation witnesses for consumer-visible comparison failures."""
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
import json
import re


@dataclass(frozen=True)
class Mutation:
    cid: str
    what: str
    apply: Callable[[Path], None]


def replace(path, old, new):
    def apply(root):
        target = root / path
        text = target.read_text()
        if old not in text:
            raise ValueError(f"missing behavior mutation target: {path}")
        target.write_text(text.replace(old, new))
    return apply


def reference(root):
    target = root / "reference/REFERENCE.sha256"
    text = target.read_text()
    target.write_text(("0" if text[0] != "0" else "1") + text[1:])


def altered_candidate(root):
    case = root / "shared/cases/PC-03"
    source = json.loads((case / "sources.json").read_text())["sources"]["SB-PC-03#payload"]
    target = case / "candidate-a.md"
    target.write_text(re.sub(r"^\| Payload mass.*$", f"| Payload mass | {source['payload_kg']} kg | {source['locator']} |", target.read_text(), flags=re.M))


def overwrite(root):
    replace("scripts/evaluate_pairs.py", "if results_path.exists() or results_path.is_symlink():", "if False:")(root)
    replace("scripts/evaluate_pairs.py", 'results_path.open("x",', 'results_path.open("w",')(root)


def leaked_answer(root):
    target = root / "README.md"
    target.write_text(target.read_text() + "\nThe sealed source result is 246 kg.\n")


MUTATIONS = [
    Mutation("M7-REF", "corrupt frozen reference identity", reference),
    Mutation("M7-EVAL", "erase a supplied candidate failure", altered_candidate),
    Mutation("M7-EVAL", "replace existing result attempts", overwrite),
    Mutation("M7-GATE", "accept a mass that is only a digit substring", replace("shared/controls/hard_gates.py", 'return bool(re.search(r"(?<![\\w.])" + re.escape(needle) + r"(?!\\w)", record["text"]))', 'return needle in record["text"]')),
    Mutation("M7-FREEZE", "ignore changed batch manifest identity", replace("scripts/evaluate_pairs.py", "if config.get(variant) != actual:", "if False:")),
    Mutation("M7-SOURCE", "accept a source packet from another case", replace("scripts/evaluate_pairs.py", 'if packet["case_id"] != case_id:', 'if False:')),
    Mutation("M7-SOURCE", "skip source-schema validation during comparison", replace("scripts/evaluate_pairs.py", 'packet = gates.load_sources(sources)', 'packet = load_json(sources)')),
    Mutation("M7-RESTORE", "restore from a changed frozen authority", replace("scripts/restore_baseline.py", "if actual != expected:", "if False:")),
    Mutation("M7-LIVE-HOLD", "report success after an incomplete paid attempt", replace("scripts/stretch_runner.py", 'return 0 if status == "COMPLETE" else 1', 'return 0')),
    Mutation("M7-LEAK", "publish another case's sealed answer", leaked_answer),
]
