"""
Refusal rules

Question:
“Should the system answer at all?”

This is about permission.

Examples:
	•	user asks for internal-only info
	•	requests instructions to bypass security
	•	nonsense / malicious input
	•	policy-forbidden content

Outcome:
Hard stop with:

“I can’t help with that” + reason
"""

def should_refuse(user_text: str, intents: list[dict]) -> tuple[bool, str | None]:

    if not user_text.strip():
        return True, "The request is not understandable."

    forbidden_intents = {"internal_policy_request", "bypass_security"}

    for intent in intents:
        if intent["name"] in forbidden_intents:
            return True, "I can’t help with that request."

    return False, None