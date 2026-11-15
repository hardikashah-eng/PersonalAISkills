#!/usr/bin/env python3
"""Format a ThankYou / Reconnect note for a delivery channel and build a share link.

It never sends anything. It prints the channel-ready text (and a subject line for
email) plus, where the app supports one, a link that opens the app with the
message filled in. The user taps the link and chooses to send.

Usage:
    python3 share.py note.json --channel whatsapp
    python3 share.py note.json --channel email --subject "Thank you, Maya"
    python3 share.py note.json --channel sms --to "+16195550123"   # number used only in the link
    python3 share.py note.json --channel slack --json

Channels: email, whatsapp, sms, imessage, telegram, line, signal, wechat,
kakaotalk, messenger, slack, teams, lark, linkedin, plain.

A phone number or email given with --to goes only into the printed link. It is
never written to a file.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

CHAT_APPS = {"whatsapp", "telegram", "line", "signal", "wechat", "kakaotalk", "messenger"}
WORK_CHAT = {"slack", "teams", "lark"}
SHORT = {"sms", "imessage", "linkedin"}
CHANNELS = sorted({"email", "plain"} | CHAT_APPS | WORK_CHAT | SHORT)

# Soft word limits per channel (beyond these, suggest a shorter version).
WORD_LIMITS = {"sms": 60, "imessage": 60, "linkedin": 110, "whatsapp": 130, "telegram": 130,
               "line": 130, "signal": 130, "wechat": 130, "kakaotalk": 130, "messenger": 130,
               "slack": 160, "teams": 160, "lark": 160}


def quote_lines(note: dict, style: str) -> list[str]:
    q = note.get("quote") or {}
    if not q.get("text"):
        return []
    text = f"“{q['text']}”"
    if style == "whatsapp":
        text = f"_{text}_"
    elif style == "slack":
        text = f"> {text}"
    lines = [text]
    if q.get("translation"):
        lines.append(("> " if style == "slack" else "") + q["translation"])
    if q.get("attribution"):
        lines.append(("> " if style == "slack" else "") + f"— {q['attribution']}")
    return lines + [""]


def as_list(value) -> list[str]:
    if not value:
        return []
    return [value] if isinstance(value, str) else list(value)


def body_for(note: dict, channel: str, post: bool = False) -> list[str]:
    """Paragraphs to use: a short or channel-post version when the note provides one."""
    if channel in WORK_CHAT and (post or note.get("audience") in ("team", "org")) and note.get("channel_post"):
        return [note["channel_post"]]
    if channel in SHORT and note.get("short_body"):
        return as_list(note["short_body"])
    return as_list(note.get("body"))


def format_text(note: dict, channel: str, post: bool = False, manager: bool = False) -> str:
    if manager:
        if not note.get("manager_note"):
            raise SystemExit("note.json has no manager_note")
        sig = note.get("sender_first_name") or note.get("signature") or ""
        return "\n\n".join(as_list(note["manager_note"]) + ([sig] if sig else [])).strip() + "\n"
    if channel == "linkedin" and note.get("public_post"):
        # A public post stands on its own: no greeting, sign-off or P.S.
        return "\n\n".join(as_list(note["public_post"])).strip() + "\n"
    sig = note.get("signature") or note.get("sender_first_name", "")
    closing = note.get("closing") or ""
    posting_to_group = (channel in WORK_CHAT and note.get("channel_post")
                        and (post or note.get("audience") in ("team", "org")))

    lines: list[str] = []
    if channel in ("email", "plain"):
        lines += quote_lines(note, "plain")
    elif channel == "whatsapp":
        lines += quote_lines(note, "whatsapp")
    elif channel in WORK_CHAT and not posting_to_group:
        lines += quote_lines(note, "slack")
    elif channel in CHAT_APPS:
        lines += quote_lines(note, "plain")
    # SMS, iMessage, LinkedIn: no quote, to keep it short.

    if note.get("title") and not posting_to_group:
        lines += [note["title"], ""]
    if not posting_to_group and note.get("greeting"):
        lines += [note["greeting"], ""]
    for para in body_for(note, channel, post):
        lines += [para, ""]
    if not posting_to_group:
        for it in note.get("items") or []:
            why = " ".join(x for x in (it.get("why"), it.get("difference")) if x)
            subject = it.get("subject", "")
            if channel == "whatsapp":
                subject = f"*{subject}*"
            elif channel in WORK_CHAT:
                subject = f"*{subject}*"
            lines.append(f"✦ {subject}" + (f" — {why}" if why else ""))
            if it.get("forward"):
                lines.append(f"   ↪ {it['forward']}")
            lines.append("")
    if posting_to_group:
        lines.append(f"— {sig}" if sig else "")
    else:
        if closing:
            lines.append(closing)
        if sig:
            lines.append(sig)
    lm = note.get("light_moment") or {}
    if lm.get("title") and channel not in ("sms", "imessage"):
        lines += ["", f"{lm.get('lead') or 'For a smile, whenever you want one:'} {lm['title']}"]
        if lm.get("url"):
            lines.append(lm["url"])
    ff = note.get("fun_fact")
    ff = (ff.get("text") if isinstance(ff, dict) else ff) or ""
    if ff.strip() and channel not in ("sms", "imessage"):
        lines += ["", f"P.S. {ff.strip()}"]
    return "\n".join(lines).strip() + "\n"


def default_subject(note: dict) -> str:
    if note.get("subject"):
        return note["subject"]
    if note.get("kind") == "gratitude":
        return note.get("title") or "What I'm grateful for"
    name = note.get("recipient_name") or note.get("recipient_first_name") or ""
    occasion = (note.get("occasion") or "").split("·")[-1].strip()
    if occasion and name:
        return f"{occasion}, {name}"
    return f"Thank you, {name}" if name else "Thank you"


def share_link(channel: str, text: str, to: str | None, subject: str | None) -> str | None:
    t = quote(text, safe="")
    if channel == "whatsapp":
        digits = re.sub(r"\D", "", to or "")
        return f"https://wa.me/{digits}?text={t}" if digits else f"https://wa.me/?text={t}"
    if channel in ("sms", "imessage"):
        addr = re.sub(r"[^\d+]", "", to or "")
        return f"sms:{addr}?&body={t}"
    if channel == "email":
        return f"mailto:{quote(to or '', safe='@')}?subject={quote(subject or '', safe='')}&body={t}"
    if channel == "telegram":
        return f"https://t.me/share/url?url=&text={t}"
    if channel == "line":
        return f"https://line.me/R/share?text={t}"
    return None  # Signal, WeChat, KakaoTalk, Messenger, LinkedIn, Slack, Teams, Lark: copy and paste


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("note", type=Path)
    ap.add_argument("--channel", required=True, choices=CHANNELS)
    ap.add_argument("--to", help="phone number or email, used only in the printed link")
    ap.add_argument("--subject", help="email subject (default from note.json or the occasion)")
    ap.add_argument("--post", action="store_true",
                    help="posting to a channel (#kudos, a team thread): use channel_post from note.json")
    ap.add_argument("--manager", action="store_true",
                    help="the note to the person's manager (manager_note in note.json)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    try:
        note = json.loads(args.note.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: cannot read {args.note}: {exc}", file=sys.stderr)
        return 2

    text = format_text(note, args.channel, args.post, args.manager)
    subject = (args.subject or default_subject(note)) if args.channel == "email" else None
    link = share_link(args.channel, text, args.to, subject)

    warnings = []
    words = len(text.split())
    limit = WORD_LIMITS.get(args.channel)
    if limit and words > limit:
        warnings.append(f"{words} words is long for {args.channel} (aim for under {limit}); "
                        "write a shorter version that keeps the specific moment"
                        + (" or add 'short_body' to note.json" if args.channel in SHORT else ""))
    if args.channel == "linkedin" and note.get("public_post"):
        warnings.append("public post: run safety_check.py --profile public first, and post only with the "
                        "colleague's OK to be named and within your company's social media policy")
        warnings.append("LinkedIn has no link that fills in post text: open https://www.linkedin.com/feed/, "
                        "select 'Start a post', and paste")
    elif args.channel in CHAT_APPS | SHORT | WORK_CHAT and not note.get("text_only"):
        warnings.append("send the card as an image (card_to_png.py) or the clean photo with the text")
    if link and len(link) > 2000:
        warnings.append("the link is very long; some apps may cut it off, so copy the text instead")

    if args.json:
        print(json.dumps({"channel": args.channel, "subject": subject, "text": text,
                          "link": link, "warnings": warnings}, ensure_ascii=False, indent=2))
        return 0

    print(f"== {args.channel} ==")
    if subject:
        print(f"Subject: {subject}\n")
    print(text)
    if link:
        print("Share link (opens the app with the message filled in; you choose to send):")
        print(link)
    else:
        print("No share link for this channel: copy the text above into the app.")
    for w in warnings:
        print(f"note: {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
