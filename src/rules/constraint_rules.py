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

def apply_constraints(chunks: list[dict]) -> list[dict]:
    cleaned = []

    for chunk in chunks:
        metadata = chunk["metadata"]

        # hard block internal notes
        if metadata.get("source_type") == "note":
            continue

        cleaned.append(chunk)

    return cleaned