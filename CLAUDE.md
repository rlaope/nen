# CLAUDE.md

## What this repo is — and is not

nen ships six installable agent skills: engineering disciplines that borrow their names from the six Nen categories in Hunter x Hunter. The anime is a naming metaphor and nothing more. This is **not** a fan-fiction, lore, or anime project — never generate Hunter x Hunter story content, character material, or derivative anime assets here. The repo's own quality rule applies to every file: delete every Nen reference and what remains must still stand as a serious engineering document.

## Source of truth and generated files

- `skills/<name>/SKILL.md` is the single source of truth. The skills: enhancer, transmuter, emitter, specialist, conjurer, manipulator, hatsu (forges new skills — route "add a skill" work through it), en (auto-routing — reads the problem shape and engages abilities), and vow (pre-commitment — falsifiable pledges declared before work, audited before any done claim).
- `AGENTS.md` and `.cursor/rules/*.mdc` are **generated** — never edit them by hand. After changing any skill, regenerate: `python3 scripts/gen-adapters.py`
- `install.sh` wires the skills into agent runtimes at install time. Keep it POSIX sh (no bashisms) and BSD/macOS-compatible (no GNU-only flags — BSD sed has already bitten this repo once).

## The skill contract (enforced by scripts/lint-skills.py)

- Frontmatter: exactly two keys, `name` (== directory name) and `description`; the description must contain an explicit "Use when" trigger clause and is deliberately assertive.
- Body: six H2 sections in this order — `Stance`, `Boundaries`, `Method`, `Worked trace`, `Anti-patterns`, `Done means`. `Worked trace` needs at least one fenced code block. `Boundaries` must name each paired sibling; the adjacency graph lives in the lint.
- Repository content is English only — the lint rejects Hangul in any tracked file.
- Length is guidance (~60–150 body lines). Padding to reach a length is a defect; so is thinness that skips the craft.

## Gates — run before every commit

```sh
python3 scripts/lint-skills.py --release
python3 scripts/gen-adapters.py --check
claude plugin validate .claude-plugin/plugin.json --strict   # when the claude CLI is available
```

CI runs the first two on every push; a red check on main is a stop-everything event. The plugin validator emits one **known, accepted warning** — "CLAUDE.md at the plugin root is not loaded as project context" — because this repo doubles as its own plugin root and CLAUDE.md is contributor context, not plugin cargo. That single warning is expected; any other warning or error is a failure.

## Git conventions

- Commits are authored as `rlaope <105429536+rlaope@users.noreply.github.com>` via repo-local git config. Do **not** add AI co-author trailers to commit messages.
- Conventional commits (`feat(scope):`, `fix(scope):`, `docs:`, `chore:`), one purpose per commit, split rather than bundled.

## IP note

`assets/nen-hexagon.png` is rights-holder material explicitly excluded from the MIT grant (see README). Never present it as MIT-licensed and never generate derivative versions of it.
