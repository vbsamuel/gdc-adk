from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, TypedDict
import uuid

from gdc_adk.core.contracts import Artifact, Issue, WorkflowRun
from gdc_adk.core.contracts import validate_workflow_run_record
from gdc_adk.core.state import validate_workflow_mode
from gdc_adk.substrate.artifact_store import (
    create_artifact,
    link_issue_to_artifact as link_artifact_to_issue,
    new_artifact,
    update_artifact_workflow_run,
)
from gdc_adk.substrate.event_spine import create_event
from gdc_adk.substrate.issue_tracker import create_issue, link_issue_to_artifact as link_issue_to_artifact_record

_WORKFLOW_RUNS: Dict[str, WorkflowRun] = {}
_STAGE1_WORKFLOW_MODES: frozenset[str] = frozenset({"single_run", "fix_flow"})


class DispatchRequest(TypedDict):
    request_id: str
    raw_signal: str | dict
    source_metadata: Dict[str, Any]
    workflow_hint: Optional[str]
    artifact_reference_ids: List[str]
    correlation_id: str


class DispatchResult(TypedDict):
    request_artifact: Artifact
    workflow_run: WorkflowRun
    created_issue: Optional[Issue]
    emitted_event_ids: List[str]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _raw_text(raw_signal: str | dict) -> str:
    if isinstance(raw_signal, str):
        return raw_signal
    if isinstance(raw_signal, dict):
        return str(raw_signal.get("text", ""))
    return str(raw_signal)


def _validate_stage1_workflow_mode(workflow_mode: str) -> str:
    validated_mode = validate_workflow_mode(workflow_mode)
    if validated_mode not in _STAGE1_WORKFLOW_MODES:
        raise ValueError(f"Unsupported Stage 1 workflow_mode: {validated_mode}")
    return validated_mode


def reset_workflow_runs() -> None:
    _WORKFLOW_RUNS.clear()


def export_workflow_runs() -> List[WorkflowRun]:
    return [dict(workflow_run) for workflow_run in _WORKFLOW_RUNS.values()]


def load_workflow_runs(workflow_runs: List[WorkflowRun]) -> None:
    reset_workflow_runs()
    for workflow_run in workflow_runs:
        validate_workflow_run_record(workflow_run)
        workflow_run_id = workflow_run["workflow_run_id"]
        if workflow_run_id in _WORKFLOW_RUNS:
            raise ValueError(f"Duplicate workflow_run_id: {workflow_run_id}")
        _WORKFLOW_RUNS[workflow_run_id] = dict(workflow_run)


def select_workflow_mode(request: DispatchRequest) -> str:
    hint = request.get("workflow_hint")
    if hint is not None:
        return _validate_stage1_workflow_mode(hint)

    text = _raw_text(request["raw_signal"]).lower()
    if any(x in text for x in ["bug", "broken", "fix", "error", "issue", "failed"]):
        return "fix_flow"
    return "single_run"


def initialize_workflow_run(request: DispatchRequest, workflow_mode: str, input_artifact_id: str) -> WorkflowRun:
    _validate_stage1_workflow_mode(workflow_mode)
    initial_state = "received"
    workflow_run_id = f"wr_{uuid.uuid4().hex[:12]}"
    workflow_run: WorkflowRun = {
        "workflow_run_id": workflow_run_id,
        "workflow_mode": workflow_mode,
        "current_state": initial_state,
        "input_artifact_ids": [input_artifact_id],
        "output_artifact_ids": [],
        "issue_ids": [],
        "finding_ids": [],
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
        "state_history": [{"state": initial_state, "timestamp": _now_iso()}],
    }
    validate_workflow_run_record(workflow_run)
    _WORKFLOW_RUNS[workflow_run_id] = workflow_run
    return workflow_run


def should_create_issue(request: DispatchRequest, workflow_mode: str) -> bool:
    if workflow_mode == "fix_flow":
        return True
    return False


