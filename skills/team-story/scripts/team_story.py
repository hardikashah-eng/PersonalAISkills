#!/usr/bin/env python3
"""Build a team highlight reel: one self-contained HTML page that tells a
project or a quarter through everyone's contributions, with a "who helped
whom" map, plus a #wins post and a slide outline.

  python3 team_story.py story.json --out q4-story.html
  python3 team_story.py story.json --evidence evidence.jsonl --out q4-story.html   # draw the map from Spotlight evidence
  python3 team_story.py story.json --post       # text for a #wins or all-hands channel
  python3 team_story.py story.json --slides     # a slide-by-slide outline (for a Slides deck)

The map shows connections, not rankings: every person is the same size, and
lines show who helped whom (thicker = more often). Nobody is scored. Runs
locally; sends nothing.
"""
from __future__ import annotations

import argparse
import html
import json
import math
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "thankyou" / "scripts"))
from render_card import hand_font_faces  # noqa: E402

HELP_KINDS = {"peer-thanks", "review-for-others", "incident-help", "on-call-cover", "mentoring",
              "onboarding-help", "cross-team-help", "unblocked"}


def esc(x) -> str:
    return html.escape(str(x or ""), quote=True)


def edges_from(story: dict, evidence: Path | None) -> Counter:
    """(helper, helped) → count, from the story's own list and/or Spotlight evidence."""
    c: Counter = Counter()
    for e in story.get("helped") or []:
        c[(e["helper"], e["helped"])] += int(e.get("times", 1))
    if evidence and evidence.exists():
        period = story.get("since"), story.get("until")
        for line in evidence.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get("kind") not in HELP_KINDS or not r.get("from") or r["from"] == r["person"]:
                continue
            if period[0] and r["date"] < period[0] or period[1] and r["date"] > period[1]:
                continue
            c[(r["person"], r["from"])] += 1
    return c


def people_in(story: dict, edges: Counter) -> list[str]:
    seen: list[str] = []
    for name in story.get("team") or []:
        if name not in seen:
            seen.append(name)
    for ch in story.get("chapters") or []:
        for c in ch.get("contributors") or []:
            if c["name"] not in seen:
                seen.append(c["name"])
    for a, b in edges:
        for n in (a, b):
            if n not in seen:
                seen.append(n)
    return seen


def map_svg(people: list[str], edges: Counter, team: set[str], accent: str, ink: str) -> str:
    if not edges:
        return ""
    w, h, r = 640, 420, 150
    cx, cy = w / 2, h / 2 + 4
    pos = {p: (cx + r * 1.35 * math.cos(2 * math.pi * i / len(people) - math.pi / 2),
               cy + r * math.sin(2 * math.pi * i / len(people) - math.pi / 2)) for i, p in enumerate(people)}
    top = max(edges.values())
    parts = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
             f'aria-label="Who helped whom on the team">',
             '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="11" markerHeight="11" '
             f'markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{accent}" opacity=".75"/></marker></defs>']
    for (a, b), n in sorted(edges.items(), key=lambda kv: kv[1]):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy) or 1
        sx, sy, ex, ey = x1 + dx / d * 34, y1 + dy / d * 34, x2 - dx / d * 36, y2 - dy / d * 36
        mx, my = (sx + ex) / 2 - dy / d * 18, (sy + ey) / 2 + dx / d * 18
        width = 1.4 + 3.2 * (n / top)
        parts.append(f'<path d="M{sx:.1f} {sy:.1f} Q{mx:.1f} {my:.1f} {ex:.1f} {ey:.1f}" fill="none" '
                     f'stroke="{accent}" stroke-opacity=".55" stroke-width="{width:.1f}" marker-end="url(#arr)"/>')
    for p, (x, y) in pos.items():
        outside = p not in team
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="30" fill="#fff" stroke="{ink}" stroke-width="1.6"'
                     f'{" stroke-dasharray=\"4 3\"" if outside else ""}/>')
        parts.append(f'<text x="{x:.1f}" y="{y + 5:.1f}" text-anchor="middle" font-family="PAI Hand, cursive" '
                     f'font-size="19" fill="{ink}">{esc(p)}</text>')
    parts.append("</svg>")
    return "".join(parts)


CSS = """
:root { --bg:%(bg)s; --ink:%(ink)s; --accent:%(accent)s; --paper:%(paper)s; }
%(faces)s
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--ink); font:17px/1.6 system-ui, -apple-system, "Segoe UI", sans-serif; }
main { max-width:860px; margin:36px auto; background:var(--paper); border-radius:18px; padding:52px 60px;
       box-shadow:0 18px 50px rgba(0,0,0,.10); }
.kicker { font:600 13px/1 system-ui, sans-serif; letter-spacing:.16em; text-transform:uppercase; color:var(--accent); margin:0; }
h1 { font:700 54px/1.05 "PAI Hand", cursive; margin:10px 0 8px; }
.headline { font-size:20px; margin:0 0 28px; }
h2 { font:700 32px/1.1 "PAI Hand", cursive; margin:34px 0 10px; color:var(--accent); }
.chapter { border-left:3px solid var(--accent); padding:2px 0 2px 20px; margin:18px 0; }
.chapter h3 { margin:0; font-size:19px; }
.chapter .when { font-size:13px; opacity:.65; margin:2px 0 8px; }
.chapter ul { margin:8px 0 0; padding:0; list-style:none; }
.chapter li { margin:6px 0; }
.chapter li b { font-family:"PAI Hand", cursive; font-size:21px; font-weight:700; margin-right:6px; }
.quotes { display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:14px; }
.quote { background:var(--bg); border-radius:12px; padding:14px 18px; font:500 21px/1.35 "PAI Hand", cursive; }
.quote span { display:block; font:13px/1.4 system-ui, sans-serif; opacity:.7; margin-top:6px; }
.map svg { width:100%%; height:auto; }
.map p { font-size:13px; opacity:.7; margin:4px 0 0; }
.thanks { columns:2; font-size:16px; } .thanks li { break-inside:avoid; margin:4px 0; }
.closing { font:600 26px/1.3 "PAI Hand", cursive; margin:30px 0 0; }
@media (max-width:640px) { main { padding:30px 22px; } h1 { font-size:40px; } .thanks { columns:1; } }
"""


