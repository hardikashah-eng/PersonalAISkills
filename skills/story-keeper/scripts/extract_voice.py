#!/usr/bin/env python3
"""Cut a short voice snippet from the user's own family video, for a keepsake.

Runs entirely on this machine with ffmpeg. Nothing is uploaded. The snippet is
the person's real voice, cut at the timestamps the user chooses: it is never
cloned, synthesized, re-voiced, sped up, or spliced to change what was said.

  # 1. See what's in the video and where the talking is
  python3 extract_voice.py diwali-2009.mp4 --scan

  # 2. Cut the part the user picked (10-30 s works best)
  python3 extract_voice.py diwali-2009.mp4 --start 1:23 --end 1:48 --out nani-mango-tree.m4a

Output: AAC audio (.m4a) with a gentle fade in and out, loudness evened out
(EBU R128) and every metadata tag removed (no dates, device or location).
Needs ffmpeg and ffprobe on PATH.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

MIN_S, SOFT_MAX_S, HARD_MAX_S = 3.0, 30.0, 90.0


def ts(value: str) -> float:
    """Parse 83, 83.5, 1:23, 1:23.5 or 0:01:23 into seconds."""
    parts = value.strip().split(":")
    if not 1 <= len(parts) <= 3 or not all(re.fullmatch(r"\d+(\.\d+)?", p) for p in parts):
        raise argparse.ArgumentTypeError(f"not a timestamp: {value!r} (use 83, 1:23 or 0:01:23)")
    secs = 0.0
    for p in parts:
        secs = secs * 60 + float(p)
    return secs


def fmt(secs: float) -> str:
    m, s = divmod(max(secs, 0.0), 60)
    return f"{int(m)}:{s:04.1f}"


def need(tool: str) -> str:
    path = shutil.which(tool)
    if not path:
        sys.exit(f"{tool} not found. Install ffmpeg (https://ffmpeg.org/download.html) and try again.")
    return path


def probe(src: Path) -> dict:
    out = subprocess.run([need("ffprobe"), "-v", "error", "-show_entries",
                          "format=duration:stream=index,codec_type,codec_name,channels,sample_rate",
                          "-of", "json", str(src)], capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit(f"could not read {src}: {out.stderr.strip()}")
    return json.loads(out.stdout)


def scan(src: Path, noise_db: int, min_gap: float) -> list[tuple[float, float]]:
    """Return stretches of sound between silences: the likely talking parts."""
    info = probe(src)
    duration = float(info.get("format", {}).get("duration") or 0)
    run = subprocess.run([need("ffmpeg"), "-hide_banner", "-nostats", "-i", str(src), "-vn",
                          "-af", f"highpass=f=80,lowpass=f=4000,silencedetect=noise={noise_db}dB:d={min_gap}",
                          "-f", "null", "-"], capture_output=True, text=True)
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", run.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", run.stderr)]
    segments, cursor = [], 0.0
    for i, s in enumerate(starts):
        if s - cursor >= 1.5:
            segments.append((cursor, s))
        cursor = ends[i] if i < len(ends) else duration
    if duration - cursor >= 1.5:
        segments.append((cursor, duration))
    return segments


def extract(src: Path, start: float, end: float, out: Path, fade: float, normalize: bool, bitrate: str) -> None:
    length = end - start
    if length < MIN_S:
        sys.exit(f"snippet is {length:.1f} s; choose at least {MIN_S:.0f} s")
    if length > HARD_MAX_S:
        sys.exit(f"snippet is {length:.0f} s; keep it under {HARD_MAX_S:.0f} s (10-30 s works best)")
    if length > SOFT_MAX_S:
        print(f"note: {length:.0f} s is long for a keepsake; 10-30 s is easier to listen to", file=sys.stderr)
    fade = min(fade, length / 4)
    filters = [f"afade=t=in:st=0:d={fade:.2f}", f"afade=t=out:st={length - fade:.2f}:d={fade:.2f}"]
    if normalize:
        filters.append("loudnorm=I=-18:TP=-1.5:LRA=11")
    cmd = [need("ffmpeg"), "-hide_banner", "-loglevel", "error", "-y",
           "-ss", f"{start:.3f}", "-t", f"{length:.3f}", "-i", str(src),
           "-vn", "-sn", "-dn", "-map", "0:a:0",
           "-af", ",".join(filters), "-ac", "1", "-ar", "44100",
           "-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact", "-flags:a", "+bitexact",
           "-c:a", "aac", "-b:a", bitrate, "-movflags", "+faststart", str(out)]
    run = subprocess.run(cmd, capture_output=True, text=True)
    if run.returncode != 0:
        sys.exit(f"ffmpeg failed: {run.stderr.strip()}")
    size = out.stat().st_size
    print(f"voice snippet → {out}  ({fmt(start)}–{fmt(end)}, {length:.1f} s, {size / 1024:.0f} KB, metadata removed)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", type=Path, help="the user's own video or audio file")
    ap.add_argument("--scan", action="store_true", help="list the stretches with sound (likely talking) and exit")
    ap.add_argument("--start", type=ts, help="start time, e.g. 1:23")
    ap.add_argument("--end", type=ts, help="end time, e.g. 1:48")
    ap.add_argument("--out", type=Path, help="output .m4a (default: <video>-snippet.m4a)")
    ap.add_argument("--fade", type=float, default=0.4, help="fade in/out seconds (default 0.4)")
    ap.add_argument("--no-normalize", action="store_true", help="keep the original loudness")
    ap.add_argument("--bitrate", default="64k", help="AAC bitrate (default 64k: clear speech, small file)")
    ap.add_argument("--noise", type=int, default=-35, help="--scan: silence threshold in dB (default -35)")
    ap.add_argument("--gap", type=float, default=0.8, help="--scan: shortest pause that splits talking (s)")
    args = ap.parse_args()

    if not args.video.exists():
        sys.exit(f"not found: {args.video}")
    info = probe(args.video)
    audio = [s for s in info.get("streams", []) if s.get("codec_type") == "audio"]
    if not audio:
        sys.exit("this file has no sound track, so there's no voice to keep")

    if args.scan:
        duration = float(info.get("format", {}).get("duration") or 0)
        print(f"{args.video.name}: {fmt(duration)} long, audio {audio[0].get('codec_name')}")
        segs = scan(args.video, args.noise, args.gap)
        if not segs:
            print("no clear talking found; try --noise -45, or listen and pick the times yourself")
        for a, b in segs:
            print(f"  {fmt(a)} – {fmt(b)}  ({b - a:.0f} s)")
        print("Listen to these parts with the user, then cut the one they choose with --start/--end.")
        return 0

    if args.start is None or args.end is None:
        sys.exit("give --start and --end (or --scan first to find the talking)")
    if args.end <= args.start:
        sys.exit("--end must be after --start")
    out = args.out or args.video.with_name(args.video.stem + "-snippet.m4a")
    extract(args.video, args.start, args.end, out, args.fade, not args.no_normalize, args.bitrate)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
