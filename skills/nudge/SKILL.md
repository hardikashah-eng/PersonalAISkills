---
name: nudge
description: A short daily or after-meeting list of people moments worth acting on, each with a ready draft for the user to approve. Reads the user's connected sources (merged PRs, resolved incidents, meeting transcripts, calendar, growth-log follow-ups, drifted contacts) and suggests kudos, private feedback notes, follow-ups on commitments, welcomes, check-ins and reconnections. After a meeting with a transcript, it finds praise, wins, possible feedback and commitments. Never sends anything without the user's approval. Use for "what should I follow up on", "anyone I should thank", "after standup", or a daily people brief.
argument-hint: "[daily|after-meeting <transcript or meeting>|weekly] [--max 5]"
---

# Nudge

Good intentions to thank, follow up or check in are easy to lose in a busy
day. This skill finds the moments, drafts the message with the right skill,
and puts a short list in front of the user to approve, edit or skip. It is the
automation hub for the other skills (`../../AUTOMATION.md`).

## Non-negotiables

1. **The user approves every message.** Drafts only; nothing is sent, posted
   or logged about a person without the user's explicit yes to that item.
   Approving a reviewed list counts as yes for the items checked.
2. **Feedback stays private.** Possible feedback moments are shown only to
   the user, as prompts to check the facts. They are never sent to the person
   from a nudge and never logged until the user has talked with them.
3. **No mood reading.** Don't infer emotions, stress or sentiment about a
   person from tone, wording or voice. Only what was said: "thanks to Chen",
   "we're waiting on Arjun".
4. **Personal matters are skipped.** Lines about health, family, leave or
   personal life are not analysed or surfaced.
5. **Only meetings the user may use.** Transcripts of meetings the user
   organized or attended, where recording or transcription was announced and
   the company allows this use. Never HR, medical or legal meetings, or 1:1s
   the other person didn't know were transcribed.
6. **Few and fair.** At most five nudges a day (`--max`). Rotate who gets
   recognized, and flag people who haven't been for a while.

## Modes

### After a meeting (`after-meeting`)

1. Get the transcript: from Zoom, Microsoft Teams, Google Meet (Docs),
   Lark/Feishu Minutes, Otter or similar through the user's connectors, or a
   file the user shares (VTT, SRT or "Name: text").
2. Scan it:
   ```bash
   python3 scripts/scan_transcript.py standup.vtt --me "Hardik" --people "Bea,Chen,Dami,Ola,Arjun"
   ```
   It lists **recognition moments** (someone thanked or credited a colleague),
   **wins** people reported, **possible feedback moments** (for the user only)
   and **commitments** (who said they'd do what, and when).
3. Read the work behind each moment (the PR, doc or ticket) before drafting.
4. Draft with the right skill: Kudos for recognition and wins
   (`../kudos/SKILL.md`), a private note for the user's 1:1 for feedback
   (`../feedback/SKILL.md`), a reminder for the user's own commitments, and
   Repair if the user wants to follow up on a tense moment.
5. Run each draft through the safety check, and present a review list
   (`examples/standup-2026-11-16/review.md`).
6. On approval: send each item through its channel (connector or copy),
   one at a time, and report what happened ("sent", "draft created", "skipped").
   Log strengths only for kudos the user sent and asked to log.

### Daily (`daily`)

A morning list of three to five items, from whatever the user has connected:

| Source | Nudge |
|---|---|
| GitHub/GitLab: PRs merged, reviews given | Kudos for specific work |
| PagerDuty, Jira, incident channels: resolved incidents, finished on-call | Kudos for calm, careful handling |
| Yesterday's meeting transcripts | Recognition moments, commitments due |
| Growth log (`../feedback/scripts/growth_log.py due`) | Feedback follow-ups and progress to notice |
| Calendar or HR calendar the user shares | First days (Welcome), work anniversaries (ThankYou), returns from leave (a simple "welcome back", no questions) |
| Growth log (`growth_log.py gaps --team … --days 30`) | People not recognized lately, and recognition spread across locations or roles |
| Email, chat history | Drifted contacts (Reconnect), unanswered intros (Intro) |

Each item has a one-line reason and a ready draft.

### Weekly (`weekly`)

Friday: a recognition sweep of the week's merged work and incidents, open
growth follow-ups for the coming week, and commitments still open.

## Scheduling

The Routines skill (`../routines/SKILL.md`) sets these up: it asks a few
questions, shows the plan, generates standalone prompts with
`make_routines.py`, and creates the scheduled tasks only after the user says
yes. Offer it once, after a nudge list that helped.

A scheduled run prepares the list and sends the user a short "ready to
review" message; it never sends drafts to anyone else.

## Files

- `scripts/scan_transcript.py`: find recognition, wins, possible feedback and commitments in a transcript (local, read-only)
- `references/sources.md`: what each source gives, and the privacy rules for each
- `examples/standup-2026-11-16/`: a transcript, the scan, two Kudos drafts and the review list
