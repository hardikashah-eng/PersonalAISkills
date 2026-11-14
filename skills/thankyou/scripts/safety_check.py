#!/usr/bin/env python3
"""Safety scan for a ThankYou note.

Flags PII, financial and health details, harsh or judgemental wording, and any
recipient-specific topics to avoid. It is a backstop for human judgement, not a
replacement: a clean result does not prove a note is safe.

Usage:
    python3 safety_check.py note.json [--avoid "loss,divorce,baby"] [--profile reconnect|team|family]
                                      [--roster "Ana,Ben,Chen"] [--json]

Exit code 0 = no blocking issues, 1 = blocking issues found, 2 = bad input.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# --- Blocking patterns -------------------------------------------------------

PII_PATTERNS = {
    "email address": r"[\w.+-]+@[\w-]+\.[\w.-]+",
    "phone number": r"(?:\+?\d[\s().-]?){7,}\d",
    "URL": r"\b(?:https?://|www\.)\S+",
    "long number (ID/account?)": r"\b\d{6,}\b",
    "street address": r"\b\d{1,5}\s+\w+(?:\s\w+)?\s(?:street|st|avenue|ave|road|rd|lane|ln|drive|dr|blvd|boulevard|court|ct|way)\b",
    "social handle": r"(?<![\w.])@[A-Za-z0-9_]{2,}",
}

CURRENCY = r"(?:[$€£¥₹₩]\s?\d|\d[\d,.]*\s?(?:k|K|lakh|lakhs|crore|USD|INR|EUR|GBP|dollars?|rupees?|euros?|pounds?|yuan|yen)\b)"

FINANCIAL_TERMS = [
    "salary", "salaries", "paycheck", "loan", "loaned", "lend", "lending", "lent me", "debt", "debts",
    "mortgage", "rent money", "bank", "credit card", "bonus", "raise", "compensation",
    "stock options", "equity", "invest", "investment", "bankrupt", "broke", "money",
    "paid for", "cash", "wire", "venmo", "paypal", "upi",
]

HEALTH_TERMS = [
    "hospital", "surgery", "surgeon", "cancer", "chemo", "chemotherapy", "tumor",
    "diagnos", "therapy", "therapist", "counsel", "psychiatr", "medication", "meds",
    "pills", "prescription", "pregnan", "miscarriage", "ivf", "fertility",
    "depression", "depressed", "anxiety", "panic attack", "rehab", "addiction",
    "sober", "illness", "disease", "injury", "injured", "icu", "er visit", "clinic",
    "doctor", "diabetes", "heart attack", "stroke", "covid", "disabled", "disability",
    "mental health", "suicid", "self-harm", "eating disorder",
]

SENSITIVE_OTHER = [
    "lawsuit", "court case", "arrest", "visa status", "green card", "immigration",
    "divorce", "laid off", "fired", "layoff",
]

# --- Review (tone) patterns --------------------------------------------------

HARSH_TERMS = [
    "stupid", "idiot", "dumb", "lazy", "useless", "pathetic", "annoying", "hate",
    "shut up", "crazy", "insane", "loser", "weird", "ugly", "fat", "old man", "old lady",
    "for once", "even you", "despite your", "unlike you", "for a change",
    "you never", "you always", "should have", "finally did", "about time",
    "damn", "hell", "crap",
]

# --- Profile: reconnect -------------------------------------------------------

RECONNECT_BLOCK = {
    "guilt / time-counting": [
        "it's been forever", "it has been forever", "been ages", "been so long",
        "long time no", "years already", "sorry i disappeared", "sorry i've been mia",
        "sorry for being mia", "i'm terrible at", "i'm the worst at", "i am terrible at",
        "you probably don't remember", "you may not remember", "dropped the ball",
    ],
    "surveillance-sounding": [
        "saw on your profile", "noticed on your profile", "noticed you moved",
        "saw you moved", "noticed you were at", "saw you were at", "saw you were in",
        "checked in at", "your location", "stalking",
    ],
}

RECONNECT_REVIEW = {
    "possible hidden ask": [
        "quick favor", "quick favour", "refer me", "referral", "could you introduce",
        "can you introduce", "looking for a job", "job search", "are you hiring",
        "pick your brain",
    ],
}

# --- Profile: team / org ------------------------------------------------------

TEAM_BLOCK = {
    "confidential business detail": [
        "confidential", "internal only", "do not share", "don't share", "revenue",
        "headcount", "profit", "margin", "arr", "burn rate", "valuation",
    ],
}

TEAM_REVIEW = {
    "reads like a performance review": [
        "exceeded expectations", "meets expectations", "met expectations",
        "performance review", "performance rating", "rating", "promotion", "promoted",
        "top performer", "high performer", "low performer", "pip",
    ],
    "ranking people": [
        "mvp", "most valuable", "the best on the team", "best of the team", "star of the team",
    ],
    "non-inclusive or cliché wording": [
        "guys", "rockstar", "rockstars", "rock star", "rock stars", "ninja", "ninjas",
        "10x", "manpower",
    ],
}

# --- Profile: family ----------------------------------------------------------

FAMILY_BLOCK = {
    "comparison or ranking": [
        "favorite child", "favourite child", "favorite sibling", "favourite sibling",
        "favorite grandchild", "favourite grandchild", "unlike your", "better than your",
        "why can't you",
    ],
    "pressure": [
        "when are you getting", "when will you", "settle down", "give us grandchildren",
        "grandkids yet", "it's time you",
    ],
}

FAMILY_REVIEW = {
    "guilt or debt language": [
        "after all you sacrificed", "after all you've sacrificed", "after everything you sacrificed",
        "can never repay", "can't ever repay", "i owe you everything", "i don't call enough",
        "i should call more", "i know i never",
    ],
}

PROFILES = {
    "default": ({}, {}),
    "reconnect": (RECONNECT_BLOCK, RECONNECT_REVIEW),
    "team": (TEAM_BLOCK, TEAM_REVIEW),
    "family": (FAMILY_BLOCK, FAMILY_REVIEW),
}

CLICHES = [
    "words cannot express", "words can't express", "from the bottom of my heart",
    "you're the best ever", "best ever", "means the world",
]


def collect_text(note: dict) -> list[tuple[str, str]]:
    """Return (field, text) pairs for every human-visible field."""
    out: list[tuple[str, str]] = []
    quote = note.get("quote") or {}
    for key in ("text", "attribution", "translation"):
        if quote.get(key):
            out.append((f"quote.{key}", str(quote[key])))
    for key in ("greeting", "closing", "signature", "occasion"):
        if note.get(key):
            out.append((key, str(note[key])))
    for i, para in enumerate(note.get("body") or []):
        out.append((f"body[{i}]", str(para)))
    photo = note.get("photo") or {}
    for key in ("caption", "alt"):
        if photo.get(key):
            out.append((f"photo.{key}", str(photo[key])))
    return out


def term_hits(text: str, terms: list[str]) -> list[str]:
    """Stem match: word boundary at the start only (e.g. "diagnos" -> diagnosis)."""
    lowered = text.lower()
    hits = []
    for term in terms:
        if re.search(r"(?<![\w])" + re.escape(term.lower()), lowered):
            hits.append(term)
    return hits


def word_hits(text: str, terms: list[str]) -> list[str]:
    """Whole-word or whole-phrase match (so "hell" doesn't match "hello")."""
    lowered = text.lower().replace("’", "'")
    hits = []
    for term in terms:
        if re.search(r"(?<![\w])" + re.escape(term.lower()) + r"(?![\w])", lowered):
            hits.append(term)
    return hits


REAL_PHOTO_CLAIMS = [
    "found this photo", "found this picture", "found this from", "found this today",
    "look what turned up", "remember this", "photo of us", "picture of us", "this photo of",
    "this is us", "here's us", "us at the", "photo from", "picture from", "snapped this",
    "took this",
]


def honesty_issues(note: dict) -> list[dict]:
    """A drawn sketch or stock photo must not be presented as a real photo of the moment."""
    photo = note.get("photo") or {}
    if photo.get("source") not in ("sketch", "stock"):
        return []
    out = []
    for field, text in collect_text(note):
        if field.startswith("photo.alt"):
            continue
        for t in word_hits(text, REAL_PHOTO_CLAIMS):
            out.append({"level": "block",
                        "category": f"honesty: wording presents a {photo['source']} as a real photo of the moment",
                        "field": field, "match": t})
    if photo.get("source") == "stock" and not (photo.get("credit") or photo.get("license")):
        out.append({"level": "review", "category": "stock photo: record its licence (and credit if required)",
                    "field": "photo", "match": "no credit/license"})
    return out


def roster_issues(note: dict, roster: list[str]) -> list[dict]:
    """Name everyone or no one: if any roster member is named, all must be."""
    names = [n for n in roster if n]
    if not names:
        return []
    text = " ".join(t for _, t in collect_text(note))
    named = [n for n in names if word_hits(text, [n])]
    if not named:
        return []
    missing = [n for n in names if n not in named]
    return [{"level": "block", "category": "group: named some people but not everyone",
             "field": "roster", "match": m} for m in missing]


def scan(note: dict, avoid: list[str], profile: str = "default",
         roster: list[str] | None = None) -> list[dict]:
    issues: list[dict] = []
    extra_block, extra_review = PROFILES[profile]

    def add(level, category, field, match):
        issues.append({"level": level, "category": category, "field": field, "match": match})

    for field, text in collect_text(note):
        for label, pattern in PII_PATTERNS.items():
            for m in re.finditer(pattern, text, flags=re.IGNORECASE):
                add("block", f"PII: {label}", field, m.group(0))
        for m in re.finditer(CURRENCY, text):
            add("block", "financial: amount", field, m.group(0))
        for t in term_hits(text, FINANCIAL_TERMS):
            add("block", "financial term", field, t)
        for t in term_hits(text, HEALTH_TERMS):
            add("block", "health term", field, t)
        for t in term_hits(text, SENSITIVE_OTHER):
            add("block", "sensitive topic", field, t)
        for t in term_hits(text, [a for a in avoid if a]):
            add("block", "recipient trigger (--avoid)", field, t)
        for t in word_hits(text, HARSH_TERMS):
            add("review", "tone: harsh/judgemental", field, t)
        for t in word_hits(text, CLICHES):
            add("review", "tone: cliché", field, t)
        for category, terms in extra_block.items():
            for t in word_hits(text, terms):
                add("block", f"{profile}: {category}", field, t)
        for category, terms in extra_review.items():
            for t in word_hits(text, terms):
                add("review", f"{profile}: {category}", field, t)
        if text.count("!") > 1:
            add("review", "tone: too many exclamation marks", field, "!" * text.count("!"))

    total_bang = sum(t.count("!") for _, t in collect_text(note))
    if total_bang > 1:
        add("review", "tone: more than one '!' in the note", "*", str(total_bang))

    words = sum(len(t.split()) for f, t in collect_text(note) if f.startswith("body"))
    if words > 220:
        add("review", "length: body over 220 words", "body", str(words))

    issues += roster_issues(note, roster if roster is not None else note.get("roster") or [])
    issues += honesty_issues(note)
    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("note", type=Path)
    ap.add_argument("--avoid", default="", help="comma-separated topics to avoid for this recipient")
    ap.add_argument("--json", action="store_true", help="print machine-readable output")
    ap.add_argument("--profile", choices=sorted(PROFILES), default="default",
                    help="extra checks: reconnect, team (team/org notes), family")
    ap.add_argument("--roster", default=None,
                    help="comma-separated names in the group; if any are named, all must be "
                         "(defaults to the note's 'roster' list)")
    args = ap.parse_args()

    try:
        note = json.loads(args.note.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: cannot read {args.note}: {exc}", file=sys.stderr)
        return 2

    avoid = [a.strip() for a in args.avoid.split(",")]
    roster = [r.strip() for r in args.roster.split(",")] if args.roster is not None else None
    issues = scan(note, avoid, args.profile, roster)
    blocking = [i for i in issues if i["level"] == "block"]

    if args.json:
        print(json.dumps({"ok": not blocking, "issues": issues}, ensure_ascii=False, indent=2))
    else:
        if not issues:
            print("✓ clean — no PII, financial, health, trigger, or tone flags")
        for i in issues:
            mark = "✗" if i["level"] == "block" else "•"
            print(f"{mark} [{i['category']}] {i['field']}: {i['match']!r}")
        if blocking:
            print(f"\n{len(blocking)} blocking issue(s): abstract or remove them, then re-run.")
        elif issues:
            print("\nNo blocking issues; review the tone notes above.")
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
