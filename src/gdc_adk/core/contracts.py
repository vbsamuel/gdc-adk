from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional, TypedDict
import json

from gdc_adk.core.state import (
    validate_event_type,
    validate_issue_status,
    validate_issue_type,
    validate_severity,
    validate_workflow_mode,
    validate_workflow_state,
)


class Artifact(TypedDict):
    artifact_id: str
    artifact_kind: str
    content: Optional[str]
    content_ref: Optional[str]
    source: Dict[str, Any]
    metadata: Dict[str, Any]
    created_at: str
    parent_artifact_ids: List[str]
    workflow_run_id: Optional[str]
    issue_ids: List[str]


class Issue(TypedDict):
    issue_id: str
    issue_type: str
    title: str
    description: str
    severity: str
    status: str
    related_artifact_ids: List[str]
    related_finding_ids: List[str]
    created_at: str
    updated_at: str
    reopen_count: int


class WorkflowRun(TypedDict):
    workflow_run_id: str
    workflow_mode: str
    current_state: str
    input_artifact_ids: List[str]
    output_artifact_ids: List[str]
    issue_ids: List[str]
    finding_ids: List[str]
    created_at: str
    updated_at: str
    state_history: List[Dict[str, Any]]


class Event(TypedDict):
    event_id: str
    event_type: str
    created_at: str
    correlation_id: str
    workflow_run_id: Optional[str]
    payload: Dict[str, Any]


class ReviewFinding(TypedDict):
    finding_id: str
    severity: str
    description: str
    related_artifact_ids: List[str]
    status: str
    created_at: str


class Emission(TypedDict):
    emission_id: str
    emission_type: str
    payload: Dict[str, Any]
    target: str
    created_at: str


class ContinuitySnapshot(TypedDict):
    snapshot_id: str
    workflow_run_id: str
    artifact_ids: List[str]
    issue_ids: List[str]
    created_at: str


