"""
Job:
Given a user question → decide what the question is about.

Input: "How can I close my account and get a refund?"

Output:
[
    { "intent": "account_closure", "confidence": 0.81 },
    { "intent": "refund_query", "confidence": 0.67 }
]

What it does NOT do:
	•	doesn't choose documents
	•	doesn't apply rules
	•	doesn't answer anything

Think of it as: Labeling the question, not solving it.
"""

def detect_intent(user_text: str) -> dict:
    """
    Detects the intent of a user question.

    Input:
        user_text (str): The user's question

    Output:
        dict: Detected intents with confidence
    """

    # TEMPORARY: hardcoded intent detection
    # We will replace this with real logic later

    return {
        "intents": [
            {
                "name": "refund_query",
                "confidence": 0.80
            }
        ]
    }
    


