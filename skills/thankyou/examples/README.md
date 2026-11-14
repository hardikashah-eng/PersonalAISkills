# ThankYou examples

All people are fictional. Photos are illustrated stand-ins, and sketches are
drawn by the skill.

| Example | Mode | Picture | Shows |
|---|---|---|---|
| `maya-thanksgiving/` | individual (mentor) | own photo (whiteboard), metadata stripped | the specific moment, paying it forward, quote, art |
| `sharma-sir-diwali/` | individual (teacher, elder) | none | bilingual Hindi/English, honorifics, Kabir couplet |
| `platform-team-thanksgiving/` | `--team` | drawn pencil sketch | shared achievement, names no one (`--roster` check), paying it forward |
| `family-navidad/` | `--family` | drawn pencil sketch | Spanish at home, one picture of a lifetime, paying it forward to the next generation |

## `--team` example: the channel-ready version

Alongside the card, team notes come with a version for the team channel, with
the sketch or team photo to attach. The user posts it; the skill never does.

> Happy Thanksgiving, team. In the spring we set a goal that sounded a little unreasonable: every simulation run on the new farm by year's end, without stopping anyone's work. We got there in October, and test runs that took a week now finish the same afternoon. That came from late nights nobody asked for, careful reviews, and the habit you kept no matter what: no one debugs alone. Three other teams now build on what you made, and I'm taking that habit everywhere I go. Grateful for every one of you who touched this, on-site and remote. 🧡

Checks run:

```bash
python3 scripts/safety_check.py examples/platform-team-thanksgiving/note.json --profile team
# roster (Ana, Ben, Chen, Dev, Elena, Farid) comes from note.json: nobody is named, so nobody is left out
python3 scripts/safety_check.py examples/family-navidad/note.json --profile family
```

## How the pictures were made

- **Maya:** the user's own photo, chosen by the user. `render_card.py --photo`
  stripped its GPS and camera data.
- **Platform team, family:** no suitable photo, so the skill drew a pencil
  sketch of the scene (`sketch.svg`, see `references/sketch.md`). Their
  captions describe the scene, not "us", because a sketch isn't a photo of
  the moment.
- A freely licensed stock photo can also be turned into a sketch:
  `python3 scripts/sketch_photo.py stock.jpg --out sketch.jpg`.

## Delivery

Each note can go out on the channel that fits (`references/delivery.md`).
Nothing is sent without an explicit yes to the exact message.

| Example | Channel | How |
|---|---|---|
| Maya | email | `share.py --channel email`: subject "Thank you, Maya", full note; with Outlook or Gmail connected, a draft with `card.png` and the photo attached, sent only after "send" |
| Platform team | Slack | `share.py --channel slack` uses `channel_post`; posted to the channel the user names, only after a yes that names the channel |
| Family | WhatsApp | `card_to_png.py` for the image, then `share.py --channel whatsapp` for a `wa.me` link with the text filled in; the user picks the family chat and sends |
| Sharma Sir | printed card | print `card.html` on card stock (A5 or 5×7) |

```bash
python3 scripts/render_card.py examples/family-navidad/note.json --art examples/family-navidad/art.svg \
  --photo examples/family-navidad/sketch.svg --out /tmp/navidad.html
python3 scripts/card_to_png.py /tmp/navidad.html --out /tmp/navidad.png
python3 scripts/share.py examples/family-navidad/note.json --channel whatsapp
```
