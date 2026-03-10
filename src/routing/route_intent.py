"""
Job: Take detected intents → decide which document buckets are allowed.

Input:
[
    { "intent": "account_closure", "confidence": 0.81 }
]
Output:
{
    "allowed_owners": "ops"
}

Important:
	•	It reads rules from ROUTING_MAP.md
	•	It does NOT care about the question text
	•	It does NOT know what's inside documents

Think of it as: “Which rooms are unlocked before searching?”
"""
INTENT_TO_OWNERS = {
    "access_request": ["ops", "security"],
    "account_closure": ["ops"],
    "refund_query": ["finance"],
    "billing_query": ["finance"],
    "security_policy_query": ["security"],
    "support_process_query": ["ops"],
}

def route_intent(intents: list) -> dict:
	"""
	Routes detected intents to allowed document owners.

	Input:
		intents (list): List of detected intents with confidence

	Output:
		dict: Allowed document owners based on intents
	"""

	allowed_owners = set()

	for intent in intents:
		intent_name = intent["name"]
		if intent_name in INTENT_TO_OWNERS:
			allowed_owners.update(INTENT_TO_OWNERS[intent_name])

	return {
		"allowed_owners": list(allowed_owners)
	}
