# Automating PersonalAISkills

The skills save the most time when the moments come to you: after a meeting,
every morning, at the end of the week, and before an occasion. Automation here
means **Claude prepares; you approve**. A scheduled run finds the moments,
drafts the messages with the right skill, runs the safety checks, and sends
you one "ready to review" note. Nothing goes to anyone else until you say yes.

## What can be automated

| Skill | Trigger | What's prepared | What needs your yes |
|---|---|---|---|
| Kudos | PR merged, incident resolved, on-call shift ended, praise in a meeting | a DM, a #kudos post, a manager note; a LinkedIn draft only for public work | sending or posting each one; logging the strength |
| Feedback | a possible feedback moment in a meeting; a growth-log follow-up date | private talking points for your 1:1 | the conversation; then adding it to the growth log |
| Intro | someone asks "who knows X?", a new hire's first week | the two private asks | each ask; the intro only after both say yes |
| Welcome | a start date on the calendar | the personal note, the team post, a card | each message, timed for their first morning |
| Repair | a commitment you missed (from your own meeting notes or task list) | a short owned follow-up | sending it |
| Nudge | every morning; after a recurring meeting; Friday | the review list | each item on it |
| ThankYou, Grateful | an occasion (Thanksgiving, Diwali, year-end), a work anniversary | notes and cards for the people on your list | each note (see the roadmap for reviewed batches) |
| Reconnect | monthly | two or three check-ins with drifted contacts | each one |
| Comfort | never automatically | — | Comfort only starts when you ask |

## Three ways to run it

### 1. Scheduled routines (recommended)

Say "set up my routines" (or accept the offer after a kudos or feedback
session). The [Routines skill](skills/routines/SKILL.md) asks a few questions
(which routines, times and time zone, your team, connected sources, where
approved messages go, where your growth log lives), shows you the plan, and
creates each one with your app's scheduling tool only after you say yes. Its
`make_routines.py` writes complete prompts, with the approval and privacy
rules built in, because each scheduled run starts fresh.

You can also change, pause or remove them the same way: "move the Friday
sweep to Thursday", "pause the daily brief while I'm on vacation".

The prompts below are simplified versions, if you'd rather set one up by hand.

**Daily people brief (weekdays, 8:40 a.m.)**
> Run the nudge skill from PersonalAISkills in daily mode. Use my connected
> GitHub, calendar, incident tool and growth log. Find at most five moments
> from the last working day worth acting on: specific work to recognize,
> growth-log follow-ups due, first days and work anniversaries, people I
> haven't recognized in 30 days. Draft each with the right skill, run the
> safety check, and send me one review list. Don't send anything to anyone else.

**After standup (weekdays, 30 minutes after it ends)**
> Run the nudge skill in after-meeting mode on today's standup transcript from
> my meeting tool. I'm "Hardik" in the transcript; the team is Bea, Chen,
> Dami, Ola and Arjun. Draft Kudos for recognition moments and wins (read the
> PR or doc first), list possible feedback moments only for me, and remind me
> of my own commitments. Send me the review list only.

**Friday recognition sweep (Fridays, 3:10 p.m.)**
> Run the nudge skill in weekly mode: the week's merged PRs, resolved
> incidents and on-call shifts for my team, open growth-log follow-ups for
> next week, and commitments still open. Draft Kudos where it's deserved,
> fairly spread across the team. Send me the review list only.

**Before an occasion (one week ahead)**
> It's a week before Thanksgiving. Using ThankYou and Grateful, prepare notes
> for the people on my list, each grounded in a real moment from my connected
> sources. Send me the review list only.

### 2. On demand, in one line

- "After standup" (with the transcript attached or in your meeting tool)
- "Thank Bea for #482, and post it in #kudos"
- "Welcome Kenji, starting Monday"
- "What follow-ups are due this week?"

### 3. From your tools (for teams that want it)

Teams can start the same flow from their own systems, for example a CI job on
PR merge that asks Claude (through Claude Code or the API) to run Kudos and
put the draft in the owner's review list. The rules don't change: drafts go
to a person to approve, never straight to the recipient.

## Approving a review list

- Each item shows the recipient, the channel, the full text, and the safety
  check result.
- Reply "send 1 and 3", "edit 2: …", "skip the rest", or "send all".
  Approving a list you've read counts as your yes for the items you choose.
- Items are sent one at a time through each recipient's channel (a connector
  draft or post, or a share link), and you get a result for each.
- Items with an unresolved safety flag are never in a "send all".

## What never happens

- Sending, posting or logging on a schedule without your approval.
- Public posts (LinkedIn) without the person's OK and the public safety check.
- Constructive feedback sent from a nudge, or logged before you've talked.
- Reading emotions, health or personal matters from meetings or messages.
- Storing your messages, transcripts or contacts, including in memory.
