---
name: repair
description: Help the user repair a working relationship after something went wrong, such as a tense meeting, a sharp comment, a missed commitment, a dropped handoff or credit not given, with a sincere apology or follow-up that names what happened, owns it without excuses, acknowledges the effect, says what will change and offers to make it right. Blocks non-apologies ("sorry if you felt…") and suggests when to talk in person instead. Use when the user wants to apologize, smooth things over, or follow up after a difficult interaction at work or at home.
argument-hint: "[person] [what happened] [via in-person|slack|lark|email|text]"
---

# Repair

Every working relationship takes a hit sometimes. What matters is the repair:
quick, specific and without excuses. A good one often leaves trust stronger
than before. This skill helps the user say it well, in a few honest sentences.

## Non-negotiables

1. **Own it.** First person, plainly: "I cut you off in planning, and I'm
   sorry." No "sorry if", "sorry you feel", "mistakes were made", "no
   offense", "to be fair". The `repair` safety profile blocks these.
2. **No excuses, no "but".** Context only if it helps them, and only after
   the apology, never as a defence.
3. **Name the effect on them**, not how bad the user feels.
4. **Say what will change** (`commitment`), and make it right now if possible
   (`make_right`): re-send the review, give credit publicly, fix the handoff.
5. **No pressure to forgive.** They don't have to reply or accept.
6. **Match the channel to the hurt.** In person or on a call for anything
   heated or personal; a message for a small miss or as a follow-up to the
   conversation. If the miss was public (credit not given in a meeting),
   repair it in the same place as well as privately.
7. **Kind to the user too.** One apology, not grovelling. If the user wasn't
   at fault, help with a calm follow-up instead of an apology.
8. **Not for serious misconduct.** Harassment, discrimination or safety
   issues go through the company's process, not an apology note.
9. **Send only on an explicit yes.**

## Workflow

### 1. Understand what happened

- **Who**, the **relationship** and the **channel** they usually use.
- **What happened**, in the user's words, and what the other person likely
  experienced. Ask gently what the user is sorry for, specifically.
- **Is it an apology or a follow-up?** If the user didn't do anything wrong
  (a tense debate both took part in), write a follow-up that resets the tone
  and moves the work forward.

### 2. Write it (`references/repair-patterns.md`)

40–100 words for a message; talking points for a conversation:

1. **What happened**, owned: "In planning today, I cut you off twice while
   you were explaining the migration risks."
2. **The effect**: "That wasn't fair to you, and the team missed points we
   needed to hear."
3. **I'm sorry**, plainly.
4. **What will change** (`commitment`): "In Thursday's review, I'll make sure
   you get the floor first, and I'll hold my questions until you're done."
5. **Make it right** (`make_right`), if possible: "I've added your risk list
   to the top of the planning doc."
6. **An open door, no pressure**: "If you'd like to talk it through, I'm
   around. No need to reply."

### 3. Check and deliver

```bash
python3 ../thankyou/scripts/safety_check.py note.json --profile repair
python3 ../thankyou/scripts/share.py note.json --channel slack
```

Send only on the user's yes; for in-person repairs, give the talking points.
Offer a reminder for the user to follow through on the commitment (for
example, before Thursday's review). Keeping it is the real apology.

## Files

- `references/repair-patterns.md`: apologies and follow-ups by situation, what to avoid
- `examples/ravi-planning-meeting/`: after cutting a colleague off in a planning meeting
