#!/usr/bin/env python3
"""Build a family keepsake booklet (one self-contained HTML file) from keepsake.json.

The booklet has a cover with the elder's photo, a dedication, one chapter per
part of their life (their stories in their own words, family photos with
captions, and short clips of their real voice), and closing words. Everything
is embedded, so the file works offline and can be emailed, kept on a drive, or
printed. Photos have all metadata removed; voice clips should come from
extract_voice.py (metadata already removed).

Usage:
    python3 keepsake.py keepsake.json --out nani-stories.html
    python3 keepsake.py keepsake.json --out nani-stories.html --pdf nani-stories.pdf

Paths in keepsake.json are relative to the JSON file. A photo with
"sketch": true is turned into a pencil sketch first (needs Pillow and numpy).
"""
from __future__ import annotations

import argparse
import base64
import html
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "thankyou" / "scripts"))
from render_card import clean_photo, hand_font_faces  # noqa: E402

AUDIO_TYPES = {".m4a": "audio/mp4", ".mp4": "audio/mp4", ".aac": "audio/aac",
               ".mp3": "audio/mpeg", ".ogg": "audio/ogg", ".opus": "audio/ogg", ".wav": "audio/wav"}
AUDIO_MAX = 3 * 1024 * 1024

CSS = """
:root { --bg:%(bg)s; --ink:%(ink)s; --accent:%(accent)s; --paper:%(paper)s; }
%(faces)s
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--ink);
       font: 18px/1.7 "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, "Noto Serif", serif; }
.book { max-width:760px; margin:40px auto; }
.page { background:var(--paper); border-radius:16px; padding:56px 64px; margin:0 0 28px;
        box-shadow:0 18px 50px rgba(0,0,0,.10); }
.hand { font-family:"PAI Hand", "Segoe Print", "Bradley Hand", cursive; }
.cover { text-align:center; padding-top:64px; }
.cover h1 { font: 700 64px/1.05 "PAI Hand", cursive; margin:10px 0 6px; color:var(--ink); }
.cover .subtitle { font: 500 26px/1.3 "PAI Hand", cursive; color:var(--accent); margin:0 0 28px; }
.cover .dedication { max-width:520px; margin:26px auto 0; font-style:italic; }
figure { margin:26px auto; text-align:center; }
figure .frame { display:inline-block; background:#fff; padding:12px 12px 14px; max-width:100%%;
                box-shadow:0 6px 18px rgba(0,0,0,.14); transform:rotate(-1.2deg); }
figure.alt .frame { transform:rotate(1.1deg); }
figure img { display:block; max-width:100%%; max-height:440px; height:auto; }
figure.portrait img { max-height:520px; }
figcaption { font: 500 21px/1.3 "PAI Hand", cursive; margin-top:10px; color:var(--ink); }
figure .credit { font: 12px/1.3 system-ui, sans-serif; opacity:.6; margin:4px 0 0; }
.chapter-no { font: 600 13px/1 system-ui, sans-serif; letter-spacing:.18em; text-transform:uppercase;
              color:var(--accent); margin:0 0 6px; }
h2 { font: 700 44px/1.1 "PAI Hand", cursive; margin:0 0 6px; }
.when { font: 500 20px/1.3 "PAI Hand", cursive; opacity:.75; margin:0 0 24px; }
.story p { margin:0 0 16px; }
.story p:first-child::first-letter { font: 700 3.1em/0.9 "PAI Hand", cursive; float:left;
                                     margin:6px 16px 0 0; padding-right:.06em; color:var(--accent); }
.pull { font: 500 30px/1.3 "PAI Hand", cursive; color:var(--accent); border-left:3px solid var(--accent);
        margin:26px 0; padding:4px 0 4px 20px; transform:rotate(-0.4deg); }
.voice { background:var(--bg); border-radius:14px; padding:18px 20px; margin:26px 0 8px; }
.voice .label { font: 600 22px/1.2 "PAI Hand", cursive; margin:0 0 10px; }
.voice .label::before { content:""; display:inline-block; width:.9em; height:.9em; margin-right:8px;
  vertical-align:-2px; background:var(--accent);
  -webkit-mask:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path d='M12 3a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V6a3 3 0 0 0-3-3zm-7 9h2a5 5 0 0 0 10 0h2a7 7 0 0 1-6 6.9V21h3v2H8v-2h3v-2.1A7 7 0 0 1 5 12z'/></svg>") center/contain no-repeat;
          mask:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path d='M12 3a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V6a3 3 0 0 0-3-3zm-7 9h2a5 5 0 0 0 10 0h2a7 7 0 0 1-6 6.9V21h3v2H8v-2h3v-2.1A7 7 0 0 1 5 12z'/></svg>") center/contain no-repeat; }
.voice audio { width:100%%; }
.voice .transcript { font-style:italic; margin:10px 0 0; font-size:16px; }
.voice .translation { font-size:15px; opacity:.75; margin:4px 0 0; }
.voice .when { font: 13px/1.3 system-ui, sans-serif; opacity:.6; margin:8px 0 0; }
.closing p { margin:0 0 14px; }
.closing .sig { font: 600 30px/1.2 "PAI Hand", cursive; color:var(--accent); margin-top:18px; }
.colophon { font: 13px/1.5 system-ui, sans-serif; opacity:.6; text-align:center; margin:0 0 40px; }
@media print {
  body { background:#fff; } .book { margin:0; max-width:none; }
  .page { box-shadow:none; border-radius:0; page-break-after:always; margin:0; }
  .voice audio { display:none; }
}
@media (max-width:640px) { .page { padding:32px 24px; } .cover h1 { font-size:46px; } h2 { font-size:34px; } }
"""


