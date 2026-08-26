from __future__ import annotations

import json
import math
import os
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    def load_dotenv(*_args: Any, **_kwargs: Any) -> bool:
        return False


ROOT = Path(__file__).resolve().parents[1]
RAW_DOCS_DIR = ROOT / "data" / "raw_docs"
SEARCH_INDEX_PATH = ROOT / "data" / "search-index.json"

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GEMINI_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")

IntentName = Literal[
    "access_request",
    "account_closure",
    "refund_query",
    "billing_query",
    "security_policy_query",
    "support_process_query",
]

Verdict = Literal["SAFE", "REFUSE_POLICY", "REFUSE_INVALID", "ESCALATE"]

ALLOWED_INTENTS: set[str] = {
    "access_request",
    "account_closure",
    "refund_query",
    "billing_query",
    "security_policy_query",
    "support_process_query",
}

INTENT_TO_OWNERS: dict[str, list[str]] = {
    "access_request": ["ops", "security"],
    "account_closure": ["ops"],
    "refund_query": ["finance"],
    "billing_query": ["finance"],
    "security_policy_query": ["security"],
    "support_process_query": ["ops"],
}


@dataclass
class Chunk:
    chunk_id: str
    text: str
    metadata: dict[str, Any]
    embedding: list[float] | None = None
    score: float = 0


def _load_env() -> None:
    load_dotenv(ROOT / ".env.local")
    load_dotenv(ROOT / ".env")


def _post_json(url: str, headers: dict[str, str], payload: dict[str, Any]) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc


def _groq_json(messages: list[dict[str, str]]) -> dict[str, Any]:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured.")

    data = _post_json(
        GROQ_URL,
        {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        {
            "model": GROQ_MODEL,
            "temperature": 0,
            "response_format": {"type": "json_object"},
            "messages": messages,
        },
    )

    raw = data.get("choices", [{}])[0].get("message", {}).get("content")
    if not isinstance(raw, str):
        raise RuntimeError("Groq response did not include message content.")
    return json.loads(raw)


def _embed_text(text: str, task_type: str) -> list[float]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    endpoint = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:embedContent?key={api_key}"
    )
    data = _post_json(
        endpoint,
        {"Content-Type": "application/json"},
        {
            "model": f"models/{GEMINI_MODEL}",
            "content": {"parts": [{"text": text}]},
            "taskType": task_type,
        },
    )
    values = data.get("embedding", {}).get("values")
    if not isinstance(values, list):
        raise RuntimeError("Gemini embedding response did not include embedding.values.")
    vector = [float(value) for value in values]
    magnitude = math.sqrt(sum(value * value for value in vector))
    if magnitude == 0:
        raise RuntimeError("Gemini returned a zero-length embedding.")
    return [value / magnitude for value in vector]


def _metadata_from_header(text: str) -> tuple[dict[str, Any], str]:
    metadata: dict[str, Any] = {}
    body_lines: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^([a-zA-Z_]+):\s*(.*?)\s*(?:<br>)?\s*$", line)
        if match and not body_lines:
            metadata[match.group(1)] = match.group(2)
        else:
            body_lines.append(line)
    return metadata, "\n".join(body_lines).strip()


def _chunk_text(text: str, size: int = 900, overlap: int = 160) -> list[str]:
    words = text.split()
    if not words:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(words):
        end = min(len(words), start + size)
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = max(0, end - overlap)
    return chunks


def _version_group(path: str) -> str:
    return re.sub(r"_v\d+", "", path)


def _load_raw_chunks() -> list[Chunk]:
    docs = sorted(
        path for path in RAW_DOCS_DIR.rglob("*") if path.suffix.lower() in {".md", ".txt"}
    )
    latest_by_group: dict[str, str] = {}
    parsed_docs: list[tuple[Path, dict[str, Any], str]] = []

    for path in docs:
        relative = path.relative_to(ROOT).as_posix()
        metadata, body = _metadata_from_header(path.read_text(encoding="utf-8"))
        metadata.setdefault("path", relative)
        metadata.setdefault("owner", _owner_from_path(relative))
        metadata.setdefault("source_type", _source_type_from_path(relative))
        metadata.setdefault("version_group", _version_group(relative))
        latest_key = metadata["version_group"]
        last_updated = str(metadata.get("last_updated", ""))
        if latest_key not in latest_by_group or last_updated > latest_by_group[latest_key]:
            latest_by_group[latest_key] = last_updated
        parsed_docs.append((path, metadata, body))

    chunks: list[Chunk] = []
    for path, metadata, body in parsed_docs:
        relative = path.relative_to(ROOT).as_posix()
        is_latest = str(metadata.get("last_updated", "")) >= latest_by_group[metadata["version_group"]]
        for index, chunk_text in enumerate(_chunk_text(body)):
            chunk_metadata = {
                **metadata,
                "path": relative,
                "is_latest": is_latest,
                "chunk_index": index,
            }
            chunks.append(
                Chunk(
                    chunk_id=f"{relative}:{index}",
                    text=chunk_text,
                    metadata=chunk_metadata,
                )
            )
    return chunks


