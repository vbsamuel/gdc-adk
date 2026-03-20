from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from gdc_adk.memory.contracts import ContinuitySnapshot, ReplayPackage
from gdc_adk.workflows.agent_contracts import Stage7ForwardEnvelope


@dataclass(frozen=True)
class ReplayReferenceEnvelope:
    workflow_run_id: str
    handoff_ids: tuple[str, ...] = ()
    continuity_snapshot_ids: tuple[str, ...] = ()
    context_block_ids: tuple[str, ...] = ()
    replay_package_id: str | None = None
    finding_ids: tuple[str, ...] = ()
    issue_ids: tuple[str, ...] = ()


def _validate_identifier_tuple(values: tuple[str, ...], field_name: str) -> None:
    if not isinstance(values, tuple):
        raise ValueError(f"{field_name} must be a tuple.")
    for value in values:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must contain only non-empty identifiers.")


def validate_replay_reference_envelope(replay_reference_envelope: ReplayReferenceEnvelope) -> None:
    if not isinstance(replay_reference_envelope, ReplayReferenceEnvelope):
        raise ValueError("replay_reference_envelope must be a ReplayReferenceEnvelope.")

    if not isinstance(replay_reference_envelope.workflow_run_id, str) or not replay_reference_envelope.workflow_run_id.strip():
        raise ValueError("workflow_run_id must be non-empty.")

    _validate_identifier_tuple(replay_reference_envelope.handoff_ids, "handoff_ids")
    _validate_identifier_tuple(replay_reference_envelope.continuity_snapshot_ids, "continuity_snapshot_ids")
    _validate_identifier_tuple(replay_reference_envelope.context_block_ids, "context_block_ids")
    _validate_identifier_tuple(replay_reference_envelope.finding_ids, "finding_ids")
    _validate_identifier_tuple(replay_reference_envelope.issue_ids, "issue_ids")

    if replay_reference_envelope.replay_package_id is not None:
        if (
            not isinstance(replay_reference_envelope.replay_package_id, str)
            or not replay_reference_envelope.replay_package_id.strip()
        ):
            raise ValueError("replay_package_id must be non-empty when provided.")


def build_replay_reference_envelope(
    stage7_forward_envelope: Stage7ForwardEnvelope,
    replay_package: ReplayPackage | None = None,
    continuity_snapshot: ContinuitySnapshot | None = None,
) -> ReplayReferenceEnvelope:
    if not isinstance(stage7_forward_envelope, Stage7ForwardEnvelope):
        raise ValueError("stage7_forward_envelope must be a Stage7ForwardEnvelope.")

    continuity_snapshot_ids = tuple(stage7_forward_envelope.continuity_snapshot_ids)

    if continuity_snapshot is not None:
        if not isinstance(continuity_snapshot, ContinuitySnapshot):
            raise ValueError("continuity_snapshot must be a ContinuitySnapshot.")
        continuity_snapshot_ids = tuple(
            dict.fromkeys(continuity_snapshot_ids + (continuity_snapshot.snapshot_id,))
        )

    envelope = ReplayReferenceEnvelope(
        workflow_run_id=stage7_forward_envelope.workflow_run_id,
        handoff_ids=tuple(stage7_forward_envelope.handoff_ids),
        continuity_snapshot_ids=continuity_snapshot_ids,
        context_block_ids=tuple(stage7_forward_envelope.context_block_ids),
        replay_package_id=None if replay_package is None else replay_package.replay_package_id,
        finding_ids=tuple(stage7_forward_envelope.finding_ids),
        issue_ids=tuple(stage7_forward_envelope.issue_ids),
    )
    validate_replay_reference_envelope(envelope)
    return envelope


def serialize_replay_reference_envelope(replay_reference_envelope: ReplayReferenceEnvelope) -> dict[str, Any]:
    validate_replay_reference_envelope(replay_reference_envelope)
    return asdict(replay_reference_envelope)


def deserialize_replay_reference_envelope(payload: dict[str, Any]) -> ReplayReferenceEnvelope:
    if not isinstance(payload, dict):
        raise ValueError("payload must be a dict.")

    envelope = ReplayReferenceEnvelope(
        workflow_run_id=str(payload.get("workflow_run_id", "")).strip(),
        handoff_ids=tuple(str(value).strip() for value in payload.get("handoff_ids", ())),
        continuity_snapshot_ids=tuple(str(value).strip() for value in payload.get("continuity_snapshot_ids", ())),
        context_block_ids=tuple(str(value).strip() for value in payload.get("context_block_ids", ())),
        replay_package_id=(
            None
            if payload.get("replay_package_id") is None
            else str(payload.get("replay_package_id")).strip()
        ),
        finding_ids=tuple(str(value).strip() for value in payload.get("finding_ids", ())),
        issue_ids=tuple(str(value).strip() for value in payload.get("issue_ids", ())),
    )
    validate_replay_reference_envelope(envelope)
    return envelope