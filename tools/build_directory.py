#!/usr/bin/env python3
"""Build the Claude plugin directory edition of PersonalAISkills.

The directory accepts scripts, fonts and other restricted files only from
Verified organizations. This repo keeps the full plugin (with its scripts) at
the root for Claude Code, and generates a Markdown-and-images-only copy in
``directory/personalaiskills/``, which is the folder submitted to the directory.

    python3 tools/build_directory.py build    # regenerate directory/personalaiskills
    python3 tools/build_directory.py check    # fail if it is stale or breaks a directory rule
    python3 tools/build_directory.py record   # save hand edits made in the output as patches

How the output is made from ``skills/``:

1. Files the directory refuses are dropped: ``scripts/``, fonts, audio.
2. Data files are converted: ``.svg`` -> ``.png`` (rsvg-convert), ``.jsonl``
   and ``.csv`` -> ``.json``, ``.vtt`` -> ``.txt``.
3. Markdown is patched with ``tools/directory/patches/**.diff``. Those patches
   replace every "run this script" step with instructions Claude follows itself.
   If a root file changes so a patch no longer applies, ``build`` and ``check``
   fail and say which file to update: edit the output file by hand, then run
   ``record``.
4. Files that exist only in the directory edition come from
   ``tools/directory/add/``. ``references/safety-checklist.md`` is generated
   from the term lists in ``skills/thankyou/scripts/safety_check.py``, and the
   routine prompts from ``skills/routines/scripts/make_routines.py``.
5. The plugin's README is the root README, patched the same way.

Needs Python 3.9+, git, and rsvg-convert (only when an SVG changed).
"""
from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import importlib.util
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_SKILLS = ROOT / "skills"
OUT = ROOT / "directory" / "personalaiskills"
TOOLS = ROOT / "tools" / "directory"
PATCHES = TOOLS / "patches"
ADD = TOOLS / "add"
MANIFEST = TOOLS / "manifest.json"

DROP_DIRS = {"scripts", "fonts", "__pycache__"}
DROP_SUFFIXES = {".py", ".pyc", ".woff", ".woff2", ".ttf", ".otf", ".m4a", ".mp3", ".mp4", ".wav", ".ogg", ".html"}
CONVERT = {".svg": ".png", ".jsonl": ".json", ".csv": ".json", ".vtt": ".txt"}
GENERATED = {"skills/thankyou/references/safety-checklist.md", "skills/routines/references/routine-prompts.md",
             "skills/routines/examples/team-lead/routines-plan.json"}

# The routine prompts come from make_routines.py, with each script step reworded.
# If one of these phrases disappears from the script, the build stops so the
# wording here can be updated.
ROUTINE_REWORDS = [
    ("read it with skills/feedback/scripts/growth_log.py",
     "read and edit it as described in skills/feedback/references/growth-log.md"),
    ("(skills/nudge/scripts/scan_transcript.py with --me \"{me}\")",
     "(reading it as in skills/nudge/references/transcript-scan.md, with me as the meeting owner)"),
    ("Run growth_log.py due --days 7 on my growth log",
     "List the follow-ups due in the next 7 days in my growth log (skills/feedback/references/growth-log.md)"),
    ("(growth_log.py summary)", "(the growth log summary)"),
    ("(skills/peer-pulse/scripts/pulse.py prompt)", "(skills/peer-pulse/references/prompt-and-tally.md)"),
    ("run pulse.py tally with --drafts and --evidence",
     "tally them as in skills/peer-pulse/references/prompt-and-tally.md, with thank-you drafts and Spotlight evidence"),
    ("run spotlight.py analyze, and run growth_log.py gaps for fairness",
     "run the pattern check (skills/spotlight/references/evidence-and-analysis.md), and the growth log's gaps check for fairness"),
]

TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
ROOT_FILES = {"LICENSE", "README.md", ".claude-plugin/plugin.json", ".claude-plugin/icon.png"}
MAX_TEXT_BYTES = 256 * 1024
MAX_FILES = 512


