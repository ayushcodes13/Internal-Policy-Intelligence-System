"""
Constraint rules

Question:
“Is there anything in the retrieved context that must NOT be used?”

This is about documents, not users.

Examples:
	•	internal notes accidentally retrieved
	•	outdated policy version
	•	wrong owner (finance doc leaking into security answer)

Outcome:
Cleaned context (some chunks removed).

Never stops the system. Never escalates. Never refuses.
"""

from typing import List, Dict

def apply_constraint_rules(
    chunks: List[Dict],
    allowed_owners: List[str],
    allowed_source_types: List[str] | None = None,
) -> List[Dict]:
    """
    Constraint Rules
    ----------------
    Filters retrieved chunks based on hard constraints.

    These rules:
    - REMOVE disallowed content
    - DO NOT decide escalation
    - DO NOT decide refusal
    - DO NOT generate explanations

    Input:
        chunks: Retrieved chunks from similarity search
        allowed_owners: Owners allowed by routing (e.g. ["finance"])
        allowed_source_types: Optional source filter (e.g. ["policy", "faq"])

    Output:
        Filtered list of chunks
    """

    filtered_chunks = []

    for chunk in chunks:
        metadata = chunk.get("metadata", {})

        owner = metadata.get("owner")
        source_type = metadata.get("source_type")

        if owner not in allowed_owners:
            continue

        if allowed_source_types is not None:
            if source_type not in allowed_source_types:
                continue

        filtered_chunks.append(chunk)

    return filtered_chunks