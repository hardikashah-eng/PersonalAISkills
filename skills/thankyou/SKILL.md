---
name: thankyou
description: Write a heartfelt, one-of-a-kind thank-you note to a person, a team (--team), an organization (--org), or family (--family) for Thanksgiving, holidays, Diwali, farewells or any occasion. It opens with a fitting quote, recalls the specific moment or shared achievement that made a real difference (found via the user's email, chat, LinkedIn, or opt-in WhatsApp/SMS), fits the relationship and culture, uses the native language when appropriate, can show how the sender is paying it forward, and includes a small original artwork and, when available, a photo from a good time together. It helps deliver the note by email, WhatsApp, SMS, Slack, Teams, Lark, LinkedIn or other messengers, sending only after the user explicitly approves the exact message. Use when the user asks to thank someone, their team, an organization, or their family.
argument-hint: "[--team <name> | --org <name> | --family [name]] [recipient] [occasion] [via whatsapp|email|sms|slack|...]"
---

# ThankYou

A thank-you note lands when it proves the sender *noticed*. Generic gratitude
("thanks for everything!") is forgettable; "the Sunday you spent walking me
through my first on-call incident is why I stayed in this field" is kept for
years. This skill finds that specific moment — using the sender's own
communication history when they have connected it — and turns it into a warm,
safe, personal note with a quote, a small piece of art made only for the
recipient, and, when the user has one, a photo from a good time they shared.

## Who is being thanked: modes

| Mode | Use for | Guide |
|---|---|---|
| *(default)* | one person: a mentor, friend, colleague, teacher, neighbour | this file |
| `--team <name>` | a group the sender worked with or led: their team, a project crew, a class, a volunteer group | `references/team-and-org.md` |
| `--org <name>` | an organization as a whole: a partner company, nonprofit, school, club, former employer | `references/team-and-org.md` |
| `--family [name]` | one relative (`--family Mom`) or the whole family (`--family`) | `references/family.md` |

The mode comes from the arguments when given (`/thankyou --team Platform
Thanksgiving`), otherwise from plain language ("thank my team for the launch",
"a note to my parents"). If it's genuinely unclear, ask once. The mode changes
what to look for (a shared achievement and goal reached together for a team or
org; one picture of a lifetime for family), the tone, the photo, and the
safety checks. Every other step and rule below still applies.

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
3. **Read-only while searching; send only on an explicit yes.** Search and read
   only what is needed to find the moment. Never reply, react, or post anything
   while searching. Deliver only through the channel the user chooses, and
   **send or post only after the user says yes to that exact message, recipient,
   and channel** (`references/delivery.md`). Otherwise, create a draft or give
   ready-to-send text. Never send unattended or on a schedule.
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
10. **Groups: everyone or no one.** In team, org, and whole-family notes,
    credit the group first. If you name individuals, name every member, each
    with something specific; otherwise name no one. Never rank or compare
    people. No confidential business details in team or org notes.
11. **Paying it forward only when true.** A line about how the sender passes
    the gift on is included only if the user confirms it, and it never names
    or exposes the people they helped (`references/paying-it-forward.md`).

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

If the user wants **separate notes for each person** (e.g. "a thank-you for each
person on my team"), do the steps per person and keep each note distinct — no
copy-paste templates. If they want **one note to the group**, use `--team`,
`--org`, or `--family` mode.

**Team / org:** also learn who's in the group (get the roster if anyone will be
named), the goal achieved together, the sender's role (leader, peer, partner,
customer), and where the note goes (channel post, card, email).
**Family:** also learn what the sender calls them (Mom, Amma, Nani, Abuela…)
and the language of the home. See the mode guides.

### 2. Find the moment that made a tangible difference

