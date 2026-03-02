# Internal Policy Intelligence System

## Overview

The Internal Policy Intelligence System is a controlled Retrieval-Augmented Generation (RAG) architecture designed for policy-bound internal operations environments.

It combines:
- Deterministic governance gating
- Version-aware retrieval
- Owner-scoped access filtering
- Evidence-backed generation
- Lexical grounding verification
- Offline evaluation discipline

This system is designed to prioritize correctness, traceability, and architectural clarity over raw generative capability.

---

## System Architecture

### Execution Flow

```
User Query
    ↓
Intent Detection
    ↓
Routing (Owner Scoping)
    ↓
Retrieval (FAISS)
    • Version dominance (v2 > v1)
    • Owner filtering
    • Overfetch + rerank
    ↓
Constraint Filtering
    ↓
Governance (Risk Gate)
    ↓
Verdict Handler
    ↓
Generation (Strict JSON)
    ↓
Lexical Grounding Check
    ↓
Structured Response
```

<img width="532" height="551" alt="Screenshot 2026-03-02 at 11 08 22 PM" src="https://github.com/user-attachments/assets/14eb2d06-02f0-47b6-9257-52869b0edea5" />

The pipeline enforces strict separation of concerns:
- **Governance** makes decisions.
- **Retrieval** fetches context.
- **Generation** synthesizes.
- **Grounding** verifies.
- **Handlers** execute.

No layer mixes responsibilities.

---

## Core Capabilities

### Version-Aware Retrieval
Older document versions are automatically suppressed in favor of the most recent policy version using deterministic dominance rules.

### Owner-Based Scoping
Documents are filtered based on routed intent ownership, preventing cross-domain contamination.

### Deterministic Governance Gating
A structured governance layer classifies queries into:
- `SAFE`
- `REFUSE_POLICY`
- `REFUSE_INVALID`
- `ESCALATE`

Escalation is strictly limited to security, legal, or compromise cases.

### Evidence-Backed Refusals
Policy denials must cite exact clauses from retrieved documents.

### Lexical Grounding Verification
Generated `SAFE` answers undergo sentence-level lexical grounding checks:
- Unsupported sentences are flagged.
- Confidence is downgraded if grounding is weak.
- Unsupported clauses are logged.

This prevents silent hallucination drift.

### Offline Evaluation Harness
Retrieval and governance performance are measured using structured test cases.

---

## Evaluation Baseline (Frozen v1)

### Retrieval Evaluation
| Metric | Value |
|---|---|
| Total Queries Evaluated | 18 |
| Recall@5 | 0.8889 |
| MRR | 0.5259 |

### Governance Evaluation
| Metric | Value |
|---|---|
| Verdict Accuracy | 85% (20 test cases) |

These metrics represent the frozen v1 baseline. No further tuning was performed after freezing.

---

## Known Limitations

This system intentionally avoids overengineering. Current limitations include:

- Governance is semantic-only and operates at query level.
- Policy eligibility reasoning (e.g., conditional policy logic) is not implemented.
- Multi-intent queries may bias dense retrieval toward dominant semantic clusters.
- Hybrid retrieval (BM25 + vector) is implemented but not enabled.
- Grounding is lexical, not semantic.
- No production hardening (rate limiting, async execution, deployment config).

These limitations are explicitly documented to maintain architectural transparency.

---

## Design Principles

This system was built with the following principles:
- Layered separation of responsibility
- Deterministic risk control before generation
- Evidence-backed outputs
- Measurable performance
- Minimal hidden logic

The goal is architectural clarity, not maximal feature density.

---

## How to Run

### Build Index
```bash
python -m src.retrieval.index_builder
```

### Run Evaluation
```bash
python -m evaluation.run_evaluation
```

### Run Pipeline Locally
```bash
python -m src.pipeline.rag_pipeline
```

> Ensure `GROQ_API_KEY` is set in your environment.

---

## What This Project Represents

This project demonstrates:
- A layered RAG architecture
- Version-aware policy retrieval
- Deterministic governance gating
- Execution isolation
- Offline evaluation discipline
- Basic grounding enforcement

It is a controlled internal knowledge system, not a generic chatbot wrapper.
