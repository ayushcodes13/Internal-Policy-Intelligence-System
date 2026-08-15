const GEMINI_EMBED_MODEL =
  process.env.GEMINI_EMBEDDING_MODEL || "gemini-embedding-001";

type GeminiTaskType = "RETRIEVAL_QUERY" | "RETRIEVAL_DOCUMENT";

export async function embedText(
  text: string,
  taskType: GeminiTaskType
): Promise<number[]> {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    throw new Error("GEMINI_API_KEY is not configured.");
  }

  const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_EMBED_MODEL}:embedContent?key=${apiKey}`;

  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: `models/${GEMINI_EMBED_MODEL}`,
      content: {
        parts: [{ text }]
      },
      taskType
    })
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Gemini embedding request failed: ${response.status} ${body}`);
  }

  const data = await response.json();
  const values = data?.embedding?.values;
  if (!Array.isArray(values)) {
    throw new Error("Gemini embedding response did not include embedding.values.");
  }

  const vector = values.map(Number);
  const magnitude = Math.sqrt(vector.reduce((sum, value) => sum + value * value, 0));

  if (!magnitude) {
    throw new Error("Gemini returned a zero-length embedding.");
  }

  return vector.map((value) => value / magnitude);
}
