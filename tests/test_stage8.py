"""Stage 8 acceptance mapping for the bounded observability/replay slice.

Requirement mapping:
- FX-R015: important runs are reconstructible from typed events, artifacts, issues, and snapshots through replay-safe lifecycle behavior

Acceptance scenarios:
- Scenario A: bounded golden-path workflow run can be reconstructed from structured records
- Scenario B: artifact, issue, event, and snapshot linkage is preserved through replay
- Scenario C: export -> reset -> load -> replay round trip is proven through public lifecycle APIs
- Scenario D: malformed, duplicate, or inconsistent replay inputs are rejected
- Scenario E: full-system replay evidence is bounded, typed, and audit-safe
"""

from __future__ import annotations

import pytest

from gdc_adk.adapters.adk.replay_envelope import build_replay_reference_envelope
from gdc_adk.memory.continuity import create_snapshot, load_snapshots, reset_continuity_store
from gdc_adk.memory.contracts import ContinuitySnapshot
from gdc_adk.substrate.artifact_store import export_artifact_records, load_artifact_records, reset_artifact_store
from gdc_adk.substrate.dispatch_system import (
    ReplayEvidenceBundle,
    build_replay_evidence_bundle,
    dispatch_text_request,
    export_workflow_runs,
    load_workflow_runs,
    reconstruct_workflow_run,
    reset_workflow_runs,
    validate_replay_evidence_bundle,
)
from gdc_adk.substrate.event_spine import export_event_records, load_event_records, reset_events
from gdc_adk.substrate.issue_tracker import export_issue_records, load_issue_records, reset_issue_store
from gdc_adk.validation.validator import create_validation_finding
from gdc_adk.workflows.agent_contracts import AgentTraceRecord, Stage7ForwardEnvelope


def reset_stage8_state() -> None:
    reset_events()
    reset_artifact_store()
    reset_issue_store()
    reset_workflow_runs()
    reset_continuity_store()


@pytest.fixture(autouse=True)
def _reset_state_per_test() -> None:
    reset_stage8_state()


def _build_snapshot(workflow_run_id: str, artifact_ids: tuple[str, ...], issue_ids: tuple[str, ...]) -> ContinuitySnapshot:
    return ContinuitySnapshot(
        snapshot_id="snap_stage8",
        workflow_run_id=workflow_run_id,
        workflow_mode="fix_flow",
        current_state="classified",
        state_history=(
            {"state": "received", "timestamp": "2026-03-20T12:00:00Z"},
            {"state": "classified", "timestamp": "2026-03-20T12:00:01Z"},
        ),
        artifact_ids=artifact_ids,
        issue_ids=issue_ids,
        finding_ids=(),
        context_refs=("ctx_stage8",),
        pending_actions=("replay_review",),
        created_at="2026-03-20T12:00:02Z",
    )


def _build_stage7_forward_envelope(
    workflow_run_id: str,
    artifact_ids: tuple[str, ...],
    issue_ids: tuple[str, ...],
    finding_ids: tuple[str, ...],
) -> Stage7ForwardEnvelope:
    trace_record = AgentTraceRecord(
        workflow_run_id=workflow_run_id,
        handoff_id="handoff_stage8",
        from_role="planner",
        to_role="executor",
        action_type="handoff_completed",
        artifact_ids=artifact_ids,
        issue_ids=issue_ids,
        finding_ids=finding_ids,
        context_block_ids=("ctx_stage8",),
        continuity_snapshot_id="snap_stage8",
        delegation_depth=1,
        status="completed",
        recorded_at="2026-03-20T12:00:03Z",
    )
    return Stage7ForwardEnvelope(
        workflow_run_id=workflow_run_id,
        handoff_ids=("handoff_stage8",),
        completed_handoff_ids=("handoff_stage8",),
        artifact_ids=artifact_ids,
        issue_ids=issue_ids,
        finding_ids=finding_ids,
        continuity_snapshot_ids=("snap_stage8",),
        context_block_ids=("ctx_stage8",),
        trace_records=(trace_record,),
    )


