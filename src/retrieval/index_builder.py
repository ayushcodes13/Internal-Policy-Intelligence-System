"""
Index Builder

One-time ingestion pipeline.

Steps:
1. Load raw documents
2. Chunk documents
3. Add version metadata (version_group, is_latest)
4. Embed chunks
5. Build FAISS flat index
6. Save index + metadata store

Run:
python -m src.retrieval.index_builder
"""

import os
import pickle
from collections import defaultdict
from typing import Dict, List

import faiss
import numpy as np

from src.utils.loaders import load_markdown_files
from src.retrieval.chunker import chunk_documents
from src.retrieval.embedder import embed_chunks


INDEX_DIR = "data/index"
INDEX_PATH = os.path.join(INDEX_DIR, "faiss.index")
METADATA_PATH = os.path.join(INDEX_DIR, "metadata.pkl")


def _base_key(path: str) -> str:
    filename = path.split("/")[-1]
    return filename.split("_v")[0]


def _apply_version_metadata(chunks: List[Dict]) -> List[Dict]:
    grouped = defaultdict(list)

    for chunk in chunks:
        path = chunk["metadata"].get("path", "")
        key = _base_key(path)
        grouped[key].append(chunk)

    enriched_chunks = []

    for key, group in grouped.items():
        sorted_group = sorted(
            group,
            key=lambda c: c["metadata"].get("last_updated", ""),
            reverse=True,
        )

        newest_date = sorted_group[0]["metadata"].get("last_updated")

        for chunk in sorted_group:
            chunk["metadata"]["version_group"] = key
            chunk["metadata"]["is_latest"] = (
                chunk["metadata"].get("last_updated") == newest_date
            )
            enriched_chunks.append(chunk)

    return enriched_chunks


def build_index():

    if os.path.exists(INDEX_PATH):
        print("Index already exists. Skipping build.")
        return

    print("Loading documents...")
    docs = load_markdown_files(base_path="data/raw_docs")

    print("Chunking documents...")
    chunks = chunk_documents(docs)

    print("Applying version metadata...")
    chunks = _apply_version_metadata(chunks)

    print("Embedding chunks...")
    embedded_chunks = embed_chunks(chunks)

    # -------------------------
    # SAFETY: Empty embedding check
    # -------------------------
    if not embedded_chunks:
        raise RuntimeError("No chunks were embedded. Cannot build index.")

    print("Building FAISS index...")

    dimension = len(embedded_chunks[0]["embedding"])
    index = faiss.IndexFlatIP(dimension)

    vectors = []
    metadata_store = {}

    # -------------------------
    # DUPLICATE DETECTION
    # -------------------------
    seen_texts = set()
    seen_doc_text_pairs = set()

    for idx, chunk in enumerate(embedded_chunks):

        text = chunk["text"]
        path = chunk["metadata"].get("path", "")

        # Exact global duplicate text check
        if text in seen_texts:
            raise RuntimeError(f"Duplicate chunk text detected in {path}")
        seen_texts.add(text)

        # Duplicate within same document
        key = (path, text)
        if key in seen_doc_text_pairs:
            raise RuntimeError(f"Duplicate chunk detected in {path}")
        seen_doc_text_pairs.add(key)

        vector = np.array(chunk["embedding"]).astype("float32")

        # -------------------------
        # Embedding dimension validation
        # -------------------------
        if len(vector) != dimension:
            raise RuntimeError(
                f"Inconsistent embedding dimension detected in {path}. "
                f"Expected {dimension}, got {len(vector)}"
            )

        # normalize for cosine similarity
        faiss.normalize_L2(vector.reshape(1, -1))

        vectors.append(vector)

        metadata_store[idx] = {
            "text": chunk["text"],
            "metadata": chunk["metadata"],
        }

    vectors_np = np.vstack(vectors).astype("float32")
    index.add(vectors_np)

    os.makedirs(INDEX_DIR, exist_ok=True)

    faiss.write_index(index, INDEX_PATH)

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata_store, f)

    print(f"Indexed {len(embedded_chunks)} chunks successfully.")


if __name__ == "__main__":
    build_index()