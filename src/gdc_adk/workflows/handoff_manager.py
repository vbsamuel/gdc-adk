from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

from gdc_adk.validation.handoff_validator import (
    validate_handoff_artifacts,
    validate_review_requirements,
    validate_traceability_links,
)
from gdc_adk.workflows.agent_contracts import (
    AgentTraceRecord,
    CoordinationEnvelope,
    CoordinationExportResult,
    HandoffArtifact,
    HandoffExportResult,
    HandoffLifecycleResult,
    create_agent_trace_record,
    validate_handoff_contract,
)
from gdc_adk.workflows.state_machine import WorkflowRun


_HANDOFFS: dict[str, HandoffArtifact] = {}
_ENVELOPES: dict[str, CoordinationEnvelope] = {}


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _require_workflow_run(workflow_run: WorkflowRun) -> WorkflowRun:
    if not isinstance(workflow_run, WorkflowRun):
        raise ValueError("workflow_run must be a WorkflowRun.")
    return workflow_run


def _get_envelope(workflow_run_id: str, root_handoff_id: str) -> CoordinationEnvelope:
    envelope = _ENVELOPES.get(workflow_run_id)
    if envelope is not None:
        return envelope
    created_at = _utc_now()
    envelope = CoordinationEnvelope(
        coordination_envelope_id=f"coord_{workflow_run_id}",
        workflow_run_id=workflow_run_id,
        root_handoff_id=root_handoff_id,
        active_handoff_ids=(),
        completed_handoff_ids=(),
        rejected_handoff_ids=(),
        trace_records=(),
        created_at=created_at,
        updated_at=created_at,
    )
    _ENVELOPES[workflow_run_id] = envelope
    return envelope


def _append_trace(envelope: CoordinationEnvelope, trace_record: AgentTraceRecord) -> CoordinationEnvelope:
    return replace(
        envelope,
        trace_records=envelope.trace_records + (trace_record,),
        updated_at=_utc_now(),
    )


def initiate_handoff(handoff_artifact: HandoffArtifact, workflow_run: WorkflowRun) -> HandoffLifecycleResult:
    run = _require_workflow_run(workflow_run)
    validate_handoff_contract(handoff_artifact)
    if handoff_artifact.handoff_id in _HANDOFFS:
        raise ValueError(f"handoff_id already exists: {handoff_artifact.handoff_id}")

    artifact_validation = validate_handoff_artifacts(handoff_artifact)
    traceability_validation = validate_traceability_links(handoff_artifact, run)
    review_validation = validate_review_requirements(handoff_artifact, run)

    if not artifact_validation.is_valid:
        raise ValueError(artifact_validation.message)
    if not traceability_validation.is_valid:
        raise ValueError(traceability_validation.message)
    if not review_validation.is_valid:
        raise ValueError(review_validation.message)

    accepted_handoff = replace(handoff_artifact, status="accepted")
    _HANDOFFS[accepted_handoff.handoff_id] = accepted_handoff
    envelope = _get_envelope(run.workflow_run_id, accepted_handoff.handoff_id)
    active_handoff_ids = envelope.active_handoff_ids + (accepted_handoff.handoff_id,)
    trace_record = create_agent_trace_record(accepted_handoff, "handoff_initiated", "accepted")
    updated_envelope = _append_trace(replace(envelope, active_handoff_ids=active_handoff_ids), trace_record)
    _ENVELOPES[run.workflow_run_id] = updated_envelope
    return HandoffLifecycleResult(
        status="initiated",
        handoff=accepted_handoff,
        coordination_envelope=updated_envelope,
        trace_record=trace_record,
        owner_role=accepted_handoff.to_role,
        pending_actions=accepted_handoff.requested_actions,
        message="Handoff initiated through typed coordination contract.",
    )

