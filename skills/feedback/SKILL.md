---
name: feedback
description: Help an engineer or leader give constructive feedback that is specific, kind and actionable, shaped as what happened, what it affected, and what to try next, starting from what's going well. Prepares talking points for a 1:1 and an optional written follow-up, checks the wording for labels, absolutes and coded language, and, once it's been shared, adds it to the user's private growth log of improvement opportunities with a follow-up date. Works for feedback to a direct report, a peer or a manager. Use when the user wants to give, write or prepare feedback, or track someone's growth areas.
argument-hint: "[person] [what happened] [--report|--peer|--upward] [--log <file>]"
---

# Feedback

Most people put off hard feedback until it's too late, then deliver it too
vaguely to act on ("be more strategic"). This skill turns what the user saw
into a short, clear conversation: what happened, what it affected, what to try
next, and then keeps track of it, so growth gets noticed and followed up.

## Non-negotiables

1. **Behaviour, not character.** Describe what was seen or heard, never a
   label ("careless", "not a team player", "bad attitude"). No "you always" or
   "you never". No comparisons with colleagues.
2. **Specific and recent.** One or two concrete examples from the last few
   weeks, not a list of grievances.
3. **Kind and direct.** Start with something real that's going well. Say the
   point clearly; don't bury it in softeners.
4. **Spoken first.** Feedback is a conversation, ideally in a 1:1. A written
   note is a follow-up or for remote teams, never a surprise in a channel.
   Never post constructive feedback publicly.
5. **Nothing personal or protected.** No health, family, age, appearance,
   accent, religion, or anything about leave. If an issue may involve health,
   wellbeing or a legal matter, stop and suggest HR or the right support
   instead (`references/when-not-to.md`).
6. **The log holds only what the person has heard.** An improvement
   opportunity is logged once it's been shared with them, with what's going
   well alongside. No secret files.

## Workflow

### 1. Gather

Ask the user (briefly):

- **Who**, and the **relationship**: direct report, peer, their manager (upward),
  someone on another team.
- **What happened**: one or two specific moments, with when and where.
- **What it affected**: the team, a customer, a deadline, how others felt or worked.
- **What they'd like instead**: the change, or an open question if they're not sure.
- **What's going well**, honestly. If the user says "nothing", help them find
  one true thing, or keep the conversation to the one issue.

With connectors, Claude can look at the specific item the user names (the
design doc, the PR thread, the meeting notes) to get the facts right. It
doesn't search someone's history for problems.

### 2. Shape it (`references/feedback-model.md`)

Fill `feedback` in `note.json`:

```json
"feedback": {
  "strength": "what's going well, specifically",
  "observation": "what happened: specific, recent, observable",
  "impact": "what it affected",
  "next": "what to try next (a request or an open question)",
  "area": "communication",
  "follow_up": "2026-12-05"
}
```

Then write:

- **Talking points** (`talking_points`): 4–6 short lines for the 1:1, in
  order: what's going well → what happened → what it affected → ask for their
  view and listen → agree what to try → when to check in.
- **A written follow-up** (`body`), optional: 60–120 words, sent after the
  conversation to confirm what was agreed, never instead of it.

Upward and peer feedback: ask permission first ("Can I share an observation
about Tuesday's review?"), keep to how it affected you or the work, and offer
help. See `references/feedback-model.md` for examples.

### 3. Check it

```bash
python3 ../thankyou/scripts/safety_check.py note.json --profile feedback
```

The `feedback` profile blocks labels, absolutes and comparisons, flags coded
or vague words ("abrasive", "emotional", "executive presence", "culture fit")
and missing parts (observation, impact, next).

### 4. Deliver

The conversation happens in person or on a call. For the written follow-up,
use `../thankyou/scripts/share.py note.json --channel email` (or Slack, Lark,
Teams as a direct message), and send only on the user's explicit yes.

### 5. Add it to improvement opportunities (automatic once shared)

When the user confirms the conversation happened (or approves sending the
written follow-up), add it to their growth log, with no extra step:

```bash
python3 scripts/growth_log.py add --log <their log file> --person Dami --type growth --area communication \
  --observation "…" --impact "…" --next "…" --source feedback --shared --follow-up 2026-12-05
```

- The log is a file the user keeps (a private folder, or exported to a
  private Google Sheet, Lark Base table, Notion database or Excel with
  `growth_log.py export --csv`). If the user prefers a connected tool, Claude
  adds the same fields as a row there instead (`references/growth-log.md`).
- Kudos adds **strengths** to the same log, so the picture stays balanced.
- `growth_log.py due` lists follow-ups coming up; the daily nudge surfaces them.
- When progress is seen, update it (`update --status done --note "…"`) and say
  so to the person. That closing of the loop is the point of the log.
- `growth_log.py summary --person Dami` prints both strengths and growth areas
  for a 1:1 or review.

## Files

- `references/feedback-model.md`: the model, examples (report, peer, upward), wording that helps
- `references/growth-log.md`: what's logged, where it can live, privacy and fairness rules
- `references/when-not-to.md`: when to involve HR or other support instead
- `scripts/growth_log.py`: the private log of strengths and improvement opportunities
- `examples/dami-design-reviews/`: talking points, a written follow-up and the log entry
