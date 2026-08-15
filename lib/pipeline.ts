import { groqJson } from "./groq";
import { retrieveChunks } from "./retrieval";
import type {
  GovernanceVerdict,
  IntentName,
  PipelineResult,
  RetrievedChunk
} from "./types";

const allowedIntents = new Set<IntentName>([
  "access_request",
  "account_closure",
  "refund_query",
  "billing_query",
  "security_policy_query",
  "support_process_query"
]);

const intentToOwners: Record<IntentName, string[]> = {
  access_request: ["ops", "security"],
  account_closure: ["ops"],
  refund_query: ["finance"],
  billing_query: ["finance"],
  security_policy_query: ["security"],
  support_process_query: ["ops"]
};

type IntentResponse = {
  intents?: Array<{ name?: string; confidence?: number }>;
};

type GovernanceSignals = {
  is_invalid?: boolean;
  is_escalation?: boolean;
  is_policy_denial?: boolean;
  is_action_request?: boolean;
  confidence?: string;
};

type GeneratedAnswer = {
  answer?: string | null;
  sources?: string[];
  supporting_clauses?: string[];
  confidence?: "high" | "medium" | "low";
};

type GeneratedDenial = {
  message?: string;
  supporting_clauses?: string[];
  confidence?: "high" | "medium" | "low";
};

async function detectIntent(userText: string): Promise<IntentName[]> {
  const response = await groqJson<IntentResponse>([
    {
      role: "system",
      content: `You are an intent classifier.

You MUST choose only from these intent labels:
${JSON.stringify(Array.from(allowedIntents))}

Return STRICT JSON in this exact format:
{
  "intents": [
    {
      "name": string,
      "confidence": number
    }
  ]
}

Rules:
- Multiple intents are allowed.
- If unsure, return an empty intents array.
- Do not add extra fields.`
    },
    { role: "user", content: userText }
  ]);

  return (response.intents || [])
    .filter(
      (intent): intent is { name: IntentName; confidence: number } =>
        typeof intent.name === "string" &&
        allowedIntents.has(intent.name as IntentName) &&
        typeof intent.confidence === "number" &&
        intent.confidence >= 0.5
    )
    .map((intent) => intent.name);
}

function routeIntent(intents: IntentName[]): string[] {
  return Array.from(
    new Set(intents.flatMap((intent) => intentToOwners[intent] || []))
  );
}

function applyConstraints(
  retrievedChunks: RetrievedChunk[],
  allowedOwners: string[]
): RetrievedChunk[] {
  const seen = new Set<string>();

  return retrievedChunks
    .filter((chunk) => chunk.metadata.source_type !== "notes")
    .filter((chunk) => allowedOwners.includes(chunk.metadata.owner || ""))
    .filter((chunk) => {
      if (!chunk.chunk_id) {
        return true;
      }
      if (seen.has(chunk.chunk_id)) {
        return false;
      }
      seen.add(chunk.chunk_id);
      return true;
    });
}

async function evaluateGovernance(
  userQuery: string,
  cleanedChunks: RetrievedChunk[]
): Promise<GovernanceVerdict> {
  const signals = await groqJson<GovernanceSignals>([
    {
      role: "system",
      content: `You are a governance classifier.

You must return STRICT JSON with this exact structure:
{
  "is_invalid": boolean,
  "is_escalation": boolean,
  "is_policy_denial": boolean,
  "is_action_request": boolean,
  "confidence": string
}

Rules:
- is_invalid = true if query is nonsense, malicious, or unrelated to system domain.
- is_escalation = true ONLY if the user explicitly reports hacked account, unauthorized access, legal action, or financial fraud.
- Do not mark escalation for requests, complaints, refund demands, policy discussions, or asking how to escalate.
- is_policy_denial = true if the user is requesting something explicitly not allowed by policy.
- is_action_request = true if the user is asking the system to perform an action.
- Do not mark informational questions as action requests.
- Do not add extra fields.`
    },
    { role: "user", content: userQuery }
  ]);

  let verdict: GovernanceVerdict = "SAFE";
  if (signals.is_invalid) {
    verdict = "REFUSE_INVALID";
  } else if (signals.is_policy_denial) {
    verdict = "REFUSE_POLICY";
  } else if (signals.is_escalation && signals.confidence !== "low") {
    verdict = "ESCALATE";
  }

  if (verdict === "SAFE" && cleanedChunks.length === 0) {
    return "REFUSE_INVALID";
  }

  return verdict;
}

function contextFromChunks(chunks: RetrievedChunk[]): string {
  return chunks
    .slice(0, 5)
    .map((chunk) => `Document: ${chunk.metadata.path}\n${chunk.text}`)
    .join("\n\n---\n\n");
}

