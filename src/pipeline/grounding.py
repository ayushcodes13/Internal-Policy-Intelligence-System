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