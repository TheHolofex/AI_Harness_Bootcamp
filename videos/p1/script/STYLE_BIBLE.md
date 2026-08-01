# P1 Intro — Style Bible

Lock this before any Kling / Grok Imagine generation. Every prompt must include the **Global negative** and the **Palette block**.

## Dual surface (from course visual system)

Use **both**, with clear roles:

| Surface | When | Ground | Ink |
|---|---|---|---|
| **Paper** | Titles, objective cards, stage map, diagram holds | `#FFFFFF` / `#FAFAF8` | `#0A0A0A` |
| **Field** | Hook atmosphere, abstract “stale truth” beats, close sting | `#0D0906` | sand `#C8B78A` / gold `#A58650` |

Crimson `#E31C23` is **accent only** (disc, one emphasis rule, critical label). Never full-frame red washes.

## Typography on screen

- Section labels: uppercase, tracked, small, muted  
- Titles: large, tight, near-black on paper / sand on field  
- Prefer Inter / Helvetica Neue / system geometric sans  
- No gradient text, no neon glow type, no sticker badges

**Allowed on-screen strings only** (verbatim — do not invent others in AI clips):

```
FRIDAY'S STATUS IS ALREADY WRONG
ONE-SHOT ESSAY ≠ MACHINE
THE MACHINE THAT MAKES THE ANSWER
WHAT YOU LEAVE WITH
HOW TO WORK WITH THE HARNESS
SIX STAGES
OPEN P1 · START THE CONTRACT
LIVE
CONTRACT
CORPUS
MACHINE
AUDIT
PROBES
VERDICT
DIRECTION BRIEF
CITATION AUDIT
DELTA TEST
STALE-SOURCE TEST
[C#]
```

Prefer **burn-in titles in ffmpeg** over trusting generative models to spell. AI clips should be **visual motion under clean title overlays**.

## Motion law

| Do | Don't |
|---|---|
| Slow pans across paper diagrams | Handheld documentary shake |
| Soft opacity fades 8–16 frames | Whoosh-spin transitions |
| Trace lines drawing along flows | Particle explosions, neural webs |
| One idea moving at a time | Montage chaos |
| Hold readable labels ≥1.5s | Flash cuts under 12 frames on text |

Duration per generative clip: **5–10 seconds**. Longer beats = hold still + Ken Burns in ffmpeg, or stitch 2 clips.

## Figure / diagram law (Axis split from figure-gen)

1. **No scene staging** — no operator hero, desk, coffee, monitors-as-prop, room, window, antenna  
2. **Figure richness OK on field** — restrained gold sheen, hairlines, panel tiles — not sci-fi HUD overload  
3. **Content honesty** — no fake metrics, throughputs, confidence %, live clocks, dollar amounts

Course SVGs in `site/assets/blocks/p1/` are first-class stills. Prefer them over invented diagrams.

## Logo

- Optional corner bug: red disc + STARZL ENTERPRISES  
- Clear space ≥ disc diameter  
- Do not animate the mark into a “loading brain”

## Audio

- VO dry or light room, no radio announcer  
- Bed: very low ambient bed or silence; never lyric music  
- Duck bed −18 to −22 LUFS under VO; VO target ≈ −14 LUFS integrated  
- Hard cut or 4-frame fade at end — no long musical outro

## Global negative (paste into every gen prompt)

```
no people, no faces, no hands, no desk, no laptop hero shot, no coffee mug,
no neon brain, no neural network cloud, no holographic UI overload,
no cyberpunk city, no volumetric god-rays, no cinematic anamorphic flare,
no depth-of-field bokeh portrait look, no stock handshake, no confetti,
no 3D chrome logo spin, no fake dashboards with random percentages,
no watermark, no subtitle burn-in, no misspelled text
```

## Palette block (paste into every gen prompt)

```
Starzl courseware palette. Paper shots: pure white #FFFFFF ground, near-black #0A0A0A ink,
hairline gray #D0D0D0 rules, crimson #E31C23 used only as a thin accent line or small disc.
Field shots: deep warm black #0D0906 ground, muted gold #A58650 signals, sand #C8B78A labels,
panel brown-black #17110C. Restrained, defense-industrial, calm, exact. Not consumer edtech. Not sci-fi.
```