def test_stage8_positive_reconstruction_path_and_linkage_preservation() -> None:
    result = dispatch_text_request("bug: weather output failed")
    workflow_run = result["workflow_run"]
    snapshot = _build_snapshot(
        workflow_run["workflow_run_id"],
        tuple(workflow_run["input_artifact_ids"]),
        tuple(workflow_run["issue_ids"]),
    )
    create_snapshot(snapshot)

    replay_bundle = build_replay_evidence_bundle(workflow_run["workflow_run_id"], snapshots=(snapshot,))
    reconstructed = reconstruct_workflow_run(replay_bundle)

    assert reconstructed.status == "reconstructed"
    assert reconstructed.workflow_run_id == workflow_run["workflow_run_id"]
    assert reconstructed.artifact_ids == tuple(workflow_run["input_artifact_ids"])
    assert reconstructed.issue_ids == tuple(workflow_run["issue_ids"])
    assert reconstructed.snapshot_ids == ("snap_stage8",)
    assert len(reconstructed.event_ids) == len(result["emitted_event_ids"])


def test_stage8_end_to_end_replay_proof_across_prior_stage_outputs() -> None:
    result = dispatch_text_request("bug: full replay across prior stage outputs")
    workflow_run = result["workflow_run"]
    artifact_ids = tuple(workflow_run["input_artifact_ids"])
    issue_ids = tuple(workflow_run["issue_ids"])
    finding = create_validation_finding(
        "quality_gap",
        "medium",
        "Replay must preserve finding linkage.",
        artifact_ids,
        {"workflow_run_id": workflow_run["workflow_run_id"]},
        "validator",
    )
    workflow_run["finding_ids"] = [finding.finding_id]
    snapshot = _build_snapshot(workflow_run["workflow_run_id"], artifact_ids, issue_ids)
    create_snapshot(snapshot)
    stage7_forward_envelope = _build_stage7_forward_envelope(workflow_run["workflow_run_id"], artifact_ids, issue_ids, (finding.finding_id,))
    replay_reference_envelope = build_replay_reference_envelope(stage7_forward_envelope, continuity_snapshot=snapshot)

    replay_bundle = build_replay_evidence_bundle(
        workflow_run["workflow_run_id"],
        findings=(finding,),
        snapshots=(snapshot,),
        replay_reference_envelopes=(replay_reference_envelope,),
    )
    reconstructed = reconstruct_workflow_run(replay_bundle)

    assert reconstructed.finding_ids == (finding.finding_id,)
    assert reconstructed.replay_reference_workflow_ids == (workflow_run["workflow_run_id"],)
    assert reconstructed.snapshot_ids == ("snap_stage8",)


def test_stage8_export_reset_load_and_replay_round_trip() -> None:
    result = dispatch_text_request("bug: dispatch replay me")
    workflow_run = result["workflow_run"]
    snapshot = _build_snapshot(
        workflow_run["workflow_run_id"],
        tuple(workflow_run["input_artifact_ids"]),
        tuple(workflow_run["issue_ids"]),
    )
    create_snapshot(snapshot)

    exported_events = export_event_records()
    exported_artifacts = export_artifact_records()
    exported_issues = export_issue_records()
    exported_workflows = export_workflow_runs()

    reset_stage8_state()

    load_event_records(exported_events)
    load_artifact_records(exported_artifacts)
    load_issue_records(exported_issues)
    load_workflow_runs(exported_workflows)
    load_snapshots((snapshot,))

    replay_bundle = build_replay_evidence_bundle(workflow_run["workflow_run_id"], snapshots=(snapshot,))
    reconstructed = reconstruct_workflow_run(replay_bundle)

    assert reconstructed.workflow_run_id == workflow_run["workflow_run_id"]
    assert reconstructed.snapshot_ids == ("snap_stage8",)
    assert set(reconstructed.event_ids) == {event["event_id"] for event in exported_events if event["workflow_run_id"] == workflow_run["workflow_run_id"]}


