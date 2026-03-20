from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


HANDOFF_STATUSES: frozenset[str] = frozenset({"pending", "accepted", "rejected", "completed"})


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _normalize_identifiers(values: tuple[str, ...] | list[str] | None, field_name: str) -> tuple[str, ...]:
    if values is None:
        return ()
    normalized = tuple(str(value) for value in values)
    if any(not value.strip() for value in normalized):
        raise ValueError(f"{field_name} must contain only non-empty identifiers.")
    return normalized


def _normalize_actions(values: tuple[str, ...] | list[str], field_name: str) -> tuple[str, ...]:
    normalized = tuple(str(value) for value in values)
    if not normalized:
        raise ValueError(f"{field_name} must contain at least one action.")
    if any(not value.strip() for value in normalized):
        raise ValueError(f"{field_name} must contain only non-empty action names.")
    return normalized


@dataclass(frozen=True)
class HandoffArtifact:
    handoff_id: str
    workflow_run_id: str
    from_role: str
    to_role: str
    artifact_ids: tuple[str, ...]
    issue_ids: tuple[str, ...]
    finding_ids: tuple[str, ...]
    context_block_ids: tuple[str, ...]
    continuity_snapshot_id: str | None
    created_at: str
    handoff_reason: str
    requested_actions: tuple[str, ...]
    pending_actions: tuple[str, ...] = ()
    review_required: bool = False
    validation_required: bool = True
    delegation_depth: int = 0
    status: str = "pending"


@dataclass(frozen=True)
class AgentTraceRecord:
    workflow_run_id: str
    handoff_id: str
    from_role: str
    to_role: str
    action_type: str
    artifact_ids: tuple[str, ...]
    issue_ids: tuple[str, ...]
    finding_ids: tuple[str, ...]
    context_block_ids: tuple[str, ...]
    continuity_snapshot_id: str | None
    delegation_depth: int
    status: str
    recorded_at: str


@dataclass(frozen=True)
class CoordinationEnvelope:
    coordination_envelope_id: str
    workflow_run_id: str
    root_handoff_id: str
    active_handoff_ids: tuple[str, ...]
    completed_handoff_ids: tuple[str, ...]
    rejected_handoff_ids: tuple[str, ...]
    trace_records: tuple[AgentTraceRecord, ...]
    created_at: str
    updated_at: str


@dataclass(frozen=True)
class HandoffValidationResult:
    handoff_id: str
    status: str
    is_valid: bool
    violations: tuple[str, ...] = ()
    message: str = ""


@dataclass(frozen=True)
class GovernanceCheckResult:
    status: str
    blocked: bool
    violations: tuple[str, ...] = ()
    message: str = ""


@dataclass(frozen=True)
class HandoffLifecycleResult:
    status: str
    handoff: HandoffArtifact | None = None
    coordination_envelope: CoordinationEnvelope | None = None
    trace_record: AgentTraceRecord | None = None
    owner_role: str | None = None
    pending_actions: tuple[str, ...] = ()
    message: str = ""


@dataclass(frozen=True)
class DelegationResult:
    status: str
    handoff: HandoffArtifact | None = None
    coordination_envelope: CoordinationEnvelope | None = None
    governance_result: GovernanceCheckResult | None = None
    validation_result: HandoffValidationResult | None = None
    message: str = ""


@dataclass(frozen=True)
class Stage7ForwardEnvelope:
    workflow_run_id: str
    handoff_ids: tuple[str, ...]
    completed_handoff_ids: tuple[str, ...]
    artifact_ids: tuple[str, ...]
    issue_ids: tuple[str, ...]
    finding_ids: tuple[str, ...]
    continuity_snapshot_ids: tuple[str, ...]
    context_block_ids: tuple[str, ...]
    trace_records: tuple[AgentTraceRecord, ...] = ()


@dataclass(frozen=True)
class HandoffExportResult:
    handoffs: tuple[HandoffArtifact, ...] = ()


@dataclass(frozen=True)
class CoordinationExportResult:
    coordination_envelopes: tuple[CoordinationEnvelope, ...] = ()


def create_handoff_artifact(
    workflow_run_id: str,
    from_role: str,
    to_role: str,
    handoff_reason: str,
    requested_actions: tuple[str, ...] | list[str],
    artifact_ids: tuple[str, ...] | list[str] | None = None,
    issue_ids: tuple[str, ...] | list[str] | None = None,
    finding_ids: tuple[str, ...] | list[str] | None = None,
    context_block_ids: tuple[str, ...] | list[str] | None = None,
    continuity_snapshot_id: str | None = None,
    review_required: bool = False,
    validation_required: bool = True,
    delegation_depth: int = 0,
    handoff_id: str | None = None,
    created_at: str | None = None,
) -> HandoffArtifact:
    artifact = HandoffArtifact(
        handoff_id=handoff_id or f"handoff_{uuid4().hex[:12]}",
        workflow_run_id=str(workflow_run_id).strip(),
        from_role=str(from_role).strip(),
        to_role=str(to_role).strip(),
        artifact_ids=_normalize_identifiers(artifact_ids, "artifact_ids"),
        issue_ids=_normalize_identifiers(issue_ids, "issue_ids"),
        finding_ids=_normalize_identifiers(finding_ids, "finding_ids"),
        context_block_ids=_normalize_identifiers(context_block_ids, "context_block_ids"),
        continuity_snapshot_id=None if continuity_snapshot_id is None else str(continuity_snapshot_id).strip(),
        created_at=created_at or _utc_now(),
        handoff_reason=str(handoff_reason).strip(),
        requested_actions=_normalize_actions(requested_actions, "requested_actions"),
        review_required=bool(review_required),
        validation_required=bool(validation_required),
        delegation_depth=int(delegation_depth),
    )
    validate_handoff_contract(artifact)
    return artifact


