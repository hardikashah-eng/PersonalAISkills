# personalaiskills

Small, careful AI skills for human connection. They use AI to help people show
up better for each other, not to stand in for them.

Each skill follows the same principles:

- **Specific over generic.** Find the real moment, not a template.
- **Private by default.** Personal connectors (email, chat, WhatsApp, SMS…) are
  read-only, used only with permission, and nothing sensitive ends up in the output.
- **Kind always.** Tone fits the relationship and the recipient's culture, and
  the skill steers around topics that could hurt.
- **The human sends.** Skills draft; people review, edit, and send.

## Skills

| Skill | What it does |
|---|---|
| [ThankYou](skills/thankyou/SKILL.md) | A one-of-one thank-you note for any occasion: an opening quote, the specific moment the person made a difference (found in your connectors with your permission), your native language where it fits, and a small artwork made only for them. |

## Layout

```
skills/<name>/
  SKILL.md        # instructions the agent follows
  references/     # detailed guidance loaded on demand
  scripts/        # deterministic helpers (safety checks, renderers)
  examples/       # finished samples
```

## Try ThankYou locally

```bash
cd skills/thankyou
python3 scripts/safety_check.py examples/maya-thanksgiving/note.json
python3 scripts/render_card.py examples/maya-thanksgiving/note.json \
  --art examples/maya-thanksgiving/art.svg --out /tmp/maya.html
```

Requires Python 3.9+, no dependencies.
