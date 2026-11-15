# Kudos on LinkedIn

A public shout-out can help someone's career, but only when the work is
public and they want it seen.

## Post publicly only if all of these are true

1. **The work is public**: open-source contributions, a launched feature, a
   published paper, a conference talk, a public product milestone, a community
   event. Internal fixes, incidents, roadmaps, customers and metrics stay internal.
2. **The person agreed** to be named and tagged (`consent.named_person_ok`).
   Ask them; some people prefer not to be on LinkedIn or not to be tagged.
3. **Your company's social media policy allows it** (`consent.company_policy_ok`).
   Many require that only announced work is discussed.
4. **It passes** `safety_check.py --profile public`: no ticket or PR numbers,
   internal links, confidential or unreleased work, security details, people
   matters, and any metric already published.

## Shape of a good post (40–110 words)

- Open with the person and what they did, in public terms.
- One sentence on why it matters to users or the community.
- One sentence on the quality you admire.
- Optional: a link to the public artifact (release notes, the open-source PR,
  the talk), and two or three relevant hashtags.

> Shout-out to Bea Ramos, who made our open-source client's retries smarter
> this month. Her change spreads out reconnect attempts, so apps using the
> library recover from network blips without overwhelming servers. What I
> admire most: she wrote the tests and the docs before anyone asked. Thank
> you, Bea. #opensource #reliability

## How it gets posted

LinkedIn's share link can't pre-fill post text, so:

- **Paste:** open https://www.linkedin.com/feed/, select **Start a post**, paste.
- **With Claude's help in the user's browser:** only if the user asks, Claude
  opens LinkedIn, fills in the post and stops before **Post**, so the user
  reviews and posts it themselves.
- **@mentions:** type "@" and pick the person from LinkedIn's list, only if
  they agreed to be tagged.

When in doubt, keep it internal: a #kudos post and a note to their manager do
most of the good with none of the risk.
