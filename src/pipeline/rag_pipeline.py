"""
Job: Wire everything together in order.

Rough flow:
question
→ detect_intent
→ route_intent
→ retrieve
→ return chunks (for now)

Later this file will grow:
	•	rules
	•	refusals
	•	final answer generation

It does not think, not decide, not store knowledge.
It only connects the parts in the correct order.
"""