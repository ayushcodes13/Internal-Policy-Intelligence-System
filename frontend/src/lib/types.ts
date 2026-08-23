export type GovernanceVerdict =
  | "SAFE"
  | "REFUSE_POLICY"
  | "REFUSE_INVALID"
  | "ESCALATE";

export type PipelineResult = {
  status: "SAFE" | "REFUSED" | "ESCALATED";
  verdict: GovernanceVerdict;
  answer: string | null;
  message: string | null;
  sources: string[];
  supporting_clauses: string[];
  confidence: "high" | "medium" | "low";
  context_used: number;
  hallucination_detected?: boolean;
  unsupported_clauses?: string[];
  total_latency_ms?: number;
};
