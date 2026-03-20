from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4

from gdc_adk.information_plane.normalization.canonicalizer import CanonicalSignal


@dataclass(frozen=True)
class IndexedArtifact:
    artifact_id: str
    artifact_kind: str
    normalized_signal_id: str
    source_kind: str
    extracted_text: str
    issue_ids: tuple[str, ...]
    entity_aliases: tuple[str, ...]
    timestamp_values: tuple[str, ...]
    provenance_notes: tuple[str, ...]
    created_at: str
    metadata: dict[str, object] = field(default_factory=dict)


_ARTIFACT_INDEX: dict[str, IndexedArtifact] = {}


def build_indexed_artifact(canonical_signal: CanonicalSignal, issue_ids: tuple[str, ...] = ()) -> IndexedArtifact:
    if not isinstance(canonical_signal, CanonicalSignal):
        raise ValueError("canonical_signal must be a CanonicalSignal.")
    if not canonical_signal.extracted_text:
        raise ValueError("canonical_signal must contain extracted_text for indexing.")

    timestamp_values = tuple(canonical_signal.timestamps.values())
    return IndexedArtifact(
        artifact_id=f"idx_{uuid4().hex[:12]}",
        artifact_kind="normalized_signal",
        normalized_signal_id=canonical_signal.normalized_signal_id,
        source_kind=canonical_signal.source_kind,
        extracted_text=canonical_signal.extracted_text,
        issue_ids=issue_ids,
        entity_aliases=canonical_signal.alias_candidates,
        timestamp_values=timestamp_values,
        provenance_notes=canonical_signal.provenance_notes,
        created_at=timestamp_values[0] if timestamp_values else canonical_signal.timestamps.get("received_at", ""),
        metadata={
            "normalized_type": canonical_signal.normalized_type,
            "coarse_intent": canonical_signal.coarse_intent,
        },
    )


def index_artifact(artifact: IndexedArtifact, normalized_signal: CanonicalSignal | None = None) -> None:
    if not isinstance(artifact, IndexedArtifact):
        raise ValueError("artifact must be an IndexedArtifact.")
    if normalized_signal is not None and not isinstance(normalized_signal, CanonicalSignal):
        raise ValueError("normalized_signal must be a CanonicalSignal when provided.")
    if artifact.artifact_id in _ARTIFACT_INDEX:
        raise ValueError(f"artifact_id already indexed: {artifact.artifact_id}")
    if not artifact.extracted_text.strip():
        raise ValueError("artifact.extracted_text must be non-empty.")
    _ARTIFACT_INDEX[artifact.artifact_id] = artifact


def get_artifact_by_id(artifact_id: str) -> IndexedArtifact:
    if artifact_id not in _ARTIFACT_INDEX:
        raise ValueError(f"Unknown artifact_id: {artifact_id}")
    return _ARTIFACT_INDEX[artifact_id]


def search_text(query_text: str) -> list[str]:
    if not isinstance(query_text, str) or not query_text.strip():
        raise ValueError("query_text must be a non-empty string.")
    lowered_query = query_text.lower()
    return [
        artifact_id
        for artifact_id, artifact in _ARTIFACT_INDEX.items()
        if lowered_query in artifact.extracted_text.lower()
    ]


def list_artifacts_by_source_kind(source_kind: str) -> list[str]:
    if not isinstance(source_kind, str) or not source_kind.strip():
        raise ValueError("source_kind must be a non-empty string.")
    return [artifact_id for artifact_id, artifact in _ARTIFACT_INDEX.items() if artifact.source_kind == source_kind]


def list_artifacts_linked_to_issue(issue_id: str) -> list[str]:
    if not isinstance(issue_id, str) or not issue_id.strip():
        raise ValueError("issue_id must be a non-empty string.")
    return [
        artifact_id
        for artifact_id, artifact in _ARTIFACT_INDEX.items()
        if issue_id in artifact.issue_ids
    ]


def search_by_entity_alias(alias_value: str) -> list[str]:
    if not isinstance(alias_value, str) or not alias_value.strip():
        raise ValueError("alias_value must be a non-empty string.")
    lowered_alias = alias_value.lower()
    return [
        artifact_id
        for artifact_id, artifact in _ARTIFACT_INDEX.items()
        if any(lowered_alias == alias.lower() for alias in artifact.entity_aliases)
    ]


def search_by_time_window(start_ts: str, end_ts: str) -> list[str]:
    if not start_ts or not end_ts:
        raise ValueError("start_ts and end_ts must be non-empty timestamps.")
    start_dt = datetime.fromisoformat(start_ts.replace("Z", "+00:00"))
    end_dt = datetime.fromisoformat(end_ts.replace("Z", "+00:00"))
    return [
        artifact_id
        for artifact_id, artifact in _ARTIFACT_INDEX.items()
        if any(
            start_dt <= datetime.fromisoformat(timestamp.replace("Z", "+00:00")) <= end_dt
            for timestamp in artifact.timestamp_values
        )
    ]


def reset_artifact_index() -> None:
    _ARTIFACT_INDEX.clear()


def export_artifact_index_records() -> list[dict[str, Any]]:
    return [asdict(record) for record in _ARTIFACT_INDEX.values()]


def load_artifact_index_records(records: list[dict[str, Any]]) -> None:
    if not isinstance(records, list):
        raise ValueError("records must be a list of artifact index records.")
    reset_artifact_index()
    for record in records:
        try:
            artifact = IndexedArtifact(
                artifact_id=str(record["artifact_id"]),
                artifact_kind=str(record["artifact_kind"]),
                normalized_signal_id=str(record["normalized_signal_id"]),
                source_kind=str(record["source_kind"]),
                extracted_text=str(record["extracted_text"]),
                issue_ids=tuple(str(item) for item in record.get("issue_ids", ())),
                entity_aliases=tuple(str(item) for item in record.get("entity_aliases", ())),
                timestamp_values=tuple(str(item) for item in record.get("timestamp_values", ())),
                provenance_notes=tuple(str(item) for item in record.get("provenance_notes", ())),
                created_at=str(record["created_at"]),
                metadata=dict(record.get("metadata", {})),
            )
        except KeyError as exc:
            raise ValueError(f"artifact index record missing required field: {exc.args[0]}") from exc

        if artifact.artifact_id in _ARTIFACT_INDEX:
            raise ValueError(f"artifact_id already indexed: {artifact.artifact_id}")
        index_artifact(artifact)
