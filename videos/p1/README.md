# P1 Intro Video Pipeline

≥2-minute module intro for **The Daily Status Brief**.

VO is the clock. Generative tools (Kling / Grok Imagine) supply short motion clips. ffmpeg assembles the movie.

## Status

| Artifact | State |
|---|---|
| Locked VO script | `script/VO_SCRIPT.md` — **approve before clip spend** |
| Plain narration for TTS | `script/vo_narration.txt` |
| Style bible | `script/STYLE_BIBLE.md` |
| Shot list | `shots/SHOT_LIST.md` |
| Gen prompts | `shots/PROMPTS.md` |
| Design timecodes | `script/timecodes.json` |
| Stills (SVG + title cards) | `stills/*.png` |
| Assembler | `assembly/build_p1_intro.py` |
| AI clips | drop into `clips/` when generated |
| VO audio | drop as `audio/p1_vo.wav` (or `.mp3`) |
| MVP silent cut | build with assembler (no VO yet) |

## Folder map

```
videos/p1/
  script/     VO + style + timecodes
  shots/      shot list + Kling/Imagine prompts
  stills/     1920×1080 PNGs (course diagrams + cards)
  clips/      generative mp4s (gitignored pattern via *.mp4)
  audio/      VO master
  assembly/   build scripts + outputs
  qa/         video-review frames later
```

## Build order (do not skip)

1. **Approve VO script** (`script/VO_SCRIPT.md`).
2. **Render VO** → `audio/p1_vo.wav`  
   ElevenLabs / macOS `say` / studio read. Target 2:20–2:40 @ ~145 wpm.
3. **Probe VO** and optionally rewrite `script/timecodes.json` to word boundaries.  
   Assembler auto-scales design targets to VO duration if off by >1s.
4. **Generate priority clips** from `shots/PROMPTS.md` (S01, S03, S06, S11, S14).  
   Save exact filenames under `clips/`.
5. **Assemble**
   ```bash
   videos/p1/assembly/build_p1_intro.sh \
     --vo videos/p1/audio/p1_vo.wav \
     --out videos/p1/assembly/p1_intro.mp4
   ```
6. **QA** with video-review skill on the mp4 (silent gaps, title collisions, under-2:00).
7. **Revise** only failed shots; do not regen the whole set.

### MVP without any AI clips

Stills alone already cover a full 2:30 timeline:

```bash
videos/p1/assembly/build_p1_intro.sh --out videos/p1/assembly/p1_intro_mvp_silent.mp4
```

Add VO when ready; drop clips over placeholders anytime — existing clip files win over fallbacks.

## Human checkpoints

| Gate | Owner | Pass bar |
|---|---|---|
| Script lock | you | Guide-beside, accurate to `site/blocks/p1.html`, ≥2:00 spoken |
| Clip accept | you | Style bible negatives clean; no garbage text; palette holds |
| Final picture lock | you | Titles readable; VO sync; no marketing register |

## Site embed (later)

After picture lock, host the mp4 (Course site or object storage) and add a player on `site/blocks/p1.html` under Orientation. Binaries stay gitignored (`*.mp4`).

## Regenerating stills

Title cards: re-run the PIL block in the session notes, or ask the agent to regenerate `stills/card_*.png`.  
SVG diagrams: export from `site/assets/blocks/p1/*.svg` (qlmanage or rsvg-convert) and letterbox to 1920×1080 paper.

## Template for P2–P8

Copy `videos/p1/` → `videos/pN/`, replace VO from that block page, swap SVG stills, keep style bible + assembler.
