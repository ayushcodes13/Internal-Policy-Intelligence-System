export type IntentName =
  | "access_request"
  | "account_closure"
  | "refund_query"
  | "billing_query"
  | "security_policy_query"
  | "support_process_query";

export type GovernanceVerdict =
  | "SAFE"
  | "REFUSE_POLICY"
  | "REFUSE_INVALID"
  | "ESCALATE";

export type ChunkMetadata = {
  source_type?: string;
  owner?: string;
  last_updated?: string;
  path: string;
  version_group?: string;
  is_latest?: boolean;
  chunk_index?: number;
};

export type SearchChunk = {
  chunk_id: string;
  text: string;
  metadata: ChunkMetadata;
  embedding: number[];
};

export type RetrievedChunk = SearchChunk & {
  score: number;
};

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
