from typing import List, Dict
from src.retrieval.retrieve import retrieve_chunks


def evaluate_retrieval(
    test_cases: List[Dict],
    top_k: int = 5,
    deduplicate_documents: bool = False
) -> Dict:
    """
    Computes:
    - Recall@k
    - MRR (Mean Reciprocal Rank)

    Retrieval ONLY.
    No governance.
    No generation.
    """

    total_queries = 0
    recall_hits = 0
    reciprocal_rank_sum = 0.0
    unique_doc_counts = []

    for case in test_cases:
        query = case["query"]
        expected_sources = set(case.get("expected_sources", []))

        # Skip cases where no expected sources exist
        if not expected_sources:
            continue

        total_queries += 1

        retrieved_chunks = retrieve_chunks(
            user_query=query,
            allowed_owners=["finance", "ops", "security", "support"],
            top_k=top_k,
            debug=False
        )

        # Extract paths from chunks
        retrieved_paths = [
            chunk["metadata"].get("path")
            for chunk in retrieved_chunks
        ]

        # --- Evaluation-only deduplication ---
        if deduplicate_documents:
            unique_paths = []
            for path in retrieved_paths:
                if path not in unique_paths:
                    unique_paths.append(path)
            retrieved_paths = unique_paths

        unique_doc_counts.append(len(retrieved_paths))

        # --- Recall@k ---
        hit = any(path in expected_sources for path in retrieved_paths)
        if hit:
            recall_hits += 1

        # --- MRR ---
        rank = 0
        for idx, path in enumerate(retrieved_paths, start=1):
            if path in expected_sources:
                rank = idx
                break

        if rank > 0:
            reciprocal_rank_sum += 1.0 / rank

    recall_at_k = recall_hits / total_queries if total_queries else 0
    mrr = reciprocal_rank_sum / total_queries if total_queries else 0
    avg_unique_docs = (
        sum(unique_doc_counts) / len(unique_doc_counts)
        if unique_doc_counts else 0
    )

    return {
        "total_queries": total_queries,
        f"recall@{top_k}": round(recall_at_k, 4),
        "mrr": round(mrr, 4),
        "avg_unique_docs_in_top_k": round(avg_unique_docs, 2),
    }