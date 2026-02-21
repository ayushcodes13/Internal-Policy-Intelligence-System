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

    # 1️⃣ Load docs
    docs = load_markdown_files(base_path="data/raw_docs")

    # 2️⃣ Chunk
    chunks = chunk_documents(docs)

    # 3️⃣ Embed chunks
    embedded_chunks = embed_chunks(chunks)

    # 4️⃣ Metadata filter
    filtered_chunks = [
        chunk for chunk in embedded_chunks
        if chunk["metadata"].get("owner") in allowed_owners
    ]

    if not filtered_chunks:
        return []

    # 5️⃣ Embed query
    question_vector = embed_query(user_query)

    # 6️⃣ Similarity scoring
    scored_chunks = []
    for chunk in filtered_chunks:
        score = cosine_similarity(
            question_vector,
            np.array(chunk["embedding"])
        )
        scored_chunks.append({
            "content": chunk["text"],
            "metadata": chunk["metadata"],
            "score": score
        })

    scored_chunks.sort(key=lambda x: x["score"], reverse=True)

    return scored_chunks[:top_k]