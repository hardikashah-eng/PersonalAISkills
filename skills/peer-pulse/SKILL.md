---
name: peer-pulse
description: Run a lightweight weekly peer-recognition pulse for a team, two questions ("Who helped you this week? How did it help?") sent privately in Slack, Lark, Teams, email or WhatsApp, then turn the answers into thank-you drafts for the people named, quoting peers only as they allowed (named, anonymous or just for the organizer), and into evidence for Spotlight and Team Story. Personal or sensitive answers are held for the organizer and never stored. Use when a leader wants peers to recognize each other, find the help managers miss, or start a weekly appreciation ritual.
argument-hint: "[team] [prompt|tally <answers>] [--due 'Friday 4 pm'] [--channel slack|lark|teams|email|whatsapp]"
---

# Peer Pulse

Managers see a fraction of the help that happens on a team. Peers see the
rest: the quick answer that saved an afternoon, the pairing session, the
review that taught something. Two questions a week bring it to the surface,
and the people who help get thanked by name in their peers' own words.

## Non-negotiables

1. **Voluntary and light.** Two questions, one minute, no reminders beyond
   one. Nobody is chased for not answering.
2. **Private replies.** Answers go to the organizer (a DM, a form), not a
   public thread, so nobody feels left out in public.
3. **The writer decides how they're quoted:** `yes` (name me), `anonymous`
   ("a teammate"), or `private` (just for the organizer; no thank-you drafted).
4. **No counting or ranking.** The tally is for thanking people, never a
   scoreboard. "Not mentioned this week" is private, for awareness, and often
   just a quiet week.
5. **Personal stays personal.** Answers about health, family or personal
   matters are held for the organizer to read in the original; no draft is
   made and nothing is stored.
6. **Send only on an explicit yes.** The organizer reviews every draft.

## Workflow

### 1. Post the prompt (Friday)

```bash
python3 scripts/pulse.py prompt --team "Platform" --due "Friday 4 pm" --channel slack
```

The organizer posts it in the team channel (asking for replies by DM), or
sends it as a short form (Google Forms, Microsoft Forms, a Lark form). With a
connector, Claude can draft the post or schedule it, for the user to approve.

### 2. Collect the answers

From DMs (with a connector, only the replies to the prompt), a form export
(CSV), or pasted in. Columns: `date, from, helped, how, share`.

### 3. Tally

```bash
python3 scripts/pulse.py tally answers.csv --team "Bea,Chen,Dami,Ola,Kenji,Arjun" \
  --organizer "Hardik" --drafts drafts/ --evidence evidence.jsonl
```

- A private summary for the organizer: who was thanked, for what, and by whom (as allowed)
- One Kudos draft per person thanked (`drafts/kudos-<name>.json`), quoting peers as they allowed.
  Polish each with the Kudos skill if needed, and include people on other teams
- Lines added to Spotlight's `evidence.jsonl` (private answers stored without their text)
- Answers held because they touch on personal matters

### 4. Thank people, and close the loop

Review the drafts, then send each as a DM on an explicit yes. Optionally, a
short team post: "This week, people thanked each other for: pairing on the
scheduler, unblocking the eu rollout, a flaky test fixed…" (no names unless
they agreed). Feed the month's answers into Team Story, and the quarter's
into Spotlight.

## Automate it

The Routines skill can draft the Friday prompt and, on Monday, the tally and
thank-you drafts for the organizer to review (`../routines/SKILL.md`).

## Files

- `scripts/pulse.py`: the prompt (by channel) and the tally (drafts, evidence, held answers)
- `references/running-it.md`: getting started, keeping it light, what to do with what you learn
- `examples/week-46/`: six answers, the tally and four thank-you drafts
