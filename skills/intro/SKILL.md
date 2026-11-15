---
name: intro
description: Make warm, double opt-in introductions between two people who should know each other, such as a new hire and an expert, two engineers solving the same problem on different teams, a mentor and mentee, or a job seeker and someone hiring, by writing a short private ask to each person first and, only once both say yes, an introduction that says who each is, why they should meet and one easy next step. Shares no contact details until both agree. Use when the user wants to introduce, connect or refer two people.
argument-hint: "[person A] [person B] [why] [via email|slack|lark|teams|whatsapp|linkedin]"
---

# Intro

A good introduction can change someone's year: the right mentor, the person
who already solved your problem, the hiring manager who needed exactly you.
A bad one lands as an unwanted obligation. This skill makes introductions the
considerate way: ask each person first, then connect them with a clear reason
and an easy first step.

## Non-negotiables

1. **Double opt-in.** Ask each person privately before introducing them. If
   either says no or doesn't answer, there's no intro, and no one is told why.
2. **No contact details until both agree.** Never share an email, phone number
   or handle in the ask; only in the intro, after both said yes.
3. **A real, specific reason.** "You both work on X" isn't enough; say what
   each can offer or learn ("Ola built the NPU compiler's tiling pass; Chen is
   about to optimize the same kernels").
4. **Light on their time.** Suggest one small next step (a 20-minute call, a
   doc to read), and make it easy to say no.
5. **Honest and kind.** Don't oversell either person. Keep personal details
   out (`../thankyou/references/safety.md`). For job referrals, say only what
   you can vouch for.
6. **Send only on an explicit yes** from the user, at each step.

## Workflow

### 1. Understand the match

- **Who** the two people are and how the user knows each one.
- **Why they should meet**: what each can give and get. Look at the specific
  things the user points to (a design doc, a talk, a repo, a profile) through
  connectors to get it right.
- **Channel**: email for people outside the company, a DM or a small group
  chat inside it, LinkedIn for professional contacts the user knows there.

### 2. Ask each person first (`invite`)

A private message to each, 40–80 words: who the other person is, why the
user thought of them, what it would involve, and an easy out:

> Hi Ola, would you be open to a short intro to Chen, who just joined the
> kernels team? He's about to optimize the same conv kernels your tiling pass
> handles, and I think 20 minutes with you would save him weeks. Totally fine
> to say no if your plate's full.

Ask the busier or more senior person first; then the other.

### 3. The introduction (`body`), once both said yes

60–120 words, to both together (an email with both on "To", a group DM):

1. One line each: who they are, in a way that makes the other want to meet.
2. Why now: the specific overlap.
3. One easy next step ("Chen, maybe you could suggest a time?").
4. The user steps back ("I'll let you two take it from here").

### 4. Check, deliver, follow up

```bash
python3 ../thankyou/scripts/safety_check.py note.json
python3 ../thankyou/scripts/share.py note.json --channel email
```

Send only on the user's yes. Offer one gentle reminder to the user (not to
them) in two weeks: "Did Chen and Ola connect?"

## note.json

```json
{
  "kind": "intro",
  "people": [{"name": "Ola", "why_them": "…"}, {"name": "Chen", "why_them": "…"}],
  "invite": [{"to": "Ola", "text": "…"}, {"to": "Chen", "text": "…"}],
  "opted_in": {"Ola": true, "Chen": true},
  "greeting": "Ola, meet Chen. Chen, meet Ola.",
  "body": ["…"],
  "subject": "Intro: Ola <> Chen (conv kernels)"
}
```

Don't write or send the `body` until `opted_in` is true for both.

## Files

- `references/intro-patterns.md`: kinds of introductions, asks and intros that work, what to avoid
- `examples/chen-meets-ola/`: a new hire meets the engineer who built the part he's about to change
