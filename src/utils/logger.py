"""
Role in simple language:

“Record what happened for every query.”

Example log entry:

{
  "query": "Can I get refund after termination?",
  "intents": ["refund_query"],
  "allowed_owners": ["finance"],
  "retrieval_time_ms": 18,
  "governance_verdict": "REFUSE_POLICY",
  "final_status": "REFUSED",
  "confidence": "high",
  "sources": ["billing_and_refund_policy_v2.md"],
  "total_latency_ms": 210
}

This is system telemetry.

If a founder asks:
“Why did it refuse that?”

You can trace it.
Logging is black-box recording.

"""