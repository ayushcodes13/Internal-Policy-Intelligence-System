""" Job: Split documents into searchable chunks.

Why this exists:
	•	LLMs can't search whole documents well
	•	Small chunks improve relevance
	•	Metadata sticks to each chunk

Example:

account_closure_policy.md
→ 12 chunks
→ each chunk has:
    - text
    - source_type
    - owner
    - last_updated
"""

from typing import List, Dict

def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100
) -> List[str]:
    """
    Splits text into overlapping chunks.

    Args:
        text (str): Full document text
        chunk_size (int): Max size of each chunk
        overlap (int): Overlap between chunks

    Returns:
        List[str]: List of text chunks
    """

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        # move start forward, keeping overlap
        start = end - overlap

        if start < 0:
            start = 0

    return chunks


def chunk_documents(
    documents: List[Dict],
    chunk_size: int = 500,
    overlap: int = 100
) -> List[Dict]:
    """
    Chunks a list of loaded documents.

    Args:
        documents (List[Dict]): Output of loaders.py
        chunk_size (int): Chunk size
        overlap (int): Overlap size

    Returns:
        List[Dict]: Chunked documents with metadata
    """

    chunked_docs = []

    for doc in documents:
        text = doc["content"]
        metadata = doc["metadata"]
        path = metadata.get("path", "unknown")

        chunks = chunk_text(text, chunk_size, overlap)

        for idx, chunk in enumerate(chunks):
            chunked_docs.append({
                "chunk_id": f"{path}::chunk_{idx}",
                "text": chunk,
                "metadata": {
                    **metadata,
                    "chunk_index": idx
                }
            })

    return chunked_docs