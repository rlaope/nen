---
type: llm
focus: last_message
weight: 1
---

The response applies behavior-preserving refactoring discipline to src/orders_service.py, which exists in the working directory (a ~45-line function mixing payload parsing, nested plan/region/coupon pricing, and DB writes, guarded only by tests/test_orders.py — a mock-interaction test that asserts nothing about behavior). Award a pass only if all of the following hold:

1. A safety net comes BEFORE restructuring, grounded in the actual file: characterization tests that pin handle_order's observable outputs (totals/currency across plan, region, seats, coupon branches) — the existing mock test must not be treated as adequate protection.
2. The refactor is explicitly separated from the feature: restructuring the tangle and adding the "enterprise" plan type are distinct steps, not one combined rewrite.
3. Behavior is preserved during the restructuring step — the plan reshapes (extract pricing, isolate persistence, or equivalent) without changing what handle_order observably returns, and does not propose "rewrite it from scratch" as the method.

Evidence the file was actually read (referencing its real branches, the coupon quirks, the mock test's weakness) strengthens a pass. Fail if the response starts adding the plan type directly into the tangle, proposes a rewrite without pinning behavior first, treats the mock test as a sufficient net, ignores the seeded code and answers generically, or mixes behavior changes into the cleanup with no way to tell which change broke what.
