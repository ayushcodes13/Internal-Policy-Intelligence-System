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
frontend/
api/
data/
docs/
evaluation/
```

Do not reintroduce retired app surfaces or deleted prototype backends as the current production path.

## Key Constraints

- Do not commit API keys.
- Keep `GROQ_API_KEY` and `GEMINI_API_KEY` as environment variables.
- Do not reintroduce TypeScript AI backend logic. The AI pipeline belongs in Python.
- Do not add local model runtimes or native vector-store dependencies unless the architecture docs are updated with the deployment tradeoff.
- Preserve the core verdict flow: `SAFE`, `REFUSE_POLICY`, `REFUSE_INVALID`, `ESCALATE`.
- Preserve source citations, supporting clauses, confidence, and grounding warnings.
- Keep `frontend/src/lib/product.ts` as the source of truth for product naming and visible product copy.

## Useful Commands

```bash
pnpm install
pip install -r requirements.txt
pnpm run build:index
pnpm run dev:api
pnpm run dev
pnpm run build
pnpm run build:vercel
```

`pnpm run build:index` and `pnpm run build:vercel` require `GEMINI_API_KEY`.

## Handoff Rule

Before reporting completion, run the relevant build or explain exactly why it could not be run. For frontend or API changes, the minimum verification is:

```bash
pnpm run build
```
