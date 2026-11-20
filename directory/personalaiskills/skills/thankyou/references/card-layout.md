# Building the card

Every skill that makes a card (ThankYou, Reconnect, Grateful, Comfort, Tribute,
Welcome) builds it the same way: one self-contained HTML file written from
`note.json`, the artwork, and the optional photo. Write the file yourself,
following this layout. No server, no web fonts, no scripts, no external
requests: everything is inline, so the card opens offline, prints, and can be
attached to an email.

## Structure

Top to bottom, inside `<article class="card">`, leaving out any part the note
doesn't have:

1. **Artwork**: the SVG from `art.svg`, inline, in `<div class="art" role="img"
   aria-label="Illustration made for <name>">`.
2. **Occasion**: a small upper-case label (`<p class="occasion">`).
3. **Quote**: `<blockquote>` with the quote in curly quotes, the translation
   under it (`<p class="translation">`), and `<cite>— Attribution</cite>`.
4. **Title** (gratitude lists): `<p class="title">`.
5. **Greeting**: `<p class="greeting">`.
6. **Body**: one `<p>` per paragraph in `<div class="body">`.
7. **Items** (lists): `<ul class="items">`, each `<li>` with `subject`, then
   `why` and `difference` joined, then `forward` (shown as "↪ …").
8. **Photo**: an instant-photo frame, `<figure class="photo"><div class="frame">
   <img src="data:…" alt="…"><figcaption>…</figcaption></div></figure>`, with
   the credit under the caption for stock images. Add the class `wide` when the
   photo is at least 1.5 times wider than it is tall (group shots).
9. **Closing**, then the **signature**.
10. **Light moment**: "For a smile, whenever you want one:" (or the note's
    `lead`) and the linked title.
11. **P.S.**: `<p class="ps"><b>P.S.</b> fun fact…</p>`.

Set `<html lang="…" dir="ltr|rtl">` from `language` and `direction`, and the
page title to "For <name>" (or the list's title). Escape every piece of text
from the note (`&`, `<`, `>`, quotes).

## Artwork and sketches

Before putting an SVG in the card, make it inert: remove any XML prolog or
DOCTYPE, `<script>` elements, `on…=` event attributes, and any `href` that
points to a web address or `javascript:`. Keep `xmlns` on the root `<svg>`.
A drawn pencil sketch used in place of a photo goes in the photo frame the
same way, as inline SVG or as a `data:image/svg+xml` image.

## Photos

Embed the photo as a `data:` URL only after its metadata is removed and it is
at most about 1200 px on the long side (`references/images.md`). If you can't
remove the metadata, leave the photo out of the card and tell the user.

## Style

Use the note's `palette` (defaults: background `#FBF6EE`, ink `#3B2F2A`,
accent `#C8693C`, card `#FFFDF9`) as CSS variables.

**Print style** (`"style": "print"`): Georgia or a similar serif, 16 px body,
18 px italic quote, accent-coloured signature in italic.

**Handwritten style** (the default): the text in a handwriting typeface the
recipient's computer already has, ink on card stock, with slightly uneven lines:

```css
:root { --bg:#FBF6EE; --ink:#3B2F2A; --accent:#C8693C; --paper:#FFFDF9; }
* { box-sizing:border-box; }
body { margin:0; min-height:100vh; display:flex; align-items:center; justify-content:center;
       background:var(--bg); color:var(--ink); padding:32px 16px;
       font-family:"Caveat","Bradley Hand","Segoe Print","Kalam","Kaiti SC","STKaiti","KaiTi",
                   "Klee","Nanum Pen Script","Noto Serif",cursive; }
.card { width:100%; max-width:520px; background:var(--paper); border-radius:18px; overflow:hidden;
        box-shadow:0 1px 2px rgba(0,0,0,.06), 0 12px 40px rgba(60,40,20,.12);
        background-image:radial-gradient(rgba(120,100,70,.035) 1px, transparent 1px); background-size:5px 5px; }
.art svg { display:block; width:100%; height:auto; background:var(--bg); }
.content { padding:30px 40px 36px; }
.occasion { font:600 11px/1.2 system-ui,sans-serif; letter-spacing:.14em; text-transform:uppercase;
            color:var(--accent); margin:0 0 14px; }
blockquote { margin:0 0 20px; padding:0 0 20px; border-bottom:1px dashed rgba(0,0,0,.18); }
blockquote p { margin:0; font-size:25px; line-height:1.25; }
blockquote .translation { font-size:20px; opacity:.72; margin-top:6px; }
blockquote cite { display:block; margin-top:8px; font-size:20px; font-style:normal; color:var(--accent); }
.greeting { font-size:30px; margin:0 0 10px; }
.title { font-size:34px; line-height:1.15; margin:0 0 12px; color:var(--accent); transform:rotate(-0.8deg); }
.body p { font-size:25px; line-height:1.36; margin:0 0 14px; }
.body p:nth-child(odd) { transform:rotate(-0.3deg); }
.body p:nth-child(even) { transform:rotate(0.25deg); margin-left:5px; }
ul.items { list-style:none; margin:6px 0 10px; padding:0; }
ul.items li { position:relative; padding-left:36px; margin:0 0 18px; font-size:28px; }
ul.items li::before { content:"✦"; position:absolute; left:4px; color:var(--accent); }
ul.items .subject { font-weight:700; margin:0 0 2px; }
ul.items .why { font-size:24px; line-height:1.32; margin:0; }
ul.items .forward { font-size:23px; line-height:1.3; margin:4px 0 0; color:var(--accent); }
.photo { margin:22px 0 10px; display:flex; justify-content:center; }
.photo .frame { background:#fff; padding:10px 10px 0; max-width:82%; transform:rotate(-1.6deg);
                box-shadow:0 1px 2px rgba(0,0,0,.08), 0 8px 22px rgba(60,40,20,.16); }
.photo.wide .frame { max-width:100%; transform:rotate(-1deg); }
.photo img { display:block; width:100%; height:auto; }
.photo figcaption { font-size:22px; text-align:center; padding:8px 6px 12px; }
.photo .credit { font:11px/1.3 system-ui,sans-serif; text-align:center; opacity:.6; margin:-8px 0 0; padding:0 6px 10px; }
.closing { font-size:26px; margin:22px 0 0 18px; }
.signature { font-weight:700; font-size:40px; margin:0 0 0 34px; color:var(--accent);
             transform:rotate(-3deg); transform-origin:left center; }
.light { font-size:22px; line-height:1.3; margin:18px 0 0 6px; }
.light a { color:var(--accent); }
.ps { font-size:22px; line-height:1.3; margin:22px 0 0 6px; opacity:.9; transform:rotate(-0.4deg); }
.ps b { color:var(--accent); }
@media print { body { background:#fff; padding:0; } .card { box-shadow:none; } }
```

The list mark follows the note's `bullet`: ✦ (`sparkle`, the default), a leaf
❦ (`leaf`), ♥ (`heart`) or ★ (`star`). Handwriting typefaces differ from one
computer to the next, which is fine: the card still reads as handwritten. For
Devanagari, Chinese, Japanese, Korean and Arabic text, the stack falls back to
fonts the system has for that script. If the user wants the look to be exactly
the same everywhere, send the card as an image (`references/images.md`).

## Plain-text version

Also keep a plain-text copy for messages and email: the quote, translation and
attribution; the greeting; the paragraphs; each item as "✦ subject — why" (and
"↪ forward" on the next line); the closing and signature; the light moment with
its link; and "P.S. …".