def _owner_from_path(path: str) -> str:
    if "billing" in path or "refund" in path:
        return "finance"
    if "security" in path or "incident" in path or "access" in path:
        return "security"
    if "support" in path:
        return "ops"
    return "ops"


def _source_type_from_path(path: str) -> str:
    if "/policies/" in path:
        return "policy"
    if "/sops/" in path:
        return "sop"
    if "/faqs/" in path:
        return "faq"
    return "notes"


def _load_index() -> list[Chunk]:
    if not SEARCH_INDEX_PATH.exists():
        return _load_raw_chunks()

    parsed = json.loads(SEARCH_INDEX_PATH.read_text(encoding="utf-8"))
    return [
        Chunk(
            chunk_id=chunk["chunk_id"],
            text=chunk["text"],
            metadata=chunk["metadata"],
            embedding=chunk.get("embedding"),
        )
        for chunk in parsed.get("chunks", [])
    ]


def _keywords(text: str) -> set[str]:
    return {
        word
        for word in re.sub(r"[^a-z0-9\s-]", " ", text.lower()).split()
        if len(word) > 3
    }


def _dot(a: list[float], b: list[float]) -> float:
    return sum(left * right for left, right in zip(a, b))


def _is_note_chunk(chunk: Chunk) -> bool:
    source_type = str(chunk.metadata.get("source_type", "")).lower()
    path = str(chunk.metadata.get("path", "")).lower()
    return source_type in {"note", "notes"} or "/notes/" in path


def detect_intents(user_query: str) -> list[str]:
    if os.getenv("GROQ_API_KEY"):
        try:
            parsed = _groq_json(
                [
                    {
                        "role": "system",
                        "content": (
                            "You are an intent classifier. Return strict JSON with "
                            '{"intents":[{"name": string, "confidence": number}]}. '
                            f"Only use these names: {json.dumps(sorted(ALLOWED_INTENTS))}."
                        ),
                    },
                    {"role": "user", "content": user_query},
                ]
            )
            return [
                intent["name"]
                for intent in parsed.get("intents", [])
                if intent.get("name") in ALLOWED_INTENTS and float(intent.get("confidence", 0)) >= 0.5
            ]
        except Exception:
            pass

    text = user_query.lower()
    intents: list[str] = []
    if any(word in text for word in ["refund", "cancel", "billing", "invoice", "payment", "charge", "charged"]):
        intents.append("refund_query" if "refund" in text or "cancel" in text else "billing_query")
    if any(word in text for word in ["access", "permission", "login", "role", "verification", "verify", "documents"]):
        intents.append("access_request")
    if any(word in text for word in ["close", "closure", "terminate", "termination", "suspended", "violate", "violation", "terms of service"]):
        intents.append("account_closure")
    if any(word in text for word in ["hacked", "fraud", "security", "unauthorized", "incident", "without permission"]):
        intents.append("security_policy_query")
    if any(word in text for word in ["support", "sla", "ticket"]):
        intents.append("support_process_query")
    return list(dict.fromkeys(intents))


def route_intents(intents: list[str]) -> list[str]:
    owners: list[str] = []
    for intent in intents:
        owners.extend(INTENT_TO_OWNERS.get(intent, []))
    return list(dict.fromkeys(owners))


