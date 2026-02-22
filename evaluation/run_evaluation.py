"""
Role in simple language: “Is the system correct across many queries?”

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

If you ever:
	•	Change retrieval
	•	Add hybrid search
	•	Switch embedding model
	•	Tune governance prompts

Evaluation tells you:
Did it improve or did it break?

THIS IS ONLY USED FOR OFFLINE CASE AND NOT USED IN REALTIME DECISION MAKING.
Evaluation exists for one reason:

To know if your system is actually good — instead of just feeling good about it.
"""