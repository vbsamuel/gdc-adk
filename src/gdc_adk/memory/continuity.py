from __future__ import annotations

from typing import Iterable

from gdc_adk.memory.contracts import (
    ContinuityExportResult,
    ContinuitySnapshot,
    ContinuityStoreResult,
    RehydrationResult,
)


_SNAPSHOTS: dict[str, ContinuitySnapshot] = {}


def create_snapshot(snapshot_payload: ContinuitySnapshot) -> ContinuityStoreResult:
    if not isinstance(snapshot_payload, ContinuitySnapshot):
        raise ValueError("snapshot_payload must be a ContinuitySnapshot.")
    if snapshot_payload.snapshot_id in _SNAPSHOTS:
        raise ValueError(f"snapshot_id already exists: {snapshot_payload.snapshot_id}")
    if not snapshot_payload.workflow_run_id.strip():
        raise ValueError("snapshot_payload.workflow_run_id must be non-empty.")
    _SNAPSHOTS[snapshot_payload.snapshot_id] = snapshot_payload
    return ContinuityStoreResult(status="stored", snapshot=snapshot_payload, message="Continuity snapshot stored.")


def get_snapshot(snapshot_id: str) -> ContinuityStoreResult | None:
    if not isinstance(snapshot_id, str) or not snapshot_id.strip():
        raise ValueError("snapshot_id must be a non-empty string.")
    snapshot = _SNAPSHOTS.get(snapshot_id)
    if snapshot is None:
        return None
    return ContinuityStoreResult(status="found", snapshot=snapshot, message="Continuity snapshot found.")


def list_snapshots_for_workflow(workflow_run_id: str) -> list[ContinuitySnapshot]:
    if not isinstance(workflow_run_id, str) or not workflow_run_id.strip():
        raise ValueError("workflow_run_id must be a non-empty string.")
    return [snapshot for snapshot in _SNAPSHOTS.values() if snapshot.workflow_run_id == workflow_run_id]


def export_snapshots(filter_spec: dict[str, object] | None = None) -> ContinuityExportResult:
    filter_spec = dict(filter_spec or {})
    workflow_run_id = filter_spec.get("workflow_run_id")
    records: list[ContinuitySnapshot] = []
    for snapshot in _SNAPSHOTS.values():
        if workflow_run_id is not None and snapshot.workflow_run_id != workflow_run_id:
            continue
        records.append(snapshot)
    return ContinuityExportResult(snapshots=tuple(records))


def mark_snapshot_superseded(snapshot_id: str, superseded_by_id: str) -> ContinuityStoreResult:
    if not isinstance(superseded_by_id, str) or not superseded_by_id.strip():
        raise ValueError("superseded_by_id must be a non-empty string.")
    result = get_snapshot(snapshot_id)
    if result is None or result.snapshot is None:
        raise ValueError(f"Unknown snapshot_id: {snapshot_id}")
    snapshot = result.snapshot
    updated_snapshot = ContinuitySnapshot(
        snapshot_id=snapshot.snapshot_id,
        workflow_run_id=snapshot.workflow_run_id,
        workflow_mode=snapshot.workflow_mode,
        current_state=snapshot.current_state,
        state_history=snapshot.state_history,
        artifact_ids=snapshot.artifact_ids,
        issue_ids=snapshot.issue_ids,
        finding_ids=snapshot.finding_ids,
        context_refs=snapshot.context_refs,
        pending_actions=snapshot.pending_actions,
        created_at=snapshot.created_at,
        completion_reason=snapshot.completion_reason,
        blocked_reason=snapshot.blocked_reason,
        superseded_by=superseded_by_id,
    )
    _SNAPSHOTS[snapshot_id] = updated_snapshot
    return ContinuityStoreResult(status="superseded", snapshot=updated_snapshot, message="Snapshot superseded.")


def rehydrate_snapshot(snapshot_or_id: str | ContinuitySnapshot) -> ContinuityStoreResult:
    if isinstance(snapshot_or_id, str):
        result = get_snapshot(snapshot_or_id)
        if result is None or result.snapshot is None:
            raise ValueError(f"Unknown snapshot_id: {snapshot_or_id}")
        snapshot = result.snapshot
    elif isinstance(snapshot_or_id, ContinuitySnapshot):
        snapshot = snapshot_or_id
    else:
        raise ValueError("snapshot_or_id must be a snapshot_id or ContinuitySnapshot.")

    missing_references: list[str] = []
    if not snapshot.context_refs:
        missing_references.append("context_refs")
    if not snapshot.state_history:
        missing_references.append("state_history")

    if missing_references:
        rehydration_result = RehydrationResult(
            rehydration_status="partial",
            snapshot=snapshot,
            missing_references=tuple(missing_references),
            message="Snapshot rehydrated partially with explicit missing references.",
        )
        return ContinuityStoreResult(status="rehydrated", snapshot=snapshot, rehydration_result=rehydration_result)

    rehydration_result = RehydrationResult(
        rehydration_status="success",
        snapshot=snapshot,
        message="Snapshot rehydrated successfully.",
    )
    return ContinuityStoreResult(status="rehydrated", snapshot=snapshot, rehydration_result=rehydration_result)


def reset_continuity_store() -> None:
    _SNAPSHOTS.clear()


def load_snapshots(records: Iterable[ContinuitySnapshot]) -> None:
    if not isinstance(records, Iterable):
        raise ValueError("records must be an iterable of ContinuitySnapshot.")
    reset_continuity_store()
    for record in records:
        if not isinstance(record, ContinuitySnapshot):
            raise ValueError("all records must be ContinuitySnapshot instances.")
        if record.snapshot_id in _SNAPSHOTS:
            raise ValueError(f"Duplicate snapshot_id during load: {record.snapshot_id}")
        _SNAPSHOTS[record.snapshot_id] = record
