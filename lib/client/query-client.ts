import type { PipelineResult } from "../types";

export async function runPolicyQuery(query: string): Promise<PipelineResult> {
  const response = await fetch("/api/query", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ query })
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data?.error || "Request failed.");
  }

  return data as PipelineResult;
}
