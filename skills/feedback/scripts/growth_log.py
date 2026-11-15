#!/usr/bin/env python3
"""A private growth log: strengths (from Kudos) and improvement opportunities
(from Feedback) for the people you support, ready for 1:1s and reviews.

Entries live in one JSON Lines file that the user chooses and keeps (a folder
on their computer, a private drive). Nothing is sent anywhere. Each entry is
checked with the safety check first, so health, money, personal-life and
labelling language never get stored.

  # add an improvement opportunity after feedback was shared
  python3 growth_log.py add --log team-growth.jsonl --person "Dami" --type growth \
      --area "communication" --observation "In the last two design reviews, the risks section came after the demo" \
      --impact "Reviewers raised the risks late, and the decision slipped a week" \
      --next "Lead with risks and the decision needed, then demo" --source feedback --shared --follow-up 2026-12-05

  # add a strength from a kudos note
  python3 growth_log.py add --log team-growth.jsonl --person "Bea" --type strength --area "reliability" \
      --observation "Found and fixed the retry storm in #482, with tests" --source kudos --shared

  python3 growth_log.py list --log team-growth.jsonl --person Dami --open
  python3 growth_log.py update --log team-growth.jsonl --id 3 --status done --note "Led with risks in the 12/3 review"
  python3 growth_log.py summary --log team-growth.jsonl --person Dami          # Markdown for a 1:1 or review
  python3 growth_log.py due --log team-growth.jsonl                            # follow-ups due this week
  python3 growth_log.py export --log team-growth.jsonl --csv growth.csv        # for Sheets, Lark Base, Excel
  python3 growth_log.py gaps --log team-growth.jsonl --team "Bea,Chen,Dami" --days 30 \
      --groups "Bea=Seattle,Chen=Shanghai,Dami=Seattle"                       # who hasn't been recognized lately
  python3 growth_log.py add --log team-growth.jsonl --person Chen --type sponsorship --area leadership \
      --observation "Nominated for the Q4 impact award" --source spotlight --shared
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "thankyou" / "scripts"))
from safety_check import scan  # noqa: E402

AREAS = ["delivery", "craft", "reliability", "communication", "collaboration", "ownership",
         "leadership", "mentoring", "customer focus", "learning", "other"]
STATUSES = ["open", "in progress", "done", "dropped"]


def load(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                sys.exit(f"{path}:{n} is not valid JSON; fix or remove that line")
    return rows


def save(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    tmp.replace(path)


def check_safe(entry: dict) -> None:
    text = [entry.get(k) for k in ("observation", "impact", "next", "note") if entry.get(k)]
    issues = scan({"body": text}, [], "feedback" if entry["type"] == "growth" else "default")
    blocking = [i for i in issues if i["level"] == "block"]
    if blocking:
        for i in blocking:
            print(f"✗ [{i['category']}] {i['match']!r}", file=sys.stderr)
        sys.exit("not saved: describe the behaviour and its effect, and leave out personal, health and money details")
    for i in issues:
        if i["level"] == "review" and not i["category"].startswith("feedback: add"):
            print(f"• check: [{i['category']}] {i['match']!r}", file=sys.stderr)


def cmd_add(a, rows: list[dict]) -> None:
    entry = {
        "id": max((r.get("id", 0) for r in rows), default=0) + 1,
        "date": a.date or dt.date.today().isoformat(),
        "person": a.person.strip(),
        "type": a.type,
        "area": a.area,
        "observation": a.observation.strip(),
        "impact": (a.impact or "").strip(),
        "next": (a.next or "").strip(),
        "source": a.source,
        "shared_with_person": bool(a.shared),
        "status": "open" if a.type in ("growth", "sponsorship") else "noted",
        "follow_up": a.follow_up or "",
        "history": [],
    }
    if a.type == "growth" and not entry["next"]:
        sys.exit("an improvement opportunity needs --next (what to try next)")
    check_safe(entry)
    rows.append(entry)
    print(f"added #{entry['id']}: {entry['type']} for {entry['person']} ({entry['area']})")
    if a.type == "sponsorship":
        print("note: update it with the outcome later (update --id N --status done --note \"…\")")
    if a.type == "growth" and not a.shared:
        print("note: share this with them directly; a growth log shouldn't hold anything they haven't heard from you")


def cmd_update(a, rows: list[dict]) -> None:
    for r in rows:
        if r.get("id") == a.id:
            if a.status:
                r["status"] = a.status
            if a.follow_up is not None:
                r["follow_up"] = a.follow_up
            if a.shared:
                r["shared_with_person"] = True
            if a.note:
                check_safe({"type": r["type"], "note": a.note})
            r.setdefault("history", []).append({"date": dt.date.today().isoformat(),
                                                "status": r.get("status"), "note": a.note or ""})
            print(f"updated #{r['id']}: {r['status']}")
            return
    sys.exit(f"no entry #{a.id}")


def select(rows, person=None, kind=None, open_only=False):
    out = rows
    if person:
        out = [r for r in out if r.get("person", "").lower() == person.lower()]
    if kind:
        out = [r for r in out if r.get("type") == kind]
    if open_only:
        out = [r for r in out if r.get("status") in ("open", "in progress")]
    return out


def cmd_list(a, rows) -> None:
    for r in select(rows, a.person, a.type, a.open):
        flag = "" if r.get("shared_with_person") else "  (not yet shared)"
        due = f"  follow up {r['follow_up']}" if r.get("follow_up") else ""
        print(f"#{r['id']} {r['date']} {r['person']} · {r['type']} · {r['area']} · {r['status']}{due}{flag}")
        print(f"    {r['observation']}")
        if r.get("next"):
            print(f"    → {r['next']}")


def cmd_due(a, rows) -> None:
    horizon = (dt.date.today() + dt.timedelta(days=a.days)).isoformat()
    due = [r for r in rows if r.get("follow_up") and r["follow_up"] <= horizon and r.get("status") in ("open", "in progress")]
    if not due:
        print(f"nothing due in the next {a.days} days")
    for r in sorted(due, key=lambda r: r["follow_up"]):
        print(f"{r['follow_up']}  #{r['id']} {r['person']}: {r['next']}")


def cmd_summary(a, rows) -> None:
    mine = select(rows, a.person)
    if a.since:
        mine = [r for r in mine if r["date"] >= a.since]
    if not mine:
        sys.exit(f"no entries for {a.person}")
    strengths = [r for r in mine if r["type"] == "strength"]
    growth = [r for r in mine if r["type"] == "growth"]
    out = [f"# {a.person}: strengths and growth" + (f" since {a.since}" if a.since else ""), ""]
    out += ["## What's going well", ""]
    for r in strengths or []:
        out.append(f"- **{r['area'].capitalize()}** ({r['date']}): {r['observation']}" + (f" {r['impact']}" if r.get("impact") else ""))
    if not strengths:
        out.append("- _No strengths logged yet. Add what's going well before the conversation._")
    sponsor = [r for r in mine if r["type"] == "sponsorship"]
    if sponsor:
        out += ["", "## Sponsorship (opportunities and nominations)", ""]
        for r in sponsor:
            outcome = "; ".join(h["note"] for h in r.get("history", []) if h.get("note"))
            out.append(f"- ({r['date']}, {r['status']}): {r['observation']}" + (f" Outcome: {outcome}" if outcome else ""))
    out += ["", "## Growth areas", ""]
    for r in growth:
        progress = "; ".join(h["note"] for h in r.get("history", []) if h.get("note"))
        out.append(f"- **{r['area'].capitalize()}** ({r['date']}, {r['status']}): {r['observation']}")
        if r.get("impact"):
            out.append(f"  - Effect: {r['impact']}")
        out.append(f"  - Next: {r['next']}")
        if progress:
            out.append(f"  - Progress: {progress}")
    if not growth:
        out.append("- _None logged._")
    def n(count, one, many):
        return f"{count} {one if count == 1 else many}"
    out += ["", f"_{n(len(strengths), 'strength', 'strengths')}, {n(len(growth), 'growth area', 'growth areas')} "
            f"({sum(r['status'] == 'done' for r in growth)} done)._"]
    if growth and len(strengths) < len(growth):
        out.append("_More growth notes than strengths: before the conversation, recall what's going well too._")
    unshared = [r for r in mine if not r.get("shared_with_person")]
    if unshared:
        out.append(f"_{len(unshared)} entr{'y has' if len(unshared) == 1 else 'ies have'} not been shared with {a.person} yet._")
    print("\n".join(out))


def cmd_gaps(a, rows) -> None:
    """Fairness check: who hasn't been recognized lately, and how recognition is spread across groups."""
    team = [t.strip() for t in a.team.split(",") if t.strip()]
    since = (dt.date.today() - dt.timedelta(days=a.days)).isoformat()
    recent = [r for r in rows if r["type"] in ("strength", "sponsorship") and r["date"] >= since]
    seen = {r["person"].lower() for r in recent}
    missing = [t for t in team if t.lower() not in seen]
    print(f"Recognition in the last {a.days} days ({len(recent)} strengths and sponsorship entries)\n")
    if missing:
        print("Not recognized lately: " + ", ".join(missing))
        print("  Look for their recent contributions (reviews, docs, on-call, helping others); "
              "quiet or remote work is easy to miss.\n")
    else:
        print("Everyone on the team has been recognized in this period.\n")
    if a.groups:
        group_of = {}
        for pair in a.groups.split(","):
            name, _, group = pair.partition("=")
            if name.strip():
                group_of[name.strip().lower()] = group.strip() or "unspecified"
        members, got = {}, {}
        for t in team:
            g = group_of.get(t.lower(), "unspecified")
            members[g] = members.get(g, 0) + 1
            got.setdefault(g, 0)
        for r in recent:
            g = group_of.get(r["person"].lower(), "unspecified")
            got[g] = got.get(g, 0) + 1
        total = max(len(recent), 1)
        print("Spread across groups (share of team → share of recognition):")
        for g in sorted(members):
            team_share = members[g] / max(len(team), 1)
            rec_share = got.get(g, 0) / total
            flag = "  ← lower than its share of the team" if rec_share + 0.15 < team_share else ""
            print(f"  {g}: {team_share:.0%} of the team → {rec_share:.0%} of recognition{flag}")


