---
name: spotlight
description: Find the people who consistently go above and beyond, judged by a pattern over weeks and from several sources and colleagues (help on code reviews, incidents outside their rota, mentoring, docs other teams use, peer thanks), not one big launch. Turns that pattern into an evidence-backed impact story, then into sponsorship (a nomination, a note to their manager and skip-level, a stretch opportunity, an introduction, a public shout-out with consent) and checks whether the extra effort is sustainable. No scores or rankings. Use when a leader wants to recognize or elevate someone, prepare an award or promotion case, or ask "who is quietly carrying the team?"
argument-hint: "[team or person] [period, e.g. this quarter] [--nominate|--story|--check]"
---

# Spotlight

Some people make everyone around them better, week after week, often in ways
that never show up in a launch announcement. Spotlight finds that pattern in
the evidence, tells their story with links to the real work, and helps the
user do something that changes their career, not just say thanks.

## Non-negotiables

1. **A pattern, not a moment.** Someone is surfaced only when the evidence
   spans several weeks (default four or more), several kinds of source (two
   or more) and several colleagues (three or more), and shows help beyond their
   own role, across teams, or in several ways.
2. **No scores, rankings or leaderboards.** Candidates are listed
   alphabetically with the reasons. Nobody is shown as "less" than anyone else,
   and the evidence is never used to criticize anyone.
3. **Check the load.** "Always going above and beyond" can mean overloaded.
   Flags like repeated on-call covers or carrying most of the review load are
   prompts for the user to ask how they're doing and rebalance. Never guess at
   personal reasons, and never mention health.
4. **Grounded and linked.** Every claim in the story comes from an evidence
   line with its source; nothing is invented or inflated.
5. **Private until shared.** The analysis and story are for the user. Public
   or formal steps (an award nomination, an all-hands mention, a LinkedIn
   post) follow the person's wishes; ask them first unless the company runs
   surprise awards, and then still keep anything personal out.
6. **Fair.** Watch for who's easy to miss: remote, other time zones, quieter,
   newer, or doing "glue work". The gaps check in the growth log
   (`../feedback/references/growth-log.md`) helps.
7. **Send only on an explicit yes** (`../thankyou/references/delivery.md`).

## Workflow

### 1. Gather evidence (a quarter is a good window)

Keep one evidence file (`evidence.jsonl`, private to the user) and add to it from:

| Source | How |
|---|---|
| GitHub reviews on others' PRs, thanks in PR threads | the GitHub connector, read-only, for the repos, period and team logins the user names (`references/evidence-and-analysis.md`) |
| Meeting transcripts | Nudge's recognition moments from a transcript, added as `peer-thanks` |
| Peer Pulse answers | Peer Pulse's tally adds them (`../peer-pulse/SKILL.md`) |
| Kudos the user sent | growth-log strengths, added as `kudos` |
| Incidents, on-call, cross-team help, mentoring, docs | the user's incident tool, chat and docs through connectors, or the user's own notes |

Each line: date, person, kind, from, source, summary, link, `beyond_role`,
`cross_team` (format in `references/evidence-and-analysis.md`). Use first names
consistently, and keep personal details out.

### 2. Look for the pattern

Run the pattern check in `references/evidence-and-analysis.md` over the
period (for example, since 2026-10-01). It lists people with a sustained pattern (alphabetical, with reasons), people
where a pattern may be forming, and workload to check. Discuss it with the user;
they know context the evidence doesn't.

### 3. Tell their story

Gather Chen's moments for the period, grouped by theme with links
(`references/evidence-and-analysis.md`), into `chen-evidence.md`. From the evidence, write the impact story (`references/impact-story.md`):
a two-sentence summary of the pattern, then three or four themes with the
strongest examples and links, what colleagues said, and the difference it made.

### 4. Elevate them (`references/sponsorship.md`)

Help the user pick and draft what fits the person and the company:

- **A note to their manager and skip-level** (if the user isn't their manager)
- **A nomination** for an award or a promotion case, in the company's own
  template (ask for it); the story is the evidence section
- **A stretch opportunity** they'd want: leading a design review, owning a
  launch, presenting at a staff meeting or a conference
- **An introduction** to someone senior who should know their work (Intro)
- **A public shout-out**, only for public work and with their OK (Kudos, with the public-post checks)
- **A mention in the next Team Story** or all-hands

Then talk to the person: what they'd value, and the workload question if
it was flagged.

### 5. Log it and follow through

Log each sponsorship step and its outcome in the growth log
(`../feedback/references/growth-log.md`): for example, a sponsorship entry for
Chen, area leadership, observation "Nominated for the Q4 engineering award;
offered the build-queue redesign lead", source review, shared.

Update it when there's an outcome ("won", "took the lead", "promoted").

## Automate it

The Routines skill can run a quarterly Spotlight check that gathers evidence,
runs the analysis and sends the user a private summary (`../routines/SKILL.md`).

## Files

- `references/evidence-and-analysis.md`: the evidence file, collecting from GitHub, the pattern check, assembling the evidence for a story
- `references/impact-story.md`: how to write the story, with an example
- `references/sponsorship.md`: ways to elevate someone, nomination shape, the workload conversation
- `examples/q4-platform/`: a quarter of evidence, the analysis, Chen's impact story, a nomination and a manager note
