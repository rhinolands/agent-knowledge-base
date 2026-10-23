# agent-knowledge-base

A small, **agent-readable knowledge base** with a build step that turns Markdown into a RAG-ingestable index — context engineering as code.

Most "docs folders" force an agent to read everything to find anything. This one is split into **three typed buckets** so a loader can pull exactly the context a task needs, and an `index.py` step makes the whole thing retrievable.

## The three buckets

| Bucket | Holds | An agent uses it to… |
|---|---|---|
| `concept` | durable "how it works" explanations | **ground** itself before acting |
| `reference` | pointers to authoritative sources | **fetch** a link without inlining stale copy |
| `log` | time-ordered decisions / activity | see **what changed lately** and why |

Each doc carries three frontmatter fields:

```markdown
---
name: durable-workflows
type: concept
description: One line — used as the retrieval summary.
---
```

## The build step — `index.py`

```bash
python index.py                 # → index.json + capability-map.md
python index.py --chunk-size 800 --overlap 100
```

It does four things, **stdlib-only**:

1. **Parse** frontmatter from every `kb/**/*.md`.
2. **Lint** — every doc must declare `name` / `type` / `description` and a known type. No two docs may share a `name`. A violation **exits non-zero**, so it gates CI.
3. **Chunk** each body into overlapping windows tagged with the doc's metadata — drop straight into a vector store.
4. **Emit** `index.json` (chunks + metadata) and `capability-map.md` (overview grouped by bucket — the agent's table of contents).

## Why this shape

- **Selective loading** beats "stuff the whole repo in the prompt" — cheaper context, sharper answers.
- **Typed + linted** means the KB can't silently rot; a malformed doc fails the build.
- **One command** regenerates the index, so it lives in CI next to the content.

Bring your own embedder/vector store — `index.json` is the hand-off point.

## CI and tests

`.github/workflows/ci.yml` runs on every push and pull request.
It runs the KB lint (`python index.py`), the tests, ruff, and a gitleaks scan over every commit.

```bash
pip install pytest ruff
pytest
ruff check . && ruff format --check .
```

---

By **Gustavo Norymberg** — AI & Agentic Platform Architect. [LinkedIn](https://www.linkedin.com/in/gustavonorymberg)
