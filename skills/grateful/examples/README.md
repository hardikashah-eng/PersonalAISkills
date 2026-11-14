# Grateful examples

All people are fictional. The sketches were drawn by the skill.

| Example | Language | Visibility | Shows |
|---|---|---|---|
| `thanksgiving-2026/` | English | family | a person, the people at work, and an ordinary thing, each with the difference it made and a pay-it-forward (two already happening, one a plan); sketch of the feeling (tea by an autumn window) |
| `diwali-2026-hindi/` | Hindi | family | the whole list in Hindi, a Sanskrit subhashita about living for others, and a sketch of the occasion (five diyas on the doorstep) |

```bash
cd skills/grateful
python3 ../thankyou/scripts/safety_check.py examples/thanksgiving-2026/grateful.json --profile grateful
python3 ../thankyou/scripts/render_card.py examples/thanksgiving-2026/grateful.json \
  --art examples/thanksgiving-2026/sketch.svg --out /tmp/grateful.html
python3 ../thankyou/scripts/card_to_png.py /tmp/grateful.html --out /tmp/grateful.png
python3 ../thankyou/scripts/share.py examples/thanksgiving-2026/grateful.json --channel whatsapp
```

Safe reasons in practice: "a heavy year" stands in for whatever made it heavy,
and the people are "my sister" and "the people I get to work with", without
details of their lives.
