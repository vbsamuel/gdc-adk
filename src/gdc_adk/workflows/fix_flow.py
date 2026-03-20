from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime
from uuid import uuid4

from gdc_adk.workflows.state_machine import WorkflowRun, transition_workflow_state


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class VerificationResult:
    issue_id: str
    workflow_run_id: str
    evidence_artifact_ids: tuple[str, ...]
    verification_status: str
    verifier: str
    verification_reason: str
    verified_at: str


@dataclass(frozen=True)
class FixFlowResult:
    workflow_run: WorkflowRun
    issue_id: str
    remediation_notes: tuple[str, ...] = ()
    remediation_artifact_ids: tuple[str, ...] = ()
    evidence_artifact_ids: tuple[str, ...] = ()
    verification_result: VerificationResult | None = None


def _require_fix_flow_run(workflow_run: WorkflowRun) -> WorkflowRun:
    if not isinstance(workflow_run, WorkflowRun):
        raise ValueError("workflow_run must be a WorkflowRun.")
    if workflow_run.workflow_mode != "fix_flow":
        raise ValueError("workflow_run.workflow_mode must be 'fix_flow'.")
    return workflow_run


def _require_issue_link(issue_id: str) -> str:
    if not isinstance(issue_id, str) or not issue_id.strip():
        raise ValueError("issue_id must be a non-empty string.")
    return issue_id


def start_fix_flow(
    workflow_run: WorkflowRun,
    issue_id: str,
    artifact_ids: tuple[str, ...] | list[str],
) -> FixFlowResult:
    run = _require_fix_flow_run(workflow_run)
    normalized_issue_id = _require_issue_link(issue_id)
    remediation_artifact_ids = tuple(str(artifact_id) for artifact_id in artifact_ids)
    if not remediation_artifact_ids:
        raise ValueError("artifact_ids must contain at least one artifact identifier.")
    linked_issue_ids = run.issue_ids if normalized_issue_id in run.issue_ids else run.issue_ids + (normalized_issue_id,)
    linked_run = replace(run, issue_ids=linked_issue_ids, output_artifact_ids=run.output_artifact_ids + remediation_artifact_ids)
    transitioned_run = transition_workflow_state(linked_run, "issue_opened", "Fix-flow issue linkage established.")
    return FixFlowResult(
        workflow_run=transitioned_run,
        issue_id=normalized_issue_id,
        remediation_artifact_ids=remediation_artifact_ids,
    )


def record_remediation_attempt(
    workflow_run: WorkflowRun,
    issue_id: str,
    remediation_notes: str,
    artifact_ids: tuple[str, ...] | list[str],
) -> FixFlowResult:
    run = _require_fix_flow_run(workflow_run)
    normalized_issue_id = _require_issue_link(issue_id)
    if normalized_issue_id not in run.issue_ids:
        raise ValueError("workflow_run must already be linked to issue_id.")
    if not remediation_notes.strip():
        raise ValueError("remediation_notes must be non-empty.")
    remediation_artifact_ids = tuple(str(artifact_id) for artifact_id in artifact_ids)
    transitioned_run = transition_workflow_state(run, "remediation_in_progress", remediation_notes)
    updated_run = replace(
        transitioned_run,
        output_artifact_ids=transitioned_run.output_artifact_ids + remediation_artifact_ids,
    )
    return FixFlowResult(
        workflow_run=updated_run,
        issue_id=normalized_issue_id,
        remediation_notes=(remediation_notes,),
        remediation_artifact_ids=remediation_artifact_ids,
    )


def attach_remediation_evidence(
    workflow_run: WorkflowRun,
    issue_id: str,
    evidence_artifact_ids: tuple[str, ...] | list[str],
) -> FixFlowResult:
    run = _require_fix_flow_run(workflow_run)
    normalized_issue_id = _require_issue_link(issue_id)
    evidence_ids = tuple(str(artifact_id) for artifact_id in evidence_artifact_ids)
    if normalized_issue_id not in run.issue_ids:
        raise ValueError("workflow_run must already be linked to issue_id.")
    if not evidence_ids:
        raise ValueError("evidence_artifact_ids must contain at least one artifact identifier.")
    updated_run = replace(run, output_artifact_ids=run.output_artifact_ids + evidence_ids)
    return FixFlowResult(
        workflow_run=updated_run,
        issue_id=normalized_issue_id,
        evidence_artifact_ids=evidence_ids,
    )


