from __future__ import annotations

from typing import Dict, List

from gdc_adk.substrate.artifact_store import get_artifact

_PROVENANCE: Dict[str, Dict[str, object]] = {}


def reset_provenance_records() -> None:
    _PROVENANCE.clear()


def export_provenance_records() -> Dict[str, Dict[str, object]]:
    return {
        artifact_id: {
            "source": dict(record.get("source", {})),
            "parents": list(record.get("parents", [])),
        }
        for artifact_id, record in _PROVENANCE.items()
    }


def load_provenance_records(records: Dict[str, Dict[str, object]]) -> None:
    reset_provenance_records()
    for artifact_id, record in records.items():
        _ensure_artifact_exists(artifact_id)
        source = record.get("source", {})
        parents = record.get("parents", [])
        if not isinstance(source, dict):
            raise TypeError("record.source must be dict")
        if not isinstance(parents, list):
            raise TypeError("record.parents must be list")
        for parent_id in parents:
            _ensure_artifact_exists(parent_id)
        _PROVENANCE[artifact_id] = {"source": dict(source), "parents": list(parents)}


def _ensure_artifact_exists(artifact_id: str) -> None:
    try:
        get_artifact(artifact_id)
    except KeyError as exc:
        raise KeyError(f"Artifact not found: {artifact_id}") from exc


def record_artifact_source(artifact_id: str, source: dict) -> dict:
    _ensure_artifact_exists(artifact_id)
    if not isinstance(source, dict):
        raise TypeError("source must be dict")

    entry = _PROVENANCE.setdefault(artifact_id, {"source": {}, "parents": []})
    entry["source"] = source
    return {"artifact_id": artifact_id, **entry}


def record_artifact_derivation(artifact_id: str, parent_artifact_ids: List[str]) -> dict:
    _ensure_artifact_exists(artifact_id)
    if not isinstance(parent_artifact_ids, list):
        raise TypeError("parent_artifact_ids must be list")
    for parent_id in parent_artifact_ids:
        _ensure_artifact_exists(parent_id)

    entry = _PROVENANCE.setdefault(artifact_id, {"source": {}, "parents": []})
    entry["parents"] = list({*entry.get("parents", []), *parent_artifact_ids})
    return {"artifact_id": artifact_id, **entry}


def get_artifact_provenance(artifact_id: str) -> dict:
    _ensure_artifact_exists(artifact_id)
    if artifact_id not in _PROVENANCE:
        return {"artifact_id": artifact_id, "source": {}, "parents": []}
    return {"artifact_id": artifact_id, **_PROVENANCE[artifact_id]}
