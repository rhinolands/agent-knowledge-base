---
name: durable-workflows
type: concept
description: Why long-running agent work should run as a durable, retryable workflow instead of an in-process loop.
---

# Durable workflows

An agent action that spans minutes, calls flaky tools, or must survive a process
restart should not live in a single in-memory loop. Model it as a **durable
workflow**: each step is checkpointed, retries are automatic, and a crash
resumes from the last completed step rather than the beginning.

## Why

- **Crash-safety** — the orchestrator restarts; the workflow continues.
- **Idempotent retries** — a failed tool call retries without redoing prior steps.
- **Observability** — every step has a recorded start, end, and outcome.

## Shape

```
workflow(goal):
    plan   = step("plan", llm.plan, goal)        # checkpointed
    for task in plan.tasks:
        result = step(f"do:{task.id}", run, task)  # retried independently
    return step("summarize", llm.summarize, results)
```

Related: [[policy-as-code]] (the same audit trail feeds drift detection).
