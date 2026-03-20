from __future__ import annotations


def emit(data: dict) -> dict:
    return {
        "status": "emitted",
        "payload": data,
    }
