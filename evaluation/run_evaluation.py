"""
Role in simple language:

“Is the system correct across many queries?”

Example test case:

{
  "query": "What is the refund period?",
  "expected_status": "SAFE",
  "expected_source_contains": "billing_and_refund_policy_v2"
}

Evaluation runs 20 such queries and outputs:
	•	Status accuracy: 95%
	•	Retrieval Recall@5: 90%
	•	Refusal precision: 100%

This tells you if the system is reliable overall.

Evaluation = performance scoreboard.

"""