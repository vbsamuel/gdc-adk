from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any, Mapping
from uuid import uuid4


SUPPORTED_EMISSION_TYPES: frozenset[str] = frozenset(
    {
        "direct_answer",
        "generated_artifact",
        "issue_update",
        "workflow_status",
        "review_packet",
        "handoff_package",
    }
)


@dataclass(frozen=True)
class EmissionInput:
    artifact_ids: tuple[str, ...]
    payload: dict[str, object]
    provenance_notes: tuple[str, ...]
    workflow_run_id: str | None = None


@dataclass(frozen=True)
class EmissionResult:
    emission_id: str
    emission_type: str
    artifact_ids: tuple[str, ...]
    workflow_run_id: str | None
    provenance_notes: tuple[str, ...]
    created_at: str
    payload: dict[str, object]


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _validate_emission_input(emission_input: EmissionInput) -> EmissionInput:
    if not isinstance(emission_input, EmissionInput):
        raise ValueError("emission_input must be an EmissionInput.")
    if not emission_input.artifact_ids or any(not artifact_id.strip() for artifact_id in emission_input.artifact_ids):
        raise ValueError("emission_input.artifact_ids must contain at least one non-empty artifact identifier.")
    if not isinstance(emission_input.payload, dict) or not emission_input.payload:
        raise ValueError("emission_input.payload must be a non-empty structured payload.")
    return emission_input


def _emit(emission_type: str, emission_input: EmissionInput) -> EmissionResult:
    if emission_type not in SUPPORTED_EMISSION_TYPES:
        raise ValueError(f"Unsupported emission_type: {emission_type}")
    validated_input = _validate_emission_input(emission_input)
    return EmissionResult(
        emission_id=f"emit_{uuid4().hex[:12]}",
        emission_type=emission_type,
        artifact_ids=validated_input.artifact_ids,
        workflow_run_id=validated_input.workflow_run_id,
        provenance_notes=validated_input.provenance_notes,
        created_at=_utc_now(),
        payload=validated_input.payload,
    )


def emit_direct_answer(emission_input: EmissionInput) -> EmissionResult:
    return _emit("direct_answer", emission_input)


def emit_generated_artifact(emission_input: EmissionInput) -> EmissionResult:
    return _emit("generated_artifact", emission_input)


def emit_issue_update(emission_input: EmissionInput) -> EmissionResult:
    return _emit("issue_update", emission_input)


def emit_workflow_status(emission_input: EmissionInput) -> EmissionResult:
    return _emit("workflow_status", emission_input)


def emit_review_packet(emission_input: EmissionInput) -> EmissionResult:
    return _emit("review_packet", emission_input)


def emit_handoff_package(emission_input: EmissionInput) -> EmissionResult:
    return _emit("handoff_package", emission_input)


def emission_result_to_record(emission_result: EmissionResult) -> dict[str, Any]:
    return asdict(emission_result)
