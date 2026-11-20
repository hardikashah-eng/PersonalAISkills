# Evidence and the pattern check

## The evidence file

One private file the user keeps, `evidence.jsonl`: JSON Lines, one moment per
line. Read it, add to it and write it back yourself, keeping existing lines
as they are. Skip a new moment if the same person, kind, link, from and date
are already there.

```json
{"date": "2026-10-07", "person": "Chen", "kind": "review-for-others", "from": "Dami",
 "source": "github", "summary": "Reviewed the cache rollout PR; caught a stale-key bug",
 "link": "https://github.com/acme/api/pull/501", "beyond_role": false, "cross_team": false}
```

Kinds: `peer-thanks`, `kudos`, `review-for-others`, `incident-help`,
`on-call-cover`, `mentoring`, `docs`, `onboarding-help`, `cross-team-help`,
`unblocked`, `other`. Use first names consistently, and keep personal details
and email addresses out.

## Collecting from GitHub

With the GitHub connector (read-only), for the repositories and period the user
names, and a map of GitHub logins to first names for the team:

- **Reviews on others' PRs:** for each PR updated in the period, each review
  (approved, changes requested, or commented) by a team member on a PR they
  didn't write becomes a `review-for-others` moment: `from` is the PR author,
  `summary` is `Reviewed "<PR title>" (<state>)`, `link` is the PR, and
  `cross_team` is true when the author isn't on the team.
- **Thanks in PR threads:** a comment that contains thanks, kudos, appreciate,
  great or nice catch, or saved, and @-mentions a team member (who didn't write
  it) becomes a `peer-thanks` moment for that member: `from` is the writer,
  `summary` is the comment (up to about 200 characters, emails removed), and
  `link` is the comment.

Without the connector, ask the user for the PR links or a list of moments.

## The pattern check

For the period, group the moments by person. For each person, count the
distinct ISO weeks, the kinds of source, the colleagues who gave thanks or got
help (`from`, other than themselves), the kinds of moment, and the moments
that were beyond their role or across teams.

- **Sustained pattern:** at least 4 weeks, 2 kinds of source and 3 colleagues,
  and at least one moment beyond their role or across teams, or 3 or more
  kinds of moment. Give the reasons: "7 different weeks; 4 kinds of source;
  5 colleagues; reviews, incident help, mentoring, docs".
- **Worth watching:** not sustained, but moments in 2 or more weeks.
- **Check workload** (ask, don't assume): covered others' on-call twice or
  more; helped on two or more incidents outside their own rota; or did at
  least 6 reviews for others and two and a half times the team's typical
  (median) number.

Show it to the user privately, alphabetically, never ranked or scored:

```markdown
Spotlight check, 2026-10-01 to today

## Sustained pattern of going above and beyond (alphabetical, not ranked)
- **Chen**: 7 different weeks; 4 kinds of source; 5 colleagues; reviews, incident help, mentoring, docs

## Worth watching (a pattern may be forming)
- Bea, Dami

## Check workload (ask, don't assume)
- **Chen**: covered others' on-call 2 times. Ask how they're doing and whether the load is sustainable.

_Private to you. No scores or rankings; use this to decide who to look at more closely._
```

If nobody meets the bar, say so: that's fine, the bar is several weeks,
sources and colleagues.

## Gathering the evidence for a story

For one person, sorted by date: a line with the period, the number of
moments, weeks, sources and colleagues; a placeholder for "The pattern" (one
or two sentences written from the evidence); then the moments grouped by
theme, each as "date: summary (from X)" with a Markdown link to the work,
tagged "beyond role" or "another team" where it applies:

| Theme | Kinds |
|---|---|
| Raising others | mentoring, onboarding-help, unblocked |
| Reviews and quality | review-for-others |
| Reliability | incident-help, on-call-cover |
| Knowledge sharing | docs |
| Across teams | cross-team-help |
| What peers said | peer-thanks, kudos |

End with "Ways to elevate them" as a checklist: a note to their manager and
skip-level; a nomination; a stretch opportunity they'd want; an introduction
to someone senior (Intro); a public shout-out, only for public work and with
their OK (Kudos); a mention in the next Team Story or all-hands. Then the
story itself follows `impact-story.md`.
