#!/usr/bin/env python3
"""Turn a photo into a graphite pencil sketch on warm paper.

Meant for freely licensed stock photos of scenes and objects (see
references/sketch.md). It needs Pillow. All metadata is removed from the output.

Usage:
    python3 sketch_photo.py stock.jpg --out sketch.jpg [--strength 1.0] [--max-px 1200]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

PAPER = (247, 244, 238)   # warm paper
GRAPHITE = (58, 58, 58)   # darkest pencil tone


def sketch(src: Path, out: Path, strength: float = 1.0, max_px: int = 1200) -> None:
    try:
        from PIL import Image, ImageChops, ImageFilter, ImageOps
    except ImportError:
        raise SystemExit("error: sketch_photo.py needs Pillow (pip install pillow). "
                         "Without it, draw the scene as a pencil-style SVG instead.")

    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        im.thumbnail((max_px, max_px))
        gray = ImageOps.grayscale(im)

    w, h = gray.size
    scale = min(w, h) / 900

    # Pencil lines: difference of two blurs finds edges in photos and flat images alike.
    fine = gray.filter(ImageFilter.GaussianBlur(0.8 * scale + 0.4))
    wide = gray.filter(ImageFilter.GaussianBlur(3.2 * scale + 1))
    edges = ImageOps.autocontrast(ImageChops.difference(fine, wide), cutoff=2)
    lines = ImageOps.invert(edges.point(lambda v: min(255, int(v * 1.6 * strength))))

    # Soft tonal shading underneath, kept light like graphite rubbed on paper.
    shade = ImageOps.autocontrast(gray, cutoff=1).filter(ImageFilter.GaussianBlur(1.2 * scale))
    shade = shade.point(lambda v: 150 + v * 105 // 255)

    sketch_l = ImageChops.multiply(lines, shade)

    # Fine paper grain.
    grain = Image.effect_noise((w, h), 24).filter(ImageFilter.GaussianBlur(0.5))
    grain = grain.point(lambda v: max(232, min(255, 244 + (v - 128) // 6)))
    sketch_l = ImageChops.multiply(sketch_l, grain)

    # Map white -> paper, black -> graphite.
    toned = ImageOps.colorize(sketch_l, black=GRAPHITE, white=PAPER)

    fmt = "PNG" if out.suffix.lower() == ".png" else "JPEG"
    params = {"optimize": True} if fmt == "PNG" else {"quality": 88, "optimize": True}
    toned.save(out, format=fmt, **params)   # saved without EXIF or other metadata


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("photo", type=Path)
    ap.add_argument("--out", type=Path, default=Path("sketch.jpg"))
    ap.add_argument("--strength", type=float, default=1.0, help="0.6 (lighter) to 1.6 (darker, bolder lines)")
    ap.add_argument("--max-px", type=int, default=1200)
    args = ap.parse_args()
    if not args.photo.exists():
        print(f"error: {args.photo} not found", file=sys.stderr)
        return 2
    sketch(args.photo, args.out, args.strength, args.max_px)
    print(f"sketch → {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
