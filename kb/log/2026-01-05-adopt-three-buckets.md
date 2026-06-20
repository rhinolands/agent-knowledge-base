---
name: 2026-01-05-adopt-three-buckets
type: log
description: Decision to split the knowledge base into concept / reference / log buckets so an agent can load the right context cheaply.
---

# 2026-01-05 — adopt the three-bucket structure

**Decision.** Split the KB into three buckets: `concept` (durable how-it-works),
`reference` (pointers), `log` (time-ordered decisions).

**Why.** A flat folder forces an agent to read everything to find anything.
Typed buckets let the loader be selective: pull `concept` docs for grounding,
search `reference` for a link, scan recent `log` for "what changed lately."

**Result.** The indexer ([[../../index.py]]) emits a capability map grouped by
bucket, and chunks bodies for retrieval. Context cost per task dropped.
