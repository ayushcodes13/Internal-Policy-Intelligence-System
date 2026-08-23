# Agent Instructions

This repository is **CANON**, a governance-gated policy intelligence system. Treat approved policy documents as the canonical source of truth and preserve the separation between UI, retrieval, governance, and generation.

## Current Production Path

The production app is the Vite/TanStack frontend plus Python API path:

```text
frontend/             React 19, TanStack Router, TanStack Query, Vite
frontend/src/lib/     Browser-only types, product config, API client
frontend/src/components/ui/
                      shadcn-style local UI components
api/                  Python API, policy pipeline, Gemini index builder
data/                 Markdown policy corpus and generated JSON search index
docs/                 Architecture and deployment documentation
evaluation/           Offline pipeline checks
```

Do not reintroduce deleted prototype app surfaces or inactive AI backends unless the task explicitly asks for an architecture migration.

## Product Principles

- CANON answers only from approved policy evidence.
- Owner scoping must happen before retrieval results are used.
- Latest-version policy documents should dominate older versions.
- Governance decisions must remain explicit: `SAFE`, `REFUSE_POLICY`, `REFUSE_INVALID`, or `ESCALATE`.
- Generated answers should include sources, supporting clauses, confidence, and grounding status.
- Do not silently remove refusals, escalations, source validation, or grounding checks to make demos look smoother.

## Runtime Architecture

The live query flow is:

```text
Browser
  -> Vite React UI
  -> TanStack Query mutation
  -> Python POST /api/query
  -> Python Groq intent detection
  -> deterministic owner routing
  -> Python Gemini query embedding
  -> cosine retrieval over data/search-index.json
  -> owner/latest-version constraints
  -> Python Groq governance classification
  -> Python Groq answer or refusal generation
  -> lexical grounding check
  -> JSON response
```

Key files:

- `frontend/src/screens/home.tsx` owns the main UI.
- `frontend/src/sections/query-console.tsx` owns the live query console.
- `frontend/src/lib/api.ts` calls the Python API.
- `api/index.py` exposes the FastAPI app to Vercel Python Functions.
- `api/main.py` validates request input and returns pipeline output.
- `api/pipeline.py` owns intent detection, routing, constraints, governance, generation, and grounding orchestration.
- `api/build_search_index.py` generates the static embedding index.

## Environment Variables

Required:

```bash
GROQ_API_KEY
GEMINI_API_KEY
```

Optional:

```bash
GROQ_MODEL=llama-3.3-70b-versatile
GEMINI_EMBEDDING_MODEL=gemini-embedding-001
```

Never commit real API keys. Keep `.env`, `.env.local`, and secret files untracked.

## Development Commands

Use the repo's Node package manager setup. In this Codex environment, system `npm` may be unavailable; use the bundled Node/Pnpm path if needed.

```bash
pnpm install
pip install -r requirements.txt
pnpm run build:index
pnpm run dev:api
pnpm run dev
pnpm run build
pnpm run build:vercel
```

`npm run build:index`, `pnpm run build:index`, and `pnpm run build:vercel` require `GEMINI_API_KEY`.

## Deployment

Deploy as one Vercel project. The frontend is emitted to `dist/`, and `/api/*` rewrites to `api/index.py`, which imports `api.main:app`. Keep `VITE_API_BASE_URL` unset for this same-origin deployment.

## Frontend Guidelines

- Keep the first screen product-like and polished, but preserve access to the live query console.
- Prefer dense, credible operational UI over decorative marketing sections.
- Keep cards at `16px` radius or below unless there is a strong visual reason.
- Keep text readable on mobile; avoid fixed-width content that can overflow.
- Use `frontend/src/lib/product.ts` for product name, tagline, domains, and sample prompts.
- Do not hardcode `CANON` or the brand mark in components if it can come from config.

## Code Guidelines

- Keep browser API contracts typed with `frontend/src/lib/types.ts`.
- Keep browser-only code out of server-only modules.
- Keep secret usage in Python only.
- Keep generated retrieval indexes separate from raw policy documents.
- Prefer simple deterministic code over clever abstractions for policy gates.
- If changing document metadata semantics, update `api/build_search_index.py`, `api/pipeline.py`, and the docs together.
- If changing output shape, update Python responses, `PipelineResult`, `ResultPanel`, README examples, and any tests together.

## Git Hygiene

- Make small, meaningful commits when possible.
- Keep unrelated macOS metadata such as `.DS_Store` out of commits.
- Do not rewrite public history unless the user explicitly asks for it.
- If the user requests dated commits, set both author and committer dates consistently.

## Verification Checklist

Before handing off code changes:

```bash
pnpm run build
```

When retrieval docs change:

```bash
pnpm run build:index
```

The index build requires a valid `GEMINI_API_KEY`.
