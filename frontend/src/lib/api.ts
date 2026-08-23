import type { PipelineResult } from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

export async function fetchPolicyQuery(query: string): Promise<PipelineResult> {
  const response = await fetch(`${API_BASE_URL}/api/query`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ query })
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => null);
    throw new Error(errorBody?.detail || `Request failed with ${response.status}`);
  }

  return response.json();
}
