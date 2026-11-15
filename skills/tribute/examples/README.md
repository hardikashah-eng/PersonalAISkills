# Tribute example

## meena-farewell: the Platform team says goodbye to its tech lead
- Five contributions, each credited, with hand-drawn star marks.
- Opening quote (Aesop), the organizer's two-line intro, a drawn whiteboard
  sketch, and a team signature.
- A light moment: Buster Keaton's *One Week* (1920), a public-domain short on
  Wikimedia Commons, for her first week in a new place.
- A P.S. fun fact about ibises sharing the lead.

```bash
python3 ../../thankyou/scripts/safety_check.py meena-farewell/note.json --profile team --roster "Arjun,Bea,Chen,Dami,Hardik"
python3 ../../thankyou/scripts/render_card.py meena-farewell/note.json --art meena-farewell/art.svg --photo meena-farewell/sketch.svg --out /tmp/meena.html
```
