# nen

Skill packs that give an AI coding agent a discipline — six abilities, one per Nen category.

![The six Nen categories](assets/nen-hexagon.png)

## What this is

In *Hunter x Hunter*, every fighter's aura falls into one of six Nen categories, and mastery means knowing which category a problem belongs to. **nen** maps those six categories to six engineering disciplines and ships each one as an installable agent skill: a stance, a method, hard boundaries, and a worked trace that shows the discipline actually being applied.

v0.1 ships **skills only** — no runtime, no hooks, no MCP servers. Each skill is a single portable `SKILL.md`, and the installer wires the same six files into whatever agent you run: Claude Code, Codex CLI, Cursor, OpenCode, Gemini CLI, Qwen Code, Kimi CLI, Antigravity, Pi, GitHub Copilot, or anything that reads an `AGENTS.md`-style instructions file. One skill text, every runtime.

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

### One-line install

```sh
curl -fsSL https://raw.githubusercontent.com/rlaope/nen/main/install.sh | sh
```

Adaptive by design: the script detects every agent on your machine — Claude Code, Codex CLI, Cursor, OpenCode, Gemini CLI, Qwen Code, and anything in the `AGENTS.md` family — and wires the skills into each one it finds. Skill bodies land in `~/.nen/skills/`; each agent gets only a small routing block (name + trigger description + "read the SKILL.md first"), so full bodies load on demand. Re-running the installer updates in place.

### Ask your agent

Paste this into whatever coding agent you use and let it install nen for its own environment:

```text
Install the nen skill pack from https://github.com/rlaope/nen into this environment.

1. Fetch the repo: git clone --depth 1 https://github.com/rlaope/nen.git /tmp/nen
   (or download and extract https://codeload.github.com/rlaope/nen/tar.gz/refs/heads/main).
2. Copy the six skill files to ~/.nen/skills/<name>/SKILL.md
   (enhancer, transmuter, emitter, specialist, conjurer, manipulator).
3. Wire them into YOUR runtime, whichever you are:
   - Claude Code: copy the whole repo to ~/.claude/skills/nen instead — it loads
     as a namespaced plugin (/nen:<skill>).
   - Cursor: for each skill create .cursor/rules/nen-<name>.mdc — frontmatter
     description = the skill's description, alwaysApply: false, body = the
     SKILL.md body without its frontmatter.
   - Any agent with an instructions file (AGENTS.md, GEMINI.md, QWEN.md,
     copilot-instructions.md, ...): append a "nen skills" section listing each
     skill's name, its ~/.nen/skills path, and its description, plus this rule:
     "when a task matches a description, read that SKILL.md first and follow
     its Method before acting."
4. Do not edit the SKILL.md files themselves.
5. Verify: list the six skills you installed and where each one landed.
```

### More ways

**Claude Code plugin** — managed updates, namespaced `/nen:*` commands:

```
/plugin marketplace add rlaope/nen
/plugin install nen@nen
```

**Already wired in-repo.** Cloning the repo gives you working project-level setups out of the box: `AGENTS.md` for anything that reads it (Codex, OpenCode, Antigravity, Kimi, OpenClaw, ...), `.cursor/rules/` for Cursor, `.claude-plugin/` for Claude Code. Copy any of them into your own project to vendor nen. These adapters are generated from `skills/` by `scripts/gen-adapters.py` — edit the skills, never the copies.

**Raw files.** The skills are plain frontmatter-plus-markdown in `skills/<name>/SKILL.md` — point any [Agent Skills](https://agentskills.io)-compatible runtime at them directly. The `.claude-plugin/` manifests and `install.sh` are additive packaging that other consumers simply ignore.

## Usage

Skills auto-activate when your request matches a skill's description, or invoke one explicitly:

```
/nen:conjurer harden the webhook consumer before launch
```

On runtimes without slash commands (Codex, OpenCode, Gemini CLI, Qwen Code, and the rest of the `AGENTS.md` family), the installed routing block auto-matches requests against the descriptions — or just say "use the nen conjurer skill".

A design stance, stated honestly: the descriptions are written deliberately assertive, because skills under-trigger by default — a timid description means the discipline never fires when it should. The cost of the aggressive side is bounded: if a skill fires on the wrong problem, its Boundaries section recognizes that and hands off to the right sibling instead of plowing ahead.

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
