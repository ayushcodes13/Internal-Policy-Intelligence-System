"""
Query-Time Retrieval

Uses pre-built FAISS index.

Steps:
1. Load FAISS index
2. Load metadata store
3. Embed query
4. Search index
5. Reconstruct chunks
6. Filter latest versions
7. Return top-k
"""

import os
import pickle
from typing import List, Dict

import faiss
import numpy as np

from src.retrieval.embedder import embed_query


INDEX_PATH = "data/index/faiss.index"
METADATA_PATH = "data/index/metadata.pkl"


def retrieve_chunks(
    user_query: str,
    allowed_owners: List[str],
    top_k: int = 5
) -> List[Dict]:

    if not os.path.exists(INDEX_PATH):
        raise RuntimeError("FAISS index not found. Run index_builder first.")

    # Load FAISS index
    index = faiss.read_index(INDEX_PATH)

    # Load metadata store
    with open(METADATA_PATH, "rb") as f:
        metadata_store = pickle.load(f)

    # Embed query
    query_vector = np.array(embed_query(user_query)).astype("float32")
    faiss.normalize_L2(query_vector.reshape(1, -1))

    # Search
    distances, indices = index.search(
        query_vector.reshape(1, -1),
        top_k * 3  # over-fetch to allow filtering
    )

    results = []

    for idx in indices[0]:
        if idx == -1:
            continue

        chunk_data = metadata_store.get(idx)

        if not chunk_data:
            continue

        metadata = chunk_data["metadata"]

        # Owner filter
        if metadata.get("owner") not in allowed_owners:
            continue

        # Latest version filter
        if not metadata.get("is_latest", False):
            continue

        results.append({
            "text": chunk_data["text"],
            "metadata": metadata
        })

        if len(results) >= top_k:
            break

    return results