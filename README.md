# nen

Skill packs that give an AI coding agent a discipline — six abilities, one per Nen category.

![The six Nen categories](assets/nen-hexagon.png)

## What this is

In *Hunter x Hunter*, every fighter's aura falls into one of six Nen categories, and mastery means knowing which category a problem belongs to. **nen** maps those six categories to six engineering disciplines and ships each one as an installable agent skill: a stance, a method, hard boundaries, and a worked trace that shows the discipline actually being applied.

v0.1 ships **skills only** — no runtime, no hooks, no MCP servers. Each skill is a single portable `SKILL.md` that any [Agent Skills](https://agentskills.io)-compatible agent can read. Claude Code gets first-class packaging on top; everything else just reads the files.

## The six categories

| Category | Discipline | Skill | Invocation |
|---|---|---|---|
| Enhancement 強化系 | Profiling-first performance engineering — baseline, profile, change one thing, re-measure | [enhancer](skills/enhancer/) | `/nen:enhancer` |
| Transmutation 変化系 | Behavior-preserving refactoring under characterization tests, plus severity-rated code review | [transmuter](skills/transmuter/) | `/nen:transmuter` |
| Emission 放出系 | Launch, positioning, and promotion — making finished work land with the audience that should care | [emitter](skills/emitter/) | `/nen:emitter` |
| Specialization 特質系 | Reverse engineering and mechanism-comparison research — when the docs run out, read the artifact | [specialist](skills/specialist/) | `/nen:specialist` |
| Conjuration 具現化系 | Failure-mode-driven reliability engineering — enumerate how it breaks, prove every handler with a test | [conjurer](skills/conjurer/) | `/nen:conjurer` |
| Manipulation 操作系 | Orchestration for multi-agent and deep-research work — decomposition, routing, verified delegation | [manipulator](skills/manipulator/) | `/nen:manipulator` |

The skills know about each other. Each one's **Boundaries** section names the sibling disciplines it hands off to — enhancer locks in the benchmark and hands the restructuring to transmuter; specialist decodes the mechanism before conjurer enumerates how it fails. The hand-off graph is enforced by the lint, not left to prose.

## Install

**Claude Code — plugin (recommended).** Managed updates, namespaced `/nen:*` commands:

```
/plugin marketplace add rlaope/nen
/plugin install nen@nen
```

**Claude Code — manual.** Clone into your skills directory; loads as `nen@skills-dir`, still namespaced:

```sh
git clone https://github.com/rlaope/nen.git ~/.claude/skills/nen
```

**Any other agent supporting Agent Skills.** Point it at `skills/<name>/SKILL.md`. The `.claude-plugin/` manifests are additive Claude Code packaging that other agents simply ignore — the skills themselves are plain frontmatter-plus-markdown.

## Usage

Skills auto-activate when your request matches a skill's description, or invoke one explicitly:

```
/nen:conjurer harden the webhook consumer before launch
```

A design stance, stated honestly: the descriptions are written deliberately assertive, because skills under-trigger by default — a timid description means the discipline never fires when it should. The cost of the aggressive side is bounded: if a skill fires on the wrong problem, its Boundaries section recognizes that and hands off to the right sibling instead of plowing ahead.

## Context cost

Installing all six skills adds **~1,075 tokens** of always-on context to every session — the frontmatter descriptions the agent scans for trigger matching. A skill's full body (~2.5k–3.5k tokens) is loaded only when that skill fires. Measured on the plugin-dir install path:

```sh
cd nen && claude --plugin-dir . plugin details nen
```

## Repository layout

```
nen/
├── .claude-plugin/
│   ├── plugin.json          # Claude Code plugin manifest
│   └── marketplace.json     # marketplace listing (source: ./)
├── assets/
│   └── nen-hexagon.png
├── scripts/
│   └── lint-skills.py       # structural lint; --release runs the full gate
└── skills/
    └── <name>/SKILL.md      # one file per skill, six skills
```

## Contributing

No separate CONTRIBUTING.md yet — the conventions fit here, and the lint enforces all of them:

- **Frontmatter** holds exactly two keys: `name` (must equal the directory name) and `description`. The description must contain an explicit "Use when" trigger clause.
- **Body** has six required H2 sections in this order: `Stance`, `Boundaries`, `Method`, `Worked trace`, `Anti-patterns`, `Done means`. Extra sections are allowed; the required six keep their relative order.
- `Worked trace` needs at least one fenced code block — a discipline you can't show in a transcript isn't one.
- `Boundaries` must name each sibling skill it hands off to; the adjacency graph lives in the lint.
- Repository content is English only.

Run the lint before sending a PR:

```sh
python3 scripts/lint-skills.py --release
```

## License & disclaimer

Skill content is MIT-licensed — see [LICENSE](LICENSE).

This is an unofficial fan project, not affiliated with or endorsed by the Hunter x Hunter rights holders. `assets/nen-hexagon.png` is a rights-holder image and is **not** covered by the MIT grant.

## Roadmap

v0.2 candidates: trigger-precision evals (`claude plugin eval`) to measure how accurately each skill fires, and an original SVG recreation of the hexagon to replace the rights-holder image.
