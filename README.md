# fact-frontier

Prototype of a goal-driven learning tool: read papers (later: any goal), build a growing pool
of the atomic facts you need to understand them, and learn and review those facts with
varied questions. See [DESIGN.md](DESIGN.md).

Currently: the ingestion pipeline only.

```bash
uv sync
export OPENROUTER_API_KEY=...
# edit profile.md to describe yourself
uv run frontier ingest 2209.05364 2308.03296 2602.07852 2606.28548
# open reports/index.html (and the per-source snapshots beside it)
```

Needs `pdftotext` (poppler-utils).
