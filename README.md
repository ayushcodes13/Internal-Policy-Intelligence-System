<div align="center">
  
# 🛡️ Internal Policy Intelligence System

*A Deterministic, Governance-Gated Retrieval-Augmented Generation (RAG) Architecture for Enterprise Operations.*

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-red?style=for-the-badge&logo=streamlit)](https://policy-intelligence-system.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Groq API](https://img.shields.io/badge/Groq-Llama_3-f57f17?style=for-the-badge)](https://groq.com/)
[![FAISS](https://img.shields.io/badge/Vector_Store-FAISS-2b3137?style=for-the-badge)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-success.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

---

**[Insert Demo Video Placeholder / Replace with Video or GIF later]**

---

## 📖 Table of Contents
- [Overview](#-overview)
- [Why Use This?](#-why-use-this)
- [System Architecture](#-system-architecture)
- [Core Capabilities](#-core-capabilities)
- [Tech Stack](#%EF%B8%8F-tech-stack)
- [Folder Structure](#-folder-structure)
- [Evaluation Baseline](#-evaluation-baseline-frozen-v1)
- [Getting Started](#-getting-started)

---

## 🎯 Overview

The **Internal Policy Intelligence System** is a heavily controlled RAG engine designed specifically for policy-bound internal operations (e.g., HR, Finance, IT Helpdesks). 

Unlike typical conversational AI chatbots that prioritize fluency, this system is designed to prioritize **correctness, traceability, and architectural clarity** over raw generative capability. It strictly enforces governance so the system knows exactly when to answer, when to refuse, and when to escalate—and importantly, *why*.

---

## 🚀 Why Use This?

In corporate environments, large language models (LLMs) cannot be allowed to guess. If an employee asks about a refund policy or a security protocol, giving a "creative" but incorrect answer is a liability.

This project solves that by enforcing:
> **Zero-Trust Generation:** The LLM is only allowed to generate a response *after* deterministic risk gates confirm the query is safe, and the context retrieved is the latest, owner-approved version. Every generated sentence is lexically verified against the source text.

---

## 🏛️ System Architecture

### Execution Flow

The pipeline enforces strict separation of concerns. No layer mixes responsibilities.

1. 🧭 **Intent Detection** → *What is the user asking?*
2. 🚦 **Routing (Owner Scoping)** → *Which departments are allowed to answer this?*
3. 🔎 **Retrieval (FAISS)** → *Version dominance (v2 > v1) & Owner filtering.*
4. 🛡️ **Constraint Filtering & Governance** → *Risk Gate: Is it safe? Should we refuse? Should we escalate?*
5. ⚖️ **Verdict Handler** → *Execute decision based on the gate.*
6. ✍️ **Strict JSON Generation** → *Formulate objective answer.*
7. 🔍 **Lexical Grounding Check** → *Verify every generated clause against the text.*

<div align="center">
  <img width="532" height="551" alt="Architecture Flow" src="https://github.com/user-attachments/assets/14eb2d06-02f0-47b6-9257-52869b0edea5" />
</div>

---

## ✨ Core Capabilities

### 🗂️ Version-Aware Retrieval
Older document versions are automatically suppressed in favor of the most recent policy version using deterministic dominance rules during the ranking phase.

### 🔐 Owner-Based Scoping
Documents are rigidly filtered based on routed intent ownership, preventing cross-domain contamination (e.g., Support agents accessing Finance internal memos).

### 🛡️ Deterministic Governance Gating
A structured governance layer classifies queries into strict verdicts: 
- ✅ `SAFE`
- 🚫 `REFUSE_POLICY`
- ❌ `REFUSE_INVALID`
- 🚨 `ESCALATE` (Limited strictly to security, legal, or compromise cases).

### ⚖️ Evidence-Backed Refusals & Lexical Grounding
Policy denials must cite exact clauses from retrieved documents. Generated `SAFE` answers undergo sentence-level lexical grounding checks. Unsupported sentences are flagged, preventing silent hallucination drift.

### 📊 Interactive Dashboard & Document Viewer
A responsive Streamlit web interface provides basic session-based anti-spam rate limiting, real-time metrics visibility (confidence, verdicts, execution latency), and an interactive document explorer for direct comparison against raw markdown policies.

---

## 🛠️ Tech Stack

*   **Frontend:** [Streamlit](https://streamlit.io/) (for rapid dashboarding & prototyping)
*   **LLM Engine:** [Groq](https://groq.com/) (Using `llama-3.3-70b-versatile` for blazing fast structured generation)
*   **Vector Database:** [FAISS (CPU)](https://github.com/facebookresearch/faiss) (For local, high-speed similarity search)
*   **Embeddings:** [Sentence-Transformers](https://sbert.net/) (`all-MiniLM-L6-v2`)
*   **Evaluation:** Custom offline Python test harnesses

---

## 📁 Folder Structure

```text
Internal-Policy-Intelligence-System/
├── app.py                      # Main Streamlit Dashboard UI
├── run_app.sh                  # UI Launcher script
├── data/
│   ├── index/                  # Compiled FAISS vectors & metadata (Git-ignored)
│   └── raw_docs/               # Source-of-truth markdown files
│       ├── policies/
│       ├── sops/
│       ├── faqs/
│       └── notes/
├── evaluation/
│   ├── metrics.py              # Recall@k, MRR calculation logic
│   └── run_evaluation.py       # Offline evaluation harness
├── src/                        # Core Application Conveyor Belt
│   ├── intent_detection/
│   ├── pipeline/               # Main rag_pipeline.py orchestration
│   ├── retrieval/              # Indexer, Embedder, Chunker, Reranker
│   ├── routing/
│   ├── rules/                  # Governance & Constraint logic
│   └── utils/
└── system/                     # Configuration Maps (Prompts, Routing tables)
```

---

## 📈 Evaluation Baseline (Frozen v1)

Retrieval and governance performance are routinely measured using structured test cases offline to prevent regressions.

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

*(No further tuning was performed after freezing the v1 baseline.)*

---

## ⚠️ Known Limitations

This system intentionally avoids overengineering. Current limitations include:
- Governance is semantic-only and operates at the query level.
- Multi-intent queries may bias dense retrieval toward dominant semantic clusters.
- Hybrid retrieval (BM25 + vector) is implemented but not enabled default.
- Grounding is lexical, not semantic.
- No production hardening for the core pipeline (async execution, distributed databases). The Streamlit frontend uses a simple in-memory session state for basic spam prevention.

These limitations are explicitly documented to maintain architectural transparency.

---

## 💻 Getting Started

### Prerequisites
- Python 3.10+
- A [Groq API Key](https://console.groq.com/keys)

### 1. Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file in the root directory:
```bash
GROQ_API_KEY=gsk_your_api_key_here
```

### 3. Build the Vector Index
Run this to parse `/data/raw_docs/` into FAISS before running the app.
```bash
python -m src.retrieval.index_builder
```

### 4. Launch the Interactive Dashboard
```bash
./run_app.sh
```

### 5. (Optional) Run Evaluations
Test the codebase against the frozen test suite to generate offline metrics:
```bash
python -m evaluation.run_evaluation
```

---

*Engineered for architectural clarity, strict governance, and measurable performance.*
