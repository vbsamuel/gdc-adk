from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from typing import Mapping
from uuid import uuid4


BASELINE_STATES: tuple[str, ...] = (
    "received",
    "classified",
    "activated",
    "planned",
    "executing",
    "awaiting_review",
    "revising",
    "validated",
    "completed",
    "failed",
    "blocked",
    "reopened",
)

FIX_FLOW_STATES: tuple[str, ...] = (
    "issue_opened",
    "remediation_in_progress",
    "verification_pending",
    "resolution_proposed",
    "resolution_verified",
)


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class WorkflowHistoryEntry:
    from_state: str
    to_state: str
    reason: str
    changed_at: str


@dataclass(frozen=True)
class WorkflowRun:
    workflow_run_id: str
    workflow_mode: str
    workflow_state: str
    issue_ids: tuple[str, ...] = ()
    finding_ids: tuple[str, ...] = ()
    input_artifact_ids: tuple[str, ...] = ()
    output_artifact_ids: tuple[str, ...] = ()
    continuity_requirements: tuple[str, ...] = ()
    history: tuple[WorkflowHistoryEntry, ...] = ()
    last_reason: str | None = None


ALLOWED_TRANSITIONS: dict[str, dict[str, tuple[str, ...]]] = {
    "single_run": {
        "received": ("classified", "failed", "blocked"),
        "classified": ("activated", "failed", "blocked"),
        "activated": ("planned", "executing", "blocked"),
        "planned": ("executing", "blocked", "failed"),
        "executing": ("awaiting_review", "validated", "failed", "blocked"),
        "awaiting_review": ("validated", "revising", "blocked", "failed"),
        "revising": ("executing", "awaiting_review", "failed", "blocked"),
        "validated": ("completed", "reopened", "failed", "blocked"),
        "completed": (),
        "failed": ("reopened",),
        "blocked": ("reopened", "failed"),
        "reopened": ("planned", "executing", "blocked", "failed"),
    },
    "iterative": {
        "received": ("classified", "failed", "blocked"),
        "classified": ("activated", "failed", "blocked"),
        "activated": ("planned", "blocked"),
        "planned": ("executing", "blocked", "failed"),
        "executing": ("awaiting_review", "failed", "blocked"),
        "awaiting_review": ("revising", "validated", "failed", "blocked"),
        "revising": ("executing", "awaiting_review", "blocked", "failed", "reopened"),
        "validated": ("completed", "reopened", "failed"),
        "completed": (),
        "failed": ("reopened",),
        "blocked": ("reopened", "failed"),
        "reopened": ("planned", "revising", "executing"),
    },
    "fix_flow": {
        "received": ("classified", "failed", "blocked"),
        "classified": ("activated", "failed", "blocked"),
        "activated": ("issue_opened", "blocked"),
        "issue_opened": ("remediation_in_progress", "blocked", "failed"),
        "remediation_in_progress": ("verification_pending", "resolution_proposed", "blocked", "failed"),
        "verification_pending": ("resolution_verified", "reopened", "failed", "blocked"),
        "resolution_proposed": ("verification_pending", "blocked", "failed"),
        "resolution_verified": ("validated", "reopened", "failed"),
        "validated": ("completed", "reopened", "failed"),
        "completed": (),
        "failed": ("reopened",),
        "blocked": ("reopened", "failed"),
        "reopened": ("remediation_in_progress", "verification_pending", "blocked"),
    },
    "dynamic_flow": {
        "received": ("classified", "failed", "blocked"),
        "classified": ("activated", "failed", "blocked"),
        "activated": ("planned", "executing", "blocked"),
        "planned": ("executing", "revising", "blocked", "failed"),
        "executing": ("awaiting_review", "planned", "blocked", "failed"),
        "awaiting_review": ("revising", "validated", "blocked", "failed"),
        "revising": ("planned", "executing", "blocked", "failed"),
        "validated": ("completed", "reopened", "failed"),
        "completed": (),
        "failed": ("reopened",),
        "blocked": ("reopened", "failed"),
        "reopened": ("planned", "executing", "blocked"),
    },
    "fuzzy_logical_flow": {
        "received": ("classified", "failed", "blocked"),
        "classified": ("activated", "blocked", "failed"),
        "activated": ("planned", "revising", "blocked"),
        "planned": ("executing", "revising", "blocked", "failed"),
        "executing": ("awaiting_review", "revising", "blocked", "failed"),
        "awaiting_review": ("revising", "validated", "blocked", "failed"),
        "revising": ("planned", "executing", "blocked", "failed"),
        "validated": ("completed", "reopened", "failed"),
        "completed": (),
        "failed": ("reopened",),
        "blocked": ("reopened", "failed"),
        "reopened": ("planned", "revising", "executing"),
    },
}