async function generateAnswer(
  userQuery: string,
  cleanedChunks: RetrievedChunk[]
): Promise<Omit<PipelineResult, "verdict" | "total_latency_ms">> {
  if (cleanedChunks.length === 0) {
    return {
      status: "SAFE",
      answer: null,
      message: null,
      sources: [],
      supporting_clauses: [],
      confidence: "low",
      context_used: 0
    };
  }

  const topChunks = cleanedChunks.slice(0, 5);
  const validPaths = new Set(topChunks.map((chunk) => chunk.metadata.path));
  const parsed = await groqJson<GeneratedAnswer>([
    {
      role: "system",
      content: `You are a strict internal policy assistant.

Return STRICT JSON:
{
  "answer": string | null,
  "sources": [string],
  "supporting_clauses": [string],
  "confidence": "high" | "medium" | "low"
}

Rules:
- Use only the provided context.
- Every source must match a document path exactly.
- Supporting clauses must be exact quotes.
- If unsupported, return null answer and low confidence.
- No extra fields.`
    },
    {
      role: "user",
      content: `User Question:
${userQuery}

Context:
${contextFromChunks(topChunks)}`
    }
  ]);

  return {
    status: "SAFE",
    answer: parsed.answer ?? null,
    message: null,
    sources: (parsed.sources || []).filter((source) => validPaths.has(source)),
    supporting_clauses: parsed.supporting_clauses || [],
    confidence: parsed.confidence || "low",
    context_used: topChunks.length
  };
}

async function generatePolicyDenial(
  userQuery: string,
  cleanedChunks: RetrievedChunk[]
): Promise<Omit<PipelineResult, "verdict" | "total_latency_ms">> {
  if (cleanedChunks.length === 0) {
    return {
      status: "REFUSED",
      answer: null,
      message: "This request cannot be fulfilled due to existing policy restrictions.",
      sources: [],
      supporting_clauses: [],
      confidence: "low",
      context_used: 0
    };
  }

  const topChunks = cleanedChunks.slice(0, 5);
  const parsed = await groqJson<GeneratedDenial>([
    {
      role: "system",
      content: `You are a strict policy enforcement assistant.

Return STRICT JSON:
{
  "message": string,
  "supporting_clauses": [string],
  "confidence": "high" | "medium" | "low"
}

Rules:
- Identify exact clauses enforcing denial.
- Quote clauses exactly.
- Base everything only on context.
- No extra fields.`
    },
    {
      role: "user",
      content: `User Question:
${userQuery}

Context:
${contextFromChunks(topChunks)}`
    }
  ]);

  return {
    status: "REFUSED",
    answer: null,
    message:
      parsed.message ||
      "This request cannot be fulfilled due to existing policy restrictions.",
    sources: Array.from(new Set(topChunks.map((chunk) => chunk.metadata.path))),
    supporting_clauses: parsed.supporting_clauses || [],
    confidence: parsed.confidence || "low",
    context_used: topChunks.length
  };
}

function checkGrounding(
  answer: string | null,
  cleanedChunks: RetrievedChunk[]
): { grounded: boolean; unsupported: string[] } {
  if (!answer || cleanedChunks.length === 0) {
    return { grounded: false, unsupported: ["No context available"] };
  }

  const retrievedText = cleanedChunks.map((chunk) => chunk.text).join(" ").toLowerCase();
  const sentences = answer
    .split(".")
    .map((sentence) => sentence.trim())
    .filter(Boolean);

  const unsupported = sentences.filter((sentence) => {
    const words = sentence
      .toLowerCase()
      .split(/\s+/)
      .map((word) => word.replace(/[^a-z0-9-]/g, ""))
      .filter((word) => word.length > 4);

    if (words.length === 0) {
      return false;
    }

    const matches = words.filter((word) => retrievedText.includes(word)).length;
    return matches / words.length < 0.4;
  });

  return { grounded: unsupported.length === 0, unsupported };
}

export async function runPipeline(userQuery: string): Promise<PipelineResult> {
  const start = Date.now();
  const intents = await detectIntent(userQuery);
  const allowedOwners = routeIntent(intents);
  const retrievedChunks = await retrieveChunks(userQuery, allowedOwners);
  const cleanedChunks = applyConstraints(retrievedChunks, allowedOwners);
  const verdict = await evaluateGovernance(userQuery, cleanedChunks);

  let result: Omit<PipelineResult, "verdict" | "total_latency_ms">;
  if (verdict === "REFUSE_INVALID") {
    result = {
      status: "REFUSED",
      answer: null,
      message: "I cannot assist with that request as it is not related to this system.",
      sources: [],
      supporting_clauses: [],
      confidence: "low",
      context_used: 0
    };
  } else if (verdict === "ESCALATE") {
    result = {
      status: "ESCALATED",
      answer: null,
      message: "This request requires human review and has been escalated.",
      sources: [],
      supporting_clauses: [],
      confidence: "low",
      context_used: cleanedChunks.length
    };
  } else if (verdict === "REFUSE_POLICY") {
    result = await generatePolicyDenial(userQuery, cleanedChunks);
  } else {
    result = await generateAnswer(userQuery, cleanedChunks);
  }

  const withVerdict: PipelineResult = {
    ...result,
    verdict,
    total_latency_ms: Date.now() - start
  };

  if (withVerdict.status === "SAFE" && withVerdict.answer) {
    const grounding = checkGrounding(withVerdict.answer, cleanedChunks);
    withVerdict.hallucination_detected = !grounding.grounded;
    withVerdict.unsupported_clauses = grounding.unsupported;
    if (!grounding.grounded) {
      withVerdict.confidence = "low";
    }
  }

  console.log(
    JSON.stringify({
      event: "QUERY_EXECUTION",
      data: {
        query: userQuery,
        intents,
        allowedOwners,
        retrievedCount: retrievedChunks.length,
        governanceVerdict: verdict,
        finalStatus: withVerdict.status,
        confidence: withVerdict.confidence,
        totalLatencyMs: withVerdict.total_latency_ms
      }
    })
  );

  return withVerdict;
}
