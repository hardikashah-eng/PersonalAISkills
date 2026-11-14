---
name: thankyou
description: Write a heartfelt, one-of-a-kind thank-you note (Thanksgiving, holidays, Diwali, farewells, any occasion) that opens with a fitting quote, recalls the specific moment the recipient made a real difference (found via the user's email, chat, LinkedIn, or opt-in WhatsApp/SMS), fits the relationship and culture, uses the native language when appropriate, and includes a small original artwork and, when the user has one, a photo from a good time together. Use when the user asks to thank someone or write thank-you notes.
---

# ThankYou

A thank-you note lands when it proves the sender *noticed*. Generic gratitude
("thanks for everything!") is forgettable; "the Sunday you spent walking me
through my first on-call incident is why I stayed in this field" is kept for
years. This skill finds that specific moment — using the sender's own
communication history when they have connected it — and turns it into a warm,
safe, personal note with a quote, a small piece of art made only for the
recipient, and, when the user has one, a photo from a good time they shared.

## Non-negotiables (apply to every step)

1. **Kind, always.** Warm, sincere, humble. Never rude, sarcastic, judgemental,
   guilt-inducing, explicit, or backhanded ("despite your usual chaos…").
   No comparisons to others, no jokes at anyone's expense.
2. **No sensitive data in the note.** No personally identifiable information
   (addresses, phone numbers, emails, ID/account numbers, birthdates, workplace
   internals), no financial details (amounts, salaries, loans, prices), no health
   details (conditions, diagnoses, treatments, hospitals, therapy, pregnancy).
   If the moment involved one of these, *abstract it*:
   - "when you lent me $2,000 for rent" → "when you stepped in without a second thought during a hard month"
   - "you drove me to chemo every week" → "you showed up, week after week, when it mattered most"
   See `references/safety.md`.
3. **Read-only on connectors. Never send.** Search and read only what is needed
   to find the moment. Never send, post, reply, or react on the user's behalf.
   Creating a *draft* is allowed only when the user asks; sending needs their
   explicit go-ahead on the final text.
4. **The user confirms the moment.** Anything mined from connectors is shown to
   the user as a one-line summary before it goes into a note — they decide
   whether it is accurate and appropriate to mention.
5. **Nothing about third parties** beyond what the recipient already knows; no
   quoting private messages verbatim unless the user wrote them and wants it.
6. **Honest quotes.** Never invent or misattribute a quote (see `references/quotes.md`).
7. **Private channels are opt-in.** WhatsApp, SMS/iMessage, and other personal
   messaging are read only after the user explicitly allows it *for this note*
   ("Yes, you can look at my WhatsApp chat with Priya"). Ask once; a no is final.
8. **Respect the person being thanked.** Adjust tone to the relationship
   (spouse, parent, sibling, friend, mentor, colleague…), steer around anything
   that could be painful for them, and follow their cultural norms
   (`references/relationships-and-culture.md`).
9. **Photos: the user's own, chosen by the user, never altered.** Use only
   photos from the user's own library, drive, attachments, or the two people's
   shared threads; never from the web, social media, or profile pictures.
   Never identify anyone by face, and never edit or generate a person's face or
   body. Metadata is always stripped. See `references/photos.md`.

## Workflow

### 1. Understand the ask (one short exchange, only if needed)

Collect what is not already given:
- **Recipient** — first name (and how the user refers to them) and relationship
  (spouse/partner, parent, child, sibling, grandparent, in-law, friend, mentor,
  teacher, manager, colleague, report, neighbour…). The relationship sets the
  tone, form of address, and sign-off — see the table in
  `references/relationships-and-culture.md`.
- **Anything tender for them right now?** — ask briefly unless context makes it
  clear ("Anything I should steer clear of — a recent loss, a hard year?").
  Steer around it silently; never name it in the note.
- **Culture / traditions**, only when relevant and not already clear — which
  holiday they celebrate, honorifics, formality. Never infer from a name.
- **Occasion** — Thanksgiving, Christmas/holidays, Diwali, Lunar New Year,
  farewell, promotion, "just because"… Default: no occasion, a general thank-you.
- **Format** — handwritten card (~80–120 words), email (~120–200 words),
  chat message (~40–70 words). Default: card.
- **Tone dial** — warm-professional (colleague, manager) or warm-personal
  (friend, family). Infer from the relationship; ask only if unclear.

If the user is thanking many people (e.g. "thank-yous for my whole team"),
do the steps per person and keep each note distinct — no copy-paste templates.

### 2. Find the moment that made a tangible difference

**If personal connectors are available** (email: Gmail/Outlook; chat: Slack,
Teams, Lark/Feishu; LinkedIn; calendar; and — only with explicit permission —
WhatsApp and SMS/iMessage), follow `references/connector-mining.md`:
- Check which connectors are connected; do not ask the user to connect more
  unless nothing is available — then mention once which connector would help.
- Search for the recipient by name/handle, then for gratitude and impact
  signals ("thank you", "couldn't have", "that worked", "got the offer",
  "intro", "recommend", "advice", "unblocked", "covered for me").
- Score candidate moments (rubric in the reference) and keep the top 2–3.
  The best moment has a **before → help → after** shape: the user was stuck or
  facing something, the recipient did something specific, and something real
  changed (a job, a launch, a skill, confidence, a hard week survived).
- Present the candidates to the user as one-liners, already abstracted to be
  safe, and let them pick or correct:
  > 1. Mar 2024 — Priya reviewed your design doc on a weekend; it became the approved architecture.
  > 2. Aug 2025 — she introduced you to the hiring manager at your current team.

**If no connectors (or nothing found)**, ask at most three questions:
1. What did they do — one specific time you remember?
2. What changed for you because of it?
3. Anything about them (a hobby, a phrase they say, something they love) that
   could inspire a small drawing? (optional)

Never fabricate a moment. If the user gives nothing specific, write a shorter,
honest note about qualities they've shown, and say it would be stronger with one real memory.

### 3. Choose the language

Follow `references/language.md`. In short:
- Write in the language the user and the recipient actually use with each other
  (visible in their messages), or the language the user writes to you in.
- If the user is a non-English speaker (they write to you in another language,
  or ask for it), write the note in their native language.
- If the relationship is mixed (e.g. Hindi/English, Spanish/English), offer a
  **bilingual touch**: the greeting, a key line, or the closing in the native
  language, the body in the shared working language. Keep honorifics and
  culturally right greetings (e.g. "Shukriya", "Muchas gracias de corazón",
  "Danke von Herzen", "感谢您").
- Do not guess a language from a person's name or ethnicity — only from how
  they actually communicate or what the user says.

### 4. Pick an opening quote

Follow `references/quotes.md`: one short (≤ 25 words) quote that fits the
*specific* moment (mentorship, kindness, courage, friendship, teaching), not a
generic gratitude line. Prefer public-domain authors, proverbs, or scripture/
classical texts with well-established attribution; in the note's language when
a good native-language quote exists (e.g. a Sanskrit subhashita with translation,
a Spanish refrán). If attribution is uncertain, label it "Proverb" or use an
original line clearly unattributed — never put words in a real person's mouth.

### 5. Write the note

Structure (keep it short — specific beats long):

1. **Quote** — italic line with attribution.
2. **Greeting** — first name, matching the relationship ("Dear Priya," / "Hi Sam,").
3. **The moment** — one or two sentences naming what they did, concretely
   (abstracted per the safety rules).
4. **The difference** — what changed for the sender because of it. This is the
   heart of the note; be specific and honest, not grand.
5. **What it says about them** — one sentence about the quality it showed
   (generosity, patience, belief in people). Sincere, not flattering.
6. **Occasion tie-in** — one line connecting to Thanksgiving/holiday/etc., if any.
7. **Warm close + signature** — "With gratitude," / "Thank you, truly," + sender's first name.

Match the relationship: tender for a spouse, reverent for a parent or elder,
lightly playful (never teasing) for a sibling or close friend, warm-professional
for a manager or colleague, encouraging for a child or report. Use the honorific
and register the recipient's culture expects (formal *you* for elders and
teachers in languages that have one). Only mention a holiday they celebrate.

