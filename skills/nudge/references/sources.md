# Sources and what they're used for

Every source is read-only, used only for the nudge in front of the user, and
never stored. The user chooses which ones to connect.

| Source | Read | Never |
|---|---|---|
| Meeting transcripts (Zoom, Teams, Meet, Lark Minutes, Otter) | who credited whom, reported wins, blockers that name a person, commitments | infer emotion or stress; analyse personal remarks; HR, medical or legal meetings |
| Code hosts (GitHub, GitLab, Bitbucket) | merged PRs, reviews, issues closed | count lines of code or rank people by activity |
| Incident and ticket tools (PagerDuty, Opsgenie, Jira, Linear) | resolved incidents, on-call shifts, closed tickets | assign blame |
| Calendar | meetings that just ended, first days, recurring 1:1s | read private event details |
| HR calendar (only if the user shares it) | start dates, work anniversaries, returns from leave | the reason for any leave |
| Chat and email | threads the user names, replies to an intro ask | read private conversations broadly |
| Growth log (the user's own file) | follow-up dates, recent strengths | share it with anyone |

## Transcript etiquette

- Use transcripts only from meetings where transcription was announced.
- Quote at most one sentence, and only to the user, to show why a nudge exists.
- When a kudos draft is based on what someone said in a meeting, say so
  ("Bea mentioned in standup…"), so the recognition is honest about its source.
