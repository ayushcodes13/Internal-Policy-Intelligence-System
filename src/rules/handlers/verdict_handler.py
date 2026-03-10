"""
Role in simple language: “Given a governance decision, what should the system actually do?”

This file translates a GovernanceVerdict into a real system response.

Example:

If verdict = SAFE  
→ Generate grounded answer using retrieved chunks.

If verdict = REFUSE_POLICY  
→ Generate policy-backed denial.

If verdict = ESCALATE  
→ Stop generation and mark for human review.

If verdict = REFUSE_INVALID  
→ Return domain refusal message.

It does NOT:
• Decide the verdict  
• Retrieve documents  
• Modify governance logic  

It only routes execution cleanly.

This keeps:
Decision logic separate from action logic.

Without this layer, escalation, refusal, and answer generation would mix together and break architectural clarity.
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