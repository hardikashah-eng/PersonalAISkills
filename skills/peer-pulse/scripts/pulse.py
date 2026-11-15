#!/usr/bin/env python3
"""Peer Pulse: a two-question weekly prompt ("Who helped you this week, and how?")
and a tally that turns the answers into thank-you drafts and Spotlight evidence.

  # the message the organizer posts (or sends as a form)
  python3 pulse.py prompt --team "Platform" --due "Friday 4 pm" --channel slack

  # after the answers are in (CSV or JSON: date, from, helped, how, share)
  python3 pulse.py tally answers.csv --team "Bea,Chen,Dami,Ola,Kenji,Arjun" \
      --drafts drafts/ --evidence evidence.jsonl --organizer "Hardik"

`share` is each writer's choice: yes (name me), anonymous (say "a teammate"),
or private (only the organizer sees it; no thank-you is drafted). Every answer
is safety-checked; anything flagged goes to the organizer instead of a draft.
Runs locally; nothing is posted or sent.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "thankyou" / "scripts"))
from safety_check import scan  # noqa: E402

PERSONAL = re.compile(
    r"\b(sick|ill|illness|doctor|hospital|surgery|therapy|medical|medication|diagnos\w*|pregnan\w*|maternity|"
    r"paternity|funeral|passed away|bereavement|divorce|family emergency|mental health|burn(?:ed|t)?\s?out|"
    r"anxiety|depress\w*|visa|salary|raise|layoff|fired)\b", re.I)

PROMPTS = {
    "slack": ("🙌 *Peer Pulse* for {team}: two quick questions, one minute.\n\n"
              "1️⃣ Who helped you this week?\n2️⃣ How did it help?\n\n"
              "Reply to me directly (not in the channel) by {due}. Tell me if I can name you when I pass "
              "it on (yes / anonymous / just for me). Small things count: a review, an answer, a pairing session."),
    "plain": ("Peer Pulse for {team}: two quick questions.\n\n"
              "1. Who helped you this week?\n2. How did it help?\n\n"
              "Reply to me directly by {due}, and say whether I can name you when I pass it on "
              "(yes / anonymous / just for me). Small things count."),
}
PROMPTS["lark"] = PROMPTS["teams"] = PROMPTS["slack"].replace("*Peer Pulse*", "**Peer Pulse**")
PROMPTS["email"] = PROMPTS["whatsapp"] = PROMPTS["plain"]


def load_answers(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        rows = json.loads(text)
    else:
        rows = list(csv.DictReader(text.splitlines()))
    out = []
    for r in rows:
        r = {k.strip().lower(): (v or "").strip() for k, v in r.items()}
        if not (r.get("helped") and r.get("how")):
            continue
        share = r.get("share", "private").lower()
        r["share"] = "yes" if share in ("yes", "y", "ok", "name me") else "anonymous" if share.startswith("anon") else "private"
        r["date"] = r.get("date") or dt.date.today().isoformat()
        out.append(r)
    return out


def canonical(name: str, team: list[str]) -> tuple[str, bool]:
    for t in team:
        if name.lower() == t.lower() or name.split()[0].lower() == t.split()[0].lower():
            return t, True
    return name, False


def tally(rows: list[dict], team: list[str]):
    by_person = defaultdict(list)
    held = []
    for r in rows:
        helped_names = [n.strip() for n in re.split(r",|&| and ", r["helped"]) if n.strip()]
        issues = [i for i in scan({"body": [r["how"]]}, [], "team") if i["level"] == "block"]
        if PERSONAL.search(r["how"]):
            issues.append({"category": "personal detail"})
        for n in helped_names:
            name, on_team = canonical(n, team)
            item = {**r, "helped": name, "on_team": on_team}
            (held if issues else by_person[name]).append(item)
    return by_person, held


def draft(name: str, items: list[dict], organizer: str) -> dict:
    shared = [it for it in items if it["share"] != "private"]
    if not shared:
        return {}
    count = "Someone" if len(shared) == 1 else f"{len(shared)} people"
    quotes = []
    for it in shared:
        who = it.get("from") if it["share"] == "yes" and it.get("from") else "a teammate"
        quotes.append(f"{who}: \"{it['how'].rstrip('.')}.\"")
    body = [f"{count} mentioned you in this week's Peer Pulse. " + " ".join(quotes),
            "Thank you for making the team better. It was noticed."]
    return {"kind": "kudos", "text_only": True, "audience": "individual", "recipient_first_name": name,
            "sender_first_name": organizer, "source": "Peer Pulse", "greeting": f"{name},",
            "body": body, "closing": "", "signature": organizer}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prompt")
    p.add_argument("--team", default="the team")
    p.add_argument("--due", default="Friday 4 pm")
    p.add_argument("--channel", default="slack", choices=sorted(PROMPTS))
    t = sub.add_parser("tally")
    t.add_argument("answers", type=Path)
    t.add_argument("--team", required=True, help="comma-separated first names")
    t.add_argument("--organizer", default="")
    t.add_argument("--drafts", type=Path, help="folder for one Kudos note.json per person thanked")
    t.add_argument("--evidence", type=Path, help="Spotlight evidence.jsonl to append to")
    a = ap.parse_args()

    if a.cmd == "prompt":
        print(PROMPTS[a.channel].format(team=a.team, due=a.due))
        return 0

    team = [x.strip() for x in a.team.split(",") if x.strip()]
    rows = load_answers(a.answers)
    by_person, held = tally(rows, team)
    print(f"Peer Pulse: {len(rows)} answers, {sum(len(v) for v in by_person.values())} thank-yous\n")
    for name in sorted(by_person):
        items = by_person[name]
        tag = "" if items[0]["on_team"] else " (another team)"
        print(f"## {name}{tag}")
        for it in items:
            who = it.get("from") or "?"
            note = {"yes": "", "anonymous": "  [anonymous]", "private": "  [just for you]"}[it["share"]]
            print(f"- from {who}: {it['how']}{note}")
        print()
    quiet = [m for m in team if m not in by_person]
    if quiet:
        print("Not mentioned this week (for your awareness only; often just a quiet week): " + ", ".join(quiet) + "\n")
    if held:
        print("Held for you to read in the original (personal or sensitive; no draft, not stored):")
        for it in held:
            print(f"- {it.get('from', '?')} about {it['helped']}")
        print()
    if a.drafts:
        a.drafts.mkdir(parents=True, exist_ok=True)
        made = 0
        for name, items in by_person.items():
            d = draft(name, items, a.organizer)
            if d:
                (a.drafts / f"kudos-{name.split()[0].lower()}.json").write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
                made += 1
        print(f"{made} Kudos draft(s) → {a.drafts}/ (review each before sending)")
    if a.evidence:
        lines = [{"date": it["date"], "person": name, "kind": "peer-thanks" if it["on_team"] else "cross-team-help",
                  "from": (it.get("from") if it["share"] == "yes" else "a teammate") or "a teammate",
                  "source": "peer-pulse",
                  "summary": it["how"] if it["share"] != "private" else "Thanked privately in Peer Pulse (not for quoting)",
                  "link": "", "beyond_role": False, "cross_team": not it["on_team"]}
                 for name, items in by_person.items() for it in items]
        with a.evidence.open("a", encoding="utf-8") as fh:
            for line in lines:
                fh.write(json.dumps(line, ensure_ascii=False) + "\n")
        print(f"{len(lines)} moment(s) added to {a.evidence} for Spotlight")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
