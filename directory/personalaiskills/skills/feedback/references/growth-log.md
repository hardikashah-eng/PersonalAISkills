# The growth log

A running, private record of strengths and improvement opportunities for the
people the user supports. It makes 1:1s and reviews fair and specific, and it
makes sure growth gets noticed when it happens.

## What's in an entry

`date, person, type (strength | growth | sponsorship), area, observation, impact, next,
source (kudos | feedback | 1:1 | review), shared_with_person, status
(open | in progress | done | dropped), follow_up, history`

Areas: delivery, craft, reliability, communication, collaboration, ownership,
leadership, mentoring, customer focus, learning, other.

## Rules

1. **Only what the person has heard.** Growth items are logged after the
   conversation, marked as shared. Point out any entry that isn't.
2. **Strengths too.** Kudos adds strengths automatically when the user asks
   to log them; summaries show both, and warn when growth notes outnumber
   strengths.
3. **Facts, not labels.** Every entry passes the feedback checks in
   `../../thankyou/references/safety-checklist.md` before it's saved; labels,
   health, money and personal details are refused.
4. **Follow up and close.** Each growth item gets a follow-up date. When
   things improve, mark it done, note what you saw, and tell the person.
5. **The person can see it.** If they ask, share their entries. If the user
   wouldn't be comfortable showing an entry to the person, it shouldn't be there.
6. **Not memory.** Entries are never saved to Claude's memory; they live only
   in the file or tool the user chooses.

## Sponsorship and fairness

- **Sponsorship** entries record what the user did to elevate someone (a
  nomination, a stretch project, an introduction, a mention to leadership)
  and, once updated, the outcome. Spotlight adds them.
- **The gaps check** lists people with no strengths or sponsorship logged in
  the last N days (30 by default), and, given groups (location, time zone,
  role), whether recognition is spread fairly. It's a prompt to look for
  contributions that are easy to miss, never a judgement.

## Where it can live

| Option | How |
|---|---|
| A file the user keeps (default) | `team-growth.jsonl` in a folder on their computer, or a private drive folder |
| Google Sheets, Excel | a CSV export Claude writes from the file, then import; or Claude adds rows through a connected Sheets or Excel tool |
| Lark / Feishu Base | Claude adds a record per entry through a Lark connector, with the same fields |
| Notion, Airtable | a database with the same fields, through the connector |
| Jira or Linear | only for personal development goals the person owns and can see, never as tickets about them |

Formal HR systems (Workday, Lattice, 15Five, Culture Amp) have their own
rules; enter feedback there yourself, using the summary as a draft.

## Working with the log

The default file is JSON Lines: one entry per line, as a JSON object. Read it,
change it and write it back yourself; keep every line you didn't change
exactly as it was. Write only entries the user approved.

```json
{"id": 3, "date": "2026-11-14", "person": "Dami", "type": "growth", "area": "communication",
 "observation": "In the last two design reviews, the risks section came after the demo",
 "impact": "Reviewers raised the risks late, and the decision slipped a week",
 "next": "Lead with the decision needed and the top three risks", "source": "feedback",
 "shared_with_person": true, "status": "open", "follow_up": "2026-12-05", "history": []}
```

- **Add:** the next `id` (one more than the highest), today's date unless the
  user gives one, `status` `open` for growth and sponsorship and `noted` for
  strengths, and an empty `history`. A growth entry needs `next`. Check the
  text first (rule 3) and refuse to save anything that fails. After adding a
  growth entry that isn't shared yet, remind the user to share it directly. For
  sponsorship, remind them to add the outcome later.
- **Update:** change `status`, `follow_up` or `shared_with_person`, and append
  `{"date", "status", "note"}` to `history`. Check a note's text the same way.
- **List:** filter by person, type, or open items (`open` or `in progress`);
  mark entries not yet shared.
- **Due:** open items whose `follow_up` falls within the next N days (7 by
  default), soonest first, as "date · #id person: next".
- **Summary for one person** (Markdown, for a 1:1 or review): "What's going
  well" (strengths, with area, date and observation) first; then sponsorship
  with outcomes from `history`; then growth areas with effect, next and
  progress notes. End with the counts, a note if growth entries outnumber
  strengths, and how many entries haven't been shared yet.
- **Gaps:** people on the team with no strength or sponsorship entry in the
  last N days. With groups, show each group's share of the team next to its
  share of recognition, and point out any group whose share of recognition is
  more than 15 points lower.
- **Export:** a CSV with the same fields, for Sheets, Lark Base or Excel.
