# Getting oriented

Read [DESIGN.md](DESIGN.md) before changing behavior; update it when structure changes. Keep it
brief and code-free — reasoning about *why* something is built a certain way belongs in a
comment beside that code.

- Python 3.14 via `uv`; `uv run pytest`, `uv run ruff check`, `uv run pyright`.
- All model calls go through `frontier/llm.py` (OpenRouter), which records each call's cost in
  `llm_calls`. Don't call a provider directly.
- `data/` (the pool database, downloaded PDFs) and `reports/` are gitignored.
