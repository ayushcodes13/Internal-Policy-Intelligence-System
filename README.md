# Enterprise SaaS Internal Compliance & IT Operations Knowledge System

**Governed Retrieval-Augmented Generation (RAG) Pipeline**

---

## Overview

This project implements a governed Retrieval-Augmented Generation (RAG) system designed for internal enterprise support operations.

The system simulates a production-grade internal knowledge assistant capable of:

- Handling policy and SOP-based queries
- Enforcing document-level governance
- Preventing cross-domain leakage
- Applying structured rule layers before generation

Unlike generic chatbot implementations, this system emphasizes **controlled retrieval**, **rule enforcement**, and **explainable decision layers**.

---

## System Architecture

```
User Query
    ↓
Intent Detection
    ↓
Routing (Owner-Based Scope)
    ↓
Retrieval (Dense Similarity Search)
    ↓
Constraint Cleaning
    ↓
Governance Verdict
    ↓
Generation (Placeholder)
```

Each stage is intentionally separated to ensure:

- **Auditability** – Every decision is traceable
- **Replaceability** – Components can be swapped independently
- **Production extensibility** – Easy to add new features
- **Controlled context usage** – No unfiltered content reaches generation

---

## Core Design Principles

### 1. Separation of Concerns

Each component performs exactly one job:

- **Intent detection** labels the query
- **Routing** determines allowed document owners
- **Retrieval** selects relevant chunks
- **Constraint rules** clean unsafe or outdated content
- **Governance rules** decide escalation or refusal
- **Generation** produces the final response

No layer mixes responsibilities.

### 2. Owner-Based Isolation

Documents are segmented by metadata:

- `finance`
- `security`
- `ops`
- etc.

Routing restricts retrieval to allowed owners, preventing cross-domain leakage.

### 3. Governance Before Generation

Before any response is generated:

- Outdated documents are removed
- Internal notes are filtered
- Conflicts between versions are resolved
- Escalation and refusal logic is applied

The system is designed to **fail safely**, not optimistically.

---

## Project Structure

```
data/
  raw_docs/
    policies/
    sops/
    faqs/
    notes/

system/
  intents/
  routing/
  retrieval/

src/
  intent_detection/
  routing/
  retrieval/
    chunker.py
    embedder.py
    vector_store.py
    retrieve.py
  rules/
    constraint_rules.py
    governance_rules.py
  pipeline/
    rag_pipeline.py
```

---

## Retrieval Strategy (Current Version)

- Dense embeddings using `sentence-transformers`
- Cosine similarity ranking
- Metadata filtering (owner-based scope enforcement)
- Top-k chunk retrieval

This version uses brute-force similarity. The architecture is designed to allow easy migration to:

- FAISS indexing
- Hybrid retrieval (BM25 + dense)
- Cross-encoder reranking

without modifying intent, routing, or rule layers.

---

## Governance Layers

### Constraint Rules

- Remove internal notes
- Drop outdated policy versions
- Enforce owner boundaries
- Clean retrieved context

### Governance Rules

- Detect escalation conditions
- Identify unsafe or invalid requests
- Determine final system action

**Possible outcomes:**

- Proceed to generation
- Escalate to human review
- Refuse with explanation

---

## Current Capabilities

- End-to-end structured RAG flow
- Metadata-aware retrieval
- Deterministic rule enforcement
- Clear architectural boundaries
- Extendable retrieval layer
- Modular governance system

---

## Future Enhancements (Planned)

- Hybrid retrieval (BM25 + dense fusion)
- Vector indexing with FAISS
- Retrieval evaluation metrics
- Faithfulness scoring
- Latency and cost logging
- Reranking with cross-encoders

---

## Intended Use Case

This system simulates an internal enterprise support assistant for:

- Policy interpretation
- Refund and billing queries
- Security documentation
- SOP-based workflows
- Incident handling references

The architecture is domain-agnostic but designed for enterprise environments requiring governance.

---

## Why This Project Matters

**This is not a chatbot.**

It is a controlled, governed knowledge retrieval system built with production constraints in mind:

- **Safety over convenience**
- **Traceability over heuristics**
- **Modularity over entanglement**

It reflects real-world enterprise AI system design.

---

## Getting Started

*(Add installation and usage instructions here)*

---

## License

*(Add license information here)*

---

## Contact

*(Add contact information here)*