def retrieve_chunks(user_query: str, allowed_owners: list[str], top_k: int = 5) -> list[Chunk]:
    if not allowed_owners:
        return []

    chunks = [
        chunk
        for chunk in _load_index()
        if chunk.metadata.get("owner") in allowed_owners
        and chunk.metadata.get("is_latest") is not False
        and not _is_note_chunk(chunk)
    ]

    if not chunks:
        return []

    if SEARCH_INDEX_PATH.exists() and os.getenv("GEMINI_API_KEY"):
        try:
            query_embedding = _embed_text(user_query, "RETRIEVAL_QUERY")
            scored = [
                Chunk(**{**chunk.__dict__, "score": _dot(query_embedding, chunk.embedding or [])})
                for chunk in chunks
            ]
            scored.sort(key=lambda chunk: chunk.score, reverse=True)
            return scored[:top_k] if scored and scored[0].score >= 0.25 else []
        except Exception:
            pass

    query_words = _keywords(user_query)
    scored = []
    for chunk in chunks:
        chunk_words = _keywords(chunk.text)
        overlap = len(query_words & chunk_words)
        score = overlap / max(1, len(query_words))
        path = str(chunk.metadata.get("path", ""))
        source_type = str(chunk.metadata.get("source_type", ""))
        if source_type == "policy":
            score += 0.2
        elif source_type == "sop":
            score += 0.15
        if "refund" in query_words and "refund" in path:
            score += 0.1
        if score > 0:
            scored.append(Chunk(**{**chunk.__dict__, "score": score}))
    scored.sort(key=lambda chunk: chunk.score, reverse=True)
    return scored[:top_k]


def apply_constraints(chunks: list[Chunk], allowed_owners: list[str]) -> list[Chunk]:
    seen: set[str] = set()
    cleaned: list[Chunk] = []
    for chunk in chunks:
        if _is_note_chunk(chunk):
            continue
        if chunk.metadata.get("owner") not in allowed_owners:
            continue
        if chunk.chunk_id in seen:
            continue
        seen.add(chunk.chunk_id)
        cleaned.append(chunk)
    return cleaned


def evaluate_governance(user_query: str, chunks: list[Chunk]) -> Verdict:
    text = user_query.lower()
    refund_after_days = re.search(r"\bafter\s+(\d+)\s+days?\b", text)
    if any(phrase in text for phrase in ["hacked", "fraud", "unauthorized", "without permission", "legal action", "charged twice", "double charged"]):
        return "ESCALATE"
    if any(
        phrase in text
        for phrase in [
            "bypass",
            "fake",
            "ignore policy",
            "override",
            "outside the allowed window",
            "another user's data",
            "all user payment data",
            "refund all charges",
        ]
    ):
        return "REFUSE_POLICY"
    if "refund" in text and refund_after_days and int(refund_after_days.group(1)) > 7:
        return "REFUSE_POLICY"
    if "refund" in text and any(phrase in text for phrase in ["policy violation", "terms of service violation", "account termination"]):
        return "REFUSE_POLICY"
    if not chunks:
        return "REFUSE_INVALID"
    return "SAFE"


def _context(chunks: list[Chunk]) -> str:
    return "\n\n---\n\n".join(
        f"Document: {chunk.metadata.get('path')}\n{chunk.text}" for chunk in chunks[:5]
    )


def _best_evidence_sentence(user_query: str, chunks: list[Chunk]) -> tuple[Chunk, str]:
    query_words = _keywords(user_query)
    refund_request_query = "refund" in query_words and any(
        token in user_query.lower() for token in ["how", "get", "request", "apply", "submit"]
    )
    best_chunk = chunks[0]
    best_sentence = re.split(r"(?<=[.!?])\s+", best_chunk.text.strip())[0]
    best_score = -1.0

    for chunk in chunks[:5]:
        candidates = [
            candidate.strip(" -")
            for candidate in re.split(r"(?<=[.!?])\s+|\n+", chunk.text)
            if candidate.strip(" -")
        ]
        for sentence in candidates:
            sentence_words = _keywords(sentence)
            score = len(query_words & sentence_words)
            if refund_request_query:
                score += sum(
                    1
                    for token in ["request", "submitted", "support", "channels", "intake"]
                    if token in sentence.lower()
                )
            if score > best_score:
                best_chunk = chunk
                best_sentence = sentence
                best_score = score

    return best_chunk, best_sentence


