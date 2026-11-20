# Reading a meeting transcript for people moments

Read the transcript yourself and list, for the meeting owner only, four kinds
of moment. It only reads: nothing is sent, and no one is contacted.

## Getting the lines

Transcripts come as WebVTT (`<v Name>text`), SRT, Lark/Feishu Minutes ("Name
00:12" on its own line, then the text), or plain "Name: text" lines, as
exported from Zoom, Teams, Google Meet, Lark, Otter and similar. Turn it into
speaker, time and text for each line. If there are no speaker names, ask the
user to export the transcript with them.

**Skip personal lines entirely.** Any line that touches on health (sick, ill,
doctor, hospital, surgery, therapy, medication, diagnosis, pregnancy), family
(kids, partner, family, funeral, passed away), leave (maternity, paternity,
leave), personal life or stress (personal, mental, stressed, burnout,
anxiety), immigration (visa), or pay and job status (salary, raise,
promotion, PIP, fired, layoff) is not analysed or surfaced. Count how many
were skipped and say so at the end. Don't infer tone or emotion.

## The four kinds of moment

| Moment | Cues | Who it's about | Next step |
|---|---|---|---|
| **Recognition** | thanks, thank you, shout-out, kudos, props, credit to, great job / work / catch / call / find / write-up / idea, nice work / job / catch / find, saved / unblocked / rescued us, couldn't have done it without, huge help, well done, nailed it, really helped | the colleague named in that sentence; if no one is named and the line starts with thanks, nice or great (not "thanks, everyone"), the previous speaker | a Kudos draft, after reading the work it refers to |
| **Win** | shipped, merged, launched, released, landed, went live, is live, rolled out, in prod; no pages / alerts / incidents; fixed, closed out, finished, wrapped up | the speaker (not the meeting owner) | maybe a Kudos from the owner, after checking the work |
| **Possible feedback** | blocked on / by, still waiting on, waiting on, slipped / slipping, missed the / our / a, didn't get / have / hear / see, no update, not done, dropped, fell through, behind on / schedule, again, confused / confusing, without telling / a heads-up / review, broke the / prod / staging / main | a colleague named in that line | private to the owner: check the facts, then decide whether it's worth a word in a 1:1 |
| **Commitment** | I'll, I will, I'm going to, I can have, will have, let me … (and a when: by, before, on, this, next, tomorrow, today, EOD, end of day / week) | the speaker; mark the owner's own | a follow-up reminder |

Match names by first name, including team members who didn't speak (the user
can give the team list). Quote the sentence that holds the cue, cut to about
28 words.

## The list

```markdown
Participants: Arjun, Bea, Chen, Dami, Hardik

## Recognition moments (→ Kudos drafts)
- **Chen**, from Bea at 00:41: “Huge thanks to Chen for pairing on the flaky test yesterday.”

## Wins people reported (→ maybe a Kudos from you)
- **Dami** at 01:10: “The cache rollout went live this morning.”

## Possible feedback moments (private to you; check the facts first)
- **Arjun**, raised by Bea at 01:52: “Still waiting on the API review from Arjun.”

## Commitments (→ follow-up reminders)
- **You** at 02:30: “I'll send the plan by Friday.”
- Chen at 02:41: “I'll write up the runbook tomorrow.”

_1 line touching on personal matters was skipped and not analysed._

_Nothing has been sent. Approve each draft before it goes anywhere._
```

Write "none found" under any heading with nothing in it.
