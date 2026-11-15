#!/usr/bin/env python3
"""Turn a user's answers (routines.json) into ready-to-schedule routines.

Each routine gets a name, a cron schedule in the user's time zone, and a
complete, standalone prompt. A scheduled run starts fresh with no memory of
the conversation, so the prompt carries everything it needs: who the user is,
which skills to run, which sources to read, where the growth log lives, and
the rule that nothing is sent without the user's approval.

  python3 make_routines.py routines.json                 # human-readable plan
  python3 make_routines.py routines.json --json          # for creating the scheduled tasks
  python3 make_routines.py routines.json --only daily-brief,weekly-kudos

The script only prints. Creating the scheduled tasks is done by Claude with
the scheduling tool of the app in use, after the user approves the plan.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DAYS = {"mon": 1, "tue": 2, "wed": 3, "thu": 4, "fri": 5, "sat": 6, "sun": 0}
WEEKDAYS = "1-5"

APPROVAL_RULE = (
    "Approval rule: you prepare drafts only. Do not send, post, comment, message anyone, or write to the "
    "growth log or any shared tool during this run, except the one review message to me. "
    "End with a review list: number each item and show the recipient, the channel, the full draft, and the "
    "safety-check result. I will reply with what to send, edit or skip; act only on items I approve in that reply."
)

PRIVACY_RULE = (
    "Privacy: read only the sources named here, and only what each item needs. Skip anything about health, "
    "family, leave or personal life. Don't infer anyone's mood or emotions. Don't save anything to memory."
)


def parse_time(value: str) -> tuple[int, int]:
    m = re.fullmatch(r"(\d{1,2}):(\d{2})\s*([ap]m)?", value.strip().lower())
    if not m:
        sys.exit(f"time must look like 8:40, 16:10 or 4:10pm (got {value!r})")
    h, mnt, ampm = int(m.group(1)), int(m.group(2)), m.group(3)
    if ampm == "pm" and h < 12:
        h += 12
    if ampm == "am" and h == 12:
        h = 0
    if not (0 <= h < 24 and 0 <= mnt < 60):
        sys.exit(f"not a valid time: {value!r}")
    return h, mnt


def jitter(name: str, h: int, m: int) -> tuple[int, int]:
    """Move times that land exactly on :00 or :30 a few minutes earlier, so runs aren't queued behind everyone else's."""
    if m not in (0, 30):
        return h, m
    shift = len(name) % 29 + 1
    total = (h * 60 + m - shift) % (24 * 60)
    return divmod(total, 60)


def cron(tz: str, name: str, time: str, days: str) -> tuple[str, str]:
    h, m = jitter(name, *parse_time(time))
    if days in ("weekdays", "1-5"):
        dow = WEEKDAYS
    elif days in ("daily", "*"):
        dow = "*"
    else:
        try:
            dow = ",".join(str(DAYS[d.strip()[:3].lower()]) for d in days.split(","))
        except KeyError:
            sys.exit(f"days must be weekdays, daily, or names like mon,fri (got {days!r})")
    dom = "*"
    if days.startswith("monthly"):
        dom, dow = "1-7", "1"   # first Monday of the month
    return f"CRON_TZ={tz} {m} {h} {dom} * {dow}", f"{h:02d}:{m:02d}"


def is_local_log(cfg: dict) -> bool:
    return str(cfg.get("growth_log", "")).strip().lower().endswith((".jsonl", ".json", ".csv"))


def context(cfg: dict) -> str:
    me = cfg["me"]
    team = ", ".join(cfg.get("team") or []) or "my team"
    parts = [
        f"You are running a scheduled routine for {me['name']} ({me.get('role', 'a team lead')}), "
        f"time zone {cfg['timezone']}, using the PersonalAISkills plugin "
        "(https://github.com/hardikashah-eng/PersonalAISkills).",
        f"My team: {team}.",
    ]
    src = cfg.get("sources") or {}
    named = [f"{k}: {v}" for k, v in src.items() if v]
    if named:
        parts.append("Sources I've connected: " + "; ".join(named) + ".")
    ch = cfg.get("channels") or {}
    if ch:
        parts.append("Where things go when I approve them: " + "; ".join(f"{k}: {v}" for k, v in ch.items()) + ".")
    if cfg.get("growth_log"):
        how = ("read it with skills/feedback/scripts/growth_log.py" if is_local_log(cfg)
               else "read it through that connector, with the fields described in skills/feedback/references/growth-log.md")
        parts.append(f"My private growth log: {cfg['growth_log']} ({how}; write to it only for items I approve).")
    parts.append(f"Keep the list to at most {cfg.get('max_items', 5)} items, spread fairly across people.")
    return " ".join(parts)


def routine_prompts(cfg: dict) -> dict[str, dict]:
    ctx = context(cfg)
    meeting = cfg.get("meeting") or {}
    r = {
        "daily-brief": {
            "title": "Daily people brief",
            "what": "Morning list of recognition, follow-ups, first days and anniversaries",
            "task": ("Run the nudge skill in daily mode for the last working day. Look for: specific work to "
                     "recognize (merged PRs, resolved incidents, finished on-call shifts, docs), growth-log "
                     "follow-ups due in the next two days, first days and work anniversaries on my calendar, "
                     "and people I haven't recognized in 30 days. Draft each with the right skill (Kudos, "
                     "Welcome, ThankYou), run the safety check, and send me the review list. If nothing is "
                     "worth a nudge today, send one line saying so."),
        },
        "after-meeting": {
            "title": f"After {meeting.get('name', 'standup')}",
            "what": f"Recognition and commitments from {meeting.get('name', 'standup')}",
            "task": (f"Find today's transcript of '{meeting.get('name', 'standup')}' in "
                     f"{meeting.get('transcript_source', 'my meeting tool')}. If there's no transcript, or "
                     "transcription wasn't announced in the meeting, stop and tell me in one line. Otherwise run "
                     "the nudge skill in after-meeting mode (skills/nudge/scripts/scan_transcript.py with --me "
                     f"\"{cfg['me']['name']}\"). Draft Kudos for recognition moments and reported wins after "
                     "reading the work they refer to; list possible feedback moments for me only, as prompts to "
                     "check the facts; and list my own commitments with a suggested reminder time. Send me the "
                     "review list."),
        },
        "weekly-kudos": {
            "title": "Friday recognition sweep",
            "what": "The week's work worth recognizing, spread across the team",
            "task": ("Run the nudge skill in weekly mode: this week's merged PRs, reviews, resolved incidents "
                     "and on-call shifts for my team. Draft Kudos for the work that most deserves it (DM, plus a "
                     "#kudos post where it fits; LinkedIn only for public work, marked as needing the person's "
                     "consent). Include anyone who hasn't been recognized in 30 days if there's real work to "
                     "name. Send me the review list."),
        },
        "feedback-followups": {
            "title": "Monday growth follow-ups",
            "what": "Growth-log follow-ups due this week, and 1:1 prep",
            "task": ("Run growth_log.py due --days 7 on my growth log, and for each person with a 1:1 this week "
                     "on my calendar, prepare a short summary (growth_log.py summary) with what's going well first "
                     "and any follow-up due. Suggest one specific strength to mention for each person. Don't draft "
                     "new feedback and don't contact anyone. Send me the prep list."),
        },
        "monthly-reconnect": {
            "title": "Monthly reconnect",
            "what": "Two or three people worth reconnecting with",
            "task": ("Run the reconnect skill: find two or three people I've drifted from (former teammates, "
                     "mentors, friends) using my connected email and chat history, each with a real shared moment "
                     "as the hook, and draft a no-guilt check-in for each. Send me the review list."),
        },
    }
    for v in r.values():
        v["prompt"] = f"{ctx}\n\n{v['task']}\n\n{PRIVACY_RULE}\n\n{APPROVAL_RULE}"
    return r


def plan(cfg: dict, only: set[str] | None) -> list[dict]:
    prompts = routine_prompts(cfg)
    out = []
    for key, spec in (cfg.get("routines") or {}).items():
        if not spec or not spec.get("enabled", True):
            continue
        if only and key not in only:
            continue
        if key not in prompts:
            sys.exit(f"unknown routine {key!r}; choose from {', '.join(prompts)}")
        if key == "after-meeting" and not (cfg.get("meeting") or {}).get("name"):
            sys.exit("after-meeting needs meeting.name (and meeting.transcript_source)")
        expr, at = cron(cfg["timezone"], prompts[key]["title"], spec["time"], spec.get("days", "weekdays"))
        out.append({"key": key, "name": prompts[key]["title"], "what": prompts[key]["what"],
                    "cron": expr, "runs_at": at, "days": spec.get("days", "weekdays"),
                    "needs_local_files": is_local_log(cfg) and key in ("daily-brief", "feedback-followups"),
                    "prompt": prompts[key]["prompt"]})
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("config", type=Path)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--only", help="comma-separated routine keys")
    a = ap.parse_args()
    cfg = json.loads(a.config.read_text(encoding="utf-8"))
    for key in ("me", "timezone", "routines"):
        if key not in cfg:
            sys.exit(f"routines.json needs {key!r}")
    only = {x.strip() for x in a.only.split(",")} if a.only else None
    routines = plan(cfg, only)
    if a.json:
        print(json.dumps(routines, indent=2, ensure_ascii=False))
        return 0
    print(f"{len(routines)} routine(s) for {cfg['me']['name']} ({cfg['timezone']}):\n")
    for r in routines:
        local = "  (runs on your computer: the growth log is a local file)" if r["needs_local_files"] else ""
        print(f"• {r['name']}: {r['what']}\n  {r['days']} at {r['runs_at']}  [{r['cron']}]{local}")
    print("\nEach run prepares drafts and sends you one review list. Nothing is sent without your yes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
