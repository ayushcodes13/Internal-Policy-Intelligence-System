import fs from "node:fs";
import path from "node:path";
import type { RetrievedChunk, SearchChunk } from "./types";
import { embedText } from "./gemini";

const INDEX_PATH = path.join(process.cwd(), "data", "search-index.json");

let cachedIndex: SearchChunk[] | null = null;

function loadIndex(): SearchChunk[] {
  if (cachedIndex) {
    return cachedIndex;
  }

  if (!fs.existsSync(INDEX_PATH)) {
    throw new Error(
      "data/search-index.json is missing. Run `npm run build:index` with GEMINI_API_KEY before deploying."
    );
  }

  const parsed = JSON.parse(fs.readFileSync(INDEX_PATH, "utf8")) as {
    chunks: SearchChunk[];
  };

  cachedIndex = parsed.chunks;
  return cachedIndex;
}

function dotProduct(a: number[], b: number[]): number {
  const len = Math.min(a.length, b.length);
  let score = 0;
  for (let i = 0; i < len; i += 1) {
    score += a[i] * b[i];
  }
  return score;
}

export async function retrieveChunks(
  userQuery: string,
  allowedOwners: string[],
  topK = 5
): Promise<RetrievedChunk[]> {
  if (allowedOwners.length === 0) {
    return [];
  }

  const chunks = loadIndex();
  const queryEmbedding = await embedText(userQuery, "RETRIEVAL_QUERY");

  const candidates = chunks
    .filter((chunk) => allowedOwners.includes(chunk.metadata.owner || ""))
    .filter((chunk) => chunk.metadata.is_latest !== false)
    .map((chunk) => ({
      ...chunk,
      score: dotProduct(queryEmbedding, chunk.embedding)
    }))
    .sort((a, b) => b.score - a.score);

  const minSimilarityScore = 0.25;
  if (candidates.length > 0 && candidates[0].score < minSimilarityScore) {
    return [];
  }

  return candidates.slice(0, topK);
}

export function getAvailableDocuments(): Array<{ path: string; text: string }> {
  return loadIndex().reduce<Array<{ path: string; text: string }>>((docs, chunk) => {
    if (chunk.metadata.chunk_index === 0) {
      docs.push({ path: chunk.metadata.path, text: chunk.text });
    }
    return docs;
  }, []);
}
