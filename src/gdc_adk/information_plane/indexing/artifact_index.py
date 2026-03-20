from __future__ import annotations

_INDEX: list[dict] = []


def add(item: dict) -> None:
    _INDEX.append(item)


def search(query: str) -> list[dict]:
    q = query.lower()
    return [i for i in _INDEX if q in str(i).lower()]
