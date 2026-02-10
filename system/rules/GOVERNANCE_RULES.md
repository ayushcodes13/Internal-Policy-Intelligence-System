# Governance Rules

## Purpose

Governance rules decide **how to interpret allowed documents**.

They operate only after constraint rules have finished.

Governance is where **policy authority and precedence** live.

---

## Core Question

“Given the allowed documents, how should they be applied or explained?”

This is about **meaning**, not access.

---

## What Governance Rules Do

Governance rules may:
- resolve conflicts between documents
- prefer newer policies over older ones
- enforce policy hierarchy
- determine authoritative sources
- explain outcomes to the user

Governance rules **do not delete documents blindly**.
They decide **which ones dominate**.

---

## What Governance Rules Do NOT Do

Governance rules do NOT:
- handle forbidden access
- remove internal notes (already done earlier)
- escalate to humans
- refuse to answer on safety grounds

They assume the context is already clean.

---

## Examples

### Example 1: Policy Supersession

Allowed context:
- refund_policy_v1 (2022)
- refund_policy_v2 (2023)

Governance decision:
- v2 supersedes v1

User explanation:
“Refunds are not allowed after termination due to policy violations, per the current refund policy.”

---

### Example 2: Conflicting Statements

Allowed context:
- SLA says 24h response
- FAQ says 48h response

Governance decision:
- SLA is authoritative
- FAQ is explanatory only

---

## Output

Governance rules produce:
- an interpreted context
- a structured decision basis
- explanations usable by generation

They **do not stop the system**.

---

## Design Principle

Governance rules are:
- semantic
- explicit
- explainable
- traceable

This is where **correctness beats convenience**.