def validate_handoff_contract(handoff_artifact: HandoffArtifact) -> None:
    if not isinstance(handoff_artifact, HandoffArtifact):
        raise ValueError("handoff_artifact must be a HandoffArtifact.")
    if not handoff_artifact.handoff_id.strip():
        raise ValueError("handoff_id must be non-empty.")
    if not handoff_artifact.workflow_run_id.strip():
        raise ValueError("workflow_run_id must be non-empty.")
    if not handoff_artifact.from_role.strip() or not handoff_artifact.to_role.strip():
        raise ValueError("from_role and to_role must be non-empty.")
    if not handoff_artifact.handoff_reason.strip():
        raise ValueError("handoff_reason must be non-empty.")
    if handoff_artifact.status not in HANDOFF_STATUSES:
        raise ValueError(f"Unsupported handoff status: {handoff_artifact.status}")
    if handoff_artifact.delegation_depth < 0:
        raise ValueError("delegation_depth must be zero or greater.")
    if not handoff_artifact.created_at.strip():
        raise ValueError("created_at must be non-empty.")
    if not (
        handoff_artifact.artifact_ids
        or handoff_artifact.issue_ids
        or handoff_artifact.finding_ids
        or handoff_artifact.context_block_ids
        or handoff_artifact.continuity_snapshot_id
    ):
        raise ValueError("handoff_artifact must carry at least one durable coordination reference.")
    if handoff_artifact.review_required and handoff_artifact.from_role == handoff_artifact.to_role:
        raise ValueError("review-required handoffs must preserve role independence.")


def create_agent_trace_record(handoff_artifact: HandoffArtifact, action_type: str, status: str) -> AgentTraceRecord:
    validate_handoff_contract(handoff_artifact)
    if not isinstance(action_type, str) or not action_type.strip():
        raise ValueError("action_type must be a non-empty string.")
    if not isinstance(status, str) or not status.strip():
        raise ValueError("status must be a non-empty string.")
    return AgentTraceRecord(
        workflow_run_id=handoff_artifact.workflow_run_id,
        handoff_id=handoff_artifact.handoff_id,
        from_role=handoff_artifact.from_role,
        to_role=handoff_artifact.to_role,
        action_type=action_type,
        artifact_ids=handoff_artifact.artifact_ids,
        issue_ids=handoff_artifact.issue_ids,
        finding_ids=handoff_artifact.finding_ids,
        context_block_ids=handoff_artifact.context_block_ids,
        continuity_snapshot_id=handoff_artifact.continuity_snapshot_id,
        delegation_depth=handoff_artifact.delegation_depth,
        status=status,
        recorded_at=_utc_now(),
    )


def build_stage7_forward_envelope(
    workflow_run_id: str,
    handoffs: tuple[HandoffArtifact, ...],
    coordination_envelope: CoordinationEnvelope,
) -> Stage7ForwardEnvelope:
    if not isinstance(workflow_run_id, str) or not workflow_run_id.strip():
        raise ValueError("workflow_run_id must be a non-empty string.")
    if not isinstance(coordination_envelope, CoordinationEnvelope):
        raise ValueError("coordination_envelope must be a CoordinationEnvelope.")
    handoff_tuple = tuple(handoffs)
    for handoff in handoff_tuple:
        validate_handoff_contract(handoff)
        if handoff.workflow_run_id != workflow_run_id:
            raise ValueError("All handoffs must belong to the same workflow_run_id.")
    artifact_ids = tuple(sorted({artifact_id for handoff in handoff_tuple for artifact_id in handoff.artifact_ids}))
    issue_ids = tuple(sorted({issue_id for handoff in handoff_tuple for issue_id in handoff.issue_ids}))
    finding_ids = tuple(sorted({finding_id for handoff in handoff_tuple for finding_id in handoff.finding_ids}))
    continuity_snapshot_ids = tuple(
        sorted({handoff.continuity_snapshot_id for handoff in handoff_tuple if handoff.continuity_snapshot_id is not None})
    )
    context_block_ids = tuple(
        sorted({context_block_id for handoff in handoff_tuple for context_block_id in handoff.context_block_ids})
    )
    return Stage7ForwardEnvelope(
        workflow_run_id=workflow_run_id,
        handoff_ids=tuple(handoff.handoff_id for handoff in handoff_tuple),
        completed_handoff_ids=coordination_envelope.completed_handoff_ids,
        artifact_ids=artifact_ids,
        issue_ids=issue_ids,
        finding_ids=finding_ids,
        continuity_snapshot_ids=continuity_snapshot_ids,
        context_block_ids=context_block_ids,
        trace_records=coordination_envelope.trace_records,
    )


def serialize_handoff_artifact(handoff_artifact: HandoffArtifact) -> dict[str, Any]:
    validate_handoff_contract(handoff_artifact)
    return asdict(handoff_artifact)


def serialize_coordination_envelope(coordination_envelope: CoordinationEnvelope) -> dict[str, Any]:
    if not isinstance(coordination_envelope, CoordinationEnvelope):
        raise ValueError("coordination_envelope must be a CoordinationEnvelope.")
    return asdict(coordination_envelope)


def serialize_stage7_forward_envelope(stage7_forward_envelope: Stage7ForwardEnvelope) -> dict[str, Any]:
    if not isinstance(stage7_forward_envelope, Stage7ForwardEnvelope):
        raise ValueError("stage7_forward_envelope must be a Stage7ForwardEnvelope.")
    return asdict(stage7_forward_envelope)