Style: plain words, first person, active voice. One exclamation mark at most.
No clichés stack ("words cannot express…", "you're the best ever"). No
over-sharing about the sender's own struggles. Read it aloud — it should sound
like the sender, not a greeting-card company.

### 6. Make a small artwork for this person only

Follow `references/art.md`. Draw a small original SVG (about 320×200) built from
2–3 motifs taken from the shared moment and the recipient's interests
(e.g. a lighthouse for "you guided me", a bridge for an introduction, a seedling
for mentorship, a coffee cup for the 7am calls) plus the occasion
(autumn leaves, snowflakes, diyas, lanterns). Rules: no faces of real people,
no logos, brands, or copyrighted characters, no text containing PII. A tiny
hidden-in-plain-sight detail (their favourite colour, a constellation, initials
of the first name only) makes it one-of-one. Save it as `art.svg`.

### 7. Add a photo of a good time together (optional)

A real photo from the moment you're thanking them for, or from a happy time
together, makes the note unmistakably personal. Follow `references/photos.md`:

- **Find candidates by context, never by face**, in the user's own sources:
  photos from the date or event of the moment (their connected photo library
  or drive, such as Google Photos, OneDrive, or iCloud via a connected folder),
  photos the two of them already exchanged in email or chat (WhatsApp/SMS only
  with the same opt-in), albums or person labels the user created, or a photo
  the user attaches. Often the quickest path is to ask: "Do you have a photo
  from that time together? You can attach it here."