def dispatch_request(request: DispatchRequest) -> DispatchResult:
    workflow_mode = select_workflow_mode(request)
    raw_text = _raw_text(request["raw_signal"])

    artifact_obj = new_artifact(kind="request", content=raw_text, source=request.get("source_metadata", {}).get("origin", "request"), metadata={"source_metadata": request.get("source_metadata", {})})
    artifact = create_artifact(artifact_obj)

    workflow_run = initialize_workflow_run(request, workflow_mode, artifact["artifact_id"])
    artifact = update_artifact_workflow_run(artifact["artifact_id"], workflow_run["workflow_run_id"])

    emitted_event_ids: List[str] = []

    ev = create_event(
        event_type="request_received",
        correlation_id=request["correlation_id"],
        payload={"request_id": request["request_id"], "workflow_mode": workflow_mode, "raw_signal": raw_text},
        workflow_run_id=workflow_run["workflow_run_id"],
    )
    emitted_event_ids.append(ev["event_id"])

    ev = create_event(
        event_type="artifact_created",
        correlation_id=request["correlation_id"],
        payload={"artifact_id": artifact["artifact_id"]},
        workflow_run_id=workflow_run["workflow_run_id"],
    )
    emitted_event_ids.append(ev["event_id"])

    ev = create_event(
        event_type="workflow_started",
        correlation_id=request["correlation_id"],
        payload={"workflow_run_id": workflow_run["workflow_run_id"]},
        workflow_run_id=workflow_run["workflow_run_id"],
    )
    emitted_event_ids.append(ev["event_id"])

    # immediate classification transition
    next_state = "classified"
    workflow_run["current_state"] = next_state
    workflow_run["state_history"].append({"state": next_state, "timestamp": _now_iso()})
    workflow_run["updated_at"] = _now_iso()

    ev = create_event(
        event_type="workflow_transitioned",
        correlation_id=request["correlation_id"],
        payload={"from": "received", "to": next_state},
        workflow_run_id=workflow_run["workflow_run_id"],
    )
    emitted_event_ids.append(ev["event_id"])

    created_issue: Optional[Issue] = None
    if should_create_issue(request, workflow_mode):
        issue_obj: Issue = {
            "issue_id": f"iss_{uuid.uuid4().hex[:12]}",
            "issue_type": "defect",
            "title": "Auto-identified fix_flow request",
            "description": raw_text,
            "severity": "medium",
            "status": "open",
            "related_artifact_ids": [artifact["artifact_id"]],
            "related_finding_ids": [],
            "created_at": _now_iso(),
            "updated_at": _now_iso(),
            "reopen_count": 0,
        }
        created_issue = create_issue(issue_obj)
        link_issue_to_artifact_record(created_issue["issue_id"], artifact["artifact_id"])
        artifact = link_artifact_to_issue(artifact["artifact_id"], created_issue["issue_id"])
        workflow_run["issue_ids"].append(created_issue["issue_id"])

        ev = create_event(
            event_type="issue_created",
            correlation_id=request["correlation_id"],
            payload={"issue_id": created_issue["issue_id"], "related_artifact_id": artifact["artifact_id"]},
            workflow_run_id=workflow_run["workflow_run_id"],
        )
        emitted_event_ids.append(ev["event_id"])

    return {
        "request_artifact": artifact,
        "workflow_run": workflow_run,
        "created_issue": created_issue,
        "emitted_event_ids": emitted_event_ids,
    }


def dispatch_text_request(text: str) -> DispatchResult:
    request: DispatchRequest = {
        "request_id": f"req_{uuid.uuid4().hex[:12]}",
        "raw_signal": text,
        "source_metadata": {"origin": "text_input"},
        "workflow_hint": None,
        "artifact_reference_ids": [],
        "correlation_id": f"corr_{uuid.uuid4().hex[:12]}",
    }
    return dispatch_request(request)
