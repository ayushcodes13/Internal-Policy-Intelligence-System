"""
Job:
Turn text chunks into vectors.

Input: text
Output: numbers

No business logic. No intelligence.

It's a translator.
"""

from typing import List, Dict
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

def embed_chunks(chunks: List[Dict]) -> List[Dict]:
    """
    Convert text chunks into vector embeddings using a local transformer model.

    Input:
        chunks: List of dicts with 'text' and 'metadata'

    Output:
        Same list with an added 'embedding' field
    """

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    embedded_chunks = []
    for chunk, vector in zip(chunks, embeddings):
        embedded_chunks.append({
            "chunk_id": chunk.get("chunk_id"),
            "text": chunk["text"],
            "embedding": vector.tolist(),  
            "metadata": chunk["metadata"]
        })
    
    return embedded_chunks

def embed_query(question: str) -> List[float]:
    """
    Embed a single user query into a vector.
    """
    vector = model.encode(
        question,
        convert_to_numpy=True,
        normalize_embeddings=True
    )
    return vector.tolist()

if __name__ == "__main__":
    test_chunks = [
        {
            "text": "Refunds are processed within 14 days.",
            "metadata": {"owner": "finance"}
        },
        {
            "text": "Account closure requires identity verification.",
            "metadata": {"owner": "ops"}
        }
    ]

    result = embed_chunks(test_chunks)
    print("Vector length:", len(result[0]["embedding"]))
    print("Sample vector (first 5 values):", result[0]["embedding"][:5])