- **A photo of the shared thing counts.** The whiteboard from that night, the
  trail you hiked, or the lab bench can be as personal as a photo of people.
- **Check it's right for them.** It should be happy, flattering, and from a good
  time, with nothing inappropriate, no former partners, no one they've lost
  (unless the user wants a remembrance), no other people's children, no
  addresses, plates, or screens in frame, and nothing at odds with their
  culture. If in doubt, skip it.
- **The user picks.** Show 2–4 candidates; use only the one they choose. Crop,
  straighten, or brighten if needed, but never retouch, alter, or generate a
  person.
- **Caption it warmly.** One short line with no personal details, such as
  "The night the demo finally worked, 2019". Add plain alt text.

No good photo? That's fine. The drawing carries the card on its own.

### 8. Safety pass — mandatory before showing the note

Run the automated check, then review by hand:

```bash
python3 scripts/safety_check.py note.json
```

The script flags emails, phone numbers, URLs, long numbers, currency amounts,
health and financial terms, and harsh words, in the note and in the photo
caption and alt text. Fix every flag (abstract or remove) and re-run until
clean. Then re-read against the non-negotiables above — the script is a
backstop, not a substitute for judgement. Ask: *Would the recipient feel seen
and happy? Would anything make them uncomfortable if someone read it over their
shoulder? Does anything touch a trigger, or break a norm of their culture or
our relationship? Would they be glad to see this photo?*

### 9. Deliver

Render a card the user can view, print, or screenshot:

```bash
python3 scripts/render_card.py note.json --art art.svg --out thankyou-<firstname>.html
# with a photo (metadata is stripped; --photo-out saves the clean copy to attach)
python3 scripts/render_card.py note.json --art art.svg --photo moment.jpg \
  --photo-out moment-clean.jpg --out thankyou-<firstname>.html
```

Give the user:
- the rendered card (send the HTML file). If it contains a personal photo,
  keep it as a file or draft; publish it as a shareable link only if the user
  explicitly asks,
- the plain-text version ready to paste into a card, email, or chat,
- one line on the moment you used and why, and an offer to adjust tone, length,
  or language.

If they want it emailed, create a **draft** in their email connector and tell
them it's waiting in Drafts, with the cleaned photo attached if there is one.
For WhatsApp/SMS, give the text ready to paste and suggest sending the cleaned
photo first (the card can also be sent as an image). Do not send.

## note.json format

```json
{
  "recipient_first_name": "Priya",
  "sender_first_name": "Hardik",
  "language": "en",
  "direction": "ltr",
  "occasion": "Thanksgiving",
  "quote": {"text": "…", "attribution": "…", "translation": null},
  "greeting": "Dear Priya,",
  "body": ["paragraph 1", "paragraph 2"],
  "closing": "With gratitude,",
  "signature": "Hardik",
  "photo": {"caption": "The night the demo finally worked, 2019", "alt": "A whiteboard covered in boxes and arrows"},
  "palette": {"bg": "#FBF6EE", "ink": "#3B2F2A", "accent": "#C8693C"}
}
```

`translation` is used when the quote is in another language (shown under it).
`direction` is `rtl` for Arabic, Hebrew, Urdu, Persian.
`photo` is optional; the image file itself is passed with `--photo`.

## Files

- `references/connector-mining.md` — how to search each connector, impact scoring rubric
- `references/quotes.md` — choosing and verifying quotes, starter bank by theme
- `references/language.md` — language detection and bilingual patterns
- `references/art.md` — motif library and SVG rules for the one-of-one artwork
- `references/safety.md` — what never goes in a note, and how to abstract it
- `references/relationships-and-culture.md` — tone by relationship, recipient triggers, cultural norms
- `references/photos.md` — finding, choosing, cleaning, and captioning a photo of a good time together
- `scripts/safety_check.py` — automated PII / financial / health / harshness scan
- `scripts/render_card.py` — renders note.json + art.svg (+ optional photo, metadata stripped) into a printable HTML card
- `examples/` — a finished sample (note.json, art.svg, rendered card)