**Team / org mode:** look for the **shared achievement**, the goal reached
together: launch and milestone threads in the team channel, release notes,
retros, partner emails, the offsite on the calendar. Build the arc *goal → what
it took → the moment it landed → what it made possible*, and offer 2–3
candidates (`references/team-and-org.md`).
**Family mode:** turn the lifetime of gratitude into **one picture**, a single
moment that sums it up, usually from the user ("Is there one moment that sums
it up?") (`references/family.md`).

**Paying it forward (any mode, optional):** ask once whether the sender has
passed the gift on, by teaching it, doing the same for someone else, or
building on it. Use it only if it's real (`references/paying-it-forward.md`).

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
6. **Paying it forward** (optional, only if true) — one or two sentences on how
   the sender passes it on, framed as the giver's influence: "I've passed that
   on to every engineer I've mentored since."
7. **Occasion tie-in** — one line connecting to Thanksgiving/holiday/etc., if any.
8. **Warm close + signature** — "With gratitude," / "Thank you, truly," + sender's first name.
9. **P.S. fun fact** (when it fits) — one short, true, delightful fact tied to
   the relationship or occasion, with a warm tie-back: "P.S. Fun fact: "mentor"
   comes from Mentor, the friend Odysseus trusted to guide his son. You were
   mine." Use the verified bank in `references/fun-facts.md`, or verify a new
   fact in an original source and record it in `fun_fact.source`. Skip it for
   hard-time notes or when nothing fits naturally.

If the note lists several things, don't number them. The card draws a small
hand-drawn mark for each one, and plain text uses ✦.

**Team / org notes** follow the same shape with the group as the subject:
greeting to the group → the goal and the moment it landed → what it took
(collectively, or for *every* named person) → what it made possible → paying
it forward → occasion → close. Lead with "we", keep business details
non-confidential, and avoid anything that reads like a performance review.
Also give a channel-ready version (about 80–150 words, no card formatting).
**Family notes** use the family's own forms of address and sign-offs ("Dear
Amma," … "Your loving son,"), often the home language, and no guilt, debt,
ranking, or pressure. A blessing in the family's tradition fits the close.

Match the relationship: tender for a spouse, reverent for a parent or elder,
lightly playful (never teasing) for a sibling or close friend, warm-professional
for a manager or colleague, encouraging for a child or report. Use the honorific
and register the recipient's culture expects (formal *you* for elders and
teachers in languages that have one). Only mention a holiday they celebrate.

Style: plain words, first person, active voice. One exclamation mark at most.
No clichés stack ("words cannot express…", "you're the best ever"). No
over-sharing about the sender's own struggles. Read it aloud — it should sound
like the sender, not a greeting-card company.

**Write it like a handwritten note**, because the card is rendered in
handwriting by default. Use contractions ("I've", "you're", "it's"), short
sentences, and the rhythm of someone writing by hand. Small asides are fine
("and yes, I still have the marker"), but there are no bullet points and no
formal phrasing ("I would like to express my gratitude…").

### 6. Make a small artwork for this person only

Follow `references/art.md`. Draw a small original SVG (about 320×200) built from
2–3 motifs taken from the shared moment and the recipient's interests
(e.g. a lighthouse for "you guided me", a bridge for an introduction, a seedling
for mentorship, a coffee cup for the 7am calls) plus the occasion
(autumn leaves, snowflakes, diyas, lanterns). Rules: no faces of real people,
no logos, brands, or copyrighted characters, no text containing PII. A tiny
hidden-in-plain-sight detail (their favourite colour, a constellation, initials
of the first name only) makes it one-of-one. Save it as `art.svg`.
For a team or org: a rowing boat with one oar per person, a constellation with
one star per member, a relay baton, a bridge of many planks. For family: a
family tree with one leaf per person, a home with lit windows, a long table.

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

**Team / org photo:** a group photo from the moment (the launch-day shot, the
offsite, the event), preferably one already shared with that group. Everyone
pictured should belong to the group, and if a few people are missing, use a
photo of the shared thing instead (the finished build, the launch cake, the
event banner). **Family photo:** a happy family moment; children only if
they're the user's own family and the user picks it; respect relatives' wishes
about photos.

