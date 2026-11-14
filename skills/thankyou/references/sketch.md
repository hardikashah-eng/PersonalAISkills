# No photo? A pencil sketch of the moment

When the user has no suitable photo of their own (see `photos.md`), the card
still gets a picture of the moment: a **pencil sketch**. It sits in the same
instant-photo frame as a photo would. Shared by ThankYou and Reconnect.

Two ways to make it, in order of preference:

## A. Draw it (default)

Claude draws an original pencil-style SVG of the *scene* of the moment: the
whiteboard with three boxes and arrows, two cups on a kitchen table beside an
open notebook, a team roped together near a summit flag, a lit window on a
winter night. Nothing is downloaded and there is no licence to check.

**What to draw**
- The place or the thing from the moment, plus one or two details from the
  note (the number of people, the season, the festival).
- People, if needed, as simple gesture figures: from behind, at a distance, or
  as silhouettes. **Never** a recognisable likeness of a real person, and no
  faces.
- No logos, brands, characters, or text beyond a single word.

**Pencil style**, in an SVG with a viewBox of about `0 0 600 400`:
- Warm paper background (`#F7F4EE`) with a faint grain.
- Graphite strokes in greys (`#3A3A3A` to `#8A8A8A`), round caps, widths of
  1.2–2.2 px, and slight opacity (0.75–0.9).
- Draw important lines twice, offset by about 1 px, like a pencil going back
  over a line.
- Wobble every line slightly with an SVG displacement filter, and shade with
  hatching patterns, not flat fills.
- At most one soft accent colour (a coloured-pencil touch, such as the flame of
  a diya or the flag at the summit).

```svg
<defs>
  <filter id="pencil" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="7" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="2.6" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="paper">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3"/>
    <feColorMatrix values="0 0 0 0 0.45  0 0 0 0 0.42  0 0 0 0 0.38  0 0 0 0.06 0"/>
  </filter>
  <pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(40)">
    <line x1="0" y1="0" x2="0" y2="6" stroke="#6b6b6b" stroke-width="0.9" opacity=".55"/>
  </pattern>
</defs>
<rect width="600" height="400" fill="#F7F4EE"/>
<rect width="600" height="400" filter="url(#paper)"/>
<g filter="url(#pencil)" fill="none" stroke="#3A3A3A" stroke-linecap="round" stroke-linejoin="round">
  <!-- scene strokes here; shaded areas use fill="url(#hatch)" -->
</g>
```

Save it as `sketch.svg` and pass it with `--photo sketch.svg`; the renderer
frames it like a photo.

## B. A freely licensed stock photo, turned into a pencil sketch

Use this when a drawn scene can't capture the moment, such as a specific
landscape or a kind of place, and the user would like something closer to a
photograph.

- **Free licences only**, and check the licence on the photo's own page at
  the time: public domain or CC0 (for example on Wikimedia Commons), or a
  free-to-use licence such as Unsplash's or Pexels'. If the licence asks for
  credit (CC BY), credit the author on the card. If a licence is unclear,
  don't use the photo.
- **Scenes and objects only**: landscapes, places, food, everyday things.
  **Never** a photo of identifiable people, never a public figure, never the
  recipient, and never anything taken from social media.
- **Matching the tone**: warm, calm, and fitting the occasion and culture, with
  no logos, brands, or text in the frame.
- Download it with the web tools available, then convert it:

  ```bash
  python3 scripts/sketch_photo.py stock.jpg --out sketch.jpg
  ```

  The script needs Pillow. It turns the photo into a graphite-on-paper sketch
  and removes all metadata. Without Pillow, use option A.
- Record the source in `note.json`:
  `"photo": {"source": "stock", "credit": "Photo: A. Author / Unsplash", "license": "Unsplash License", "url": "…"}`.
  If the licence requires credit, the renderer shows it under the caption.
- If the sandbox or tools can't download images, fall back to option A.

## Honesty

A sketch or a stock photo **is not a photo of their moment**, so the words
around it must never pretend it is:
- Never "Found this photo from launch week", "Remember this?", or "this photo
  of us". Those are only for the user's own real photos.
- Caption it as an image, not as a record: "Two cups, one long week" or
  "Where the trail ends", not "Us at the summit, 2019".
- Set `"source": "sketch"` or `"source": "stock"` in `note.json`.
  `safety_check.py` then blocks wording that presents the picture as a real
  photo of the moment.
- If a stock photo was converted, the credit line says so ("Pencil sketch
  after a photo by A. Author, Unsplash").

## Choosing between a drawing, a sketch, and a photo

| Situation | Use |
|---|---|
| The user has a good photo of their own | the real photo (`photos.md`) |
| No photo; the moment is a scene or an object | **A. drawn pencil sketch** |
| No photo; a place or landscape needs to look real | **B. stock photo as a pencil sketch** |
| The user prefers no picture | the header drawing alone |
