# Story Keeper example

## nani-stories: "Nani's Stories", three chapters for Diwali
- Cover, dedication, three chapters (story, pull quote, picture), closing words.
- Chapter 1 has a voice player with the words heard in the clip.
- `keepsake-preview.jpg` shows the whole booklet.

Everything here is a stand-in: Nani and the stories are fictional, the
pictures are drawn pencil sketches (labelled as such), and
`standin-voice.m4a` is a plain tone, not a voice, made by cutting a generated
test video with `extract_voice.py`. In real use the photos are the family's own
and the clip is the elder's real voice.

```bash
cd nani-stories
python3 ../../scripts/keepsake.py keepsake.json --out /tmp/nani.html --pdf /tmp/nani.pdf
python3 ../../../thankyou/scripts/safety_check.py keepsake.json --profile family
```
