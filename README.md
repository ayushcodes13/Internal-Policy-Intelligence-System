# CANON

CANON is a governance-gated policy intelligence system for teams that need internal policy answers with traceable evidence. It routes each question through intent detection, owner scoping, retrieval, governance classification, source-backed generation, and lexical grounding before returning an answer.

The current production app is a **Vercel-ready Next.js application**. The older Streamlit/FAISS Python implementation is preserved only as a reference path.

## What It Does

- Answers internal policy questions from approved source documents.
- Routes queries to the correct owner domains before retrieval.
- Suppresses outdated policy versions through deterministic metadata rules.
- Refuses unrelated, invalid, or policy-disallowed requests.
- Escalates security, legal, unauthorized-access, and fraud cases.
- Returns sources, supporting clauses, confidence, verdict, and grounding warnings.
- Runs on Vercel without loading local transformer models at request time.

## Production Architecture

```text
Browser
  -> Next.js UI
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

See `docs/ARCHITECTURE.md` for the folder-level architecture.

## Why The Architecture Changed

The original app was built with Streamlit, FAISS, and local SentenceTransformers. That worked for a demo, but it was a poor fit for Vercel:

- Streamlit expects a persistent Python app server.
- `sentence-transformers` loads a local embedding model.
- the cross-encoder reranker also loads a local model.
- `faiss-cpu` is a native dependency.
- serverless functions should not depend on local model warmup for every cold start.
- local JSONL logging is not durable in a serverless environment.

CANON now keeps the same governance idea but moves heavy embedding work out of the request runtime.

## Tech Stack

- **Frontend:** Next.js App Router, React, TypeScript
- **Hosting target:** Vercel
- **Generation/classification:** Groq chat completions
- **Embeddings:** Gemini Embedding API
- **Retrieval:** cosine similarity over a generated static JSON index
- **Source documents:** Markdown files under `data/raw_docs`

## Folder Structure

```text
app/
  api/query/route.ts        API route for policy queries
  layout.tsx                App metadata and document shell
  page.tsx                  Page controller and section composition
  globals.css               Product-site styling

components/
  hero-section.tsx          Landing hero and product preview
  product-sections.tsx      Product, workflow, architecture, docs bands
  query-composer.tsx        Query input
  result-panel.tsx          Answer, warnings, evidence
  site-header.tsx           Sticky navigation
  status-metrics.tsx        Verdict/status metrics

config/
  product.ts                Product name, copy, domains, sample prompts

lib/
  client/query-client.ts    Browser API client
  gemini.ts                 Gemini embedding client
  groq.ts                   Groq JSON client
  pipeline.ts               Intent, routing, governance, generation, grounding
  retrieval.ts              Static index loading and vector scoring
  types.ts                  Shared types

scripts/
  build-search-index.mjs    Builds data/search-index.json with Gemini

data/
  raw_docs/                 Policy, FAQ, SOP, and notes source documents
  search-index.json         Generated embedding index

docs/
  ARCHITECTURE.md           Production architecture notes
```

## Environment Variables

Required:

```bash
GROQ_API_KEY=...
GEMINI_API_KEY=...
```

Optional:

```bash
GROQ_MODEL=llama-3.3-70b-versatile
GEMINI_EMBEDDING_MODEL=gemini-embedding-001
```

Use `.env.example` as the local template.

## Local Development

Install dependencies:

```bash
npm install
```

Create a local environment file:

```bash
cp .env.example .env.local
```

Add `GROQ_API_KEY` and `GEMINI_API_KEY`, then build the retrieval index:

```bash
npm run build:index
```

Start the app:

```bash
npm run dev
```

Open the local Next.js URL printed by the dev server.

## Building The Search Index

`npm run build:index` performs the production ingestion step:

1. Reads markdown files from `data/raw_docs`.
2. Extracts metadata headers such as owner, source type, and update date.
3. Splits documents into overlapping chunks.
4. Applies latest-version metadata.
5. Calls Gemini with `RETRIEVAL_DOCUMENT`.
6. Normalizes vectors.
7. Writes `data/search-index.json`.

The generated index is intentionally simple because the current document universe is small. This avoids FAISS and local transformer dependencies in Vercel runtime.

## Running The Query Pipeline

The frontend calls:

```http
POST /api/query
Content-Type: application/json

{
  "query": "How do I request a refund?"
}
```

The response includes:

```json
{
  "status": "SAFE",
  "verdict": "SAFE",
  "answer": "...",
  "sources": ["data/raw_docs/policies/billing_and_refund_policy_v2.md"],
  "supporting_clauses": ["..."],
  "confidence": "high",
  "context_used": 5,
  "hallucination_detected": false
}
```

Possible verdicts:

- `SAFE`
- `REFUSE_POLICY`
- `REFUSE_INVALID`
- `ESCALATE`

## Deploying To Vercel

Before deploying, make sure `data/search-index.json` exists:

```bash
npm run build:index
```

Then set these Vercel environment variables:

```bash
GROQ_API_KEY
GEMINI_API_KEY
GROQ_MODEL
GEMINI_EMBEDDING_MODEL
```

Deploy:

```bash
vercel deploy
```

Use `vercel deploy --prod` only when you intentionally want a production deployment.

## Free Domain Plan

The recommended free deployment hostname is a Cloudflare Workers subdomain:

```text
canon-policy.<your-cloudflare-subdomain>.workers.dev
```

The repository includes `wrangler.jsonc` and Cloudflare scripts:

```bash
npm run cf:build
npm run cf:preview
npm run cf:deploy
```

After a stable deployment exists, a cleaner free alias such as `canon.is-a.dev` can point to the live app. See `docs/DOMAINS.md`.

## Troubleshooting

### `data/search-index.json is missing`

Run:

```bash
npm run build:index
```

This requires `GEMINI_API_KEY`.

### `GROQ_API_KEY is not configured`

Set the key locally in `.env.local` or in the Vercel project environment variables.

### `GEMINI_API_KEY is not configured`

Set the key before running `npm run build:index` and before deploying the API route.

### Query returns no sources

Check:

- the detected intent maps to an owner in `lib/pipeline.ts`
- matching documents have the expected `owner` metadata
- older versions are not being filtered by `is_latest`
- the generated index was rebuilt after document changes

## Legacy Python Reference

The previous implementation remains in the repository:

```text
app.py
src/
requirements.txt
run_app.sh
data/index/
```

That path is useful for historical comparison and offline experiments. New production work should target the Next.js app under `app/`, `components/`, `config/`, `lib/`, and `scripts/`.

## Current Status

- Next.js frontend implemented.
- TypeScript API route implemented.
- Gemini embedding client implemented.
- Groq JSON client implemented.
- Static retrieval index builder implemented.
- Production build verified.
- Deployment still requires real `GEMINI_API_KEY` and `GROQ_API_KEY`.
