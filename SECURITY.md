# Security Policy

## What this repository contains

nen is a markdown skill pack plus one POSIX installer script. The skills themselves execute nothing — agents read them as instructions. The two surfaces worth scrutiny:

- **`install.sh`** — fetched and piped to `sh` by the README one-liner. It downloads the repo tarball over HTTPS from GitHub, copies markdown files, and appends marker-delimited blocks to agent config files. It never elevates privileges, never touches credentials, and is idempotent. Read it before running it; that advice applies to every `curl | sh` on the internet, including this one.
- **Skill content** — the SKILL.md files instruct AI agents. A malicious edit to them is a prompt-injection vector for anyone who installs the pack, which is why `main` is the only supported channel and every change lands through the lint and adapter-sync gates.

## Supported versions

Only the `main` branch. There are no backported fixes.

## Reporting a vulnerability

Use GitHub's private vulnerability reporting on this repository (Security → Report a vulnerability). Reports are handled best-effort by a single maintainer — expect an acknowledgment within a few days, not hours. Please do not open public issues for exploitable problems in `install.sh`.