def esc(x) -> str:
    return html.escape(str(x or ""), quote=True)


def photo_src(path: Path, sketch: bool) -> str:
    if sketch and path.suffix.lower() != ".svg":
        from sketch_photo import sketch as make_sketch  # thankyou/scripts
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "sketch.jpg"
            make_sketch(str(path), str(out), 1.0, 1400, "photo")
            data, mime, _ = clean_photo(out)
    else:
        data, mime, _ = clean_photo(path)
    return f"data:{mime};base64,{base64.b64encode(data).decode('ascii')}"


def figure(p: dict, base: Path, i: int, cls: str = "") -> str:
    path = base / p["path"]
    if not path.exists():
        print(f"warning: photo not found, skipped: {path}", file=sys.stderr)
        return ""
    src = photo_src(path, bool(p.get("sketch")))
    alt = esc(p.get("alt") or p.get("caption") or "A family photo")
    cap = f"<figcaption>{esc(p['caption'])}</figcaption>" if p.get("caption") else ""
    credit = f'<p class="credit">{esc(p["credit"])}</p>' if p.get("credit") else ""
    classes = " ".join(c for c in (cls, "alt" if i % 2 else "") if c)
    return f'<figure class="{classes}"><div class="frame"><img src="{src}" alt="{alt}">{cap}{credit}</div></figure>'


def voice_block(v: dict, base: Path) -> str:
    path = base / v["path"]
    label = esc(v.get("label") or "Hear it in their voice")
    if not path.exists():
        print(f"warning: voice clip not found, skipped: {path}", file=sys.stderr)
        return ""
    data = path.read_bytes()
    if len(data) > AUDIO_MAX:
        print(f"warning: {path.name} is {len(data) // 1024} KB; trim it with extract_voice.py (10-30 s)", file=sys.stderr)
    mime = AUDIO_TYPES.get(path.suffix.lower(), "audio/mp4")
    src = f"data:{mime};base64,{base64.b64encode(data).decode('ascii')}"
    parts = [f'<div class="voice"><p class="label">{label}</p>',
             f'<audio controls preload="none" src="{src}"></audio>']
    if v.get("transcript"):
        parts.append(f'<p class="transcript">“{esc(v["transcript"])}”</p>')
    if v.get("translation"):
        parts.append(f'<p class="translation">{esc(v["translation"])}</p>')
    if v.get("recorded"):
        parts.append(f'<p class="when">{esc(v["recorded"])}</p>')
    parts.append("</div>")
    return "".join(parts)


