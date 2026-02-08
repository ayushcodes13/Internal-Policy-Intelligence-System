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
import math


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Compute cosine similarity between two vectors.
    Output range: [-1, 1]
    """

    dot_product = sum(a * b for a, b in zip(vec1, vec2))

    norm_vec1 = math.sqrt(sum(a * a for a in vec1))
    norm_vec2 = math.sqrt(sum(b * b for b in vec2))

    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0

    return dot_product / (norm_vec1 * norm_vec2)


def retrieve_top_k(
    query_embedding: List[float],
    documents: List[Dict],
    allowed_owners: List[str],
    k: int = 5
) -> List[Dict]:
    """
    Retrieve top-k most relevant document chunks.

    Inputs:
    - query_embedding: embedding of user query
    - documents: list of chunks with embeddings + metadata
    - allowed_owners: owners allowed by routing (finance, security, ops)
    - k: number of chunks to return

    Output:
    - list of top-k document chunks with similarity score
    """

    scored_chunks = []

    for doc in documents:
        owner = doc["metadata"].get("owner")

        if owner not in allowed_owners:
            continue

        similarity = cosine_similarity(query_embedding, doc["embedding"])

        scored_chunks.append({
            "text": doc["text"],
            "metadata": doc["metadata"],
            "score": similarity
        })

    scored_chunks.sort(key=lambda x: x["score"], reverse=True)

    return scored_chunks[:k]