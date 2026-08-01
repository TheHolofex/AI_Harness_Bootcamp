#!/usr/bin/env python3
"""Assemble P1 intro video from timecodes.json + stills/clips + optional VO.

Titles are burned with Pillow (Homebrew ffmpeg often lacks libfreetype drawtext).

Usage (from repo root):

  videos/.venv/bin/python videos/p1/assembly/build_p1_intro.py
  videos/.venv/bin/python videos/p1/assembly/build_p1_intro.py --vo videos/p1/audio/p1_vo.wav
  videos/.venv/bin/python videos/p1/assembly/build_p1_intro.py --out videos/p1/assembly/p1_intro_mvp_silent.mp4

Requires: ffmpeg, ffprobe, pillow.
"""
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

P1 = Path(__file__).resolve().parents[1]
FPS = 30
W, H = 1920, 1080


def run(cmd: list[str]) -> None:
    print("+", " ".join(shlex.quote(c) for c in cmd))
    subprocess.run(cmd, check=True)


def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def find_font(size: int = 48) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for c in candidates:
        if Path(c).exists():
            try:
                return ImageFont.truetype(c, size)
            except OSError:
                continue
    return ImageFont.load_default()


def resolve_visual(shot: dict) -> Path:
    visual = shot.get("visual", "")
    primary = P1 / visual if visual else None
    fallback = P1 / shot["fallback_still"] if shot.get("fallback_still") else None
    if primary is not None and primary.exists():
        return primary
    if fallback is not None and fallback.exists():
        return fallback
    for c in (P1 / "stills/placeholder_field.png", P1 / "stills/end_card.png"):
        if c.exists():
            return c
    raise FileNotFoundError(
        f"No visual for shot {shot.get('id')}: visual={visual!r} "
        f"fallback={shot.get('fallback_still')!r}"
    )


def letterbox(im: Image.Image) -> Image.Image:
    if im.size == (W, H):
        return im.convert("RGB")
    canvas = Image.new("RGB", (W, H), (255, 255, 255))
    tmp = im.convert("RGBA")
    tmp.thumbnail((W, H), Image.Resampling.LANCZOS)
    canvas.paste(tmp, ((W - tmp.width) // 2, (H - tmp.height) // 2), tmp if tmp.mode == "RGBA" else None)
    return canvas


def burn_title(src: Path, title: str, x: int, y: int, out: Path) -> None:
    im = letterbox(Image.open(src))
    if title.strip():
        d = ImageDraw.Draw(im)
        font = find_font(48)
        d.text((x + 2, y + 2), title, font=font, fill=(0, 0, 0))
        sample = im.crop((x, y, min(W, x + 400), min(H, y + 60))).resize((1, 1))
        r, g, b = sample.getpixel((0, 0))
        lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
        fill = (250, 250, 248) if lum < 128 else (10, 10, 10)
        d.text((x, y), title, font=font, fill=fill)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, "PNG")


def still_to_seg(still: Path, dur: float, out: Path) -> None:
    frames = max(int(dur * FPS), 1)
    vf = (
        f"scale=8000:-1,"
        f"zoompan=z='min(1.06,1+0.06*on/{frames})':"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"d={frames}:s={W}x{H}:fps={FPS},format=yuv420p"
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-loop",
            "1",
            "-i",
            str(still),
            "-t",
            f"{dur:.3f}",
            "-vf",
            vf,
            "-an",
            "-r",
            str(FPS),
            "-pix_fmt",
            "yuv420p",
            str(out),
        ]
    )


def clip_to_seg(clip: Path, dur: float, out: Path) -> None:
    vf = (
        f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
        f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,fps={FPS},format=yuv420p"
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-stream_loop",
            "-1",
            "-i",
            str(clip),
            "-t",
            f"{dur:.3f}",
            "-vf",
            vf,
            "-an",
            "-r",
            str(FPS),
            "-pix_fmt",
            "yuv420p",
            str(out),
        ]
    )


def make_segment(shot: dict, out_path: Path, titled_dir: Path) -> None:
    src = resolve_visual(shot)
    dur = float(shot["end"]) - float(shot["start"])
    if dur <= 0:
        raise ValueError(f"bad duration for {shot['id']}")
    title = shot.get("title") or ""
    print(f"Building {shot['id']} from {src.name} ({dur:.2f}s)")
    if src.suffix.lower() in {".png", ".jpg", ".jpeg"}:
        still = titled_dir / f"{shot['id']}.png"
        burn_title(
            src,
            title,
            int(shot.get("title_x", 96)),
            int(shot.get("title_y", 860)),
            still,
        )
        still_to_seg(still, dur, out_path)
    else:
        # Motion clip: titles already on cards preferred; optional future overlay
        clip_to_seg(src, dur, out_path)


def concat_segments(paths: list[Path], out_path: Path) -> None:
    list_path = out_path.parent / "concat.txt"
    list_path.write_text("".join(f"file '{p.resolve()}'\n" for p in paths))
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(list_path),
            "-c",
            "copy",
            str(out_path),
        ]
    )


def mux_audio(video: Path, audio: Path | None, out_path: Path) -> None:
    if not audio or not audio.exists():
        run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(video),
                "-c",
                "copy",
                str(out_path),
            ]
        )
        return
    run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(video),
            "-i",
            str(audio),
            "-filter_complex",
            "[1:a]loudnorm=I=-14:TP=-1.5:LRA=11[a]",
            "-map",
            "0:v",
            "-map",
            "[a]",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            str(out_path),
        ]
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--timecodes", type=Path, default=P1 / "script/timecodes.json")
    ap.add_argument("--vo", type=Path, default=P1 / "audio/p1_vo.wav")
    ap.add_argument("--out", type=Path, default=P1 / "assembly/p1_intro.mp4")
    ap.add_argument(
        "--mvp-stills-only",
        action="store_true",
        help="Accepted for compatibility; missing clips always fall back to stills.",
    )
    args = ap.parse_args()

    data = json.loads(args.timecodes.read_text())
    shots = data["shots"]

    vo_path = args.vo if args.vo.exists() else None
    if vo_path:
        vo_dur = probe_duration(vo_path)
        design_end = max(float(s["end"]) for s in shots)
        if design_end > 0 and abs(vo_dur - design_end) > 1.0:
            scale = vo_dur / design_end
            print(f"Scaling timeline to VO duration {vo_dur:.2f}s (scale={scale:.4f})")
            for s in shots:
                s["start"] = round(float(s["start"]) * scale, 3)
                s["end"] = round(float(s["end"]) * scale, 3)

    work = P1 / "assembly" / "_segments"
    titled = P1 / "assembly" / "_titled_stills"
    work.mkdir(parents=True, exist_ok=True)
    titled.mkdir(parents=True, exist_ok=True)

    seg_paths: list[Path] = []
    for s in shots:
        seg = work / f"{s['id']}.mp4"
        make_segment(s, seg, titled)
        seg_paths.append(seg)

    silent = P1 / "assembly" / "_silent.mp4"
    concat_segments(seg_paths, silent)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    mux_audio(silent, vo_path, args.out)
    dur = probe_duration(args.out)
    print(f"Wrote {args.out} ({dur:.2f}s)")
    if dur < 120:
        print("WARNING: under 2:00 — lengthen VO or add beats before shipping.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