# ---------------------------------------------------------------- base copy

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}


def svg_to_png(src: Path, dst: Path) -> None:
    exe = shutil.which("rsvg-convert")
    if not exe:
        sys.exit(f"{src.relative_to(ROOT)} changed and rsvg-convert is not installed to convert it to PNG")
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([exe, "--zoom", "2", "--background-color", "white", "-o", str(dst), str(src)], check=True)
    strip_png(dst)


def strip_png(path: Path) -> None:
    """Keep only the chunks needed to draw the image: no text, time or EXIF chunks."""
    data = path.read_bytes()
    sig, keep = data[:8], {b"IHDR", b"PLTE", b"IDAT", b"IEND", b"tRNS", b"gAMA", b"sRGB", b"pHYs"}
    out, i = bytearray(sig), 8
    while i < len(data):
        n = int.from_bytes(data[i:i + 4], "big")
        kind = data[i + 4:i + 8]
        if kind in keep:
            out += data[i:i + 12 + n]
        i += 12 + n
        if kind == b"IEND":
            break
    path.write_bytes(bytes(out))


def convert_data(src: Path) -> str:
    text = src.read_text(encoding="utf-8")
    if src.suffix == ".jsonl":
        rows = [json.loads(line) for line in text.splitlines() if line.strip()]
    elif src.suffix == ".csv":
        rows = list(csv.DictReader(io.StringIO(text)))
    else:  # .vtt keeps its text
        return text
    return json.dumps(rows, ensure_ascii=False, indent=2) + "\n"


def build_base(dest: Path, manifest: dict, pngs_from: Path | None, rasterize: bool) -> dict:
    """Copy skills/ into dest/skills with drops and conversions. Returns the new manifest."""
    new_manifest = {}
    for src in sorted(SRC_SKILLS.rglob("*")):
        if src.is_dir():
            continue
        rel = src.relative_to(SRC_SKILLS)
        if DROP_DIRS & set(rel.parts[:-1]) or src.suffix.lower() in DROP_SUFFIXES or src.name == ".DS_Store":
            continue
        if src.name.startswith("OFL-") and "fonts" in rel.parts:
            continue
        out_rel = Path("skills") / rel
        suffix = src.suffix.lower()
        if suffix in CONVERT:
            out_rel = out_rel.with_suffix(CONVERT[suffix])
        dst = dest / out_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if suffix == ".svg":
            digest = sha(src.read_bytes())
            key = str(out_rel)
            new_manifest[key] = digest
            existing = pngs_from / out_rel if pngs_from else None
            if manifest.get(key) == digest and existing and existing.exists():
                shutil.copyfile(existing, dst)
            elif rasterize:
                svg_to_png(src, dst)
            else:
                sys.exit(f"{rel} is new or changed: run `python3 tools/build_directory.py build` to convert it")
        elif suffix in (".jsonl", ".csv", ".vtt"):
            dst.write_text(convert_data(src), encoding="utf-8")
        else:
            shutil.copyfile(src, dst)
    shutil.copyfile(ROOT / "README.md", dest / "README.md")
    return new_manifest


# ---------------------------------------------------------------- patches and extras

def apply_patches(dest: Path) -> None:
    for diff in sorted(PATCHES.rglob("*.diff")):
        run = subprocess.run(["git", "apply", "--whitespace=nowarn", "-p1", str(diff)],
                             cwd=dest, capture_output=True, text=True)
        if run.returncode != 0:
            target = diff.relative_to(PATCHES).with_suffix("")
            sys.exit(f"patch for {target} no longer applies: {target} changed in the full edition.\n"
                     f"Run `build --no-patches {target}`, edit {OUT.relative_to(ROOT)}/{target} by hand to match the "
                     f"directory edition, then run `record`.\n{run.stderr.strip()}")


