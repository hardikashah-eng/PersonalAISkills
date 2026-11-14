#!/usr/bin/env python3
"""Save a rendered card (HTML) as a PNG image for messaging apps and email.

Messaging apps show images, not HTML, so this turns card.html into card.png.
It uses a local headless browser and makes no network requests: the card is
self-contained (fonts, art and photo are embedded).

Usage:
    python3 card_to_png.py card.html --out card.png [--width 560] [--scale 2]

Tries, in order: Playwright (if installed), then a Chrome or Chromium binary
in headless mode. If neither is available, open card.html in any browser and
take a screenshot, or print it to PDF.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CHROME_NAMES = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome",
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chromium.app/Contents/MacOS/Chromium",
                r"C:\Program Files\Google\Chrome\Application\chrome.exe"]


def find_chrome() -> str | None:
    for name in CHROME_NAMES:
        found = shutil.which(name) or (name if Path(name).exists() else None)
        if found:
            return found
    return None


def with_playwright(html: Path, out: Path, width: int, scale: float) -> bool:
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except ImportError:
        return False
    chrome = find_chrome()
    try:
        with sync_playwright() as p:
            launch = {"executable_path": chrome} if chrome else {}
            browser = p.chromium.launch(**launch)
            page = browser.new_page(viewport={"width": width + 80, "height": 900}, device_scale_factor=scale)
            page.goto(html.resolve().as_uri())
            page.wait_for_timeout(300)  # let embedded fonts settle
            page.locator(".card").screenshot(path=str(out))
            browser.close()
        return True
    except Exception as exc:  # browser missing or failed: try the next method
        print(f"note: Playwright could not render ({exc.__class__.__name__}); trying headless Chrome", file=sys.stderr)
        return False


def with_chrome_cli(html: Path, out: Path, width: int, scale: float) -> bool:
    chrome = find_chrome()
    if not chrome:
        return False
    # The CLI captures a fixed window, so render tall and trim the empty bottom if Pillow exists.
    with tempfile.TemporaryDirectory() as tmp:
        shot = Path(tmp) / "shot.png"
        cmd = [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-sandbox",
               f"--force-device-scale-factor={scale}", f"--window-size={width + 80},3600",
               f"--screenshot={shot}", html.resolve().as_uri()]
        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=60)
        except (subprocess.SubprocessError, OSError):
            return False
        try:
            from PIL import Image, ImageChops  # type: ignore
            im = Image.open(shot).convert("RGB")
            bg = Image.new("RGB", im.size, im.getpixel((2, im.height - 2)))
            box = ImageChops.difference(im, bg).getbbox()
            if box:
                pad = int(16 * scale)
                im = im.crop((max(0, box[0] - pad), max(0, box[1] - pad),
                              min(im.width, box[2] + pad), min(im.height, box[3] + pad)))
            im.save(out)
        except ImportError:
            shutil.copy(shot, out)
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("card", type=Path, help="card HTML from render_card.py")
    ap.add_argument("--out", type=Path, default=Path("card.png"))
    ap.add_argument("--width", type=int, default=560)
    ap.add_argument("--scale", type=float, default=2.0, help="pixel density (2 = sharp on phones)")
    args = ap.parse_args()
    if not args.card.exists():
        print(f"error: {args.card} not found", file=sys.stderr)
        return 2
    if with_playwright(args.card, args.out, args.width, args.scale) or \
       with_chrome_cli(args.card, args.out, args.width, args.scale):
        print(f"image → {args.out}")
        return 0
    print("error: no headless browser found. Open the card in a browser and take a screenshot, "
          "or print it to PDF.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