def _validate_serializable(value: Any, name: str) -> None:
    try:
        json.dumps(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be JSON serializable") from exc


def _validate_timestamp(value: str, field_name: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    try:
        datetime.fromisoformat(value.replace("Z", ""))
    except ValueError as exc:
        raise ValueError(f"{field_name} must be ISO8601 format") from exc


def _validate_artifact_shape(artifact: Artifact) -> None:
    if not isinstance(artifact, dict):
        raise TypeError("artifact must be a dict-like object")

    required = [
        "artifact_id",
        "artifact_kind",
        "content",
        "content_ref",
        "source",
        "metadata",
        "created_at",
        "parent_artifact_ids",
        "workflow_run_id",
        "issue_ids",
    ]
    for key in required:
        if key not in artifact:
            raise ValueError(f"artifact missing required field: {key}")

    if not artifact["artifact_id"] or not isinstance(artifact["artifact_id"], str):
        raise ValueError("artifact_id must be non-empty string")
    if not artifact["artifact_kind"] or not isinstance(artifact["artifact_kind"], str):
        raise ValueError("artifact_kind must be non-empty string")
    if artifact["content"] is None and artifact["content_ref"] is None:
        raise ValueError("artifact must have content or content_ref")
    if not isinstance(artifact["source"], dict):
        raise TypeError("artifact.source must be dict")
    _validate_serializable(artifact["metadata"], "artifact.metadata")
    if not isinstance(artifact["parent_artifact_ids"], list):
        raise TypeError("artifact.parent_artifact_ids must be list")
    if not isinstance(artifact["issue_ids"], list):
        raise TypeError("artifact.issue_ids must be list")
    _validate_timestamp(artifact["created_at"], "artifact.created_at")


def _validate_issue_shape(issue: Issue) -> None:
    if not isinstance(issue, dict):
        raise TypeError("issue must be dict-like")
    required = [
        "issue_id",
        "issue_type",
        "title",
        "description",
        "severity",
        "status",
        "related_artifact_ids",
        "related_finding_ids",
        "created_at",
        "updated_at",
        "reopen_count",
    ]
    for key in required:
        if key not in issue:
            raise ValueError(f"issue missing required field: {key}")

    if not issue["issue_id"] or not isinstance(issue["issue_id"], str):
        raise ValueError("issue_id must be non-empty string")
    validate_issue_type(issue["issue_type"])
    if not isinstance(issue["title"], str) or not issue["title"]:
        raise ValueError("issue.title must be non-empty string")
    if not isinstance(issue["description"], str):
        raise ValueError("issue.description must be string")
    validate_severity(issue["severity"])
    validate_issue_status(issue["status"])
    if not isinstance(issue["related_artifact_ids"], list):
        raise TypeError("related_artifact_ids must be list")
    if not isinstance(issue["related_finding_ids"], list):
        raise TypeError("related_finding_ids must be list")
    _validate_timestamp(issue["created_at"], "issue.created_at")
    _validate_timestamp(issue["updated_at"], "issue.updated_at")
    if not isinstance(issue["reopen_count"], int) or issue["reopen_count"] < 0:
        raise ValueError("reopen_count must be non-negative int")


def _validate_workflow_shape(workflow_run: WorkflowRun) -> None:
    if not isinstance(workflow_run, dict):
        raise TypeError("workflow_run must be dict-like")
    required = [
        "workflow_run_id",
        "workflow_mode",
        "current_state",
        "input_artifact_ids",
        "output_artifact_ids",
        "issue_ids",
        "finding_ids",
        "created_at",
        "updated_at",
        "state_history",
    ]
    for key in required:
        if key not in workflow_run:
            raise ValueError(f"workflow_run missing required field: {key}")

    if not workflow_run["workflow_run_id"] or not isinstance(workflow_run["workflow_run_id"], str):
        raise ValueError("workflow_run_id must be non-empty string")
    validate_workflow_mode(workflow_run["workflow_mode"])
    validate_workflow_state(workflow_run["current_state"])
    if not isinstance(workflow_run["input_artifact_ids"], list):
        raise TypeError("input_artifact_ids must be list")
    if not isinstance(workflow_run["output_artifact_ids"], list):
        raise TypeError("output_artifact_ids must be list")
    if not isinstance(workflow_run["issue_ids"], list):
        raise TypeError("issue_ids must be list")
    if not isinstance(workflow_run["finding_ids"], list):
        raise TypeError("finding_ids must be list")
    if not isinstance(workflow_run["state_history"], list):
        raise TypeError("state_history must be list")
    _validate_timestamp(workflow_run["created_at"], "workflow_run.created_at")
    _validate_timestamp(workflow_run["updated_at"], "workflow_run.updated_at")


def _validate_event_shape(event: Event) -> None:
    if not isinstance(event, dict):
        raise TypeError("event must be dict-like")
    required = ["event_id", "event_type", "created_at", "correlation_id", "workflow_run_id", "payload"]
    for key in required:
        if key not in event:
            raise ValueError(f"event missing required field: {key}")

    if not event["event_id"] or not isinstance(event["event_id"], str):
        raise ValueError("event_id must be non-empty string")
    validate_event_type(event["event_type"])
    _validate_timestamp(event["created_at"], "event.created_at")
    if not isinstance(event["correlation_id"], str):
        raise TypeError("correlation_id must be string")
    if event["workflow_run_id"] is not None and not isinstance(event["workflow_run_id"], str):
        raise TypeError("workflow_run_id must be string or None")
    if not isinstance(event["payload"], dict):
        raise TypeError("payload must be dict")
    _validate_serializable(event["payload"], "event.payload")


def validate_artifact_record(artifact: Artifact) -> None:
    _validate_artifact_shape(artifact)


def validate_issue_record(issue: Issue) -> None:
    _validate_issue_shape(issue)


def validate_workflow_run_record(workflow_run: WorkflowRun) -> None:
    _validate_workflow_shape(workflow_run)


def validate_event_record(event: Event) -> None:
    _validate_event_shape(event)


def serialize_artifact(artifact: Artifact) -> Dict[str, Any]:
    validate_artifact_record(artifact)
    return dict(artifact)


def serialize_issue(issue: Issue) -> Dict[str, Any]:
    validate_issue_record(issue)
    return dict(issue)


def serialize_workflow_run(workflow_run: WorkflowRun) -> Dict[str, Any]:
    validate_workflow_run_record(workflow_run)
    return dict(workflow_run)


def serialize_event(event: Event) -> Dict[str, Any]:
    validate_event_record(event)
    return dict(event)
