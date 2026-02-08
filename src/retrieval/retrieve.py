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


def retrieve_chunks(
    question: str,
    chunks: List[Dict],
    allowed_owners: List[str],
    top_k: int = 5
) -> List[Dict]:
    """
    Retrieve top-k relevant chunks based on semantic similarity,
    after enforcing routing constraints.

    Inputs:
        question: user query
        chunks: list of chunk dicts
                {
                "content": str,
                "embedding": np.ndarray,
                "metadata": {
                    "owner": str,
                    "source_type": str,
                    "path": str
                }
                }
        allowed_owners: owners permitted by routing
        top_k: number of chunks to return

    Output:
        List of chunks sorted by relevance score
    """

    # 1️⃣ Metadata filtering (ENFORCEMENT)
    filtered_chunks = [
        chunk for chunk in chunks
        if chunk["metadata"].get("owner") in allowed_owners
    ]

    if not filtered_chunks:
        return []

    # 2️⃣ Embed the question
    question_vector = embed_query(question)
    
    # 3️⃣ Similarity computation
    scored_chunks = []
    for chunk in filtered_chunks:
        score = cosine_similarity(question_vector, chunk["embedding"])
        scored_chunks.append({
            "text": chunk["text"],
            "metadata": chunk["metadata"],
            "score": score
        })

    # 4️⃣ Top-K selection
    scored_chunks.sort(key=lambda x: x["score"], reverse=True)

    return scored_chunks[:top_k]

if __name__ == "__main__":
    from src.utils.loaders import load_markdown_files as load_documents
    from src.retrieval.chunker import chunk_documents
    from src.retrieval.embedder import embed_chunks

    docs = load_documents(base_path="data/raw_docs")

    print("SAMPLE DOC:")
    print(docs[0])
    print(type(docs[0]))
    
    chunks = chunk_documents(docs)
    chunks = embed_chunks(chunks)

    results = retrieve_chunks(
        question="How can I close my account and get a refund?",
        chunks=chunks,
        allowed_owners=["finance"],
        top_k=3
    )

    for r in results:
        print(r["score"], r["metadata"]["path"])
        
