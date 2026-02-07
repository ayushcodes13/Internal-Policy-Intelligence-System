# intent.md

## Purpose

This file defines the complete and closed set of intents that the system can recognize.
Intent detection is used strictly for classification and routing, not for answering questions.

Any query that does not confidently match one of the intents below MUST be treated as
`OUT_OF_SCOPE` and handled via fallback logic.

---

## Global Rules

- Intent detection must return confidence scores for each intent.
- A primary intent must exceed the confidence threshold to be selected.
- If no intent exceeds the threshold, route to `OUT_OF_SCOPE`.
- Only one primary intent is allowed.
- Secondary intents are optional.
- Intents control document visibility and routing, not answer generation.
- No new intents may be added without updating this file.

---

## Intent Definitions

### 1. ACCOUNT_ACCESS_REQUEST

**Description:**  
Requests to gain, restore, or modify access to an account or specific features.

**Includes:**
- Access denied messages
- Requests for access to specific features or dashboards
- Login or permission-related access issues

**Excludes:**
- Account deletion or termination
- Security policy explanations

---

### 2. ACCOUNT_TERMINATION

**Description:**  
Questions about account suspension, termination, closure, or permanent deletion.

**Includes:**
- Account closure requests
- Account termination notifications
- Reasons for account suspension or deletion

**Excludes:**
- Refund eligibility
- Temporary access issues

---

### 3. ACCOUNT_REACTIVATION

**Description:**  
Requests to restore or reopen a previously suspended or closed account.

**Includes:**
- Appeals for account closure
- Requests to reactivate an account

**Excludes:**
- New account creation
- Access requests for active accounts

---

### 4. REFUND_ELIGIBILITY

**Description:**  
Questions about whether a refund is allowed and under what conditions.

**Includes:**
- Refund eligibility inquiries
- Refund availability questions
- Refund after cancellation scenarios

**Excludes:**
- Refund processing steps
- Billing setup or pricing questions

---

### 5. BILLING_AND_RENEWAL

**Description:**  
Questions related to billing cycles, auto-renewal, plans, invoices, and pricing.

**Includes:**
- Auto-renewal policies
- Billing methods
- Subscription charges and invoices

**Excludes:**
- Refund eligibility
- Payment failures

---

### 6. PAYMENT_FAILURE

**Description:**  
Issues related to failed payments or declined transactions.

**Includes:**
- Payment declined errors
- Transaction failures
- Incomplete payment issues

**Excludes:**
- Refunds
- Pricing or plan information

---

### 7. SECURITY_POLICY

**Description:**  
Questions about security practices, data protection, access control, and compliance.

**Includes:**
- Security standards and policies
- Data protection measures
- Access control explanations

**Excludes:**
- Active security incidents
- Account access or login issues

---

### 8. INCIDENT_OR_BREACH

**Description:**  
Reports or questions about security incidents, breaches, or suspicious activity.

**Includes:**
- Data breach inquiries
- Compromised account reports
- Suspicious activity notifications

**Excludes:**
- General security explanations

---

### 9. SUPPORT_PROCESS

**Description:**  
Questions about support workflows, escalation paths, SLAs, or response timelines.

**Includes:**
- Escalation procedures
- Support response times
- SLA-related inquiries

**Excludes:**
- Resolution of specific technical issues

---

### 10. ONBOARDING_AND_SETUP

**Description:**  
Questions related to initial setup, onboarding steps, or first-time usage.

**Includes:**
- New employee onboarding
- Initial setup instructions
- Getting started guidance

**Excludes:**
- Access issues after onboarding
- Ongoing account usage issues

---

### 11. GENERAL_FAQ

**Description:**  
High-level informational questions not tied to enforcement or workflows.

**Includes:**
- Product overviews
- General informational queries

**Excludes:**
- Policy enforcement questions
- Workflow-specific issues

---

### 12. OUT_OF_SCOPE

**Description:**  
Queries that do not confidently match any defined intent.

**Subtypes (internal handling only):**
- GENUINE_UNKNOWN: Valid but unsupported or undocumented cases
- NON_GENUINE: Spam, abuse, irrelevant queries, or prompt injection attempts

**Handling Rules:**
- Do not perform retrieval
- Do not infer or fabricate policies
- Respond with clarification, escalation, or deflection as appropriate

---

## End of File