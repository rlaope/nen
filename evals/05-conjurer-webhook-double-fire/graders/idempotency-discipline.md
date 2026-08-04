---
type: llm
focus: last_message
weight: 1
---

The response applies failure-mode-driven reliability discipline to duplicate webhook delivery. The working directory contains no code, so two shapes can pass:

A. Delivered fix: all of the following hold —
   1. duplicate delivery is recognized as expected webhook behavior (at-least-once delivery, provider retries), not purely a vendor bug to report;
   2. the core fix is idempotency: dedup on an event id or an idempotency key so the same event charges at most once, with the mechanism named (dedup store, unique constraint, idempotency key on the charge call);
   3. the fix is proven: a reproducing test that delivers the same event twice and asserts a single charge, or an equivalently concrete verification step.

B. Asks for the missing handler/provider details, with conjurer discipline visible in the request: the response treats double-fire as a failure mode to enumerate rather than a mystery — e.g. it names provider retry/delivery semantics as a likely cause, raises missing idempotency/dedup as a suspect or as part of the plan, and states intent to diagnose and harden the handler (enumerate failure modes, reproduce, or test). Idempotency or deduplication must appear somewhere in the response for shape B to pass; the reproducing test may be implicit in the stated hardening plan.

Fail if the response only proposes refunding the customers, only blames or escalates to the payment provider, asks for the code with no reliability reasoning attached, or never mentions idempotency/deduplication in any form.
