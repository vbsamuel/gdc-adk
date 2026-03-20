from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, TypedDict
import uuid

from gdc_adk.core.contracts import Artifact, Event, Issue, WorkflowRun
from gdc_adk.core.contracts import validate_workflow_run_record
from gdc_adk.core.state import validate_workflow_mode
from gdc_adk.adapters.adk.replay_envelope import ReplayReferenceEnvelope
from gdc_adk.memory.contracts import ContinuitySnapshot
from gdc_adk.substrate.artifact_store import (
    create_artifact,
    get_artifact,
    link_issue_to_artifact as link_artifact_to_issue,
    new_artifact,
    update_artifact_workflow_run,
)
from gdc_adk.substrate.event_spine import create_event, export_event_records
from gdc_adk.substrate.issue_tracker import (
    create_issue,
    get_issue,
    link_issue_to_artifact as link_issue_to_artifact_record,
)
from gdc_adk.validation.validator import ReviewFinding

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


@dataclass(frozen=True)
class ReplayEvidenceBundle:
    workflow_run: WorkflowRun
    events: tuple[Event, ...]
    artifacts: tuple[Artifact, ...]
    issues: tuple[Issue, ...]
    findings: tuple[ReviewFinding, ...] = ()
    snapshots: tuple[ContinuitySnapshot, ...] = ()
    replay_reference_envelopes: tuple[ReplayReferenceEnvelope, ...] = ()


@dataclass(frozen=True)
class ReplayReconstructionResult:
    status: str
    workflow_run_id: str
    event_ids: tuple[str, ...]
    artifact_ids: tuple[str, ...]
    issue_ids: tuple[str, ...]
    finding_ids: tuple[str, ...]
    snapshot_ids: tuple[str, ...]
    replay_reference_workflow_ids: tuple[str, ...]
    message: str


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


def get_workflow_run(workflow_run_id: str) -> WorkflowRun:
    if workflow_run_id not in _WORKFLOW_RUNS:
        raise KeyError(f"Workflow run not found: {workflow_run_id}")
    return _WORKFLOW_RUNS[workflow_run_id]


def build_replay_evidence_bundle(
    workflow_run_id: str,
    findings: tuple[ReviewFinding, ...] | list[ReviewFinding] = (),
    snapshots: tuple[ContinuitySnapshot, ...] | list[ContinuitySnapshot] = (),
    replay_reference_envelopes: tuple[ReplayReferenceEnvelope, ...] | list[ReplayReferenceEnvelope] = (),
) -> ReplayEvidenceBundle:
    if not isinstance(workflow_run_id, str) or not workflow_run_id.strip():
        raise ValueError("workflow_run_id must be a non-empty string.")

    workflow_run = get_workflow_run(workflow_run_id)
    events = tuple(event for event in export_event_records() if event["workflow_run_id"] == workflow_run_id)
    if not events:
        raise ValueError(f"No events found for workflow_run_id: {workflow_run_id}")

    artifact_ids = tuple(dict.fromkeys(workflow_run["input_artifact_ids"] + workflow_run["output_artifact_ids"]))
    if not artifact_ids:
        raise ValueError("workflow_run must reference at least one artifact.")
    artifacts = tuple(get_artifact(artifact_id) for artifact_id in artifact_ids)

    issues = tuple(get_issue(issue_id) for issue_id in workflow_run["issue_ids"])
    normalized_findings = tuple(findings)
    normalized_snapshots = tuple(snapshots)
    normalized_replay_reference_envelopes = tuple(replay_reference_envelopes)
    validate_replay_evidence_bundle(
        ReplayEvidenceBundle(
            workflow_run=workflow_run,
            events=events,
            artifacts=artifacts,
            issues=issues,
            findings=normalized_findings,
            snapshots=normalized_snapshots,
            replay_reference_envelopes=normalized_replay_reference_envelopes,
        )
    )
    return ReplayEvidenceBundle(
        workflow_run=workflow_run,
        events=events,
        artifacts=artifacts,
        issues=issues,
        findings=normalized_findings,
        snapshots=normalized_snapshots,
        replay_reference_envelopes=normalized_replay_reference_envelopes,
    )


