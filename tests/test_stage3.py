"""Stage 3 acceptance mapping for the bounded information-plane slice.

Requirement mapping:
- FX-R006: raw signals are ingested, canonicalized, and indexed before activation
- FX-R008: fix-like normalized signals surface explicit fix_flow activation metadata for downstream issue creation

Acceptance scenarios:
- Scenario A: meaningful raw input becomes a structured canonical signal
- Scenario B: canonicalized information is indexed and replayable through public lifecycle APIs
- Scenario C: activation consumes canonicalized and indexed outputs and egress emits a structured artifact
- Scenario D: invalid ingestion, canonicalization, indexing, activation, and egress inputs are rejected
- Scenario E: a Stage 2 RouteRequest contract can feed Stage 3 processing, including a negative boundary path
"""

from __future__ import annotations

import pytest

from gdc_adk.control_plane.router import RouteRequest, route_request
from gdc_adk.information_plane.activation.trigger_router import (
    ActivationTrigger,
    build_activation_trigger,
    build_activation_reason,
    classify_activation_category,
    select_workflow_mode,
    should_trigger_issue,
)
from gdc_adk.information_plane.activation.workflow_activation import activate_workflow
from gdc_adk.information_plane.egress.artifact_emitter import (
    EmissionInput,
    emit_workflow_status,
)
from gdc_adk.information_plane.indexing.artifact_index import (
    build_indexed_artifact,
    export_artifact_index_records,
    get_artifact_by_id,
    index_artifact,
    list_artifacts_by_source_kind,
    list_artifacts_linked_to_issue,
    load_artifact_index_records,
    reset_artifact_index,
    search_by_entity_alias,
    search_by_time_window,
    search_text,
)
from gdc_adk.information_plane.ingestion.document_ingestor import (
    RawSignal,
    ingest_document_signal,
    ingest_structured_signal,
    ingest_text_signal,
)
from gdc_adk.information_plane.normalization.canonicalizer import (
    CanonicalSignal,
    canonicalize_text_payload,
    extract_text_if_available,
    normalize_signal,
)


@pytest.fixture(autouse=True)
def reset_stage3_state() -> None:
    reset_artifact_index()


def test_stage3_pipeline_ingests_canonicalizes_indexes_activates_and_emits() -> None:
    raw_signal = ingest_text_signal(
        "Please investigate the broken payment flow and fix the failing checkout.",
        {"source_kind": "user_input", "provenance_notes": ["cli_request"]},
    )
    canonical_signal = normalize_signal(raw_signal)
    indexed_artifact = build_indexed_artifact(canonical_signal, issue_ids=("iss_pending",))
    index_artifact(indexed_artifact, canonical_signal)
    activation_trigger = build_activation_trigger(canonical_signal)
    activation_output = activate_workflow(canonical_signal, (indexed_artifact.artifact_id,), activation_trigger)
    emission_result = emit_workflow_status(
        EmissionInput(
            artifact_ids=activation_output.related_artifact_ids,
            provenance_notes=canonical_signal.provenance_notes,
            payload={
                "activation_output_id": activation_output.activation_output_id,
                "candidate_workflow_mode": activation_output.candidate_workflow_mode,
            },
        )
    )

    assert raw_signal.detected_modality == "plain_text"
    assert canonical_signal.extracted_text is not None
    assert get_artifact_by_id(indexed_artifact.artifact_id) == indexed_artifact
    assert activation_output.candidate_workflow_mode == "fix_flow"
    assert activation_output.issue_triggered is True
    assert emission_result.emission_type == "workflow_status"
    assert emission_result.artifact_ids == activation_output.related_artifact_ids


def test_stage3_fix_flow_activation_surfaces_issue_trigger_metadata() -> None:
    canonical_signal = canonicalize_text_payload(
        ingest_text_signal("Bug: the billing export is broken and needs a fix.", {"source_kind": "email_ingest"})
    )

    assert classify_activation_category(canonical_signal) == "issue_candidate"
    assert select_workflow_mode(canonical_signal) == "fix_flow"
    assert should_trigger_issue(canonical_signal) is True
    assert build_activation_reason(canonical_signal).rationale_code == "defect_keyword_match"
    assert build_activation_trigger(canonical_signal).next_action_types == ("local_reasoning",)