def test_stage8_malformed_replay_input_is_rejected() -> None:
    result = dispatch_text_request("bug: malformed replay")
    workflow_run = result["workflow_run"]
    artifact = export_artifact_records()[0]

    malformed_bundle = ReplayEvidenceBundle(
        workflow_run=workflow_run,
        events=(),
        artifacts=(artifact,),
        issues=(),
        snapshots=(),
    )

    try:
        validate_replay_evidence_bundle(malformed_bundle)
    except ValueError as exc:
        assert "at least one event" in str(exc)
    else:
        raise AssertionError("Expected malformed replay bundle to be rejected.")


def test_stage8_missing_required_snapshot_and_partial_replay_payload_are_rejected() -> None:
    result = dispatch_text_request("bug: partial replay should reject")
    workflow_run = result["workflow_run"]
    artifact = next(artifact for artifact in export_artifact_records() if artifact["workflow_run_id"] == workflow_run["workflow_run_id"])
    issue = next(issue for issue in export_issue_records() if issue["issue_id"] in workflow_run["issue_ids"])
    finding = create_validation_finding(
        "quality_gap",
        "medium",
        "Replay requires finding preservation.",
        (artifact["artifact_id"],),
        {"workflow_run_id": workflow_run["workflow_run_id"]},
        "validator",
    )
    workflow_run["finding_ids"] = [finding.finding_id]
    event = next(event for event in export_event_records() if event["workflow_run_id"] == workflow_run["workflow_run_id"])

    missing_snapshot_bundle = ReplayEvidenceBundle(
        workflow_run=workflow_run,
        events=(event,),
        artifacts=(artifact,),
        issues=(issue,),
        findings=(finding,),
        snapshots=(),
    )
    with pytest.raises(ValueError, match="at least one snapshot"):
        validate_replay_evidence_bundle(missing_snapshot_bundle)

    partial_payload_bundle = ReplayEvidenceBundle(
        workflow_run=workflow_run,
        events=(event,),
        artifacts=(artifact,),
        issues=(issue,),
        findings=(),
        snapshots=(_build_snapshot(workflow_run["workflow_run_id"], (artifact["artifact_id"],), (issue["issue_id"],)),),
    )
    with pytest.raises(ValueError, match="missing required findings"):
        validate_replay_evidence_bundle(partial_payload_bundle)


def test_stage8_duplicate_and_inconsistent_replay_inputs_are_rejected() -> None:
    result = dispatch_text_request("bug: inconsistent replay")
    workflow_run = result["workflow_run"]
    event = next(event for event in export_event_records() if event["workflow_run_id"] == workflow_run["workflow_run_id"])
    artifact = next(artifact for artifact in export_artifact_records() if artifact["workflow_run_id"] == workflow_run["workflow_run_id"])
    issue = next(issue for issue in export_issue_records() if issue["issue_id"] in workflow_run["issue_ids"])

    duplicate_event_bundle = ReplayEvidenceBundle(
        workflow_run=workflow_run,
        events=(event, dict(event)),
        artifacts=(artifact,),
        issues=(issue,),
        snapshots=(),
    )
    try:
        validate_replay_evidence_bundle(duplicate_event_bundle)
    except ValueError as exc:
        assert "Duplicate event_id" in str(exc)
    else:
        raise AssertionError("Expected duplicate event replay bundle to be rejected.")

    inconsistent_snapshot = _build_snapshot("wr_other", (artifact["artifact_id"],), (issue["issue_id"],))
    inconsistent_bundle = ReplayEvidenceBundle(
        workflow_run=workflow_run,
        events=(event,),
        artifacts=(artifact,),
        issues=(issue,),
        snapshots=(inconsistent_snapshot,),
    )
    try:
        validate_replay_evidence_bundle(inconsistent_bundle)
    except ValueError as exc:
        assert "different workflow_run_id" in str(exc)
    else:
        raise AssertionError("Expected inconsistent snapshot replay bundle to be rejected.")
