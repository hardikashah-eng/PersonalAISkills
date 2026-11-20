# Delivering the note

Shared by ThankYou and Reconnect. Once the note is final and has passed the
safety check, help the user get it to the person on the channel that suits
them both.

## The sending rule

**Nothing is sent without an explicit "yes, send it" for that exact message.**

Before any send or post, show the user a preview and wait for a clear yes:

> **Ready to send?**
> **To:** Maya (email)  ·  **Subject:** Thank you, Maya
> **Message:** (the final text, in full)
> **Attachments:** card.png, photo.jpg
> Reply **send** to send it now, or tell me what to change. I can also leave it as a draft.

- One confirmation covers one message to one recipient or channel. A team
  thank-you posted to a channel needs a yes that names the channel.
  Several notes need a yes for each note, or the user can approve a list that
  shows every recipient and message in full.
- "Looks good" about the wording is not a yes to send. Ask.
- **Default is a draft**: if the user hasn't said "send", create a draft (where
  the connector supports drafts) or give them the ready-to-send text and link.
- Never send on a schedule unattended. If the user wants it to go out on the
  day (Thanksgiving morning, say), offer a reminder for them to send it, or a
  draft they can schedule in their own email app.
- Never send to anyone other than the person or group the note is for, never
  CC or BCC others unless the user asks, and never post a personal note in a
  group or channel unless the user picks that group.
- Contact details (email addresses, phone numbers, handles) are used only for
  the send itself. They never go into `note.json`, the card, or any saved file.

## Choosing the channel

1. **The user says**: "send it on WhatsApp", "email it", "post in #platform".
2. **Where they actually talk**: the channel where the moment was found, or
   where most of their exchanges with this person happen.
3. **By relationship** if still unclear:

| Relationship | Usually |
|---|---|
| Family, close friends | WhatsApp, iMessage/SMS, Signal, Telegram, WeChat, LINE, KakaoTalk (whatever the family uses) |
| Colleague, manager, report | Slack, Microsoft Teams, Lark/Feishu DM, or email |
| Team (`--team`) | the team's channel, plus the printed card in the team space |
| Organization (`--org`) | email to their general or relevant contact, or a printed card |
| Mentor, teacher, former colleague | email or LinkedIn message |
| Anyone, for a keepsake | printed card (print the HTML on card stock) |

Ask once if it's still unclear: "How would you like to send this: WhatsApp,
text, email, Slack, or a printed card?"

## Two ways to deliver

### A. Through a connected app (can send, after a yes)

Check which connectors this session has, and use the one for the chosen channel:

| Channel | Typical connector | What to do |
|---|---|---|
| Email | Gmail, Outlook (Microsoft 365) | Create a draft with subject, body, card image inline or attached, and the clean photo attached. After a yes, send the draft. |
| Slack | Slack | DM the person, or post in the channel the user named (team notes). Upload the card or photo if the connector supports files. |
| Microsoft Teams | Microsoft 365 / Teams | Chat message or channel post, same as Slack. |
| Lark / Feishu | Lark | Same as Slack. |
| LinkedIn | LinkedIn (if connected) | A message to a connection, text only (50–100 words). |
| WhatsApp, Telegram, other messengers | only if a connector for that app exists in the session | Same rules. |

If the connector can only read, or the send fails, fall back to B.

### B. Ready-to-send (no connector needed)

Give the user everything to send it themselves in a couple of taps:
- **The text formatted for the channel** (see below).
- **The card as an image** (`card.png`), since messaging apps show images, not
  HTML (`references/images.md`).
- **The clean photo**, if there is one, with its metadata removed.
- **A share link** that opens the app with the message filled in
  (`references/channel-formats.md`).

| Channel | Share link | Notes |
|---|---|---|
| WhatsApp | `https://wa.me/?text=…` | Opens WhatsApp and lets the user pick the chat. With a number the user gives, opens that chat directly. |
| SMS / iMessage | `sms:?&body=…` | Opens Messages. With a number the user gives, addressed to it. |
| Email (any app) | `mailto:?subject=…&body=…` | With an address the user gives, addressed. Attach the card and photo by hand. |
| Telegram | `https://t.me/share/url?url=&text=…` | Pick the chat in Telegram. |
| LINE | `https://line.me/R/share?text=…` | Pick the chat in LINE. |
| Signal, WeChat, KakaoTalk, Messenger, LinkedIn | none | Copy the text and attach the card image. |

Links carry only the message text. A phone number or address is added only if
the user gives it for this send, and it is never written to a file.

## Formatting by channel

| Channel | Length | Format |
|---|---|---|
| Printed card | whole note | the rendered card |
| Email | whole note | subject line ("Thank you, Maya", "Happy Diwali, Sharma Sir"), plain text body including the quote, card inline or attached |
| Slack / Teams / Lark | 80–150 words for a team post; whole note for a DM | plain text, no card formatting, card or photo attached |
| WhatsApp / Telegram / Signal / LINE | under about 120 words | the photo or card image first, then the text; one emoji at most if that's their style |
| SMS / iMessage | under about 60 words | short version; send the card image after |
| LinkedIn | 50–100 words | warm-professional, text only |

Make the channel version with `references/channel-formats.md`: drop the
card-only parts for short channels (the quote attribution layout, extra blank
lines), add a subject for email, and shorten the text when it's long for the
channel. For SMS and chat, write a shorter version by hand. Keep the
specific moment, as it's the heart of the note.

## After delivering

Tell the user, in one line, what happened: "Sent to Maya by email." or "Draft
is in your Outlook Drafts." or "WhatsApp link ready: tap it, pick Arjun, and
attach card.png." Don't save the message, contact, or delivery record anywhere.
