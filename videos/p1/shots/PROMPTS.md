# P1 Intro — Generation Prompts

Use with **Kling**, **Grok Imagine**, or similar image-to-video / text-to-video tools.

For each shot:

1. Paste **Palette block** + **Global negative** from `script/STYLE_BIBLE.md`  
2. Paste the shot prompt  
3. Duration 5–10s, 16:9, 1080p if available  
4. Save to the filename under `clips/`  
5. Prefer **image-to-video** when a still is listed: generate/export still first, then animate gently

---

## Shared suffixes

**Motion suffix (append to all video prompts):**

```
Slow, minimal camera move. Soft linear motion only. Hold composition steady enough to read. 16:9. Extremely restrained animation. No jump cuts inside the clip.
```

**Still suffix (append to all still prompts):**

```
Full-bleed 16:9 technical figure, sharp vector-like edges, print-courseware clarity, no photography.
```

---

## S01 — Stale drift (field) · `clips/s01_stale_drift.mp4`

**Mode:** text-to-video or still→video  
**Duration:** 8s

```
Field surface abstract figure: a single status document panel floating on deep warm black #0D0906. Hairline gold #A58650 frame. Inside the panel, muted sand text blocks as abstract lines (no readable fake paragraphs). A thin crimson #E31C23 rule ticks once like a cut. Subtle dust of wrongness: one section dims and drifts half a degree out of register while the frame stays square. Defense-industrial composure. Label-dense briefing aesthetic without readable body copy.
```

+ Palette + Negative + Motion suffix

---

## S02 — Wrong page (paper) · `clips/s02_wrong_page.mp4`

**Mode:** still→video  
**Duration:** 8–10s

```
Paper surface: clean white courseware page. Top eyebrow micro-label area empty of real words. A simple four-section status layout as gray boxes with hairline #D0D0D0 borders. One box slowly desaturates and its inner rule cracks into a thin crimson accent line. No people. No desktop photo. Flat graphic, editorial, exact.
```

---

## S03 — One-shot essay chaos (paper) · `clips/s03_oneshot_essay.mp4`

**Mode:** text-to-video  
**Duration:** 8–10s

```
Paper white ground. A single column of abstract text lines reshuffles order every two seconds — blocks swap, emphasis bars jump — conveying an unstable essay. Opposite right side stays empty negative space for a later title overlay. Motion is mechanical and quiet, not glitchy cyber. Courseware graphic, not UI screenshot of a real chat app. No logos of vendors. No readable sentences.
```

---

## S04 — Contrast hold · `clips/s04_contrast_hold.mp4`

**Mode:** still→video  
**Duration:** 8–10s

```
Split paper composition. Left: messy stacked abstract paragraphs (one-shot). Right: a tight machine card with four fixed section slots and small citation ticks as geometric marks. A slow horizontal wipe strengthens the right card's black border while the left stays soft gray. Minimal. Exact. No icons of robots.
```

---

## S06 — Flow machine · `clips/s06_flow_machine.mp4`

**Mode:** text-to-video **or** animate from exported `stills/p1-overview.png`  
**Duration:** 10s  
**Preferred:** image-to-video from the real overview SVG export (label fidelity)

```
Animate a paper-surface systems diagram already in frame: corpus node to machine node to cited brief node to probes to verdict. Draw hairline black connector arrows slowly left to right. A dashed crimson return path subtly pulses once under the row labeled as regenerate conceptually (do not render new words). Keep all existing labels fixed and legible. No extra decorations. No camera orbit.
```

If the tool reflows text, **reject** and fall back to ffmpeg Ken Burns on the PNG.

---

## S11 — Harness frame (field) · `clips/s11_harness_frame.mp4`

**Mode:** text-to-video  
**Duration:** 8–10s

```
Field #0D0906. An abstract rectangular instrument frame in gold hairline, empty center. Corners show small bound-markers like tick stops. Inside the frame, a faint sand schematic of a document with citation ticks. Outside the frame, nothing — pure field. Message is structural: bounds around a thinking instrument. No human silhouette. No cockpit. No HUD spam. Slow push-in of 3 percent only.
```

---

## S14 — Six stages · `clips/s14_six_stages.mp4`

**Mode:** prefer **assembled still sequence in ffmpeg** (most reliable labels).  
Generative option only if needed:

```
Paper white. A horizontal rail of six equal rounded-rect stage chips with black index blocks 01-06. Chips read only: CONTRACT, CORPUS, MACHINE, AUDIT, PROBES, VERDICT. A gold or black progress hairline fills left to right under the rail. One chip at a time gains a stronger border. Exact spelling required. If text cannot be perfect, output blank chips for external labels.
```

**Fallback (recommended):** render `stills/stages_01.png` … `stages_06.png` from SVG/HTML and xfade in ffmpeg.

---

## Still cards (no video model required)

Generate as PNG 1920×1080 via HTML capture, Figma, or figure-gen — then Ken Burns lightly.

### `stills/card_objectives.png`
- Eyebrow: `P1 · MONDAY PM`  
- Title: `WHAT YOU LEAVE WITH`  
- Five short lines (not full VO): LIVE brief · regenerable path · citation audit · two probes · draft vs judgment  

### `stills/card_live_brief.png`
- Large word `LIVE` in crimson disc adjacency  
- Fields as empty labeled rows: Outcome · Done looks like · Bounds · Evidence · Stop  

### `stills/card_rerun.png`
- Center mono line: `./regenerate` or `one saved command`  
- Subtitle: `same frame · fresh evidence`  

### `stills/end_card.png`
- Title: `OPEN P1 · START THE CONTRACT`  
- Sub: `Codex app · Operator — Direction & Log`  
- Footer: `STARZL ENTERPRISES · AI Harness Bootcamp`  
- Thin crimson rule above footer  

---

## SVG exports (required)

From repo (white background already in files):

```bash
# requires: rsvg-convert or inkscape or qlmanage
rsvg-convert -w 1920 site/assets/blocks/p1/p1-overview.svg -o videos/p1/stills/p1-overview.png
rsvg-convert -w 1920 site/assets/blocks/p1/p1-idea-citation-circuit.svg -o videos/p1/stills/p1-idea-citation-circuit.png
rsvg-convert -w 1920 site/assets/blocks/p1/p1-idea-two-probes.svg -o videos/p1/stills/p1-idea-two-probes.png
rsvg-convert -w 1920 site/assets/blocks/p1/p1-stage-03-machine.svg -o videos/p1/stills/p1-stage-03-machine.png
rsvg-convert -w 1920 site/assets/blocks/p1/p1-stage-04-audit.svg -o videos/p1/stills/p1-stage-04-audit.png
```

Pad to 1920×1080 with paper ground in ffmpeg if aspect differs.

---

## Acceptance per clip

Reject a gen if any of these fail:

- [ ] Readable accidental garbage text  
- [ ] People / hands / laptop hero  
- [ ] Neon brain / cyber city  
- [ ] Wrong palette (blue tech, purple haze)  
- [ ] Duration <4s usable  
- [ ] Motion so hard labels would smear under overlay  

Keep rejects in `clips/reject/` for prompt learning; do not delete immediately.
