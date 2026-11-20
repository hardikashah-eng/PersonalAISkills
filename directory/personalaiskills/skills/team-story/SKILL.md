---
name: team-story
description: Showcase great teamwork by telling a project, launch or quarter through everyone's contributions, including the invisible work, as a one-page highlight reel with a "who helped whom" map, quotes and thanks to people on other teams, plus a #wins channel post, an all-hands slide outline and a short note for leadership. Shows connections, never rankings, and names people only for what they'd be glad to see shared. Use when a leader wants to celebrate a team win, prepare an all-hands or quarterly update, or show leadership how the team works together.
argument-hint: "[project or period] [page|post|slides|leadership note]"
---

# Team Story

Launch announcements usually name the project and the leader. The real story
is a chain of people: the one who found the bug at 2 a.m., the reviewer who
caught the edge case, the new hire who fixed the flaky test, the friend on
another team who tested it. Team Story tells it that way, so everyone sees
their part and leadership sees how the team actually works.

## Non-negotiables

1. **Everyone who contributed, in their own role.** Include the invisible
   work: reviews, docs, on-call, mentoring, coordination, help from other teams.
   Check the list with the user so nobody's missing.
2. **Connections, not rankings.** The map shows who helped whom, every person
   the same size; no counts per person, no "MVP", no top contributors.
3. **True and specific.** Each line names what the person did, from the
   work itself (PRs, docs, incidents, transcripts) or the user. No inflated outcomes;
   numbers only from real sources.
4. **Shared with consent where it matters.** Quotes are used with the
   speaker's OK. Nothing internal goes into anything public; for public
   versions, use Kudos' public rules.
5. **Send or post only on an explicit yes.**

## Workflow

### 1. Gather

- **The arc**: what the team set out to do, the turning points, the outcome
  (in the team's own terms: faster builds, fewer pages, a launch).
- **Who did what** in each chapter, from the user, connected tools (merged
  PRs, design docs, incident timelines, release notes) and Spotlight evidence
  if the user keeps it.
- **Quotes** from the team, users or other teams: from Peer Pulse answers,
  meeting transcripts, threads (with the speaker's OK).
- **Thanks beyond the team**: partner teams, a leader who protected focus time.

### 2. Write `story.json` (`references/story-shape.md`)

Title, period, a one-sentence headline, three to five chapters (title, when,
what, contributors with what each did), quotes, `also_thanks`, and a closing
line. Optional `helped` pairs, or point to Spotlight evidence for the map.

### 3. Build the versions

From `story.json` (and Spotlight's evidence file for the map, if the user
keeps one), make the page, a #wins or all-hands channel post, and a slide
outline for an all-hands deck, following `references/page-and-map.md`.

- **The page** is one self-contained HTML file (publish it as an artifact
  where available, or share the file).
- **Slides:** use the slide outline to make a deck with the Slides artifact
  type where it's available, or the pptx skill when the user asks for PowerPoint.
- **For leadership:** write a five-line note: the outcome,
  how the team worked together, two people to know about, and one ask
  (resources, a recognition, a decision).

### 4. Check and share

Check `story.json` with `../thankyou/references/safety-checklist.md` (the
every-note and team checks, and the public-post checks for anything public). Show the user each version, and post or send only on
an explicit yes. Offer to send each contributor a Kudos note with their line.

## Automate it

The Routines skill can run a monthly Team Story draft from the month's merged
work and Spotlight evidence for the user to review (`../routines/SKILL.md`).

## Files

- `references/page-and-map.md`: build the page with the who-helped-whom map, the post and the slide outline
- `references/story-shape.md`: the arc, chapters, what to include, examples of good lines
- `examples/q4-build-queue/`: a quarter's story with the map, post and slide outline
