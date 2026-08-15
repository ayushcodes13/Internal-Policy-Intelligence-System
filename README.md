# PolicyLens

A governance-gated policy retrieval system deployed as a Vercel-ready Next.js app.

The production path no longer depends on Streamlit, FAISS, or local transformer model loading at request time. Query embeddings are generated with Gemini, while policy classification and answer generation use Groq.

## Current Architecture

```text
Next.js UI
  -> /api/query
  -> Groq intent detection
  -> Gemini query embedding
  -> cosine retrieval over data/search-index.json
  -> deterministic owner/version filters
  -> Groq governance classification
  -> answer, refusal, or escalation response
  -> lexical grounding check
```

See `docs/ARCHITECTURE.md` for the production folder structure.

## Why This Changed

The previous Streamlit app worked, but it was not a good fit for Vercel:

- Streamlit requires a persistent Python app server.
- `sentence-transformers` and the cross-encoder reranker load local ML models.
- `faiss-cpu` is a native Python dependency.
- Streamlit session state and local file logging do not map cleanly to serverless functions.

The new Vercel path keeps the product behavior but removes the heavy runtime pieces.

## Required Environment Variables

```bash
GROQ_API_KEY=...
GEMINI_API_KEY=...
```

Optional:

```bash
GROQ_MODEL=llama-3.3-70b-versatile
GEMINI_EMBEDDING_MODEL=gemini-embedding-001
```

## Local Setup

```bash
npm install
npm run build:index
npm run dev
```

`npm run build:index` reads `data/raw_docs`, chunks the documents, calls Gemini embeddings once per chunk, and writes `data/search-index.json`.

## Deploying

Set `GROQ_API_KEY` and `GEMINI_API_KEY` in Vercel, then deploy:

```bash
vercel deploy
```

The generated `data/search-index.json` should be present before deployment. It contains embeddings derived from the public policy documents and allows the Vercel API route to avoid local ML packages.

## Legacy Python Reference

The original Streamlit/FAISS implementation remains in:

- `app.py`
- `src/`
- `requirements.txt`
- `run_app.sh`

Use that only for comparison or offline experiments. The Vercel production app is the Next.js application under `app/`, `lib/`, and `scripts/`.
