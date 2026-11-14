---
name: grateful
description: Create a seasonal gratitude list (Thanksgiving, Diwali, New Year, year-end or any season) of the people, moments and facts the user is grateful for. Each entry gives a safe, non-revealing reason, the real difference it made, and how the user is already paying it forward or plans to. It opens with a fitting quote, includes a pencil sketch of the occasion, a person (never a likeness) or the feeling, and is written in warm, kind, heartfelt handwriting in the user's own language. Use when the user wants to list what they're grateful for, write a gratitude reflection, journal, post, or share at the holiday table.
argument-hint: "[season or occasion] [--private | --family | --public] [number of entries]"
---

# Grateful

A gratitude list is easy to write and easy to forget: "family, health, my job".
This skill helps the user write one they'll want to keep. Each entry names a
real person, moment, or fact, says honestly why it mattered and what changed
because of it, and shows how the good is travelling on. It is gentle,
personal, and safe to share.

It is a sibling of ThankYou: a thank-you note speaks *to* someone, while a
gratitude list is the user's own reflection, which they can keep, read at the
holiday table, send to family, or post.

## Non-negotiables

1. **Safe and non-revealing.** The reasons never reveal health, money,
   addresses, contact details, ID numbers, legal or immigration matters, or
   anyone's private story. Abstract instead: "grateful my dad is home and
   laughing again", not the diagnosis; "grateful we found our footing this
   year", not the debt. See `../thankyou/references/safety.md`.
