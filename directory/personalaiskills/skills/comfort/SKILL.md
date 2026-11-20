---
name: comfort
description: Write a short, steady, kind message to someone going through a hard time (a loss, an illness, a layoff, a breakup, a hard anniversary) that acknowledges it without fixing or minimising, offers one specific kind of help, can include a gentle thought about something warm to eat, and, only when the user says it's welcome, a link to a comedy scene to lighten the mood. Fits the relationship, culture and language; sends only on an explicit yes. Use when the user wants to reach out to someone who is grieving, ill, or struggling.
argument-hint: "[person] [what happened] [via whatsapp|email|sms|card|...]"
---

# Comfort

When someone is hurting, most people freeze, or send something that stings
without meaning to ("everything happens for a reason", "at least…"). This
skill helps the user send a short, steady message that says: I see you, I'm
here, and here is one real thing I can do.

## Non-negotiables

1. **Acknowledge, don't fix.** No silver linings, no "at least", no "everything
   happens for a reason", no "they're in a better place" (unless the family's
   own faith uses those words and the user asks), no advice, no "stay strong".
2. **About them, not the sender.** No "I know exactly how you feel" and no
   stories about the sender's own loss, unless the user wants one short line of
   solidarity and they know the person would welcome it.
3. **Specific beats vague.** Replace "let me know if you need anything" with one
   concrete, easy-to-accept offer: "I'm dropping dinner off Thursday, no need to
   answer the door"; "I can take the kids Saturday morning"; "I'll cover your
   Monday stand-up".
4. **No pressure to reply.** Say it: "No need to reply."
5. **Private stays private.** Never name a diagnosis, cause of death, the
   reason for a layoff, or details the person hasn't shared widely. No PII,
   money or health details (`../thankyou/references/safety.md`).
6. **No medical, legal or financial advice**, ever.
7. **Humour only when welcome.** A light moment (a sitcom scene) is added only
   if the user confirms the person would enjoy it, and never for a fresh loss,
   a serious diagnosis, pregnancy loss, or anything traumatic
   (`../thankyou/references/light-moments.md`). No fun facts.
8. **Respect their culture and faith.** Mourning customs, words and food
   differ; follow theirs, not the sender's (`references/customs.md`,
   `../thankyou/references/relationships-and-culture.md`).
9. **Send only on an explicit yes.** Follow-ups are reminders *to the user*,
   never automatic messages (`../thankyou/references/delivery.md`).

## Workflow

### 1. Understand what happened (gently, briefly)

- **Who** and the **relationship** (colleague, friend, neighbour, family, a
  former manager…).
- **What happened**, in the words the user is comfortable with: a loss (whose?
  a parent, a partner, a pet), an illness or surgery (theirs or a loved one's),
  a layoff, a breakup or divorce, a pregnancy loss, a hard anniversary, a
  disaster such as a fire or flood.
- **How recent**: today, this week, months ago, an anniversary.
- **What the person has shared publicly**, so the message never reveals more.
- **Their language, culture and faith**, if relevant and known.
- **The channel**: text, WhatsApp, email, a card, a handwritten note with food.

### 2. Choose the shape (`references/what-to-say.md`)

Short beats long. A text is 25–60 words; a card or email is 60–120.

1. **Greeting** in the way they're usually addressed.
2. **Acknowledge plainly**: "I just heard about your dad, and I'm so sorry."
   For a layoff: "I heard about the changes at work. That's a hard thing to get
   hit with."
3. **One true, warm memory or quality**, when there is one:
   - for a loss: a memory of the person who died ("I'll always remember how he
     cheered loudest at your graduation")
   - for other hard times: something about them ("You're one of the most
     generous people I've worked with")
4. **One specific offer of help**, sized to the relationship.
5. **A food thought** (optional, `references/comfort-food.md`): a gentle,
   culturally fitting idea, usually something the sender will *bring* rather
   than something the person should *eat*: "I'm making a pot of dal on Thursday
   and I'll leave some at your door," or, from afar, "If cooking feels like too
   much this week, a bowl of something warm counts as dinner."
6. **No need to reply.**
7. **Close** with warmth: "Thinking of you," / "Holding you all close," /
   "With love,", or the words that fit their faith and culture.
8. **A light moment** (optional, only when welcome): "For a smile, whenever
   you want one:" with a link to an official clip or a public-domain short.

### 3. Language and culture

Write in the language the person grieves in when the user can share it; a
native-language condolence phrase can mean a great deal ("Om Shanti"; "Que en
paz descanse"; "节哀顺变"; "إنا لله وإنا إليه راجعون" for Muslim families).
Only use a religious phrase that belongs to *their* faith, and only when the
user confirms it fits (`references/customs.md`).

### 4. A small sketch (optional, for cards)

A gentle pencil sketch can sit at the top of a card: a lit candle by a window,
a cup of tea, a single flower, a lantern, an open door with warm light. Follow
`../thankyou/references/sketch.md`, with soft greys and one warm accent. Avoid
any imagery tied to the loss itself. A user's own photo of the person who
died goes in only if the family would want it and the user chooses it.

### 5. Safety pass

Go through `../thankyou/references/safety-checklist.md`, including the Comfort
messages section, which blocks minimising phrases, "I know how you feel",
advice and pressure, vague "let me know if you need anything", and fun facts;
it flags any humour for a second look. Then re-read it slowly, as the person
would on their worst day.

### 6. Deliver, and remember to follow up

Build the card and deliver as in ThankYou (`../thankyou/references/card-layout.md`,
then `../thankyou/references/channel-formats.md` or a connector draft), and send only on an explicit yes.

Support often fades after the first week. Offer, once, to remind the
**user** (not message the person) at a gentle moment: two or three weeks
later, a month later, or before a hard date such as a birthday, an anniversary,
the first holidays, or the end of a mourning period. Use a scheduled reminder
that drafts a short check-in for the user to review. It never sends on its own.

## note.json

Same format as ThankYou, plus:

```json
{
  "situation": "loss | illness | layoff | breakup | pregnancy-loss | anniversary | disaster | other",
  "offer": "the one specific help, as written in the body",
  "light_moment": {"title": "…", "url": "…", "source": "official channel or public domain"}
}
```

## Files

- `references/what-to-say.md`: words that help and words that hurt, by situation
- `references/comfort-food.md`: food thoughts that fit (and when not to mention food)
- `references/customs.md`: mourning customs and phrases to check before using
- `examples/`: a sympathy card for a colleague's loss, and a message to a friend after a layoff
- Shared with ThankYou: `../thankyou/references/{light-moments,sketch,safety,safety-checklist,language,relationships-and-culture,delivery,card-layout,channel-formats,images}.md`
