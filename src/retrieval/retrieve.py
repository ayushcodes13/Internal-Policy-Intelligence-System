from typing import List, Dict, Union
import numpy as np
import faiss
import pickle
import os

from src.retrieval.embedder import embed_query
from src.retrieval.reranker import rerank
# Hybrid import (safe even if file not fully used yet)
try:
    from src.retrieval.hybrid import hybrid_merge
except Exception:
    hybrid_merge = None

INDEX_PATH = "data/index/faiss.index"
METADATA_PATH = "data/index/metadata.pkl"

# ==============================
# Feature Flags (Future-Proof)
# ==============================
ENABLE_HYBRID = False      # OFF by default
ENABLE_RERANKER = True     # Keep current behavior


def retrieve_chunks(
    user_query: str,
    allowed_owners: List[str],
    top_k: int = 5,
    debug: bool = False
) -> Union[List[Dict], Dict]:

    if not os.path.exists(INDEX_PATH):
        raise RuntimeError("FAISS index not found. Run index_builder first.")

    # Load index + metadata
    index = faiss.read_index(INDEX_PATH)

    with open(METADATA_PATH, "rb") as f:
        metadata_store = pickle.load(f)

    # 1️⃣ Embed query
    query_vector = np.array([embed_query(user_query)]).astype("float32")

    # 2️⃣ Over-fetch
    overfetch_k = top_k * 8
    distances, indices = index.search(query_vector, overfetch_k)

    print("Overfetch_k:", overfetch_k)
    print("Returned indices:", len(indices[0]))

    candidates = []
    diagnostics = []

    for score, idx in zip(distances[0], indices[0]):

        if idx == -1:
            continue

        chunk = metadata_store[idx]

        diag_entry = {
            "path": chunk["metadata"].get("path"),
            "owner": chunk["metadata"].get("owner"),
            "is_latest": chunk["metadata"].get("is_latest"),
            "score": float(score),
            "filtered_out": False,
            "reason": None
        }

        # Owner filter
        if chunk["metadata"].get("owner") not in allowed_owners:
            diag_entry["filtered_out"] = True
            diag_entry["reason"] = "owner_mismatch"
            diagnostics.append(diag_entry)
            continue

        # Version dominance (is_latest filter)
        if not chunk["metadata"].get("is_latest", True):
            diag_entry["filtered_out"] = True
            diag_entry["reason"] = "not_latest_version"
            diagnostics.append(diag_entry)
            continue

        diag_entry["filtered_out"] = False
        diagnostics.append(diag_entry)

        candidates.append({
            "chunk_id": chunk.get("chunk_id"),
            "text": chunk.get("text"),
            "metadata": chunk.get("metadata"),
            "score": float(score)
        })

    # ✅ Print after filtering
    print("Candidates after metadata filter:", len(candidates))

    # 3️⃣ Sort by FAISS similarity
    candidates.sort(key=lambda x: x["score"], reverse=True)

    # ✅ Print ranking before rerank
    print("\nTop candidates after FAISS (before rerank):")
    for i, chunk in enumerate(candidates[:10]):
        print(f"{i+1}.", chunk["metadata"].get("path"), "| Score:", chunk["score"])

    # ==============================
    # Hybrid (Optional, OFF by default)
    # ==============================
    if ENABLE_HYBRID and hybrid_merge is not None:
        try:
            # Placeholder: vector-only fallback if no BM25 yet
            # You can later plug real BM25 results here
            candidates = hybrid_merge(candidates, [])
        except Exception:
            pass

    # ==============================
    # Reranker (Controlled by flag)
    # ==============================
    if ENABLE_RERANKER and candidates:
        try:
            reranked = rerank(user_query, candidates)
        except Exception:
            reranked = candidates
    else:
        reranked = candidates

    final_chunks = reranked[:top_k]

    if debug:
        return {
            "final_chunks": final_chunks,
            "diagnostics": diagnostics
        }

    return final_chunks


"""
Role of Retrieval diagnostic in simple language:

“Show me what the retriever actually did.”

Example:

Query:
“What is the refund period?”

Diagnostics shows:
    • Rank 1 → billing_and_refund_policy_v2 (score 0.88, is_latest=True)
    • Rank 2 → refund_handling_sop (score 0.81)
    • Rank 3 → billing_and_refund_policy_v1 (score 0.79, is_latest=False → filtered)

You immediately see:
    • Good: v2 ranked top
    • Good: v1 filtered
    • Owner filter worked

If it ranked v1 first and v2 fifth:
Diagnostics exposes ranking weakness.

It does NOT say whether the system is correct.
It only shows internal mechanics.

Think: X-ray of retrieval.
"""