# Team Story example

## q4-build-queue: the Platform team's quarter, told through everyone's work

- `story.json`: the headline, three chapters with each contributor's part,
  quotes, thanks to people on other teams, and a closing line
- `team-story.html` (not tracked; rebuild it with the command below) and
  `preview.jpg`: the one-page highlight reel, including a "who helped whom" map drawn from
  `../../spotlight/examples/q4-platform/evidence.jsonl`
- `wins-post.txt`: the #wins or all-hands channel version
- `slides-outline.md`: a slide-by-slide outline for an all-hands deck

```bash
python3 ../scripts/team_story.py q4-build-queue/story.json \
  --evidence ../../spotlight/examples/q4-platform/evidence.jsonl --out /tmp/team-story.html
```
