#!/usr/bin/env python3
"""Structural lint for the nen skill pack.

Usage: python3 scripts/lint-skills.py [--release]

Default mode lints whatever exists, skipping checks whose inputs are absent.
--release requires the complete tree and forbids any check from skipping.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RELEASE = "--release" in sys.argv

SKILLS = ["enhancer", "transmuter", "emitter", "specialist", "conjurer", "manipulator", "hatsu", "en"]

# Cross-skill hand-off adjacency. Every edge is bidirectional. Each skill's
# "## Boundaries" section must name each of its paired siblings.
PAIRS = {
    "enhancer": ["transmuter", "specialist", "conjurer"],
    "transmuter": ["enhancer", "conjurer", "specialist"],
    "emitter": ["manipulator", "conjurer"],
    "specialist": ["enhancer", "conjurer", "manipulator", "transmuter"],
    "conjurer": ["transmuter", "specialist", "emitter", "enhancer"],
    "manipulator": ["emitter", "specialist", "hatsu", "en"],
    "hatsu": ["manipulator"],
    "en": ["manipulator"],
}

# Required H2 sections, in contract order. Extra H2 sections are allowed;
# the required six must appear in this relative order.
SECTIONS = ["Stance", "Boundaries", "Method", "Worked trace", "Anti-patterns", "Done means"]

# The complete tracked tree. Doubles as the release file-count assertion and
# bounds the Hangul scan: the working tree may hold unrelated local state
# (e.g. .omc/) that is not repository content.
FILES = [
    ".claude-plugin/marketplace.json",
    ".claude-plugin/plugin.json",
    ".gitattributes",
    ".github/workflows/lint.yml",
    ".gitignore",
    "AGENTS.md",
    "CLAUDE.md",
    "LICENSE",
    "README.md",
    "SECURITY.md",
    "assets/agent-x-agent.png",
    "assets/nen-hexagon.png",
    "install.sh",
    "scripts/gen-adapters.py",
    "scripts/lint-skills.py",
] + [f"skills/{s}/SKILL.md" for s in SKILLS] + [
    f".cursor/rules/nen-{s}.mdc" for s in SKILLS
]

TRIGGER = re.compile(r"use (?:this skill )?when\b", re.I)
# Escaped range on purpose: a literal Hangul character class would make this
# script flag its own source on every run.
HANGUL = re.compile("[\uAC00-\uD7A3]")

errors = []
skipped = []


def fail(msg):
    errors.append(msg)


def section(body, heading):
    m = re.search(rf"^##\s+{re.escape(heading)}\s*$(.*?)(?=^##\s|\Z)", body, re.S | re.M)
    return m.group(1) if m else ""


present = [s for s in SKILLS if (ROOT / "skills" / s / "SKILL.md").exists()]
for s in present:
    text = (ROOT / "skills" / s / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        fail(f"{s}: no YAML frontmatter block")
        continue
    fm, body = m.groups()

    keys = re.findall(r"^([A-Za-z][\w-]*):", fm, re.M)
    extra = [k for k in keys if k not in ("name", "description")]
    if extra:
        fail(f"{s}: frontmatter must hold only name and description, found {extra}")
    name = re.search(r"^name:\s*(\S+)\s*$", fm, re.M)
    desc = re.search(r"^description:\s*(.+)$", fm, re.M)
    if not name or name.group(1) != s:
        fail(f"{s}: frontmatter name must equal the directory name")
    if not desc:
        fail(f"{s}: missing description")
    elif not TRIGGER.search(desc.group(1)):
        fail(f"{s}: description lacks an explicit 'Use when' trigger clause")

    found = re.findall(r"^##\s+(.+?)\s*$", body, re.M)
    missing = set(SECTIONS) - set(found)
    if missing:
        fail(f"{s}: missing required H2 sections {sorted(missing)}")
    elif [h for h in found if h in SECTIONS] != SECTIONS:
        fail(f"{s}: required H2 sections out of contract order (extras are allowed)")

    if "```" not in section(body, "Worked trace"):
        fail(f"{s}: '## Worked trace' needs at least one fenced code block")

    bounds = section(body, "Boundaries")
    for sib in PAIRS[s]:
        if sib not in bounds:
            fail(f"{s}: '## Boundaries' must name sibling '{sib}'")

    n = len(body.strip().splitlines())
    if not 40 <= n <= 220:
        print(f"  note: {s} body is {n} lines (guidance ~60-150)")

pj = ROOT / ".claude-plugin/plugin.json"
mj = ROOT / ".claude-plugin/marketplace.json"
if pj.exists() and mj.exists():
    try:
        pv = json.loads(pj.read_text(encoding="utf-8"))["version"]
        market = json.loads(mj.read_text(encoding="utf-8"))
        mv = market["version"]
        ev = market["plugins"][0]["version"]
        if not (pv == mv == ev):
            fail(f"version drift: plugin.json={pv} marketplace={mv} entry={ev}")
    except (KeyError, IndexError) as exc:
        fail(f"version parity: missing field {exc}")
else:
    skipped.append("version-parity")

readme = ROOT / "README.md"
if readme.exists():
    linked = set(
        re.findall(r"\]\(skills/([a-z-]+)/(?:SKILL\.md)?\)", readme.read_text(encoding="utf-8"))
    )
    if linked != set(SKILLS):
        fail(f"README drift: skill links resolve to {sorted(linked)}, expected all six skills")
else:
    skipped.append("readme-drift")

for rel in FILES:
    f = ROOT / rel
    if not f.exists() or rel.endswith(".png"):
        continue
    if HANGUL.search(f.read_text(encoding="utf-8", errors="ignore")):
        fail(f"Korean text in {rel} (repository content must be English)")

if RELEASE:
    absent = [rel for rel in FILES if not (ROOT / rel).exists()]
    if absent:
        fail(f"release: missing files {absent}")
    tracked = [rel for rel in FILES if (ROOT / rel).exists()]
    if len(tracked) != len(FILES):
        fail(f"release: expected {len(FILES)} files, found {len(tracked)}")
    if len(present) != len(SKILLS):
        fail(f"release: expected {len(SKILLS)} skills, found {len(present)}")
    for c in skipped:
        fail(f"release: check '{c}' was skipped")

for e in errors:
    print("FAIL:", e)
print("LINT OK" if not errors else f"LINT FAILED ({len(errors)})")
sys.exit(1 if errors else 0)
