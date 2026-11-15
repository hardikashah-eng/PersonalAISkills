# Routine catalog

| Key | Name | Reads | Prepares | Default |
|---|---|---|---|---|
| `daily-brief` | Daily people brief | code host, incident tool, calendar, growth log | up to five drafts: kudos, welcomes, anniversaries, follow-ups due, people not recognized lately | weekdays 8:40 |
| `after-meeting` | After *meeting name* | that meeting's transcript | kudos for praise and reported wins; possible feedback moments (for the user only); the user's commitments | weekdays, 30–40 minutes after the meeting ends |
| `weekly-kudos` | Friday recognition sweep | the week's merged PRs, reviews, incidents, on-call | kudos spread fairly across the team; #kudos posts | Friday mid-afternoon |
| `feedback-followups` | Monday growth follow-ups | growth log, calendar 1:1s | 1:1 prep: strengths first, follow-ups due; no new feedback | Monday early morning |
| `monthly-reconnect` | Monthly reconnect | email and chat history | two or three no-guilt check-ins | early in the month, afternoon |
| `weekly-peer-pulse` | Peer Pulse | replies to the Friday prompt | Friday: the prompt for the user to post; Monday: the private tally and thank-you drafts | Friday and Monday, early afternoon |
| `monthly-team-story` | Monthly Team Story | the month's merged work, incidents, launches, Peer Pulse moments | a draft highlight reel, #wins post and slide outline | early in the month |
| `quarterly-spotlight` | Quarterly Spotlight | evidence file, growth log, sources | private: sustained patterns, workload flags, fairness gaps, impact-story drafts | a few days into the new quarter |

## Starting small

Most people do best with **one daily and one weekly** routine: the
after-standup scan (or the daily brief) plus the Friday sweep. Add the Monday
follow-ups once the growth log has a few entries.

## What a run sends

One message to the user: a numbered review list (recipient, channel, full
draft, safety-check result), or "Nothing today". The user replies "send 1 and
3", "edit 2: …" or "skip"; only then are items sent, one at a time.

## Times

Times are in the user's time zone. Monthly and quarterly routines run on a
day of the month (`"monthly 3"`, `"quarterly 5"`), since cron can't say "first
Monday" on its own. Times exactly on the hour or half hour are
moved a few minutes earlier, since many scheduled jobs start then.
