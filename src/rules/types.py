"""
Governance Verdict Types

Question:
“What are the only valid outcomes governance is allowed to return?”

This file defines the finite decision states of the system.

Why this exists:
    • prevents silent string bugs
    • enforces controlled system states
    • guarantees governance returns only valid outcomes
    • keeps pipeline logic predictable

Without this:
    • typos fail silently
    • inconsistent verdict labels break flow
    • state handling becomes fragile

Outcome:
Governance must return exactly one of:

    SAFE
    ESCALATE
    REFUSE_INVALID
    REFUSE_POLICY
"""
from enum import Enum
class GovernanceVerdict(Enum):
    SAFE = "SAFE"
    ESCALATE = "ESCALATE"
    REFUSE_INVALID = "REFUSE_INVALID"
    REFUSE_POLICY = "REFUSE_POLICY"