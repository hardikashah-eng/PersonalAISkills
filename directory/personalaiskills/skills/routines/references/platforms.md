# Creating routines in each app

## Claude app (claude.ai on the web, desktop, mobile)

Claude creates each routine as a **scheduled task** with its own scheduling
tool: the name, the cron schedule in the user's time zone, and the generated
prompt. Then:

- **Local files:** if a routine reads a growth log on the user's computer, it
  must run on that computer (the desktop app open), with the folder attached.
  Otherwise, keep the log in a Sheet, Lark Base or Notion table so routines can
  run in the cloud.
- **Approval:** prefer the setting where runs ask before acting. Say which
  setting each task got; the user can change it in the task's settings.
- **Notifications:** turn on push notifications so the review list reaches
  the user's phone. Email only if the user asks.
- The user reviews each run's list in that run's conversation and replies
  there with what to send.

## Claude Code

- **Cloud routine:** `/schedule` in the CLI walks through creating one, or
  the user adds it at claude.ai/code/routines. Paste the generated prompt and
  set the schedule; custom cron expressions go in through `/schedule update`.
- **Desktop scheduled task:** for routines that need local files; it runs only
  while the desktop app is open and the computer is awake.
- `/loop` and in-session cron tools stop when the session ends, so they are
  not used for routines.

## By hand

If no scheduling tool is available, give the user the plan and each prompt
and schedule, and point them to claude.ai/code/routines or the desktop app's
Schedule page.
