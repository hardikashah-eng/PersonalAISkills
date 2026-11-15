#!/usr/bin/env python3
"""Find people who consistently go above and beyond, from evidence over weeks,
and build an evidence-backed impact story for them.

Evidence lives in a JSON Lines file the user keeps (one line per moment):

  {"date": "2026-10-07", "person": "Chen", "kind": "review-for-others", "from": "Dami",
   "source": "github", "summary": "Reviewed the cache rollout PR; caught a stale-key bug",
   "link": "https://github.com/acme/api/pull/501", "beyond_role": false, "cross_team": false}

Kinds: peer-thanks, kudos, review-for-others, incident-help, on-call-cover, mentoring,
docs, onboarding-help, cross-team-help, unblocked, other.

Evidence comes from GitHub (`collect-github`), meeting scans (Nudge), Peer Pulse
answers, kudos the user sent, and items the user adds. Nothing is ranked or scored:
the analysis says whether a pattern is sustained, from several sources and people,
and flags workload to check. It runs locally and sends nothing.

  python3 spotlight.py collect-github --evidence ev.jsonl --repo acme/api --since 2026-10-01 \
      --team "chen-l=Chen,bea-r=Bea,dami-o=Dami"
  python3 spotlight.py analyze --evidence ev.jsonl --since 2026-10-01
  python3 spotlight.py story   --evidence ev.jsonl --person Chen --since 2026-10-01 > chen-impact.md
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

KINDS = ["peer-thanks", "kudos", "review-for-others", "incident-help", "on-call-cover", "mentoring", "docs",
         "onboarding-help", "cross-team-help", "unblocked", "other"]
THEMES = {
    "Raising others": ["mentoring", "onboarding-help", "unblocked"],
    "Reviews and quality": ["review-for-others"],
    "Reliability": ["incident-help", "on-call-cover"],
    "Knowledge sharing": ["docs"],
    "Across teams": ["cross-team-help"],
    "What peers said": ["peer-thanks", "kudos"],
}
THANKS = re.compile(r"\b(thank|thanks|great catch|nice catch|appreciate|saved|kudos)\b", re.I)
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")


# ---------- evidence file ----------

def load(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                sys.exit(f"{path}:{n} is not valid JSON")
    return rows


def append(path: Path, rows: list[dict]) -> int:
    existing = {(r.get("person"), r.get("kind"), r.get("link"), r.get("from"), r.get("date")) for r in load(path)}
    new = [r for r in rows if (r.get("person"), r.get("kind"), r.get("link"), r.get("from"), r.get("date")) not in existing]
    with path.open("a", encoding="utf-8") as fh:
        for r in new:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    return len(new)


def in_window(rows: list[dict], since: str | None, until: str | None) -> list[dict]:
    return [r for r in rows if (not since or r["date"] >= since) and (not until or r["date"] <= until)]


# ---------- GitHub ----------

def gh(path: str):
    if not shutil.which("gh"):
        sys.exit("GitHub CLI (gh) not found; install it and run `gh auth login`, or add evidence another way")
    run = subprocess.run(["gh", "api", "--paginate", "-H", "Accept: application/vnd.github+json", path],
                         capture_output=True, text=True)
    if run.returncode != 0:
        sys.exit(f"gh api {path} failed: {run.stderr.strip()}")
    out = run.stdout.strip() or "[]"
    if out.startswith("[") and "][" in out:
        out = "[" + out[1:-1].replace("][", ",") + "]"
    return json.loads(out)


def collect_github(repo: str, since: str, team: dict[str, str]) -> list[dict]:
    """Reviews team members gave on others' PRs, and thanks addressed to them in PR threads (read-only)."""
    rows: list[dict] = []
    pulls = gh(f"repos/{repo}/pulls?state=all&sort=updated&direction=desc&per_page=100")
    for pr in pulls:
        if (pr.get("updated_at") or "")[:10] < since:
            continue
        author = pr["user"]["login"]
        num, url, title = pr["number"], pr["html_url"], pr["title"]
        for rv in gh(f"repos/{repo}/pulls/{num}/reviews?per_page=100"):
            who = (rv.get("user") or {}).get("login")
            date = (rv.get("submitted_at") or "")[:10]
            if who in team and who != author and date >= since and rv.get("state") in ("APPROVED", "CHANGES_REQUESTED", "COMMENTED"):
                rows.append({"date": date, "person": team[who], "kind": "review-for-others",
                             "from": team.get(author, author), "source": "github",
                             "summary": f"Reviewed \"{title}\" ({rv['state'].lower().replace('_', ' ')})",
                             "link": url, "beyond_role": False, "cross_team": author not in team})
        for c in gh(f"repos/{repo}/issues/{num}/comments?per_page=100"):
            body, writer = c.get("body") or "", (c.get("user") or {}).get("login")
            date = (c.get("created_at") or "")[:10]
            if date < since or not THANKS.search(body):
                continue
            for login, name in team.items():
                if login != writer and re.search(rf"@{re.escape(login)}\b", body):
                    quote = EMAIL.sub("[email]", " ".join(body.split()))[:200]
                    rows.append({"date": date, "person": name, "kind": "peer-thanks",
                                 "from": team.get(writer, writer), "source": "github",
                                 "summary": quote, "link": c.get("html_url", url),
                                 "beyond_role": False, "cross_team": writer not in team})
    return rows


