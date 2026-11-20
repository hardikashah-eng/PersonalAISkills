# The prompt and the tally

Both are prepared by Claude. Nothing is posted or sent: the organizer posts
the prompt and approves every thank-you.

## The prompt

For Slack (use `**Peer Pulse**` for Teams and Lark; plain text for email and WhatsApp):

```text
🙌 *Peer Pulse* for <team>: two quick questions, one minute.

1️⃣ Who helped you this week?
2️⃣ How did it help?

Reply to me directly (not in the channel) by <due>. Tell me if I can name you when I pass it on (yes / anonymous / just for me). Small things count: a review, an answer, a pairing session.
```

Plain version:

```text
Peer Pulse for <team>: two quick questions.

1. Who helped you this week?
2. How did it help?

Reply to me directly by <due>, and say whether I can name you when I pass it on (yes / anonymous / just for me). Small things count.
```

## Reading the answers

Each answer has `date`, `from`, `helped`, `how` and `share`. Skip answers
with no `helped` or `how`. Read `share` as **yes** (yes, y, ok, name me),
**anonymous** (anything starting with "anon") or **private** (anything else,
including blank). One answer can thank several people ("Chen and Dami", "Bea,
Ola"): count it once for each. Match names to the team by full or first name;
people not on the team are kept and marked "another team".

**Hold an answer** (no draft, not stored, not quoted) when its `how` fails the
every-note or team checks in `../../thankyou/references/safety-checklist.md`,
or touches on personal matters: illness, a doctor or hospital, surgery,
therapy, medical or medication, a diagnosis, pregnancy, maternity or
paternity, a funeral, passed away or bereavement, divorce, a family
emergency, mental health, burnout, anxiety or depression, a visa, salary or a
raise, a layoff, being fired.

## The organizer's private summary

```markdown
Peer Pulse: 6 answers, 5 thank-yous

## Chen
- from Bea: paired with me for an hour on the flaky scheduler test
- from Ola: reviewed my migration on a Sunday  [anonymous]

## Ravi (another team)
- from Dami: unblocked the eu rollout  [just for you]

Not mentioned this week (for your awareness only; often just a quiet week): Kenji

Held for you to read in the original (personal or sensitive; no draft, not stored):
- Arjun about Dami
```

## Thank-you drafts

One Kudos `note.json` per person thanked (`drafts/kudos-<firstname>.json`),
only from answers that aren't private. Quote each as the writer allowed: their
name for "yes", "a teammate" for "anonymous".

```json
{"kind": "kudos", "text_only": true, "audience": "individual", "recipient_first_name": "Chen",
 "sender_first_name": "Hardik", "source": "Peer Pulse", "greeting": "Chen,",
 "body": ["2 people mentioned you in this week's Peer Pulse. Bea: \"Paired with me for an hour on the flaky scheduler test.\" a teammate: \"Reviewed my migration on a Sunday.\"",
          "Thank you for making the team better. It was noticed."],
 "closing": "", "signature": "Hardik"}
```

("Someone mentioned you…" when there is one.)

## Evidence for Spotlight

If the organizer keeps a Spotlight evidence file
(`../../spotlight/references/evidence-and-analysis.md`), add one line per
thank-you: kind `peer-thanks` (or `cross-team-help` for another team),
`from` the writer's name only for "yes" (otherwise "a teammate"), source
`peer-pulse`, and the `how` as the summary. For private answers the summary
is "Thanked privately in Peer Pulse (not for quoting)". Held answers are not
added.
