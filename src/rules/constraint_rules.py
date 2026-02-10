def apply_constraints(chunks: list[dict]) -> list[dict]:
    cleaned = []

    for chunk in chunks:
        metadata = chunk["metadata"]

        # hard block internal notes
        if metadata.get("source_type") == "note":
            continue

        cleaned.append(chunk)

    return cleaned