**No suitable photo? Use a pencil sketch of the moment** (`references/sketch.md`):
- **Default: draw it.** Make an original pencil-style SVG of the *scene*, such
  as the whiteboard, two cups and an open notebook, or a team roped together
  near a summit flag. Use graphite greys on warm paper, wobbly doubled lines,
  hatching, and at most one coloured-pencil accent. People appear only as
  simple figures from behind or at a distance, never as a likeness.
- **Or a freely licensed stock photo turned into a sketch**, when a place
  needs to look real. Use only public domain, CC0, or free-to-use licences,
  checked on the photo's page. Scenes and objects only; never people, public
  figures, or anything from social media. Convert it with
  `scripts/sketch_photo.py`, and credit the author if the licence asks.
- **Be honest.** A sketch or stock image isn't a photo of their moment. Never
  write "found this photo" or "remember this?", and never caption it as "us".
  Set `"source": "sketch"` or `"stock"` so the safety check can enforce this.

The user can also say no picture at all; the header drawing carries the card.

### 8. Safety pass — mandatory before showing the note

Run the automated check, then review by hand:

```bash
python3 scripts/safety_check.py note.json
# team / org: also checks for confidential details, review language, and
# non-inclusive words; --roster flags anyone left out when some are named
python3 scripts/safety_check.py note.json --profile team --roster "Ana,Ben,Chen,Dev"
# family: also checks for comparison, pressure, and guilt phrases
python3 scripts/safety_check.py note.json --profile family
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

Render a card the user can view, print, or screenshot. Cards are **handwritten
by default**: the note is set in a handwriting font (Caveat, with Kalam for
Devanagari, both bundled and embedded so the card works offline) in ink on card
stock, with slightly uneven lines and a signature. Chinese, Japanese and Korean
use a handwriting-like system font where one is installed; other scripts use the
system font. Use `--style print` for the clean serif look.

```bash
python3 scripts/render_card.py note.json --art art.svg --out thankyou-<firstname>.html
python3 scripts/render_card.py note.json --art art.svg --style print --out thankyou-<firstname>.html
# with a photo (metadata is stripped; --photo-out saves the clean copy to attach)
python3 scripts/render_card.py note.json --art art.svg --photo moment.jpg \
  --photo-out moment-clean.jpg --out thankyou-<firstname>.html
