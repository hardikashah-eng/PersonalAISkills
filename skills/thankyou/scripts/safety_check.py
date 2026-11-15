#!/usr/bin/env python3
"""Safety scan for a ThankYou note.

Flags PII, financial and health details, harsh or judgemental wording, and any
recipient-specific topics to avoid. It is a backstop for human judgement, not a
replacement: a clean result does not prove a note is safe.

Usage:
    python3 safety_check.py note.json [--avoid "loss,divorce,baby"] [--profile reconnect|team|family|grateful|comfort|public|feedback|repair]
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
    "mortgage", "rent money", "bank account", "bank loan", "credit card", "bonus", "pay raise", "a raise",
    "compensation", "stock options", "investment", "investments", "bankrupt", "was broke", "were broke",
    "flat broke", "money", "paid for", "cash", "wire transfer", "venmo", "paypal", "upi",
]

HEALTH_TERMS = [
    "hospital", "surgery", "surgeon", "cancer", "chemo", "chemotherapy", "tumor",
    "diagnos", "therapy", "therapist", "counseling", "counselling", "counselor", "counsellor", "psychiatr", "medication", "meds",
    "pills", "prescription", "pregnan", "miscarriage", "ivf", "fertility",
    "depression", "depressed", "anxiety", "panic attack", "rehab", "addiction",
    "sober", "illness", "disease", "injury", "injured", "icu", "er visit", "clinic",
    "doctor", "diabetes", "heart attack", "had a stroke", "suffered a stroke", "covid", "disabled", "disability",
    "mental health", "suicid", "self-harm", "eating disorder",
]

SENSITIVE_OTHER = [
    "lawsuit", "court case", "arrest", "visa status", "green card", "immigration",
    "divorce", "laid off", "got fired", "was fired", "were fired", "layoff",
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

# --- Profile: grateful (gratitude lists) --------------------------------------

GRATEFUL_BLOCK = {
    "comparison with others' misfortune": [
        "at least i'm not", "at least i am not", "at least we're not", "at least we are not",
        "unlike some people", "unlike others", "less fortunate", "luckier than", "better off than",
        "poor people", "those poor",
    ],
}

GRATEFUL_REVIEW = {
    "bragging or humble-bragging": [
        "humbled to announce", "so humbled", "blessed beyond measure", "#blessed", "living my best life",
        "crushed it", "killing it", "promotion", "promoted",
    ],
    "guilt": [
        "i don't deserve", "i never thank", "i should have been", "i know i haven't",
    ],
}

# --- Profile: comfort (hard times) -------------------------------------------

COMFORT_BLOCK = {
    "minimising or silver-lining": [
        "at least", "everything happens for a reason", "happens for a reason", "better place",
        "god's plan", "part of god's plan", "silver lining", "look on the bright side",
        "could have been worse", "could be worse", "it was meant to be", "time heals",
        "move on", "moving on", "get over it", "you'll get over", "plenty of fish",
    ],
    "making it about the sender": [
        "i know exactly how you feel", "i know how you feel", "when my", "same thing happened to me",
    ],
    "pressure or advice": [
        "stay strong", "be strong", "you should", "you need to", "have you tried",
        "you must", "don't cry", "cheer up", "let me know if you need anything",
    ],
}

COMFORT_REVIEW = {
    "check the tone": ["fun fact", "lol", "haha", "!!"],
}

# --- Profile: public (LinkedIn and other public posts) ------------------------

PUBLIC_BLOCK = {
    "confidential or unreleased": [
        "confidential", "internal only", "nda", "under nda", "unreleased", "not yet announced",
        "unannounced", "embargo", "embargoed", "stealth", "codename", "code name", "pre-release",
    ],
    "security details": [
        "vulnerability", "vulnerabilities", "exploit", "cve", "security incident", "breach",
        "data leak", "leaked", "credentials", "password", "api key",
    ],
    "people matters": [
        "performance review", "pip", "headcount", "layoff", "layoffs", "reorg", "promotion packet",
        "compensation", "salary", "rating",
    ],
}

PUBLIC_REVIEW = {
    "may be internal (check it's public)": [
        "incident", "outage", "sev1", "sev2", "sev-1", "sev-2", "postmortem", "post-mortem",
        "customer", "customers", "roadmap", "launch date", "beta", "internal", "on-call", "oncall",
        "rollback", "downtime", "pager", "escalation", "deadline",
    ],
}

PUBLIC_PATTERNS = {
    "ticket or PR reference": r"(?<![\w/])#\d{2,}\b|\b[A-Z][A-Z0-9]{1,9}-\d{1,6}\b",
    "internal link": r"https?://[^\s]*(?:internal|intranet|corp|\.local\b|jira|atlassian\.net|"
                     r"feishu|larksuite|slack\.com|teams\.microsoft|sharepoint|confluence|grafana|"
                     r"datadog|pagerduty|localhost|\b10\.\d|\b192\.168\.)[^\s]*",
    "a metric or number (check it's public)": r"\b\d+(?:\.\d+)?\s?(?:%|percent|x\b|ms\b|k\b|m\b|users\b|qps\b)",
}

# --- Profile: feedback (constructive feedback) --------------------------------

FEEDBACK_BLOCK = {
    "labels the person instead of the behaviour": [
        "lazy", "careless", "incompetent", "sloppy", "attitude problem", "bad attitude", "not a team player",
        "unprofessional", "lack of commitment", "doesn't care", "don't care", "useless", "hopeless", "immature",
    ],
    "absolutes": ["you always", "you never", "every single time", "constantly"],
    "comparing to others": ["unlike", "why can't you be like", "compared to"],
}

FEEDBACK_REVIEW = {
    "coded or vague words (describe the behaviour instead)": [
        "abrasive", "bossy", "emotional", "aggressive", "shrill", "too nice", "culture fit", "not a fit",
        "attitude", "personality", "lack of polish", "executive presence", "too quiet", "too direct",
    ],
    "softeners that hide the point": ["just a thought", "no big deal", "maybe it's just me", "sort of", "kind of"],
}

# --- Profile: repair (apologies and follow-ups) -------------------------------

REPAIR_BLOCK = {
    "non-apology": [
        "sorry if", "sorry you feel", "sorry that you feel", "if anyone was offended", "if i offended",
        "mistakes were made", "i'm sorry but", "sorry, but", "no offense", "you misunderstood",
        "you took it the wrong way", "to be fair", "you overreacted", "calm down",
    ],
}

REPAIR_REVIEW = {
    "excuses that dilute it": ["but", "however", "i was just", "i only", "anyway"],
}

PROFILES = {
    "default": ({}, {}),
    "reconnect": (RECONNECT_BLOCK, RECONNECT_REVIEW),
    "team": (TEAM_BLOCK, TEAM_REVIEW),
    "family": (FAMILY_BLOCK, FAMILY_REVIEW),
    "grateful": (GRATEFUL_BLOCK, GRATEFUL_REVIEW),
    "comfort": (COMFORT_BLOCK, COMFORT_REVIEW),
    "public": (PUBLIC_BLOCK, PUBLIC_REVIEW),
    "feedback": (FEEDBACK_BLOCK, FEEDBACK_REVIEW),
    "repair": (REPAIR_BLOCK, REPAIR_REVIEW),
}

CLICHES = [
    "words cannot express", "words can't express", "from the bottom of my heart",
    "you're the best ever", "best ever", "means the world",
]


def as_paras(value) -> list[str]:
    if not value:
        return []
    if isinstance(value, str):
        return [value]
    return [str(v.get("text", "")) if isinstance(v, dict) else str(v) for v in value]


def collect_text(note: dict) -> list[tuple[str, str]]:
    """Return (field, text) pairs for every human-visible field."""
    out: list[tuple[str, str]] = []
    quote = note.get("quote") or {}
    for key in ("text", "attribution", "translation"):
        if quote.get(key):
            out.append((f"quote.{key}", str(quote[key])))
    for key in ("greeting", "closing", "signature", "occasion"):
        if note.get(key) and not isinstance(note[key], dict):
            out.append((key, str(note[key])))
    for i, para in enumerate(note.get("body") or []):
        out.append((f"body[{i}]", str(para)))
    photo = note.get("photo") or {}
    for key in ("caption", "alt"):
        if photo.get(key):
            out.append((f"photo.{key}", str(photo[key])))
    if note.get("title"):
        out.append(("title", str(note["title"])))
    for i, it in enumerate(note.get("items") or []):
        for key in ("subject", "why", "difference", "forward"):
            if it.get(key):
                out.append((f"items[{i}].{key}", str(it[key])))
    ff = note.get("fun_fact")
    ff_text = ff.get("text") if isinstance(ff, dict) else ff
    if ff_text:
        out.append(("fun_fact", str(ff_text)))
    # Channel versions used by share.py
    for key in ("subject", "channel_post"):
        if note.get(key):
            out.append((key, str(note[key])))
    sb = note.get("short_body") or []
    for i, para in enumerate([sb] if isinstance(sb, str) else sb):
        out.append((f"short_body[{i}]", str(para)))
    for key in ("public_post", "manager_note", "talking_points", "commitment", "ask", "invite", "agenda"):
        for i, para in enumerate(as_paras(note.get(key))):
            out.append((f"{key}[{i}]", para))
    fb = note.get("feedback") or {}
    for key in ("observation", "impact", "next", "strength"):
        if fb.get(key):
            out.append((f"feedback.{key}", str(fb[key])))
    lm = note.get("light_moment") or {}
    for key in ("lead", "title"):
        if lm.get(key):
            out.append((f"light_moment.{key}", str(lm[key])))
    # Story Keeper booklets (keepsake.json)
    for key in ("subtitle", "dedication", "colophon", "intro"):
        if note.get(key):
            out.append((key, str(note[key])))

    def photo_text(prefix: str, p: dict) -> None:
        for key in ("caption", "alt", "credit"):
            if (p or {}).get(key):
                out.append((f"{prefix}.{key}", str(p[key])))

    photo_text("cover_photo", note.get("cover_photo") or {})
    for c, ch in enumerate(note.get("chapters") or []):
        for key in ("title", "when", "pullquote"):
            if ch.get(key):
                out.append((f"chapters[{c}].{key}", str(ch[key])))
        for i, para in enumerate(ch.get("story") or []):
            out.append((f"chapters[{c}].story[{i}]", str(para)))
        for i, p in enumerate(ch.get("photos") or []):
            photo_text(f"chapters[{c}].photos[{i}]", p)
        v = ch.get("voice") or {}
        for key in ("label", "transcript", "translation"):
            if v.get(key):
                out.append((f"chapters[{c}].voice.{key}", str(v[key])))
    cl = note.get("closing")
    if isinstance(cl, dict):
        for key in ("title", "signature"):
            if cl.get(key):
                out.append((f"closing.{key}", str(cl[key])))
        for i, para in enumerate(cl.get("body") or []):
            out.append((f"closing.body[{i}]", str(para)))
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

    texts = collect_text(note)
    if profile == "public" and note.get("public_post"):
        # Only the public post goes public; the private versions are checked without --profile public.
        texts = [(f, t) for f, t in texts if f.startswith("public_post")]
    for field, text in texts:
        for label, pattern in PII_PATTERNS.items():
            for m in re.finditer(pattern, text, flags=re.IGNORECASE):
                add("block", f"PII: {label}", field, m.group(0))
        for m in re.finditer(CURRENCY, text):
            add("block", "financial: amount", field, m.group(0))
        for t in word_hits(text, FINANCIAL_TERMS):
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
        if profile == "public":
            for label, pattern in PUBLIC_PATTERNS.items():
                for m in re.finditer(pattern, text):
                    level = "review" if label.startswith("a metric") else "block"
                    add(level, f"public: {label}", field, m.group(0))
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
    lm = note.get("light_moment") or {}
    if lm.get("title"):
        out_text = " ".join(str(lm.get(k, "")) for k in ("lead", "title"))
        for t in word_hits(out_text, HARSH_TERMS):
            issues.append({"level": "review", "category": "light moment: tone", "field": "light_moment", "match": t})
        if not lm.get("source"):
            issues.append({"level": "review", "category": "light moment: record the official or public-domain source",
                           "field": "light_moment", "match": "no source"})
        if profile == "comfort":
            issues.append({"level": "review", "category": "comfort: humour only if the user confirmed it's welcome, never for a fresh loss",
                           "field": "light_moment", "match": lm.get("title", "")})
    if profile == "feedback":
        fb = note.get("feedback") or {}
        for key, why in (("observation", "what you saw or heard, specifically"),
                         ("impact", "what it affected"),
                         ("next", "what to try next")):
            if not fb.get(key):
                issues.append({"level": "review", "category": f"feedback: add '{key}' ({why})",
                               "field": f"feedback.{key}", "match": "missing"})
    if profile == "repair":
        all_text = " ".join(t for _, t in collect_text(note)).lower()
        if not re.search(r"\bi(?:'m| am)? (?:sorry|apologi[sz]e)|\bmy (?:mistake|fault|bad)|\bi should have\b|\bi own\b", all_text):
            issues.append({"level": "review", "category": "repair: say plainly what you're sorry for, in the first person",
                           "field": "*", "match": "no first-person apology"})
        if not note.get("commitment"):
            issues.append({"level": "review", "category": "repair: add what you'll do differently ('commitment')",
                           "field": "commitment", "match": "missing"})
    if note.get("kind") == "intro" and note.get("body"):
        people = [p.get("name") for p in note.get("people") or [] if p.get("name")]
        opted = note.get("opted_in") or {}
        missing = [p for p in people if not opted.get(p)]
        if missing:
            issues.append({"level": "block", "category": "intro: double opt-in, so ask each person first and introduce only after both say yes",
                           "field": "opted_in", "match": ", ".join(missing)})
    if profile == "public":
        consent = note.get("consent") or {}
        if not consent.get("named_person_ok"):
            issues.append({"level": "block", "category": "public: confirm the colleague is happy to be named publicly (consent.named_person_ok)",
                           "field": "consent", "match": "not confirmed"})
        if not consent.get("company_policy_ok"):
            issues.append({"level": "review", "category": "public: check your company's social media policy (consent.company_policy_ok)",
                           "field": "consent", "match": "not confirmed"})
    if profile == "comfort" and note.get("fun_fact"):
        issues.append({"level": "block", "category": "comfort: no fun facts in a hard-time note",
                       "field": "fun_fact", "match": "fun_fact"})
    ff = note.get("fun_fact")
    if ff and not (isinstance(ff, dict) and ff.get("source")):
        issues.append({"level": "review", "category": "fun fact: record where it was verified (fun_fact.source)",
                       "field": "fun_fact", "match": "no source"})
    ff_text = ff.get("text") if isinstance(ff, dict) else ff
    if ff_text and len(str(ff_text).split()) > 45:
        issues.append({"level": "review", "category": "fun fact: keep it under about 35 words",
                       "field": "fun_fact", "match": str(len(str(ff_text).split()))})
    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("note", type=Path)
    ap.add_argument("--avoid", default="", help="comma-separated topics to avoid for this recipient")
    ap.add_argument("--json", action="store_true", help="print machine-readable output")
    ap.add_argument("--profile", choices=sorted(PROFILES), default="default",
                    help="extra checks: reconnect, team (team/org notes, tributes, kudos), family, grateful, comfort, "
                         "public (LinkedIn and other public posts), feedback, repair")
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