def mark_verification_pending(workflow_run: WorkflowRun, issue_id: str) -> FixFlowResult:
    run = _require_fix_flow_run(workflow_run)
    normalized_issue_id = _require_issue_link(issue_id)
    if normalized_issue_id not in run.issue_ids:
        raise ValueError("workflow_run must already be linked to issue_id.")
    transitioned_run = transition_workflow_state(run, "verification_pending", "Verification pending.")
    return FixFlowResult(workflow_run=transitioned_run, issue_id=normalized_issue_id)


def build_verification_result(
    issue_id: str,
    workflow_run_id: str,
    evidence_artifact_ids: tuple[str, ...] | list[str],
    verification_status: str,
    verifier: str,
    verification_reason: str,
) -> VerificationResult:
    normalized_issue_id = _require_issue_link(issue_id)
    if not workflow_run_id.strip():
        raise ValueError("workflow_run_id must be non-empty.")
    evidence_ids = tuple(str(artifact_id) for artifact_id in evidence_artifact_ids)
    if not evidence_ids:
        raise ValueError("evidence_artifact_ids must contain at least one artifact identifier.")
    if verification_status not in {"passed", "failed"}:
        raise ValueError("verification_status must be 'passed' or 'failed'.")
    if not verifier.strip():
        raise ValueError("verifier must be non-empty.")
    if not verification_reason.strip():
        raise ValueError("verification_reason must be non-empty.")
    return VerificationResult(
        issue_id=normalized_issue_id,
        workflow_run_id=workflow_run_id,
        evidence_artifact_ids=evidence_ids,
        verification_status=verification_status,
        verifier=verifier,
        verification_reason=verification_reason,
        verified_at=_utc_now(),
    )


def verify_resolution(
    workflow_run: WorkflowRun,
    issue_id: str,
    verification_result: VerificationResult,
) -> FixFlowResult:
    run = _require_fix_flow_run(workflow_run)
    normalized_issue_id = _require_issue_link(issue_id)
    if verification_result.issue_id != normalized_issue_id or verification_result.workflow_run_id != run.workflow_run_id:
        raise ValueError("verification_result must link the same issue_id and workflow_run_id.")
    if verification_result.verification_status == "passed":
        transitioned_run = transition_workflow_state(run, "resolution_verified", verification_result.verification_reason)
    else:
        transitioned_run = transition_workflow_state(run, "reopened", verification_result.verification_reason)
    return FixFlowResult(
        workflow_run=transitioned_run,
        issue_id=normalized_issue_id,
        evidence_artifact_ids=verification_result.evidence_artifact_ids,
        verification_result=verification_result,
    )


def close_fix_flow(workflow_run: WorkflowRun, issue_id: str, closure_reason: str) -> FixFlowResult:
    run = _require_fix_flow_run(workflow_run)
    normalized_issue_id = _require_issue_link(issue_id)
    if normalized_issue_id not in run.issue_ids:
        raise ValueError("workflow_run must already be linked to issue_id.")
    if run.workflow_state != "validated":
        raise ValueError("workflow_run must be in 'validated' before closure.")
    transitioned_run = transition_workflow_state(run, "completed", closure_reason)
    return FixFlowResult(workflow_run=transitioned_run, issue_id=normalized_issue_id)


def reopen_fix_flow(workflow_run: WorkflowRun, issue_id: str, reopen_reason: str) -> FixFlowResult:
    run = _require_fix_flow_run(workflow_run)
    normalized_issue_id = _require_issue_link(issue_id)
    if normalized_issue_id not in run.issue_ids:
        raise ValueError("workflow_run must already be linked to issue_id.")
    transitioned_run = transition_workflow_state(run, "reopened", reopen_reason)
    return FixFlowResult(workflow_run=transitioned_run, issue_id=normalized_issue_id)
