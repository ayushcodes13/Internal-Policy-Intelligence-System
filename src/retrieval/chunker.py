""" Job: Split documents into searchable chunks.

Why this exists:
	•	LLMs can’t search whole documents well
	•	Small chunks improve relevance
	•	Metadata sticks to each chunk

Example:

account_closure_policy.md
→ 12 chunks
→ each chunk has:
    - text
    - source_type
    - owner
    - last_updated
"""