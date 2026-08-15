# Agent Instructions

This repository is **CANON**, a governance-gated policy intelligence system. Treat approved policy documents as the canonical source of truth and preserve the separation between UI, retrieval, governance, and generation.

## Current Production Path

The production app is the Next.js/Vercel/Cloudflare path:

```text
app/                  Next.js App Router pages and API routes
components/           React UI components
config/product.ts     Brand, copy, domains, and sample prompts
lib/                  TypeScript runtime pipeline
scripts/              Build-time indexing tools
docs/                 Architecture and deployment documentation
```

The legacy Python/Streamlit path remains for reference only:

```text
app.py
src/
requirements.txt
run_app.sh
data/index/
```

Do not add new production behavior to the legacy Python path unless the task explicitly asks for Streamlit or offline Python work.

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
  -> POST /api/query
  -> Groq intent detection
  -> deterministic owner routing
  -> Gemini query embedding
  -> cosine retrieval over data/search-index.json
  -> owner/latest-version constraints
  -> Groq governance classification
  -> Groq answer or refusal generation
  -> lexical grounding check
  -> JSON response
```

Key files:

- `app/api/query/route.ts` validates request input and returns pipeline output.
- `lib/pipeline.ts` owns intent detection, routing, constraints, governance, generation, and grounding orchestration.
- `lib/retrieval.ts` loads `data/search-index.json` and scores chunks.
- `lib/gemini.ts` calls Gemini embeddings and normalizes vectors.
- `lib/groq.ts` calls Groq with JSON response mode.
- `scripts/build-search-index.mjs` generates the static embedding index.

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
pnpm run build:index
pnpm run dev
pnpm exec next build
pnpm run cf:build
```

`npm run build:index` or `pnpm run build:index` requires `GEMINI_API_KEY`.

## Deployment

Vercel is supported through the standard Next.js build.

Cloudflare Workers is supported through OpenNext:

```bash
pnpm run cf:build
pnpm run cf:preview
pnpm run cf:deploy
```

The intended free Cloudflare hostname is:

```text
canon-policy.<your-cloudflare-subdomain>.workers.dev
```

See `docs/DOMAINS.md` before changing domain strategy.

## Frontend Guidelines

- Keep the first screen product-like and polished, but preserve access to the live query console.
- Prefer dense, credible operational UI over decorative marketing sections.
- Keep cards at `16px` radius or below unless there is a strong visual reason.
- Keep text readable on mobile; avoid fixed-width content that can overflow.
- Use `config/product.ts` for product name, tagline, domains, and sample prompts.
- Do not hardcode `CANON` or the brand mark in components if it can come from config.

## Code Guidelines

- Keep API contracts typed with `lib/types.ts`.
- Keep browser-only code out of server-only modules.
- Keep secret usage server-side only.
- Keep generated retrieval indexes separate from raw policy documents.
- Prefer simple deterministic code over clever abstractions for policy gates.
- If changing document metadata semantics, update `scripts/build-search-index.mjs`, `lib/retrieval.ts`, and the docs together.
- If changing output shape, update `PipelineResult`, `ResultPanel`, README examples, and any tests or scripts together.

## Git Hygiene

- Make small, meaningful commits when possible.
- Keep unrelated macOS metadata such as `.DS_Store` out of commits.
- Do not rewrite public history unless the user explicitly asks for it.
- If the user requests dated commits, set both author and committer dates consistently.

## Verification Checklist

Before handing off code changes:

```bash
pnpm exec next build
```

When Cloudflare deploy config changes:

```bash
pnpm run cf:build
```

When retrieval docs change:

```bash
pnpm run build:index
```

The index build requires a valid `GEMINI_API_KEY`.
