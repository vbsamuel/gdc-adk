from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from gdc_adk.adapters.adk.external_contracts import (
    AdapterInvocationContext,
    ExternalRequest,
    ExternalValidationResult,
    validate_adapter_invocation_context,
    validate_external_request,
)
from gdc_adk.adapters.adk.replay_envelope import (
    ReplayReferenceEnvelope,
    deserialize_replay_reference_envelope,
    validate_replay_reference_envelope,
)


@dataclass(frozen=True)
class InternalAdapterRequest:
    request_id: str
    adapter_name: str
    operation: str
    normalized_prompt: str
    requested_capabilities: tuple[str, ...]
    requested_locations: tuple[str, ...]
    invocation_origin: str
    caller_identity: str
    workflow_mode_hint: str | None
    replay_reference_envelope: ReplayReferenceEnvelope | None = None


def _coerce_replay_reference_envelope(
    replay_reference_envelope: ReplayReferenceEnvelope | dict[str, Any] | None,
) -> ReplayReferenceEnvelope | None:
    if replay_reference_envelope is None:
        return None

    if isinstance(replay_reference_envelope, ReplayReferenceEnvelope):
        return replay_reference_envelope

    if isinstance(replay_reference_envelope, dict):
        return deserialize_replay_reference_envelope(replay_reference_envelope)

    raise ValueError(
        "replay_reference_envelope must be a ReplayReferenceEnvelope, "
        "serialized replay envelope dict, or None."
    )


def validate_external_request_for_mapping(
    external_request: ExternalRequest,
    invocation_context: AdapterInvocationContext,
) -> ExternalValidationResult:
    try:
        validate_external_request(external_request)
        validate_adapter_invocation_context(invocation_context)

        replay_reference_envelope = _coerce_replay_reference_envelope(
            external_request.replay_reference_envelope
        )
        if replay_reference_envelope is not None:
            validate_replay_reference_envelope(replay_reference_envelope)

        if external_request.metadata is not None:
            blocked_fields = {"provider_name", "provider_payload", "memory_store", "workflow_run"}
            if any(field_name in external_request.metadata for field_name in blocked_fields):
                raise ValueError("external_request metadata may not leak provider or memory internals.")

    except ValueError as exc:
        return ExternalValidationResult(
            status="rejected",
            is_valid=False,
            violations=("external_request_invalid",),
            message=str(exc),
        )

    return ExternalValidationResult(
        status="accepted",
        is_valid=True,
        message="External request is valid.",
    )


def map_external_request(
    external_request: ExternalRequest,
    invocation_context: AdapterInvocationContext,
) -> InternalAdapterRequest:
    validation_result = validate_external_request_for_mapping(external_request, invocation_context)
    if not validation_result.is_valid:
        raise ValueError(validation_result.message)

    replay_reference_envelope = _coerce_replay_reference_envelope(
        external_request.replay_reference_envelope
    )
    if replay_reference_envelope is not None:
        validate_replay_reference_envelope(replay_reference_envelope)

    return InternalAdapterRequest(
        request_id=external_request.request_id,
        adapter_name=invocation_context.adapter_name,
        operation=external_request.operation,
        normalized_prompt=external_request.prompt.strip(),
        requested_capabilities=external_request.requested_capabilities,
        requested_locations=external_request.requested_locations,
        invocation_origin=invocation_context.request_origin,
        caller_identity=invocation_context.caller_identity,
        workflow_mode_hint=invocation_context.workflow_mode_hint,
        replay_reference_envelope=replay_reference_envelope,
    )