# Roadmap

## Next: occasions, recipient lists, and sending in batches

Wire the skills to occasions on the calendar (Thanksgiving, Christmas, Diwali,
Lunar New Year, Eid, New Year, birthdays, work anniversaries) and to a list of
people, so the user can thank or reconnect with many people at once.

### Occasions
- A scheduled task per occasion, set up with the user. For example, a week
  before Thanksgiving: "prepare thank-you notes for my list".
- It runs ahead of the day and **prepares** everything: notes, cards, images
  and channel versions. It doesn't send anything.
- The scheduled run sends the user one message, such as "Your 12 Thanksgiving
  notes are ready to review".
- Occasion dates come from the user's calendar or a small built-in table, and
  only for holidays the user says they celebrate.

### Recipient lists
- Built **with** the user, from sources they connect and allow: phone
  contacts, WhatsApp, Slack or Teams workspace members, email contacts, a
  LinkedIn connections export, or a list they paste or attach (CSV or sheet).
- Each person on the list gets their own note. The usual pipeline finds their
  moment, relationship, language and channel, and runs the safety check, so
  there are no copy-paste templates.
- Reconnect's "leave alone" rules apply to the whole list: no conflicts, exes,
  estranged family, or anyone who may have passed away.
- The list holds names and channels. Contact details stay in the source app
  and are used only at send time, never written to the repo or memory.

### Sending in batches ("bulk send"), the safe way
- A review screen shows **every** message in full: recipient, channel, text,
  attachments, and the safety-check status.
- The user can approve all, approve some, or edit any. Approving a reviewed
  list counts as the explicit yes the delivery rule requires
  (`skills/thankyou/references/delivery.md`).
- Sending runs only from that live approval, never unattended from a schedule.
- Messages go out one at a time through each recipient's own channel
  (connectors where available, share links otherwise), with a per-message
  result ("sent", "draft", "link ready", "failed").
- Rate limits and app rules are respected: no mass messaging that apps treat as
  spam, and an option to spread sends over the day.
- Messages with an unresolved safety flag never go out in a batch; they wait
  for individual review.

### Open questions
- Which contact sources are available as connectors on each platform, and
  which need an export?
- How to show a long review list comfortably: a Sheets or Dashboard artifact,
  or a chat-based review?
- Per-person opt-outs ("don't include Sam in holiday batches").

## Later
- Comfort: messages for someone grieving, ill, or going through a hard time
  (reuses the triggers and kindness rules).
- Tribute: farewell cards, retirement tributes and toasts, with contributions
  from many people.
- Kudos: specific recognition at work, grounded in the actual work.
- Move shared pieces into `skills/_core/`.
