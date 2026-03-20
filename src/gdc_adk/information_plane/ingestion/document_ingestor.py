from __future__ import annotations


def ingest_text(text: str, source: str = "user_input") -> dict:
    return {
        "type": "text",
        "source": source,
        "content": text,
    }
