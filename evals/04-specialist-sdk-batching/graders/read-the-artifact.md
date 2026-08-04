---
type: llm
focus: last_message
weight: 1
---

The docs have run out, so the discipline is to read the artifact itself instead of guessing. The working directory contains no code, so asking which SDK/package it is (or where the project lives) is acceptable — provided the stated plan is artifact inspection. Award a pass only if both of the following hold:

1. The response's primary move is inspecting the actual artifact: reading the SDK's source (it is on disk in the project's dependencies), un-minifying the bundle, capturing the network traffic it emits, or tracing its calls — with at least one concrete inspection step named (e.g. locate the batching code in the installed package, grep for the constant 25, capture requests and observe grouping). If it asks for the SDK's name/location first, the request must come with this inspection plan attached.
2. Any hypothesis about the cause (e.g. an upstream API's batch limit) is presented as a hypothesis to verify against the artifact, not as the confident final answer. A plausible-sounding explanation delivered with no verification plan is exactly the folklore this discipline exists to prevent.

Fail if the response only speculates about why vendors batch things, only suggests emailing the vendor or re-reading the docs, or states a specific cause as fact without any step that would confirm it from the SDK's own code or traffic.
