---
type: llm
focus: last_message
weight: 1
---

The response treats the p99 regression as a measurement problem, not a guessing problem. The working directory contains no code or dashboards, so asking for access to metrics, traces, profiles, or the deploy diff is itself a measurement-first move and counts toward a pass. Award a pass only if all of the following hold:

1. The first concrete steps are about measurement: profiling the affected path, comparing latency before vs. after the deploy, isolating which endpoints or operations regressed, diffing the deploy's changes against the measured hot path, or asking for the metrics/traces/deploy diff needed to do so.
2. It does NOT commit to a specific code fix (caching, pool sizing, query rewrites, adding an index, etc.) before any measurement has been proposed or taken. Listing hypotheses to test is fine; prescribing a fix as the answer is not.
3. It engages with tail latency specifically in some observable way — e.g. it considers that only some requests may be slow, mentions percentiles, saturation, queueing, or a subset of traffic being affected.

Fail if the response is a generic checklist of optimizations, or if it names a root cause with confidence without proposing any way to verify it.
