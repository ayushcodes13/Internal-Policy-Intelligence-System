export const productConfig = {
  name: "PolicyLens",
  tagline: "The policy intelligence layer built for decisions that need proof.",
  description:
    "PolicyLens routes internal policy questions through owner scoping, governed retrieval, source-backed generation, and grounding review before it answers.",
  domains: ["Finance", "Operations", "Security", "Support"],
  navItems: ["Product", "Workflow", "Architecture", "Docs"],
  heroChips: ["Analyze refund policy", "Check access rules", "Escalate security incidents"],
  sampleQueries: [
    "How do I request a refund?",
    "Can support override the refund deadline?",
    "My account was hacked and I see unauthorized access.",
    "What is the account closure process?"
  ],
  stats: [
    { label: "Verdict modes", value: "4" },
    { label: "Policy domains", value: "4" },
    { label: "Runtime model downloads", value: "0" }
  ],
  features: [
    {
      title: "Owner-scoped retrieval",
      body:
        "Queries are routed to the right policy owner before retrieval, limiting Finance, Security, Support, and Operations context leakage."
    },
    {
      title: "Governance before generation",
      body:
        "The system chooses between safe answer, refusal, invalid request, and escalation before final response generation."
    },
    {
      title: "Evidence-first output",
      body:
        "Every useful answer returns cited source paths, supporting clauses, confidence, and a lightweight grounding signal."
    }
  ]
};
