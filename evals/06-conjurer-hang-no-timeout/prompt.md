---
runs: 2
max_turns: 8
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
model: sonnet
---

The checkout call sometimes hangs forever and nothing ever times out.
