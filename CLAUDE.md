# Claude Project Guide

This project is **CANON**: a policy-governed intelligence system that answers internal policy questions only after routing, retrieval, governance, and grounding checks.

Use `AGENTS.md` as the canonical source for repository instructions. This file exists so Claude-based coding sessions can quickly find the same operating rules.

## Start Here

Read these files before making changes:

1. `AGENTS.md`
2. `README.md`
3. `docs/ARCHITECTURE.md`
4. The specific source files you plan to modify

## Production Path

Work primarily in:

```text
app/
components/
config/
lib/
scripts/
docs/
```

The old Python/Streamlit implementation is retained for reference:

```text
app.py
src/
requirements.txt
run_app.sh
```

Do not treat the Streamlit app as the current production frontend.

## Key Constraints

- Do not commit API keys.
- Keep `GROQ_API_KEY` and `GEMINI_API_KEY` as environment variables.
- Do not reintroduce runtime `sentence-transformers`, cross-encoder reranking, or `faiss-cpu` into the production Next.js app.
- Preserve the core verdict flow: `SAFE`, `REFUSE_POLICY`, `REFUSE_INVALID`, `ESCALATE`.
- Preserve source citations, supporting clauses, confidence, and grounding warnings.
- Keep `config/product.ts` as the source of truth for product naming and visible product copy.

## Useful Commands

```bash
pnpm install
pnpm run build:index
pnpm run dev
pnpm exec next build
pnpm run cf:build
```

`pnpm run build:index` requires `GEMINI_API_KEY`.

## Handoff Rule

Before reporting completion, run the relevant build or explain exactly why it could not be run. For frontend or API changes, the minimum verification is:

```bash
pnpm exec next build
```
