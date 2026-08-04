---
type: llm
focus: last_message
weight: 1
---

The response applies orchestration discipline to decomposing work for delegation. The prompt names no specific migration, so the response may either ask what the migration is before decomposing, or present a decomposition framework with clearly-marked placeholder workstreams — both are acceptable shapes. Award a pass only if all of the following hold:

1. Workstreams are independently verifiable units: for each stream (or the template for one), the response states a checkable output — a passing command, a document with named required fields, a diff scoped to named files — not just a topic ("agent 1 handles the database"). If the response instead asks for the migration's specifics, it must say what it needs to know in order to cut verifiable seams (dependencies, shared files, done-criteria), not just "tell me more".
2. Independence and integration are addressed: which streams can truly run in parallel, where they collide (shared schema, shared config, ordering constraints), and how the pieces get integrated or sequenced at the end.
3. Verification of delegated work is explicit: the response does not treat an agent's "done" as done — it names how each stream's output will be checked on return (run the command, inspect the named fields, review the diff).

Fail if the response is three vague buckets with no checkable outputs, ignores dependencies between streams, or accepts subagent completion claims without any audit step.
