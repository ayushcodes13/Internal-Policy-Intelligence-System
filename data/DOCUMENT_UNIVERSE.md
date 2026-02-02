# Document Universe

This project simulates the internal knowledge base of a mid-sized B2B SaaS company with a customer support and operations team.

The system is designed to answer internal operational and policy-related questions using these documents, while handling ambiguity, conflicts, and outdated information safely.

---

## Document Types

The document universe consists of four types, each with a defined authority level.

### 1. Policies (High Authority)
Authoritative documents that define company rules and constraints.

Examples:
- Billing and Refund Policy
- Security Policy
- Data Access Policy
- Incident Response Policy
- Account Termination Policy

Policies are considered the source of truth.

---

### 2. SOPs (Medium Authority)
Operational documents describing how teams execute processes.

Examples:
- Customer Support SOP
- Refund Handling SOP
- Escalation Process SOP
- Incident Handling SOP

SOPs may reference policies but must not override them.

---

### 3. FAQs (Low Authority)
Interpretive documents intended to help support agents answer common questions.

Examples:
- Support FAQ
- Billing FAQ
- Security FAQ

FAQs may simplify or paraphrase policies and can be incomplete or misleading.

---

### 4. Notes / Memos (Very Low Authority)
Informal internal documents with no guaranteed correctness.

Examples:
- Ops notes
- Internal memos
- Draft guidelines

These documents may contain vague language, undocumented exceptions, or outdated practices.

---

## Authority Hierarchy

When conflicts occur, documents are evaluated using the following authority order:

1. Policy  
2. SOP  
3. FAQ  
4. Notes / Memos  

Conflicts between documents at the same authority level (e.g., two policies) are treated as unresolved and trigger refusal.

---

## Metadata Fields

Documents may include the following metadata:

- `source_type` (policy | sop | faq | note)
- `owner` (finance | support | security | ops)
- `last_updated` (YYYY-MM)

Some documents intentionally have missing or outdated metadata to reflect real-world conditions.

---

## Known Data Issues (Intentional)

The document universe intentionally includes:

- Outdated policy versions
- Conflicting rules across documents
- Vague or informal guidance in notes
- FAQs that partially contradict policies

These issues are included to test retrieval quality, ranking logic, and refusal behavior.

---

## System Assumptions

- The system must not infer or guess beyond documented evidence.
- Answers must be grounded in authoritative documents.
- When evidence is insufficient, conflicting, or outdated, the system must refuse to answer.

This document defines the boundaries of what the system is allowed to trust.
