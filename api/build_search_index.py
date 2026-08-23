from __future__ import annotations

import json
import os
from pathlib import Path

from api.pipeline import ROOT, _embed_text, _load_env, _load_raw_chunks


def main() -> None:
    _load_env()
    if not os.getenv("GEMINI_API_KEY"):
        print("GEMINI_API_KEY is not configured; skipping data/search-index.json generation.")
        return

    chunks = []
    for chunk in _load_raw_chunks():
        chunks.append(
            {
                "chunk_id": chunk.chunk_id,
                "text": chunk.text,
                "metadata": chunk.metadata,
                "embedding": _embed_text(chunk.text, "RETRIEVAL_DOCUMENT"),
            }
        )

    output = ROOT / "data" / "search-index.json"
    output.write_text(json.dumps({"chunks": chunks}, indent=2), encoding="utf-8")
    print(f"Wrote {len(chunks)} chunks to {output}")


if __name__ == "__main__":
    main()
