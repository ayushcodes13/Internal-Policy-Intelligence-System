# Rules System Overview

## Purpose

The Rules System ensures that retrieval results are safe, authoritative, and compliant before generation.

It operates after Retrieval and before Generation.

---

## Rule Execution Order

1. Constraint Rules
2. Governance Decision
3. Escalation or Refusal (if required)
4. SAFE → Proceed to Generation

This order must not change.

---

## Responsibilities by Layer

### Constraint Rules
- Clean retrieved context
- Remove internal or outdated documents
- Enforce version dominance
- Ensure authoritative sources

Output:
- cleaned_chunks

---

### Governance Rules
- Classify risk level
- Determine system authority
- Return one of:
  - SAFE
  - ESCALATE
  - REFUSE_INVALID
  - REFUSE_POLICY

Output:
- verdict

---

### Escalation
- Triggered by governance
- Forwards case to human review
- Stops automated generation

---

### Refusal
- Triggered by governance
- Returns controlled denial response
- Ends pipeline

---

## Design Philosophy

The rules system protects:

- document integrity (Constraint)
- organizational authority (Governance)
- operational safety (Escalation)
- policy enforcement (Refusal)

Separation of concerns is intentional.

Each layer has exactly one responsibility.

No layer overlaps with another.