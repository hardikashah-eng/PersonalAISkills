#!/usr/bin/env python3
"""Render a ThankYou / Reconnect note into a self-contained HTML card.

Usage:
    python3 render_card.py note.json --art art.svg --out thankyou-priya.html
    python3 render_card.py note.json --art art.svg --style print --out thankyou-priya.html
    python3 render_card.py note.json --art art.svg --photo moment.jpg \
        --photo-out moment-clean.jpg --out card.html

The optional photo is shown in a small instant-photo frame with the caption,
alt text and optional credit from note.json ("photo": {"caption": ..., "alt": ...,
"credit": ...}). It can also be a drawn pencil-sketch SVG (see
references/sketch.md), which is cleaned and embedded the same way. Before a photo
is embedded, all metadata (EXIF, GPS location, XMP, IPTC, text chunks) is
removed. If Pillow is installed the photo is also turned upright and shrunk to
at most 1200 px; otherwise JPEG and PNG are cleaned with the standard library
only. --photo-out writes the cleaned copy, for attaching to an email or chat.

Cards are written in a handwriting font by default (Caveat, with Kalam for
Devanagari; both SIL Open Font License, bundled in ../assets/fonts and embedded
so the card works offline). Scripts without a bundled handwriting font, such as
Chinese or Arabic, fall back to the system fonts. --style print gives the clean
serif look instead.
"""
from __future__ import annotations

import argparse
import base64
import html
import io
import json
import re
import struct
import sys
from pathlib import Path

DEFAULT_PALETTE = {"bg": "#FBF6EE", "ink": "#3B2F2A", "accent": "#C8693C", "paper": "#FFFDF9"}
MAX_PHOTO_PX = 1200
MAX_EMBED_BYTES = 3 * 1024 * 1024

# --- Handwritten style ----------------------------------------------------------
# Fonts are bundled under ../assets/fonts (SIL Open Font License 1.1, see the
# OFL-*.txt files there). Only the subsets a card's text needs are embedded.
FONT_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"

HAND_FONTS = [
    # (file, weight, unicode-range, regex that triggers embedding, size-adjust)
    ("caveat-latin-500-normal.woff2", 500,
     "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,"
     "U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD", r".", None),
    ("caveat-latin-700-normal.woff2", 700,
     "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,"
     "U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD", r".", None),
    ("caveat-latin-ext-500-normal.woff2", 500,
     "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+1D00-1DBF,U+1E00-1E9F,"
     "U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF",
     r"[Ā-˿Ḁ-ỿ]", None),
    ("caveat-cyrillic-500-normal.woff2", 500,
     "U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116", r"[Ѐ-ӿ]", None),
    ("kalam-devanagari-400-normal.woff2", 500,
     "U+0900-097F,U+1CD0-1CF9,U+200C-200D,U+20A8,U+20B9,U+20F0,U+25CC,U+A830-A839,U+A8E0-A8FF",
     r"[ऀ-ॿ]", "82%"),
]

SQUIGGLE = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='8' "
            "viewBox='0 0 40 8'%3E%3Cpath d='M0 4 Q5 0 10 4 T20 4 T30 4 T40 4' fill='none' "
            "stroke='%23000' stroke-opacity='.22' stroke-width='1.3' stroke-linecap='round'/%3E%3C/svg%3E\")")

