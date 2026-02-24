"""
generate a short readme for what this file do
"""
from src.rules.types import GovernanceVerdict

def handle_verdict(
    verdict,
    user_query,
    cleaned_chunks,
    pipeline
):

    if verdict == GovernanceVerdict.REFUSE_INVALID:
        return {
            "status": "REFUSED",
            "answer": None,
            "message": "I cannot assist with that request as it is not related to this system.",
            "sources": [],
            "supporting_clauses": [],
            "confidence": "low",
            "context_used": 0,
        }

    if verdict == GovernanceVerdict.ESCALATE:
        return {
            "status": "ESCALATED",
            "answer": None,
            "message": "This request requires human review and has been escalated.",
            "sources": [],
            "supporting_clauses": [],
            "confidence": "low",
            "context_used": len(cleaned_chunks),
        }

    if verdict == GovernanceVerdict.REFUSE_POLICY:
        return pipeline._generate_policy_denial(
            user_query,
            cleaned_chunks
        )

    if verdict == GovernanceVerdict.SAFE:
        return pipeline._generate_answer(
            user_query,
            cleaned_chunks
        )