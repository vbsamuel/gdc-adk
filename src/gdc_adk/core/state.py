from __future__ import annotations

from typing import Any

WORKFLOW_MODES: frozenset[str] = frozenset(
    [
        "single_run",
        "iterative",
        "fix_flow",
        "dynamic_flow",
        "fuzzy_logical_flow",
    ]
)

WORKFLOW_STATES: frozenset[str] = frozenset(
    [
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
    ]
)

FIX_FLOW_STATES: frozenset[str] = frozenset(
    [
        "issue_opened",
        "remediation_in_progress",
        "verification_pending",
        "resolution_proposed",
        "resolution_verified",
    ]
)

ISSUE_TYPES: frozenset[str] = frozenset(
    [
        "defect",
        "drift",
        "grounding_gap",
        "contradiction",
        "enhancement",
        "blocked_dependency",
        "policy_violation",
    ]
)

ISSUE_STATUSES: frozenset[str] = frozenset(
    [
        "open",
        "in_progress",
        "blocked",
        "resolved",
        "closed",
        "reopened",
    ]
)

FINDING_TYPES: frozenset[str] = frozenset(
    [
        "unsupported_claim",
        "missing_case",
        "architecture_drift",
        "contract_violation",
        "provider_policy_violation",
        "traceability_gap",
        "replayability_gap",
        "validation_gap",
        "grounding_gap",
        "contradiction",
    ]
)

SEVERITIES: frozenset[str] = frozenset(["critical", "high", "medium", "low"])

EVENT_TYPES: frozenset[str] = frozenset(
    [
        "request_received",
        "signal_ingested",
        "signal_normalized",
        "artifact_indexed",
        "activation_classified",
        "artifact_created",
        "artifact_revised",
        "artifact_emitted",
        "issue_created",
        "issue_status_changed",
        "issue_reopened",
        "finding_created",
        "finding_resolved",
        "workflow_started",
        "workflow_transitioned",
        "workflow_blocked",
        "workflow_completed",
        "workflow_failed",
        "workflow_reopened",
        "provider_selected",
        "provider_invoked",
        "provider_failed",
        "cache_hit",
        "cache_miss",
    ]
)


def _validate_choice(value: str, allowed: frozenset[str], name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    if value not in allowed:
        raise ValueError(f"Invalid {name}: {value}")
    return value


def validate_workflow_mode(workflow_mode: str) -> str:
    return _validate_choice(workflow_mode, WORKFLOW_MODES, "workflow_mode")


def validate_workflow_state(workflow_state: str) -> str:
    return _validate_choice(workflow_state, WORKFLOW_STATES, "workflow_state")


def validate_issue_type(issue_type: str) -> str:
    return _validate_choice(issue_type, ISSUE_TYPES, "issue_type")


def validate_issue_status(issue_status: str) -> str:
    return _validate_choice(issue_status, ISSUE_STATUSES, "issue_status")


def validate_severity(severity: str) -> str:
    return _validate_choice(severity, SEVERITIES, "severity")


def validate_event_type(event_type: str) -> str:
    return _validate_choice(event_type, EVENT_TYPES, "event_type")


def is_terminal_workflow_state(workflow_state: str) -> bool:
    state = validate_workflow_state(workflow_state)
    return state in {"completed", "failed", "blocked"}


def is_reopenable_issue_status(issue_status: str) -> bool:
    status = validate_issue_status(issue_status)
    return status in {"resolved", "closed"}
