# CANON Architecture

## Production App

```text
frontend/
  index.html                Vite HTML shell
  src/main.tsx              React 19 entry point
  src/router.tsx            TanStack Router setup in a TanStack Start-ready Vite app
  src/screens/home.tsx      Main product and dashboard screen
  src/sections/             Feature sections and query console
  src/components/ui/        shadcn-style local UI components
  src/lib/                  Browser-only API client, product copy, types
api/
  main.py                   FastAPI app and /api/query route
  pipeline.py               Python AI orchestration
  build_search_index.py     Gemini-powered index builder
data/
  raw_docs/                 Source policy documents
  search-index.json         Generated retrieval index, not produced without GEMINI_API_KEY
```

## Request Flow

```text
Browser
  -> Vite React UI
  -> TanStack Query mutation
  -> Python POST /api/query
  -> Python Groq intent detection
  -> owner routing
  -> Python Gemini query embedding
  -> cosine search over generated document embeddings
  -> deterministic owner/latest-version constraints
  -> Python Groq governance classifier
  -> Python Groq answer or refusal generation
  -> lexical grounding check
  -> JSON response
```

## Repository Boundaries

```text
frontend/             Browser UI and client-side state
api/                  Python policy intelligence runtime
data/raw_docs/        Authoritative markdown policy corpus
data/search-index.json
docs/                 Human-readable architecture and domain notes
evaluation/           Offline checks against the current Python pipeline
```

Inactive demo surfaces and binary retrieval artifacts are intentionally not part of the repository. New production behavior should be added to `frontend/`, `api/`, `data/`, `docs/`, or `evaluation/` depending on the ownership boundary.
