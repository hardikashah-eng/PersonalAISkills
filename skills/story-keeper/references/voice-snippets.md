# Voice snippets

Hearing a grandparent laugh or say a grandchild's name is often the most
treasured part of a keepsake. This page covers finding and cutting short
clips of their **real** voice from the family's own videos.

## Where clips come from

- Videos the family already has: birthday toasts, festival videos, weddings,
  video calls the family recorded with permission, phone videos of a story
  being told.
- A new recording made during the interview, with the elder's agreement.
- Voice messages the elder sent to the user (WhatsApp voice notes, for
  example), exported by the user.

Only use recordings the family owns or made, and only with the elder's (or,
if they've died or can't consent, the family's) agreement.

## Finding the moment

```bash
python3 scripts/extract_voice.py video.mp4 --scan
```

`--scan` lists the stretches with sound, which are likely to be talking. The
user (not Claude) listens and chooses. Good clips:

- 10–30 seconds: one complete thought, a laugh, a blessing, a phrase they
  always said, the punchline of a family story.
- Clear enough to hear; background noise is fine and often part of the charm.
- Something the elder would be happy for the family to hear again.

## Cutting it

```bash
python3 scripts/extract_voice.py video.mp4 --start 1:23 --end 1:48 --out nani-mango.m4a
```

The script keeps the audio only, adds a short fade, evens out loudness,
saves small AAC audio (.m4a, about 8 KB per second), and removes every
metadata tag (date, device, location). It runs locally with ffmpeg; nothing is
uploaded. Clips over 30 seconds get a warning and over 90 seconds are refused.

## Captioning it

Under each clip, write the words heard, exactly as said (with a translation
if needed), and when it was recorded if the family knows ("Diwali 2009").
Printed copies show this text in place of the player.

## Never

- Clone, synthesize, or "AI-enhance" a voice into saying anything new.
- Splice words or sentences together, reorder them, or remove words to change
  the meaning. A single continuous clip, trimmed at the start and end, is the
  rule.
- Speed up, pitch-shift or re-voice.
- Use clips for anything outside the family keepsake without the family's
  agreement.

## Without ffmpeg

Install it from https://ffmpeg.org/download.html (or `brew install ffmpeg`,
`winget install ffmpeg`, `sudo apt install ffmpeg`). Or the user can trim the
clip with the phone's built-in editor and attach the result.
