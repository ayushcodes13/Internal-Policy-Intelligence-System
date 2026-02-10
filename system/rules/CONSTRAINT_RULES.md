# Constraint Rules

## Purpose

Constraint rules decide **whether a retrieved chunk is allowed to be used at all**.

They operate on **document properties**, not meaning.

They are purely defensive.

---

## Core Question

“Is there anything in the retrieved context that must NOT be used?”

This is about **documents**, not users.

---

## What Constraint Rules Do

Constraint rules:
- remove forbidden document types
- enforce visibility boundaries
- enforce ownership boundaries
- enforce explicit allow/deny flags

They **delete chunks** that should never reach reasoning.

---

## What Constraint Rules Do NOT Do

Constraint rules do NOT:
- interpret policy meaning
- resolve policy conflicts
- decide which policy is correct
- explain outcomes
- stop the system
- escalate to humans
- refuse to answer

If a human needs to *think*, it is not a constraint.

---

## Examples

### Example 1: Internal Leakage

Retrieved:
- refund_policy_v2 (policy, finance)
- refund_policy_v1 (policy, finance)
- internal_refund_exceptions_memo (notes)

Constraint action:
- remove `notes`

Output:
- refund_policy_v2
- refund_policy_v1

---

### Example 2: Owner Mismatch

User intent:
- security_policy_query

Retrieved:
- security_policy (security)
- billing_policy (finance)

Constraint action:
- remove non-security documents

Output:
- security_policy

---

## Output

Constraint rules return:
- a **cleaned list of chunks**

They never:
- halt execution
- raise decisions
- generate explanations

They only clean the context.

---

## Design Principle

Constraint rules are:
- strict
- boring
- deterministic
- meaning-blind

They exist to **prevent damage**, not to make decisions.