"""
	1.	FAISS → 25 candidates
	2.	Metadata filtering
	3.	Reranker scores those 25
	4.	Sort by reranker score
	5.	Take top_k = 5

FAISS becomes candidate generator.
Reranker becomes final ranker.
"""


from typing import List, Dict
from sentence_transformers import CrossEncoder

MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

reranker_model = CrossEncoder(MODEL_NAME)


def rerank(
    query: str,
    candidates: List[Dict],
) -> List[Dict]:
    """
    Re-rank candidate chunks using cross-encoder.
    """

    if not candidates:
        return []

    pairs = [(query, chunk["text"]) for chunk in candidates]

    scores = reranker_model.predict(pairs)

    for chunk, score in zip(candidates, scores):
        chunk["rerank_score"] = float(score)

    # Sort by rerank_score descending
    candidates.sort(key=lambda x: x["rerank_score"], reverse=True)

    return candidates