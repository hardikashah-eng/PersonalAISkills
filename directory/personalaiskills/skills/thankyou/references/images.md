# Photos, card images and sketches

How to handle pictures without any tool shipped in this plugin. Use what your
environment already has (an image library, a document or file tool, the
user's own apps). If a step can't be done safely, skip that picture and tell
the user in one line; never send a photo with its metadata.

## Cleaning a photo before it goes anywhere

Before a photo is embedded in a card or booklet, attached, or shared:

1. **Remove all metadata**: EXIF (camera, timestamps, GPS location), XMP,
   IPTC, comments, and PNG text and time chunks. Keep only what's needed to
   draw the image (and a colour profile, if any).
2. **Turn it upright** using its orientation tag, then remove the tag.
3. **Shrink it** to about 1200 px on the long side (a card needs no more, and
   the file stays small enough to email).
4. **Save it as JPEG** (or PNG when it has transparency).

If you can process images in your environment, do these steps there and keep
the clean copy to attach. If you can't, don't embed the photo: ask the user to
attach a copy exported without location (most phone share sheets have an
option to leave location out), or use a drawn sketch instead. iPhone HEIC
photos need to be exported as JPEG first.

## Sending the card as an image

Messaging apps show images, not HTML. When a card goes to WhatsApp, iMessage,
Slack and similar:

- If your environment can render HTML to an image (a headless browser tool, a
  screenshot tool), render the card at about 560 px wide and twice the pixel
  density, and save it as `card.png`.
- Otherwise, tell the user to open the card file and take a screenshot, or to
  print it to PDF.

The rendered image is a new file with no personal metadata. Check it before
sending, as you would the HTML.

## Pencil sketches

When there is no suitable photo, draw an original pencil-style SVG of the
scene (`references/sketch.md`). Turning a real or stock photo into a sketch
needs an image tool: do it only if your environment has one, only for a
freely licensed stock photo of a scene or object (or the user's own photo
when they ask for a sketch), and remove all metadata from the result.
Otherwise, draw the scene instead.
