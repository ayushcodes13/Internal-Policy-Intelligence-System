"""
Constraint Rules

Question:
“Is there anything in the retrieved context that must NOT be used?”

This is about documents, not users.

Examples:
    • internal notes accidentally retrieved
    • wrong owner leakage
    • malformed metadata

Outcome:
Cleaned context (some chunks removed).

Never stops the system. Never escalates. Never refuses.
"""

from typing import List, Dict


def apply_constraints(
    retrieved_chunks: List[Dict],
    allowed_owners: List[str],
) -> List[Dict]:
    """
    Cleans retrieved chunks.

    Steps:
        1. Remove forbidden source types
        2. Enforce owner scope (defensive)
        3. Deduplicate
    """

    # 1️⃣ Remove forbidden source types (e.g., internal notes)
    filtered = [
        chunk for chunk in retrieved_chunks
        if chunk.get("metadata", {}).get("source_type") != "notes"
    ]

    # 2️⃣ Defensive owner enforcement
    filtered = [
        chunk for chunk in filtered
        if chunk.get("metadata", {}).get("owner") in allowed_owners
    ]

    # 3️⃣ Deduplicate (by chunk_id if present)
    seen = set()
    final_chunks = []

    for chunk in filtered:
        chunk_id = chunk.get("chunk_id")

        # If no chunk_id exists, allow it (defensive behavior)
        if not chunk_id:
            final_chunks.append(chunk)
            continue

        if chunk_id not in seen:
            seen.add(chunk_id)
            final_chunks.append(chunk)

    return final_chunks