HAND_CSS = """
  body {{ font-family: "PAI Hand", "Bradley Hand", "Segoe Print",
                      "Kaiti SC", "STKaiti", "KaiTi", "BiauKai", "Klee", "Nanum Pen Script",
                      "Noto Serif", cursive; }}
  .card {{ background-image: radial-gradient(rgba(120,100,70,.035) 1px, transparent 1px);
          background-size: 5px 5px; }}
  .content {{ padding:30px 40px 36px; color:var(--ink); text-shadow:0 0 .35px currentColor; }}
  blockquote {{ border-bottom:none; padding-bottom:20px; margin-bottom:20px;
               background:{squiggle} repeat-x left bottom / 40px 8px; }}
  blockquote p {{ font-style:normal; font-size:25px; line-height:1.25; }}
  blockquote .translation {{ font-size:20px; opacity:.72; margin-top:6px; }}
  blockquote cite {{ font: 500 20px/1.2 "PAI Hand", cursive; margin-top:8px; }}
  .greeting {{ font-size:30px; margin:0 0 10px; }}
  .body p {{ font-size:25px; line-height:1.36; margin:0 0 14px; }}
  .body p:nth-child(4n+1) {{ transform:rotate(-0.35deg); margin-left:1px; }}
  .body p:nth-child(4n+2) {{ transform:rotate(0.25deg); margin-left:5px; }}
  .body p:nth-child(4n+3) {{ transform:rotate(-0.15deg); margin-left:2px; }}
  .body p:nth-child(4n)   {{ transform:rotate(0.3deg); margin-left:6px; }}
  .photo figcaption {{ font-style:normal; font-size:22px; padding:8px 6px 12px; }}
  .closing {{ font-size:26px; margin:22px 0 0 18px; }}
  .signature {{ font-style:normal; font-weight:700; font-size:40px; margin:0 0 0 34px;
               transform:rotate(-3deg); transform-origin:left center; }}
"""


def hand_font_faces(text: str) -> str | None:
    """@font-face rules for the subsets this text needs, or None if fonts are missing."""
    rules = []
    for fname, weight, urange, trigger, size_adjust in HAND_FONTS:
        if not re.search(trigger, text):
            continue
        path = FONT_DIR / fname
        if not path.exists():
            return None
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        adjust = f" size-adjust:{size_adjust};" if size_adjust else ""
        rules.append(
            f'  @font-face {{ font-family:"PAI Hand"; font-style:normal; font-weight:{weight}; '
            f'font-display:swap;{adjust} src:url(data:font/woff2;base64,{data}) format("woff2"); '
            f"unicode-range:{urange}; }}"
        )
    return "\n".join(rules)


TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}" dir="{direction}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  :root {{ --bg:{bg}; --ink:{ink}; --accent:{accent}; --paper:{paper}; }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; min-height:100vh; display:flex; align-items:center; justify-content:center;
         background:var(--bg); color:var(--ink); padding:32px 16px;
         font-family: Georgia, "Iowan Old Style", "Palatino Linotype", "Noto Serif",
                      "Noto Serif Devanagari", "Noto Serif Tamil", "Noto Serif CJK SC",
                      "Noto Naskh Arabic", serif; }}
  .card {{ width:100%; max-width:520px; background:var(--paper); border-radius:18px;
          box-shadow:0 1px 2px rgba(0,0,0,.06), 0 12px 40px rgba(60,40,20,.12);
          overflow:hidden; }}
  .art {{ display:block; width:100%; height:auto; background:var(--bg); }}
  .art svg {{ display:block; width:100%; height:auto; }}
  .content {{ padding:28px 36px 34px; }}
  .occasion {{ font: 600 11px/1.2 system-ui, sans-serif; letter-spacing:.14em; text-transform:uppercase;
              color:var(--accent); margin:0 0 14px; }}
  blockquote {{ margin:0 0 22px; padding:0 0 18px; border-bottom:1px solid rgba(0,0,0,.08); }}
  blockquote p {{ margin:0; font-style:italic; font-size:18px; line-height:1.45; }}
  blockquote .translation {{ font-size:14px; opacity:.75; margin-top:6px; }}
  blockquote cite {{ display:block; margin-top:8px; font: 13px/1.3 system-ui, sans-serif; font-style:normal;
                    color:var(--accent); }}
  .greeting {{ font-size:18px; margin:0 0 12px; }}
  .body p {{ font-size:16px; line-height:1.65; margin:0 0 12px; }}
  .photo {{ margin:22px 0 10px; display:flex; justify-content:center; }}
  .photo .frame {{ background:#fff; padding:10px 10px 0; max-width:82%;
                  box-shadow:0 1px 2px rgba(0,0,0,.08), 0 8px 22px rgba(60,40,20,.16);
                  transform:rotate(-1.6deg); }}
  .photo img {{ display:block; width:100%; height:auto; }}
  .photo figcaption {{ font-style:italic; font-size:15px; text-align:center; padding:9px 6px 13px;
                      color:var(--ink); }}
  .photo .credit {{ font: 11px/1.3 system-ui, sans-serif; text-align:center; opacity:.6; margin:-8px 0 0; padding:0 6px 10px; }}
  .closing {{ margin:20px 0 2px; font-size:16px; }}
  .signature {{ font-size:22px; font-style:italic; color:var(--accent); margin:0; }}
  @media print {{ body {{ background:#fff; padding:0; }} .card {{ box-shadow:none; }} }}
{style_css}
</style>
</head>
<body>
<article class="card">
  {art}
  <div class="content">
    {occasion}
    {quote_block}
    <p class="greeting">{greeting}</p>
    <div class="body">{body}</div>
    {photo_block}
    {closing_block}
    <p class="signature">{signature}</p>
  </div>
</article>
</body>
</html>
"""


# --- SVG ----------------------------------------------------------------------

def clean_svg(svg: str) -> str:
    """Strip XML prolog, scripts, and event handlers so the inline SVG is inert."""
    svg = re.sub(r"<\?xml[^>]*\?>", "", svg)
    svg = re.sub(r"<!DOCTYPE[^>]*>", "", svg, flags=re.IGNORECASE)
    svg = re.sub(r"<script\b.*?</script>", "", svg, flags=re.IGNORECASE | re.DOTALL)
    svg = re.sub(r"\son\w+\s*=\s*(\"[^\"]*\"|'[^']*')", "", svg, flags=re.IGNORECASE)
    svg = re.sub(r"(href\s*=\s*[\"'])\s*(?:https?:|javascript:)[^\"']*", r"\1#", svg, flags=re.IGNORECASE)
    return svg.strip()


# --- Photo cleaning -----------------------------------------------------------

class PhotoError(ValueError):
    pass


def _jpeg_orientation(app1: bytes) -> int:
    """Read the EXIF orientation tag (0x0112) from an APP1 payload; 1 if absent."""
    if not app1.startswith(b"Exif\x00\x00"):
        return 1
    tiff = app1[6:]
    if len(tiff) < 8:
        return 1
    endian = {b"II": "<", b"MM": ">"}.get(tiff[:2])
    if not endian:
        return 1
    try:
        ifd = struct.unpack(endian + "I", tiff[4:8])[0]
        count = struct.unpack(endian + "H", tiff[ifd:ifd + 2])[0]
        for i in range(count):
            entry = tiff[ifd + 2 + 12 * i: ifd + 14 + 12 * i]
            tag, _typ, _n = struct.unpack(endian + "HHI", entry[:8])
            if tag == 0x0112:
                return struct.unpack(endian + "H", entry[8:10])[0]
    except (struct.error, IndexError):
        pass
    return 1


def strip_jpeg(data: bytes) -> tuple[bytes, list[str]]:
    """Drop EXIF/XMP (APP1), IPTC (APP13), comments and other app segments.

    Keeps JFIF (APP0), ICC colour profiles (APP2) and Adobe (APP14), which
    affect how the image looks but hold no personal data.
    """
    if data[:2] != b"\xff\xd8":
        raise PhotoError("not a JPEG file")
    out = bytearray(b"\xff\xd8")
    notes: list[str] = []
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            raise PhotoError("unexpected data in JPEG header")
        marker = data[i + 1]
        if marker == 0xFF:  # fill byte
            i += 1
            continue
        if marker == 0xDA:  # start of scan: image data follows, copy the rest
            out += data[i:]
            break
        if marker in (0x01,) or 0xD0 <= marker <= 0xD7:
            out += data[i:i + 2]
            i += 2
            continue
        length = struct.unpack(">H", data[i + 2:i + 4])[0]
        segment = data[i:i + 2 + length]
        payload = segment[4:]
        keep = marker < 0xE0 and marker != 0xFE or marker in (0xE0, 0xE2, 0xEE)
        if marker == 0xE2 and not payload.startswith(b"ICC_PROFILE"):
            keep = False
        if marker == 0xE1:
            orientation = _jpeg_orientation(payload)
            if orientation != 1:
                notes.append(
                    f"photo had EXIF orientation {orientation}; without Pillow it may now appear "
                    "rotated. Install Pillow (pip install pillow) or rotate the photo first."
                )
            notes.append("removed EXIF/XMP metadata (location, camera, timestamps)")
        elif not keep:
            notes.append(f"removed metadata segment 0x{marker:02X}")
        if keep:
            out += segment
        i += 2 + length
    return bytes(out), notes


PNG_KEEP = {b"IHDR", b"PLTE", b"IDAT", b"IEND", b"tRNS", b"gAMA", b"cHRM", b"sRGB", b"iCCP",
            b"sBIT", b"bKGD", b"pHYs", b"acTL", b"fcTL", b"fdAT"}


def strip_png(data: bytes) -> tuple[bytes, list[str]]:
    """Drop text, EXIF and time chunks from a PNG."""
    sig = b"\x89PNG\r\n\x1a\n"
    if not data.startswith(sig):
        raise PhotoError("not a PNG file")
    out = bytearray(sig)
    notes: list[str] = []
    i = len(sig)
    while i < len(data):
        length = struct.unpack(">I", data[i:i + 4])[0]
        ctype = data[i + 4:i + 8]
        chunk = data[i:i + 12 + length]
        if ctype in PNG_KEEP:
            out += chunk
        else:
            notes.append(f"removed PNG {ctype.decode('latin-1')} chunk")
        i += 12 + length
        if ctype == b"IEND":
            break
    return bytes(out), notes


def clean_photo(path: Path) -> tuple[bytes, str, list[str]]:
    """Return (clean_bytes, mime, notes). Metadata is always removed."""
    if path.suffix.lower() == ".svg":
        svg = clean_svg(path.read_text(encoding="utf-8"))
        if "xmlns=" not in svg[:300]:
            svg = svg.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
        return svg.encode("utf-8"), "image/svg+xml", ["embedded drawn sketch (scripts and external links removed)"]
    raw = path.read_bytes()
    try:
        from PIL import Image, ImageOps  # type: ignore
    except ImportError:
        Image = None

    if Image is not None:
        try:
            with Image.open(io.BytesIO(raw)) as im:
                im = ImageOps.exif_transpose(im)
                im.thumbnail((MAX_PHOTO_PX, MAX_PHOTO_PX))
                buf = io.BytesIO()
                if im.mode in ("RGBA", "LA", "P") and "transparency" in im.info or im.mode in ("RGBA", "LA"):
                    im.save(buf, format="PNG", optimize=True)
                    mime = "image/png"
                else:
                    im.convert("RGB").save(buf, format="JPEG", quality=85, optimize=True)
                    mime = "image/jpeg"
            # Pillow does not copy EXIF unless asked; strip again to be certain.
            data = buf.getvalue()
            data, _ = strip_jpeg(data) if mime == "image/jpeg" else strip_png(data)
            return data, mime, [f"turned upright, resized to at most {MAX_PHOTO_PX}px, removed all metadata"]
        except Exception as exc:  # unreadable by Pillow: fall through to stdlib
            if not raw[:2] == b"\xff\xd8" and not raw.startswith(b"\x89PNG"):
                raise PhotoError(
                    "could not read this photo. Use a JPEG or PNG copy "
                    "(for iPhone HEIC photos, export as JPEG or install pillow-heif)."
                ) from exc

    if raw[:2] == b"\xff\xd8":
        data, notes = strip_jpeg(raw)
        mime = "image/jpeg"
    elif raw.startswith(b"\x89PNG"):
        data, notes = strip_png(raw)
        mime = "image/png"
    else:
        raise PhotoError(
            "unsupported photo format. Use JPEG or PNG, or install Pillow "
            "(HEIC also needs pillow-heif)."
        )
    if len(data) > MAX_EMBED_BYTES:
        raise PhotoError(
            f"photo is {len(data) // 1024} KB after cleaning; install Pillow to resize it "
            "automatically, or export a smaller copy (about 1200 px wide)."
        )
    return data, mime, notes


# --- Rendering ----------------------------------------------------------------

def render(note: dict, art_svg: str | None, photo: tuple[bytes, str] | None = None,
           style: str = "handwritten") -> str:
    e = lambda s: html.escape(str(s or ""))
    palette = {**DEFAULT_PALETTE, **(note.get("palette") or {})}
    quote = note.get("quote") or {}
    photo_meta = note.get("photo") or {}
    body = "".join(f"<p>{e(p)}</p>" for p in note.get("body") or [])
    name = e(note.get("recipient_name") or note.get("recipient_first_name", ""))

    photo_block = ""
    if photo:
        data, mime = photo
        src = f"data:{mime};base64,{base64.b64encode(data).decode('ascii')}"
        alt = e(photo_meta.get("alt") or "A photo from a good time together")
        caption = f"<figcaption>{e(photo_meta['caption'])}</figcaption>" if photo_meta.get("caption") else ""
        if photo_meta.get("credit"):
            caption += f'<p class="credit">{e(photo_meta["credit"])}</p>'
        photo_block = f'<figure class="photo"><div class="frame"><img src="{src}" alt="{alt}">{caption}</div></figure>'

    closing = note.get("closing", "With gratitude,")

    style_css = ""
    if style == "handwritten":
        all_text = json.dumps(note, ensure_ascii=False)
        faces = hand_font_faces(all_text)
        if faces is None:
            print("note: handwriting fonts not found; using the print style", file=sys.stderr)
        else:
            style_css = faces + HAND_CSS.format(squiggle=SQUIGGLE)

    return TEMPLATE.format(
        lang=e(note.get("language", "en")),
        direction="rtl" if note.get("direction") == "rtl" else "ltr",
        title=f"For {name}" if name else "A note for you",
        art=f'<div class="art" role="img" aria-label="Illustration made for {name}">{clean_svg(art_svg)}</div>' if art_svg else "",
        occasion=f'<p class="occasion">{e(note["occasion"])}</p>' if note.get("occasion") else "",
        quote_block=(
            "<blockquote>"
            f"<p>“{e(quote.get('text'))}”</p>"
            + (f'<p class="translation">{e(quote["translation"])}</p>' if quote.get("translation") else "")
            + (f"<cite>— {e(quote['attribution'])}</cite>" if quote.get("attribution") else "")
            + "</blockquote>"
        ) if quote.get("text") else "",
        greeting=e(note.get("greeting")),
        body=body,
        photo_block=photo_block,
        closing_block=f'<p class="closing">{e(closing)}</p>' if closing else "",
        signature=e(note.get("signature") or note.get("sender_first_name")),
        style_css=style_css,
        **{k: e(v) for k, v in palette.items()},
    )


def plain_text(note: dict) -> str:
    q = note.get("quote") or {}
    lines = []
    if q.get("text"):
        lines.append(f"“{q['text']}”")
        if q.get("translation"):
            lines.append(q["translation"])
        if q.get("attribution"):
            lines.append(f"— {q['attribution']}")
        lines.append("")
    lines.append(note.get("greeting", ""))
    lines.append("")
    for p in note.get("body") or []:
        lines += [p, ""]
    if note.get("closing"):
        lines.append(note["closing"])
    lines.append(note.get("signature") or note.get("sender_first_name", ""))
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("note", type=Path)
    ap.add_argument("--art", type=Path, help="SVG artwork file")
    ap.add_argument("--photo", type=Path, help="JPEG or PNG photo from a shared moment (metadata is removed), "
                    "or a drawn pencil-sketch SVG when there is no photo")
    ap.add_argument("--photo-out", type=Path, help="also write the cleaned photo, for attaching to an email or chat")
    ap.add_argument("--out", type=Path, default=Path("thankyou.html"))
    ap.add_argument("--style", choices=["handwritten", "print"], default=None,
                    help="handwritten (default): embedded handwriting font, ink on card stock; "
                         "print: the clean serif look. Overrides note.json 'style'.")
    ap.add_argument("--text-out", type=Path, help="also write a plain-text version")
    args = ap.parse_args()

    note = json.loads(args.note.read_text(encoding="utf-8"))
    svg = args.art.read_text(encoding="utf-8") if args.art else None

    photo = None
    if args.photo:
        try:
            data, mime, notes = clean_photo(args.photo)
        except (OSError, PhotoError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        photo = (data, mime)
        for n in notes:
            print(f"photo: {n}")
        if args.photo_out:
            args.photo_out.write_bytes(data)
            print(f"clean photo → {args.photo_out}")

    style = args.style or note.get("style") or "handwritten"
    args.out.write_text(render(note, svg, photo, style), encoding="utf-8")
    print(f"card → {args.out}")
    if args.text_out:
        args.text_out.write_text(plain_text(note), encoding="utf-8")
        print(f"text → {args.text_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
