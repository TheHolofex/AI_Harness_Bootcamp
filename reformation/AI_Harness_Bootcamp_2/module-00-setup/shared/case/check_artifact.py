#!/usr/bin/env python3
"""Practice check for the Harbor Depot desk note to Field Clinic S-3.

This is public, inspectable practice software. Its result is a mechanical check,
not independent evidence of source interpretation, safe use, or human qualification.
Any separate assessment needs an actual evaluator and independently held evidence.

What it does: for each fact the source packet confirms, it finds the sentences that
talk about that fact and decides whether the draft AFFIRMS it, DENIES it, or is
SILENT. Denying a confirmed fact fails. Promising a movement the source does not
confirm fails. A number is only accepted when it is attached to the thing it counts.

What it cannot do: decide whether the writing is clear, whether the tone suits the
reader, whether the email answers the request, or whether anyone should send it.
Those are yours.

One limit worth knowing before you rely on it. This finds a fact that was CONTRADICTED
using wording it recognises, and a specific that was INVENTED. It can still miss a
contradiction phrased in wording it does not recognise, sitting beside the correct
sentence rather than replacing it — because a draft can assert two incompatible things
at once and neither one looks wrong on its own. Independently compare the source and
the draft yourself; a mechanical pass does not settle that judgment.

Usage:  python3 check_artifact.py artifact.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------------------
# Reading the draft

ABBREVIATIONS = {"p.m.": "p<DOT>m<DOT>", "a.m.": "a<DOT>m<DOT>"}


def sentences(text: str) -> list[str]:
    """Split into clauses without breaking on '9:00 a.m.'.

    Semicolons split too. Two claims in one line are two claims.
    """
    for real, safe in ABBREVIATIONS.items():
        text = text.replace(real, safe)
    parts = re.split(r"(?<=[.!?])\s+|\s*;\s*|\n{2,}", text)
    out = []
    for part in parts:
        for safe, real in ((v, k) for k, v in ABBREVIATIONS.items()):
            part = part.replace(safe, real)
        if part.strip():
            out.append(" ".join(part.split()))
    return out


def words(text: str) -> list[str]:
    return re.findall(r"\b[\w’'-]+\b", text)


# --------------------------------------------------------------------------------------
# Deciding what a draft says about one fact

AFFIRMED, DENIED, SILENT = "affirms", "denies", "is silent about"


def stance(text: str, topic: str, affirm: str, deny: str) -> tuple[str, str]:
    """Does the draft affirm or deny this fact? A denial anywhere outranks an
    affirmation, because a reader who meets the denial acts on it."""
    affirming = ""
    for sentence in sentences(text):
        if not re.search(topic, sentence, re.I):
            continue
        affirmations = list(re.finditer(affirm, sentence, re.I))
        # "vehicle is assigned" inside "no vehicle is assigned" is not a
        # separate assertion. A contradictory occurrence elsewhere still wins.
        if deny and any(
            not any(a.start() <= d.start() and d.end() <= a.end() for a in affirmations)
            for d in re.finditer(deny, sentence, re.I)
        ):
            return DENIED, sentence
        if affirmations:
            affirming = affirming or sentence
    return (AFFIRMED, affirming) if affirming else (SILENT, "")


def attached(text: str, subject: str, patterns: tuple[str, ...]) -> set[int]:
    """Numbers in sentences about `subject` that match a count pattern.

    A phone number, a pen number, and a clock are not kit counts unless a pattern
    says they are.
    """
    found: set[int] = set()
    for sentence in sentences(text):
        if not re.search(subject, sentence, re.I):
            continue
        for pattern in patterns:
            for match in re.finditer(pattern, sentence, re.I):
                found.add(int(match.group(1)))
    return found


# --------------------------------------------------------------------------------------
# The facts this case confirms, and the promises it rejects

# A helpful draft smooths the documentation window into this sentence. The source
# does not say it. Presence fails, including inside a longer paragraph.
PROHIBITED_SENTENCE = (
    "you can expect the kits during the thursday and friday documentation window."
)

CONFIRMED = [
    ("subject line", r"(?im)^\s*subject\s*:", None, None),
    ("commodity", r"water-treatment kits", r"water-treatment kits", None),
    ("origin", r"harbor depot", r"harbor depot", None),
    ("destination", r"field clinic s-3", r"field clinic s-3", None),
    ("thursday", r"thursday", r"thursday", r"thursday[^.]*(?:cancell?ed|closed|not open)"),
    ("friday", r"friday", r"friday", r"friday[^.]*(?:cancell?ed|closed|not open)"),
    ("documentation hours", r"9:00\s*a\.?m\.?|5:00\s*p\.?m\.?|documentation window",
     r"9:00\s*a\.?m\.?[\s\S]{0,40}5:00\s*p\.?m\.?",
     r"\b(?:8:00|10:00|11:00|12:00|1:00|2:00|3:00|4:00|6:00|7:00)\s*[ap]\.?m\.?"),
    ("contact line", r"call|contact|phone|reach|555-0194", r"555-0194", None),
    ("pen 4", r"pen\s*4", r"pen\s*4", r"pen\s*(?!4\b)\d+"),
    ("custody not release", r"release|custody|staged|counted",
     r"not a release|releases no lot|not released",
     r"is a release|are released|has been released|counts as a release"),
    ("release owner", r"ivo marsh", r"ivo marsh", None),
    ("no vehicle", r"vehicle",
     r"assigns no vehicle|no vehicle is assigned",
     r"vehicle is assigned|a vehicle is assigned|assigns vehicle"),
    ("no permit", r"permit",
     r"approves no permit|no permit is approved",
     r"permit is approved|approves the permit"),
    ("no receipt", r"receipt",
     r"confirms no receipt|no receipt is confirmed",
     r"receipt is confirmed|confirms the receipt"),
    ("supportability unknown", r"supportable",
     r"unknown",
     r"is confirmed|can go|is supportable and ready"),
    ("class participants", r"class participants", r"class participants", None),
]

# Clock times the source does not contain. 9:00 a.m. and 5:00 p.m. are the window.
UNSUPPORTED_CLOCKS = re.compile(r"\b(\d{1,2}:\d{2})\s*(?:a\.?m\.?|p\.?m\.?)", re.I)
ALLOWED_CLOCKS = {"9:00", "5:00"}

# Promises a clerk would act on. A denial in the same sentence outranks the promise.
DELIVERY_PROMISE = (
    r"expect|pickup|deliver|ship|coming|stage",
    r"expect the kits|expect receipt|will deliver|will ship|ready for pickup|"
    r"stage the kits|treatment water is coming|pickup appointment|delivery promise",
    r"not a pickup|not a delivery|not a dispatch|do not tell|do not stage|"
    r"do not schedule|must not",
)

PROHIBITED_DISTRIBUTION = (
    r"\bforward (?:this|it)\b|\bpost (?:it|this)\b|\bpass (?:this|it) (?:along|on)\b|"
    r"\bshare (?:this|it)\b|\bsend (?:this|it) to (?:every|all|your)\b|\btell everyone\b|"
    r"radio station|press release|public bulletin|social media|neighborhood list|"
    r"every household|door to door|noticeboard|notice board|operations list"
)


def _normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def run(text: str) -> list[tuple[str, bool, str]]:
    checks: list[tuple[str, bool, str]] = []

    n = len(words(text))
    checks.append(("word count 130-190", 130 <= n <= 190, f"the draft has {n} words"))

    for name, topic, affirm, deny in CONFIRMED:
        if affirm is None:
            ok = re.search(topic, text) is not None
            checks.append((name, ok, "present" if ok else "not found in the draft"))
            continue
        verdict, sentence = stance(text, topic, affirm, deny or r"(?!x)x")
        checks.append((name, verdict == AFFIRMED,
                       "stated" if verdict == AFFIRMED
                       else f"the draft {verdict} it: {sentence[:90] or '(no sentence mentions it)'}"))

    requested = attached(text, r"request", (r"asks for (\d+)", r"requested(?: quantity)?[: ]+(\d+)"))
    checks.append(("requested 40", requested == {40},
                   "40 kits requested" if requested == {40}
                   else f"the draft attaches {sorted(requested) or 'no number'} to the request, not 40"))

    on_hand = attached(
        text,
        r"on hand|on-hand",
        (r"(\d+)\s+water-treatment kits on hand", r"on hand(?: count)?(?: is| of|:)?\s*(\d+)"),
    )
    checks.append(("on-hand 27", on_hand == {27},
                   "27 kits on hand" if on_hand == {27}
                   else f"the draft attaches {sorted(on_hand) or 'no number'} to on-hand, not 27"))

    prohibited = PROHIBITED_SENTENCE in _normalized(text)
    checks.append(("prohibited sentence", not prohibited,
                   "absent" if not prohibited
                   else "the draft contains the sentence that turns the window into a promise"))

    hs3_assigned = False
    hs3_sentence = ""
    for sentence in sentences(text):
        if not re.search(r"HS-3", sentence):
            continue
        if re.search(r"not assigned|no vehicle|does not assign|assigns no", sentence, re.I):
            continue
        if re.search(r"assign", sentence, re.I):
            hs3_assigned = True
            hs3_sentence = sentence
            break
    checks.append(("HS-3", not hs3_assigned,
                   "not assigned" if not hs3_assigned
                   else f"the draft assigns HS-3: {hs3_sentence[:80]}"))

    topic, affirm, deny = DELIVERY_PROMISE
    promised = ""
    for sentence in sentences(text):
        if not re.search(topic, sentence, re.I):
            continue
        if re.search(affirm, sentence, re.I) and not re.search(deny, sentence, re.I):
            promised = sentence
            break
    checks.append(("no delivery promise", not promised,
                   "not promised" if not promised
                   else f"the draft promises movement: {promised[:80]}"))

    go = re.search(r"\bGO\b", text)
    checks.append(("no GO", go is None,
                   "absent" if go is None else "the draft calls the movement a GO"))

    invented = [m.group(1) for m in UNSUPPORTED_CLOCKS.finditer(text)
                if m.group(1) not in ALLOWED_CLOCKS]
    checks.append(("no invented clock time", not invented,
                   "none" if not invented
                   else f"the source packet does not contain a clock time of {sorted(set(invented))}"))

    distributed = re.search(PROHIBITED_DISTRIBUTION, text, re.I)
    checks.append(("no prohibited distribution", distributed is None,
                   "stays with named class participants" if distributed is None
                   else f"the draft directs wider distribution: {distributed.group(0)!r}"))

    return checks


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("artifact.md")
    if not path.exists():
        print(f"HOLD: there is no file at {path}")
        return 1
    checks = run(path.read_text(encoding="utf-8"))
    for name, ok, why in checks:
        print(f"{'PASS' if ok else 'FAIL'}: {name} — {why}")
    failed = [name for name, ok, _ in checks if not ok]
    if failed:
        print(f"\nHOLD: {len(failed)} mechanical requirement(s) failed; this is practice only")
        return 1
    print("\nPASS: mechanical requirements passed; this is practice only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
