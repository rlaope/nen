---
type: llm
focus: last_message
weight: 1
---

The response applies behavior-preserving refactoring discipline. The working directory contains no code, so the response may either lay out the refactoring plan or ask to see the file first; a request for the file passes only when the stated plan that comes with it is discipline-conformant. Award a pass only if all of the following hold (whether stated as a plan or as the intent behind a request for the file):

1. A safety net comes BEFORE restructuring: characterization tests, pinning current observable behavior, or an equivalent regression guard is named as the prerequisite step.
2. The refactor is explicitly separated from the feature: restructuring the tangled code and adding the new plan type are distinct steps, not one combined rewrite.
3. Behavior is preserved during the restructuring step — the plan does not change what the service observably does while reshaping it, and it does not propose "rewrite it from scratch" as the method.

Fail if the response starts adding the plan type directly into the tangle, proposes a rewrite without tests, asks for the file with no stated plan at all, or mixes behavior changes into the cleanup with no way to tell which change broke what.