# ---------- analysis ----------

def week(d: str) -> str:
    y, w, _ = dt.date.fromisoformat(d).isocalendar()
    return f"{y}-W{w:02d}"


def profile(rows: list[dict]) -> dict:
    givers = {r["from"] for r in rows if r.get("from") and r["from"] != r["person"]}
    return {
        "moments": len(rows),
        "weeks": sorted({week(r["date"]) for r in rows}),
        "sources": sorted({r.get("source", "other") for r in rows}),
        "kinds": Counter(r["kind"] for r in rows),
        "peers": sorted(givers),
        "beyond_role": sum(1 for r in rows if r.get("beyond_role")),
        "cross_team": sum(1 for r in rows if r.get("cross_team") or r["kind"] == "cross-team-help"),
    }


def analyze(rows: list[dict], min_weeks: int, min_sources: int, min_peers: int) -> dict:
    by_person = defaultdict(list)
    for r in rows:
        by_person[r["person"]].append(r)
    profiles = {p: profile(rs) for p, rs in by_person.items()}
    review_counts = [pr["kinds"].get("review-for-others", 0) for pr in profiles.values()]
    review_median = median(review_counts) if review_counts else 0
    out = {"sustained": {}, "emerging": [], "workload": {}}
    for person, pr in sorted(profiles.items()):
        reasons = []
        sustained = (len(pr["weeks"]) >= min_weeks and len(pr["sources"]) >= min_sources
                     and len(pr["peers"]) >= min_peers and (pr["beyond_role"] or pr["cross_team"]
                                                            or len(pr["kinds"]) >= 3))
        if sustained:
            reasons = [f"{len(pr['weeks'])} different weeks", f"{len(pr['sources'])} kinds of source",
                       f"{len(pr['peers'])} colleagues", ", ".join(k for k, _ in pr["kinds"].most_common(4))]
            out["sustained"][person] = reasons
        elif len(pr["weeks"]) >= 2:
            out["emerging"].append(person)
        load = []
        if pr["kinds"].get("on-call-cover", 0) >= 2:
            load.append(f"covered others' on-call {pr['kinds']['on-call-cover']} times")
        off_rota = sum(1 for r in by_person[person] if r["kind"] == "incident-help" and r.get("beyond_role"))
        if off_rota >= 2:
            load.append(f"helped on {off_rota} incidents outside their own rota")
        if review_median and pr["kinds"].get("review-for-others", 0) >= 2.5 * review_median and pr["kinds"]["review-for-others"] >= 6:
            load.append("is carrying much more of the team's review load than most")
        if load:
            out["workload"][person] = load
    return out


def print_analysis(res: dict, since: str | None, until: str | None) -> None:
    span = f"{since or 'start'} to {until or 'today'}"
    print(f"Spotlight check, {span}\n")
    print("## Sustained pattern of going above and beyond (alphabetical, not ranked)\n")
    if not res["sustained"]:
        print("- Nobody meets the bar yet. That's fine: the bar is several weeks, sources and colleagues.\n")
    for p, why in res["sustained"].items():
        print(f"- **{p}**: {'; '.join(why)}")
    if res["emerging"]:
        print("\n## Worth watching (a pattern may be forming)\n")
        print("- " + ", ".join(res["emerging"]))
    if res["workload"]:
        print("\n## Check workload (ask, don't assume)\n")
        for p, why in res["workload"].items():
            print(f"- **{p}**: {'; '.join(why)}. Ask how they're doing and whether the load is sustainable.")
    print("\n_Private to you. No scores or rankings; use this to decide who to look at more closely._")


