"""
Role in simple language:

“Show me what the retriever actually did.”

Example:

Query:
“What is the refund period?”

Diagnostics shows:
	•	Rank 1 → billing_and_refund_policy_v2 (score 0.88, is_latest=True)
	•	Rank 2 → refund_handling_sop (score 0.81)
	•	Rank 3 → billing_and_refund_policy_v1 (score 0.79, is_latest=False → filtered)

You immediately see:
	•	Good: v2 ranked top
	•	Good: v1 filtered
	•	Owner filter worked

If it ranked v1 first and v2 fifth:
Diagnostics exposes ranking weakness.

It does NOT say whether the system is correct.
It only shows internal mechanics.

Think: X-ray of retrieval.
"""