def safety_checklist() -> str:
    spec = importlib.util.spec_from_file_location("safety_check", SRC_SKILLS / "thankyou/scripts/safety_check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    def terms(items) -> str:
        return ", ".join(f"`{t}`" for t in items)

    lines = [
        "# Safety checklist",
        "",
        "Go through this list for every note, post, card, booklet and log entry before you",
        "show it to the user. Read every visible field: quote, greeting, body, items,",
        "closing, signature, photo caption and alt text, fun fact, light moment, subject,",
        "short and channel versions, public post and manager note.",
        "",
        "If you can run code in your environment, you may write a quick pattern scan for the",
        "lists below to help, but the read-through is what counts. It is a backstop for",
        "judgement, not a replacement: a clean pass does not prove a note is safe.",
        "",
        "**Block** means fix it (abstract or remove) before the user sees the note.",
        "**Review** means read it again and change it unless it's clearly fine.",
        "Match terms as whole words or phrases, except where a list says it matches word starts.",
        "",
        "## Every note",
        "",
        "Block:",
        "",
        "- **Personal details:** email addresses, phone numbers, web links, numbers of six or more",
        "  digits (IDs, accounts), street addresses, and social handles (`@name`).",
        "- **Money amounts:** a currency sign with a number (`$`, `€`, `£`, `¥`, `₹`, `₩`), or a number",
        "  with `k`, `lakh`, `crore`, `USD`, `INR`, `EUR`, `GBP`, `dollars`, `rupees`, `euros`, `pounds`,",
        "  `yuan` or `yen`.",
        f"- **Financial terms:** {terms(mod.FINANCIAL_TERMS)}.",
        f"- **Health terms** (match word starts, so `diagnos` catches diagnosis): {terms(mod.HEALTH_TERMS)}.",
        f"- **Other sensitive topics** (word starts): {terms(mod.SENSITIVE_OTHER)}.",
        "- **The recipient's own topics to avoid:** anything the user said to steer clear of.",
        "",
        "Review:",
        "",
        f"- **Harsh or judgemental:** {terms(mod.HARSH_TERMS)}.",
        f"- **Clichés:** {terms(mod.CLICHES)}.",
        "- More than one `!` in the whole note.",
        "- A body over about 220 words.",
        "",
        "## Photos, sketches and stock images",
        "",
        "When the picture is a drawn sketch or a stock photo, block any wording that presents it as",
        f"a real photo of the moment: {terms(mod.REAL_PHOTO_CLAIMS)}. A stock photo needs its licence",
        "(and credit, if the licence asks) recorded.",
        "",
        "## Groups",
        "",
        "If the note names any member of the group, it must name every member (block). Otherwise",
        "it names no one.",
        "",
        "## Extra checks by kind of note",
        "",
        "Use the profile that fits, in addition to the checks above.",
        "",
    ]
    names = {
        "reconnect": "Reconnect check-ins", "team": "Team and org notes, tributes and kudos",
        "family": "Family notes", "grateful": "Gratitude lists", "comfort": "Comfort messages",
        "public": "Public posts (LinkedIn and others)", "feedback": "Feedback and growth-log entries",
        "repair": "Apologies and follow-ups",
    }
    for key, title in names.items():
        block, review = mod.PROFILES[key]
        lines += [f"### {title}", ""]
        for cat, items in block.items():
            lines.append(f"- Block, {cat}: {terms(items)}.")
        for cat, items in review.items():
            lines.append(f"- Review, {cat}: {terms(items)}.")
        extra = {
            "public": [
                "- Block: ticket or PR references (`#482`, `ABC-123`) and internal links (intranet, Jira,",
                "  Confluence, Slack, Teams, SharePoint, Lark/Feishu, Grafana, Datadog, PagerDuty, private IPs).",
                "- Review: metrics and numbers (`40%`, `3x`, `200 ms`, `10k users`): check they're public.",
                "- Block until the user confirms the colleague is happy to be named publicly.",
                "- Review until the user confirms the post fits their company's social media policy.",
                "- Check only the public post with this profile; private versions use the checks above.",
            ],
            "feedback": ["- Review: each piece of feedback needs what happened, what it affected and what to try next."],
            "repair": [
                "- Review: the note says plainly, in the first person, what the sender is sorry for.",
                "- Review: the note says what the sender will do differently.",
            ],
            "comfort": [
                "- Block: no fun fact in a hard-time note.",
                "- Review: a light moment only if the user confirmed humour is welcome, never for a fresh loss.",
            ],
        }.get(key, [])
        lines += extra + [""]
    lines += [
        "## Introductions",
        "",
        "Block an introduction until both people have said yes privately (double opt-in).",
        "",
        "## Fun facts and light moments",
        "",
        "- Review: a fun fact needs a record of where it was verified, and stays under about 35 words.",
        "- Review: a light moment needs its official or public-domain source, and a kind tone.",
        "",
        "## Then read it as the recipient",
        "",
        "Would they feel seen and happy? Would anything make them uncomfortable if someone read it",
        "over their shoulder? Does anything touch a trigger, or break a norm of their culture or the",
        "relationship? Would they be glad to see this photo?",
        "",
        "_This file is generated from the full edition's safety check, so both editions check the same things._",
        "",
    ]
    return "\n".join(lines)


def load_script(rel: str):
    spec = importlib.util.spec_from_file_location(Path(rel).stem, SRC_SKILLS / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def reword_routines(text: str, me: str) -> str:
    for old, new in ROUTINE_REWORDS:
        old = old.replace("{me}", me)
        text = text.replace(old, new)
    return text


def routine_plan(cfg: dict) -> list[dict]:
    mod = load_script("routines/scripts/make_routines.py")
    me = cfg["me"]["name"]
    plan = mod.plan(cfg, None)
    for r in plan:
        r["prompt"] = reword_routines(r["prompt"], me)
    return plan


def routine_prompts_md() -> str:
    mod = load_script("routines/scripts/make_routines.py")
    cfg = {"me": {"name": "<name>", "role": "<role>"}, "timezone": "<time zone>", "team": ["<first names>"],
           "sources": {"<kind>": "<source>"}, "channels": {"<kind of message>": "<where it goes>"},
           "growth_log": "<where the growth log lives>", "max_items": 5,
           "meeting": {"name": "<meeting>", "transcript_source": "<where its transcripts are>"}}
    prompts = mod.routine_prompts(cfg)
    raw = " ".join(p["task"] for p in prompts.values()) + mod.context({**cfg, "growth_log": "x.jsonl"})
    for old, _ in ROUTINE_REWORDS:
        if old.replace("{me}", "<name>") not in raw:
            sys.exit(f"make_routines.py no longer says {old!r}: update ROUTINE_REWORDS in tools/build_directory.py")
    ctx_file = reword_routines(mod.context({**cfg, "growth_log": "team-growth.jsonl"}), "<name>")
    local_sentence = re.search(r"My private growth log: .*?items I approve\)\.", ctx_file).group(0)
    ctx_tool = reword_routines(mod.context(cfg), "<name>")
    lines = [
        "# Routine prompts and schedules",
        "",
        "Build each routine from the user's answers (`routines.json`, as in",
        "`examples/team-lead/routines.json`). A scheduled run starts fresh, with no memory",
        "of this conversation, so each prompt carries everything it needs.",
        "",
        "## The schedule",
        "",
        "- A 5-field cron expression in the user's time zone, written as",
        "  `CRON_TZ=<time zone> <minute> <hour> <day of month> <month> <day of week>`.",
        "- Days: `weekdays` (1-5), `daily` (*), day names such as `fri` or `fri,mon`",
        "  (Sunday is 0), `monthly <day>` (that day of every month), or `quarterly <day>`",
        "  (that day of January, April, July and October). Monthly and quarterly runs",
        "  pin the day of the month and leave the day of the week as *.",
        "- Times like 8:40, 16:10 or 4:10pm. A time exactly on :00 or :30 moves a few",
        "  minutes earlier (by the length of the routine's name modulo 29, plus 1), so",
        "  runs aren't queued behind everyone else's.",
        "- A routine that reads a growth log kept as a file on the user's computer",
        "  (the daily brief, Monday follow-ups, quarterly Spotlight) must run on that computer.",
        "",
        "## The plan to show the user",
        "",
        "```text",
        "<N> routine(s) for <name> (<time zone>):",
        "",
        "• <routine name>: <what it does>",
        "  <days> at <HH:MM>  [<cron>]  (runs on your computer: the growth log is a local file)",
        "",
        "Each run prepares drafts and sends you one review list. Nothing is sent without your yes.",
        "```",
        "",
        "## Each prompt",
        "",
        "Every prompt is four paragraphs: the context, the routine's task, the privacy",
        "rule, and the approval rule.",
        "",
        "**Context** (fill in the user's answers; leave out parts they didn't give):",
        "",
        "> " + ctx_tool,
        "",
        "When the growth log is a file on their computer (here `team-growth.jsonl`), its sentence reads:",
        "",
        "> " + local_sentence,
        "",
        "**Privacy rule:**",
        "",
        "> " + mod.PRIVACY_RULE,
        "",
        "**Approval rule:**",
        "",
        "> " + mod.APPROVAL_RULE,
        "",
        "## The routines",
        "",
    ]
    for key, p in prompts.items():
        lines += [f"### {p['title']} (`{key}`)", "", p["what"] + ".", "", "> " + reword_routines(p["task"], "<name>"), ""]
    lines += ["_This file is generated from the full edition's routine builder, so both editions schedule the same routines._", ""]
    return "\n".join(lines)


def add_extras(dest: Path) -> None:
    for src in sorted(ADD.rglob("*")):
        if src.is_file():
            dst = dest / src.relative_to(ADD)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
    (dest / "skills/thankyou/references/safety-checklist.md").write_text(safety_checklist(), encoding="utf-8")
    (dest / "skills/routines/references/routine-prompts.md").write_text(routine_prompts_md(), encoding="utf-8")
    cfg = json.loads((SRC_SKILLS / "routines/examples/team-lead/routines.json").read_text(encoding="utf-8"))
    (dest / "skills/routines/examples/team-lead/routines-plan.json").write_text(
        json.dumps(routine_plan(cfg), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    shutil.copyfile(ROOT / "LICENSE", dest / "LICENSE")
    (dest / ".claude-plugin").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT / ".claude-plugin/icon.png", dest / ".claude-plugin/icon.png")
    manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
    manifest["homepage"] = "https://github.com/hardikashah-eng/personalaiskills/tree/main/directory/personalaiskills"
    (dest / ".claude-plugin/plugin.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")


def generate(dest: Path, rasterize: bool, patches: bool = True) -> dict:
    manifest = build_base(dest, load_manifest(), OUT if OUT.exists() else None, rasterize)
    if patches:
        apply_patches(dest)
    add_extras(dest)
    return manifest


# ---------------------------------------------------------------- directory rules

INSTALL = re.compile(r"\b(pip3?|pipx|uv|npm|pnpm|yarn|npx|brew|apt(-get)?|dnf|yum|winget|choco|scoop|port|conda|gem|cargo)"
                     r"\s+(install|add|i)\b|\bcurl\b[^\n]*\|\s*(ba)?sh|\bwget\b", re.I)
SCRIPT_REF = re.compile(r"\bpython3?\s|\b[\w-]+\.py\b|\bscripts/|\bgh (api|auth|pr)\b|\bffmpeg\b|\bffprobe\b|\bPillow\b|\.woff2?\b")
LINK = re.compile(r"\]\(([^)\s#]+)(?:#[^)]*)?\)")
PATH_TOKEN = re.compile(r"`((?:references|examples|assets)/[\w./-]+\.(?:md|json|png|jpg|txt))`")
BAD_NAMES = {"requirements.txt", "package.json", "package-lock.json", "pnpm-workspace.yaml", "pnpm-lock.yaml",
             "yarn.lock", "pipfile", "pipfile.lock", "pyproject.toml", "setup.py", "hooks.json", ".mcp.json",
             ".lsp.json", "monitors.json", "gemfile", "cargo.toml", "go.mod"}
RESERVED = re.compile(r"^(con|prn|aux|nul|com\d|lpt\d)(\.|$)", re.I)
SAFE_PATH = re.compile(r"^[A-Za-z0-9._/-]+$")


def lint(root: Path) -> list[str]:
    problems = []
    files = [p for p in root.rglob("*") if p.is_file()]
    if len(files) > MAX_FILES:
        problems.append(f"{len(files)} files; the directory allows {MAX_FILES}")
    for p in files:
        rel = p.relative_to(root).as_posix()
        suffix = p.suffix.lower()
        data = p.read_bytes()
        if not SAFE_PATH.match(rel) or any(RESERVED.match(part) for part in rel.split("/")):
            problems.append(f"{rel}: path has a character or name some computers can't keep")
        if p.name.lower() in BAD_NAMES:
            problems.append(f"{rel}: package or tool config file")
        if "/.claude/" in f"/{rel}" or (".claude-plugin" in rel and not rel.startswith(".claude-plugin/")):
            problems.append(f"{rel}: only the plugin's own .claude-plugin folder is allowed")
        if rel.startswith(".claude-plugin/") and rel not in ROOT_FILES:
            problems.append(f"{rel}: .claude-plugin may hold only plugin.json and the icon")
        if suffix in IMAGE_SUFFIXES:
            if b"PK\x03\x04" in data:
                problems.append(f"{rel}: image looks like it holds a zip archive")
            if suffix == ".png":
                end = data.find(b"IEND")
                if end == -1 or len(data) > end + 8:
                    problems.append(f"{rel}: PNG has data after its end")
            continue
        if suffix not in TEXT_SUFFIXES and rel != "LICENSE":
            problems.append(f"{rel}: not Markdown, text, JSON, YAML or an allowed image")
            continue
        if b"\x00" in data:
            problems.append(f"{rel}: NUL bytes")
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            problems.append(f"{rel}: not UTF-8")
            continue
        if text.startswith("#!"):
            problems.append(f"{rel}: starts with #!")
        if len(data) > MAX_TEXT_BYTES:
            problems.append(f"{rel}: over 256 KB")
        for n, line in enumerate(text.splitlines(), 1):
            if INSTALL.search(line):
                problems.append(f"{rel}:{n}: install command (link to the tool's own instructions instead)")
            if SCRIPT_REF.search(line):
                problems.append(f"{rel}:{n}: refers to a script or tool the directory edition doesn't ship")
        if suffix == ".md":
            for target in LINK.findall(text):
                if re.match(r"^[a-z]+:", target):
                    continue
                if not (p.parent / target).exists():
                    problems.append(f"{rel}: broken link {target}")
            skill_dir = root / "/".join(rel.split("/")[:2]) if rel.startswith("skills/") else root
            for token in PATH_TOKEN.findall(text):
                if not ((p.parent / token).exists() or (skill_dir / token).exists()):
                    problems.append(f"{rel}: refers to {token}, which isn't in this edition")
        if suffix == ".json":
            try:
                json.loads(text)
            except json.JSONDecodeError as exc:
                problems.append(f"{rel}: invalid JSON ({exc})")
    return problems


def compare(expected: Path, actual: Path) -> list[str]:
    diffs = []
    exp = {p.relative_to(expected).as_posix() for p in expected.rglob("*") if p.is_file()}
    act = {p.relative_to(actual).as_posix() for p in actual.rglob("*") if p.is_file()}
    for rel in sorted(exp - act):
        diffs.append(f"missing: {rel}")
    for rel in sorted(act - exp):
        diffs.append(f"unexpected: {rel}")
    for rel in sorted(exp & act):
        if (expected / rel).read_bytes() != (actual / rel).read_bytes():
            diffs.append(f"out of date: {rel}")
    return diffs


# ---------------------------------------------------------------- commands

def cmd_build(args) -> int:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / "out"
        manifest = generate(tmp, rasterize=True, patches=not args.no_patches)
        if args.no_patches:
            for rel in args.no_patches:
                src = tmp / rel
                if not src.exists():
                    sys.exit(f"{rel} is not in the output")
                (OUT / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, OUT / rel)
                print(f"reset {rel} to the unpatched root text; edit it, then run record")
            return 0
        if OUT.exists():
            shutil.rmtree(OUT)
        shutil.copytree(tmp, OUT)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    problems = lint(OUT)
    for p in problems:
        print(f"✗ {p}")
    print(f"built {OUT.relative_to(ROOT)} ({sum(1 for p in OUT.rglob('*') if p.is_file())} files)")
    return 1 if problems else 0


def cmd_check(_args) -> int:
    if not OUT.exists():
        sys.exit(f"{OUT.relative_to(ROOT)} is missing: run build")
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / "out"
        manifest = generate(tmp, rasterize=False)
        problems = compare(tmp, OUT)
    if manifest != load_manifest():
        problems.append("tools/directory/manifest.json is out of date: run build")
    problems += lint(OUT)
    for p in problems:
        print(f"✗ {p}")
    if problems:
        print("\nThe directory edition is stale or breaks a directory rule. Run "
              "`python3 tools/build_directory.py build` and fix what it reports.")
        return 1
    print(f"✓ {OUT.relative_to(ROOT)} is up to date and follows the directory rules")
    return 0


def cmd_record(_args) -> int:
    """Diff each edited Markdown file in the output against the unpatched base and save it as a patch."""
    with tempfile.TemporaryDirectory() as td:
        base = Path(td) / "base"
        build_base(base, load_manifest(), OUT, rasterize=False)
        added = {p.relative_to(ADD).as_posix() for p in ADD.rglob("*") if p.is_file()} if ADD.exists() else set()
        if PATCHES.exists():
            shutil.rmtree(PATCHES)
        count = 0
        for out_file in sorted(p for p in OUT.rglob("*") if p.suffix in TEXT_SUFFIXES):
            rel = out_file.relative_to(OUT).as_posix()
            if rel in GENERATED or rel in added or not (rel.startswith("skills/") or rel == "README.md"):
                continue
            base_file = base / rel
            if not base_file.exists():
                dst = ADD / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(out_file, dst)
                print(f"new file → tools/directory/add/{rel}")
                continue
            if base_file.read_bytes() == out_file.read_bytes():
                continue
            a = base_file.read_text(encoding="utf-8").splitlines(keepends=True)
            b = out_file.read_text(encoding="utf-8").splitlines(keepends=True)
            if (a and not a[-1].endswith("\n")) or (b and not b[-1].endswith("\n")):
                sys.exit(f"{rel}: end the file with a newline before recording")
            diff = "".join(difflib.unified_diff(a, b, f"a/{rel}", f"b/{rel}", n=2))
            dst = PATCHES / f"{rel}.diff"
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(diff, encoding="utf-8")
            count += 1
        for rel in sorted(added):
            out_file = OUT / rel
            if out_file.exists():
                shutil.copyfile(out_file, ADD / rel)
    print(f"recorded {count} patch(es) in {PATCHES.relative_to(ROOT)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="regenerate directory/personalaiskills")
    b.add_argument("--no-patches", nargs="+", metavar="FILE",
                   help="reset these output files (e.g. skills/kudos/SKILL.md) to the unpatched root text")
    sub.add_parser("check", help="fail if the output is stale or breaks a directory rule")
    sub.add_parser("record", help="save hand edits in the output as patches")
    args = ap.parse_args()
    return {"build": cmd_build, "check": cmd_check, "record": cmd_record}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
