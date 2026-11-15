#!/usr/bin/env python3
"""Find recognition and feedback moments in a meeting transcript.

Reads a transcript the user has access to (WebVTT, SRT, or plain "Name: text"
lines, as exported from Zoom, Teams, Google Meet, Lark/Feishu Minutes, Otter
and similar) and lists, for the meeting owner only:

  praise      someone thanked or credited a colleague  → a Kudos draft
  wins        someone reported shipping or fixing      → maybe a Kudos from the owner
  feedback    a possible issue worth a private word     → a private note for the owner's 1:1
  commitment  someone said they'd do something by when → a follow-up reminder

It runs locally and only reads. It never contacts anyone. Lines that touch on
health, family or personal life are skipped entirely, and tone or emotion are
not inferred: a "feedback" moment is a prompt for the owner to check the
facts, not a judgement.

  python3 scan_transcript.py standup.vtt --me "Hardik"
  python3 scan_transcript.py standup.txt --me "Hardik" --people "Bea,Chen,Dami,Ola" --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TS = r"(\d{1,2}:\d{2}(?::\d{2})?(?:[.,]\d{1,3})?)"
CUE_TIME = re.compile(rf"^{TS}\s*-->\s*{TS}")
VTT_VOICE = re.compile(r"<v\s+([^>]+)>(.*?)(?:</v>|$)")
NAMED_LINE = re.compile(rf"^(?:\[?{TS}\]?\s*)?([A-Z][\w .'-]{{0,40}}?)\s*(?:\(\s*{TS}\s*\))?\s*:\s+(.+)$")
LARK_HEADER = re.compile(rf"^([A-Z][\w .'-]{{0,40}}?)\s+{TS}\s*$")

PRAISE = [
    r"\bthank(?:s| you)\b", r"\bshout[- ]?out\b", r"\bkudos\b", r"\bprops\b", r"\bcredit (?:goes )?to\b",
    r"\bgreat (?:job|work|catch|call|find|writeup|write-up|idea)\b", r"\bnice (?:work|job|catch|find)\b",
    r"\b(?:saved|unblocked|rescued) (?:us|me|the)\b", r"\bcouldn't have done (?:it|this) without\b",
    r"\bhuge help\b", r"\bwell done\b", r"\bnailed it\b", r"\breally helped\b",
]
FEEDBACK = [
    r"\bblocked (?:on|by)\b", r"\bstill waiting (?:on|for)\b", r"\bwaiting on\b", r"\bslipp(?:ed|ing)\b",
    r"\bmissed (?:the|our|a)\b", r"\bdidn't (?:get|have|hear|see)\b", r"\bno update\b", r"\bnot done\b",
    r"\bdropped\b", r"\bfell through\b", r"\bbehind (?:on|schedule)\b", r"\bagain\b", r"\bconfus(?:ed|ing)\b",
    r"\bwithout (?:telling|a heads[- ]up|review)\b", r"\bbroke (?:the|prod|staging|main)\b",
]
WINS = [r"\b(?:shipped|merged|launched|released|landed|went live|is live|rolled out|in prod)\b",
        r"\bno (?:\w+ )?(?:pages|alerts|incidents)\b", r"\b(?:fixed|closed out|finished|wrapped up)\b"]
GENERIC = re.compile(r"\b(?:everyone|everybody|all|team|folks|y'all|you all|guys)\b", re.I)
COMMIT = re.compile(r"\b(?:I'll|I will|I'm going to|I can have|will have|let me)\b(.{3,90}?)"
                    r"(?:\b(by|before|on|this|next|tomorrow|today|eod|end of (?:day|week))\b.{0,30})?(?:[.;!?]|$)", re.I)
PERSONAL = re.compile(
    r"\b(sick|ill|doctor|hospital|surgery|therapy|therapist|medical|medication|diagnos\w*|pregnan\w*|"
    r"maternity|paternity|leave|funeral|passed away|died|kid|kids|child|children|daughter|son|wife|husband|"
    r"partner|divorce|family|personal|mental|stress(?:ed)?|burn(?:ed|t)?\s?out|anxious|anxiety|visa|"
    r"salary|raise|promotion|pip|fired|layoff)\b", re.I)
STOPWORDS = {"I", "We", "You", "The", "This", "That", "And", "But", "So", "Thanks", "Thank", "Great", "Nice",
             "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "OK", "Okay", "Yes", "No",
             "Also", "Just", "Kudos", "Shout", "Props", "Huge", "Well", "Really", "Let", "Hey", "Hi", "PR", "EOD"}


def parse(text: str) -> list[dict]:
    """Return [{speaker, time, text}] from VTT, SRT, Lark-style or 'Name: text' transcripts."""
    out: list[dict] = []
    time = ""
    pending_speaker = None
    for raw in text.splitlines():
        line = raw.strip().lstrip("﻿")
        if not line or line == "WEBVTT" or line.isdigit() or line.startswith(("NOTE", "STYLE", "Kind:", "Language:")):
            continue
        m = CUE_TIME.match(line)
        if m:
            time = m.group(1).split(".")[0].split(",")[0]
            continue
        v = VTT_VOICE.search(line)
        if v:
            out.append({"speaker": v.group(1).strip(), "time": time, "text": re.sub(r"<[^>]+>", "", v.group(2)).strip()})
            pending_speaker = None
            continue
        h = LARK_HEADER.match(line)
        if h and len(line.split()) <= 5:
            pending_speaker, time = h.group(1).strip(), h.group(2)
            continue
        n = NAMED_LINE.match(line)
        if n and n.group(2).split()[0] not in STOPWORDS:
            out.append({"speaker": n.group(2).strip(), "time": n.group(1) or n.group(3) or time, "text": n.group(4).strip()})
            pending_speaker = None
            continue
        if pending_speaker:
            out.append({"speaker": pending_speaker, "time": time, "text": line})
        elif out:
            out[-1]["text"] += " " + line
    return [u for u in out if u["text"]]


def names_in(text: str, people: set[str]) -> list[str]:
    found = []
    for p in people:
        first = p.split()[0]
        if re.search(rf"\b{re.escape(first)}\b", text):
            found.append(p)
    return found


def sentence_with(text: str, patterns: list[str]) -> str:
    """The sentence that triggered the match, so the quote shows the point."""
    for sent in re.split(r"(?<=[.!?])\s+", text):
        if any(re.search(p, sent, re.I) for p in patterns):
            return sent
    return text


def short(text: str, words: int = 28) -> str:
    w = text.split()
    return " ".join(w[:words]) + (" …" if len(w) > words else "")


def scan(utterances: list[dict], me: str | None, people: set[str]) -> dict:
    speakers = {u["speaker"] for u in utterances}
    everyone = speakers | people
    result = {"participants": sorted(speakers), "praise": [], "wins": [], "feedback": [], "commitments": [],
              "skipped_personal": 0}
    for i, u in enumerate(utterances):
        text, who = u["text"], u["speaker"]
        if PERSONAL.search(text):
            result["skipped_personal"] += 1
            continue
        mentioned = [p for p in names_in(text, everyone) if p.split()[0] != who.split()[0]]
        if any(re.search(p, text, re.I) for p in PRAISE):
            said = sentence_with(text, PRAISE)
            about = [p for p in mentioned if re.search(rf"\b{re.escape(p.split()[0])}\b", said)] or mentioned
            if not about and i > 0 and not GENERIC.search(said) and re.match(r"(thanks|thank you|nice|great)", said, re.I):
                prev = utterances[i - 1]["speaker"]
                about = [prev] if prev != who else []
            for person in about:
                result["praise"].append({"about": person, "from": who, "time": u["time"], "said": short(said),
                                         "next": "Kudos draft (read the work it refers to first)"})
        if any(re.search(p, text, re.I) for p in WINS) and not (me and who.split()[0].lower() == me.split()[0].lower()):
            result["wins"].append({"about": who, "time": u["time"], "said": short(sentence_with(text, WINS)),
                                   "next": "Worth a Kudos from you? (check the work first)"})
        if any(re.search(p, text, re.I) for p in FEEDBACK) and mentioned:
            said = sentence_with(text, FEEDBACK)
            for person in mentioned:
                result["feedback"].append({"about": person, "raised_by": who, "time": u["time"], "said": short(said),
                                           "next": "Private: check the facts, then decide whether it's worth a word in your 1:1"})
        for m in COMMIT.finditer(text):
            what = m.group(0).strip()
            if len(what.split()) >= 3:
                result["commitments"].append({"who": who, "time": u["time"], "said": short(what, 22),
                                              "yours": bool(me and who.split()[0].lower() == me.split()[0].lower())})
    return result


def to_markdown(r: dict, me: str | None) -> str:
    lines = [f"Participants: {', '.join(r['participants'])}", ""]
    lines += ["## Recognition moments (→ Kudos drafts)", ""]
    lines += [f"- **{p['about']}**, from {p['from']} at {p['time'] or '?'}: “{p['said']}”" for p in r["praise"]] or ["- none found"]
    lines += ["", "## Wins people reported (→ maybe a Kudos from you)", ""]
    lines += [f"- **{w['about']}** at {w['time'] or '?'}: “{w['said']}”" for w in r["wins"]] or ["- none found"]
    lines += ["", "## Possible feedback moments (private to you; check the facts first)", ""]
    lines += [f"- **{f['about']}**, raised by {f['raised_by']} at {f['time'] or '?'}: “{f['said']}”" for f in r["feedback"]] or ["- none found"]
    lines += ["", "## Commitments (→ follow-up reminders)", ""]
    mine = [c for c in r["commitments"] if c["yours"]]
    others = [c for c in r["commitments"] if not c["yours"]]
    lines += [f"- **You** at {c['time'] or '?'}: “{c['said']}”" for c in mine]
    lines += [f"- {c['who']} at {c['time'] or '?'}: “{c['said']}”" for c in others]
    if not r["commitments"]:
        lines.append("- none found")
    if r["skipped_personal"]:
        lines += ["", f"_{r['skipped_personal']} line(s) touching on personal matters were skipped and not analysed._"]
    lines += ["", "_Nothing has been sent. Approve each draft before it goes anywhere._"]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("transcript", type=Path)
    ap.add_argument("--me", help="the meeting owner's name as it appears in the transcript")
    ap.add_argument("--people", default="", help="comma-separated team names, to catch mentions of people who didn't speak")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    utterances = parse(a.transcript.read_text(encoding="utf-8", errors="replace"))
    if not utterances:
        sys.exit("couldn't find any 'Speaker: text' lines; export the transcript with speaker names")
    people = {p.strip() for p in a.people.split(",") if p.strip()}
    r = scan(utterances, a.me, people)
    print(json.dumps(r, indent=2, ensure_ascii=False) if a.json else to_markdown(r, a.me))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
