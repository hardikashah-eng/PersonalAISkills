---
name: routines
description: Set up, change, pause or remove scheduled routines that keep the user's people habits going, such as a daily people brief, an after-standup scan for praise and commitments, a Friday kudos sweep, Monday growth-log follow-ups and 1:1 prep, a monthly reconnect, a weekly Peer Pulse, a monthly Team Story or a quarterly Spotlight. Asks a few questions, shows the plan, and creates each routine with the app's scheduling tool only after the user says yes. Every run prepares drafts and one review list; nothing is sent without approval. Use when the user wants nudges, kudos or feedback follow-ups on a schedule, says "do this every week", or accepts the offer to make it regular.
argument-hint: "[setup|list|change|pause|remove] [daily-brief|after-meeting|weekly-kudos|feedback-followups|monthly-reconnect|weekly-peer-pulse|monthly-team-story|quarterly-spotlight]"
---

# Routines

The other skills help in the moment. Routines make the moments come to the
user: a short list each morning, after standup, or on Friday, with drafts ready
to approve. This skill sets them up with the scheduling tool of the app the
user is in, and keeps them easy to change or stop.

## Non-negotiables

1. **Opt-in only.** Offer once, when it would clearly help (see "When to
   offer"). If the user says no or ignores it, don't offer again in that
   conversation. Never create a routine without an explicit yes to the plan.
2. **Every run is drafts-only.** The prompt in each routine forbids sending,
   posting or logging during the run, except one review message to the user.
   Items go out only when the user approves them in reply.
3. **Runs ask before acting.** When the scheduling tool lets you choose,
   create routines whose actions need the user's approval. Tell the user, in one
   sentence, which approval setting each routine got.
4. **Standalone prompts.** A scheduled run starts fresh, with no memory of this
   conversation. Write the prompt as in `references/routine-prompts.md`, so it
   carries the user's name, time zone, team, sources, channels, growth log and
   the approval and privacy rules.
5. **Few and quiet.** Start with one or two routines. A run with nothing worth
   doing sends one line ("Nothing today"), not an empty list.
6. **Nothing private in the prompt.** Names of teammates, tools and channels
   are fine; feedback content, health, personal details and credentials never
   go in a routine's prompt.

## When to offer

Offer once, in one line, at the end of a task, when the user:

- has used Kudos, Feedback or Nudge and it went well ("Want me to check for
  moments like this every Friday?")
- asks for something recurring ("remind me", "every week", "after standup")
- logs a growth item with a follow-up date ("Want a Monday list of follow-ups due?")

Don't offer during Comfort, Repair or anything sensitive.

## Setup

### 1. Ask (keep it to what's needed; use multiple-choice questions where possible)

1. **Which routines?** (`references/catalog.md`)
   - Daily people brief (weekday mornings)
   - After a recurring meeting (needs the meeting's name and where its transcripts live)
   - Friday kudos sweep
   - Monday growth follow-ups and 1:1 prep
   - Monthly reconnect
   - Weekly Peer Pulse (Friday prompt, Monday thank-you drafts)
   - Monthly Team Story draft
   - Quarterly Spotlight (who's consistently going above and beyond, with workload checks)
2. **When?** Times and days, and the user's **time zone** (ask; don't guess).
3. **Who's the team?** First names as they appear in tools and transcripts.
4. **Which sources are connected?** (code host, incident tool, calendar,
   meeting transcripts, chat). Check what's actually connected in this session;
   suggest a connector only for a source the user wants.
5. **Where does approved work go?** (Slack/Lark/Teams DM, #kudos, email)
6. **Growth log location** (a file on their computer, or a Sheet, Lark Base or
   Notion table). A local file means the routines that read it must run on
   the user's computer (see step 3).

Write the answers to `routines.json` (`examples/team-lead/routines.json`).

### 2. Show the plan

Turn `routines.json` into each routine's name, schedule and standalone prompt,
following `references/routine-prompts.md`. Show each routine's name, what it does, when it runs, and that it sends only
a review list. Ask: "Create these?"

### 3. Create them (only after a yes)

Use the scheduling tool available in this session (`references/platforms.md`):

- **Claude app (web, desktop, mobile):** create each as a scheduled task with
  the generated name, schedule and prompt. If a routine reads a local growth
  log, create it as one that runs on the user's computer, with that folder
  attached. Turn on push notifications if the tool offers them, so the
  review list reaches the user's phone.
- **Claude Code:** create a cloud routine (`/schedule`, or claude.ai/code/routines)
  with the generated prompt, or a Desktop scheduled task when it must read
  local files.
- **No scheduling tool here:** give the user the plan and the prompts, and
  the steps to add them at claude.ai/code/routines or in the desktop app.

Confirm what was created: names, next run times, the approval setting, and
how to change or stop each one.

## Manage

- **List:** the user's existing routines from this plugin (names start with
  the routine titles above), with their schedules.
- **Change:** a new time, days, team members or sources: write that routine's
  prompt and schedule again (`references/routine-prompts.md`) and update the routine.
- **Pause or remove:** on request, with the user confirming each removal.
- **Too noisy?** Suggest fewer routines, a lower `max_items`, or weekly instead of daily.

## Files

- `references/routine-prompts.md`: turns `routines.json` into names, schedules and standalone prompts
- `references/catalog.md`: each routine, what it reads, what it prepares, and good default times
- `references/platforms.md`: how to create routines in the Claude app, Claude Code, or by hand
- `examples/team-lead/`: an example `routines.json`, the plan (`plan.txt`) and the generated routines (`routines-plan.json`)
