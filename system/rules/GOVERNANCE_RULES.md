# Governance Rules

## Purpose

Governance rules decide what type of outcome the system should produce.

They operate only after constraint rules have cleaned the context.

Governance is about **authority and risk classification**, not document filtering.

---

## Core Question

“Given the cleaned context and the user query, are we allowed to answer this — and how?”

---

## Possible Outcomes

Governance must return exactly one of the following:

- SAFE
- ESCALATE
- REFUSE_INVALID
- REFUSE_POLICY

---

## Outcome Definitions

### SAFE

The system is allowed to generate a response using the cleaned context.

Conditions:
- Query is within supported domain
- No risk signals detected
- No policy violations implied
- No escalation triggers present

---

### ESCALATE

The query requires human review.

Conditions may include:
- fraud or abuse indicators
- legal threats or litigation references
- regulatory or compliance-sensitive matters
- unusual override requests
- high-risk operational impact

When triggered:
- The system must not generate a final answer
- The query and cleaned context are forwarded to human review

---

### REFUSE_INVALID

The query is outside the supported domain.

Examples:
- unrelated personal requests
- creative writing
- technical coding help unrelated to internal policies
- gibberish or malformed input

Response style:
- Short
- Neutral
- Domain-limited clarification

---

### REFUSE_POLICY

The query is valid and within domain, but the requested outcome violates policy.

Example:
User requests refund after termination due to policy violation.

The system must:
- Explain the policy
- Clearly state the restriction
- Provide reasoning
- Remain neutral and factual

This is not silence.
This is structured denial.

---

## Inputs

- user_query (str)
- cleaned_chunks (List[Dict])

---

## Outputs

One of:
- SAFE
- ESCALATE
- REFUSE_INVALID
- REFUSE_POLICY

No partial states.
No multiple flags.
Exactly one verdict.

---

## Design Principle

Governance protects the organization.

It ensures:
- Risk is managed
- Authority boundaries are respected
- AI does not overstep

It does not clean documents.
It does not interpret policy hierarchy.
It does not generate final answers.

It decides the system’s next action.