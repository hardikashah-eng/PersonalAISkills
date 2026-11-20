---
name: story-keeper
description: Help someone record and keep the life stories of a parent, grandparent or elder as a family keepsake booklet, with gentle interview questions in the elder's own language, their stories in their own words, the family's own photos (optionally as pencil sketches), and short clips of their real voice cut from family videos. Consent first, the family decides what's kept and shared, and voices are never cloned or altered. Use when the user wants to capture, preserve or write down a family member's memories, or make a memory book for a birthday, anniversary or reunion.
argument-hint: "[elder, e.g. Nani] [occasion] [--photos <folder>] [--videos <folder>] [--language gu]"
---

# Story Keeper

Every family has stories that live in one person's head: how grandparents
met, the village, the journey, the recipe, the joke that's been told for fifty
years. This skill helps the user ask, listen, and keep those stories in a
booklet the whole family can open for generations, with photos and, when
there's a family video, the person's real voice telling it.

## Non-negotiables

1. **Consent first.** The elder agrees to being interviewed and to what's kept.
   If they can no longer consent (for example, advanced memory loss), work only
   with the family's shared memories, and the family decides together. A
   remembrance book for someone who has died is made only at the family's wish.
2. **The family decides what's shared.** The booklet is private by default
   ("Shared only with the family."). Nothing is posted publicly unless the
   elder and family ask for it.
3. **Their words, their voice.** Stories are written in the first person, as
   close to how they said it as possible; edit only for clarity, never to
   change meaning or add events. Voice clips are cut from real recordings at
   the user's chosen times. **Never clone, synthesize, re-voice or splice** a
   voice, and never generate "new" lines in their voice.
4. **Real photos stay real.** Use the family's own photos. Allowed: straighten,
   crop, gentle brightness fix, or a whole-photo pencil sketch on request. Not
   allowed: AI face "restoration", colourising presented as original, adding or
   removing people (`../thankyou/references/photos.md`).
5. **Painful memories are the elder's to share.** Don't push on loss, war,
   partition, illness, abuse or hardship. If they bring it up, listen; keep it
   in the book only if they say so, and in the words they choose.
6. **No sensitive details.** Leave out addresses, ID numbers, finances, health
   and anything that could embarrass a living person
   (`../thankyou/references/safety.md`). Old village or city names are fine.
7. **Their language.** Ask questions in the language they're most at home in;
   keep their words in that language, with a translation for grandchildren
   who need it (`../thankyou/references/language.md`).

## Workflow

### 1. Plan with the user

- **Who** (Nani, Dada, Mom, Uncle Joe) and their **language**.
- **The occasion and audience**: a birthday, an anniversary, Diwali, a family
  reunion, or just "before we forget"; grandchildren of what ages.
- **How the stories will be gathered**: the user interviews in person or on
  a call, records audio, or already has stories (letters, notes, a recorded
  talk). Suggest short sessions (30–45 minutes) over several days.
- **Photos and videos** the family already has, and who can share them.

### 2. Prepare the interview (`references/interview-guide.md`)

Pick 10–15 questions from the guide, by life chapter (childhood, family,
work, love, moving, traditions and food, lessons, wishes), translated into the
elder's language. Lead with easy, happy questions; save reflection for later.
Give the user the list as a printable sheet and as a message they can read
from their phone.

### 3. Turn conversations into stories

From the user's notes, transcript or recording summary:

- Group memories into **3–7 chapters**, each a place or time ("The mango
  tree", "The train to Bombay", "Sunday dal").
- Write each in the **first person**, in the elder's voice and phrasing, and
  keep their own words in the original language with a translation.
- Pull one line per chapter as a **pull quote**, in their words.
- Mark anything unsure ("1967 or 1968?") and ask the user rather than guess.
- **Read it back to the elder** (or have the user do so) before anything is
  printed or shared.

### 4. Photos of the people in the stories

Ask the user for photos of the elder and the people in the stories (parents,
grandparents, siblings, the house, the shop, the wedding):

- Use them as they are, after cleaning (remove the metadata, `../thankyou/references/images.md`).
- Old prints: help photograph or scan them flat, then crop and straighten.
- A **pencil sketch** of a photo is available on request (`"sketch": true`),
  and can look lovely for the cover; keep the original for the family.
- No photo of a place or time? Offer a drawn pencil sketch of the scene,
  labelled as a drawing (`../thankyou/references/sketch.md`).
- Captions name who's in the photo and roughly when, as the family knows it.

### 5. Voice snippets from family videos (`references/voice-snippets.md`)

If the family has videos of the elder talking (a birthday toast, a festival,
a phone video of them telling a story), cut 1–3 short clips (10–30 s each) of
their real voice, such as `nani-mango.m4a` from 1:23 to 1:48 of
`diwali-2009.mp4`. The user trims the clip, or you do if your environment can
(`references/voice-snippets.md`).

Listen with the user and let them choose the moment. Add the words heard in
the clip as a short transcript (and a translation if needed), written as said.
The clip plays in the HTML booklet; printed copies show the transcript.

### 6. Build the keepsake

Fill `keepsake.json` (see `examples/nani-stories/keepsake.json`) and build
`nani-stories.html` from it, following `references/booklet-layout.md`. For
printing, the user prints it to PDF from their browser.

The booklet has a cover (title, the elder's photo, a dedication), one page per
chapter (story, photo, pull quote, voice clip) and closing words ("What I want
you to remember"), written in handwriting-style type with readable body text.
It's one self-contained file that works offline.

### 7. Review and share

Check the text before sharing with `../thankyou/references/safety-checklist.md`
(the every-note and family checks).

Then the elder (or the family) approves it. Share privately: as a file in the
family chat, by email, on a family drive, or printed as a gift. Follow
`../thankyou/references/delivery.md`; send only on an explicit yes.

## keepsake.json

```json
{
  "title": "Nani's Stories", "subtitle": "As told to Anaya, Diwali 2026", "language": "en",
  "cover_photo": {"path": "nani-1972.jpg", "caption": "…", "alt": "…", "sketch": false},
  "dedication": "…",
  "chapters": [{
    "title": "…", "when": "…", "story": ["first-person paragraph", "…"], "pullquote": "…",
    "photos": [{"path": "…", "caption": "…", "alt": "…", "credit": "…", "sketch": false}],
    "voice": {"path": "clip.m4a", "label": "Hear Nani tell it", "transcript": "…", "translation": "…", "recorded": "Diwali 2009"}
  }],
  "closing": {"title": "…", "body": ["…"], "signature": "…", "photo": {"path": "…"}},
  "colophon": "Kept by …, with …'s blessing. Shared only with the family.",
  "palette": {"bg": "#EFE6D8", "ink": "#3A2E25", "accent": "#9A5B34", "paper": "#FFFCF6"}
}
```

## Files

- `references/interview-guide.md`: questions by life chapter, and how to listen
- `references/voice-snippets.md`: finding, cutting and captioning voice clips; what never to do
- `references/consent-and-care.md`: consent, memory loss, painful memories, remembrance books
- `references/booklet-layout.md`: build the booklet (one HTML file that also prints)
- `examples/nani-stories/`: a three-chapter example with drawn stand-in pictures
- Shared with ThankYou: `../thankyou/references/{safety-checklist,images,sketch}.md` and its other references
