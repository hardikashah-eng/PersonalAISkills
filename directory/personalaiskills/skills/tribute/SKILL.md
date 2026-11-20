---
name: tribute
description: Gather short messages from a group (a team, a class, a family, a club) and weave them into one tribute card for someone being celebrated or seen off, such as a retirement, a farewell, a milestone birthday, a promotion or a big anniversary, with everyone credited, a group photo or pencil sketch, an opening quote, and optionally a link to a favourite comedy scene or a public-domain short film for a smile. Writes the request to contributors, checks every message for kindness and privacy, and sends only on an explicit yes. Use when the user is organizing a group card, farewell message, retirement tribute or birthday wall.
argument-hint: "[honoree] [occasion: farewell|retirement|birthday|promotion|anniversary|memorial] [--team|--family|--class]"
---

# Tribute

A group card is often a scramble of "Good luck!!" and "We'll miss you!" signed
in a hurry. This skill helps the organizer ask the right question, collect
real, specific messages, and turn them into one beautiful card that the
honoree will keep.

## Non-negotiables

1. **Everyone's words are their own.** Light edits for spelling and length
   only, and only with permission for anything more. Every message is credited
   to the person who wrote it (or "Anonymous" if they ask).
2. **Contributors opt in.** Nobody's name appears unless they contributed or
   agreed. No guessing what someone "would have said".
3. **Kind, inclusive and safe.** No inside jokes that embarrass or exclude, no
   jokes about age, looks, health, weight, money or personal life, no
   backhanded compliments, no private details (`../thankyou/references/safety.md`).
   Every message goes through the safety check; flagged ones go back to the
   organizer, not straight into the card.
4. **Name everyone or no one** in group greetings (the roster check), as in ThankYou
   team mode.
5. **A memorial tribute is different.** For someone who has died, follow
   Comfort's rules: no humour unless the family asks, their customs and
   words (`../comfort/SKILL.md`).
6. **Send only on an explicit yes** (`../thankyou/references/delivery.md`).

## Workflow

### 1. Set it up with the organizer

- **The honoree**, the **occasion**, the **group** (team, class, family, club)
  and the **deadline**.
- **The relationship** between the group and the honoree (manager, teacher,
  coach, grandparent), so the tone fits (`../thankyou/references/relationships-and-culture.md`).
- **Where messages come from**: replies to a message in the team's Slack,
  Teams, WhatsApp or email thread; a shared form; or the organizer pastes them
  in. With a connector, Claude can read replies in a thread the organizer
  points to; it never reads anything else.
- **The language(s)**: contributors may write in their own; keep each message
  as written, with a translation underneath if the honoree needs one.

### 2. Ask contributors (`references/collecting.md`)

Draft the request for the organizer to send. A good prompt gets specific
stories instead of "Good luck!":

> We're making a card for Meena's farewell (her last day is Friday 21 Nov).
> In 1–3 sentences: one moment with Meena you remember, and what difference
> she made for you. Reply here by Wednesday. Keep it kind and something she'd
> be happy for everyone to read.

### 3. Collect and check

Gather each message as `{"subject": "Contributor name", "why": "their message"}`
in `items`. Check every message with `../thankyou/references/safety-checklist.md`
(the every-note checks plus the team section), and check the card against the
full roster of contributors (Arjun, Bea, Chen, Dami…): if anyone is named, everyone is.

Flagged messages go back to the organizer with a suggested gentler version for
the contributor to approve. Never silently rewrite someone's message.

### 4. Shape the card

1. **Opening quote** that fits the honoree and occasion (verified; see
   `../thankyou/references/quotes.md`).
2. **Title**: "Thank you, Meena" / "Happy 80th, Dada" / "Congratulations, Coach".
3. **Organizer's intro**, 2–3 sentences: what this group shared with the
   honoree, in the group's voice.
4. **The messages**, each credited, with a hand-drawn mark (no numbers). Order
   for flow: a strong one first, a funny one in the middle, the most moving one
   last.
5. **A group photo** (the group's own, metadata removed) or a **pencil sketch** of a
   meaningful scene (`../thankyou/references/sketch.md`).
6. **A light moment** (optional): a link to the honoree's favourite comedy
   scene on an official channel, or a public-domain silent short
   (`../thankyou/references/light-moments.md`). Not for memorial tributes
   unless the family asks.
7. **Closing and signature**: "With love and gratitude, the Platform team".
8. **P.S. fun fact** (optional, `../thankyou/references/fun-facts.md`).

### 5. Render and deliver

Build `card.html` from `note.json`, `art.svg` and the group photo
(`../thankyou/references/card-layout.md`), make `card.png` for chat
(`../thankyou/references/images.md`), and prepare the Slack or other channel
text (`../thankyou/references/channel-formats.md`).

Show the organizer the finished card ("Ready to send?") and send only on an
explicit yes. For a big group, a team-channel post (`channel_post`) with the
card image, plus a direct message to the honoree, works well.

## note.json

Same format as ThankYou (`../thankyou/SKILL.md`), with `items` holding the
contributions (`subject` = contributor, `why` = message, optional
`translation` appended to `why`), `roster` listing contributors, and optional
`light_moment`.

## Files

- `references/collecting.md`: the request to contributors, reminders, handling late or tricky messages
- `examples/meena-farewell/`: a team farewell card with five contributions and a public-domain film link
- Shared with ThankYou: its references, including `card-layout.md`, `channel-formats.md`, `images.md` and `safety-checklist.md`
