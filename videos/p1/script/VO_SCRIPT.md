# P1 Intro — Locked VO Script

**Block:** P1 · The Daily Status Brief  
**Runtime target:** 2:20–2:40  
**Speaking rate:** ~145 wpm (calm, complete sentences)  
**Voice:** guide-beside — standing next to the operator, not pitching the course  
**Status:** LOCK CANDIDATE — approve before clip spend

---

## Full narration (read straight through)

By Friday of a normal week, Monday's status document is already wrong. Numbers moved. A blocker cleared. A new one landed. Somewhere a page still says otherwise.

Most people handle that by asking a chat model to summarize the latest. You get a fresh essay every time — different structure, different emphasis, and no clean way to tell what changed or whether any of it is true.

This afternoon you build the other thing: a machine that makes the answer. One folder of source reports. One fixed format. A citation on every claim. And a saved path that regenerates the whole brief on command. When the world changes, you rerun it. You can show why you trust the new brief, because you built the checks that catch it lying.

Here is what you are aiming at. You will leave with a Direction Brief marked LIVE — audience, format, citation rule, accept checks, and stop conditions pinned before the build. You will leave with a brief you can regenerate without re-explaining the mission from memory. You will audit at least five citations with your own eyes and force at least one correction. You will run two probes: a delta test that moves for the right reasons, and a stale-source test that fails out loud. And you will draw the line in the log between machine draft and your judgment.

How to think while you work with the harness. You own the mission, the bounds, and the verdict. The machine proposes and executes inside that frame. Independent evidence beats the model's self-assessment — when it says the citations look good, that is not an audit. Fluency is not verification. A complete-sounding draft still needs your call on what prints as fact, what stays flagged unverified, and what goes out under your name.

The afternoon runs in six stages. Set the contract. Meet the corpus. Build the machine. Audit the citations. Break it on purpose with both probes. Own the verdict, then close the operator pulse.

Open the P1 page, pin your operator chat, and start with the Direction Brief. The machine is an instrument. You are the operator.

---

## Word / time budget

| Metric | Value |
|---|---|
| Word count | ~348 |
| Est. duration @ 140 wpm | ~2:29 |
| Est. duration @ 145 wpm | ~2:24 |
| Est. duration @ 150 wpm | ~2:19 |
| Hard floor | ≥ 2:00 |
| Soft ceiling | ≤ 2:45 |

If TTS lands under 2:00, do **not** stretch with empty B-roll. Add one concrete sentence to the objectives or stages beat and re-render VO.

---

## Beat map (VO is the clock)

| Beat ID | Approx time | On-screen title | VO function |
|---|---|---|---|
| B01 Hook | 0:00–0:18 | FRIDAY'S STATUS IS ALREADY WRONG | Problem in the room |
| B02 Contrast | 0:18–0:38 | ONE-SHOT ESSAY ≠ MACHINE | What people do vs what we build |
| B03 Mission | 0:38–1:05 | THE MACHINE THAT MAKES THE ANSWER | Define the afternoon product |
| B04 Objectives | 1:05–1:40 | WHAT YOU LEAVE WITH | Learning objectives as artifacts |
| B05 Cothinking | 1:40–2:08 | HOW TO WORK WITH THE HARNESS | Symbiotic operator tips |
| B06 Map | 2:08–2:22 | SIX STAGES | Afternoon shape |
| B07 Close | 2:22–2:30 | OPEN P1 · START THE CONTRACT | CTA |

Exact timestamps will be rewritten after VO render using `ffprobe` durations in `script/timecodes.json`.

---

## Pronunciation / read notes

- **Direction Brief** — two words, slight weight on Brief  
- **LIVE** — spelled out as the status word, not “live stream”  
- **`[C-number]`** — say “C-tag” or “C-number,” not “bracket C pound”  
- **delta test / stale-source test** — plain, no drama  
- **harness** — the tool frame around the model (Codex app), not gym equipment  
- Pause half a beat after “catch it lying.”  
- Pause half a beat before “Open the P1 page…”

---

## Do not say (register guardrails)

- “Level up,” “supercharge,” “AI journey,” “take the wheel”  
- “You can’t break anything”  
- “In this exciting module”  
- Brand worship for Codex / OpenAI  
- Sci-fi voice (“neural nets weaving truth”)

---

## Source of truth

Grounded in:

- `site/blocks/p1.html` (lede, leave-with, ideas, six stages)  
- `DAY_PROJECT_TABLE.md` P1 row (objectives + thinking goals)  
- `MEMORY.md` cothinking standard  

If the block page changes, re-lock this script before regenerating media.
