#!/usr/bin/env python3
"""Render a ThankYou note (note.json + art.svg) into a self-contained HTML card.

Usage:
    python3 render_card.py note.json --art art.svg --out thankyou-priya.html
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

DEFAULT_PALETTE = {"bg": "#FBF6EE", "ink": "#3B2F2A", "accent": "#C8693C", "paper": "#FFFDF9"}

TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}" dir="{direction}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Thank you, {name}</title>
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
  .closing {{ margin:20px 0 2px; font-size:16px; }}
  .signature {{ font-size:22px; font-style:italic; color:var(--accent); margin:0; }}
  @media print {{ body {{ background:#fff; padding:0; }} .card {{ box-shadow:none; }} }}
</style>
</head>
<body>
<article class="card">
  {art}
  <div class="content">
    {occasion}
    <blockquote>
      <p>{quote}</p>
      {translation}
      {attribution}
    </blockquote>
    <p class="greeting">{greeting}</p>
    <div class="body">{body}</div>
    <p class="closing">{closing}</p>
    <p class="signature">{signature}</p>
  </div>
</article>
</body>
</html>
"""


def clean_svg(svg: str) -> str:
    """Strip XML prolog, scripts, and event handlers so the inline SVG is inert."""
    svg = re.sub(r"<\?xml[^>]*\?>", "", svg)
    svg = re.sub(r"<!DOCTYPE[^>]*>", "", svg, flags=re.IGNORECASE)
    svg = re.sub(r"<script\b.*?</script>", "", svg, flags=re.IGNORECASE | re.DOTALL)
    svg = re.sub(r"\son\w+\s*=\s*(\"[^\"]*\"|'[^']*')", "", svg, flags=re.IGNORECASE)
    svg = re.sub(r"(href\s*=\s*[\"'])\s*(?:https?:|javascript:)[^\"']*", r"\1#", svg, flags=re.IGNORECASE)
    return svg.strip()


def render(note: dict, art_svg: str | None) -> str:
    e = lambda s: html.escape(str(s or ""))
    palette = {**DEFAULT_PALETTE, **(note.get("palette") or {})}
    quote = note.get("quote") or {}
    body = "".join(f"<p>{e(p)}</p>" for p in note.get("body") or [])
    return TEMPLATE.format(
        lang=e(note.get("language", "en")),
        direction="rtl" if note.get("direction") == "rtl" else "ltr",
        name=e(note.get("recipient_first_name", "")),
        art=f'<div class="art" role="img" aria-label="Illustration made for {e(note.get("recipient_first_name"))}">{clean_svg(art_svg)}</div>' if art_svg else "",
        occasion=f'<p class="occasion">{e(note["occasion"])}</p>' if note.get("occasion") else "",
        quote=f"“{e(quote.get('text'))}”" if quote.get("text") else "",
        translation=f'<p class="translation">{e(quote["translation"])}</p>' if quote.get("translation") else "",
        attribution=f"<cite>— {e(quote['attribution'])}</cite>" if quote.get("attribution") else "",
        greeting=e(note.get("greeting")),
        body=body,
        closing=e(note.get("closing", "With gratitude,")),
        signature=e(note.get("signature") or note.get("sender_first_name")),
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
    lines.append(note.get("closing", ""))
    lines.append(note.get("signature") or note.get("sender_first_name", ""))
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("note", type=Path)
    ap.add_argument("--art", type=Path, help="SVG artwork file")
    ap.add_argument("--out", type=Path, default=Path("thankyou.html"))
    ap.add_argument("--text-out", type=Path, help="also write a plain-text version")
    args = ap.parse_args()

    note = json.loads(args.note.read_text(encoding="utf-8"))
    svg = args.art.read_text(encoding="utf-8") if args.art else None
    args.out.write_text(render(note, svg), encoding="utf-8")
    print(f"card → {args.out}")
    if args.text_out:
        args.text_out.write_text(plain_text(note), encoding="utf-8")
        print(f"text → {args.text_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
