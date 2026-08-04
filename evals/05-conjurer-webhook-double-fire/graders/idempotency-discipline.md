---
type: llm
focus: last_message
weight: 1
---

The response applies failure-mode-driven reliability discipline to webhooks/payments.py, which exists in the working directory (a handler that charges the card, marks the order paid, and retries a flaky fulfillment call — with no idempotency anywhere), alongside docs/provider.md stating delivery is AT LEAST ONCE with redelivery on slow responses. Award a pass only if all of the following hold:

1. Duplicate delivery is recognized as expected provider behavior (at-least-once delivery, redelivery on timeout — the seeded docs say so), not purely a vendor bug to report. Bonus signal: noticing the handler charges BEFORE recording anything, so a redelivery re-charges.
2. The core fix is idempotency, named against the actual code: dedup on the event id (dedup store or unique constraint claimed before the charge, or an idempotency key on the charge call) so the same event charges at most once.
3. The fix is proven: a reproducing test that delivers the same event twice and asserts a single charge, or an equivalently concrete red-then-green verification step.

Evidence the seeded files were actually read (the charge-then-save ordering, the bare retry loop, the 10-second acknowledgment window) strengthens a pass. Fail if the response only proposes refunding the customers, only blames or escalates to the provider, answers generically without engaging the seeded handler, or never mentions idempotency/deduplication in any form.
