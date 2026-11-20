# ThankYou examples

All people are fictional. Photos are illustrated stand-ins, and sketches are
drawn by the skill. The skill draws artwork and sketches as SVG; here they are
saved as PNG images (`art.png`, `sketch.png`) next to the finished `card.png`.

| Example | Mode | Picture | Shows |
|---|---|---|---|
| `maya-thanksgiving/` | individual (mentor) | own photo (whiteboard), metadata stripped | the specific moment, paying it forward, quote, art |
| `sharma-sir-diwali/` | individual (teacher, elder) | none | bilingual Hindi/English, honorifics, Kabir couplet |
| `platform-team-thanksgiving/` | `--team` | drawn pencil sketch | shared achievement, names no one (roster check), paying it forward |
| `family-navidad/` | `--family` | drawn pencil sketch | Spanish at home, one picture of a lifetime, paying it forward to the next generation |

## `--team` example: the channel-ready version

Alongside the card, team notes come with a version for the team channel, with
the sketch or team photo to attach. The user posts it; the skill never does.

> Happy Thanksgiving, team. In the spring we set a goal that sounded a little unreasonable: every simulation run on the new farm by year's end, without stopping anyone's work. We got there in October, and test runs that took a week now finish the same afternoon. That came from late nights nobody asked for, careful reviews, and the habit you kept no matter what: no one debugs alone. Three other teams now build on what you made, and I'm taking that habit everywhere I go. Grateful for every one of you who touched this, on-site and remote. 🧡

Checks run (`references/safety-checklist.md`):

- Platform team: every-note checks plus the team and org checks. The roster
  (Ana, Ben, Chen, Dev, Elena, Farid) comes from note.json: nobody is named,
  so nobody is left out.
- Family: every-note checks plus the family checks.

## How the pictures were made

- **Maya:** the user's own photo, chosen by the user, with its GPS and camera
  data removed before it went in the card (`references/images.md`).
- **Platform team, family:** no suitable photo, so the skill drew a pencil
  sketch of the scene (`sketch.svg`, see `references/sketch.md`). Their
  captions describe the scene, not "us", because a sketch isn't a photo of
  the moment.
- A freely licensed stock photo can also be turned into a sketch, when an
  image tool is available (`references/sketch.md`).

## Delivery

Each note can go out on the channel that fits (`references/delivery.md`).
Nothing is sent without an explicit yes to the exact message.

| Example | Channel | How |
|---|---|---|
| Maya | email | subject "Thank you, Maya", full note; with Outlook or Gmail connected, a draft with `card.png` and the photo attached, sent only after "send" |
| Platform team | Slack | the note's `channel_post`; posted to the channel the user names, only after a yes that names the channel |
| Family | WhatsApp | the card as an image, then a `wa.me` link with the text filled in; the user picks the family chat and sends |
| Sharma Sir | printed card | print the card's HTML on card stock (A5 or 5×7) |

Text and links come from `references/channel-formats.md`, the card from
`references/card-layout.md`, and the card image from `references/images.md`.
