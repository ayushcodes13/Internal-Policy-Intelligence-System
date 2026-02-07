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

