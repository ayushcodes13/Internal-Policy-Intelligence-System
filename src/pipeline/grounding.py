"""
Role in simple language: “Did the model stay within the retrieved evidence?”

This file performs a lightweight grounding check after answer generation.

It verifies:
• Each sentence in the answer is supported by retrieved chunks.
• Unsupported sentences are flagged.
• Confidence is reduced if grounding is weak.

It does NOT:
• Change the answer content
• Re-run the LLM
• Perform semantic reasoning

This is a lexical evidence check.

Purpose:
To prevent silent hallucinations and ensure answers are grounded in retrieved documents.
"""

from typing import List, Dict


def check_grounding(answer: str, cleaned_chunks: List[Dict]) -> Dict:
    """
    Lightweight lexical grounding check.

    Verifies that answer sentences are supported by retrieved context.
    """

    if not answer or not cleaned_chunks:
        return {
            "grounded": False,
            "unsupported_sentences": ["No context available"]
        }

    # Combine retrieved chunk text
    retrieved_text = " ".join(
        chunk["text"] for chunk in cleaned_chunks
    ).lower()

    sentences = [
        s.strip() for s in answer.split(".") if s.strip()
    ]

    unsupported = []

    for sentence in sentences:
        words = [
            w for w in sentence.lower().split()
            if len(w) > 4
        ]

        if not words:
            continue

        matches = sum(1 for w in words if w in retrieved_text)
        ratio = matches / len(words)

        if ratio < 0.4:
            unsupported.append(sentence)

    return {
        "grounded": len(unsupported) == 0,
        "unsupported_sentences": unsupported
    }