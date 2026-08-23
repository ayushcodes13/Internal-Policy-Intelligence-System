<div align="center">

<img src="public/canon-logo.svg" alt="CANON logo" width="120" />

# CANON

**Policy-governed intelligence for decisions that need proof.**

***Take organizational rules, retrieve the authoritative version, enforce constraints, and only then let AI answer.***

[![React](https://img.shields.io/badge/React-19-149ECA?style=for-the-badge&logo=react&logoColor=white)](https://react.dev/)
[![Live Demo](https://img.shields.io/badge/LIVE-canon.devayushrout.me-16A34A?style=for-the-badge&logo=vercel&logoColor=white)](https://canon.devayushrout.me)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![TanStack](https://img.shields.io/badge/TanStack-Router%20%2B%20Query-FF4154?style=for-the-badge)](https://tanstack.com/)
[![Vite](https://img.shields.io/badge/Vite-7-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vite.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Python](https://img.shields.io/badge/Python-AI_Backend-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Gemini](https://img.shields.io/badge/Gemini-Embeddings-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)](https://ai.google.dev/)
[![Groq](https://img.shields.io/badge/Groq-Inference-F55036?style=for-the-badge)](https://groq.com/)

[Live Demo](https://canon.devayushrout.me) | [Overview](#overview) | [Demo](#demo) | [Architecture](#architecture) | [Run Locally](#run-locally) | [Deployment](#deployment)

**Deployed CANON:** [`canon.devayushrout.me`](https://canon.devayushrout.me)

</div>

---

<img src="docs/assets/canon-home.png" alt="CANON homepage showing the policy-governed intelligence interface" width="100%" />

## Overview

CANON is a governance-gated policy intelligence system for teams that need internal policy answers with traceable evidence. It does not treat the model as the source of truth. Instead, it treats approved policy documents as the canonical authority and uses the model only after routing, retrieval, and governance checks have already narrowed the answer space.

The system is designed for organizational policy workflows where a generic chatbot would be risky: refund rules, access controls, support exceptions, security escalation, compliance-sensitive procedures, and versioned operating policies.

The current production path is a **Vite + React 19 + TanStack frontend** calling a **Python API** for policy intelligence. Groq handles classification/generation and Gemini handles embeddings from the Python layer. The repository has been cleaned so only the active frontend, Python API, policy corpus, docs, and evaluation tooling remain.

CANON can currently answer from the included markdown policy corpus, return sources and supporting clauses, refuse invalid or policy-disallowed requests, and escalate sensitive cases. It is still a project/demo system, not a substitute for legal, compliance, or human policy approval.

## Demo

Live production demo: [`canon.devayushrout.me`](https://canon.devayushrout.me)

<img src="docs/assets/canon-console.png" alt="CANON live policy console with sample questions and query input" width="100%" />

```text
Question
  -> intent detection
  -> owner routing
  -> Gemini embedding
  -> policy retrieval
  -> governance verdict
  -> source-backed answer or refusal
```

Example query:

```text
Can support override the refund deadline?
```

Example response shape:

```json
{
  "status": "SAFE",
  "verdict": "SAFE",
  "answer": "The answer is generated only from retrieved policy clauses.",
  "sources": ["data/raw_docs/policies/billing_and_refund_policy_v2.md"],
  "supporting_clauses": ["Relevant policy text used by the answer."],
  "confidence": "high",
  "context_used": 5,
  "hallucination_detected": false
}
```

## At A Glance

| Area | Current State |
| --- | --- |
| Frontend | React 19, TypeScript, TanStack Start-ready Vite app, TanStack Router, TanStack Query |
| UI | Tailwind CSS v4, Radix UI primitives, shadcn-style components, Lucide icons |
| API | Python FastAPI endpoint at `POST /api/query` |
| AI Layer | Python calls Groq chat completions and Gemini embeddings |
| Retrieval | Python retrieval over static JSON embeddings, with lexical local fallback |
| Data | Markdown policy documents under `data/raw_docs` |
| Deployment | Vercel production at [`canon.devayushrout.me`](https://canon.devayushrout.me) |
| Status | Portfolio-grade MVP with deterministic governance gates |

## Key Features

- **Policy-first answers:** every answer is grounded in approved internal documents.
- **Owner-scoped retrieval:** queries are routed to Finance, Operations, Security, or Support before evidence is used.
- **Version-aware evidence:** latest policy versions win over stale source documents.
- **Explicit governance verdicts:** responses are classified as `SAFE`, `REFUSE_POLICY`, `REFUSE_INVALID`, or `ESCALATE`.
- **Source-backed output:** answers include source paths, supporting clauses, confidence, and grounding status.
- **No Node AI backend:** Node is used only for frontend tooling; the intelligence runtime is Python.

## Product Surface

<img src="docs/assets/canon-product.jpg" alt="CANON product section showing the decision trace and response contract" width="100%" />

## Workflow

<img src="docs/assets/canon-workflow.png" alt="CANON workflow section showing the evidence-gated policy pipeline" width="100%" />

## Architecture

<img src="docs/assets/canon-architecture.jpg" alt="CANON architecture section showing the internal governed answer path" width="100%" />

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

The architecture is shaped around one rule: the model should not get to answer until the system has decided which policy owner applies, which documents are authoritative, whether the request is allowed, and whether the final answer stays close to the retrieved evidence.

Read the full architecture notes in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Tech Stack

| Layer | Tools |
| --- | --- |
| UI | React 19, TypeScript, Tailwind CSS v4 |
| Routing | TanStack Router |
| Data Fetching | TanStack React Query |
| Components | Radix UI primitives, shadcn-style local components |
| Charts/Icons | Recharts, Lucide React |
| Build | Vite with TanStack Start package alignment |
| API | Python FastAPI |
| Classification | Python calling Groq chat completions |
| Generation | Python calling Groq chat completions |
| Embeddings | Python calling Gemini Embedding API |
| Retrieval | Python static JSON index, cosine similarity, lexical fallback |
| Source Data | Markdown policy documents |
| Deploy | Vercel static frontend plus Python serverless function |

## Why This Exists

CANON exists because policy Q&A should not behave like an unconstrained chatbot. The system separates the decision path into explicit stages: detect what the user is asking, scope the policy owners, retrieve authoritative documents, apply governance rules, generate only from retrieved evidence, and return an answer with sources.

The current implementation keeps the browser app light and pushes the intelligence runtime into Python. Embeddings are generated through Gemini, model reasoning runs through Groq, and retrieval uses a static JSON index plus deterministic fallbacks so the project remains understandable and deployable.

## Run Locally

Clone the repository:

```bash
git clone https://github.com/ayushcodes13/canon.git
cd canon
```

Install dependencies:

```bash
pnpm install
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a local environment file:

```bash
cp .env.example .env.local
```

Build the retrieval index:

```bash
pnpm run build:index
```

Start the Python API:

```bash
pnpm run dev:api
```

Start the frontend in another terminal:

```bash
pnpm run dev
```

Then open the local Vite URL printed by the dev server.

## Environment Variables

```makefile
GROQ_API_KEY=
GEMINI_API_KEY=
GROQ_MODEL=llama-3.3-70b-versatile
GEMINI_EMBEDDING_MODEL=gemini-embedding-001
VITE_API_BASE_URL=
```

Never commit real secrets. Keep `.env.local` untracked and configure production secrets directly in the hosting provider.

## Project Structure

```text
frontend/
  index.html
  src/
    components/ui/
    lib/
    screens/
    sections/
    main.tsx
    router.tsx
    styles.css

api/
  index.py
  main.py
  pipeline.py
  build_search_index.py

data/
  raw_docs/
  search-index.json

docs/
  ARCHITECTURE.md
  DOMAINS.md
  assets/
```

## Engineering Decisions

- **Use the requested frontend stack:** React 19, TypeScript, TanStack Router, TanStack Query, Vite, Tailwind v4, Radix-style UI, Lucide icons, and Recharts now own the browser app.
- **Keep AI in Python:** intent detection, retrieval, governance, generation, and grounding are all behind `api/main.py`.
- **Use hosted embeddings:** Gemini embeddings keep the production index path lightweight and deployment-friendly.
- **Keep retrieval simple:** the document set is small, so a static JSON vector index is easy to build, inspect, and deploy.
- **Gate before generation:** governance classification happens before answer generation, not after.
- **Expose uncertainty:** confidence, grounding warnings, context count, and sources are part of the response contract.
- **Remove inactive surfaces:** retired demo code and unused binary indexes are kept out of the production repository so future work starts from the active architecture.

## Limitations

- The best results require valid Groq and Gemini API keys.
- Without keys, the Python API uses deterministic local fallback logic for development only.
- The current index is generated from local markdown files, not a live document management system.
- There is no authentication or role-based access control yet.
- The grounding check is lexical and lightweight, not a formal proof system.
- It is a portfolio-grade MVP and still needs security review before real organizational use.

## Roadmap

- Add a persistent document ingestion dashboard.
- Add authentication and role-aware policy access.
- Add policy owner approval workflows.
- Add richer evaluation tests for refusals, escalations, and grounding.
- Add durable production logging for audit trails.
- Keep the public Vercel demo and custom domain current with releases.
- Add a clean free subdomain such as `canon-policy.pages.dev` or `canon.is-a.dev`.

## Screenshots

<img src="docs/assets/canon-home.png" alt="CANON live homepage screenshot" width="100%" />

<img src="docs/assets/canon-console.png" alt="CANON live console screenshot" width="100%" />

<img src="docs/assets/canon-workflow.png" alt="CANON live workflow screenshot" width="100%" />

<img src="docs/assets/canon-architecture.jpg" alt="CANON live architecture screenshot" width="100%" />

## Deployment

Live production deployment:

```text
https://canon.devayushrout.me
```

CANON is configured for a single Vercel project. Vercel builds the Vite frontend, generates the Gemini embedding index during deployment, and routes `/api/*` to the Python FastAPI app through `api/index.py`.

For local frontend-only verification:

```bash
pnpm run build
```

For Vercel production builds:

```bash
pnpm run build:vercel
```

Run the Python API locally:

```bash
python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

On Vercel, set `GROQ_API_KEY` and `GEMINI_API_KEY` before deploying. `GEMINI_API_KEY` is required to generate the semantic retrieval index; without it, the build skips index generation and the API falls back to lexical retrieval. `VITE_API_BASE_URL` can stay unset for same-origin Vercel deployment because the frontend calls `/api/query`.

## License

This project is released under the Apache License 2.0. See [`LICENSE`](LICENSE).
