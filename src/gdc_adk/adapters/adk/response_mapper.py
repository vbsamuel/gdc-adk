from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from gdc_adk.adapters.adk.external_contracts import (
    ExternalErrorResponse,
    ExternalResponse,
    validate_external_error_response,
    validate_external_response,
)
from gdc_adk.adapters.adk.replay_envelope import (
    ReplayReferenceEnvelope,
    serialize_replay_reference_envelope,
)


@dataclass(frozen=True)
class InternalAdapterResult:
    request_id: str
    status: str
    response_text: str
    response_items: tuple[str, ...]
    replay_reference_envelope: ReplayReferenceEnvelope | None = None
    metadata: dict[str, object] | None = None


def _validate_external_payload_value(value: Any) -> None:
    if value is None or isinstance(value, (str, int, float, bool)):
        return

    if isinstance(value, (tuple, list)):
        for item in value:
            _validate_external_payload_value(item)
        return

    if isinstance(value, dict):
        for key, nested_value in value.items():
            if not isinstance(key, str):
                raise ValueError("External metadata keys must be strings.")
            _validate_external_payload_value(nested_value)
        return

    raise ValueError("External response metadata may not include internal object instances.")


def map_internal_result(internal_result: InternalAdapterResult) -> ExternalResponse:
    if not isinstance(internal_result, InternalAdapterResult):
        raise ValueError("internal_result must be an InternalAdapterResult.")
    if not internal_result.request_id.strip():
        raise ValueError("internal_result.request_id must be non-empty.")
    if internal_result.status not in {"completed", "accepted"}:
        raise ValueError("internal_result.status must be 'accepted' or 'completed'.")
    if not internal_result.response_text.strip():
        raise ValueError("internal_result.response_text must be non-empty.")

    metadata = None
    if internal_result.metadata is not None:
        blocked_fields = {
            "provider_name",
            "provider_payload",
            "memory_store",
            "workflow_run",
            "continuity_snapshot",
        }
        if any(field_name in internal_result.metadata for field_name in blocked_fields):
            raise ValueError("internal_result metadata may not leak provider or memory internals.")
        _validate_external_payload_value(internal_result.metadata)
        metadata = dict(internal_result.metadata)

    serialized_envelope = None
    if internal_result.replay_reference_envelope is not None:
        serialized_envelope = serialize_replay_reference_envelope(
            internal_result.replay_reference_envelope
        )

    external_response = ExternalResponse(
        request_id=internal_result.request_id,
        status=internal_result.status,
        response_text=internal_result.response_text,
        response_items=internal_result.response_items,
        replay_reference_envelope=serialized_envelope,
        metadata=metadata,
    )
    validate_external_response(external_response)
    return external_response


def map_internal_error(
    request_id: str,
    error_code: str,
    error_message: str,
    replay_reference_envelope: ReplayReferenceEnvelope | None = None,
) -> ExternalErrorResponse:
    if not request_id.strip():
        raise ValueError("request_id must be non-empty.")
    if not error_code.strip():
        raise ValueError("error_code must be non-empty.")
    if not error_message.strip():
        raise ValueError("error_message must be non-empty.")

    serialized_envelope = None
    if replay_reference_envelope is not None:
        serialized_envelope = serialize_replay_reference_envelope(replay_reference_envelope)

    error_response = ExternalErrorResponse(
        request_id=request_id,
        status="rejected",
        error_code=error_code,
        error_message=error_message,
        replay_reference_envelope=serialized_envelope,
    )
    validate_external_error_response(error_response)
    return error_response