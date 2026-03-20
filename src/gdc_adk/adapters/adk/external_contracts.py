from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, TypeAlias

from gdc_adk.adapters.adk.replay_envelope import (
    ReplayReferenceEnvelope,
    deserialize_replay_reference_envelope,
)


ALLOWED_EXTERNAL_OPERATIONS: frozenset[str] = frozenset({"weather_lookup", "time_lookup"})
ALLOWED_EXTERNAL_STATUS: frozenset[str] = frozenset({"accepted", "rejected", "completed", "failed"})

SerializedReplayReferenceEnvelope: TypeAlias = dict[str, Any]
ExternalReplayReferenceEnvelope: TypeAlias = ReplayReferenceEnvelope | SerializedReplayReferenceEnvelope | None


@dataclass(frozen=True)
class AdapterInvocationContext:
    adapter_name: str
    caller_identity: str
    request_origin: str
    workflow_mode_hint: str | None = None


@dataclass(frozen=True)
class ExternalRequest:
    request_id: str
    operation: str
    prompt: str
    requested_capabilities: tuple[str, ...]
    requested_locations: tuple[str, ...] = ()
    replay_reference_envelope: ExternalReplayReferenceEnvelope = None
    metadata: dict[str, object] | None = None


@dataclass(frozen=True)
class ExternalResponse:
    request_id: str
    status: str
    response_text: str
    response_items: tuple[str, ...]
    replay_reference_envelope: ExternalReplayReferenceEnvelope = None
    metadata: dict[str, object] | None = None


@dataclass(frozen=True)
class ExternalErrorResponse:
    request_id: str
    status: str
    error_code: str
    error_message: str
    replay_reference_envelope: ExternalReplayReferenceEnvelope = None


@dataclass(frozen=True)
class ExternalValidationResult:
    status: str
    is_valid: bool
    violations: tuple[str, ...] = ()
    message: str = ""


def _validate_non_empty_string(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be non-empty.")


def _validate_string_tuple(values: tuple[str, ...], field_name: str, *, allow_empty: bool = True) -> None:
    if not isinstance(values, tuple):
        raise ValueError(f"{field_name} must be a tuple.")
    if not allow_empty and not values:
        raise ValueError(f"{field_name} must contain at least one value.")
    for value in values:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must contain only non-empty string values.")


def _validate_replay_reference_envelope_boundary(
    replay_reference_envelope: ExternalReplayReferenceEnvelope,
) -> None:
    if replay_reference_envelope is None:
        return

    if isinstance(replay_reference_envelope, ReplayReferenceEnvelope):
        return

    if isinstance(replay_reference_envelope, dict):
        deserialize_replay_reference_envelope(replay_reference_envelope)
        return

    raise ValueError(
        "replay_reference_envelope must be a ReplayReferenceEnvelope, "
        "serialized replay envelope dict, or None."
    )


def validate_adapter_invocation_context(invocation_context: AdapterInvocationContext) -> None:
    if not isinstance(invocation_context, AdapterInvocationContext):
        raise ValueError("invocation_context must be an AdapterInvocationContext.")

    _validate_non_empty_string(invocation_context.adapter_name, "adapter_name")
    _validate_non_empty_string(invocation_context.caller_identity, "caller_identity")
    _validate_non_empty_string(invocation_context.request_origin, "request_origin")

    if invocation_context.workflow_mode_hint is not None:
        _validate_non_empty_string(invocation_context.workflow_mode_hint, "workflow_mode_hint")


def validate_external_request(external_request: ExternalRequest) -> None:
    if not isinstance(external_request, ExternalRequest):
        raise ValueError("external_request must be an ExternalRequest.")

    _validate_non_empty_string(external_request.request_id, "request_id")

    if external_request.operation not in ALLOWED_EXTERNAL_OPERATIONS:
        raise ValueError(f"Unsupported external operation: {external_request.operation}")

    _validate_non_empty_string(external_request.prompt, "prompt")
    _validate_string_tuple(
        external_request.requested_capabilities,
        "requested_capabilities",
        allow_empty=False,
    )
    _validate_string_tuple(external_request.requested_locations, "requested_locations", allow_empty=True)

    if external_request.metadata is not None and not isinstance(external_request.metadata, dict):
        raise ValueError("metadata must be a dict or None.")

    _validate_replay_reference_envelope_boundary(external_request.replay_reference_envelope)


def validate_external_response(external_response: ExternalResponse) -> None:
    if not isinstance(external_response, ExternalResponse):
        raise ValueError("external_response must be an ExternalResponse.")

    _validate_non_empty_string(external_response.request_id, "request_id")

    if external_response.status not in ALLOWED_EXTERNAL_STATUS:
        raise ValueError(f"Unsupported external response status: {external_response.status}")

    _validate_non_empty_string(external_response.response_text, "response_text")
    _validate_string_tuple(external_response.response_items, "response_items", allow_empty=True)

    if external_response.metadata is not None and not isinstance(external_response.metadata, dict):
        raise ValueError("metadata must be a dict or None.")

    _validate_replay_reference_envelope_boundary(external_response.replay_reference_envelope)


def validate_external_error_response(error_response: ExternalErrorResponse) -> None:
    if not isinstance(error_response, ExternalErrorResponse):
        raise ValueError("error_response must be an ExternalErrorResponse.")

    _validate_non_empty_string(error_response.request_id, "request_id")

    if error_response.status != "rejected":
        raise ValueError("ExternalErrorResponse status must be 'rejected'.")

    _validate_non_empty_string(error_response.error_code, "error_code")
    _validate_non_empty_string(error_response.error_message, "error_message")

    _validate_replay_reference_envelope_boundary(error_response.replay_reference_envelope)


def serialize_external_request(external_request: ExternalRequest) -> dict[str, Any]:
    validate_external_request(external_request)
    return asdict(external_request)


def serialize_external_response(external_response: ExternalResponse) -> dict[str, Any]:
    validate_external_response(external_response)
    return asdict(external_response)


def serialize_external_error_response(error_response: ExternalErrorResponse) -> dict[str, Any]:
    validate_external_error_response(error_response)
    return asdict(error_response)