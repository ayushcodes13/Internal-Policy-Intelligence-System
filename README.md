# Enterprise SaaS Internal Compliance & IT Operations Knowledge System

This project implements a governed RAG system for enterprise SaaS internal compliance & IT operations support with a production-style internal knowledge system designed to answer employee operational and policy questions using grounded retrieval over messy enterprise documents.

The system prioritizes **correctness, traceability, and refusal over coverage**, and is explicitly designed to handle outdated documents, conflicting sources, and incomplete information.

This is not a chatbot demo. It is a reliability-focused GenAI system.

---

## Problem Statement

In real companies, internal knowledge is fragmented across policies, SOPs, FAQs, and informal notes. Documents often:

- Contradict each other
- Become outdated without clear deprecation
- Lack ownership or versioning
- Are interpreted informally by employees

Naïve LLM-based systems hallucinate confidently in these conditions, creating operational and compliance risk.

This project addresses that problem by enforcing **grounded answering, authority-aware retrieval, and explicit refusal logic**.

---

## System Scope

The system is designed to answer **internal operational and policy-related questions** for a B2B SaaS company.

It is explicitly **not allowed** to:
- Make decisions on behalf of humans
- Interpret intent or provide advice
- Guess or infer beyond documented evidence

If reliable evidence is unavailable or conflicting, the system must refuse to answer.

---

## Key Guarantees

- Answers are grounded only in retrieved internal documents
- Sources are cited with every answer
- Conflicting or outdated evidence triggers refusal
- Every query is logged for audit and debugging
- Failure modes are explicit and inspectable

---

## Document Universe

The system operates over a simulated internal document set representing a mid-sized B2B SaaS company.

### Document Types and Authority

1. **Policies (High Authority)**  
   Define company rules and constraints.

2. **SOPs (Medium Authority)**  
   Describe how teams execute processes.

3. **FAQs (Low Authority)**  
   Interpretive, simplified guidance.

4. **Notes / Memos (Very Low Authority)**  
   Informal, incomplete, or outdated information.

Authority hierarchy is strictly enforced. Conflicts between documents at the same authority level trigger refusal.

Detailed documentation is available in `DOCUMENT_UNIVERSE.md`.

---

## High-Level Architecture

1. **Ingestion**
   - Loads documents from multiple formats
   - Extracts metadata (source type, owner, last updated)
   - Chunks content for retrieval

2. **Retrieval**
   - Embedding-based semantic search
   - Returns top-k candidate chunks

3. **Ranking and Filtering**
   - Authority-aware re-ranking
   - Filters outdated or low-confidence documents

4. **Answer Generation**
   - LLM synthesizes answers strictly from provided context
   - Citations required for every response
   - Refusal enforced when evidence is insufficient or conflicting

5. **Evaluation**
   - Fixed evaluation question set
   - Tracks answer correctness, refusals, and failure modes

6. **API and Logging**
   - FastAPI-based query endpoint
   - Full query trace logged for auditing

---

## Refusal Logic (First-Class Outcome)

The system refuses to answer when:
- Required information is not explicitly present
- Authoritative documents conflict
- Only low-authority evidence exists
- Relevant documents are outdated
- The query is outside system scope

Refusal is a deliberate system decision, not an error state.

---

## Tech Stack

- Python
- FastAPI
- Vector store (FAISS / pgvector)
- LLM API (OpenAI / Claude)
- Embeddings (OpenAI / SentenceTransformers)
- Docker
- JSON-based logging

The system is framework-agnostic by design.

---

## Project Structure

project/
│
├── data/
│   └── raw_docs/
│       ├── policies/
│       ├── sops/
│       ├── faqs/
│       └── notes/
│
├── ingestion/
├── retrieval/
├── generation/
├── evaluation/
├── api/
├── logs/
│
├── DOCUMENT_UNIVERSE.md
├── README.md
└── Dockerfile

---

## Design Philosophy

- Trust > coverage
- Refusal > hallucination
- Traceability > fluency
- Simple rules > complex heuristics
- Explicit failure modes > silent errors

---

## Intended Audience

This project is intended for:
- Applied AI engineers
- GenAI product teams
- Enterprise AI and compliance-focused organizations

It is not optimized for consumer chat experiences.

---

## Status

This project is actively being built as a learning and demonstration system focused on production-grade GenAI design.


