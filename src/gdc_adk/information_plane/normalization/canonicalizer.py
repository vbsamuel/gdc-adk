from __future__ import annotations


def normalize(raw: dict) -> dict:
    return {
        "normalized_type": raw.get("type", "unknown"),
        "source": raw.get("source", "unknown"),
        "text": str(raw.get("content", "")).strip(),
    }
