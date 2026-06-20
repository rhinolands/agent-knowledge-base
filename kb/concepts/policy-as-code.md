---
name: policy-as-code
type: concept
description: Express desired-state rules as code, detect drift against live state, and propose remediation — never auto-apply blindly.
---

# Policy as code

Encode the rules a system must satisfy (network exposure, identity scopes,
tagging, encryption) as **executable policy**, not a wiki page. A check
compares declared desired-state against live state and emits **drift**.

## Drift → remediation (not auto-fix)

1. **Detect** — evaluate policy against live state; emit a list of violations.
2. **Explain** — each drift item names the rule, the resource, and the gap.
3. **Propose** — generate the remediation as a reviewable change.
4. **Gate** — a human (or a higher-trust workflow) approves before apply.

Auto-applying remediation is how a small policy bug becomes an outage. The
proposal-and-gate split keeps the loop fast *and* safe — the same two-step
shape as a human-confirm tool gate.

Related: [[durable-workflows]].
