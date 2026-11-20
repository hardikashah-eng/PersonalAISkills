# Text and share links for each channel

Prepare the channel-ready text yourself from `note.json`. Nothing here sends
anything: a share link only opens the app with the message filled in, and the
user taps send.

## The text

| Channel | Quote | Formatting | Soft length limit |
|---|---|---|---|
| Email, plain text | as plain lines: “quote”, translation, — attribution | full note | none; add a subject |
| WhatsApp | in underscores: _“quote”_ | `*bold*` item subjects | 130 words |
| Telegram, LINE, Signal, WeChat, KakaoTalk, Messenger | plain | plain | 130 words |
| Slack, Teams, Lark (DM) | as a `>` block quote | `*bold*` item subjects | 160 words |
| Slack, Teams, Lark (channel post) | none | the note's `channel_post`, signed "— Name" | 160 words |
| SMS, iMessage | none | the note's `short_body` if it has one | 60 words |
| LinkedIn | none | the `short_body`, or the `public_post` alone (no greeting, sign-off or P.S.) | 110 words |

Order of the text: quote; title (lists); greeting; paragraphs (or the short or
channel version); items as "✦ subject — why", with "↪ forward" under them;
closing and signature; the light moment with its link (not in SMS or
iMessage); "P.S. …" (not in SMS or iMessage).

A **note to a manager** (`manager_note`) is just its paragraphs and the
sender's first name.

**Email subject:** the note's `subject`, or the list's title for a gratitude
list, or "<Occasion>, <Name>", or "Thank you, <Name>".

When the text is over the channel's limit, write a shorter version that keeps
the specific moment (as `short_body`) and check it again
(`references/safety-checklist.md`). For chat apps, send the card image or the
clean photo with the text, unless the note is text only.

## Share links

Encode the text for a URL (percent-encode everything, including spaces and
line breaks):

| Channel | Link |
|---|---|
| WhatsApp | `https://wa.me/<digits>?text=<text>`, or `https://wa.me/?text=<text>` to pick the chat |
| SMS, iMessage | `sms:<number>?&body=<text>` |
| Email | `mailto:<address>?subject=<subject>&body=<text>` |
| Telegram | `https://t.me/share/url?url=&text=<text>` |
| LINE | `https://line.me/R/share?text=<text>` |

Signal, WeChat, KakaoTalk, Messenger, Slack, Teams, Lark and LinkedIn have no
link that fills in a message: give the text to copy and the image to attach.
For LinkedIn, the user opens the feed, selects "Start a post", and pastes.

A phone number or email address goes only into the link you show the user.
Never write it to a file or keep it. If a link is over about 2,000
characters, some apps cut it off, so give the text to copy instead.
