---
name: kudos
description: Write specific, sincere recognition for real work, such as a merged pull request, a resolved incident, a design doc, an on-call shift, a great code review or mentoring, by reading the work itself and naming exactly what the person did and the difference it made. Delivers a direct message, a post for a #kudos or team channel (Slack, Lark, Teams), a note to their manager, or, when the work is public-safe and the person agrees, a LinkedIn post. Can log the strength for 1:1s and reviews. Use when the user wants to thank, recognize or give a shout-out to a colleague for their work.
argument-hint: "[person] [the work: PR URL, incident, doc, shift] [--dm|--channel|--manager|--linkedin] [--log]"
---

# Kudos

"Great job!" fades in a minute. "Your retry fix in #482 stopped the 2 a.m.
pages, and the tests you added mean nobody has to fear that code again" is
remembered for years. This skill reads the actual work and names the specific
thing the person did, why it mattered, and the quality behind it, in two or
three sentences, ready to post where they'll see it.

## Non-negotiables

1. **Grounded in the real work.** Read the PR, incident, doc or thread before
   writing. Never invent impact, numbers or praise. If the impact isn't known,
   describe what they did, and ask the user what changed because of it.
2. **Specific beats superlative.** One concrete detail is worth ten adjectives.
   No "rockstar", "ninja", "10x", "legend" (`references/kudos-patterns.md`).
3. **Recognize the person, not just the outcome**, and especially the work
   that's easy to miss: tests, docs, reviews, calm incident updates, unblocking
   others, mentoring, the on-call shift where nothing went wrong.
4. **Fair and inclusive.** Credit everyone who did the work. Notice people in
   other time zones and quieter roles. The daily nudge (`../nudge/SKILL.md`)
   can show who hasn't been recognized lately.
5. **Private stays private.** No health, personal life, salary or performance
   ratings, and nothing about why someone was out (`../thankyou/references/safety.md`).
6. **Public only when safe and agreed.** A LinkedIn post needs the work to be
   public (open source, a launched feature, a talk), the person's OK to be
   named, and the company's social media policy (`references/linkedin.md`).
7. **Send or post only on an explicit yes** (`../thankyou/references/delivery.md`).

## Workflow

### 1. Find the work

From the user ("thank Bea for #482") or from context: the PR or issue URL,
the incident ticket, the design doc, the on-call handoff, the thread.

- **GitHub:** `python3 scripts/work_context.py <PR or issue URL>` (read-only,
  through the user's signed-in `gh`), or the GitHub connector.
- **GitLab, Bitbucket, Jira, Confluence, PagerDuty, Lark, Google Docs, Notion,
  Slack threads:** through the user's connectors. Read only the item named.

### 2. Name the contribution

Answer three questions from what you read (`references/kudos-patterns.md`):

- **What exactly did they do?** ("traced the retry storm to a missing jitter,
  fixed it and added a load test")
- **What difference did it make?** ("on-call has been quiet for two weeks";
  "the release went out on time"). Use numbers only if they're in the source
  and the audience may see them.
- **What quality does it show?** (thoroughness, calm under pressure, care for
  the next person, generosity with time)

If the user knows something the source doesn't ("she stayed late so I could
make my kid's game"), use it; their words are the most personal part.

### 3. Write it (2–3 sentences)

Formula: **what they did → the difference → the quality**, then a plain
"Thank you". Write the versions the user needs in `note.json`:

| Field | Where it goes | Length |
|---|---|---|
| `body` | a direct message to the person | 2–3 sentences |
| `channel_post` | #kudos or the team channel, with their name and the work | 2–3 sentences |
| `manager_note` | to their manager, so it counts at review time | 2–4 sentences |
| `public_post` | LinkedIn, only when public-safe and agreed | 40–110 words |

Quick mode is the default: text only (`"text_only": true`). A card
(`../thankyou/scripts/render_card.py`) is for milestones such as a launch,
a work anniversary, or a year of on-call.

### 4. Check it

```bash
python3 ../thankyou/scripts/safety_check.py note.json                     # DM, channel, manager note
python3 ../thankyou/scripts/safety_check.py note.json --profile public    # before any LinkedIn post
```

The `public` profile blocks ticket and PR numbers, internal links, and words
like confidential, unreleased, incident details and security issues. It flags
metrics and requires `consent.named_person_ok` (the person said yes to being
named). Rewrite internal details in public terms, or keep the kudos internal.

### 5. Deliver

```bash
python3 ../thankyou/scripts/share.py note.json --channel slack            # DM text
python3 ../thankyou/scripts/share.py note.json --channel slack --post     # #kudos channel post
python3 ../thankyou/scripts/share.py note.json --channel email --manager  # note to their manager
python3 ../thankyou/scripts/share.py note.json --channel linkedin         # public_post
```

With a connector (Slack, Lark, Teams), Claude can create the draft or post
after the user's explicit yes. For LinkedIn there's no link that pre-fills
post text: the user pastes it into "Start a post", or, if they ask, Claude
opens LinkedIn in their browser, fills in the post, and stops before **Post**
for them to review. Tag the person only if they agreed.

### 6. Log the strength (optional, `--log`)

Add it to the user's private growth log, so it's there for 1:1s and reviews:

```bash
python3 ../feedback/scripts/growth_log.py add --log <their log file> --person Bea --type strength \
  --area reliability --observation "Traced the retry storm to missing jitter, fixed it and added a load test (#482)" \
  --impact "No retry pages since" --source kudos --shared
```

## Automate it

See `../../AUTOMATION.md`. In short: a weekly scheduled task can list merged
PRs, resolved incidents and finished on-call shifts from the user's
connectors, draft a kudos note for each one worth recognizing, and hand the
user a review list. Nothing is posted until the user approves each one.

## Files

- `references/kudos-patterns.md`: the formula, examples by kind of work, words to avoid, fairness
- `references/linkedin.md`: when a public post is OK, consent, company policy, how to post
- `scripts/work_context.py`: read a GitHub PR or issue (read-only) for the facts
- `examples/bea-retry-fix/`: one fix, four versions (DM, #kudos, manager note, LinkedIn)
