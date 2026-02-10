"""
Constraint rules

Question:
“Is there anything in the retrieved context that must NOT be used?”

This layer operates on documents, not users and not meaning.

Handles:
	•	removal of forbidden document types
	•	enforcement of ownership boundaries
	•	prevention of internal or draft leakage

Outcome:
A cleaned context with unsafe or disallowed chunks removed.

Constraint rules:
	•	never stop execution
	•	never escalate
	•	never refuse
	•	never interpret policy meaning

They exist purely to prevent unsafe context from entering reasoning.
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