"""
Refusal Handler

Purpose:
Return structured refusal responses.

This file:
- Maps governance verdicts to user-safe messages
- Does NOT decide refusal
"""

from src.rules.types import GovernanceVerdict


def handle_refusal(verdict: GovernanceVerdict) -> dict:
    """
    Returns structured refusal message.
    """

    if verdict == GovernanceVerdict.REFUSE_INVALID:
        return {
            "status": "REFUSED",
            "message": "I cannot assist with that request as it is not related to this system."
        }

    if verdict == GovernanceVerdict.REFUSE_POLICY:
        return {
            "status": "REFUSED",
            "message": "This request cannot be fulfilled due to existing policy restrictions."
        }

    return {
        "status": "REFUSED",
        "message": "Request cannot be processed."
    }