def build(book: dict, base: Path) -> str:
    pal = {"bg": "#EFE6D8", "ink": "#3A2E25", "accent": "#9A5B34", "paper": "#FFFCF6"}
    pal.update(book.get("palette") or {})
    faces = hand_font_faces(json.dumps(book, ensure_ascii=False)) or ""
    lang = esc(book.get("language", "en"))
    direction = esc(book.get("direction", "ltr"))

    cover = ['<section class="page cover">']
    if book.get("cover_photo"):
        cover.append(figure(book["cover_photo"], base, 0, "portrait"))
    cover.append(f'<h1>{esc(book.get("title"))}</h1>')
    if book.get("subtitle"):
        cover.append(f'<p class="subtitle">{esc(book["subtitle"])}</p>')
    if book.get("dedication"):
        cover.append(f'<p class="dedication">{esc(book["dedication"])}</p>')
    cover.append("</section>")

    chapters = []
    word = book.get("chapter_word", "Chapter")
    for n, ch in enumerate(book.get("chapters") or [], 1):
        out = ['<section class="page chapter">',
               f'<p class="chapter-no">{esc(word)} {n}</p>',
               f'<h2>{esc(ch.get("title"))}</h2>']
        if ch.get("when"):
            out.append(f'<p class="when">{esc(ch["when"])}</p>')
        photos = ch.get("photos") or []
        if photos:
            out.append(figure(photos[0], base, n))
        out.append('<div class="story">' + "".join(f"<p>{esc(p)}</p>" for p in ch.get("story") or []) + "</div>")
        if ch.get("pullquote"):
            out.append(f'<p class="pull">“{esc(ch["pullquote"])}”</p>')
        if ch.get("voice"):
            out.append(voice_block(ch["voice"], base))
        for i, p in enumerate(photos[1:], n + 1):
            out.append(figure(p, base, i))
        out.append("</section>")
        chapters.append("".join(out))

    closing = []
    if book.get("closing"):
        closing = ['<section class="page closing">']
        if book["closing"].get("title"):
            closing.append(f'<h2>{esc(book["closing"]["title"])}</h2>')
        closing += [f"<p>{esc(p)}</p>" for p in book["closing"].get("body") or []]
        if book["closing"].get("photo"):
            closing.append(figure(book["closing"]["photo"], base, 1))
        if book["closing"].get("signature"):
            closing.append(f'<p class="sig">{esc(book["closing"]["signature"])}</p>')
        closing.append("</section>")

    colophon = f'<p class="colophon">{esc(book.get("colophon") or "Kept with love. Shared only with the family.")}</p>'
    css = CSS % {**pal, "faces": faces}
    return (f'<!DOCTYPE html><html lang="{lang}" dir="{direction}"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{esc(book.get("title"))}</title><style>{css}</style></head><body><main class="book">'
            + "".join(cover) + "".join(chapters) + "".join(closing) + colophon + "</main></body></html>")


def to_pdf(html_path: Path, pdf_path: Path) -> None:
    chrome = next((shutil.which(c) for c in ("google-chrome", "chromium", "chromium-browser", "chrome")
                   if shutil.which(c)), None)
    if not chrome:
        sys.exit("PDF needs Chrome or Chromium; open the HTML and use Print → Save as PDF instead")
    subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf_path}", html_path.resolve().as_uri()],
                   check=True, capture_output=True)
    print(f"pdf → {pdf_path} (voice clips play in the HTML version)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("keepsake", type=Path)
    ap.add_argument("--out", type=Path, default=Path("keepsake.html"))
    ap.add_argument("--pdf", type=Path, help="also save a printable PDF (needs Chrome)")
    args = ap.parse_args()
    book = json.loads(args.keepsake.read_text(encoding="utf-8"))
    args.out.write_text(build(book, args.keepsake.parent), encoding="utf-8")
    print(f"keepsake → {args.out} ({args.out.stat().st_size // 1024} KB)")
    if args.pdf:
        to_pdf(args.out, args.pdf)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