def test_stage3_index_lifecycle_and_searches_use_public_apis_only() -> None:
    canonical_signal = CanonicalSignal(
        normalized_signal_id="norm_123",
        normalized_type="plain_text",
        source_kind="document_upload",
        extracted_text="Status update from Acme on 2026-03-20.",
        modality_metadata={"detected_modality": "plain_text"},
        timestamps={"received_at": "2026-03-20T10:00:00Z"},
        provenance_notes=("imported",),
        confidence=1.0,
        entity_candidates=("Acme",),
        alias_candidates=("Acme", "ACME"),
        ambiguity_markers=(),
        coarse_intent="general_request",
        activation_hints=("general_request",),
    )
    indexed_artifact = build_indexed_artifact(canonical_signal, issue_ids=("iss_1",))
    index_artifact(indexed_artifact, canonical_signal)

    assert search_text("status update") == [indexed_artifact.artifact_id]
    assert list_artifacts_by_source_kind("document_upload") == [indexed_artifact.artifact_id]
    assert list_artifacts_linked_to_issue("iss_1") == [indexed_artifact.artifact_id]
    assert search_by_entity_alias("acme") == [indexed_artifact.artifact_id]
    assert search_by_time_window("2026-03-20T00:00:00Z", "2026-03-21T00:00:00Z") == [indexed_artifact.artifact_id]

    exported_records = export_artifact_index_records()
    reset_artifact_index()
    assert search_text("status update") == []
    load_artifact_index_records(exported_records)
    assert get_artifact_by_id(indexed_artifact.artifact_id).artifact_id == indexed_artifact.artifact_id


def test_stage3_index_replay_rejects_malformed_records() -> None:
    with pytest.raises(ValueError):
        load_artifact_index_records(
            [
                {
                    "artifact_id": "idx_bad",
                    "artifact_kind": "normalized_signal",
                    "source_kind": "document_upload",
                    "extracted_text": "missing normalized signal id",
                    "issue_ids": (),
                    "entity_aliases": (),
                    "timestamp_values": ("2026-03-20T10:00:00Z",),
                    "provenance_notes": (),
                    "created_at": "2026-03-20T10:00:00Z",
                    "metadata": {},
                }
            ]
        )


def test_stage3_index_replay_rejects_duplicate_artifact_ids() -> None:
    duplicate_record = {
        "artifact_id": "idx_duplicate",
        "artifact_kind": "normalized_signal",
        "normalized_signal_id": "norm_duplicate",
        "source_kind": "document_upload",
        "extracted_text": "duplicate artifact identifier",
        "issue_ids": (),
        "entity_aliases": (),
        "timestamp_values": ("2026-03-20T10:00:00Z",),
        "provenance_notes": (),
        "created_at": "2026-03-20T10:00:00Z",
        "metadata": {},
    }

    with pytest.raises(ValueError):
        load_artifact_index_records([duplicate_record, dict(duplicate_record)])


def test_stage3_invalid_raw_input_is_rejected() -> None:
    with pytest.raises(ValueError):
        ingest_text_signal("   ", {"source_kind": "user_input"})

    with pytest.raises(ValueError):
        ingest_structured_signal({}, {"source_kind": "api"})


def test_stage3_invalid_canonicalization_input_is_rejected() -> None:
    with pytest.raises(ValueError):
        normalize_signal("not_a_raw_signal")  # type: ignore[arg-type]

    raw_signal = ingest_structured_signal({"record_id": "1"}, {"source_kind": "api"})
    assert extract_text_if_available(raw_signal) is None
    normalized_signal = normalize_signal(raw_signal)
    assert normalized_signal.ambiguity_markers == ("missing_text",)

    with pytest.raises(ValueError):
        canonicalize_text_payload(raw_signal)


def test_stage3_indexing_rejects_invalid_or_incomplete_canonicalized_payloads() -> None:
    incomplete_signal = CanonicalSignal(
        normalized_signal_id="norm_incomplete",
        normalized_type="structured_record",
        source_kind="api",
        extracted_text=None,
        modality_metadata={"detected_modality": "structured_record"},
        timestamps={"received_at": "2026-03-20T10:00:00Z"},
        provenance_notes=(),
        confidence=0.0,
        ambiguity_markers=("missing_text",),
        coarse_intent=None,
        activation_hints=(),
    )
    with pytest.raises(ValueError):
        build_indexed_artifact(incomplete_signal)

    with pytest.raises(ValueError):
        index_artifact("not_an_artifact")  # type: ignore[arg-type]


