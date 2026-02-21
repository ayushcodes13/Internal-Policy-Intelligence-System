"""
Job:
The bridge between routing and vector search.

What it does:
	1.	Accepts:
	•	question
	•	allowed_sources (from routing)
	2.	Queries vector store
	3.	Filters results by metadata
	4.	Returns top-k chunks

This is where:
	•	routing actually matters
	•	metadata becomes powerful

"""
from typing import List, Dict
import numpy as np
from .embedder import embed_query
from .embedder import embed_chunks
from collections import defaultdict


def _base_key(path: str) -> str:
    """
    Extract logical document identity.
    billing_and_refund_policy_v1.md
    billing_and_refund_policy_v2.md
    → billing_and_refund_policy
    """
    filename = path.split("/")[-1]
    return filename.split("_v")[0]


def _keep_latest_versions(chunks: List[Dict]) -> List[Dict]:
    """
    From a list of chunks, keep only chunks belonging
    to the newest document version per base_key.
    """
    grouped = defaultdict(list)

    for chunk in chunks:
        path = chunk["metadata"].get("path", "")
        key = _base_key(path)
        grouped[key].append(chunk)

    result = []

    for key, group in grouped.items():
        # sort by last_updated descending
        sorted_group = sorted(
            group,
            key=lambda c: c["metadata"].get("last_updated", ""),
            reverse=True
        )

        newest_date = sorted_group[0]["metadata"].get("last_updated")

        newest_chunks = [
            c for c in sorted_group
            if c["metadata"].get("last_updated") == newest_date
        ]

        result.extend(newest_chunks)

    return result

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
        return 0.0
    return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))


from src.utils.loaders import load_markdown_files
from src.retrieval.chunker import chunk_documents
from src.retrieval.embedder import embed_chunks


def retrieve_chunks(
    user_query: str,
    allowed_owners: List[str],
    top_k: int = 5
) -> List[Dict]:
    print("RETRIEVE - allowed_owners:", allowed_owners)

    # 1️⃣ Load docs
    docs = load_markdown_files(base_path="data/raw_docs")

    # 2️⃣ Chunk
    chunks = chunk_documents(docs)

    # 3️⃣ Embed chunks
    embedded_chunks = embed_chunks(chunks)
    print("SAMPLE METADATA OWNER:", repr(embedded_chunks[0]["metadata"].get("owner")))

    # 4️⃣ Owner filter
    filtered_chunks = [
        chunk for chunk in embedded_chunks
        if chunk["metadata"].get("owner") in allowed_owners
    ]

    print("FILTERED CHUNK COUNT:", len(filtered_chunks))

    if not filtered_chunks:
        return []

    # 5️⃣ Authority dominance (version control BEFORE similarity)
    authoritative_chunks = _keep_latest_versions(filtered_chunks)

    print("AFTER VERSION FILTER:", len(authoritative_chunks))

    # 5️⃣ Embed query
    question_vector = embed_query(user_query)

    # 6️⃣ Similarity scoring
    scored_chunks = []
    for chunk in authoritative_chunks:
        score = cosine_similarity(
            question_vector,
            np.array(chunk["embedding"])
        )
        scored_chunks.append({
            "chunk_id": chunk.get("chunk_id"),
            "text": chunk["text"],
            "metadata": chunk["metadata"],
            "score": score
})

    scored_chunks.sort(key=lambda x: x["score"], reverse=True)

    return scored_chunks[:top_k]