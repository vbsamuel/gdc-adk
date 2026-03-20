from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Mapping
from uuid import uuid4


SUPPORTED_MODALITIES: frozenset[str] = frozenset(
    {
        "plain_text",
        "markdown",
        "document_text",
        "email_text",
        "transcript_text",
        "screenshot_placeholder",
        "repository_text",
        "structured_record",
    }
)


@dataclass(frozen=True)
class RawSignal:
    raw_signal_id: str
    source_kind: str
    detected_modality: str
    raw_payload: str | dict[str, object]
    source_metadata: dict[str, object]
    received_at: str
    provenance_notes: tuple[str, ...]
    extraction_status: str | None = None


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _build_raw_signal(
    raw_payload: str | dict[str, object],
    source_metadata: Mapping[str, object] | None,
    detected_modality: str,
    extraction_status: str | None = None,
) -> RawSignal:
    if detected_modality not in SUPPORTED_MODALITIES:
        raise ValueError(f"Unsupported detected_modality: {detected_modality}")

    metadata = dict(source_metadata or {})
    source_kind = str(metadata.get("source_kind", "user_input")).strip()
    if not source_kind:
        raise ValueError("source_metadata must provide a non-empty source_kind when specified.")

    provenance_notes = tuple(str(note) for note in metadata.get("provenance_notes", ()))
    return RawSignal(
        raw_signal_id=f"raw_{uuid4().hex[:12]}",
        source_kind=source_kind,
        detected_modality=detected_modality,
        raw_payload=raw_payload,
        source_metadata=metadata,
        received_at=_utc_now(),
        provenance_notes=provenance_notes,
        extraction_status=extraction_status,
    )


def detect_modality(raw_payload: object, source_metadata: Mapping[str, object] | None = None) -> str:
    metadata = dict(source_metadata or {})
    declared_modality = metadata.get("detected_modality")
    if isinstance(declared_modality, str) and declared_modality in SUPPORTED_MODALITIES:
        return declared_modality

    if isinstance(raw_payload, dict):
        return "structured_record"

    if not isinstance(raw_payload, str):
        raise ValueError("raw_payload must be a string or a structured record.")

    stripped_payload = raw_payload.strip()
    if not stripped_payload:
        raise ValueError("raw_payload must be non-empty.")

    lowered_payload = stripped_payload.lower()
    if stripped_payload.startswith("#") or "```" in stripped_payload:
        return "markdown"
    if "subject:" in lowered_payload and "from:" in lowered_payload:
        return "email_text"
    if metadata.get("document_kind") == "transcript":
        return "transcript_text"
    if metadata.get("document_kind") == "screenshot":
        return "screenshot_placeholder"
    if metadata.get("document_kind") in {"repository", "code"}:
        return "repository_text"
    if metadata.get("document_kind") in {"document", "pdf", "docx"}:
        return "document_text"
    return "plain_text"


def ingest_text_signal(raw_text: str, source_metadata: Mapping[str, object] | None = None) -> RawSignal:
    if not isinstance(raw_text, str):
        raise ValueError("raw_text must be a string.")
    modality = detect_modality(raw_text, source_metadata)
    return _build_raw_signal(raw_text, source_metadata, modality)


def ingest_document_signal(raw_payload: str, source_metadata: Mapping[str, object] | None = None) -> RawSignal:
    if not isinstance(raw_payload, str):
        raise ValueError("raw_payload must be a string.")
    modality = detect_modality(raw_payload, source_metadata)
    extraction_status = "uncertain" if modality == "screenshot_placeholder" else None
    return _build_raw_signal(raw_payload, source_metadata, modality, extraction_status=extraction_status)


def ingest_structured_signal(
    raw_record: Mapping[str, object],
    source_metadata: Mapping[str, object] | None = None,
) -> RawSignal:
    if not isinstance(raw_record, Mapping) or not raw_record:
        raise ValueError("raw_record must be a non-empty mapping.")
    normalized_record = dict(raw_record)
    return _build_raw_signal(normalized_record, source_metadata, "structured_record")


def raw_signal_to_record(raw_signal: RawSignal) -> dict[str, object]:
    return asdict(raw_signal)
