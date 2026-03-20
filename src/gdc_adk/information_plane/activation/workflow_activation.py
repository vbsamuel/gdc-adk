from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from gdc_adk.information_plane.activation.trigger_router import ActivationTrigger
from gdc_adk.information_plane.normalization.canonicalizer import CanonicalSignal


@dataclass(frozen=True)
class ActivationOutput:
    activation_output_id: str
    activation_category: str
    candidate_workflow_mode: str
    related_artifact_ids: tuple[str, ...]
    issue_triggered: bool
    activation_reason: dict[str, object]
    next_action_types: tuple[str, ...]
    normalized_signal_id: str
    created_at: str


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _validate_activation_inputs(
    normalized_signal: CanonicalSignal,
    artifact_ids: tuple[str, ...] | list[str],
    trigger_metadata: ActivationTrigger,
) -> tuple[CanonicalSignal, tuple[str, ...], ActivationTrigger]:
    if not isinstance(normalized_signal, CanonicalSignal):
        raise ValueError("normalized_signal must be a CanonicalSignal.")
    if not isinstance(trigger_metadata, ActivationTrigger):
        raise ValueError("trigger_metadata must be an ActivationTrigger.")

    normalized_artifact_ids = tuple(str(artifact_id) for artifact_id in artifact_ids)
    if not normalized_artifact_ids or any(not artifact_id.strip() for artifact_id in normalized_artifact_ids):
        raise ValueError("artifact_ids must contain at least one non-empty artifact identifier.")
    if not normalized_signal.extracted_text:
        raise ValueError("normalized_signal must contain extracted_text.")
    return normalized_signal, normalized_artifact_ids, trigger_metadata


def build_activation_output(
    normalized_signal: CanonicalSignal,
    artifact_ids: tuple[str, ...] | list[str],
    trigger_metadata: ActivationTrigger,
) -> ActivationOutput:
    canonical_signal, normalized_artifact_ids, trigger = _validate_activation_inputs(
        normalized_signal,
        artifact_ids,
        trigger_metadata,
    )
    return ActivationOutput(
        activation_output_id=f"act_{uuid4().hex[:12]}",
        activation_category=trigger.activation_category,
        candidate_workflow_mode=trigger.candidate_workflow_mode,
        related_artifact_ids=normalized_artifact_ids,
        issue_triggered=trigger.issue_triggered,
        activation_reason=asdict(trigger.activation_reason),
        next_action_types=trigger.next_action_types,
        normalized_signal_id=canonical_signal.normalized_signal_id,
        created_at=_utc_now(),
    )


def activate_workflow(
    normalized_signal: CanonicalSignal,
    artifact_ids: tuple[str, ...] | list[str],
    trigger_metadata: ActivationTrigger,
) -> ActivationOutput:
    return build_activation_output(normalized_signal, artifact_ids, trigger_metadata)


def activation_output_to_record(activation_output: ActivationOutput) -> dict[str, Any]:
    return asdict(activation_output)
