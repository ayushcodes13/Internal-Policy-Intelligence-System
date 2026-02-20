"""
Constraint Rules

Question:
“Is there anything in the retrieved context that must NOT be used?”

This is about documents, not users.

Examples:
    • internal notes accidentally retrieved
    • outdated policy version
    • wrong owner leakage

Outcome:
Cleaned context (some chunks removed).

Never stops the system. Never escalates. Never refuses.
"""

from typing import List, Dict
from collections import defaultdict


def apply_constraints(
    retrieved_chunks: List[Dict],
    allowed_owners: List[str]
) -> List[Dict]:
    """
    Cleans retrieved chunks.

    Steps:
        1. Remove forbidden source types
        2. Enforce owner scope
        3. Resolve version dominance
        4. Deduplicate
    """

    # 1️⃣ Remove forbidden source types
    filtered = [
        chunk for chunk in retrieved_chunks
        if chunk["metadata"].get("source_type") != "notes"
    ]

    # 2️⃣ Enforce allowed owners (defensive layer)
    filtered = [
        chunk for chunk in filtered
        if chunk["metadata"].get("owner") in allowed_owners
    ]

    # 3️⃣ Resolve version dominance
    # Group by base document path (ignoring version if present)
    grouped = defaultdict(list)

    for chunk in filtered:
        path = chunk["metadata"].get("path", "")
        base_key = _base_document_key(path)
        grouped[base_key].append(chunk)

    cleaned = []

    for base_key, chunks in grouped.items():
        # Keep only newest version based on last_updated
        newest_chunks = _keep_newest_version(chunks)
        cleaned.extend(newest_chunks)

    # 4️⃣ Deduplicate (by chunk_id if exists)
    seen = set()
    final_chunks = []

    for chunk in cleaned:
        chunk_id = chunk.get("chunk_id")
        if chunk_id and chunk_id not in seen:
            seen.add(chunk_id)
            final_chunks.append(chunk)

    return final_chunks


def _base_document_key(path: str) -> str:
    """
    Extracts a base identifier for version grouping.
    Example:
        billing_and_refund_policy_v1.md
        billing_and_refund_policy_v2.md
    → billing_and_refund_policy
    """
    filename = path.split("/")[-1]
    return filename.split("_v")[0]


def _keep_newest_version(chunks: List[Dict]) -> List[Dict]:
    """
    Keeps only chunks belonging to the most recent version.
    """

    if not chunks:
        return []

    # Sort by last_updated descending
    sorted_chunks = sorted(
        chunks,
        key=lambda c: c["metadata"].get("last_updated", ""),
        reverse=True
    )

    # Determine newest date
    newest_date = sorted_chunks[0]["metadata"].get("last_updated")

    return [
        chunk for chunk in sorted_chunks
        if chunk["metadata"].get("last_updated") == newest_date
    ]