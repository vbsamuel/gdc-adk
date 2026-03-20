"""Stage 7 acceptance mapping for the bounded adapter slice.

Requirement mapping:
- FX-R016: external adapters expose typed request/response boundaries, remain thin, preserve replay/reference envelopes, reject malformed input, and prove Stage 6 -> Stage 7 boundary and replay-safe round trip

Acceptance scenarios:
- Scenario A: valid ExternalRequest is accepted and mapped into typed internal adapter surfaces
- Scenario B: valid internal typed result maps back to ExternalResponse without leaking internal details
- Scenario C: replay/reference envelope survives round-trip serialization and adapter round trip
- Scenario D: malformed or unsafe external input is rejected before internal business logic
- Scenario E: Stage 6 -> Stage 7 forward-boundary proof exists using typed Stage 6 artifacts only
- Scenario F: thin adapter and lab harness surfaces operate without owning business logic
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import pytest

from gdc_adk.adapters.adk.external_contracts import (
    AdapterInvocationContext,
    ExternalErrorResponse,
    ExternalRequest,
    ExternalResponse,
    serialize_external_request,
)
from gdc_adk.adapters.adk.replay_envelope import (
    ReplayReferenceEnvelope,
    build_replay_reference_envelope,
    deserialize_replay_reference_envelope,
    serialize_replay_reference_envelope,
)
from gdc_adk.adapters.adk.request_mapper import InternalAdapterRequest, map_external_request
from gdc_adk.adapters.adk.response_mapper import InternalAdapterResult, map_internal_error, map_internal_result
from gdc_adk.adapters.adk.weather_time_agent_adapter import WeatherTimeAgentAdapter, build_weather_time_agent, reject_adapter_misuse
from gdc_adk.memory.contracts import ContinuitySnapshot, ReplayPackage
from gdc_adk.workflows.agent_contracts import (
    AgentTraceRecord,
    Stage7ForwardEnvelope,
    build_stage7_forward_envelope,
)


def _build_stage6_forward_envelope() -> Stage7ForwardEnvelope:
    trace_record = AgentTraceRecord(
        workflow_run_id="wr_stage7",
        handoff_id="handoff_1",
        from_role="planner",
        to_role="executor",
        action_type="handoff_completed",
        artifact_ids=("art_1",),
        issue_ids=("iss_1",),
        finding_ids=("finding_1",),
        context_block_ids=("ctx_1",),
        continuity_snapshot_id="snap_1",
        delegation_depth=1,
        status="completed",
        recorded_at="2026-03-20T12:00:00Z",
    )
    return Stage7ForwardEnvelope(
        workflow_run_id="wr_stage7",
        handoff_ids=("handoff_1",),
        completed_handoff_ids=("handoff_1",),
        artifact_ids=("art_1",),
        issue_ids=("iss_1",),
        finding_ids=("finding_1",),
        continuity_snapshot_ids=("snap_1",),
        context_block_ids=("ctx_1",),
        trace_records=(trace_record,),
    )


def _build_replay_package() -> ReplayPackage:
    return ReplayPackage(
        replay_package_id="replay_stage7",
        schema_version="stage5.v1",
        exported_at="2026-03-20T12:00:00Z",
        workflow_run_ids=("wr_stage7",),
        snapshot_ids=("snap_1",),
        context_block_ids=("ctx_1",),
        artifact_summary_refs=("art_1",),
        issue_evidence_refs=("iss_1",),
        export_source="memory.replay",
    )


def _build_continuity_snapshot() -> ContinuitySnapshot:
    return ContinuitySnapshot(
        snapshot_id="snap_1",
        workflow_run_id="wr_stage7",
        workflow_mode="dynamic_flow",
        current_state="planned",
        state_history=({"from_state": "activated", "to_state": "planned", "reason": "planned", "changed_at": "2026-03-20T12:00:00Z"},),
        artifact_ids=("art_1",),
        issue_ids=("iss_1",),
        finding_ids=("finding_1",),
        context_refs=("ctx_1",),
        pending_actions=("execute_artifact",),
        created_at="2026-03-20T12:00:01Z",
    )


def _build_external_request(replay_reference_envelope: ReplayReferenceEnvelope | None = None) -> ExternalRequest:
    return ExternalRequest(
        request_id="req_stage7",
        operation="weather_lookup",
        prompt="What is the weather in Seattle?",
        requested_capabilities=("weather",),
        requested_locations=("Seattle",),
        replay_reference_envelope=None if replay_reference_envelope is None else serialize_replay_reference_envelope(replay_reference_envelope),
        metadata={"channel": "adk"},
    )


def _build_invocation_context() -> AdapterInvocationContext:
    return AdapterInvocationContext(
        adapter_name="weather_time_agent",
        caller_identity="unit_test",
        request_origin="tests",
        workflow_mode_hint="dynamic_flow",
    )


def _internal_handler(internal_request: InternalAdapterRequest) -> InternalAdapterResult:
    return InternalAdapterResult(
        request_id=internal_request.request_id,
        status="completed",
        response_text=f"Handled {internal_request.operation} for {internal_request.requested_locations[0]}.",
        response_items=(internal_request.operation, internal_request.requested_locations[0]),
        replay_reference_envelope=internal_request.replay_reference_envelope,
        metadata={"channel": "adk"},
    )


def test_stage7_valid_external_request_is_accepted_and_mapped_correctly() -> None:
    forward_envelope = _build_stage6_forward_envelope()
    replay_reference_envelope = build_replay_reference_envelope(
        forward_envelope,
        replay_package=_build_replay_package(),
        continuity_snapshot=_build_continuity_snapshot(),
    )
    external_request = _build_external_request(replay_reference_envelope)
    invocation_context = _build_invocation_context()

    mapped_request = map_external_request(external_request, invocation_context)

    assert mapped_request.adapter_name == "weather_time_agent"
    assert mapped_request.operation == "weather_lookup"
    assert mapped_request.replay_reference_envelope is not None
    assert serialize_external_request(external_request)["operation"] == "weather_lookup"


def test_stage7_valid_internal_result_maps_to_external_response_correctly() -> None:
    response = map_internal_result(
        InternalAdapterResult(
            request_id="req_stage7",
            status="completed",
            response_text="Weather handled safely.",
            response_items=("weather_lookup", "Seattle"),
            metadata={"channel": "adk"},
        )
    )

    assert isinstance(response, ExternalResponse)
    assert response.status == "completed"
    assert response.response_items == ("weather_lookup", "Seattle")


def test_stage7_replay_reference_envelope_survives_round_trip_serialization() -> None:
    replay_reference_envelope = build_replay_reference_envelope(
        _build_stage6_forward_envelope(),
        replay_package=_build_replay_package(),
        continuity_snapshot=_build_continuity_snapshot(),
    )

    serialized = serialize_replay_reference_envelope(replay_reference_envelope)
    deserialized = deserialize_replay_reference_envelope(serialized)

    assert deserialized == replay_reference_envelope
    assert deserialized.handoff_ids == ("handoff_1",)


def test_stage7_stage6_to_stage7_boundary_proof_exists_using_typed_stage6_artifacts_only() -> None:
    stage6_forward = _build_stage6_forward_envelope()
    replay_reference_envelope = build_replay_reference_envelope(stage6_forward, replay_package=_build_replay_package())
    external_request = _build_external_request(replay_reference_envelope)
    adapter = build_weather_time_agent()

    response = adapter.handle_request(external_request, _build_invocation_context(), _internal_handler)

    assert isinstance(response, ExternalResponse)
    assert response.replay_reference_envelope is not None
    assert response.replay_reference_envelope["handoff_ids"] == ("handoff_1",)


def test_stage7_malformed_external_request_is_rejected() -> None:
    adapter = WeatherTimeAgentAdapter()
    external_request = ExternalRequest(
        request_id="",
        operation="weather_lookup",
        prompt=" ",
        requested_capabilities=(),
    )

    with pytest.raises(ValueError):
        adapter.handle_request(external_request, _build_invocation_context(), _internal_handler)


def test_stage7_invalid_replay_reference_envelope_is_rejected() -> None:
    external_request = ExternalRequest(
        request_id="req_stage7",
        operation="weather_lookup",
        prompt="Weather please.",
        requested_capabilities=("weather",),
        replay_reference_envelope={"workflow_run_id": "", "handoff_ids": ("handoff_1",)},
    )

    with pytest.raises(ValueError):
        map_external_request(external_request, _build_invocation_context())


def test_stage7_invalid_response_mapping_input_is_rejected() -> None:
    with pytest.raises(ValueError):
        map_internal_result(
            InternalAdapterResult(
                request_id="req_stage7",
                status="completed",
                response_text=" ",
                response_items=(),
            )
        )


def test_stage7_adapter_misuse_or_bypass_attempt_is_rejected() -> None:
    adapter = WeatherTimeAgentAdapter()
    with pytest.raises(ValueError):
        adapter.handle_request(_build_external_request(), AdapterInvocationContext("wrong_adapter", "tester", "tests"), _internal_handler)

    error_response = reject_adapter_misuse("req_stage7", "Adapter misuse detected.")
    assert isinstance(error_response, ExternalErrorResponse)
    assert error_response.error_code == "adapter_misuse_rejected"


def test_stage7_provider_internal_leakage_is_blocked() -> None:
    with pytest.raises(ValueError):
        map_internal_result(
            InternalAdapterResult(
                request_id="req_stage7",
                status="completed",
                response_text="unsafe",
                response_items=("weather_lookup",),
                metadata={"provider_name": "internal_provider"},
            )
        )


def test_stage7_memory_internal_leakage_is_blocked() -> None:
    external_request = ExternalRequest(
        request_id="req_stage7",
        operation="time_lookup",
        prompt="What time is it?",
        requested_capabilities=("time",),
        metadata={"memory_store": "internal_memory_handle"},
    )

    with pytest.raises(ValueError):
        map_external_request(external_request, _build_invocation_context())


def test_stage7_replay_safe_adapter_round_trip_is_proven() -> None:
    stage6_forward = _build_stage6_forward_envelope()
    replay_reference_envelope = build_replay_reference_envelope(
        stage6_forward,
        replay_package=_build_replay_package(),
        continuity_snapshot=_build_continuity_snapshot(),
    )
    external_request = _build_external_request(replay_reference_envelope)
    adapter = build_weather_time_agent()

    response = adapter.handle_request(external_request, _build_invocation_context(), _internal_handler)
    round_tripped_envelope = deserialize_replay_reference_envelope(response.replay_reference_envelope)

    assert round_tripped_envelope.workflow_run_id == "wr_stage7"
    assert round_tripped_envelope.replay_package_id == "replay_stage7"


def test_stage7_thin_adapter_entry_path_and_lab_harness_work_without_business_logic() -> None:
    harness_path = Path("labs/adk/weather_time_agent.py")
    module_spec = importlib.util.spec_from_file_location("stage7_weather_time_harness", harness_path)
    assert module_spec is not None and module_spec.loader is not None
    module = importlib.util.module_from_spec(module_spec)
    sys.modules[module_spec.name] = module
    module_spec.loader.exec_module(module)

    harness = module.build_weather_time_agent_harness()
    response = harness.invoke(_build_external_request(), _build_invocation_context(), _internal_handler)

    assert isinstance(response, ExternalResponse)
    assert response.response_text.startswith("Handled weather_lookup")