def generate_answer(user_query: str, chunks: list[Chunk]) -> dict[str, Any]:
    top_chunks = chunks[:5]
    if not top_chunks:
        return {
            "status": "SAFE",
            "answer": None,
            "message": None,
            "sources": [],
            "supporting_clauses": [],
            "confidence": "low",
            "context_used": 0,
        }

    if os.getenv("GROQ_API_KEY"):
        try:
            parsed = _groq_json(
                [
                    {
                        "role": "system",
                        "content": (
                            "You are a strict internal policy assistant. Return strict JSON "
                            'with {"answer": string|null, "sources": [string], '
                            '"supporting_clauses": [string], "confidence": "high|medium|low"}. '
                            "Use only the provided context."
                        ),
                    },
                    {"role": "user", "content": f"User Question:\n{user_query}\n\nContext:\n{_context(top_chunks)}"},
                ]
            )
            valid_paths = {chunk.metadata.get("path") for chunk in top_chunks}
            return {
                "status": "SAFE",
                "answer": parsed.get("answer"),
                "message": None,
                "sources": [src for src in parsed.get("sources", []) if src in valid_paths],
                "supporting_clauses": parsed.get("supporting_clauses", []),
                "confidence": parsed.get("confidence", "low"),
                "context_used": len(top_chunks),
            }
        except Exception:
            pass

    best, first_sentence = _best_evidence_sentence(user_query, top_chunks)
    return {
        "status": "SAFE",
        "answer": f"Based on the retrieved policy evidence: {first_sentence}",
        "message": None,
        "sources": [best.metadata.get("path", "unknown")],
        "supporting_clauses": [first_sentence],
        "confidence": "medium",
        "context_used": len(top_chunks),
    }


def generate_policy_denial(chunks: list[Chunk]) -> dict[str, Any]:
    source_paths = list(dict.fromkeys(chunk.metadata.get("path", "unknown") for chunk in chunks[:5]))
    clause = chunks[0].text.split(".")[0] if chunks else ""
    return {
        "status": "REFUSED",
        "answer": None,
        "message": "This request cannot be fulfilled due to existing policy restrictions.",
        "sources": source_paths,
        "supporting_clauses": [clause] if clause else [],
        "confidence": "medium" if chunks else "low",
        "context_used": len(chunks[:5]),
    }


def check_grounding(answer: str | None, chunks: list[Chunk]) -> dict[str, Any]:
    if not answer or not chunks:
        return {"grounded": False, "unsupported": ["No context available"]}
    retrieved_text = " ".join(chunk.text for chunk in chunks).lower()
    unsupported = []
    for sentence in [part.strip() for part in answer.split(".") if part.strip()]:
        words = [word for word in _keywords(sentence) if len(word) > 4]
        if words and sum(1 for word in words if word in retrieved_text) / len(words) < 0.4:
            unsupported.append(sentence)
    return {"grounded": not unsupported, "unsupported": unsupported}


def run_pipeline(user_query: str) -> dict[str, Any]:
    _load_env()
    started = time.time()
    intents = detect_intents(user_query)
    allowed_owners = route_intents(intents)
    retrieved = retrieve_chunks(user_query, allowed_owners)
    cleaned = apply_constraints(retrieved, allowed_owners)
    verdict = evaluate_governance(user_query, cleaned)

    if verdict == "REFUSE_INVALID":
        result = {
            "status": "REFUSED",
            "answer": None,
            "message": "I cannot assist with that request as it is not related to this system.",
            "sources": [],
            "supporting_clauses": [],
            "confidence": "low",
            "context_used": 0,
        }
    elif verdict == "ESCALATE":
        result = {
            "status": "ESCALATED",
            "answer": None,
            "message": "This request requires human review and has been escalated.",
            "sources": [],
            "supporting_clauses": [],
            "confidence": "low",
            "context_used": len(cleaned),
        }
    elif verdict == "REFUSE_POLICY":
        result = generate_policy_denial(cleaned)
    else:
        result = generate_answer(user_query, cleaned)

    result["verdict"] = verdict
    result["total_latency_ms"] = round((time.time() - started) * 1000, 2)

    if result.get("status") == "SAFE" and result.get("answer"):
        grounding = check_grounding(result["answer"], cleaned)
        result["hallucination_detected"] = not grounding["grounded"]
        result["unsupported_clauses"] = grounding["unsupported"]
        if not grounding["grounded"]:
            result["confidence"] = "low"

    return result
