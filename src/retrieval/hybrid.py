## for future purpose only! not implemented in main pipeline yet. 

from typing import List, Dict

def hybrid_merge(
    vector_candidates: List[Dict],
    bm25_candidates: List[Dict],
    alpha: float = 0.6
) -> List[Dict]:
    """
    Fuse vector + BM25 scores.
    alpha = weight for vector score
    """

    # Normalize scores first (very important)
    def normalize(scores):
        if not scores:
            return scores
        min_s = min(scores)
        max_s = max(scores)
        if max_s - min_s == 0:
            return [1.0 for _ in scores]
        return [(s - min_s) / (max_s - min_s) for s in scores]

    vector_scores = normalize([c["score"] for c in vector_candidates])
    bm25_scores = normalize([c["score"] for c in bm25_candidates])

    fused = {}

    # Add vector scores
    for idx, c in enumerate(vector_candidates):
        key = c["chunk_id"]
        fused[key] = {
            "chunk": c,
            "score": alpha * vector_scores[idx]
        }

    # Add BM25 scores
    for idx, c in enumerate(bm25_candidates):
        key = c["chunk_id"]
        if key in fused:
            fused[key]["score"] += (1 - alpha) * bm25_scores[idx]
        else:
            fused[key] = {
                "chunk": c,
                # "score": (1 - alpha) * bm25_scores[idx]
            }

    merged = []
    for item in fused.values():
        chunk = item["chunk"]
        chunk["score"] = item["score"]
        merged.append(chunk)

    merged.sort(key=lambda x: x["score"], reverse=True)
    return merged