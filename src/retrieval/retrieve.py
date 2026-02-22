from typing import List, Dict, Union
import numpy as np
import faiss
import pickle
import os

from src.retrieval.embedder import embed_query


INDEX_PATH = "data/index/faiss.index"
METADATA_PATH = "data/index/metadata.pkl"


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
    overfetch_k = top_k * 5
    distances, indices = index.search(query_vector, overfetch_k)

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

    # 3️⃣ Sort remaining by similarity (FAISS already sorted but we ensure)
    candidates.sort(key=lambda x: x["score"], reverse=True)

    final_chunks = candidates[:top_k]

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
	•	Rank 1 → billing_and_refund_policy_v2 (score 0.88, is_latest=True)
	•	Rank 2 → refund_handling_sop (score 0.81)
	•	Rank 3 → billing_and_refund_policy_v1 (score 0.79, is_latest=False → filtered)

You immediately see:
	•	Good: v2 ranked top
	•	Good: v1 filtered
	•	Owner filter worked

If it ranked v1 first and v2 fifth:
Diagnostics exposes ranking weakness.

It does NOT say whether the system is correct.
It only shows internal mechanics.

Think: X-ray of retrieval.
"""