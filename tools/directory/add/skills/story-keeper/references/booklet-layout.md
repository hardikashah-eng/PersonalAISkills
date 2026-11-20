# Building the booklet

Write the booklet yourself from `keepsake.json`: one self-contained HTML file
(inline CSS, images and audio as `data:` URLs, no scripts or external
requests), so it works offline and can be emailed, kept on a family drive, or
printed. Paths in `keepsake.json` are relative to it.

## Pages

Each page is a `<section class="page">`, a sheet on a warm background.

1. **Cover**: the cover photo (portrait), the title, the subtitle, the dedication.
2. **One page per chapter**: "Chapter N" (or the family's word, `chapter_word`),
   the chapter title, when; the first photo; the story paragraphs, the first
   with a drop capital; the pull quote; the voice clip; then any other photos.
3. **Closing words** ("What I want you to remember"): title, paragraphs, an
   optional photo, and the signature.
4. A small colophon under the last page: the book's `colophon`, or "Kept with
   love. Shared only with the family."

Set `<html lang dir>` from `language` and `direction`, and escape all text.

## Photos

Every photo has its metadata removed and is shrunk to about 1400 px before it
is embedded (`../../thankyou/references/images.md`). If you can't remove the
metadata, leave it out and tell the user. Each photo sits in a white
instant-photo frame, tilted slightly (alternating left and right), with the
caption in handwriting under it and the credit in small type. A photo marked
`"sketch": true` is turned into a pencil sketch first, only if your
environment has an image tool for it; otherwise use the photo as it is and
say so. A drawn SVG sketch is embedded as it is, after removing any scripts,
event attributes and external links.

## Voice clips

Under the label (for example "Hear Nani tell it", with a small microphone
mark), an `<audio controls preload="none">` with the clip as a `data:` URL
(`audio/mp4` for .m4a and .mp4, `audio/mpeg` for .mp3, `audio/ogg`,
`audio/wav`), then the transcript in quotes, the translation, and when it was
recorded. Keep clips to 10–30 seconds; over about 3 MB, ask the user for a
shorter cut. In print, the player is hidden and the transcript stays.

## Style

Palette (or the book's own `palette`): background `#EFE6D8`, ink `#3A2E25`,
accent `#9A5B34`, page `#FFFCF6`. Body text in a readable serif (`"Iowan Old
Style","Palatino Linotype",Palatino,Georgia,serif`, 18 px, line height 1.7).
Titles, captions, the pull quote, labels and the signature in a handwriting
typeface the computer has (`"Caveat","Segoe Print","Bradley Hand",cursive`):
a 64 px cover title, 44 px chapter titles, a 30 px accent-coloured pull quote
with an accent bar on the left. Pages are about 760 px wide with generous
padding, rounded corners and a soft shadow.

For printing: white background, no shadows or rounded corners, one page per
section (`page-break-after: always`), audio players hidden. The user can print
the file to PDF from their browser.
