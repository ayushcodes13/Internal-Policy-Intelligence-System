"""
Job:
Store and search embeddings.

It answers:

“Given this question vector, which chunks are closest?”

It does NOT know:
	•	what is correct
	•	what is allowed
	•	what should be answered

Just similarity.
"""
from typing import List, Dict
import math


class VectorStore:
    """
    Simple in-memory vector store.

    Stores:
    - embedding vectors
    - original text chunks
    - metadata for each chunk
    """

    def __init__(self):
        self.vectors: List[List[float]] = []
        self.texts: List[str] = []
        self.metadatas: List[Dict] = []

    def add(self, vector: List[float], text: str, metadata: Dict):
        """
        Add a single vector entry to the store.
        """
        self.vectors.append(vector)
        self.texts.append(text)
        self.metadatas.append(metadata)

    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        """
        Compute cosine similarity between two vectors.
        """
        dot_product = sum(a * b for a, b in zip(v1, v2))
        norm_v1 = math.sqrt(sum(a * a for a in v1))
        norm_v2 = math.sqrt(sum(b * b for b in v2))

        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0

        return dot_product / (norm_v1 * norm_v2)

    def search(self, query_vector: List[float], top_k: int = 5):
        """
        Search for the most similar vectors.

        Returns:
            List of dicts containing:
            - score
            - text
            - metadata
        """
        scores = []

        for idx, vector in enumerate(self.vectors):
            score = self._cosine_similarity(query_vector, vector)
            scores.append((score, idx))

        # Sort by similarity score (highest first)
        scores.sort(reverse=True, key=lambda x: x[0])

        results = []
        for score, idx in scores[:top_k]:
            results.append({
                "score": score,
                "text": self.texts[idx],
                "metadata": self.metadatas[idx]
            })

        return results