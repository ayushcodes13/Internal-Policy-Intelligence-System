import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const RAW_DOCS_DIR = path.join(ROOT, "data", "raw_docs");
const OUT_PATH = path.join(ROOT, "data", "search-index.json");
const MODEL = process.env.GEMINI_EMBEDDING_MODEL || "gemini-embedding-001";

function walkMarkdownFiles(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const files = [];

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...walkMarkdownFiles(fullPath));
    } else if (entry.isFile() && entry.name.endsWith(".md")) {
      files.push(fullPath);
    }
  }

  return files.sort();
}

function extractMetadata(content) {
  const metadata = {};

  for (const line of content.split(/\r?\n/)) {
    if (!line.includes(":")) {
      break;
    }

    const [key, ...valueParts] = line.split(":");
    metadata[key.trim()] = valueParts
      .join(":")
      .replace(/<.*?>/g, "")
      .trim();
  }

  return metadata;
}

function stripMetadataBlock(content) {
  const lines = content.split(/\r?\n/);
  let bodyStart = 0;

  for (let i = 0; i < lines.length; i += 1) {
    if (!lines[i].includes(":")) {
      bodyStart = i;
      break;
    }
  }

  return lines.slice(bodyStart).join("\n").trim();
}

function chunkText(text, chunkSize = 500, overlap = 100) {
  const chunks = [];
  let start = 0;

  while (start < text.length) {
    const end = start + chunkSize;
    chunks.push(text.slice(start, end));
    start = Math.max(0, end - overlap);
  }

  return chunks;
}

function baseKey(filePath) {
  return path.basename(filePath).split("_v")[0];
}

function normalize(vector) {
  const magnitude = Math.sqrt(vector.reduce((sum, value) => sum + value * value, 0));
  if (!magnitude) {
    throw new Error("Embedding provider returned a zero-length vector.");
  }
  return vector.map((value) => value / magnitude);
}

async function embedDocument(text) {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    throw new Error("GEMINI_API_KEY is required to build data/search-index.json.");
  }

  const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:embedContent?key=${apiKey}`;
  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: `models/${MODEL}`,
      content: {
        parts: [{ text }]
      },
      taskType: "RETRIEVAL_DOCUMENT"
    })
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`Gemini embedding failed: ${response.status} ${body}`);
  }

  const data = await response.json();
  const values = data?.embedding?.values;
  if (!Array.isArray(values)) {
    throw new Error("Gemini embedding response did not include embedding.values.");
  }

  return normalize(values.map(Number));
}

function loadChunks() {
  const docs = walkMarkdownFiles(RAW_DOCS_DIR).map((filePath) => {
    const content = fs.readFileSync(filePath, "utf8");
    const relPath = path.relative(ROOT, filePath).split(path.sep).join("/");
    return {
      text: stripMetadataBlock(content),
      metadata: {
        ...extractMetadata(content),
        path: relPath
      }
    };
  });

  const rawChunks = docs.flatMap((doc) =>
    chunkText(doc.text).map((text, chunkIndex) => ({
      chunk_id: `${doc.metadata.path}::chunk_${chunkIndex}`,
      text,
      metadata: {
        ...doc.metadata,
        chunk_index: chunkIndex
      }
    }))
  );

  const groups = new Map();
  for (const chunk of rawChunks) {
    const key = baseKey(chunk.metadata.path);
    groups.set(key, [...(groups.get(key) || []), chunk]);
  }

  return rawChunks.map((chunk) => {
    const group = groups.get(baseKey(chunk.metadata.path)) || [chunk];
    const newestDate = group
      .map((item) => item.metadata.last_updated || "")
      .sort()
      .at(-1);

    return {
      ...chunk,
      metadata: {
        ...chunk.metadata,
        version_group: baseKey(chunk.metadata.path),
        is_latest: (chunk.metadata.last_updated || "") === newestDate
      }
    };
  });
}

async function main() {
  const chunks = loadChunks();
  const embedded = [];

  for (let i = 0; i < chunks.length; i += 1) {
    const chunk = chunks[i];
    process.stdout.write(`Embedding ${i + 1}/${chunks.length}: ${chunk.chunk_id}\n`);
    embedded.push({
      ...chunk,
      embedding: await embedDocument(chunk.text)
    });
  }

  fs.writeFileSync(
    OUT_PATH,
    JSON.stringify(
      {
        model: MODEL,
        generated_at: new Date().toISOString(),
        chunks: embedded
      },
      null,
      2
    )
  );

  process.stdout.write(`Wrote ${embedded.length} embedded chunks to ${OUT_PATH}\n`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
