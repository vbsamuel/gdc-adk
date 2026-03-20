from __future__ import annotations

from typing import Dict, List

from gdc_adk.substrate.artifact_store import get_artifact

_VERSION_HISTORY: Dict[str, List[dict]] = {}
_SUPERSEDED_BY: Dict[str, str] = {}


def reset_version_records() -> None:
    _VERSION_HISTORY.clear()
    _SUPERSEDED_BY.clear()


def export_version_records() -> dict[str, object]:
    return {
        "version_history": {
            artifact_id: [dict(record) for record in history]
            for artifact_id, history in _VERSION_HISTORY.items()
        },
        "superseded_by": dict(_SUPERSEDED_BY),
    }


def load_version_records(records: dict[str, object]) -> None:
    reset_version_records()
    version_history = records.get("version_history", {})
    superseded_by = records.get("superseded_by", {})
    if not isinstance(version_history, dict):
        raise TypeError("version_history must be dict")
    if not isinstance(superseded_by, dict):
        raise TypeError("superseded_by must be dict")

    for artifact_id, history in version_history.items():
        _ensure_artifact_exists(artifact_id)
        if not isinstance(history, list):
            raise TypeError("version history entries must be lists")
        for record in history:
            if not isinstance(record, dict):
                raise TypeError("version record must be dict")
            create_version_record(
                artifact_id=artifact_id,
                version_number=record["version_number"],
                parent_version=record.get("parent_version"),
            )

    for artifact_id, superseded_by_artifact_id in superseded_by.items():
        if not isinstance(superseded_by_artifact_id, str):
            raise TypeError("superseded_by values must be strings")
        mark_artifact_superseded(artifact_id, superseded_by_artifact_id)


def _ensure_artifact_exists(artifact_id: str) -> None:
    try:
        get_artifact(artifact_id)
    except KeyError as exc:
        raise KeyError(f"Artifact not found: {artifact_id}") from exc


def create_version_record(artifact_id: str, version_number: int, parent_version: int | None) -> dict:
    _ensure_artifact_exists(artifact_id)
    if not isinstance(version_number, int) or version_number < 0:
        raise ValueError("version_number must be non-negative int")

    history = _VERSION_HISTORY.setdefault(artifact_id, [])
    if any(r["version_number"] == version_number for r in history):
        raise ValueError("Duplicate version number for artifact")

    record = {"artifact_id": artifact_id, "version_number": version_number, "parent_version": parent_version}
    history.append(record)
    return record


def get_version_history(artifact_id: str) -> List[dict]:
    _ensure_artifact_exists(artifact_id)
    return list(_VERSION_HISTORY.get(artifact_id, []))


def mark_artifact_superseded(artifact_id: str, superseded_by_artifact_id: str) -> dict:
    _ensure_artifact_exists(artifact_id)
    _ensure_artifact_exists(superseded_by_artifact_id)
    if artifact_id == superseded_by_artifact_id:
        raise ValueError("Cannot supersede artifact with itself")

    _SUPERSEDED_BY[artifact_id] = superseded_by_artifact_id
    return {"artifact_id": artifact_id, "superseded_by": superseded_by_artifact_id}


def get_superseded_by(artifact_id: str) -> str | None:
    return _SUPERSEDED_BY.get(artifact_id)
