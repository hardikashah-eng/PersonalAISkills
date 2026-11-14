# PersonalAISkills

Small, careful AI skills for human connection. They use AI to help people show
up better for each other, not to stand in for them.

![A sample ThankYou card: a Thanksgiving note to a mentor](skills/thankyou/examples/maya-thanksgiving/card.png)

## Skills

| Skill | What it does | Try saying |
|---|---|---|
| [ThankYou](skills/thankyou/SKILL.md) | A one-of-one thank-you note for any occasion, to a person, a team (`--team`), an organization (`--org`), or family (`--family`). It opens with a fitting, correctly attributed quote, recalls the specific moment or shared achievement that made a real difference, uses your native language where it fits, can show how you are paying it forward, and adds a small artwork drawn only for them plus a photo from a good time together, or a pencil sketch of the moment when there is no photo. The card is written in handwriting. | "Write a Thanksgiving thank-you note to my mentor Maya" or "/thankyou --team Platform Thanksgiving" |
| [Reconnect](skills/reconnect/SKILL.md) | Finds people you've drifted from, and quietly leaves alone the ones you drifted from on purpose. Then it drafts a short, no-guilt check-in built on a real shared memory (often a photo from that time), a festival they celebrate, or a "thought of you" moment. | "Who have I lost touch with?" or "Help me reconnect with Arjun" |

## Install

In Claude, add **PersonalAISkills** from the plugin directory (Customize → Plugins),
once it is listed there. In Claude Code you can install it straight from GitHub:

```
/plugin install personalaiskills --marketplace hardikashah-eng/personalaiskills
```

The skills work best with your email or chat connected to Claude. They also
work without any connectors: Claude asks you a few short questions instead.

## Principles

- **Specific over generic.** Find the real moment, not a template.
- **Private by default.** Personal connectors are read-only and used only with
  permission, and nothing sensitive ends up in the output.
- **Kind always.** Tone fits the relationship (spouse, parent, elder, sibling,
  friend, mentor, colleague…) and the recipient's culture, and the skills steer
  around topics that could hurt.
- **The human sends.** The skills draft; you review, edit, and send.

## Privacy and data handling

This plugin contains only skills (instructions and three small helper scripts).
It has no hooks, no MCP servers, no package installs, and makes no network
requests of its own.

**What it reads.** To find a real moment to mention, Claude may search the
communication tools *you have already connected* to Claude, such as email,
Slack, Microsoft Teams, Lark/Feishu, LinkedIn and calendar. It reads only what
it needs about the one person you're writing to. WhatsApp and SMS/iMessage are
read only after you explicitly allow it for that note, and only your 1:1 thread
with that person. Claude shows you a one-line summary of the moment it found
and uses it only after you confirm.

**Photos.** A note can include a photo from a good time you shared. Photos
come only from your own sources: a photo library or drive you've connected, a
photo you attach, or photos the two of you already exchanged (WhatsApp and SMS
with the same opt-in as above). Claude finds candidates by the date, album or
thread of the moment, never by recognising faces, and never takes photos from
the web, social media or profile pictures. You choose the photo. Claude never
retouches, alters or generates a person. Before a photo goes into a card or
draft, its hidden data (GPS location, camera details, timestamps) is removed.
Cards with personal photos are kept as files or drafts, not shareable links,
unless you ask.

**Pencil sketches and stock photos.** When there is no suitable photo, Claude
draws an original pencil-style sketch of the scene, with no faces or
likenesses of real people. If you'd like something closer to a photograph,
Claude may instead look up a freely licensed stock photo of a place or object
(public domain, CC0, or a free-to-use licence such as Unsplash's or Pexels'),
using Claude's own web tools, and turn it into a pencil sketch. It never uses
photos of people, public figures or anything from social media, and it credits
the author when the licence asks. A sketch or stock image is never described
as a real photo of your moment.

**What it never does.** It never sends, posts, replies, or reacts on your behalf.
It creates an email draft only when you ask for one. It does not store your
messages, contacts or notes anywhere, including memory, and it sends no data
to any third party.

**What stays out of every note.** Contact details, addresses, ID or account
numbers, money amounts and other financial details, and health information.
Moments that involve these are rewritten in general terms ("you stepped in
when I needed it most"). Reconnect never suggests people from a conflict, exes,
estranged family, or anyone who may have passed away.

**What runs on your machine.** When a skill is used in an environment that can
run code, Claude may run three Python 3 scripts (no network access):

- `skills/thankyou/scripts/safety_check.py` reads a draft note (JSON) and
  flags contact details, money amounts, financial and health terms, topics to
  avoid, and harsh or guilt-inducing wording, including in a photo's caption
  and alt text. It prints a report and writes nothing.
- `skills/thankyou/scripts/render_card.py` turns a note, an optional SVG
  drawing and an optional photo into a self-contained HTML card file at the
  path you choose. It strips scripts and external links from the SVG and all
  metadata from the photo, and can save the cleaned photo for you to attach.
  It uses the standard library only; if Pillow is already installed it also
  turns photos upright and shrinks them to at most 1200 px. It can also embed a drawn
  pencil-sketch SVG, with scripts and external links removed.
- `skills/thankyou/scripts/sketch_photo.py` turns a freely licensed stock
  photo into a graphite pencil sketch and removes its metadata. It needs
  Pillow; without Pillow, Claude draws the sketch as an SVG instead.

Where scripts can't run, the skills do the same checks by hand.

**Fonts.** Cards are written in a handwriting font by default. Caveat and Kalam
are bundled in `skills/thankyou/assets/fonts/` under the SIL Open Font License
1.1 (licence files included) and embedded in each card, so nothing is fetched
when a card opens.

All people in `examples/` are fictional, the example photos are illustrated
stand-ins, and the sketches were drawn by the skill.

## Layout

```
.claude-plugin/plugin.json   # plugin manifest
skills/<name>/
  SKILL.md                   # instructions Claude follows
  references/                # detailed guidance loaded on demand
  scripts/                   # helper scripts (ThankYou; shared with Reconnect)
  examples/                  # finished samples
```

Reconnect reuses ThankYou's safety check (`--profile reconnect`), card
renderer, and its language, art, relationship and culture guides.

## Try the scripts locally

```bash
cd skills/thankyou
python3 scripts/safety_check.py examples/maya-thanksgiving/note.json
python3 scripts/render_card.py examples/maya-thanksgiving/note.json \
  --art examples/maya-thanksgiving/art.svg --out /tmp/maya.html
```

Requires Python 3.9 or later; no dependencies.

## License

[MIT](LICENSE)
