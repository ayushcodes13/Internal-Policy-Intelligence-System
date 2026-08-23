from __future__ import annotations

from typing import Any

from api.pipeline import detect_intents, retrieve_chunks, route_intents


def evaluate_retrieval(
    test_cases: list[dict[str, Any]],
    top_k: int = 5,
    deduplicate_documents: bool = False,
) -> dict[str, Any]:
    """Compute retrieval-only Recall@k and MRR against the current Python API pipeline."""

    total_queries = 0
    recall_hits = 0
    reciprocal_rank_sum = 0.0
    unique_doc_counts: list[int] = []

    for case in test_cases:
        query = case["query"]
        expected_sources = set(case.get("expected_sources", []))

        if not expected_sources:
            continue

        total_queries += 1
        allowed_owners = route_intents(detect_intents(query))
        retrieved_chunks = retrieve_chunks(query, allowed_owners, top_k=top_k)
        retrieved_paths = [chunk.metadata.get("path") for chunk in retrieved_chunks]

        if deduplicate_documents:
            retrieved_paths = list(dict.fromkeys(retrieved_paths))

        unique_doc_counts.append(len(retrieved_paths))

        if any(path in expected_sources for path in retrieved_paths):
            recall_hits += 1

        for index, path in enumerate(retrieved_paths, start=1):
            if path in expected_sources:
                reciprocal_rank_sum += 1.0 / index
                break

    recall_at_k = recall_hits / total_queries if total_queries else 0
    mrr = reciprocal_rank_sum / total_queries if total_queries else 0
    avg_unique_docs = sum(unique_doc_counts) / len(unique_doc_counts) if unique_doc_counts else 0

    return {
        "total_queries": total_queries,
        f"recall@{top_k}": round(recall_at_k, 4),
        "mrr": round(mrr, 4),
        "avg_unique_docs_in_top_k": round(avg_unique_docs, 2),
    }