# with a drawn pencil sketch instead of a photo
python3 scripts/render_card.py note.json --art art.svg --photo sketch.svg --out thankyou-<firstname>.html
# with a freely licensed stock photo turned into a pencil sketch
python3 scripts/sketch_photo.py stock.jpg --out sketch.jpg
python3 scripts/render_card.py note.json --art art.svg --photo sketch.jpg --out thankyou-<firstname>.html
```

Then **deliver** it the way the user wants (`references/delivery.md`):

1. **Choose the channel**: what the user says, or where they actually talk
   with this person, or by relationship. Options: email (Gmail/Outlook),
   WhatsApp, SMS/iMessage, Slack, Microsoft Teams, Lark/Feishu, LinkedIn,
   Telegram, Signal, WeChat, LINE, KakaoTalk, or a printed card. Ask once if
   it's unclear.
2. **Format it for that channel**: email gets a subject and the full note;
   chat apps get the photo or card image first, then the text; SMS gets a
   short version; a team gets the channel-ready post.
   ```bash
   python3 scripts/share.py note.json --channel whatsapp     # text + share link
   python3 scripts/card_to_png.py card.html --out card.png   # card as an image
   ```
   If the text is long for the channel, write a shorter version that keeps the
   specific moment (put it in `short_body`), and re-run the safety check.
3. **Deliver**:
   - **A connected app can send** (Gmail, Outlook, Slack, Teams, Lark, …):
     create the draft with the card or photo attached, show the **"Ready to
     send?" preview** (recipient, channel, full text, attachments), and send
     or post only after an explicit yes. "Looks good" is not a yes to send.
   - **No connector for the channel** (most messengers): give the
     channel-ready text, `card.png`, the clean photo, and the share link that
     opens the app with the message filled in (WhatsApp, SMS, email,
     Telegram, LINE). For Signal, WeChat, KakaoTalk, Messenger, and LinkedIn
     without a connector: copy the text and attach the image.
   - **Printed card**: the HTML prints on card stock; suggest A5 or 5×7.
4. **Confirm in one line** what happened ("Sent to Maya by email", "Draft is in
   Outlook", "WhatsApp link ready: tap it, pick Arjun, attach card.png").

Also give the user one line on the moment you used and why, and offer to adjust
tone, length, or language.

Keep any card with a personal photo as a file, draft, or message to the
recipient; publish it as a shareable link only if the user explicitly asks.
Contact details are used only for the send and never saved.

## note.json format

```json
{
  "audience": "individual",
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
  "photo": {"source": "own", "caption": "The night the demo finally worked, 2019", "alt": "A whiteboard covered in boxes and arrows"},
  "palette": {"bg": "#FBF6EE", "ink": "#3B2F2A", "accent": "#C8693C"}
}
```

`translation` is used when the quote is in another language (shown under it).
`direction` is `rtl` for Arabic, Hebrew, Urdu, Persian.
`photo` is optional; the image file itself is passed with `--photo`. Its
`source` is `own` (the user's photo), `sketch` (drawn), or `stock` (with
`credit`, `license`, and `url`).
`style` is `handwritten` (default) or `print`.
`fun_fact` (optional) is `{"text": "Fun fact: …", "source": "where it was verified"}`;
it's printed as a P.S. under the signature. `bullet` (optional) picks the
hand-drawn list mark: `sparkle` (default), `leaf`, `heart`, or `star`.
`channel` (optional) is the delivery channel; `subject` is the email subject;
`short_body` is a shorter version for SMS or LinkedIn; `channel_post` is the
team or org post for Slack, Teams, or Lark. All of these are safety-checked.
`audience` is `individual` (default), `team`, `org`, or `family`. For a group,
put the group's name in `recipient_name` (e.g. "the Platform team") and leave
`recipient_first_name` out; the optional `roster` list is what
`safety_check.py --roster` checks against.

## Files

- `references/connector-mining.md` — how to search each connector, impact scoring rubric
- `references/quotes.md` — choosing and verifying quotes, starter bank by theme
- `references/language.md` — language detection and bilingual patterns
- `references/art.md` — motif library and SVG rules for the one-of-one artwork
- `references/safety.md` — what never goes in a note, and how to abstract it
- `references/relationships-and-culture.md` — tone by relationship, recipient triggers, cultural norms
- `references/photos.md` — finding, choosing, cleaning, and captioning a photo of a good time together
- `references/team-and-org.md` — `--team` / `--org`: shared achievements, naming everyone or no one, tone by sender's role, group photos
- `references/family.md` — `--family`: forms of address, one picture of a lifetime, family rules, home language
- `references/paying-it-forward.md` — when and how to show the gift travelling on
- `references/fun-facts.md` — the optional P.S. fun fact: rules and a verified fact bank with sources
- `references/sketch.md` — no photo: a drawn pencil sketch, or a freely licensed stock photo as a sketch; honesty rules
- `scripts/sketch_photo.py` — turns a stock photo into a graphite pencil sketch (needs Pillow; strips metadata)
- `references/delivery.md` — choosing the channel, the "Ready to send?" rule, formatting per channel, share links
- `scripts/share.py` — channel-ready text, email subject, and share links (WhatsApp, SMS, email, Telegram, LINE); never sends
- `scripts/card_to_png.py` — saves the card as an image for messaging apps (local headless browser)
- `assets/fonts/` — handwriting fonts embedded in cards: Caveat (Latin, Cyrillic) and Kalam (Devanagari), SIL Open Font License 1.1
- `scripts/safety_check.py` — automated PII / financial / health / harshness scan
- `scripts/render_card.py` — renders note.json + art.svg (+ optional photo, metadata stripped) into a printable HTML card
- `examples/` — a finished sample (note.json, art.svg, rendered card)
