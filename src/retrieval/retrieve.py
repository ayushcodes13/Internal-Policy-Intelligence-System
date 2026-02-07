"""
Job:
The bridge between routing and vector search.

What it does:
	1.	Accepts:
	•	question
	•	allowed_sources (from routing)
	2.	Queries vector store
	3.	Filters results by metadata
	4.	Returns top-k chunks

This is where:
	•	routing actually matters
	•	metadata becomes powerful

"""