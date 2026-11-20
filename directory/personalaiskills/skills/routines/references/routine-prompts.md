# Routine prompts and schedules

Build each routine from the user's answers (`routines.json`, as in
`examples/team-lead/routines.json`). A scheduled run starts fresh, with no memory
of this conversation, so each prompt carries everything it needs.

## The schedule

- A 5-field cron expression in the user's time zone, written as
  `CRON_TZ=<time zone> <minute> <hour> <day of month> <month> <day of week>`.
- Days: `weekdays` (1-5), `daily` (*), day names such as `fri` or `fri,mon`
  (Sunday is 0), `monthly <day>` (that day of every month), or `quarterly <day>`
  (that day of January, April, July and October). Monthly and quarterly runs
  pin the day of the month and leave the day of the week as *.
- Times like 8:40, 16:10 or 4:10pm. A time exactly on :00 or :30 moves a few
  minutes earlier (by the length of the routine's name modulo 29, plus 1), so
  runs aren't queued behind everyone else's.
- A routine that reads a growth log kept as a file on the user's computer
  (the daily brief, Monday follow-ups, quarterly Spotlight) must run on that computer.

## The plan to show the user

```text
<N> routine(s) for <name> (<time zone>):

• <routine name>: <what it does>
  <days> at <HH:MM>  [<cron>]  (runs on your computer: the growth log is a local file)

Each run prepares drafts and sends you one review list. Nothing is sent without your yes.
```

## Each prompt

Every prompt is four paragraphs: the context, the routine's task, the privacy
rule, and the approval rule.

**Context** (fill in the user's answers; leave out parts they didn't give):

> You are running a scheduled routine for <name> (<role>), time zone <time zone>, using the PersonalAISkills plugin (https://github.com/hardikashah-eng/PersonalAISkills). My team: <first names>. Sources I've connected: <kind>: <source>. Where things go when I approve them: <kind of message>: <where it goes>. My private growth log: <where the growth log lives> (read it through that connector, with the fields described in skills/feedback/references/growth-log.md; write to it only for items I approve). Keep the list to at most 5 items, spread fairly across people.

When the growth log is a file on their computer (here `team-growth.jsonl`), its sentence reads:

> My private growth log: team-growth.jsonl (read and edit it as described in skills/feedback/references/growth-log.md; write to it only for items I approve).

**Privacy rule:**

> Privacy: read only the sources named here, and only what each item needs. Skip anything about health, family, leave or personal life. Don't infer anyone's mood or emotions. Don't save anything to memory.

**Approval rule:**

> Approval rule: you prepare drafts only. Do not send, post, comment, message anyone, or write to the growth log or any shared tool during this run, except the one review message to me. End with a review list: number each item and show the recipient, the channel, the full draft, and the safety-check result. I will reply with what to send, edit or skip; act only on items I approve in that reply.

## The routines

### Daily people brief (`daily-brief`)

Morning list of recognition, follow-ups, first days and anniversaries.

> Run the nudge skill in daily mode for the last working day. Look for: specific work to recognize (merged PRs, resolved incidents, finished on-call shifts, docs), growth-log follow-ups due in the next two days, first days and work anniversaries on my calendar, and people I haven't recognized in 30 days. Draft each with the right skill (Kudos, Welcome, ThankYou), run the safety check, and send me the review list. If nothing is worth a nudge today, send one line saying so.

### After <meeting> (`after-meeting`)

Recognition and commitments from <meeting>.

> Find today's transcript of '<meeting>' in <where its transcripts are>. If there's no transcript, or transcription wasn't announced in the meeting, stop and tell me in one line. Otherwise run the nudge skill in after-meeting mode (reading it as in skills/nudge/references/transcript-scan.md, with me as the meeting owner). Draft Kudos for recognition moments and reported wins after reading the work they refer to; list possible feedback moments for me only, as prompts to check the facts; and list my own commitments with a suggested reminder time. Send me the review list.

### Friday recognition sweep (`weekly-kudos`)

The week's work worth recognizing, spread across the team.

> Run the nudge skill in weekly mode: this week's merged PRs, reviews, resolved incidents and on-call shifts for my team. Draft Kudos for the work that most deserves it (DM, plus a #kudos post where it fits; LinkedIn only for public work, marked as needing the person's consent). Include anyone who hasn't been recognized in 30 days if there's real work to name. Send me the review list.

### Monday growth follow-ups (`feedback-followups`)

Growth-log follow-ups due this week, and 1:1 prep.

> List the follow-ups due in the next 7 days in my growth log (skills/feedback/references/growth-log.md), and for each person with a 1:1 this week on my calendar, prepare a short summary (the growth log summary) with what's going well first and any follow-up due. Suggest one specific strength to mention for each person. Don't draft new feedback and don't contact anyone. Send me the prep list.

### Monthly reconnect (`monthly-reconnect`)

Two or three people worth reconnecting with.

> Run the reconnect skill: find two or three people I've drifted from (former teammates, mentors, friends) using my connected email and chat history, each with a real shared moment as the hook, and draft a no-guilt check-in for each. Send me the review list.

### Peer Pulse (`weekly-peer-pulse`)

Friday prompt and Monday thank-you drafts from peers' answers.

> If today is Friday: draft this week's Peer Pulse prompt for my team with the peer-pulse skill (skills/peer-pulse/references/prompt-and-tally.md), for me to post. If today is Monday: collect the replies to last Friday's prompt from my direct messages or the form results I named, tally them as in skills/peer-pulse/references/prompt-and-tally.md, with thank-you drafts and Spotlight evidence, and send me the private summary and the thank-you drafts. Never post or message anyone yourself.

### Monthly Team Story (`monthly-team-story`)

A draft highlight reel of the month's teamwork.

> Run the team-story skill for last month: gather the merged work, incidents handled, launches and Peer Pulse moments from my sources, and draft story.json with chapters that name what each person did (including reviews, docs, on-call and help from other teams). Build the page, the #wins post and the slide outline, and send me the drafts with a list of anyone who may be missing. Nothing is posted until I approve it.

### Quarterly Spotlight (`quarterly-spotlight`)

Who has consistently gone above and beyond this quarter, with workload checks.

> Run the spotlight skill for the quarter that just ended: add moments from my sources to my evidence file, run the pattern check (skills/spotlight/references/evidence-and-analysis.md), and the growth log's gaps check for fairness. Send me, privately: people with a sustained pattern (alphabetical, with reasons), workload flags to ask about, people not recognized lately, and for each person with a pattern an impact-story draft and two or three ways to elevate them. No rankings or scores.

_This file is generated from the full edition's routine builder, so both editions schedule the same routines._