def create_workflow_run(
    workflow_mode: str,
    input_artifact_ids: tuple[str, ...] | list[str],
    issue_ids: tuple[str, ...] | list[str] = (),
    continuity_requirements: tuple[str, ...] | list[str] = (),
) -> WorkflowRun:
    if workflow_mode not in ALLOWED_TRANSITIONS:
        raise ValueError(f"Unsupported workflow_mode: {workflow_mode}")
    normalized_input_artifact_ids = tuple(str(artifact_id) for artifact_id in input_artifact_ids)
    if any(not artifact_id.strip() for artifact_id in normalized_input_artifact_ids):
        raise ValueError("input_artifact_ids must contain only non-empty identifiers.")
    return WorkflowRun(
        workflow_run_id=f"wr_{uuid4().hex[:12]}",
        workflow_mode=workflow_mode,
        workflow_state="received",
        issue_ids=tuple(str(issue_id) for issue_id in issue_ids),
        input_artifact_ids=normalized_input_artifact_ids,
        continuity_requirements=tuple(str(item) for item in continuity_requirements),
    )


def get_allowed_transitions(workflow_mode: str, current_state: str) -> list[str]:
    if workflow_mode not in ALLOWED_TRANSITIONS:
        raise ValueError(f"Unsupported workflow_mode: {workflow_mode}")
    if current_state not in ALLOWED_TRANSITIONS[workflow_mode]:
        raise ValueError(f"Unsupported current_state '{current_state}' for workflow_mode '{workflow_mode}'.")
    return list(ALLOWED_TRANSITIONS[workflow_mode][current_state])


def validate_transition(workflow_mode: str, current_state: str, next_state: str) -> None:
    if next_state not in BASELINE_STATES + FIX_FLOW_STATES:
        raise ValueError(f"Unsupported next_state: {next_state}")
    allowed_transitions = get_allowed_transitions(workflow_mode, current_state)
    if next_state not in allowed_transitions:
        raise ValueError(
            f"Invalid transition for workflow_mode '{workflow_mode}': {current_state} -> {next_state}"
        )


def transition_workflow_state(workflow_run: WorkflowRun, next_state: str, reason: str) -> WorkflowRun:
    if not isinstance(workflow_run, WorkflowRun):
        raise ValueError("workflow_run must be a WorkflowRun.")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("reason must be a non-empty string.")
    validate_transition(workflow_run.workflow_mode, workflow_run.workflow_state, next_state)
    history_entry = WorkflowHistoryEntry(
        from_state=workflow_run.workflow_state,
        to_state=next_state,
        reason=reason,
        changed_at=_utc_now(),
    )
    return replace(
        workflow_run,
        workflow_state=next_state,
        history=workflow_run.history + (history_entry,),
        last_reason=reason,
    )


def is_terminal_state(workflow_mode: str, state: str) -> bool:
    get_allowed_transitions(workflow_mode, state)
    return len(ALLOWED_TRANSITIONS[workflow_mode][state]) == 0
