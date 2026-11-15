---
name: welcome
description: Write a warm, specific first-week welcome for a new hire, a new team member, an intern or someone moving onto the team: a personal note from their manager or buddy saying why the team is glad they're here, what their first week looks like and who to ask, plus an optional team-channel introduction (with their OK on what's shared) and a handwritten-style card. Use when someone is joining the user's team or company, starting an internship, or switching teams.
argument-hint: "[new person] [role/team] [start date] [--from manager|buddy|team] [--card]"
---

# Welcome

The first week decides a lot: whether someone feels expected or merely
processed. A short note that shows the team prepared for *them*, and a clear
picture of the week ahead, makes a new person feel at home before their
laptop is even set up.

## Non-negotiables

1. **Specific and true.** Say why the team is glad, using only what's
   appropriate to share: their background as they've shared it (a talk, open
   source work, a project from interviews they'd be happy to have mentioned).
   Nothing from private interview notes, offers or references.
2. **Their OK on the team introduction.** Ask what they'd like shared (a fun
   fact, where they're joining from, pronouns if they offer them) before posting.
3. **Clear and calm.** A first week shouldn't feel like a test: say what's
   expected, what isn't, and that questions are welcome.
4. **Inclusive.** Time zones, remote or hybrid, languages, holidays, dietary
   needs at a team lunch, and accessibility. No assumptions about age,
   family, background or culture.
5. **Send or post only on an explicit yes** (`../thankyou/references/delivery.md`).

## Workflow

### 1. Gather (from the user, and connectors if allowed)

- **Who**: name as they like to be called, role, team, start date, time zone.
- **Why we're glad**: one or two specific, shareable reasons.
- **The first week**: buddy, key meetings, a first small task, the tools,
  where docs live. The onboarding doc or calendar, through connectors.
- **A team tradition**: a welcome lunch, the "first PR" emoji, a team photo wall.
- **From whom**: manager, buddy, the whole team.

### 2. Write

- **Personal note** (`body`, 80–150 words; `references/welcome-patterns.md`):
  welcome and the reason the team is glad, the shape of the first week, the
  buddy and how to reach them, "no question is too small", a warm close.
- **Team introduction** (`channel_post`, 40–80 words), only with what they
  agreed to share.
- **Optional card** (`--card`): a quote, a small sketch (a door with a
  welcome mat, a desk with a plant and a coffee, the city skyline) and the
  team's signatures, rendered with `../thankyou/scripts/render_card.py`.
  It can be printed for their desk on day one or sent as an image.
- **A fun fact P.S.** is welcome here (`../thankyou/references/fun-facts.md`).

### 3. Check and deliver

```bash
python3 ../thankyou/scripts/safety_check.py note.json --profile team
python3 ../thankyou/scripts/share.py note.json --channel slack           # the personal note
python3 ../thankyou/scripts/share.py note.json --channel slack --post    # the team introduction
```

Time it for their first morning, or the Friday before they start (personal
email, with their OK). Send only on the user's yes; with a connector, Claude
can schedule the draft for the user to send.

### 4. Follow up

Offer reminders to the user for day 5 ("How was week one?"), day 30 and day
90 check-ins, and a Kudos note for their first merged PR or finished task.

## Files

- `references/welcome-patterns.md`: notes and introductions that work, a first-week outline, what to avoid
- `examples/kenji-first-week/`: a manager's welcome, a team introduction and a card