def cmd_export(a, rows) -> None:
    cols = ["id", "date", "person", "type", "area", "observation", "impact", "next", "source",
            "shared_with_person", "status", "follow_up"]
    with open(a.csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(select(rows, a.person))
    print(f"exported → {a.csv}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--log", type=Path, required=True, help="the JSON Lines file to keep the log in")
        return p

    p = common(sub.add_parser("add"))
    p.add_argument("--person", required=True)
    p.add_argument("--type", required=True, choices=["strength", "growth", "sponsorship"])
    p.add_argument("--area", default="other", choices=AREAS)
    p.add_argument("--observation", required=True, help="what you saw or heard, specifically")
    p.add_argument("--impact", help="what it affected")
    p.add_argument("--next", help="what to try next (required for growth)")
    p.add_argument("--source", default="manual", choices=["kudos", "feedback", "1:1", "review", "spotlight", "peer-pulse", "manual"])
    p.add_argument("--shared", action="store_true", help="already shared with the person")
    p.add_argument("--follow-up", help="YYYY-MM-DD to check in on progress")
    p.add_argument("--date")
    p = common(sub.add_parser("update"))
    p.add_argument("--id", type=int, required=True)
    p.add_argument("--status", choices=STATUSES)
    p.add_argument("--follow-up")
    p.add_argument("--shared", action="store_true")
    p.add_argument("--note", help="progress you saw")
    p = common(sub.add_parser("list"))
    p.add_argument("--person"); p.add_argument("--type", choices=["strength", "growth", "sponsorship"]); p.add_argument("--open", action="store_true")
    p = common(sub.add_parser("due"))
    p.add_argument("--days", type=int, default=7)
    p = common(sub.add_parser("summary"))
    p.add_argument("--person", required=True); p.add_argument("--since", help="YYYY-MM-DD")
    p = common(sub.add_parser("gaps"))
    p.add_argument("--team", required=True, help="comma-separated names")
    p.add_argument("--days", type=int, default=30)
    p.add_argument("--groups", help="optional Name=group pairs (location, time zone, role), comma-separated")
    p = common(sub.add_parser("export"))
    p.add_argument("--csv", required=True); p.add_argument("--person")
    a = ap.parse_args()

    rows = load(a.log)
    if a.cmd in ("add", "update"):
        {"add": cmd_add, "update": cmd_update}[a.cmd](a, rows)
        save(a.log, rows)
    else:
        {"list": cmd_list, "due": cmd_due, "summary": cmd_summary, "export": cmd_export,
         "gaps": cmd_gaps}[a.cmd](a, rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
