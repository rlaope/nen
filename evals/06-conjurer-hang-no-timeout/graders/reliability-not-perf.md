---
type: llm
focus: last_message
weight: 1
---

This is a reliability problem (an unbounded wait), not a performance problem — the trap is treating "hangs" as "slow" and reaching for profiling. The working directory contains no code, so the response may either give the remedy directly or ask for the call site first; both shapes can pass.

Award a pass if EITHER of the following holds:

A. Direct answer: the primary fix is bounding the wait — an explicit timeout (connect/read/overall deadline) on the checkout call — and the response addresses at least one consequence of the timeout firing: retry policy with backoff, whether a checkout/charge is safe to retry (double-charge risk), surfacing the failure to the caller, or circuit-breaking/fallback.

B. Asks for the missing code, but with the right plan attached: it requests the call site / client config / code, AND the stated plan is reliability work — bounding the wait (timeout config), enumerating failure modes, or reproducing the hang with a test. A bare "show me the code" with no stated plan does not pass.

In both shapes, FAIL if the response frames the work as making the call faster — profiling, benchmarking, or latency optimization as the main move — or proposes unbounded/blind retries. Treating the hang as a reliability defect is the whole point; treating it as a slowness to optimize is the trap.
