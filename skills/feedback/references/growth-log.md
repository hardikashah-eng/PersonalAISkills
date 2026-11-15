# The growth log

A running, private record of strengths and improvement opportunities for the
people the user supports. It makes 1:1s and reviews fair and specific, and it
makes sure growth gets noticed when it happens.

## What's in an entry

`date, person, type (strength | growth), area, observation, impact, next,
source (kudos | feedback | 1:1 | review), shared_with_person, status
(open | in progress | done | dropped), follow_up, history`

Areas: delivery, craft, reliability, communication, collaboration, ownership,
leadership, mentoring, customer focus, learning, other.

## Rules

1. **Only what the person has heard.** Growth items are logged after the
   conversation (`--shared`). The script warns about unshared entries.
2. **Strengths too.** Kudos adds strengths automatically when the user asks
   to log them; summaries show both, and warn when growth notes outnumber
   strengths.
3. **Facts, not labels.** Every entry passes the feedback safety check before
   it's saved; labels, health, money and personal details are refused.
4. **Follow up and close.** Each growth item gets a follow-up date. When
   things improve, mark it done, note what you saw, and tell the person.
5. **The person can see it.** If they ask, share their entries. If the user
   wouldn't be comfortable showing an entry to the person, it shouldn't be there.
6. **Not memory.** Entries are never saved to Claude's memory; they live only
   in the file or tool the user chooses.

## Where it can live

| Option | How |
|---|---|
| A file the user keeps (default) | `--log ~/Documents/team-growth.jsonl` on their computer, or a private drive folder |
| Google Sheets, Excel | `growth_log.py export --csv growth.csv`, then import; or Claude adds rows through a connected Sheets or Excel tool |
| Lark / Feishu Base | Claude adds a record per entry through a Lark connector, with the same fields |
| Notion, Airtable | a database with the same fields, through the connector |
| Jira or Linear | only for personal development goals the person owns and can see, never as tickets about them |

Formal HR systems (Workday, Lattice, 15Five, Culture Amp) have their own
rules; enter feedback there yourself, using the summary as a draft.
