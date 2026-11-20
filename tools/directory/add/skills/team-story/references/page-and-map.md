# The page, the map, the post and the slides

Build each version yourself from `story.json`. Nothing is posted until the
user approves it.

## The page

One self-contained HTML file (inline CSS and SVG, no scripts or external
requests), in this order, leaving out anything the story doesn't have:

1. The period as a small upper-case kicker, the title (large, handwritten
   style), and the headline.
2. **How we got there**: one block per chapter with its title, when, what,
   and each contributor as "**Name** what they did".
3. **Who helped whom**: the map (below) and its caption.
4. **In their words**: the quotes as cards, each with who said it.
5. **And thank you to**: `also_thanks` as "**Name**: what for".
6. The closing line.

Palette (or the story's own `palette`): background `#EEF0F7`, ink `#2B2E3E`,
accent `#5865A8`, page `#FFFEFB`. Body in the system sans-serif at 17 px;
title, section headings, names and quotes in a handwriting typeface the
computer has (`"Caveat","Bradley Hand","Segoe Print",cursive`). The page is
a centred sheet about 860 px wide with rounded corners and a soft shadow;
chapters have an accent bar on the left; quotes sit in a grid of light cards;
the thanks list runs in two columns (one on phones).

## The who-helped-whom map

Build the connections: each `helped` pair in `story.json` (with its `times`),
plus, if the user keeps Spotlight evidence, one for each moment in the
story's period whose kind is help (peer-thanks, review-for-others,
incident-help, on-call-cover, mentoring, onboarding-help, cross-team-help,
unblocked) and whose `from` is someone else: the person helped `from`.

Draw it as an inline SVG, 640 × 420:

- Everyone is the **same size**: a white circle (radius 30) with their first
  name in the middle, placed evenly around an ellipse (about 200 px across,
  150 px tall from the centre), starting at the top. The team first, then
  other contributors, then anyone else in the connections. People from other
  teams have a dashed outline.
- One curved arrow per connection, from the helper to the person helped,
  stopping at the circles' edges, in the accent colour at about 55% opacity.
  Thicker means more often: width from 1.4 to 4.6, scaled to the busiest pair.
- Caption under it: "Arrows point from the person who helped to the person
  they helped; thicker means more often. Dashed circles are colleagues from
  other teams. It's drawn from the moments that were recorded, so some help
  isn't shown. It shows connections, not rankings."

Leave the map out if there are no connections.

## The channel post

```text
🎉 <title> (<period>)

<headline>

• <chapter title>: <what> (<contributor names>)
• …

And thank you to <name>, for <what>; <name>, for <what>.

<closing>
```

## The slide outline

Slide 1: the title, period and headline. One slide per chapter: its title,
what, and each contributor's part. Then "Who helped whom" (the map from the
page), "In their words" (the quotes, if any), and "Thank you" (the closing).
Make the deck from this outline with the Slides artifact type where it's
available.
