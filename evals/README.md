# nen — trigger-precision eval suite

Routing-precision evals for the nen skill pack, runnable with `claude plugin eval`.
Each case feeds the agent a prompt that should route to exactly one nen skill (or, for
the negative case, to none) and grades whether that skill's discipline is visibly
applied in the answer.

`plugin eval` is currently in early access; enable it with the
`CLAUDE_CODE_WALNUT_SPIRE=1` environment variable.

## Running

From the repo root:

```sh
# full suite (each case runs its own `runs:` count, currently 2)
CLAUDE_CODE_WALNUT_SPIRE=1 claude plugin eval .

# one case, one run (cheap smoke test)
CLAUDE_CODE_WALNUT_SPIRE=1 claude plugin eval . --case "06-*" --runs 1

# scaffolded cases (02, 05): --scaffold seeds their dummy repos, and the
# operator grant unlocks the gated tools the runner needs for executed proof
CLAUDE_CODE_WALNUT_SPIRE=1 claude plugin eval . --case "02-*" --runs 1 --scaffold --allow-tools Bash Write Edit

# measure uplift: run every case twice, with the plugin and without,
# and report the score delta (the headline number is the with-minus-without delta)
CLAUDE_CODE_WALNUT_SPIRE=1 claude plugin eval . --ablation with-without

# stronger judge for trusted runs (default judge is haiku; agent model is sonnet,
# so prefer a judge that is not the agent model)
CLAUDE_CODE_WALNUT_SPIRE=1 claude plugin eval . --ablation with-without --judge-model opus
```

Useful extras: `--verbose` streams the trace, `--json` dumps the full result,
`--report out.html` writes an HTML report, `--keep-temp` preserves the sandbox dirs.

Results are written to `evals/results/<timestamp>/` (gitignored — do not commit them).

## How it works

Most cases are a directory with `prompt.md` (frontmatter: `runs`, `max_turns`,
`timeout_seconds`, `allowed_tools`, `model`; body: the user prompt) plus
`graders/*.md` (frontmatter `type: llm | regex | tool_used | file_exists | ...`).
Cases run in a sandbox cwd with an isolated home.

Cases `02` and `05` use the YAML case form instead (`case.yaml` with
`schema_version: "1.0"` and `execution.prompt`) because only that form supports
scaffolding: `context.scaffold_script` names a script file relative to the case
dir (`scaffold.sh`, committed and reviewable) that seeds a small dummy repo — a
tangled service file guarded by a mock-theater test, and an idempotency-free
webhook handler beside provider docs stating at-least-once delivery. Two flags
gate the full path, by design: `--scaffold` runs the seed script (author-supplied
bash, executed as you — only pass it on case files you trust), and
`--allow-tools Bash Write Edit` is the operator grant for the gated tools the
runner needs to produce executed red-then-green proof; a case requesting them in
`allowed_tools` is not enough on its own. In the YAML form `plugins` entries are
paths relative to the case dir, so both cases pin `plugins: ["../.."]` to load
the repo's own plugin. Without the flags those two cases degrade honestly: the
skill still fires and diagnoses from the seeded files, but the discipline grader
fails the run for claiming no proof it could not produce.

The remaining rubrics accept either a substantive discipline-conformant answer or
a discipline-conformant request for the missing artifact — but always fail
wrong-discipline framing.

Every case carries:

- one scored `llm` outcome grader — the rubric checks that the expected skill's
  discipline is observable in the final answer (graded on outcome, not trajectory);
- one `tool_used: Skill` trigger check (`input_match: <skill>`) — a signal that the
  skill actually fired; under `--ablation` the runner reports it but excludes it from
  the score in both arms, so it never moves the delta.

Score semantics per positive case (plain, non-ablation run): both graders carry
weight 1, so **1.0** = the skill fired AND its discipline is visible in the answer;
**0.5** = exactly one of the two (either the discipline leaked through without the
skill, or the skill fired but its discipline is not observable in the reply);
**0.0** = neither — a true routing miss. Half scores are findings, not noise: they
localize whether the trigger surface or the skill body needs work. Expect run-to-run
variance at `runs: 2`; raise `runs` before drawing conclusions from a single number.

## Cases

| case | expected skill | what the grader checks |
|---|---|---|
| `01-enhancer-p99-spike` | enhancer | p99 regression handled measurement-first: profile / compare before-after / ask for metrics; no prescribed fix before measurement; engages with tail latency specifically |
| `02-transmuter-tangled-service` | transmuter | characterization tests before restructuring; refactor separated from the new plan-type feature; behavior preserved; no from-scratch rewrite |
| `03-emitter-launch-post` | emitter | won't fabricate a generic feature-list announcement: asks what/for-whom is launching, or anchors draft copy in a named audience and a concrete before -> after |
| `04-specialist-sdk-batching` | specialist | reads the artifact instead of guessing: inspect SDK source / capture traffic / grep for the constant; any cause stated only as a hypothesis to verify |
| `05-conjurer-webhook-double-fire` | conjurer | treats double-fire as at-least-once delivery; fix is idempotency/dedup with a named mechanism; proves it with a duplicate-delivery test |
| `06-conjurer-hang-no-timeout` | conjurer (trap: not enhancer) | bounds the wait with an explicit timeout and handles what happens when it fires (safe-retry/double-charge risk); fails if framed as profiling/latency work; plus a secondary regex that "timeout/deadline" is named |
| `07-manipulator-migration-split` | manipulator | decomposes into independently verifiable workstreams with checkable outputs; addresses independence/integration; audits subagent "done" claims |
| `08-neg-http-418` | none (should NOT fire) | scored: correct, proportionate trivia answer (teapot / RFC 2324) with no engineering ceremony, and a trace regex asserting no nen skill was invoked; plus a display `tool_used` check expecting 0 nen-skill invocations |

Case `08` is the over-triggering canary: in an `--ablation` run its with-plugin arm
loses points only if the plugin fires a skill on a prompt that deserves a one-line
answer.

## Editing guidelines

- The plugin under test is read-only: eval work never touches `skills/`,
  `scripts/`, or the manifests — only `evals/`.
- Keep at least one should-NOT-fire case in the suite.
- Every case keeps at least one outcome grader; `tool_used` is never the only grader.
- `runs: 2` per case keeps the suite cheap; raise to 3+ for lower-variance numbers.
- Keep `timeout_seconds` generous — an under-set timeout reads as a 0 score, not a
  timeout.
