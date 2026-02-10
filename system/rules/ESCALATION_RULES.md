# ESCALATION_RULES.md

## Purpose

Escalation rules decide **whether a user query should be handled automatically or routed to a human agent**.

Escalation does NOT:
- block the user
- refuse to answer
- generate explanations
- modify documents

Escalation ONLY answers one question:

**"Is it safe and appropriate to answer this automatically?"**

---

## Position in Pipeline

Escalation rules run **after constraint rules** and **before refusal rules**.

Fixed execution order:
1. Constraint rules
2. Escalation rules
3. Refusal rules
4. Final verdict

This order must not be changed.

---

## Inputs

Escalation rules receive:
- Detected intents with confidence scores
- Cleaned retrieved chunks (after constraints)
- Routing scope (document owners / domains)

Example input:
```json
{
  "intents": [
    { "name": "refund_query", "confidence": 0.78 },
    { "name": "account_termination", "confidence": 0.74 }
  ],
  "chunks": [...],
  "allowed_owners": ["finance"]
}
```

---

## Outputs

Escalation rules return one of two outcomes:

* ALLOW_AUTOMATION
* ESCALATE_TO_HUMAN

No partial states.
No explanations.
No user-facing text.

---

## Escalation Triggers

### Rule 1: Low Intent Confidence

If any detected intent has confidence below the safe threshold:

```
confidence < 0.60
```

→ Escalate

Reason:
Low confidence increases the risk of misunderstanding the user's intent.

---

### Rule 2: Conflicting or High-Risk Intent Combinations

If the query involves multiple intents whose combination implies dispute, denial, or policy enforcement, escalate.

Examples:

* refund_query + account_termination
* billing_query + policy_violation
* access_request + security_policy_query

Reason:
These scenarios often require judgment, exception handling, or legal review.

---

### Rule 3: Security-Sensitive Domains

If the query involves intents related to:

* security policies
* account access removal
* incident response
* data access restrictions

→ Escalate

Reason:
Security-related queries carry higher risk and should not be fully automated.

---

### Rule 4: Ambiguous Ownership Scope

If routing results in multiple owners (e.g., finance + security + ops) for a single query:

→ Escalate

Reason:
Cross-domain responses increase the chance of incorrect or misleading answers.

---

## Explicit Non-Triggers

Escalation rules do NOT trigger on:

* Simple FAQs
* Single-intent queries with high confidence
* Clear policy explanations
* Standard procedural questions

Escalation is not a fallback for weak answers.
It is a guardrail for risk.

---

## Relationship to Other Rules

* Constraint rules clean the input context
* Escalation rules assess response risk
* Refusal rules decide if the system must decline entirely

Escalation does not override refusal.
Refusal always has final authority.

---

## Design Principles

* Conservative by default
* Deterministic and auditable
* No LLM reasoning
* No hidden heuristics
* Easy to extend with new triggers

Escalation rules protect the system from answering when being wrong is costly, not when the answer is unknown.

