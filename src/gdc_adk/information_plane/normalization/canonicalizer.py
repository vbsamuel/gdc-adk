from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any
from uuid import uuid4

from gdc_adk.information_plane.ingestion.document_ingestor import RawSignal


@dataclass(frozen=True)
class CanonicalSignal:
    normalized_signal_id: str
    normalized_type: str
    source_kind: str
    extracted_text: str | None
    modality_metadata: dict[str, object]
    timestamps: dict[str, str]
    provenance_notes: tuple[str, ...]
    confidence: float | None = None
    entity_candidates: tuple[str, ...] = ()
    alias_candidates: tuple[str, ...] = ()
    ambiguity_markers: tuple[str, ...] = ()
    coarse_intent: str | None = None
    activation_hints: tuple[str, ...] = field(default_factory=tuple)


def extract_text_if_available(raw_signal: RawSignal) -> str | None:
    if not isinstance(raw_signal, RawSignal):
        raise ValueError("raw_signal must be a RawSignal.")

    if isinstance(raw_signal.raw_payload, str):
        extracted_text = raw_signal.raw_payload.strip()
        return extracted_text or None

    if isinstance(raw_signal.raw_payload, dict):
        for field_name in ("text", "body", "content", "message", "summary"):
            field_value = raw_signal.raw_payload.get(field_name)
            if isinstance(field_value, str) and field_value.strip():
                return field_value.strip()

    return None


def _infer_coarse_intent(extracted_text: str | None) -> str | None:
    if extracted_text is None:
        return None

    lowered_text = extracted_text.lower()
    if any(token in lowered_text for token in ("bug", "fix", "broken", "error", "failed", "issue")):
        return "defect_triage"
    if any(token in lowered_text for token in ("research", "analyze", "investigate", "specification")):
        return "analysis_request"
    if any(token in lowered_text for token in ("weather", "forecast", "temperature")):
        return "weather_lookup"
    if any(token in lowered_text for token in ("time in", "timezone", "what time")):
        return "time_lookup"
    if any(token in lowered_text for token in ("where is", "location of", "geo")):
        return "geo_lookup"
    return "general_request"


def _build_activation_hints(extracted_text: str | None, coarse_intent: str | None) -> tuple[str, ...]:
    hints: list[str] = []
    if extracted_text:
        lowered_text = extracted_text.lower()
        if "urgent" in lowered_text:
            hints.append("priority_high")
        if "blocked" in lowered_text:
            hints.append("blocked_signal")
    if coarse_intent is not None:
        hints.append(coarse_intent)
    return tuple(hints)


def canonicalize_text_payload(raw_signal: RawSignal) -> CanonicalSignal:
    extracted_text = extract_text_if_available(raw_signal)
    if extracted_text is None:
        raise ValueError("raw_signal does not contain extractable text.")

    coarse_intent = _infer_coarse_intent(extracted_text)
    return CanonicalSignal(
        normalized_signal_id=f"norm_{uuid4().hex[:12]}",
        normalized_type=raw_signal.detected_modality,
        source_kind=raw_signal.source_kind,
        extracted_text=extracted_text,
        modality_metadata={"detected_modality": raw_signal.detected_modality},
        timestamps={"received_at": raw_signal.received_at},
        provenance_notes=raw_signal.provenance_notes,
        confidence=0.5 if raw_signal.extraction_status == "uncertain" else 1.0,
        coarse_intent=coarse_intent,
        activation_hints=_build_activation_hints(extracted_text, coarse_intent),
    )


def normalize_signal(raw_signal: RawSignal) -> CanonicalSignal:
    if not isinstance(raw_signal, RawSignal):
        raise ValueError("raw_signal must be a RawSignal.")

    extracted_text = extract_text_if_available(raw_signal)
    coarse_intent = _infer_coarse_intent(extracted_text)
    confidence = 0.5 if raw_signal.extraction_status == "uncertain" else 1.0
    ambiguity_markers: tuple[str, ...] = ()
    if extracted_text is None:
        ambiguity_markers = ("missing_text",)
        confidence = 0.0

    return CanonicalSignal(
        normalized_signal_id=f"norm_{uuid4().hex[:12]}",
        normalized_type=raw_signal.detected_modality,
        source_kind=raw_signal.source_kind,
        extracted_text=extracted_text,
        modality_metadata={"detected_modality": raw_signal.detected_modality},
        timestamps={"received_at": raw_signal.received_at},
        provenance_notes=raw_signal.provenance_notes,
        confidence=confidence,
        ambiguity_markers=ambiguity_markers,
        coarse_intent=coarse_intent,
        activation_hints=_build_activation_hints(extracted_text, coarse_intent),
    )


def canonical_signal_to_record(canonical_signal: CanonicalSignal) -> dict[str, Any]:
    return asdict(canonical_signal)