def test_stage3_activation_rejects_invalid_inputs() -> None:
    canonical_signal = canonicalize_text_payload(
        ingest_text_signal("General summary for activation.", {"source_kind": "user_input"})
    )
    trigger = build_activation_trigger(canonical_signal)

    with pytest.raises(ValueError):
        activate_workflow(canonical_signal, (), trigger)

    with pytest.raises(ValueError):
        activate_workflow(canonical_signal, ("idx_123",), "bad_trigger")  # type: ignore[arg-type]


def test_stage3_egress_rejects_invalid_emission_input() -> None:
    with pytest.raises(ValueError):
        emit_workflow_status(
            EmissionInput(
                artifact_ids=(),
                provenance_notes=("cli_request",),
                payload={"message": "bad"},
            )
        )

    with pytest.raises(ValueError):
        emit_workflow_status(
            EmissionInput(
                artifact_ids=("idx_123",),
                provenance_notes=("cli_request",),
                payload={},
            )
        )


def test_stage2_route_request_contract_can_feed_stage3_information_plane() -> None:
    route_request = RouteRequest(
        task_type="general_reasoning",
        prompt="Fix the broken deployment checklist before release.",
    )
    raw_signal = ingest_text_signal(route_request.prompt, {"source_kind": "stage2_route_request"})
    canonical_signal = normalize_signal(raw_signal)
    indexed_artifact = build_indexed_artifact(canonical_signal)
    index_artifact(indexed_artifact, canonical_signal)
    activation_output = activate_workflow(
        canonical_signal,
        (indexed_artifact.artifact_id,),
        build_activation_trigger(canonical_signal),
    )

    assert route_request.task_type == "general_reasoning"
    assert canonical_signal.source_kind == "stage2_route_request"
    assert activation_output.candidate_workflow_mode == "fix_flow"
    assert activation_output.related_artifact_ids == (indexed_artifact.artifact_id,)

    negative_boundary_request = RouteRequest(task_type="general_reasoning", prompt="   ")
    with pytest.raises(ValueError):
        ingest_text_signal(negative_boundary_request.prompt, {"source_kind": "stage2_route_request"})


def test_stage3_activation_output_can_feed_stage2_routing_without_raw_text_bypass() -> None:
    raw_signal = ingest_text_signal(
        "Fix the failing deployment checklist before tonight's release.",
        {"source_kind": "stage3_forward_boundary"},
    )
    canonical_signal = normalize_signal(raw_signal)
    indexed_artifact = build_indexed_artifact(canonical_signal)
    index_artifact(indexed_artifact, canonical_signal)
    activation_output = activate_workflow(
        canonical_signal,
        (indexed_artifact.artifact_id,),
        build_activation_trigger(canonical_signal),
    )

    stage2_request = RouteRequest(task_type=activation_output.next_action_types[0])
    route_decision = route_request(stage2_request)

    assert activation_output.candidate_workflow_mode == "fix_flow"
    assert activation_output.next_action_types == ("local_reasoning",)
    assert route_decision.status == "success"
    assert route_decision.task_type == "local_reasoning"
    assert route_decision.selected_path == "local_reasoning"

    with pytest.raises(ValueError):
        route_request(RouteRequest(task_type=activation_output.candidate_workflow_mode))


def test_stage3_document_ingestion_marks_uncertain_extraction_when_applicable() -> None:
    raw_signal = ingest_document_signal(
        "Screenshot placeholder for incident panel",
        {"source_kind": "upload", "document_kind": "screenshot"},
    )

    assert raw_signal.detected_modality == "screenshot_placeholder"
    assert raw_signal.extraction_status == "uncertain"
    assert normalize_signal(raw_signal).confidence == 0.5


def test_stage3_structured_signal_ingestion_preserves_serializable_fields() -> None:
    raw_signal = ingest_structured_signal(
        {"record_id": "abc", "content": "Repository note for normalization."},
        {"source_kind": "repository_scan"},
    )
    canonical_signal = normalize_signal(raw_signal)

    assert isinstance(raw_signal, RawSignal)
    assert raw_signal.detected_modality == "structured_record"
    assert canonical_signal.extracted_text == "Repository note for normalization."
    assert canonical_signal.source_kind == "repository_scan"
