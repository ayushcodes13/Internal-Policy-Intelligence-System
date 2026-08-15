# PolicyLens Architecture

## Production App

```text
app/
  api/query/route.ts        Next.js API route for policy queries
  layout.tsx                App metadata and shell
  page.tsx                  Thin client controller
components/                 UI components only
config/product.ts           Product name, copy, domains, sample prompts
lib/
  client/query-client.ts    Browser API client
  gemini.ts                 Gemini embedding client
  groq.ts                   Groq chat client
  pipeline.ts               Intent, routing, governance, generation, grounding
  retrieval.ts              Static embedding index loading and cosine search
  types.ts                  Shared TypeScript types
scripts/
  build-search-index.mjs    Build-time document chunking and Gemini embeddings
data/
  raw_docs/                 Source policy documents
  search-index.json         Generated retrieval index, not produced without GEMINI_API_KEY
```

## Request Flow

```text
Browser
  -> POST /api/query
  -> Groq intent detection
  -> owner routing
  -> Gemini query embedding
  -> cosine search over generated document embeddings
  -> deterministic owner/latest-version constraints
  -> Groq governance classifier
  -> Groq answer or refusal generation
  -> lexical grounding check
  -> JSON response
```

## Legacy Python Path

The original Streamlit and FAISS implementation remains for reference:

```text
app.py
src/
requirements.txt
run_app.sh
```

It is not the Vercel deployment path. Do not add new product work there unless you are intentionally maintaining the old Streamlit demo.