def complete_handoff(handoff_id: str, workflow_run: WorkflowRun) -> HandoffLifecycleResult:
    run = _require_workflow_run(workflow_run)
    handoff = get_handoff(handoff_id)
    if handoff is None:
        raise ValueError(f"Unknown handoff_id: {handoff_id}")
    artifact_validation = validate_handoff_artifacts(handoff)
    traceability_validation = validate_traceability_links(handoff, run)
    review_validation = validate_review_requirements(handoff, run)
    if not (artifact_validation.is_valid and traceability_validation.is_valid and review_validation.is_valid):
        trace_record = create_agent_trace_record(handoff, "handoff_blocked", "blocked")
        envelope = _append_trace(_get_envelope(run.workflow_run_id, handoff.handoff_id), trace_record)
        _ENVELOPES[run.workflow_run_id] = envelope
        return HandoffLifecycleResult(
            status="blocked",
            handoff=handoff,
            coordination_envelope=envelope,
            trace_record=trace_record,
            owner_role=handoff.from_role,
            pending_actions=handoff.requested_actions,
            message="Handoff blocked by review or validation requirements.",
        )

    completed_handoff = replace(handoff, status="completed", pending_actions=handoff.requested_actions)
    _HANDOFFS[handoff_id] = completed_handoff
    envelope = _get_envelope(run.workflow_run_id, handoff.handoff_id)
    active_handoff_ids = tuple(item for item in envelope.active_handoff_ids if item != handoff_id)
    completed_handoff_ids = envelope.completed_handoff_ids + (handoff_id,)
    trace_record = create_agent_trace_record(completed_handoff, "handoff_completed", "completed")
    updated_envelope = _append_trace(
        replace(
            envelope,
            active_handoff_ids=active_handoff_ids,
            completed_handoff_ids=completed_handoff_ids,
        ),
        trace_record,
    )
    _ENVELOPES[run.workflow_run_id] = updated_envelope
    return HandoffLifecycleResult(
        status="completed",
        handoff=completed_handoff,
        coordination_envelope=updated_envelope,
        trace_record=trace_record,
        owner_role=completed_handoff.to_role,
        pending_actions=completed_handoff.pending_actions,
        message="Handoff completed with validated lineage.",
    )


def reject_handoff(handoff_id: str, workflow_run: WorkflowRun, reason: str) -> HandoffLifecycleResult:
    run = _require_workflow_run(workflow_run)
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("reason must be a non-empty string.")
    handoff = get_handoff(handoff_id)
    if handoff is None:
        raise ValueError(f"Unknown handoff_id: {handoff_id}")
    rejected_handoff = replace(handoff, status="rejected")
    _HANDOFFS[handoff_id] = rejected_handoff
    envelope = _get_envelope(run.workflow_run_id, handoff.handoff_id)
    active_handoff_ids = tuple(item for item in envelope.active_handoff_ids if item != handoff_id)
    rejected_handoff_ids = envelope.rejected_handoff_ids + (handoff_id,)
    trace_record = create_agent_trace_record(rejected_handoff, "handoff_rejected", "rejected")
    updated_envelope = _append_trace(
        replace(
            envelope,
            active_handoff_ids=active_handoff_ids,
            rejected_handoff_ids=rejected_handoff_ids,
        ),
        trace_record,
    )
    _ENVELOPES[run.workflow_run_id] = updated_envelope
    return HandoffLifecycleResult(
        status="rejected",
        handoff=rejected_handoff,
        coordination_envelope=updated_envelope,
        trace_record=trace_record,
        owner_role=rejected_handoff.from_role,
        pending_actions=(),
        message=reason,
    )


def get_handoff(handoff_id: str) -> HandoffArtifact | None:
    if not isinstance(handoff_id, str) or not handoff_id.strip():
        raise ValueError("handoff_id must be a non-empty string.")
    return _HANDOFFS.get(handoff_id)


def get_coordination_envelope(workflow_run_id: str) -> CoordinationEnvelope | None:
    if not isinstance(workflow_run_id, str) or not workflow_run_id.strip():
        raise ValueError("workflow_run_id must be a non-empty string.")
    return _ENVELOPES.get(workflow_run_id)


def export_handoffs() -> HandoffExportResult:
    return HandoffExportResult(handoffs=tuple(_HANDOFFS.values()))


def export_coordination_envelopes() -> CoordinationExportResult:
    return CoordinationExportResult(coordination_envelopes=tuple(_ENVELOPES.values()))


def reset_handoff_manager() -> None:
    _HANDOFFS.clear()
    _ENVELOPES.clear()


def load_handoffs(records: tuple[HandoffArtifact, ...] | list[HandoffArtifact]) -> None:
    reset_handoff_manager()
    for record in tuple(records):
        validate_handoff_contract(record)
        if record.handoff_id in _HANDOFFS:
            raise ValueError(f"Duplicate handoff_id during load: {record.handoff_id}")
        _HANDOFFS[record.handoff_id] = record


def load_coordination_envelopes(records: tuple[CoordinationEnvelope, ...] | list[CoordinationEnvelope]) -> None:
    for record in tuple(records):
        if not isinstance(record, CoordinationEnvelope):
            raise ValueError("All coordination envelope records must be CoordinationEnvelope instances.")
        if record.workflow_run_id in _ENVELOPES:
            raise ValueError(f"Duplicate workflow_run_id during load: {record.workflow_run_id}")
        _ENVELOPES[record.workflow_run_id] = record
