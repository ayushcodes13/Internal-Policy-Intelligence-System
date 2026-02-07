Got it. No theory. No extras.
Here is a direct, clean, copy-pastable ROUTING.md that matches everything we finalized.
This is the final engineering-correct version.

⸻


# ROUTING.md

## Purpose

Routing determines **which document groups are eligible for retrieval**
after intent detection.

Routing does NOT:
- detect intent
- understand the question
- apply rules or policies
- resolve conflicts
- choose answers

Routing ONLY maps:

**intent → allowed document categories**

This keeps routing simple, stable, and low-risk.

---

## Input

Routing receives:
- One or more detected intents
- Each intent has a confidence score

Example:
```yaml
intent: account_closure
confidence: 0.82


⸻

Output

Routing produces:
	•	A list of allowed document groups
	•	Nothing else

Example:

allowed_sources:
  - policies
  - faqs


⸻

Core Rules
	1.	Allow-list only
	•	Only explicitly allowed document groups are retrievable
	•	Everything else is excluded by default
	2.	No file-level routing
	•	Routing never names individual files
	•	Routing works only at document-group level
	3.	No conditional logic
	•	Routing does not inspect question wording
	•	Routing does not reason about edge cases
	•	Routing does not handle conflicts
	4.	Notes are always excluded
	•	notes/ are never routed
	•	Notes exist only for humans and future rules

⸻

Routing Table

Intent: access_request

Allowed document groups:
	•	policies
	•	sops
	•	faqs

Excluded:
	•	notes

⸻

Intent: account_closure

Allowed document groups:
	•	policies
	•	faqs

Excluded:
	•	sops
	•	notes

⸻

Intent: refund_query

Allowed document groups:
	•	policies
	•	sops
	•	faqs

Excluded:
	•	notes

⸻

Intent: billing_query

Allowed document groups:
	•	policies
	•	faqs

Excluded:
	•	sops
	•	notes

⸻

Intent: security_policy_query

Allowed document groups:
	•	policies
	•	faqs

Excluded:
	•	sops
	•	notes

⸻

Intent: support_process_query

Allowed document groups:
	•	sops
	•	faqs

Excluded:
	•	policies
	•	notes

⸻

Multiple Intents

If multiple intents are detected:
	•	Allowed document groups are merged
	•	notes remain excluded in all cases

Example:

intents:
  - refund_query
  - billing_query

allowed_sources:
  - policies
  - sops
  - faqs


⸻

Out of Scope

Routing does NOT handle:
	•	document conflicts
	•	outdated content
	•	compliance logic
	•	escalation
	•	refusal
	•	answer generation

These belong to:
	•	rules layer
	•	governance layer
	•	traceability layer

⸻

Design Principle

Routing is intentionally simple.

Simple routing:
	•	breaks less
	•	scales better
	•	is easy to audit
	•	survives document growth

All intelligence lives:
	•	before routing → intent detection
	•	after retrieval → rules and response logic

Routing is just the bridge.

---

This is **correct**, **minimal**, and **production-safe**.

Next step when you’re ready:
- implement routing as a small function that reads this logic
- then move to **rules + traceability**, where real complexity belongs