2. **Other people's privacy.** People in the list are named the way the user
   chooses. For anything **shared beyond the family or posted publicly**, use
   roles, not names ("my sister", "a colleague who covered for me", "our
   neighbour"), and nothing about their lives they haven't shared themselves.
3. **Kind, always.** Warm, humble, and heartfelt. No comparisons with people
   who have less ("at least I'm not…"), no bragging or humble-bragging, no
   guilt, no backhanded lines, and nothing that could hurt someone who reads
   it, including people left off the list.
4. **True, in the user's words.** Every entry, every "difference it made", and
   every pay-it-forward line comes from the user or is confirmed by them.
   Never invent gratitude, outcomes, or good deeds. A plan is written as a
   plan ("this winter I'll…"), not as something already done.
5. **The user's language.** Write in the language the user writes to you in,
   or the language they ask for. Mixed families get a bilingual touch. Never
   guess a language from a name (`../thankyou/references/language.md`).
6. **Connectors are optional and read-only.** If the user wants help
   remembering the year, Claude may look through connected calendars, photos,
   email or chat for moments, and shows one-line suggestions for the user to
   accept or drop. WhatsApp and SMS are read only with explicit permission.
7. **Sharing follows the delivery rule.** Nothing is sent or posted without an
   explicit yes to the exact text, audience, and channel
   (`../thankyou/references/delivery.md`).

## Workflow

### 1. Understand the ask (one short exchange, only if needed)

- **Season or occasion**: Thanksgiving, Diwali, Lunar New Year, Christmas,
  Eid, New Year, a birthday, year-end, or "just this season".
- **Who will see it** (sets how personal it can be):
  - `--private` (default): a journal entry for the user.
  - `--family`: read at the table or sent to the family chat.
  - `--public`: a social post or a team channel. Use roles, not names, and
    keep it lighter.
- **How many entries**: default 3, up to 7. Fewer, deeper entries beat a long list.
- **Language**: whatever the user writes in, unless they say otherwise.

### 2. Gather what they're grateful for

Ask gentle, open questions, and stop as soon as there's enough:
1. "Who made this year better, even in a small way?"
2. "Is there a moment you don't want to forget?"
3. "Something ordinary you're glad you didn't take for granted?"
4. "Anything that was hard, where something or someone helped you through?"
   (Keep the hardship itself out of the list unless they want it in, and
   abstracted.)

Gratitude can be for a **person** (a mentor, a sister, the bus driver who
waits), a **moment** (the first morning in the new home), or a **fact** (the
team shipped together, the kids are learning to cook, the garden came back).

**With connectors (optional, ask first):** look for the year's warm moments
(milestones on the calendar, photo albums, "thank you" threads) and offer them
as one-line suggestions to accept, change, or drop. Follow
`../thankyou/references/connector-mining.md`.

### 3. Shape each entry

For each person, moment, or fact, write four short parts. Each is one line,
two at most:

| Part | What it says | Example |
|---|---|---|
| **Who / what** | the subject, named as the user chooses | "My sister Anu" (private), or "My sister" (public) |
| **Why** | a reason that reveals nothing sensitive | "for the Sunday calls that never once felt like a chore" |
| **The difference it made** | something real that changed | "I came out of a hard year steadier than I went in." |
| **Paying it forward** | how the user is passing it on, already or as a plan | "I've started calling Dad every Sunday too." / "This winter I'll do the same for a friend who's on her own." |

The pay-it-forward line is optional per entry but aim for at least one in the
list. It must be true or a real plan; frame it as the gift travelling on, not
as the user's virtue (`../thankyou/references/paying-it-forward.md`).

**Safe reasons, abstracted:**

| Raw | Write instead |
|---|---|
| "my mom beat cancer" | "every ordinary evening with my mom this year" |
| "my brother paid off our loan" | "my brother, who quietly stood with us when it counted" |
| "my therapist" | "the people who helped me find my footing" |
| "got the visa" | "being home with the people I love" |
| "my promotion and raise" | "work that stretched me, and a team that had my back" |

### 4. Pick the opening quote

One short quote that reflects what the list is really about, not generic
gratitude. Follow `../thankyou/references/quotes.md`: real, correctly
attributed (or "Proverb"), in the user's language when a good one exists, with
a translation if needed. Examples: Cicero's "Gratitude is not only the greatest
of virtues, but the parent of all the others" for a broad list; 饮水思源 ("when
you drink water, remember its source") for a list about mentors; Dickens's
"I will honour Christmas in my heart, and try to keep it all the year" at
Christmas.

### 5. Write it

Structure:
1. **Quote**, with attribution and translation if needed.
2. **Title**, in the user's language: "This season, I'm grateful for…" /
   "इस दिवाली, मैं आभारी हूँ…" / "Este año, doy gracias por…".
3. **An opening line or two**, optional: what kind of year it was, gently
   ("It was a year of small mercies.").
4. **The entries** (3–5).
5. **A closing reflection**: one or two lines tying it together, often a
   shared pay-it-forward intention.
6. **Signature and season** ("Hardik, Thanksgiving 2026"), for private and
   family versions.

**Tone:** warm, tender, a little emotional, and never dramatic. Write it like
a handwritten page: contractions, short sentences, natural rhythm, plain
words. One exclamation mark at most. No clichés ("blessed beyond measure",
"words can't express"). It should sound like the user on a quiet evening.

### 6. Sketch the occasion, a person, or the feeling

Follow `../thankyou/references/sketch.md`. Draw an original pencil-style SVG
(graphite on warm paper, wobbly doubled lines, hatching, one coloured-pencil
accent):
- **The occasion:** a harvest table, a row of diyas, a lantern, a winter window.
- **A person,** only as a simple figure from behind or a silhouette, never a
  likeness: a grandmother's hands around a cup, two figures on a bench.
- **The feeling:** steam rising from a cup by an open window, a lit porch light
  on a dark street, a small boat in calm water, a seedling in a cracked pot.

If the user has a real photo they'd like to use, follow
`../thankyou/references/photos.md`. Otherwise the sketch is the picture.
Captions describe the scene, never claim it's a real photo of "us".

### 7. Safety pass

```bash
python3 ../thankyou/scripts/safety_check.py grateful.json --profile grateful
```

The `grateful` profile adds checks for comparison with others' misfortune,
bragging, and guilt, on top of the PII, financial, health and tone checks.
Fix every blocking flag. Then re-read: *Would everyone mentioned be glad to
read this? Would someone not on the list feel hurt? Is anything revealed that
isn't the user's to share? For `--public`: are there roles instead of names?*

### 8. Render and deliver

```bash
python3 ../thankyou/scripts/render_card.py grateful.json --art sketch.svg --out grateful.html
# with a real photo of the user's own instead: add --photo photo.jpg
python3 ../thankyou/scripts/card_to_png.py grateful.html --out grateful.png
python3 ../thankyou/scripts/share.py grateful.json --channel whatsapp
```

The card is handwritten by default (`--style print` for a typeset version):
the sketch across the top, then the quote, the title, and numbered entries,
each with its reason, the difference it made, and an ↪ pay-it-forward line. Give the user:
- the card (keep it as a file; publish a link only if they ask),
- the plain text (for a journal, a toast, or a caption),
- for `--family` or `--public`, the channel version and share link. Send or
  post only after an explicit yes (`../thankyou/references/delivery.md`).

Offer once, lightly: "Would you like to send a thank-you note to anyone on
this list?" If so, hand over to the ThankYou skill.

## grateful.json format

```json
{
  "kind": "gratitude",
  "visibility": "private",
  "sender_first_name": "Hardik",
  "language": "en",
  "direction": "ltr",
  "occasion": "Thanksgiving 2026",
  "quote": {"text": "…", "attribution": "…", "translation": null},
  "title": "This season, I'm grateful for…",
  "body": ["optional opening line"],
  "items": [
    {"subject": "My sister", "why": "…", "difference": "…", "forward": "…"}
  ],
  "closing": "closing reflection",
  "signature": "Hardik, Thanksgiving 2026",
  "photo": {"source": "sketch", "caption": "…", "alt": "…"},
  "palette": {"bg": "#F6E7D6", "ink": "#3B2F2A", "accent": "#B5562F", "paper": "#FFFDF9"}
}
```

`visibility` is `private`, `family`, or `public`. `forward` is optional per
entry. Everything visible, including every entry, is safety-checked.

## Files

- `examples/`: an English Thanksgiving list and a Hindi Diwali list, each with
  a drawn pencil sketch
- Shared with ThankYou (`../thankyou/`):
  - `references/`: safety, language, quotes, sketch, photos, paying-it-forward, delivery, connector-mining, relationships-and-culture
  - `scripts/`: safety_check (`--profile grateful`), render_card (renders `items`), share (formats `items`), card_to_png, sketch_photo