def story(rows: list[dict], person: str, since: str | None, until: str | None) -> str:
    mine = sorted([r for r in rows if r["person"].lower() == person.lower()], key=lambda r: r["date"])
    if not mine:
        sys.exit(f"no evidence for {person}")
    pr = profile(mine)
    lines = [f"# {person}: impact story", "",
             f"_{since or mine[0]['date']} to {until or mine[-1]['date']}: {pr['moments']} moments across "
             f"{len(pr['weeks'])} weeks, from {', '.join(pr['sources'])}; {len(pr['peers'])} colleagues involved._", "",
             "## The pattern", "",
             "_(One or two sentences, written by you or Claude from the evidence below: what they consistently do, "
             "and the difference it makes for the team.)_", ""]
    for theme, kinds in THEMES.items():
        items = [r for r in mine if r["kind"] in kinds]
        if not items:
            continue
        lines += [f"## {theme}", ""]
        for r in items:
            tag = []
            if r.get("beyond_role"):
                tag.append("beyond role")
            if r.get("cross_team") and r["kind"] != "cross-team-help":
                tag.append("another team")
            src = f" ([link]({r['link']}))" if r.get("link") else ""
            who = f" (from {r['from']})" if r.get("from") and r["kind"] in ("peer-thanks", "kudos") else ""
            extra = f" _{', '.join(tag)}_" if tag else ""
            lines.append(f"- {r['date']}: {r['summary']}{who}{src}{extra}")
        lines.append("")
    other = [r for r in mine if not any(r["kind"] in k for k in THEMES.values())]
    if other:
        lines += ["## Also", ""] + [f"- {r['date']}: {r['summary']}" for r in other] + [""]
    lines += ["## Ways to elevate them", "",
              "- [ ] A note to their manager and skip-level with this story",
              "- [ ] A nomination (award, promotion case) in your company's format",
              "- [ ] A stretch opportunity they'd want: lead a design review, own a launch, present at staff meeting",
              "- [ ] An introduction to someone senior who should know their work (Intro skill)",
              "- [ ] A public shout-out, only for public work and with their OK (Kudos)",
              "- [ ] A mention in the next Team Story or all-hands", "",
              "_Ask them what they'd value. Log what you do as sponsorship in your growth log, and its outcome._"]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("collect-github")
    g.add_argument("--evidence", type=Path, required=True)
    g.add_argument("--repo", required=True)
    g.add_argument("--since", required=True)
    g.add_argument("--team", required=True, help="login=Name pairs, comma-separated")
    a = sub.add_parser("analyze")
    a.add_argument("--evidence", type=Path, required=True)
    a.add_argument("--since"); a.add_argument("--until")
    a.add_argument("--min-weeks", type=int, default=4)
    a.add_argument("--min-sources", type=int, default=2)
    a.add_argument("--min-peers", type=int, default=3)
    a.add_argument("--json", action="store_true")
    s = sub.add_parser("story")
    s.add_argument("--evidence", type=Path, required=True)
    s.add_argument("--person", required=True)
    s.add_argument("--since"); s.add_argument("--until")
    args = ap.parse_args()

    if args.cmd == "collect-github":
        team = {}
        for pair in args.team.split(","):
            login, _, name = pair.strip().partition("=")
            if login:
                team[login] = name or login
        added = append(args.evidence, collect_github(args.repo, args.since, team))
        print(f"added {added} moments from {args.repo} to {args.evidence}")
        return 0
    rows = in_window(load(args.evidence), args.since, args.until)
    for r in rows:
        if r.get("kind") not in KINDS:
            r["kind"] = "other"
    if args.cmd == "analyze":
        res = analyze(rows, args.min_weeks, args.min_sources, args.min_peers)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            print_analysis(res, args.since, args.until)
    else:
        print(story(rows, args.person, args.since, args.until))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