def build(story: dict, edges: Counter) -> str:
    pal = {"bg": "#EEF0F7", "ink": "#2B2E3E", "accent": "#5865A8", "paper": "#FFFEFB"}
    pal.update(story.get("palette") or {})
    people = people_in(story, edges)
    team = set(story.get("team") or people)
    out = [f'<p class="kicker">{esc(story.get("period"))}</p>', f'<h1>{esc(story.get("title"))}</h1>']
    if story.get("headline"):
        out.append(f'<p class="headline">{esc(story["headline"])}</p>')
    if story.get("chapters"):
        out.append("<h2>How we got there</h2>")
        for ch in story["chapters"]:
            items = "".join(f'<li><b>{esc(c["name"])}</b>{esc(c["did"])}</li>' for c in ch.get("contributors") or [])
            out.append(f'<div class="chapter"><h3>{esc(ch.get("title"))}</h3>'
                       f'<p class="when">{esc(ch.get("when"))}</p><p>{esc(ch.get("what"))}</p><ul>{items}</ul></div>')
    svg = map_svg(people, edges, team, pal["accent"], pal["ink"])
    if svg:
        out.append('<h2>Who helped whom</h2><div class="map">' + svg +
                   "<p>Arrows point from the person who helped to the person they helped; thicker means more often. "
                   "Dashed circles are colleagues from other teams. It's drawn from the moments that were recorded, "
                   "so some help isn't shown. It shows connections, not rankings.</p></div>")
    if story.get("quotes"):
        out.append('<h2>In their words</h2><div class="quotes">' + "".join(
            f'<div class="quote">“{esc(q["text"])}”<span>{esc(q["by"])}</span></div>' for q in story["quotes"]) + "</div>")
    if story.get("also_thanks"):
        out.append('<h2>And thank you to</h2><ul class="thanks">' +
                   "".join(f"<li><b>{esc(t['name'])}</b>: {esc(t['for'])}</li>" for t in story["also_thanks"]) + "</ul>")
    if story.get("closing"):
        out.append(f'<p class="closing">{esc(story["closing"])}</p>')
    faces = hand_font_faces(json.dumps(story, ensure_ascii=False)) or ""
    return (f'<!DOCTYPE html><html lang="{esc(story.get("language", "en"))}"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(story.get("title"))}</title>'
            f'<style>{CSS % {**pal, "faces": faces}}</style></head><body><main>' + "".join(out) + "</main></body></html>")


def post_text(story: dict) -> str:
    lines = [f"🎉 {story.get('title')} ({story.get('period')})", ""]
    if story.get("headline"):
        lines += [story["headline"], ""]
    for ch in story.get("chapters") or []:
        names = ", ".join(c["name"] for c in ch.get("contributors") or [])
        lines.append(f"• {ch.get('title')}: {ch.get('what')} ({names})")
    if story.get("also_thanks"):
        lines += ["", "And thank you to " + "; ".join(f"{t['name']}, for {t['for']}" for t in story["also_thanks"]) + "."]
    if story.get("closing"):
        lines += ["", story["closing"]]
    return "\n".join(lines)


def slides(story: dict) -> str:
    out = [f"# Slide 1: {story.get('title')}", f"- {story.get('period')}", f"- {story.get('headline', '')}", ""]
    n = 2
    for ch in story.get("chapters") or []:
        out += [f"# Slide {n}: {ch.get('title')}", f"- {ch.get('what')}"]
        out += [f"- {c['name']}: {c['did']}" for c in ch.get("contributors") or []]
        out.append("")
        n += 1
    out += [f"# Slide {n}: Who helped whom", "- (the map from the HTML page)", ""]
    n += 1
    if story.get("quotes"):
        out += [f"# Slide {n}: In their words"] + [f"- “{q['text']}” ({q['by']})" for q in story["quotes"]] + [""]
        n += 1
    out += [f"# Slide {n}: Thank you", f"- {story.get('closing', 'Thank you, team.')}"]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("story", type=Path)
    ap.add_argument("--evidence", type=Path, help="Spotlight evidence.jsonl, to draw who helped whom")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--post", action="store_true")
    ap.add_argument("--slides", action="store_true")
    a = ap.parse_args()
    story = json.loads(a.story.read_text(encoding="utf-8"))
    if a.post:
        print(post_text(story))
    if a.slides:
        print(slides(story))
    if a.out:
        a.out.write_text(build(story, edges_from(story, a.evidence)), encoding="utf-8")
        print(f"team story → {a.out}")
    if not (a.post or a.slides or a.out):
        ap.error("choose --out, --post or --slides")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