def validate_replay_evidence_bundle(replay_bundle: ReplayEvidenceBundle) -> None:
    if not isinstance(replay_bundle, ReplayEvidenceBundle):
        raise ValueError("replay_bundle must be a ReplayEvidenceBundle.")

    workflow_run = replay_bundle.workflow_run
    validate_workflow_run_record(workflow_run)

    if not replay_bundle.events:
        raise ValueError("Replay bundle must include at least one event.")
    event_ids: set[str] = set()
    for event in replay_bundle.events:
        if event["event_id"] in event_ids:
            raise ValueError(f"Duplicate event_id in replay bundle: {event['event_id']}")
        event_ids.add(event["event_id"])
        if event["workflow_run_id"] != workflow_run["workflow_run_id"]:
            raise ValueError("Replay bundle contains an event linked to a different workflow_run_id.")

    if not replay_bundle.artifacts:
        raise ValueError("Replay bundle must include at least one artifact.")
    artifact_ids: set[str] = set()
    for artifact in replay_bundle.artifacts:
        if artifact["artifact_id"] in artifact_ids:
            raise ValueError(f"Duplicate artifact_id in replay bundle: {artifact['artifact_id']}")
        artifact_ids.add(artifact["artifact_id"])
        if artifact.get("workflow_run_id") != workflow_run["workflow_run_id"]:
            raise ValueError("Replay bundle contains an artifact linked to a different workflow_run_id.")

    issue_ids: set[str] = set()
    for issue in replay_bundle.issues:
        if issue["issue_id"] in issue_ids:
            raise ValueError(f"Duplicate issue_id in replay bundle: {issue['issue_id']}")
        issue_ids.add(issue["issue_id"])
        for artifact_id in issue["related_artifact_ids"]:
            if artifact_id not in artifact_ids:
                raise ValueError(f"Issue references unknown artifact_id: {artifact_id}")

    workflow_artifact_ids = set(workflow_run["input_artifact_ids"] + workflow_run["output_artifact_ids"])
    if not workflow_artifact_ids.issubset(artifact_ids):
        raise ValueError("Replay bundle is missing workflow-linked artifacts.")
    if not set(workflow_run["issue_ids"]).issubset(issue_ids):
        raise ValueError("Replay bundle is missing workflow-linked issues.")

    finding_ids: set[str] = set()
    for finding in replay_bundle.findings:
        if finding.finding_id in finding_ids:
            raise ValueError(f"Duplicate finding_id in replay bundle: {finding.finding_id}")
        finding_ids.add(finding.finding_id)
        if finding.related_workflow_run_id not in {None, workflow_run["workflow_run_id"]}:
            raise ValueError("Replay bundle contains a finding linked to a different workflow_run_id.")
        if not set(finding.related_artifact_ids).issubset(artifact_ids):
            raise ValueError("Replay bundle contains a finding with unknown artifact references.")

    if workflow_run["finding_ids"]:
        if not replay_bundle.findings:
            raise ValueError("Replay bundle is missing required findings for full reconstruction.")
        if not set(workflow_run["finding_ids"]).issubset(finding_ids):
            raise ValueError("Replay bundle is missing workflow-linked findings.")

    if not replay_bundle.snapshots:
        raise ValueError("Replay bundle must include at least one snapshot for full reconstruction.")
    snapshot_ids: set[str] = set()
    for snapshot in replay_bundle.snapshots:
        if snapshot.snapshot_id in snapshot_ids:
            raise ValueError(f"Duplicate snapshot_id in replay bundle: {snapshot.snapshot_id}")
        snapshot_ids.add(snapshot.snapshot_id)
        if snapshot.workflow_run_id != workflow_run["workflow_run_id"]:
            raise ValueError("Replay bundle contains a snapshot linked to a different workflow_run_id.")
        if not set(snapshot.artifact_ids).issubset(artifact_ids):
            raise ValueError("Replay bundle contains a snapshot with unknown artifact references.")
        if not set(snapshot.issue_ids).issubset(issue_ids):
            raise ValueError("Replay bundle contains a snapshot with unknown issue references.")

    for replay_reference_envelope in replay_bundle.replay_reference_envelopes:
        if replay_reference_envelope.workflow_run_id != workflow_run["workflow_run_id"]:
            raise ValueError("Replay bundle contains a replay reference envelope linked to a different workflow_run_id.")
        if not set(replay_reference_envelope.issue_ids).issubset(issue_ids):
            raise ValueError("Replay bundle contains a replay reference envelope with unknown issue references.")
        if replay_reference_envelope.finding_ids and not set(replay_reference_envelope.finding_ids).issubset(finding_ids):
            raise ValueError("Replay bundle contains a replay reference envelope with unknown finding references.")
        if replay_reference_envelope.continuity_snapshot_ids and not set(replay_reference_envelope.continuity_snapshot_ids).issubset(snapshot_ids):
            raise ValueError("Replay bundle contains a replay reference envelope with unknown snapshot references.")


def reconstruct_workflow_run(replay_bundle: ReplayEvidenceBundle) -> ReplayReconstructionResult:
    validate_replay_evidence_bundle(replay_bundle)
    workflow_run = replay_bundle.workflow_run
    return ReplayReconstructionResult(
        status="reconstructed",
        workflow_run_id=workflow_run["workflow_run_id"],
        event_ids=tuple(event["event_id"] for event in replay_bundle.events),
        artifact_ids=tuple(artifact["artifact_id"] for artifact in replay_bundle.artifacts),
        issue_ids=tuple(issue["issue_id"] for issue in replay_bundle.issues),
        finding_ids=tuple(finding.finding_id for finding in replay_bundle.findings),
        snapshot_ids=tuple(snapshot.snapshot_id for snapshot in replay_bundle.snapshots),
        replay_reference_workflow_ids=tuple(envelope.workflow_run_id for envelope in replay_bundle.replay_reference_envelopes),
        message="Workflow run reconstructed from structured replay evidence.",
    )


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
