from __future__ import annotations

from gdc_adk.memory.context_store import get_context_block
from gdc_adk.memory.continuity import get_snapshot
from gdc_adk.workflows.agent_contracts import HandoffArtifact, HandoffValidationResult, validate_handoff_contract
from gdc_adk.workflows.state_machine import WorkflowRun


def _result(handoff_id: str, violations: tuple[str, ...], success_message: str, failure_message: str) -> HandoffValidationResult:
    is_valid = len(violations) == 0
    return HandoffValidationResult(
        handoff_id=handoff_id,
        status="valid" if is_valid else "invalid",
        is_valid=is_valid,
        violations=violations,
        message=success_message if is_valid else failure_message,
    )


def validate_handoff_artifacts(handoff_artifact: HandoffArtifact) -> HandoffValidationResult:
    try:
        validate_handoff_contract(handoff_artifact)
    except ValueError as exc:
        return HandoffValidationResult(
            handoff_id="unknown",
            status="invalid",
            is_valid=False,
            violations=("contract_invalid",),
            message=str(exc),
        )

    violations: list[str] = []
    if handoff_artifact.continuity_snapshot_id is not None and get_snapshot(handoff_artifact.continuity_snapshot_id) is None:
        violations.append("continuity_snapshot_missing")
    for context_block_id in handoff_artifact.context_block_ids:
        if get_context_block(context_block_id) is None:
            violations.append(f"context_block_missing:{context_block_id}")
    return _result(
        handoff_artifact.handoff_id,
        tuple(violations),
        "Handoff artifact references are valid.",
        "Handoff artifact references are invalid.",
    )


def validate_traceability_links(handoff_artifact: HandoffArtifact, workflow_run: WorkflowRun) -> HandoffValidationResult:
    if not isinstance(workflow_run, WorkflowRun):
        raise ValueError("workflow_run must be a WorkflowRun.")
    validate_handoff_contract(handoff_artifact)
    violations: list[str] = []
    if handoff_artifact.workflow_run_id != workflow_run.workflow_run_id:
        violations.append("workflow_run_mismatch")
    known_artifact_ids = set(workflow_run.input_artifact_ids + workflow_run.output_artifact_ids)
    for artifact_id in handoff_artifact.artifact_ids:
        if artifact_id not in known_artifact_ids:
            violations.append(f"artifact_link_missing:{artifact_id}")
    for issue_id in handoff_artifact.issue_ids:
        if issue_id not in workflow_run.issue_ids:
            violations.append(f"issue_link_missing:{issue_id}")
    for finding_id in handoff_artifact.finding_ids:
        if finding_id not in workflow_run.finding_ids:
            violations.append(f"finding_link_missing:{finding_id}")
    if handoff_artifact.continuity_snapshot_id is not None:
        snapshot_result = get_snapshot(handoff_artifact.continuity_snapshot_id)
        if snapshot_result is None or snapshot_result.snapshot is None:
            violations.append("continuity_snapshot_missing")
        elif snapshot_result.snapshot.workflow_run_id != workflow_run.workflow_run_id:
            violations.append("continuity_workflow_mismatch")
    return _result(
        handoff_artifact.handoff_id,
        tuple(violations),
        "Handoff traceability links are valid.",
        "Handoff traceability links are invalid.",
    )


def validate_review_requirements(handoff_artifact: HandoffArtifact, workflow_run: WorkflowRun) -> HandoffValidationResult:
    if not isinstance(workflow_run, WorkflowRun):
        raise ValueError("workflow_run must be a WorkflowRun.")
    validate_handoff_contract(handoff_artifact)
    violations: list[str] = []
    if handoff_artifact.review_required:
        if handoff_artifact.to_role != "reviewer":
            violations.append("review_target_must_be_reviewer")
        if handoff_artifact.from_role == handoff_artifact.to_role:
            violations.append("independent_review_required")
        if not handoff_artifact.validation_required:
            violations.append("validation_required_for_reviewable_handoff")
        if not handoff_artifact.artifact_ids:
            violations.append("reviewable_handoff_requires_artifact_linkage")
    if handoff_artifact.validation_required and workflow_run.workflow_state == "failed":
        violations.append("validation_cannot_complete_failed_workflow")
    return _result(
        handoff_artifact.handoff_id,
        tuple(violations),
        "Handoff satisfies review and validation requirements.",
        "Handoff violates review or validation requirements.",
    )
