---
name: reconnect
description: Find people the user has drifted away from (old teammates, friends, mentors, family) and draft a short, warm, no-guilt check-in built on a real shared memory, fitted to the relationship, culture, and language. Use when the user wants to reconnect, catch up, or keep in touch with someone, or asks who they've lost touch with.
---

# Reconnect

Most relationships don't end; they drift. The hardest part of reaching back out
is the first message: it feels awkward, so it never gets sent. This skill
finds people worth reconnecting with and writes a first message that is easy
to send and easy to answer — anchored in a real shared memory, never in guilt.

## Non-negotiables

1. **No guilt, no time-counting.** Never "it's been forever", "sorry I
   disappeared", "I'm terrible at keeping in touch", or "3 years!". Start from
   warmth, not from the gap.
2. **No agenda hiding.** The message is about the person. If the user actually
   needs something (a referral, advice, a favour), say so: suggest reconnecting
   first and asking later, or write an honest message that names the ask
   lightly. Never disguise an ask as a catch-up.
3. **Not creepy.** Use only what the two of them shared, or what the person
   posted publicly *for their network to see* (a new role, a talk). Never
   mention location, check-ins, family details, or anything that sounds like
   monitoring ("I saw on your profile you moved…").
4. **No sensitive data.** No PII, financial, or health details in the message.
   Same rules as ThankYou (`../thankyou/references/safety.md`).
5. **Read-only. Never send.** Draft only. Creating a draft in the user's email
   or chat is fine when asked; sending needs their explicit go-ahead.
6. **Private channels are opt-in.** WhatsApp, SMS/iMessage are read only after
   the user explicitly allows it, for this task, 1:1 threads only.
7. **Some drift is a choice — respect it.** Never suggest someone the user
   distanced themselves from on purpose, someone who asked for space, an ex,
   a conflict, or someone who may have passed away (see `references/drift-detection.md`).
   When in doubt, leave them off the list.
8. **Kind, always.** Relationship-aware tone, recipient triggers avoided,
   cultural norms respected (`../thankyou/references/relationships-and-culture.md`).

## Two modes

- **Named person** — "Help me reconnect with Arjun." Skip to step 3.
- **Discovery** — "Who have I lost touch with?" / "Help me reconnect with a
  few old friends this month." Start at step 1.

## Workflow

### 1. Find drifted connections (discovery mode)

Follow `references/drift-detection.md`. In short:
- Use connected email, chat, LinkedIn, calendar (WhatsApp/SMS only with
  permission). Look for people with a **warm past** (real two-way exchanges,
  gratitude, shared projects, personal notes) and a **quiet present**
  (little or no exchange for 6+ months).
- Exclude: newsletters, vendors, recruiters, transactional contacts, large-group
  only contacts, and anyone matching the "leave alone" signals.
- Score by warmth, depth, how mutual it was, and how natural a hook exists.

Present 3–5 people as one line each — no message quotes, no sensitive detail:
> 1. **Arjun** — teammate on the 2019 launch; you two did the Friday chai runs. Last real exchange early 2025.
> 2. **Mei** — former colleague; she mentored you through your first team-lead year.

Let the user pick, remove, or add. Ask once, gently: "Anyone here you'd rather
not reach out to?" — no explanation needed.

### 2. Confirm relationship and context

For each chosen person, know (or ask, briefly):
- the relationship (friend, old teammate, mentor, cousin, college roommate…),
- anything tender for them right now (steer around it silently),
- language and culture cues (from how they wrote to each other),
- whether the user has an ask (see non-negotiable 2),
- the channel: email, LinkedIn, WhatsApp, SMS, Slack.

### 3. Find the hook

Follow `references/hooks.md`. Pick **one** hook, in this order of preference:
1. **Shared memory** — a specific moment from their history ("the night we got
   the demo working at 2am", "your terrible-but-legendary trivia team name").
2. **"Thought of you" trigger** — something real in the user's life that
   reminded them of the person ("I just used the review checklist you taught me").
   Must be true — ask the user if you don't have one.
3. **Their public milestone** — something they shared with their network
   (new role, a talk, a launch). Congratulate; don't analyse.
4. **Season or festival** — Diwali, Lunar New Year, Eid, Thanksgiving, New Year;
   only one they celebrate. Natural low-pressure opener in many cultures.
5. **Genuine question** — something only they would know or would enjoy answering.

Never invent a memory or a trigger. If nothing real exists, use 4 or 5.

### 4. Write the message

Short — this is a door-opener, not a letter.
- Chat / WhatsApp / SMS: 25–60 words. Email / LinkedIn: 50–100 words.

Shape:
1. **Greeting** in the form they used with each other (nickname, "Hey", "Namaste Mei-ji"…).
2. **Hook** — one or two sentences, specific.
3. **Warm line about them** — what you appreciated or remember about them.
4. **Easy door** — one light, easy-to-answer question, or a soft invitation
   ("would love to hear what you're building these days"). No pressure to reply
   at length; optionally say so ("no need for a long reply").
5. **Sign-off** in their usual style.

Language: the language they used with each other; bilingual touch for mixed
relationships (greeting or festival wish in the native language). Follow
`../thankyou/references/language.md`.

Offer **two variants** when it helps: one lighter, one warmer. Keep the user's
voice — if they share past messages to the person, match that register.

Optional: a tiny "postcard" image from the shared memory (art rules in
`../thankyou/references/art.md`), useful for WhatsApp or a holiday note.

### 5. Safety pass

```bash
python3 ../thankyou/scripts/safety_check.py message.json --profile reconnect
```

The `reconnect` profile adds checks for guilt and time-counting phrases,
surveillance-sounding phrases, and hidden asks. Fix all blocking flags; review
the rest. Then re-read: *Would this be a pleasant surprise to receive? Easy to
answer? Nothing that feels like pressure, guilt, or being watched?*

### 6. Deliver

For each person: the message (ready to paste), one line on why this hook, and
the variant if any. Offer to create drafts in the right connector. Never send.

Optional follow-through, only if the user wants it: offer a monthly scheduled
task ("each month, suggest two people to reconnect with and draft the notes")
— it drafts only, never sends.

## message.json format

Same schema as ThankYou (quote optional):

```json
{
  "recipient_first_name": "Arjun",
  "sender_first_name": "Hardik",
  "relationship": "former teammate",
  "channel": "whatsapp",
  "language": "en",
  "greeting": "Hey Arjun,",
  "body": ["…"],
  "closing": "",
  "signature": "Hardik"
}
```

## Files

- `references/drift-detection.md` — finding drifted connections, exclusions, scoring
- `references/hooks.md` — hook types, examples, what feels creepy or guilt-inducing
- `examples/` — sample suggestion list and messages
- Shared with ThankYou: `../thankyou/references/{safety,language,art,relationships-and-culture}.md`,
  `../thankyou/scripts/{safety_check,render_card}.py`
