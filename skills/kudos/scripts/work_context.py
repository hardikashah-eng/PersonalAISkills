#!/usr/bin/env python3
"""Gather the facts behind a piece of work, so a kudos note can be specific.

Reads a GitHub pull request or issue through the GitHub REST API with the
GitHub CLI (`gh`, already signed in by the user) and prints a short summary: what changed, why, who reviewed it,
what it closed, and the discussion highlights. Email addresses are removed.
It only reads; it never comments, approves or changes anything.

  python3 work_context.py https://github.com/acme/api/pull/482
  python3 work_context.py --repo acme/api --pr 482
  python3 work_context.py --repo acme/api --issue 77 --json

For incidents, design docs and on-call shifts (PagerDuty, Jira, Confluence,
Lark, Google Docs and so on), Claude reads them through the user's connectors
instead; this script covers GitHub.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
URL_RE = re.compile(r"https://github\.com/([^/]+/[^/]+)/(pull|issues)/(\d+)")
CLOSES = re.compile(r"\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)", re.I)
PRAISE = re.compile(r"\b(thank|great|nice|love|clean|elegant|lgtm|awesome|brilliant|well done|kudos)\b", re.I)


def clean(text: str | None, limit: int = 600) -> str:
    text = EMAIL.sub("[email]", text or "")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text if len(text) <= limit else text[:limit].rsplit(" ", 1)[0] + " …"


def api(path: str, paginate: bool = False):
    """GitHub REST API through the user's signed-in gh CLI (read-only GET requests)."""
    if not shutil.which("gh"):
        sys.exit("GitHub CLI (gh) not found. Install it and run `gh auth login`, or let Claude use the GitHub connector.")
    args = ["gh", "api", "-H", "Accept: application/vnd.github+json", path]
    if paginate:
        args.insert(2, "--paginate")
    run = subprocess.run(args, capture_output=True, text=True)
    if run.returncode != 0:
        sys.exit(f"gh api {path} failed: {run.stderr.strip()}")
    out = run.stdout.strip()
    if paginate and out.startswith("[") and "][" in out:
        out = "[" + out[1:-1].replace("][", ",") + "]"
    return json.loads(out or "null")


GROUPING_DIRS = {"src", "lib", "libs", "pkg", "packages", "apps", "services", "skills", "modules", "components", "cmd"}


def area(path: str) -> str:
    parts = path.split("/")
    if len(parts) > 2 and parts[0] in GROUPING_DIRS:
        return "/".join(parts[:2])
    return parts[0] if len(parts) > 1 else path


def login(user: dict | None) -> str:
    return (user or {}).get("login") or "unknown"


def summarize_pr(repo: str, number: int) -> dict:
    pr = api(f"repos/{repo}/pulls/{number}")
    files = api(f"repos/{repo}/pulls/{number}/files?per_page=100") or []
    reviews = api(f"repos/{repo}/pulls/{number}/reviews?per_page=100") or []
    comments = api(f"repos/{repo}/issues/{number}/comments?per_page=100") or []
    author = login(pr.get("user"))
    paths = [f["filename"] for f in files]
    tests = [p for p in paths if re.search(r"(^|/)(tests?|spec|__tests__)/|_test\.|\.test\.|(^|/)test_", p)]
    docs = [p for p in paths if p.lower().endswith((".md", ".rst", ".adoc"))]
    reviewers = sorted({login(r.get("user")) for r in reviews} - {author})
    praise = [f"{login(c.get('user'))}: {clean(c.get('body'), 240)}" for c in comments + reviews
              if PRAISE.search(c.get("body") or "") and login(c.get("user")) != author]
    return {
        "kind": "pull request",
        "repo": repo,
        "number": pr["number"],
        "url": pr["html_url"],
        "title": pr["title"],
        "author": author,
        "state": "merged" if pr.get("merged_at") else pr.get("state"),
        "merged_at": pr.get("merged_at"),
        "description": clean(pr.get("body")),
        "size": {"files": pr.get("changed_files"), "additions": pr.get("additions"), "deletions": pr.get("deletions")},
        "areas_touched": sorted({area(p) for p in paths})[:12],
        "added_or_changed_tests": tests[:10],
        "updated_docs": docs[:10],
        "labels": [l.get("name") for l in pr.get("labels") or []],
        "closes": sorted({f"#{n}" for n in CLOSES.findall(pr.get("body") or "")}),
        "reviewers": reviewers,
        "praise_in_thread": praise[:5],
    }


def summarize_issue(repo: str, number: int) -> dict:
    it = api(f"repos/{repo}/issues/{number}")
    comments = api(f"repos/{repo}/issues/{number}/comments?per_page=100") or []
    return {
        "kind": "pull request" if it.get("pull_request") else "issue",
        "repo": repo,
        "number": it["number"],
        "url": it["html_url"],
        "title": it["title"],
        "opened_by": login(it.get("user")),
        "assignees": [login(a) for a in it.get("assignees") or []],
        "state": it.get("state"),
        "closed_at": it.get("closed_at"),
        "description": clean(it.get("body")),
        "labels": [l.get("name") for l in it.get("labels") or []],
        "participants": sorted({login(c.get("user")) for c in comments}),
        "last_comments": [f"{login(c.get('user'))}: {clean(c.get('body'), 200)}" for c in comments[-4:]],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url", nargs="?", help="GitHub PR or issue URL")
    ap.add_argument("--repo", help="owner/name")
    ap.add_argument("--pr", type=int)
    ap.add_argument("--issue", type=int)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    kind, repo, number = None, a.repo, a.pr or a.issue
    if a.url:
        m = URL_RE.search(a.url)
        if not m:
            sys.exit("give a GitHub pull request or issue URL, or --repo with --pr/--issue")
        repo, kind, number = m.group(1), m.group(2), int(m.group(3))
    else:
        kind = "pull" if a.pr else "issues" if a.issue else None
    if not (repo and number and kind):
        sys.exit("give a GitHub pull request or issue URL, or --repo with --pr/--issue")
    info = summarize_pr(repo, number) if kind == "pull" else summarize_issue(repo, number)
    if a.json:
        print(json.dumps(info, indent=2, ensure_ascii=False))
        return 0
    for k, v in info.items():
        if v in (None, [], "", {}):
            continue
        if isinstance(v, list):
            print(f"{k}:")
            for x in v:
                print(f"  - {x}")
        else:
            print(f"{k}: {v}")
    print("\nUse this to name the specific contribution and its effect. Don't paste it into the note.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
