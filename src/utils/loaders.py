"""
Job:
Boring but critical glue.

Handles:
	•	reading markdown files
	•	extracting metadata headers
	•	loading documents consistently

Why this matters:
	•	keeps ingestion clean
	•	avoids copy-paste logic
	•	reduces silent bugs
"""
from pathlib import Path
from typing import List, Dict


def load_markdown_files(base_path: str) -> List[Dict]:
    """
    Loads all .md files under a directory recursively.

    Returns:
        List of dicts:
        {
            "text": str,
            "metadata": {
                "source_type": str,
                "owner": str,
                "last_updated": str,
                "path": str
            }
        }
    """
    documents = []
    base = Path(base_path)

    for file_path in base.rglob("*.md"):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        metadata = extract_metadata(content)
        metadata["path"] = str(file_path)

        documents.append(
            {
                "text": strip_metadata_block(content),
                "metadata": metadata,
            }
        )

    return documents


import re

def extract_metadata(content: str) -> Dict:
    """
    Extracts metadata from the top of the markdown file
    and cleans HTML artifacts.
    """
    metadata = {}

    for line in content.splitlines():
        if ":" not in line:
            break

        key, value = line.split(":", 1)

        clean_value = value.strip()
        clean_value = re.sub(r"<.*?>", "", clean_value)  # remove HTML tags
        clean_value = clean_value.strip()

        metadata[key.strip()] = clean_value

    return metadata


def strip_metadata_block(content: str) -> str:
    """
    Removes metadata header from markdown content.
    """
    lines = content.splitlines()
    body_start = 0

    for i, line in enumerate(lines):
        if ":" not in line:
            body_start = i
            break

    return "\n".join(lines[body_start:]).strip()


if __name__ == "__main__":
    docs = load_markdown_files("data/raw_docs")

    print(f"Loaded {len(docs)} documents\n")

    for d in docs[:2]:
        print(d["metadata"])
        print(d["text"][:200])
        print("-" * 40)