#!/usr/bin/env python3
"""Turn a photo into a graphite pencil sketch on warm paper.

For the user's own photos (when they ask for a sketch) and for freely licensed
stock photos of scenes and objects (see references/sketch.md). It needs Pillow
(and numpy for the default photo method). All metadata is removed from the output.

Usage:
    python3 sketch_photo.py photo.jpg --out sketch.jpg [--strength 1.0] [--max-px 1200] [--method photo|lines]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

PAPER = (247, 244, 238)   # warm paper
GRAPHITE = (58, 58, 58)   # darkest pencil tone


def _dodge(gray, strength: float):
    """Classic pencil sketch for real photos: colour-dodge the image with its blurred negative."""
    import numpy as np
    from PIL import Image, ImageFilter, ImageOps
    radius = max(4.0, min(gray.size) / 48.0)
    g = np.asarray(gray, dtype=np.float32)
    inv_blur = np.asarray(ImageOps.invert(gray).filter(ImageFilter.GaussianBlur(radius)), dtype=np.float32)
    out = np.clip(g * 255.0 / np.maximum(255.0 - inv_blur, 1.0), 0, 255)
    out = 255.0 * (out / 255.0) ** (2.2 * strength)          # deepen the graphite
    return Image.fromarray(out.astype(np.uint8))


def _lines(gray, strength: float):
    """Edge lines plus light shading; suits flat images and illustrations."""
    from PIL import ImageChops, ImageFilter, ImageOps
    w, h = gray.size
    scale = min(w, h) / 900
    fine = gray.filter(ImageFilter.GaussianBlur(0.8 * scale + 0.4))
    wide = gray.filter(ImageFilter.GaussianBlur(3.2 * scale + 1))
    edges = ImageOps.autocontrast(ImageChops.difference(fine, wide), cutoff=2)
    lines = ImageOps.invert(edges.point(lambda v: min(255, int(v * 1.6 * strength))))
    shade = ImageOps.autocontrast(gray, cutoff=1).filter(ImageFilter.GaussianBlur(1.2 * scale))
    shade = shade.point(lambda v: 150 + v * 105 // 255)
    return ImageChops.multiply(lines, shade)


def sketch(src: Path, out: Path, strength: float = 1.0, max_px: int = 1200, method: str = "photo") -> None:
    try:
        from PIL import Image, ImageChops, ImageFilter, ImageOps
    except ImportError:
        raise SystemExit("error: sketch_photo.py needs Pillow (pip install pillow). "
                         "Without it, draw the scene as a pencil-style SVG instead.")

    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        im.thumbnail((max_px, max_px))
        gray = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=1)

    if method == "photo":
        try:
            sketch_l = _dodge(gray, strength)
        except ImportError:  # no numpy
            print("note: numpy not found; using the line method", file=sys.stderr)
            sketch_l = _lines(gray, strength)
    else:
        sketch_l = _lines(gray, strength)

    # Fine paper grain.
    w, h = sketch_l.size
    grain = Image.effect_noise((w, h), 24).filter(ImageFilter.GaussianBlur(0.5))
    grain = grain.point(lambda v: max(236, min(255, 246 + (v - 128) // 7)))
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
    ap.add_argument("--method", choices=["photo", "lines"], default="photo",
                    help="photo (default): pencil shading for real photographs; "
                         "lines: outlines for flat images and illustrations")
    args = ap.parse_args()
    if not args.photo.exists():
        print(f"error: {args.photo} not found", file=sys.stderr)
        return 2
    sketch(args.photo, args.out, args.strength, args.max_px, args.method)
    print(f"sketch → {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
