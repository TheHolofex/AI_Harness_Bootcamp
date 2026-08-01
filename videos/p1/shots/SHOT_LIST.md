# P1 Intro — Shot List

**Master clock:** VO file `audio/p1_vo.wav` (generate first)  
**Output:** 1920×1080, 30 fps, yuv420p, AAC 48 kHz  
**Assembly:** `assembly/build_p1_intro.sh` after clips land in `clips/`

Timestamps below are **design targets**. After VO render, update `script/timecodes.json` and shift cut points to word boundaries.

| Shot | Start | End | Dur | Beat | Visual source | Clip filename | Overlay title (ffmpeg burn-in) |
|---|---|---|---|---|---|---|---|
| S01 | 0:00 | 0:08 | 8s | B01 | AI field clip — stale document drift | `clips/s01_stale_drift.mp4` | FRIDAY'S STATUS IS ALREADY WRONG |
| S02 | 0:08 | 0:18 | 10s | B01 | AI paper clip — status page with wrong numbers fading | `clips/s02_wrong_page.mp4` | _(hold title or none)_ |
| S03 | 0:18 | 0:28 | 10s | B02 | AI contrast — chat bubble essay reshuffling | `clips/s03_oneshot_essay.mp4` | ONE-SHOT ESSAY ≠ MACHINE |
| S04 | 0:28 | 0:38 | 10s | B02 | Still+move: clean machine silhouette vs messy essay | `clips/s04_contrast_hold.mp4` | _(continue)_ |
| S05 | 0:38 | 0:50 | 12s | B03 | **Course SVG** `p1-overview.svg` Ken Burns | `stills/p1-overview.png` → move | THE MACHINE THAT MAKES THE ANSWER |
| S06 | 0:50 | 1:05 | 15s | B03 | AI or SVG motion — corpus → machine → brief flow | `clips/s06_flow_machine.mp4` | _(none; diagram labels)_ |
| S07 | 1:05 | 1:14 | 9s | B04 | Title card paper | `stills/card_objectives.png` | WHAT YOU LEAVE WITH |
| S08 | 1:14 | 1:22 | 8s | B04 | Card: LIVE Direction Brief | `stills/card_live_brief.png` | DIRECTION BRIEF · LIVE |
| S09 | 1:22 | 1:30 | 8s | B04 | Card: regenerable path | `stills/card_rerun.png` | ONE SAVED COMMAND |
| S10 | 1:30 | 1:40 | 10s | B04 | **SVG** `p1-idea-citation-circuit.svg` | `stills/p1-idea-citation-circuit.png` | CITATION AUDIT |
| S11 | 1:40 | 1:50 | 10s | B05 | AI field — operator frame around instrument (no person) | `clips/s11_harness_frame.mp4` | HOW TO WORK WITH THE HARNESS |
| S12 | 1:50 | 2:00 | 10s | B05 | **SVG** `p1-stage-04-audit.svg` | `stills/p1-stage-04-audit.png` | EYES ON THE WIRE |
| S13 | 2:00 | 2:08 | 8s | B05 | **SVG** `p1-idea-two-probes.svg` | `stills/p1-idea-two-probes.png` | DELTA · STALE |
| S14 | 2:08 | 2:22 | 14s | B06 | Stage strip animation (6 stages) | `clips/s14_six_stages.mp4` or still sequence | SIX STAGES |
| S15 | 2:22 | 2:30 | 8s | B07 | Paper end card + crimson rule | `stills/end_card.png` | OPEN P1 · START THE CONTRACT |

**Clip generation priority (spend order):**

1. S01, S03, S06, S11, S14 — need generative motion  
2. S05, S10, S12, S13 — SVG stills + ffmpeg Ken Burns (no gen required)  
3. S07–S09, S15 — designed still cards (HTML/CSS or figure stills)  
4. S02, S04 — optional polish; can reuse S01/S03 holds if budget tight

**Minimum viable movie (if clip budget is tight):**

- VO full  
- S05 overview SVG  
- S10 citation SVG  
- S13 two-probes SVG  
- S14 six-stage still sequence  
- S15 end card  
- One field hook clip (S01)  

That still clears 2:00 if VO does.
