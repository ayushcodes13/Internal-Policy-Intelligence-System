"""
2️⃣ Escalation rules

Question:
“Is this safe to answer automatically?”

This is about risk, not correctness.

Examples:
	•	refund + termination
	•	billing + legal tone
	•	security + access removal
	•	low intent confidence

Outcome:
Either:
	•	ALLOW_AUTOMATION
	•	ESCALATE_TO_HUMAN

No explanations. No answers."""


def should_escalate(
    intents: list[dict],
    chunks: list[dict]
) -> bool:

    # Rule 1: low confidence
    for intent in intents:
        if intent["confidence"] < 0.6:
            return True

    intent_names = {i["name"] for i in intents}

    # Rule 2: refund + termination
    if "refund_query" in intent_names and "account_termination" in intent_names:
        return True

    # Rule 3: security-sensitive
    if "security_policy_query" in intent_names:
        return True

    return False