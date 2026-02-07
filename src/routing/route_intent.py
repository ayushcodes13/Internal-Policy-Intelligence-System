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